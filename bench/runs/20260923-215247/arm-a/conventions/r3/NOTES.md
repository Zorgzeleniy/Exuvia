# Project Notes

Tutorial repo — the product is markdown, not an app: numbered modules `01-` through `10-`, where the prefix is the curriculum order (never reorganize).

## Organization

- Each module folder: `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`).
- `scripts/` — utilities only (EPUB builder, link/mermaid/cross-ref validators), not the product.
- `02-memory/*.md` — CLAUDE.md templates users copy into their own projects; don't confuse with this file.
- `openspec/` — spec-driven change proposals; `.claude/CLAUDE.md` and `STYLE_GUIDE.md` hold stack/commands and lesson structure.

## Quality gate

```bash
pre-commit run --all-files
```

Runs on commit via pre-commit hooks; five doc checks on `.md` changes — markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering — all must pass. Fix failures at the source, never bypass with `--no-verify`.

Python tests and tooling:

```bash
pytest scripts/tests/ -v
ruff check scripts/ && ruff format scripts/
mypy scripts/ --ignore-missing-imports
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/
```

The EPUB build (`uv run scripts/build_epub.py`) is CI-only — it needs a local `mmdc` binary with no working arm64 build, so it is not a pre-commit hook.

## Commit conventions

- Format is `type(scope): subject`; the scope matches the touched module folder (e.g. `docs(memory):`) or the root-doc filename (e.g. `docs(notes):`).
- Internal links are relative (e.g. `01-slash-commands/README.md`); every code fence declares a language.
- No commit or push without an explicit user request; never add `Co-Authored-By: Claude`.
