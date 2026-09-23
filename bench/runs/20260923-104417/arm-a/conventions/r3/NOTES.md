# Project Notes

Tutorial repo whose product is markdown, not an app: modules `01-` through `10-` in numbered learning order (do not reorganize), each a `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`). Supporting dirs: `scripts/` (validators and the EPUB builder), `02-memory/*.md` (CLAUDE.md templates users copy into their own projects), `openspec/` (spec-driven change proposals).

## Quality gate

```bash
pre-commit run --all-files
pytest scripts/tests/ -v
ruff check scripts/ && ruff format scripts/
mypy scripts/ --ignore-missing-imports
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/
```

Pre-commit runs 5 doc checks on `.md` changes (markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering) and also runs on commit; a failing check must be fixed, never bypassed. The EPUB build is CI-only, not a pre-commit hook, because it needs a local `mmdc` binary.

## Conventions

Internal links are relative (`01-slash-commands/README.md`), anchors as `#heading-name`; every code fence must declare a language; external URLs must be reachable and stable; Mermaid diagrams must parse. Commits follow `type(scope): subject` with the scope matching the module folder (e.g. `feat(slash-commands):`, `docs(memory):`, `fix(README):`). Activate `.venv` before running Python scripts.
