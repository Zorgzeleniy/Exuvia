# Project notes

## Organization

- Markdown-first documentation project: content lives in numbered module folders (e.g. `01-slash-commands/`), each with its own `README.md`; the root `README.md` is treated like a module (`fix(README)`).
- The module folder name doubles as the commit scope for any change inside it (`docs(memory)`, `feat(slash-commands)`).
- Python scripts require an activated `.venv` (check `venv/`, `.venv/`, `env/` first).

## Quality gate

- Internal links use relative paths; anchors use `#heading-name`.
- External URLs must be reachable and stable — no ephemeral links.
- Every code fence declares a language — the cross-reference check fails otherwise.
- Mermaid diagrams must parse; they are validated pre-commit, but only when `mmdc` is installed — otherwise the check skips with a warning.
- A broken EPUB build usually means invalid Mermaid or a missing/failing `mmdc`.

## Commits

- Format: `type(scope): subject`, scope matching the module folder:

```text
feat(slash-commands): add retry example
docs(memory): clarify write tool usage
fix(README): correct broken anchor
```
