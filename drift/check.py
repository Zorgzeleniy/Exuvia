#!/usr/bin/env python3
"""exuvia drift check — deterministic facts-vs-environment diff.

Reads facts.toml (registry of environment facts with checkers), runs every
checker against the live machine, prints a status table, writes JSON, exits
non-zero when anything is STALE/ERROR. No LLM, no network, stdlib only.

Statuses: OK (check passes) · STALE (check fails — fact no longer true)
· UNVERIFIABLE (no check defined) · ERROR (checker itself broke).
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import subprocess
import sys
import tomllib
from pathlib import Path


def run_check(check: dict, base: Path) -> tuple[str, str]:
    t = check.get("type")
    try:
        if t is None:
            return "UNVERIFIABLE", "no check defined"
        if t == "file_exists":
            p = base / check["path"]
            return ("OK", str(p)) if p.exists() else ("STALE", f"missing: {p}")
        if t == "file_contains":
            p = base / check["path"]
            if not p.exists():
                return ("STALE", f"missing file: {p}")
            body = p.read_text(encoding="utf-8", errors="replace")
            return ("OK", "pattern found") if re.search(check["pattern"], body) \
                else ("STALE", "pattern not found")
        if t == "dir_glob":
            hits = list(base.glob(check["glob"]))
            return ("OK", f"{len(hits)} matches") if hits else ("STALE", "no matches")
        if t == "shell":
            r = subprocess.run(check["cmd"], shell=True, capture_output=True,
                               cwd=base, timeout=30)
            return ("OK" if r.returncode == 0 else "STALE",
                    f"exit={r.returncode}")
        if t == "port_open":
            host, port = check.get("host", "127.0.0.1"), int(check["port"])
            s = socket.socket()
            s.settimeout(3)
            try:
                s.connect((host, port))
                return ("OK", f"{host}:{port} open")
            except OSError:
                return ("STALE", f"{host}:{port} closed")
            finally:
                s.close()
        return ("ERROR", f"unknown check type: {t}")
    except Exception as e:
        return ("ERROR", f"{type(e).__name__}: {e}"[:120])


def main() -> int:
    ap = argparse.ArgumentParser(description="exuvia drift check")
    ap.add_argument("--facts", default=".exuvia/facts.toml")
    ap.add_argument("--base", default=".", help="dir against which relative paths resolve")
    ap.add_argument("--out", default=None, help="optional JSON output path")
    a = ap.parse_args()

    facts_path = Path(a.facts)
    base = Path(a.base).resolve()
    if not facts_path.exists():
        print(f"no facts registry at {facts_path} — run the exuvia-drift procedure "
              "(ingest) to create one", file=sys.stderr)
        return 2
    data = tomllib.loads(facts_path.read_text(encoding="utf-8"))
    registry = data.get("facts", {})

    rows = []
    for fid, spec in registry.items():
        status, detail = run_check(spec.get("check") or {}, base)
        rows.append({"id": fid, "status": status, "detail": detail,
                     "description": spec.get("description", "")})

    order = {"STALE": 0, "ERROR": 1, "UNVERIFIABLE": 2, "OK": 3}
    rows.sort(key=lambda r: (order[r["status"]], r["id"]))
    print("| status | fact | detail |")
    print("|---|---|---|")
    for r in rows:
        print(f"| {r['status']} | {r['id']} | {r['detail']} |")
    bad = [r for r in rows if r["status"] in ("STALE", "ERROR")]
    print(f"\n{len(rows) - len(bad)}/{len(rows)} facts OK · {len(bad)} need attention",
          file=sys.stderr)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
