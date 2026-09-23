#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json in the current directory."""

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
        sys.exit(f"error: {STORE} is not a JSON array")
    return data


def save(items: list[dict]) -> None:
    STORE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_index(arg: str, count: int) -> int:
    try:
        n = int(arg)
    except ValueError:
        sys.exit("no such item")
    if not 1 <= n <= count:
        sys.exit("no such item")
    return n - 1


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        sys.exit("usage: todo.py {add <text> | list | done <n> | remove <n>}")
    cmd = argv[1]
    items = load()

    if cmd == "add":
        if len(argv) < 3:
            sys.exit("usage: todo.py add <text>")
        items.append({"text": " ".join(argv[2:]), "done": False})
        save(items)
    elif cmd == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item.get("done") else " "
            print(f"{i}. [{mark}] {item.get('text', '')}")
    elif cmd in ("done", "remove"):
        if len(argv) < 3:
            sys.exit("usage: todo.py {done|remove} <n>")
        idx = parse_index(argv[2], len(items))
        if cmd == "done":
            items[idx]["done"] = True
            save(items)
        else:
            del items[idx]
            save(items)
    else:
        sys.exit(f"unknown command: {cmd}\nusage: todo.py {{add <text> | list | done <n> | remove <n>}}")


if __name__ == "__main__":
    main(sys.argv)
