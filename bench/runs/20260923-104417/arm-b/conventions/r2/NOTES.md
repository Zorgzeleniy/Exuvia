# Project Notes

## Organization

- Content is organized in module folders, each owning its own docs — e.g. numbered command modules like `01-slash-commands/` (each with a `README.md`) and `memory/`; the top-level `README.md` counts as its own module for commit scoping.
- Documentation is cross-linked Markdown: internal links use relative paths (`01-slash-commands/README.md`) with `#heading-name` anchors; external URLs must be reachable and stable — no ephemeral links.
- Diagrams are Mermaid; the docs build to an EPUB, so a broken build usually means invalid Mermaid or a missing/failing `mmdc`.
- Python scripts run only inside the project virtualenv — check `venv/`, `.venv/`, or `env/` and activate before use.

## Quality gate

Pre-commit validation enforces:

1. Cross-reference check — every internal link resolves, and every code fence declares a language; a fence without one fails the check.
2. Mermaid diagrams must parse — validated pre-commit when `mmdc` is installed, skipped with a warning otherwise.
3. Commit messages follow the `type(scope): subject` format, with `scope` matching the module folder:

```text
feat(slash-commands): add /plan command docs
docs(memory): restructure storage guide
fix(README): correct installation steps
```

4. House rules: never commit or push without an explicit request, never add `Co-Authored-By: Claude` trailers, and keep small fixes to a minimal diff.
