#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json in the current directory."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load():
    try:
        items = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    if not isinstance(items, list):
        sys.exit(f"{STORE}: corrupt store (expected a JSON array)")
    return items


def save(items):
    STORE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_index(arg, count):
    try:
        n = int(arg)
    except ValueError:
        sys.exit("no such item")
    if n < 1 or n > count:
        sys.exit("no such item")
    return n - 1


def cmd_add(args):
    items = load()
    items.append({"text": " ".join(args.text), "done": False})
    save(items)


def cmd_list(_args):
    for i, item in enumerate(items := load(), 1):
        mark = "x" if item["done"] else " "
        print(f"{i}. [{mark}] {item['text']}")


def cmd_done(args):
    items = load()
    items[parse_index(args.n, len(items))]["done"] = True
    save(items)


def cmd_remove(args):
    items = load()
    del items[parse_index(args.n, len(items))]
    save(items)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="CLI todo list stored in todo.json")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="append a new item")
    p.add_argument("text", nargs="+")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("list", help="print numbered items")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("done", help="mark item N as done (1-based)")
    p.add_argument("n")
    p.set_defaults(fn=cmd_done)

    p = sub.add_parser("remove", help="delete item N (1-based)")
    p.add_argument("n")
    p.set_defaults(fn=cmd_remove)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
