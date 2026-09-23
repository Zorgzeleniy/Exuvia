# Project Notes

Markdown-first tutorial repo — the product is the docs, not an app: numbered module folders `01-` through `10-`, where the prefix is the curriculum order (never reorganize).

## Organization

- Each module folder: a `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`).
- `scripts/` is support tooling (EPUB builder, link/mermaid/cross-ref validators), not the product.
- `02-memory/*.md` are CLAUDE.md templates users copy into their own projects.
- `openspec/` holds spec-driven change proposals; `.claude/CLAUDE.md` and `STYLE_GUIDE.md` carry stack commands and lesson-structure rules.

## Quality gate

```bash
pre-commit run --all-files
```

Runs on every commit via hooks; on `.md` changes it runs five doc checks — markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering — and all must pass. Fix failures at the source, never bypass with `--no-verify`. Python tooling:

```bash
pytest scripts/tests/ -v
ruff check scripts/ && ruff format scripts/
mypy scripts/ --ignore-missing-imports
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/
```

The EPUB build (`uv run scripts/build_epub.py`) is CI-only — it needs a local `mmdc` binary with no working arm64 build, so it is not a pre-commit hook.

## Conventions

- Internal links are relative (e.g. `01-slash-commands/README.md`); every code fence declares its language.
- Commits follow `type(scope): subject`; the scope matches the touched module folder (e.g. `docs(memory):`) or the root-doc filename (e.g. `docs(notes):`).
- No commit or push without an explicit user request; never add `Co-Authored-By: Claude`.
