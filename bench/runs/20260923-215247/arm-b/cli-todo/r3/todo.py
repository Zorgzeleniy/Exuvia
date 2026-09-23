#!/usr/bin/env python3
"""Minimal CLI todo app. Storage: todo.json in the current directory."""

import argparse
import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    if not isinstance(data, list):
        raise SystemExit(f"{STORE}: expected a JSON array")
    return data


def save(items: list[dict]) -> None:
    STORE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_index(items: list[dict], num: str) -> int:
    try:
        i = int(num) - 1
    except ValueError:
        print("no such item", file=sys.stderr)
        raise SystemExit(1)
    if not 0 <= i < len(items):
        print("no such item", file=sys.stderr)
        raise SystemExit(1)
    return i


def cmd_add(args: argparse.Namespace) -> None:
    items = load()
    items.append({"text": args.text, "done": False})
    save(items)


def cmd_list(_args: argparse.Namespace) -> None:
    for n, item in enumerate(load(), start=1):
        mark = "x" if item["done"] else " "
        print(f"{n}. [{mark}] {item['text']}")


def cmd_done(args: argparse.Namespace) -> None:
    items = load()
    items[check_index(items, args.num)]["done"] = True
    save(items)


def cmd_remove(args: argparse.Namespace) -> None:
    items = load()
    del items[check_index(items, args.num)]
    save(items)


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI todo list")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="append a new item")
    p.add_argument("text")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="print numbered items")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("done", help="mark an item as done (1-based)")
    p.add_argument("num")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("remove", help="delete an item (1-based)")
    p.add_argument("num")
    p.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
