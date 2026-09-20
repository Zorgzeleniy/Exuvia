#!/usr/bin/env python3
"""exuvia translator emit — mechanical placement of an instruction IR.

Input: IR jsonl, one entry per line:
  {"id": "r1", "text": "- ...", "kind": "safety|invariant|rule|fact",
   "source": "AGENTS.md:12", "assumes": ["f-x"], "dedup_of": null|"r0"}

Entries with dedup_of set are DROPPED (dedup was decided at IR authoring).
Placement per target:
  omp    -> RULES.md (safety) + AGENTS.md (invariant, rule, fact)
  claude -> CLAUDE.md (all, safety section first)
  codex  -> AGENTS.md (all, safety section first)
  cursor -> .cursorrules (all, safety section first)

Also writes translation-report.md: counts, dedups, source mapping.
Stdlib only; read-only except the --out dir.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

KIND_ORDER = ["safety", "invariant", "rule", "fact"]
TARGETS = {
    "omp": [("RULES.md", ["safety"]), ("AGENTS.md", ["invariant", "rule", "fact"])],
    "claude": [("CLAUDE.md", KIND_ORDER)],
    "codex": [("AGENTS.md", KIND_ORDER)],
    "cursor": [(".cursorrules", KIND_ORDER)],
}
KIND_HEADERS = {"safety": "Safety (non-negotiable)", "invariant": "Environment invariants",
                "rule": "Rules", "fact": "Facts"}


def load_ir(path: Path) -> tuple[list[dict], list[dict]]:
    kept, dropped = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        (dropped if e.get("dedup_of") else kept).append(e)
    return kept, dropped


def emit(kept: list[dict], target: str, out: Path, name: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for fname, kinds in TARGETS[target]:
        sections = []
        for kind in kinds:
            rows = [e for e in kept if e.get("kind") == kind]
            if not rows:
                continue
            body = "\n".join(e["text"].rstrip() for e in rows)
            srcs = ", ".join(sorted({e.get("source", "?").split(":")[0] for e in rows}))
            sections.append(f"## {KIND_HEADERS[kind]}\n\n{body}\n\n<!-- sources: {srcs} -->")
        if not sections:
            continue
        content = f"# {name} — translated from source corpus (exuvia)\n\n" + "\n\n".join(sections)
        (out / fname).write_text(content, encoding="utf-8")
        print(f"  wrote {out / fname} ({len(sections)} section(s))")


def report(kept: list[dict], dropped: list[dict], target: str, out: Path) -> None:
    lines = [f"# Translation report — target: {target}",
             "", f"- translated: {len(kept)} entries",
             f"- deduplicated away: {len(dropped)}"]
    for d in dropped:
        lines.append(f"  - `{d['id']}` duplicate of `{d['dedup_of']}`")
    lines += ["", "| id | kind | source |", "|---|---|---|"]
    for e in kept:
        lines.append(f"| {e['id']} | {e.get('kind')} | {e.get('source', '?')} |")
    (out / "translation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote {out / 'translation-report.md'}")


def main() -> int:
    ap = argparse.ArgumentParser(description="exuvia translator emit")
    ap.add_argument("--ir", required=True)
    ap.add_argument("--target", required=True, choices=sorted(TARGETS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", default="Agent instructions")
    a = ap.parse_args()
    kept, dropped = load_ir(Path(a.ir))
    kinds = {k: sum(1 for e in kept if e.get("kind") == k) for k in KIND_ORDER}
    print(f"IR: {len(kept)} entries kept, {len(dropped)} dedup-dropped "
          f"(safety={kinds['safety']} invariant={kinds['invariant']} "
          f"rule={kinds['rule']} fact={kinds['fact']})")
    emit(kept, a.target, Path(a.out), a.name)
    report(kept, dropped, a.target, Path(a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
