# Project Notes

Organization and rules summarized from the repo's standing instructions (`CLAUDE.md` / `AGENTS.md`).

## Organization

- Documentation project organized into module folders (e.g. `01-slash-commands/`); the folder name is the commit scope.
- Internal links are relative paths (e.g. `01-slash-commands/README.md`); anchors use `#heading-name`.
- Commit format is `type(scope): subject` with types `feat`, `fix`, `docs`, `chore`, `refactor`, `test` (e.g. `docs(memory):`, `fix(README):`).

## Hard rules

- Never commit or push without an explicit user request; never add `Co-Authored-By: Claude` to a commit message.
- Activate a virtualenv before running Python scripts (check `venv/`, `.venv/`, `env/`):

```bash
source .venv/bin/activate
```

- Code fences must declare a language (`bash`, `python`, `json`, ...).
- External URLs must be reachable and stable — no ephemeral links.
- Small fixes take a minimal diff; do not rewrite a section to fix a typo.

## Quality gate

- Pre-commit checks: the cross-reference check fails when a code fence has no declared language.
- Mermaid diagrams must parse; validated pre-commit only when `mmdc` is installed, otherwise the check skips with a warning.
- A broken EPUB build usually means invalid Mermaid or a missing/failing `mmdc`.
