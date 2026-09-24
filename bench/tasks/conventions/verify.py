#!/usr/bin/env python3
"""Verifier: checks artifacts against conventions.json in the working dir."""
import json
import re
import sys
from pathlib import Path

CONV = json.loads(Path("conventions.json").read_text(encoding="utf-8"))


def main() -> int:
    fails = []
    msg = Path("COMMIT_MSG.txt").read_text(encoding="utf-8", errors="replace").strip()
    if not re.match(CONV["commit_regex"], msg):
        fails.append(f"commit format: {msg[:50]!r}")
    notes_p = Path("NOTES.md")
    if not notes_p.exists():
        print("FAIL: NOTES.md missing"); return 1
    notes = notes_p.read_text(encoding="utf-8", errors="replace")
    lines = notes.splitlines()
    if not (10 <= len([l for l in lines if l.strip()]) <= 25): fails.append("length 10-25")
    for rule in CONV.get("file_rules", []):
        if rule == "eof_newline" and not notes.endswith("\n"): fails.append("no EOF newline")
        if rule == "no_trailing_ws" and any(l != l.rstrip() for l in lines): fails.append("trailing whitespace")
    if "fences_declare_language" in CONV.get("file_rules", []):
        in_fence = False
        for line in lines:
            s = line.strip()
            if s.startswith("```"):
                if in_fence:
                    in_fence = False
                else:
                    in_fence = True
                    if s == "```":
                        fails.append("code fence without language"); break
    if CONV.get("must_mention") and CONV["must_mention"] not in notes:
        fails.append(f"must mention: {CONV['must_mention']}")
    if fails:
        print("FAIL:", ", ".join(fails[:4])); return 1
    print("PASS: conventions followed (commit format, markdown rules)"); return 0


if __name__ == "__main__":
    sys.exit(main())
