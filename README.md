# Exuvia

**The shed skin of your AI agent. Collected.**

Exuvia audits the standing instructions of your coding agent — `AGENTS.md`, `CLAUDE.md`, skills, subagent prompts, MCP tool descriptions — for **prompt debt**: stale facts, duplicates of behavior the model already has, relics of old models, always/never rules that should be conditions, and outright conflicts.

Then it does what no linter does: it **proves** the cleanup lost nothing, with live headless probes.

## Install (same everywhere)

```bash
npx exuvia init        # detects Claude Code, Codex, omp, Cursor, OpenCode — installs the right adapter into each
npx exuvia status      # what is installed where
npx exuvia uninstall
```

Manual (no npm yet): `git clone https://github.com/Zorgzeleniy/Exuvia.git && node Exuvia/bin/exuvia.js init`

## Use

| Command (Claude Code / Codex) | What it does |
|---|---|
| `/exuvia-audit` | 5-category revision of your instruction corpus → report + decisions file (you decide) |
| `/exuvia-apply` | executes exactly your decisions: backups, edits, ledger, probes proving nothing was lost |
| `/exuvia-drift` | facts-vs-environment diff: which standing facts are STALE |
| `/exuvia-test` | constitution tests: prove rules are LIVE in fresh sessions |
| `/exuvia-blame` | provenance of an instruction line: when, which model, why, still verified |
| `/exuvia-translate` | migrate the corpus between harnesses (omp↔Claude↔Codex↔Cursor), equivalence proven by probes |

omp / Cursor / OpenCode: the audit skill auto-triggers on "audit my prompt debt"; drift/constitution/blame/translate are installed as skills there too (ask for them by name).

Audit writes `.exuvia/report.md` + `.exuvia/decisions.md`. You fill the decision column (yes / no / as-condition / merge). Apply executes exactly your decisions, backs up every file, records the ledger, and re-runs probes to verify no rule was lost.

## What it never does

1. **Never rewrites during audit.** Analysis and action are separate sessions; decisions are yours.
2. **Never deletes safety lines.** Secrets, access, prod, commit/push gates are marked invariants — dedup/move only.
3. **Never edits without a `.bak-<date>` backup** next to the file.
4. **Never adds anything of its own.** Apply performs exactly the approved decisions, word for word.
5. **Never claims a rule survived without a probe.** Verification = a fresh headless session quoting the rule.

## Roadmap

✅ core audit/apply · ✅ MCP footprint meter · ✅ drift-core · ✅ constitution tests · ✅ blame provenance · ✅ cross-harness translator — **community benchmark (next)**.

## License

MIT
