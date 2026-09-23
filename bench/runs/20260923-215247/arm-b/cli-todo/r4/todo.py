#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json (JSON array) in the current directory."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")

USAGE = "usage: todo.py add TEXT | list | done N | remove N"


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def load() -> list[dict]:
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        fail(f"corrupt store: {STORE}")
    if not isinstance(data, list):
        fail(f"corrupt store: {STORE}")
    return data


def save(items: list[dict]) -> None:
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def parse_index(arg: str, items: list[dict]) -> int:
    try:
        n = int(arg)
    except ValueError:
        fail("no such item")
    if not 1 <= n <= len(items):
        fail("no such item")
    return n - 1


def main() -> None:
    argv = sys.argv[1:]
    if not argv:
        print(USAGE, file=sys.stderr)
        sys.exit(2)
    cmd, *rest = argv

    if cmd == "add":
        text = " ".join(rest).strip()
        if not text:
            fail("usage: todo.py add TEXT")
        items = load()
        items.append({"text": text, "done": False})
        save(items)

    elif cmd == "list":
        for i, item in enumerate(load(), 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")

    elif cmd in ("done", "remove"):
        if len(rest) != 1:
            fail(f"usage: todo.py {cmd} N")
        items = load()
        idx = parse_index(rest[0], items)
        if cmd == "done":
            items[idx]["done"] = True
        else:
            del items[idx]
        save(items)

    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
