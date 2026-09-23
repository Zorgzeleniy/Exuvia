# NOTES

Summary of the project's standing instructions (CLAUDE.md / AGENTS.md).

## Organization

- Markdown documentation project organized into module folders; the `scope` in a
  commit message must match the module folder touched (e.g. `slash-commands`,
  `memory`, `README`).
- Pages cross-link via relative paths (e.g. `01-slash-commands/README.md`) with
  `#heading-name` anchors; external URLs must be reachable and stable.
- Diagrams are Mermaid; Python helper scripts run only inside an activated
  virtualenv (`venv/`, `.venv/`, or `env/`).

## Quality gate

- Enforced at pre-commit (runs on commit):
  - Mermaid diagrams must parse; the check skips with a warning when `mmdc`
    is not installed.
  - Code fences must declare a language (`bash`, `python`, `json`, ...) — the
    cross-reference check fails otherwise.
- Commit messages follow `type(scope): subject`; never add
  `Co-Authored-By: Claude`, and never commit or push without explicit request.
