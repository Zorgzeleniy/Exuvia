# NOTES

## Organization

- Markdown documentation project: content lives in module folders such as
  `01-slash-commands/` and `02-memory/`, with README-centric pages like
  `01-slash-commands/README.md`.
- Pages cross-link via relative paths; anchors use `#heading-name`.
- Docs embed code samples and Mermaid diagrams, and build into an EPUB.
- Python tooling must run inside the project virtualenv: activate `.venv`
  (check `venv/`, `.venv/`, `env/`) before running scripts.

## Quality gate

- The cross-reference check fails any code fence that does not declare a
  language (`bash`, `python`, `json`, ...).
- Mermaid diagrams must parse: validated pre-commit, and only when `mmdc` is
  installed — the check skips with a warning otherwise; a broken EPUB build is
  usually invalid Mermaid or a missing/failing `mmdc`.
- Link hygiene: internal links relative, external URLs reachable and stable
  (no ephemeral links).
- Commits follow `type(scope): subject` with the scope matching the module
  folder (e.g. `feat(slash-commands):`, `docs(memory):`, `fix(README):`);
  never commit or push without an explicit user request and never add
  `Co-Authored-By: Claude`. Small fixes stay minimal-diff.
