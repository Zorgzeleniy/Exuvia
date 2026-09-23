#!/usr/bin/env python3
"""Tiny CLI todo app. Storage: todo.json (JSON array of {"text": str, "done": bool})."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")

USAGE = """\
usage: python todo.py <command> [args]

commands:
  add "text"     append a new item
  list           print numbered items ([x] done, [ ] open)
  done N         mark item N as done (1-based)
  remove N       delete item N (1-based)
"""


def load():
    try:
        with STORE.open(encoding="utf-8") as f:
            items = json.load(f)
        return items if isinstance(items, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        sys.exit(f"error: {STORE} is not valid JSON")


def save(items):
    with STORE.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main(argv):
    if not argv:
        sys.stderr.write(USAGE)
        return 2
    cmd, *args = argv

    if cmd == "add":
        if not args:
            sys.stderr.write('usage: python todo.py add "text"\n')
            return 2
        items = load()
        items.append({"text": " ".join(args), "done": False})
        save(items)
        return 0

    if cmd == "list":
        for i, item in enumerate(load(), 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
        return 0

    if cmd in ("done", "remove"):
        items = load()
        try:
            n = int(args[0])
            if not 1 <= n <= len(items):
                raise IndexError
        except (IndexError, ValueError):
            print("no such item", file=sys.stderr)
            return 1
        if cmd == "done":
            items[n - 1]["done"] = True
        else:
            del items[n - 1]
        save(items)
        return 0

    sys.stderr.write(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
