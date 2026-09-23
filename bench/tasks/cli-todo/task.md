Create a small Python CLI todo application in `todo.py` (current directory). No external dependencies, Python 3.11+.

Commands (argparse or plain argv — your choice, but the exact interface below must work):

```
python todo.py add "buy milk"     # append a new item
python todo.py list               # print numbered items, done items prefixed with [x], open with [ ]
python todo.py done 2             # mark item #2 as done (1-based)
python todo.py remove 1           # delete item #1 (1-based)
```

Storage: `todo.json` in the current directory — a JSON array of objects `{"text": str, "done": bool}`, in insertion order. `list` output for two open items and one done item must look like:

```
1. [ ] buy milk
2. [x] wash dishes
3. [ ] call mom
```

Edge cases: `done`/`remove` with an out-of-range number print `no such item` to stderr and exit code 1; `list` on an empty store prints nothing and exits 0.
