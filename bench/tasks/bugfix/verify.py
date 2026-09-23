#!/usr/bin/env python3
"""Verifier: hidden assertions on the fixed calc.py (edge cases + API preserved).
Runs against the CURRENT working directory (the agent's workdir)."""
import inspect
import os
import sys

sys.path.insert(0, os.getcwd())


def main() -> int:
    try:
        import calc
        p = list(inspect.signature(calc.running_sum).parameters)
        if p != ["nums"]:
            print("FAIL: signature changed"); return 1
    except Exception as e:
        print("FAIL: import/signature:", e); return 1

    fails = []
    cases = [([], []), ([1], [1]), ([1, 2], [1, 3]), ([1, 2, 3], [1, 3, 6]),
             ([-1, 5], [-1, 4]), ([0, 0, 0], [0, 0, 0]), ([2.5, 2.5], [2.5, 5.0])]
    for inp, want in cases:
        try:
            got = calc.running_sum(list(inp))
            if got != want:
                fails.append(f"{inp} -> {got} != {want}")
        except Exception as e:
            fails.append(f"{inp} raised {type(e).__name__}")

    if fails:
        print("FAIL:", "; ".join(fails[:4])); return 1
    print("PASS: running_sum correct on all edge cases, signature intact"); return 0


if __name__ == "__main__":
    sys.exit(main())
