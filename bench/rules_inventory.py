#!/usr/bin/env python3
"""Rules-inventory scorer: how many corpus rules does each conventions artifact satisfy,
and how many corpus topics surface in the NOTES.md summary (grounding).

Usage:
  python bench/rules_inventory.py --config bench/configs/<name> --run bench/runs/<ts>

Scores every arm-*/conventions/r*/ NOTES.md + COMMIT_MSG.txt against the config's
inventory.json: binary "rules" (hard requirements) + "topics" (corpus facts a
grounded summary would mention). Deterministic, no LLM.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path


def score_artifact(rule: dict, notes: str, commit: str, commit_regex: str) -> bool:
    c = rule["check"]
    if c == "commit_regex":
        return bool(re.match(commit_regex, commit))
    if c == "commit_has":
        return rule["substr"].lower() in commit.lower()
    if c == "commit_absent":
        return rule["substr"].lower() not in commit.lower()
    if c == "commit_words":
        desc = commit.split(":", 1)[-1] if ":" in commit else commit
        return len(desc.split()) >= rule.get("min", 4)
    if c == "notes_has":
        return rule["substr"].lower() in notes.lower()
    if c == "fences_language":
        inf = False
        for line in notes.splitlines():
            s = line.strip()
            if s.startswith("```"):
                if inf:
                    inf = False
                else:
                    inf = True
                    if s == "```":
                        return False
        return True
    if c == "eof":
        return notes.endswith("\n")
    if c == "no_ws":
        return all(l == l.rstrip() for l in notes.splitlines())
    if c == "notes_len":
        n = len([l for l in notes.splitlines() if l.strip()])
        return rule.get("min", 10) <= n <= rule.get("max", 25)
    raise ValueError(f"unknown check: {c}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    cfg, run = Path(a.config), Path(a.run)
    inv = json.loads((cfg / "inventory.json").read_text(encoding="utf-8"))
    commit_regex = json.loads((cfg / "conventions.json").read_text(encoding="utf-8"))["commit_regex"]
    rules, topics = inv["rules"], inv.get("topics", [])

    print(f"# rules inventory — {cfg.name} / {run.name}")
    rows = {r["id"]: {arm: [0, 0] for arm in ("a", "b")} for r in rules}  # [satisfied, total]
    per_rules = {arm: [] for arm in ("a", "b")}
    per_topics = {arm: [] for arm in ("a", "b")}

    for arm in ("a", "b"):
        for d in sorted((run / f"arm-{arm}" / "conventions").glob("r*")):
            notes_p, commit_p = d / "NOTES.md", d / "COMMIT_MSG.txt"
            if not (notes_p.exists() and commit_p.exists()):
                per_rules[arm].append(0)
                per_topics[arm].append(0)
                continue
            notes = notes_p.read_text(encoding="utf-8", errors="replace")
            commit = commit_p.read_text(encoding="utf-8", errors="replace").strip()
            hits = 0
            for rule in rules:
                ok = score_artifact(rule, notes, commit, commit_regex)
                rows[rule["id"]][arm][1] += 1
                rows[rule["id"]][arm][0] += ok
                hits += ok
            per_rules[arm].append(hits)
            per_topics[arm].append(sum(1 for t in topics if t.lower() in notes.lower()))

    print("| rule | arm a | arm b |")
    print("|---|---:|---:|")
    for rid, arms in rows.items():
        print(f"| {rid} | {arms['a'][0]}/{arms['a'][1]} | {arms['b'][0]}/{arms['b'][1]} |")
    rm = {arm: sum(v) / len(v) for arm, v in per_rules.items() if v}
    print(f"\nhard rules satisfied per artifact (of {len(rules)}): A={rm.get('a', 0):.1f} · B={rm.get('b', 0):.1f}")
    if topics:
        tm = {arm: sum(v) / len(v) for arm, v in per_topics.items() if v}
        rel = (tm["b"] - tm["a"]) / tm["a"] * 100 if tm.get("a") else 0.0
        print(f"corpus-topic grounding in NOTES.md (of {len(topics)}): "
              f"A={tm.get('a', 0):.1f} · B={tm.get('b', 0):.1f} ({rel:+.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
