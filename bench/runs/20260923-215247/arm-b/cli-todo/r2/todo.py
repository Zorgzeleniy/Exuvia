"""Minimal todo list CLI. Storage: todo.json in the current directory."""

import json
import sys
from pathlib import Path

STORE = Path("todo.json")


def load() -> list[dict]:
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def save(items: list[dict]) -> None:
    STORE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def resolve_index(arg: str, items: list[dict]) -> int:
    try:
        n = int(arg)
    except ValueError:
        n = 0
    if not 1 <= n <= len(items):
        print("no such item", file=sys.stderr)
        sys.exit(1)
    return n - 1


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print("usage: todo.py add TEXT | list | done N | remove N", file=sys.stderr)
        sys.exit(2)
    cmd, *args = argv[1:]

    if cmd == "add":
        if not args:
            print("usage: todo.py add TEXT", file=sys.stderr)
            sys.exit(2)
        items = load()
        items.append({"text": args[0], "done": False})
        save(items)
    elif cmd == "list":
        for i, item in enumerate(load(), 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
    elif cmd in ("done", "remove"):
        if not args:
            print(f"usage: todo.py {cmd} N", file=sys.stderr)
            sys.exit(2)
        items = load()
        i = resolve_index(args[0], items)
        if cmd == "done":
            items[i]["done"] = True
        else:
            del items[i]
        save(items)
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
