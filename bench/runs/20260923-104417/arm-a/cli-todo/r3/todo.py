#!/usr/bin/env python3
"""Minimal CLI todo list. Items are stored in todo.json in the current directory."""

import argparse
import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load_items() -> list[dict]:
    """Return the stored items, or [] if the store does not exist yet."""
    try:
        items = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        sys.exit(f"error: {STORE} is not valid JSON: {exc}")
    if not isinstance(items, list):
        sys.exit(f"error: {STORE} must contain a JSON array")
    return items


def save_items(items: list[dict]) -> None:
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="todo.py", description="Minimal CLI todo list."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="append a new item")
    p_add.add_argument("text", help="item text")

    sub.add_parser("list", help="print numbered items")

    p_done = sub.add_parser("done", help="mark an item as done (1-based)")
    p_done.add_argument("number", type=int, help="item number")

    p_remove = sub.add_parser("remove", help="delete an item (1-based)")
    p_remove.add_argument("number", type=int, help="item number")

    args = parser.parse_args()
    items = load_items()

    if args.command == "add":
        items.append({"text": args.text, "done": False})
        save_items(items)
    elif args.command == "list":
        for i, item in enumerate(items, 1):
            print(f"{i}. [{'x' if item.get('done') else ' '}] {item['text']}")
    else:  # done / remove
        if not 1 <= args.number <= len(items):
            print("no such item", file=sys.stderr)
            sys.exit(1)
        if args.command == "done":
            items[args.number - 1]["done"] = True
        else:
            del items[args.number - 1]
        save_items(items)


if __name__ == "__main__":
    main()
