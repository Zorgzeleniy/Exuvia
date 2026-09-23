#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json (JSON array) in the current directory."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list:
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def save(items: list) -> None:
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def die() -> int:
    print("no such item", file=sys.stderr)
    return 1


def main(argv: list) -> int:
    if not argv:
        print("usage: todo.py add TEXT | list | done N | remove N", file=sys.stderr)
        return 1

    cmd, *rest = argv

    if cmd == "add":
        if not rest:
            print("usage: todo.py add TEXT", file=sys.stderr)
            return 1
        items = load()
        items.append({"text": " ".join(rest), "done": False})
        save(items)
        return 0

    if cmd == "list":
        for i, item in enumerate(load(), 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
        return 0

    if cmd in ("done", "remove"):
        try:
            n = int(rest[0])
        except (IndexError, ValueError):
            return die()
        items = load()
        if not 1 <= n <= len(items):
            return die()
        if cmd == "done":
            items[n - 1]["done"] = True
        else:
            del items[n - 1]
        save(items)
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
