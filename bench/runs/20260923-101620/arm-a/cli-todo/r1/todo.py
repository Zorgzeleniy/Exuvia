#!/usr/bin/env python3
"""Minimal CLI todo list.

Usage:
    python todo.py add "buy milk"
    python todo.py list
    python todo.py done 2
    python todo.py remove 1

Items are stored as a JSON array of {"text": str, "done": bool} in
todo.json in the current directory, in insertion order.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load_items() -> list[dict]:
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        print(f"error: {STORE} is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(1)


def save_items(items: list[dict]) -> None:
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def parse_index(arg: str, count: int) -> int | None:
    """Return the 0-based index for a 1-based item number, or None if invalid."""
    try:
        number = int(arg)
    except ValueError:
        return None
    if not 1 <= number <= count:
        return None
    return number - 1


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: todo.py {add TEXT | list | done N | remove N}", file=sys.stderr)
        return 1

    command, *args = argv
    items = load_items()

    if command == "add":
        if not args:
            print("usage: todo.py add TEXT", file=sys.stderr)
            return 1
        items.append({"text": " ".join(args), "done": False})
        save_items(items)
    elif command == "list":
        for number, item in enumerate(items, start=1):
            mark = "x" if item["done"] else " "
            print(f"{number}. [{mark}] {item['text']}")
    elif command in ("done", "remove"):
        index = parse_index(args[0], len(items)) if args else None
        if index is None:
            print("no such item", file=sys.stderr)
            return 1
        if command == "done":
            items[index]["done"] = True
        else:
            del items[index]
        save_items(items)
    else:
        print(f"unknown command: {command}", file=sys.stderr)
        print("usage: todo.py {add TEXT | list | done N | remove N}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
