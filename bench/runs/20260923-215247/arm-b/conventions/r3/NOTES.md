# NOTES

## What this project is

A tutorial repo: the product is markdown, not an app. Content lives in numbered
modules `01-` through `10-` — the prefix is the learning order, never reorganize
it. Each module is a `README.md` plus copy-paste templates; `02-memory/` holds
CLAUDE.md templates users copy into their own projects; `scripts/` holds doc
validators and the EPUB builder; `openspec/` holds spec-driven proposals.

## Quality gate

The gate is `pre-commit run --all-files`; it also fires on commit via hooks:

```bash
pre-commit run --all-files
```

On `.md` changes it runs five doc checks — markdown-lint, cross-references,
mermaid-syntax, link-check, markdown-rendering — all must pass. Python tooling
adds pytest, ruff, mypy, bandit. The EPUB build (`uv run scripts/build_epub.py`)
is CI-only: it needs a local `mmdc` binary (no working arm64 build).

## Hard conventions

- Commits follow `type(scope): subject`, scope matching the module folder
  (e.g. `docs(memory):`, `fix(README):`). Never commit or push without an
  explicit request; never add `Co-Authored-By: Claude`.
- Code fences must declare a language — the cross-reference check fails
  otherwise. Internal links are relative; anchors use `#heading-name`.
- External URLs must be reachable and stable; activate `.venv` before Python
  scripts; if a check fails, fix the cause — never bypass with `--no-verify`.
