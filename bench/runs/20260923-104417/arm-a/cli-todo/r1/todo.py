#!/usr/bin/env python3
"""Tiny CLI todo app. Storage: todo.json (a JSON array) in the current directory."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    if not STORE.exists():
        return []
    with STORE.open(encoding="utf-8") as f:
        data = json.load(f)
    return [{"text": item["text"], "done": item["done"]} for item in data]


def save(items: list[dict]) -> None:
    with STORE.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: todo.py {add <text> | list | done <n> | remove <n>}", file=sys.stderr)
        return 1

    cmd, *args = argv[1:]

    if cmd == "add":
        text = " ".join(args)
        if not text:
            print("usage: todo.py add <text>", file=sys.stderr)
            return 1
        items = load()
        items.append({"text": text, "done": False})
        save(items)
        return 0

    if cmd == "list":
        for i, item in enumerate(load(), 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
        return 0

    if cmd in ("done", "remove"):
        if len(args) != 1 or not args[0].isdigit():
            print(f"usage: todo.py {cmd} <n>", file=sys.stderr)
            return 1
        n = int(args[0])
        items = load()
        if not 1 <= n <= len(items):
            print("no such item", file=sys.stderr)
            return 1
        if cmd == "done":
            items[n - 1]["done"] = True
        else:
            del items[n - 1]
        save(items)
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
