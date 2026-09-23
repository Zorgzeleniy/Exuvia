# CLAUDE.md

## Hard rules

- **YOU MUST NOT commit or push without explicit user request.**
- **YOU MUST NOT add `Co-Authored-By: Claude`** to any commit message.
- Always activate `.venv` before running Python scripts (check `venv/`, `.venv/`, `env/`).
- Internal links use **relative paths** (e.g. `01-slash-commands/README.md`); anchors use `#heading-name`.
- Code fences **must** declare a language (`bash`, `python`, `json`, …) — the cross-reference check fails otherwise.
- Commit format: `type(scope): subject` where `scope` matches the module folder (e.g. `feat(slash-commands):`, `docs(memory):`, `fix(README):`).
- External URLs must be reachable and stable. No ephemeral links.
- Mermaid diagrams must parse (validated pre-commit, and only when `mmdc` is installed — the check skips with a warning otherwise). A broken EPUB build is usually invalid Mermaid or a missing/failing `mmdc`.

## Workflow preferences

- Small fixes → minimal diff. Don't rewrite a section to fix a typo.

## Token Efficiency
- Never re-read files you just wrote or edited. You know the contents.
- Never re-run commands to "verify" unless the outcome was uncertain.
- Don't echo back large blocks of code or file contents unless asked.
- Batch related edits into single operations. Don't make 5 edits when 1 handles it.
- Skip confirmations like "I'll continue..." Just do it.
- If a task needs 1 tool call, don't use 3. Plan before acting.
- Do not summarize what you just did unless the result is ambiguous or you need additional input.
