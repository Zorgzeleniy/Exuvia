"""Small CLI todo app. Storage: todo.json in the current directory."""

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
    STORE.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv):
    if len(argv) < 2:
        print("usage: todo.py {add|list|done|remove} [args]", file=sys.stderr)
        return 1
    cmd, *args = argv[1:]
    items = load()

    if cmd == "add":
        if not args:
            print("usage: todo.py add <text>", file=sys.stderr)
            return 1
        items.append({"text": " ".join(args), "done": False})
        save(items)
    elif cmd == "list":
        for i, item in enumerate(items, 1):
            mark = "x" if item["done"] else " "
            print(f"{i}. [{mark}] {item['text']}")
    elif cmd in ("done", "remove"):
        if not args or not args[0].lstrip("-").isdigit():
            print("usage: todo.py %s <number>" % cmd, file=sys.stderr)
            return 1
        n = int(args[0])
        if not 1 <= n <= len(items):
            print("no such item", file=sys.stderr)
            return 1
        if cmd == "done":
            items[n - 1]["done"] = True
            save(items)
        else:
            del items[n - 1]
            save(items)
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
