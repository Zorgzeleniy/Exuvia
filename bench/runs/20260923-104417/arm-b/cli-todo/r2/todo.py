#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json (JSON array of {"text": str, "done": bool})."""

import argparse
import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    try:
        with STORE.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save(items: list[dict]) -> None:
    with STORE.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Tiny CLI todo list")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="append a new item")
    p_add.add_argument("text")

    sub.add_parser("list", help="print all items")

    for name, help_text in (("done", "mark item as done"), ("remove", "delete an item")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("number", type=int, help="1-based item number")

    args = parser.parse_args()
    items = load()

    if args.command == "add":
        items.append({"text": args.text, "done": False})
        save(items)
    elif args.command == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
    else:  # done | remove
        n = args.number
        if not 1 <= n <= len(items):
            print("no such item", file=sys.stderr)
            return 1
        if args.command == "done":
            items[n - 1]["done"] = True
        else:
            del items[n - 1]
        save(items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
