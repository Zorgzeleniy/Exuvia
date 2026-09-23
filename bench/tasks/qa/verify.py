#!/usr/bin/env python3
"""Verifier: substring markers per question, from qa.json in the working dir."""
import json
import re
import sys
from pathlib import Path

QA = json.loads(Path("qa.json").read_text(encoding="utf-8"))


def main() -> int:
    ans_p = Path("answers.txt")
    if not ans_p.exists():
        cands = sorted(Path(".").glob("*.txt"))
        if not cands:
            print("FAIL: no answers file"); return 1
        ans_p = cands[0]
    text = ans_p.read_text(encoding="utf-8", errors="replace")
    fails = []
    for q in QA:
        m = re.search(rf"^{q['n']}\.\s*(.+)$", text, re.M)
        if not m:
            fails.append(f"q{q['n']}: no numbered answer"); continue
        a = m.group(1)
        if not any(marker.lower() in a.lower() for marker in q["any_of"]):
            fails.append(f"q{q['n']}: marker missing ({a[:40]!r})")
    if fails:
        print("FAIL:", "; ".join(fails[:4])); return 1
    print("PASS: all five answers carry corpus-fact markers"); return 0


if __name__ == "__main__":
    sys.exit(main())
