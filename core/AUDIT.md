# Exuvia Audit Procedure

Audit standing instructions for prompt debt. **Do not rewrite anything in this phase.**

## Phase 0 — Inventory instruction surfaces

**Scope rule: audit the CURRENT context, nothing else by default.** That means:
the active profile's own directories (for omp: the profile this session runs in —
read its `config.yml` `skills.customDirectories` to know what loads here), plus
project-local files in the working directory (repo `AGENTS.md`/`CLAUDE.md`,
.cursor/rules, .mcp.json). Other profiles, the global agent dir, and other
harnesses are OUT OF SCOPE unless the user explicitly asks for them — a sandbox
or profile session must never audit surfaces it does not own.

Find the user's persistent instruction files (existing files only — never invent paths):

- Claude Code: `CLAUDE.md` (user `~/.claude/CLAUDE.md`, project root, nested), `.claude/skills/*/SKILL.md`, `.claude/agents/*.md`, `.claude/settings.json` hooks, `.mcp.json`
- Codex: `~/.codex/AGENTS.md`, repo `AGENTS.md`, `~/.codex/skills/*/SKILL.md`, `~/.codex/prompts/*.md`, `[mcp_servers]` in `~/.codex/config.toml`
- omp (ACTIVE profile only): its `AGENTS.md`, `RULES.md`, skills dirs from its `customDirectories`, `agents/*.md`, `rules/*.md`, `mcp.json`
- Cursor: `.cursorrules`, `.cursor/rules/*.mdc`
- OpenCode: `AGENTS.md`, `~/.config/opencode/`
- Universal (project-local): `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`

## Phase 1 — Deterministic pre-pass (no LLM judgment)

For every inventoried file compute:

1. Size and share of total corpus.
2. Absolute census: `grep -c -iE '\b(always|never|никогда|всегда|обязательно|strictly|extremely|thoroughly|carefully)\b'` — plus a **work-ordering census**: `grep -n -iE '(consider|explore|compare) (several|multiple) approach(es)?|maximum certainty|make (absolutely |really )?sure|double-?check|triple-?check|think (deeply|harder)|be extremely thorough'` — phrases that commission extra agent work: measured 2.4–7.4× reasoning (approach tournaments) and up to 18× cost (verification loops) with no success gain ([arXiv 2608.01347](https://arxiv.org/abs/2608.01347)). List every hit with its line.
3. Cross-file duplicates: normalize instruction lines (lowercase, strip punctuation) for lines starting with `-|*|[0-9]+.`; `collections.Counter` — print every pair sharing a line, as `file A ↔ file B`.
4. Dead references: every `skill://name`, `@path`, agent name — verify the target exists. **Resolve against the context that OWNS the audited file, not the auditing session**: for omp profiles, check the skills roots listed in THAT profile's `config.yml` (a reference valid where the file lives is NOT dead, even if the auditing session cannot load it). Only flag a reference dead when it resolves in none of the owning context's roots.
5. Dated snapshots: regex `\d{4}-\d{2}-\d{2}` and version pins `\d+\.\d+(\.\d+)?` — list fact · date/version · age in days.
6. Few-shot blocks: output examples / mock reports (```-blocks > 10 lines with fabricated data).
7. Live MCP surfaces (requires python3): run `python <exuvia>/meters/mcp_footprint.py --out .exuvia/mcp_footprint.json`, where `<exuvia>` is the repo checkout or the installed engines dir (`~/.exuvia/engines`). Measures each unique server's standing context payload AND its actual usage mined from session logs — record per-server rows: server · tools · bytes · tokens · calls · last_used. Treat each server as an instruction surface; a server with a permanent token cost and `calls = 0` (or stale `last_used`) is a disable candidate backed by a number, not an opinion.

## Phase 2 — Categorization (if two fit, name the dominant one)

1. **INVARIANT** — a fact or constraint the model cannot know without this file (environment, routing, safety). Safety lines (secrets, access control, production, commit/push gates) are ALWAYS category 1 and are never proposed for deletion — only for dedup or relocation.
2. **TRAINED-DUPLICATE** — the model does this without the instruction (style, default formatting, well-known definitions and methods).
3. **RELIC** — written for an older model, a fixed bug, or a state that no longer exists (cross-check Phase 1, step 5: dates, versions, current environment).
4. **90%-RULE** — true most of the time but phrased as always/never → candidate for a conditional rewrite. When rewriting, prefer the **bounded-efficiency formulation**: "smallest sufficient change; run the relevant tests; stop when the acceptance criteria pass" — measured neutral-or-better on six models while preserving diagnosis and validation (same paper). Work-ordering phrases from the Phase 1 census are rewrite candidates even when no other smell is present: they buy discarded reasoning branches, not correctness.

## Phase 3 — Report and decisions file

1. Write `.exuvia/report.md`: a section per file; rows: id · line (abridged) · category · recommendation · evidence (Phase 1 fact or inference marked `[INFERENCE]`).
2. Write `.exuvia/decisions.md`: same rows plus an empty `DECISION` column.
3. Print the summary (counts per category, top-3 findings) and STOP.

Do not propose a ready rewritten version. The user fills the DECISION column (yes / no / as-condition / keep) — decisions belong to the human.
