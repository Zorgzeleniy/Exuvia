"""Minimal CLI todo app. Storage: todo.json in the current directory."""

import argparse
import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    if not STORE.exists():
        return []
    with STORE.open(encoding="utf-8") as f:
        return json.load(f)


def save(items: list[dict]) -> None:
    with STORE.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")


def cmd_add(args: argparse.Namespace) -> None:
    items = load()
    items.append({"text": args.text, "done": False})
    save(items)


def cmd_list(_args: argparse.Namespace) -> None:
    for i, item in enumerate(load(), 1):
        mark = "x" if item["done"] else " "
        print(f"{i}. [{mark}] {item['text']}")


def load_checked(args: argparse.Namespace) -> list[dict]:
    items = load()
    if not 1 <= args.number <= len(items):
        print("no such item", file=sys.stderr)
        sys.exit(1)
    return items


def cmd_done(args: argparse.Namespace) -> None:
    items = load_checked(args)
    items[args.number - 1]["done"] = True
    save(items)


def cmd_remove(args: argparse.Namespace) -> None:
    items = load_checked(args)
    del items[args.number - 1]
    save(items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal CLI todo app")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="append a new item")
    p.add_argument("text")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="print numbered items")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("done", help="mark item as done (1-based)")
    p.add_argument("number", type=int)
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("remove", help="delete an item (1-based)")
    p.add_argument("number", type=int)
    p.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
