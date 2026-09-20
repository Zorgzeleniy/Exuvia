# Exuvia — Runbook (development notes)

## Layout
- `core/AUDIT.md`, `core/APPLY.md` — the single source of truth for procedures. Edit ONLY these.
- `templates/` — per-harness wrappers with `{{AUDIT_BODY}}` / `{{APPLY_BODY}}` placeholders.
- `bin/exuvia.js` — installer: detects harnesses by marker dirs, renders templates, idempotent copy. `status | init [--dry] | uninstall`.
- `meters/` — v0.2: fixed `mcp_footprint` (live MCP context-cost meter) lands here.

## Conventions
- English only. All outputs land in `.exuvia/` inside the audited project.
- The five invariants (README "What it never does") are the product — any change to them is a semver-major decision.
- Probes: `claude -p` / `codex exec` / `omp -p` — harness-detected, never hardcoded.
- meters/mcp_footprint.py: stdio servers via Popen-in-thread (NOT asyncio transports — Windows Proactor spams `__del__`); `cwd` from server config MUST be passed (crawl4ai breaks without it); `notifications/initialized` deliberately not sent (some local servers exit on it); tiktoken optional (fallback bytes/4, marked `~`).

## Test rig (tests/run.py)
- T1 deterministic (free): render, installer idempotency, meters, drift statuses, constitution engine via fake harness, blame card. Current: 7/7.
- T2 E2E (LLM, glm-5.3-flash:high in sandbox profile with 21 vendored popular skills + realistic AGENTS.md): audit → recall → deterministic decisions → apply → post-asserts. Current best: 13/13 effective (12 PASS + recall-8/8 with paraphrase-robust markers), ~20 min.
- Rig-caught product bugs so far: relative paths in decisions edited the fixture source (→ absolute paths + integrity check); "ask user for probes" conflicts with headless (→ pre-authorization clause in core/APPLY.md); report held in chat (→ incremental writes); hot agent.db copy hangs omp (→ sqlite3 backup API + preflight).
- Blame (v0.4): `blame/blame.py` — ledger (`.exuvia/ledger.jsonl`, written by apply) + session-log mining (omp sessions jsonl: message.content[].type=="toolCall", model from model_change events, TOUCHED-flag when marker in payload) + verified-from-constitution; `/exuvia-blame` adapters. Live-proven: mined the real Sep-15 edits of factcheck-response from our own session log. Gotcha: file-name prefilter must be case-insensitive (agents.md vs AGENTS.md). INSTALLER EDIT RULE: after every edit to bin/exuvia.js run the T-key parity check (defined vs used) — three times a line got eaten by anchored inserts.

## Self-audit 2026-09-20 (pre-translator): 11 findings, all fixed
- Cycle break: apply did not write the ledger that blame mandates → APPLY step 5 (ledger) + step 6 (constitution hook: offer a test for kept/rewritten critical rules).
- Engines were repo-only: marketplace users had no python engines → installer now deploys meters/drift/constitution/blame/core to `~/.exuvia/engines` (idempotent copyTree; uninstall removes); all procedures reference `<exuvia> = checkout OR ~/.exuvia/engines`.
- package.json `files` missed drift/constitution/blame; version was 0.1.0 → 0.4.0.
- omp/Cursor/OpenCode had audit only → omp now installs 4 skills (audit/drift/constitution/blame). README Use = full 5-command table. Installer final message lists everything. .gitignore added.
- Wording: "Phase 1.5" → "Phase 1, step 5"; MCP disable-candidate phrasing; engines log prefix "=" when nothing changed (idempotency assertion). T1: 7/7 after fixes.
- npm name availability check (`exuvia`; fallback `exuvia-sh`), then `npm publish` → `npx exuvia init`.
- Marketplace listing for Claude Code (plugin.json wrapper) — after npm.
- Translator (v0.5, DONE): `translate/emit.py` (IR jsonl → mechanical placement: omp RULES+AGENTS split, claude/codex single file, cursor flat; dedup_of entries dropped; translation-report.md) + `core/TRANSLATE.md` (harvest→IR→emit→PROVE equivalence with constitution probes→ledger action "migrated") + `/exuvia-translate` commands (claude/codex) + omp skill; engines deployed. T1-emit 8/8; live roundtrip omp→IR→omp in sandbox exuvia-t2: first run 2/3 — the FAIL caught a line genuinely missing from my hand-authored IR (language-default), exactly the designed behavior; after adding r7: 3/3 green. That FAIL→fix→green loop IS the product demo.
