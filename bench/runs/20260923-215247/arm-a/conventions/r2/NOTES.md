# Project Notes

Tutorial repo — the product is markdown, not an app: numbered modules `01-` through `10-` where the prefix is the learning order (never reorganize).

## Organization

- Each module folder: `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`).
- `scripts/` — utilities only (EPUB builder, link/mermaid/cross-ref validators), not the product.
- `02-memory/*.md` — CLAUDE.md templates users copy into their own projects; don't confuse with this file.
- `openspec/` — spec-driven change proposals.

## Quality gate

```bash
pre-commit run --all-files
```

Runs on commit via pre-commit hooks; five doc checks on `.md` changes — markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering — and all must pass. Failing checks get fixed at the source, never bypassed with `--no-verify`.

The EPUB build (`uv run scripts/build_epub.py`) is CI-only — it needs a local `mmdc` binary with no working arm64 build, so it is not a pre-commit hook.

```bash
pytest scripts/tests/ -v
ruff check scripts/ && ruff format scripts/
mypy scripts/ --ignore-missing-imports
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/
```

## Conventions

- Internal links are relative (e.g. `01-slash-commands/README.md`); every code fence declares a language.
- Commit format is `type(scope): subject` with the scope matching the module folder (e.g. `docs(memory):`); root docs use the filename, e.g. `docs(notes): add project organization and quality gate summary`.
- No commit or push without an explicit user request; never add `Co-Authored-By: Claude`.
