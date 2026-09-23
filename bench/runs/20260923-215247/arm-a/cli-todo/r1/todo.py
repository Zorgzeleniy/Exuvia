"""Small file-backed todo CLI. Storage: todo.json in the current directory."""

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
    STORE.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def parse_index(arg: str, items: list[dict]) -> int:
    try:
        n = int(arg)
    except ValueError:
        fail(f"invalid item number: {arg!r}")
    if not 1 <= n <= len(items):
        fail("no such item")
    return n - 1


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        fail("usage: todo.py {add TEXT | list | done N | remove N}")

    cmd, *args = argv[1:]
    items = load()

    if cmd == "add":
        if not args:
            fail("usage: todo.py add TEXT")
        items.append({"text": " ".join(args), "done": False})
        save(items)
    elif cmd == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
    elif cmd == "done":
        i = parse_index(args[0] if args else "", items)
        items[i]["done"] = True
        save(items)
    elif cmd == "remove":
        i = parse_index(args[0] if args else "", items)
        del items[i]
        save(items)
    else:
        fail(f"unknown command: {cmd}")


if __name__ == "__main__":
    main(sys.argv)
