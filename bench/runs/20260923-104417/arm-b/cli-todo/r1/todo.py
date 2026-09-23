#!/usr/bin/env python3
"""Minimal CLI todo app backed by todo.json in the current directory."""

import argparse
import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load():
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def save(items):
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def index_arg(value):
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid index: {value!r}")


def resolve_index(items, number):
    if not 1 <= number <= len(items):
        print("no such item", file=sys.stderr)
        sys.exit(1)
    return number - 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Tiny todo list stored in todo.json")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="append a new item")
    p_add.add_argument("text")

    sub.add_parser("list", help="print numbered items")

    p_done = sub.add_parser("done", help="mark an item as done (1-based)")
    p_done.add_argument("index", type=index_arg)

    p_remove = sub.add_parser("remove", help="delete an item (1-based)")
    p_remove.add_argument("index", type=index_arg)

    args = parser.parse_args(argv)
    items = load()

    if args.command == "add":
        items.append({"text": args.text, "done": False})
        save(items)
    elif args.command == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
    elif args.command == "done":
        items[resolve_index(items, args.index)]["done"] = True
        save(items)
    elif args.command == "remove":
        del items[resolve_index(items, args.index)]
        save(items)


if __name__ == "__main__":
    main()
