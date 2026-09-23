# Project Notes

Standing instructions live in `AGENTS.md`, organized into Hard rules, Workflow preferences, and Token efficiency. The project is documentation-centric: Markdown sources with relative internal links, Mermaid diagrams, and an EPUB build.

## Hard rules

- Never commit or push without an explicit user request.
- Never add `Co-Authored-By: Claude` to any commit message.
- Always activate the virtualenv (check `venv/`, `.venv/`, `env/`) before running Python scripts:

```bash
source .venv/bin/activate
```

- Internal links use relative paths (e.g. `01-slash-commands/README.md`; anchors: `#heading-name`); external URLs must be reachable and stable, no ephemeral links.

## Commit format

- Messages follow `type(scope): subject` with allowed types: feat, fix, docs, chore, refactor, test; scope is lowercase, subject non-empty.

## Quality gate

- Pre-commit checks enforce the markdown rules: every code fence must declare a language (`bash`, `python`, `json`, ...) or the cross-reference check fails; files end with a newline and carry no trailing whitespace.
- Mermaid diagrams must parse — validated pre-commit when `mmdc` is installed (skipped with a warning otherwise). A broken EPUB build usually means invalid Mermaid or a missing/failing `mmdc`.
