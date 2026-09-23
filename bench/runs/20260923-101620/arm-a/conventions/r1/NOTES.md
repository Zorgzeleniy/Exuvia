# Project Notes

## Organization

Tutorial repo: output is markdown in numbered modules `01-` through `10-`, not an app. The numbered prefix is learning order, not alphabetical; do not reorganize.

- Each module: `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`).
- `scripts/` holds utilities (EPUB builder, link/mermaid/cross-ref validators), not the product.
- `02-memory/*.md` are CLAUDE.md templates users copy into their own projects.
- `openspec/` holds spec-driven change proposals.

## Quality gate

```bash
pre-commit run --all-files
pytest scripts/tests/ -v
uv run scripts/build_epub.py
```

Pre-commit runs five doc checks on `.md` changes (markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering); all must pass.
Code fences must declare a language, internal links use relative paths, external URLs must be reachable and stable, and Mermaid must parse. The EPUB build runs in CI only — it needs a local `mmdc` binary on PATH.

## Hard rules

Commits follow `type(scope): subject` (e.g. `docs(memory): ...`). Never commit or push without an explicit user request; never add a `Co-Authored-By: Claude` trailer.
