#!/usr/bin/env python3
"""Small CLI todo app backed by todo.json in the current directory."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load_items():
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    if not isinstance(data, list):
        raise ValueError(f"{STORE} is not a JSON array")
    items = []
    for entry in data:
        items.append({"text": entry["text"], "done": bool(entry["done"])})
    return items


def save_items(items):
    STORE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_index(value):
    try:
        return int(value)
    except ValueError:
        print("no such item", file=sys.stderr)
        sys.exit(1)


def main(argv):
    if len(argv) < 2:
        print("usage: todo.py {add <text> | list | done <n> | remove <n>}", file=sys.stderr)
        return 1

    command, *args = argv[1:]
    items = load_items()

    if command == "add":
        if not args:
            print("usage: todo.py add <text>", file=sys.stderr)
            return 1
        items.append({"text": " ".join(args), "done": False})
        save_items(items)
        return 0

    if command == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
        return 0

    if command in ("done", "remove"):
        if not args:
            print("no such item", file=sys.stderr)
            return 1
        n = parse_index(args[0])
        if n < 1 or n > len(items):
            print("no such item", file=sys.stderr)
            return 1
        if command == "done":
            items[n - 1]["done"] = True
            save_items(items)
        else:
            del items[n - 1]
            save_items(items)
        return 0

    print(f"unknown command: {command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
