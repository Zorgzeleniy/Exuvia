# Project Notes

- Standing instructions live in `CLAUDE.md` (hard rules + workflow preferences).
- Content is organized as numbered module folders (e.g. `01-slash-commands/`), each with its own README; the folder name is the commit scope.
- Docs are Markdown: internal links use relative paths (`01-slash-commands/README.md`) and `#heading-name` anchors; external URLs must be reachable and stable.
- Code fences must declare a language (`bash`, `python`, `json`, ...) or the cross-reference check fails.
- Diagrams are Mermaid and must parse (validated when `mmdc` is installed); a broken EPUB build usually means invalid Mermaid or a missing/failing `mmdc`.

## Quality gate

- Markdown changes are validated by pre-commit: cross-references, Mermaid syntax, and related checks.
- Full gate:

```bash
pre-commit run --all-files
```

- Never commit or push without explicit user request; never add `Co-Authored-By: Claude`.
- Activate `.venv` before running Python scripts; keep small fixes to a minimal diff.
- Commit format: `type(scope): subject`, scope matching the module folder (e.g. `docs(memory): ...`).
