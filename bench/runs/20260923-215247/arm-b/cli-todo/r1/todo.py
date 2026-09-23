#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json (JSON array of {"text": str, "done": bool})."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    if not STORE.exists():
        return []
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        sys.exit(f"error: cannot read {STORE}: {e}")
    if not isinstance(data, list):
        sys.exit(f"error: {STORE} is corrupt (expected a JSON array)")
    return data


def save(items: list[dict]) -> None:
    STORE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_index(arg: str, items: list[dict]) -> int:
    try:
        n = int(arg)
    except ValueError:
        sys.exit("no such item")
    if not 1 <= n <= len(items):
        sys.exit("no such item")
    return n - 1


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: todo.py add TEXT | list | done N | remove N")

    cmd, *rest = args
    items = load()

    if cmd == "add":
        text = " ".join(rest).strip()
        if not text:
            sys.exit("usage: todo.py add TEXT")
        items.append({"text": text, "done": False})
        save(items)
    elif cmd == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item.get("done") else " "
            print(f"{i}. [{mark}] {item.get('text', '')}")
    elif cmd in ("done", "remove"):
        if not rest:
            sys.exit("no such item")
        idx = parse_index(rest[0], items)
        if cmd == "done":
            items[idx]["done"] = True
            save(items)
        else:
            del items[idx]
            save(items)
    else:
        sys.exit(f"unknown command: {cmd}\nusage: todo.py add TEXT | list | done N | remove N")


if __name__ == "__main__":
    main()
