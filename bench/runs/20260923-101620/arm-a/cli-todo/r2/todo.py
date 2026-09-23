#!/usr/bin/env python3
"""Minimal CLI todo app.

Usage:
    python todo.py add "buy milk"
    python todo.py list
    python todo.py done 2
    python todo.py remove 1

Storage: todo.json in the current directory — a JSON array of
{"text": str, "done": bool} objects in insertion order.
"""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    try:
        items = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        sys.exit(f"corrupt store {STORE}: {exc}")
    if not isinstance(items, list):
        sys.exit(f"corrupt store {STORE}: expected a JSON array")
    return items


def save(items: list[dict]) -> None:
    STORE.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")


def parse_index(rest: list[str], items: list[dict]) -> int:
    """Turn 1-based argv number into a 0-based index; exit 1 if invalid."""
    try:
        n = int(rest[0])
    except (IndexError, ValueError):
        n = 0  # not a number -> falls through to "no such item"
    if not 1 <= n <= len(items):
        print("no such item", file=sys.stderr)
        sys.exit(1)
    return n - 1


def main() -> None:
    match sys.argv[1:]:
        case ["add", *text] if text:
            items = load()
            items.append({"text": " ".join(text), "done": False})
            save(items)
        case ["list"]:
            for i, item in enumerate(load(), 1):
                print(f"{i}. [{'x' if item['done'] else ' '}] {item['text']}")
        case ["done", *rest]:
            items = load()
            items[parse_index(rest, items)]["done"] = True
            save(items)
        case ["remove", *rest]:
            items = load()
            del items[parse_index(rest, items)]
            save(items)
        case _:
            sys.exit("usage: todo.py add TEXT | list | done N | remove N")


if __name__ == "__main__":
    main()
