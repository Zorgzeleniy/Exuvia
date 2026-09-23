#!/usr/bin/env python3
"""Verifier: drive the CLI end-to-end in the working dir. Deterministic, stdlib only."""
import json
import subprocess
import sys
from pathlib import Path


def run(*args):
    return subprocess.run([sys.executable, "todo.py", *args], capture_output=True,
                          text=True, timeout=30)


def main() -> int:
    fails = []

    r = run("add", "alpha")
    if r.returncode != 0: fails.append("add rc")
    run("add", "beta"); run("add", "gamma")
    data = json.loads(Path("todo.json").read_text())
    if [d["text"] for d in data] != ["alpha", "beta", "gamma"] or not all(d["done"] is False for d in data):
        fails.append("storage shape")

    r = run("list")
    lines = r.stdout.strip().splitlines()
    if not (len(lines) == 3 and lines[1].startswith("2. [ ]")): fails.append("list open")

    run("done", "2")
    r = run("list")
    if "2. [x] beta" not in r.stdout: fails.append("done marks [x]")
    data = json.loads(Path("todo.json").read_text())
    if data[1]["done"] is not True: fails.append("storage done flag")

    run("remove", "1")
    data = json.loads(Path("todo.json").read_text())
    if [d["text"] for d in data] != ["beta", "gamma"]: fails.append("remove")

    r = run("done", "9")
    if r.returncode == 0 or "no such item" not in (r.stderr or ""): fails.append("out-of-range")

    if fails:
        print("FAIL:", ", ".join(fails)); return 1
    print("PASS: cli-todo end-to-end"); return 0


if __name__ == "__main__":
    sys.exit(main())
