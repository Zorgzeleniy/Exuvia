# Project Notes

## Organization

- Modules `01-` through `10-` are the curriculum in learning order — never reorganize the numbering.
- Each module holds a `README.md` plus copy-paste templates (`.md`, `.json`, `.sh`).
- `scripts/` is tooling (CI-only EPUB builder, doc validators); `02-memory/*.md` are CLAUDE.md templates; `openspec/` holds change proposals.

## Quality gate

```bash
pre-commit run --all-files
```

Pre-commit runs 5 doc checks on `.md` changes: markdown-lint, cross-references, mermaid-syntax, link-check, markdown-rendering. Tests run separately:

```bash
pytest scripts/tests/ -v
```

## Conventions

- Internal links are relative paths; every code fence must declare a language.
- Commits follow `type(scope): subject`, scope = module folder (e.g. `docs(memory):`).
