# NOTES

## Organization

- Markdown docs in module folders: commit `scope` must match the module folder
  (e.g. `slash-commands`, `memory`, or a root file such as `README`).
- Modules are README-centric (e.g. `01-slash-commands/README.md`) and cross-link
  via relative paths; anchors use `#heading-name`.
- Content mixes fenced code samples and Mermaid diagrams; the docs also build
  into an EPUB.
- Python tooling must run inside the project virtualenv: activate `.venv`
  (check `venv/`, `.venv/`, `env/`) before running scripts.

## Quality gate

- A cross-reference check fails any code fence that does not declare a language
  (`bash`, `python`, `json`, ...).
- Mermaid must parse: validated pre-commit, but only when `mmdc` is installed —
  the check skips with a warning otherwise. A broken EPUB build usually means
  invalid Mermaid or a missing/failing `mmdc`.
- Link hygiene: internal links relative, external URLs reachable and stable
  (no ephemeral links).
- Commits follow `type(scope): subject`; never commit/push without an explicit
  request and never add `Co-Authored-By: Claude`. Small fixes stay minimal-diff.
