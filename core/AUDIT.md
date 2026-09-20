# Exuvia Audit Procedure

Audit standing instructions for prompt debt. **Do not rewrite anything in this phase.**

## Phase 0 — Inventory instruction surfaces

Find the user's persistent instruction files (existing files only — never invent paths):

- Claude Code: `CLAUDE.md` (user `~/.claude/CLAUDE.md`, project root, nested), `.claude/skills/*/SKILL.md`, `.claude/agents/*.md`, `.claude/settings.json` hooks, `.mcp.json`
- Codex: `~/.codex/AGENTS.md`, repo `AGENTS.md`, `~/.codex/skills/*/SKILL.md`, `~/.codex/prompts/*.md`, `[mcp_servers]` in `~/.codex/config.toml`
- omp: `~/.omp/agent/{AGENTS.md,RULES.md,skills/*/SKILL.md,managed-skills/*/SKILL.md,agents/*.md,rules/*.md}`, plus `~/.omp/profiles/*/agent/…`
- Cursor: `.cursorrules`, `.cursor/rules/*.mdc`
- OpenCode: `AGENTS.md`, `~/.config/opencode/`
- Universal: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`

Output a table: file · bytes · instruction-line count.

## Phase 1 — Deterministic pre-pass (no LLM judgment)

For every inventoried file compute:

1. Size and share of total corpus.
2. Absolute census: `grep -c -iE '\b(always|never|никогда|всегда|обязательно|strictly|extremely|thoroughly|carefully)\b'`
3. Cross-file duplicates: normalize instruction lines (lowercase, strip punctuation) for lines starting with `-|*|[0-9]+.`; `collections.Counter` — print every pair sharing a line, as `file A ↔ file B`.
4. Dead references: every `skill://name`, `@path`, agent name — verify the target exists.
5. Dated snapshots: regex `\d{4}-\d{2}-\d{2}` and version pins `\d+\.\d+(\.\d+)?` — list fact · date/version · age in days.
6. Few-shot blocks: output examples / mock reports (```-blocks > 10 lines with fabricated data).
7. Live MCP surfaces (requires python3): run `python <exuvia>/meters/mcp_footprint.py --out .exuvia/mcp_footprint.json`, where `<exuvia>` is the repo checkout or the installed engines dir (`~/.exuvia/engines`). Every configured MCP server contributes its tools payload (names + descriptions + inputSchemas) to EVERY session context — record per-server rows: server · tools · tokens · cold_ms. Treat each server as an instruction surface; a server whose tools no real session ever invokes is a disable candidate.

## Phase 2 — Categorization (if two fit, name the dominant one)

1. **INVARIANT** — a fact or constraint the model cannot know without this file (environment, routing, safety). Safety lines (secrets, access control, production, commit/push gates) are ALWAYS category 1 and are never proposed for deletion — only for dedup or relocation.
2. **TRAINED-DUPLICATE** — the model does this without the instruction (style, default formatting, well-known definitions and methods).
3. **RELIC** — written for an older model, a fixed bug, or a state that no longer exists (cross-check Phase 1, step 5: dates, versions, current environment).
4. **90%-RULE** — true most of the time but phrased as always/never → candidate for a conditional rewrite.
5. **CONFLICT** — contradicts or duplicates another line (cross-check Phase 1, step 3).

Recommendation, one phrase: keep / delete / rewrite-as-condition / merge-with `<file>`.

## Phase 3 — Report and decisions file

1. Write `.exuvia/report.md`: a section per file; rows: id · line (abridged) · category · recommendation · evidence (Phase 1 fact or inference marked `[INFERENCE]`).
2. Write `.exuvia/decisions.md`: same rows plus an empty `DECISION` column.
3. Print the summary (counts per category, top-3 findings) and STOP.

Do not propose a ready rewritten version. The user fills the DECISION column (yes / no / as-condition / keep) — decisions belong to the human.
