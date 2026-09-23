# Project Notes

This repo is a tutorial, not an app: content lives in numbered modules
`01-` through `10-` (numbered by learning order — never reorganize), each
with a `README.md` and copy-paste templates. `scripts/` holds doc validators
and the EPUB builder; `openspec/` holds spec-driven change proposals.

## Quality gate

```bash
pre-commit run --all-files
```

Runs 5 doc checks (markdown-lint, cross-references, mermaid-syntax,
link-check, markdown-rendering); tests: `pytest scripts/tests/ -v`.
The EPUB build (`uv run scripts/build_epub.py`) is CI-only (needs `mmdc`).

## Standing rules

- Internal links use **relative** paths (e.g. `01-slash-commands/README.md`).
- Every code fence must declare a language (`bash`, `python`, `json`, ...).
- Never commit or push without an explicit user request, and never add a
  `Co-Authored-By: Claude` trailer to any commit message.
- Commit format: `type(scope): subject`, scope matching the module folder
  (e.g. `docs(memory): ...`). Fix failing checks; never bypass with `--no-verify`.
