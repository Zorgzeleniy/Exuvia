# Project Notes

## Organization

Standing instructions live in `CLAUDE.md` / `AGENTS.md`; corpus files (`conventions.json`, `qa.json`) pin the commit format, file rules, and gate checks.

- Never commit or push without an explicit user request; never add a `Co-Authored-By: Claude` trailer.
- Activate the virtual environment (check `venv/`, `.venv/`, `env/`) before running Python scripts:

```bash
source .venv/bin/activate
```

- Internal links use relative paths (e.g. `01-slash-commands/README.md`, anchors `#heading-name`); external URLs must be reachable and stable.
- Small fixes get a minimal diff; do not rewrite a section to fix a typo.

## Quality Gate

- Commit messages follow `type(scope): subject` with types `feat|fix|docs|chore|refactor|test` and scope `[a-z0-9-]+`.
- Code fences must declare a language (`bash`, `python`, `json`, ...); the cross-reference check fails otherwise.
- Mermaid diagrams must parse — validated pre-commit when `mmdc` is installed (skipped with a warning); a broken EPUB build usually means invalid Mermaid or failing `mmdc`.
- Files end with a newline and contain no trailing whitespace.
