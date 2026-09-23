#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json (JSON array) in the current directory."""

import argparse
import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    if not STORE.exists():
        return []
    return json.loads(STORE.read_text(encoding="utf-8"))


def save(items: list[dict]) -> None:
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI todo app")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="append a new item")
    p_add.add_argument("text")

    sub.add_parser("list", help="print numbered items")

    p_done = sub.add_parser("done", help="mark an item as done (1-based)")
    p_done.add_argument("number", type=int)

    p_remove = sub.add_parser("remove", help="delete an item (1-based)")
    p_remove.add_argument("number", type=int)

    args = parser.parse_args()

    if args.command == "add":
        items = load()
        items.append({"text": args.text, "done": False})
        save(items)
    elif args.command == "list":
        for i, item in enumerate(load(), 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
    else:  # done | remove
        items = load()
        if not 1 <= args.number <= len(items):
            print("no such item", file=sys.stderr)
            return 1
        if args.command == "done":
            items[args.number - 1]["done"] = True
        else:
            del items[args.number - 1]
        save(items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
