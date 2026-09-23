# NOTES

## Organization

- Tutorial repo: the product is markdown in numbered modules `01-` through `10-` (prefix = learning order, never reorganize), not an app.
- Each module: `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`).
- `scripts/` — doc validators and the EPUB builder; utilities, not the product.
- `openspec/` — spec-driven change proposals.

## Quality gate

Pre-commit is the gate; it runs on commit and covers `.md` changes:

```bash
pre-commit run --all-files
```

Five doc checks: markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering. All must pass; never bypass with `--no-verify`.

Tests, and the EPUB build (CI-only — needs a local `mmdc` binary):

```bash
pytest scripts/tests/ -v
uv run scripts/build_epub.py
```
