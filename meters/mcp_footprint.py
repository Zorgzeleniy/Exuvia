#!/usr/bin/env python3
"""exuvia meter: live MCP context footprint.

Connects to every MCP server in the discovered harness configs, performs the
initialize + tools/list handshake, and measures the exact payload that lands in
each session's context: tool names + descriptions + inputSchemas (compact JSON).

Tokens via tiktoken cl100k when available (approximation; every provider has its
own tokenizer), otherwise bytes/4 marked "approx".

Never writes configs. Expands ${VAR} header values at runtime, never prints them.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")

    def toks(b: bytes) -> tuple[int, bool]:
        return len(_enc.encode(b.decode("utf-8", "replace"), allowed_special="all")), False
except ImportError:
    def toks(b: bytes) -> tuple[int, bool]:
        return max(1, len(b) // 4), True  # rough approximation

HOME = Path.home()
INIT_PARAMS = {"protocolVersion": "2025-06-18", "capabilities": {},
               "clientInfo": {"name": "exuvia-meter", "version": "0.2.0"}}


def discover_configs(explicit: list[str] | None) -> list[tuple[str, Path]]:
    if explicit:
        return [("explicit", Path(p)) for p in explicit]
    found: list[tuple[str, Path]] = []
    candidates = [
        ("omp/default", HOME / ".omp/agent/mcp.json"),
        ("claude/global", HOME / ".claude.json"),
        ("claude/project", Path.cwd() / ".mcp.json"),
        ("codex/global", HOME / ".codex/config.toml"),
    ]
    import glob as _g
    for p in _g.glob(str(HOME / ".omp/profiles/*/agent/mcp.json")):
        candidates.append((f"omp/{Path(p).parts[-3]}", Path(p)))
    for label, p in candidates:
        if p.exists():
            found.append((label, p))
    return found


def load_servers(label: str, path: Path) -> dict[str, dict]:
    if path.suffix == ".toml":
        import tomllib
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        raw = data.get("mcp_servers") or {}
        return {n: {"type": "stdio", "command": c.get("command", ""), "args": c.get("args", []),
                    "env": c.get("env", {})} for n, c in raw.items()}
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = data.get("mcpServers") or data.get("mcp_servers") or {}
    return {n: dict(c) for n, c in raw.items()}


def _send(fd_in, payload: dict) -> None:
    fd_in.write((json.dumps(payload) + "\n").encode())
    fd_in.flush()


def _read_result(fd_out, want_id: int) -> dict:
    for line in fd_out:
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("id") == want_id:
            if "error" in msg:
                raise RuntimeError(str(msg["error"].get("message", "rpc error"))[:120])
            return msg.get("result") or {}
    raise RuntimeError("server closed stdout before answering")


def stdio_tools_sync(cfg: dict, timeout: float) -> tuple[list, int]:
    env = {**os.environ, **{k: v for k, v in (cfg.get("env") or {}).items()}}
    cmd, args = cfg.get("command", ""), [str(a) for a in (cfg.get("args") or [])]
    if sys.platform == "win32" and cmd in ("npx", "node"):
        cmd, args = "cmd", ["/c", cmd, *args]
    t0 = time.monotonic()
    p = subprocess.Popen([cmd, *args], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, env=env, cwd=cfg.get("cwd"))
    watchdog = threading.Timer(timeout, p.kill)
    watchdog.daemon = True
    watchdog.start()
    try:
        _send(p.stdin, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": INIT_PARAMS})
        _read_result(p.stdout, 1)
        # note: "notifications/initialized" deliberately not sent — some local
        # servers (e.g. patched crawl4ai-mcp) close stdout on unknown messages.
        _send(p.stdin, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        result = _read_result(p.stdout, 2)
        ms = int((time.monotonic() - t0) * 1000)
        return result.get("tools") or [], ms
    finally:
        watchdog.cancel()
        try:
            p.stdin.close()  # EOF: well-behaved servers exit on their own
        except Exception:
            pass
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()


def http_tools_sync(cfg: dict, timeout: float) -> tuple[list, int]:
    headers = {"Content-Type": "application/json", "Accept": "application/json",
               **{k: v for k, v in (cfg.get("headers") or {}).items()}}
    url = cfg.get("url", "")
    for k, v in list(headers.items()):
        if "${" in v:
            exp = os.path.expandvars(v)
            if exp == v:
                raise RuntimeError(f"env var not set for header '{k}'")
            headers[k] = exp
    t0 = time.monotonic()

    def post(payload: dict) -> dict:
        r = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))

    res = post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": INIT_PARAMS})
    sid = ((res.get("result") or {}).get("headers") or {}).get("mcp-session-id")
    if sid:
        headers["mcp-session-id"] = sid
    res2 = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    if "error" in res2:
        raise RuntimeError(str(res2["error"].get("message", "rpc error"))[:120])
    return (res2.get("result") or {}).get("tools") or [], int((time.monotonic() - t0) * 1000)


def measure_sync(label: str, name: str, cfg: dict, timeout: float) -> dict:
    row = {"harness": label, "server": name}
    try:
        if cfg.get("type") == "http":
            tools, ms = http_tools_sync(cfg, timeout)
        else:
            tools, ms = stdio_tools_sync(cfg, timeout)
        payload = json.dumps(
            [{"name": t.get("name", ""), "description": t.get("description") or "",
              "inputSchema": t.get("inputSchema") or {}} for t in sorted(tools, key=lambda x: x.get("name", ""))],
            separators=(",", ":"), sort_keys=True).encode()
        n, approx = toks(payload)
        descs = [len((t.get("description") or "").encode()) for t in tools]
        row.update({"tools": len(tools), "bytes": len(payload), "kb": round(len(payload) / 1024, 1),
                    "tokens": n, "tokens_approx": approx, "cold_ms": ms,
                    "desc_avg": sum(descs) // max(len(descs), 1)})
    except Exception as e:
        row["error"] = f"{type(e).__name__}: {e}"[:160]
    return row


async def amain(args: argparse.Namespace) -> int:
    jobs = []
    for label, path in discover_configs(args.config):
        try:
            servers = load_servers(label, path)
        except Exception as e:
            print(f"[{label}] config parse error: {e}", file=sys.stderr)
            continue
        for name, cfg in servers.items():
            jobs.append(asyncio.to_thread(measure_sync, label, name, cfg, args.timeout))
    rows = list(await asyncio.gather(*jobs)) if jobs else []
    rows.sort(key=lambda r: (r.get("harness", ""), -(r.get("bytes") or 0)))

    print("| harness | server | tools | schema | tokens | cold ms |")
    print("|---|---|---:|---:|---:|---:|")
    ok = 0
    for r in rows:
        if "error" in r:
            print(f"| {r['harness']} | {r['server']} | ERR | {r['error']} | | |", file=sys.stderr)
        else:
            mark = "~" if r["tokens_approx"] else ""
            print(f"| {r['harness']} | {r['server']} | {r['tools']} | {r['kb']} KB | {mark}{r['tokens']:,} | {r['cold_ms']} |")
            ok += 1
    if rows:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(".tmp")
        tmp.write_text(json.dumps({"generated": time.strftime("%Y-%m-%dT%H:%M:%S"), "rows": rows},
                                  indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(out)  # atomic
    print(f"\n{ok}/{len(rows)} servers measured · json: {args.out}", file=sys.stderr)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="exuvia MCP footprint meter")
    ap.add_argument("--config", action="append", help="explicit mcp config path (repeatable)")
    ap.add_argument("--out", default=".exuvia/mcp_footprint.json")
    ap.add_argument("--timeout", type=float, default=30.0)
    return asyncio.run(amain(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
