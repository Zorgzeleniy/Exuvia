# Project Notes

Markdown-first tutorial repo: content lives in numbered modules `01-` through `10-` (prefix = learning order, never reorganize), each a `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`). `scripts/` holds validators and the EPUB builder — support tooling, not the product. `02-memory/*.md` are CLAUDE.md templates for users; `openspec/` holds spec-driven change proposals.

## Quality gate

The gate is `pre-commit run --all-files` (also runs on every commit via hooks; bypassing with `--no-verify` is forbidden):

```bash
pre-commit run --all-files
pytest scripts/tests/ -v
ruff check scripts/ && ruff format scripts/
mypy scripts/ --ignore-missing-imports
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/
```

On `.md` changes pre-commit runs five doc checks — markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering — and all must pass. The EPUB build (`uv run scripts/build_epub.py`) is CI-only (`build-epub` job in `.github/workflows/test.yml`) because it needs a local `mmdc` binary with no working arm64 build.

## Standing conventions

- Internal links use relative paths (e.g. `01-slash-commands/README.md`); anchors use `#heading-name`.
- Every code fence declares its language (`bash`, `python`, `json`, …); Mermaid diagrams must parse.
- External URLs must be reachable and stable — no ephemeral links.
- Commits follow `type(scope): subject`, scope matching the module folder (e.g. `feat(slash-commands):`, `docs(memory):`).
- Small fixes stay minimal-diff; lesson edits follow `STYLE_GUIDE.md`; a failing check is fixed at the source, never bypassed.
