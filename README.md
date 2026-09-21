<div align="center">

# 🐍 EXUVIA

**The shed skin of your AI agent. Collected.**

**Your agent's instructions rot. Exuvia catches the rot — then PROVES the cleanup lost nothing.**

<a href="https://github.com/Zorgzeleniy/Exuvia/actions/workflows/t1.yml"><img src="https://img.shields.io/github/actions/workflow/status/Zorgzeleniy/Exuvia/t1.yml?style=flat-square&label=T1%20rig" alt="T1 rig"></a>
<a href="https://github.com/Zorgzeleniy/Exuvia/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
<a href="#-quick-start"><img src="https://img.shields.io/badge/works_with-Claude_Code_·_Codex_·_omp_·_Cursor_·_OpenCode-blue?style=flat-square" alt="5 harnesses"></a>
<img src="https://img.shields.io/badge/version-0.5.0-orange?style=flat-square" alt="v0.5.0">
<img src="https://img.shields.io/badge/engines-python_stdlib-teal?style=flat-square" alt="stdlib only">
<img src="https://img.shields.io/badge/LLM_judgment-optional__and_separated-purple?style=flat-square" alt="human decides">

**One command, no account, no API key.** `git clone https://github.com/Zorgzeleniy/Exuvia.git && node Exuvia/bin/exuvia.js init` **[→ Quick Start](#-quick-start)**

</div>

---

<div align="center">

**[See it](#-see-it) · [Quick Start](#-quick-start) · [What it catches](#-what-it-catches) · [The Numbers](#-the-numbers) · [Commands](#-commands) · [What it never does](#-what-it-never-does) · [License](#-license)**

</div>

---

## 🐍 See it

Every agent accumulates instructions that outlived the truth. Here is a real `AGENTS.md` section, before and after exuvia — as the diff the apply actually produced:

```diff
 ## Deploys
- Deploys: `npm run deploy`; gateway 10.0.0.42 (legacy).
+ Deploys: `npm run deploy`; gateway 10.0.0.99 (migrated 2026-03).

 ## Code style
- Write clean, readable code and follow best practices.
- Be careful and thorough when editing files.
 - Always prefer functional, immutable patterns wherever possible.
 - NEVER use `any` in TypeScript files. NEVER disable eslint rules inline.
- Every function must have a JSDoc comment explaining what it does.
 - Always handle errors explicitly — never swallow exceptions.

 ## Git workflow
- NEVER use the `git stash` command.
- Always run the full test suite before every commit.
+ Prefer explicit branches over `git stash`; stash only to
+ rescue uncommitted noise.
 - Commit messages: conventional commits (feat:, fix:, chore:).
- Always create a new branch before starting any work.

 ## Testing
- Aim for at least 80% coverage on all new code.
- Always write tests first, then implementation (strict TDD).
 - NEVER mock what you don't own.

 ## Environment
- Final stack state (2026-01-15): toolchain v2.1 pinned; legacy
- runner until the v3 migration completes.
 - Secrets come from `.env.local` (never committed).

```


**1,775 → 365 bytes (−79%).** What went away: trained duplicates the model does anyway, a dated snapshot from January, always/never rules converted to conditions, and a conflicting gateway IP — updated to the fresh one instead of deleted. What stayed: every invariant the model couldn't know. And the proof, from fresh headless sessions right after the apply:

```
P1 secrets    → alive (source: RULES.md) — quoted verbatim by a fresh session
P2 committing → alive — "explicit request" quoted
P3 language   → alive — "English by default" quoted
```

> Snakes don't shrink. They shed what stopped fitting. Your config should too.

### It also catches things linters can't even see

**Drift** — instructions contradicting the live machine (deterministic, no LLM):

```
| status       | fact                | detail                                |
|--------------|---------------------|---------------------------------------|
| STALE        | v3-migration-done   | pattern not found                     |
| STALE        | mcp:code-index      | 1,430 tokens/session, 0 calls ever    |
| STALE        | legacy-runner-doc   | missing: docs/legacy-runner.md        |
| UNVERIFIABLE | staging-credentials | no check defined                      |
| OK           | deploy-command      | pattern found                         |
```

<details>
<summary><strong>Constitution tests</strong> — rules that exist in the file but stopped <em>binding</em> the model</summary>

```
PASS   commit-gate        "NEVER commit… without an explicit request" — quoted by a fresh session
PASS   secrets-verbatim   "redact them" — quoted
FLAKY  language-default   failed once, passed on retry — reported, not hidden
```

</details>

<details>
<summary><strong>MCP footprint + usage</strong> — what your MCP servers cost every session, and whether anything ever calls them</summary>

```
| server     | harnesses             | tools |  bytes | tokens | calls | last used  |
|------------|-----------------------|------:|-------:|-------:|------:|------------|
| code-index | omp/default,omp/parse |    14 |  6,510 |  1,430 |     0 | never      |
| crawler    | omp/parse             |     4 |  4,881 |  1,125 |    91 | 2026-09-17 |
| context7   | omp/default,omp/parse |    2 |  4,596 |    989 |    48 | 2026-09-20 |
```

Fourteen tools, 1,430 tokens, every single session, zero invocations ever. That's the tax nobody shows you — now with the number that proves it.

</details>

---

## 🌍 Why this exists

Anthropic deleted 80% of Claude Code's system prompt without losing quality. OpenAI's new guidance says overloaded prompts now **hurt more than help** — new models execute instructions as contracts, so two conflicting rules destabilize behavior more than no rule at all.

Meanwhile your `CLAUDE.md`, skills, subagents and MCP configs keep growing. Every "add a line to fix it" is a loan. The interest compounds as duplicates diverge and facts rot.

Linters see file structure. Exuvia sees the loop: **what the instructions claim vs what the machine says vs what the model actually does** — and closes all three gaps with evidence, not vibes. The taxonomy matches the first academic catalog of AGENTS.md smells ([arXiv 2606.15828](https://arxiv.org/abs/2606.15828)).

---

## ⚡ Quick Start

Detects every supported agent on your machine, installs the right adapter into each, deploys the python engines to `~/.exuvia/engines`. Safe to re-run.

**Requirements:** Node ≥ 16 (installer) · Python ≥ 3.11 (engines). Changed your mind: `node bin/exuvia.js uninstall` removes every adapter and the engines. Windows gotchas live in the [RUNBOOK](./RUNBOOK.md).

```bash
git clone https://github.com/Zorgzeleniy/Exuvia.git && node Exuvia/bin/exuvia.js init
```

### 🕐 The first five minutes

1. **Run the audit.** `/exuvia-audit` (Claude Code, Codex) or just ask *"audit my prompt debt"*. You get a report: every line categorized — invariant / trained-duplicate / relic / 90%-rule / conflict — with a recommendation each.
2. **Decide.** Fill the DECISION column in `.exuvia/decisions.md`: yes / no / as-condition / merge. Exuvia never decides for you — analysis and action are separate sessions, on purpose.
3. **Apply.** `/exuvia-apply` executes exactly your decisions: `.bak` backups first, then edits, then fresh headless probes quoting each rule to prove it survived. A probe that fails restores the line from backup.
4. **Check drift.** `/exuvia-drift` diffs your facts registry against the live machine — milliseconds, no LLM, and half of real-world findings.
5. **Prove your constitution.** `/exuvia-test` runs probe tests for your load-bearing rules. Wire it into CI: a PR that breaks a standing rule's binding goes red.

---

## 🧩 What it catches

| Smell | Example from the wild | Caught by |
|---|---|---|
| **Trained duplicate** | "Write clean code, follow best practices" | audit (trained-duplicate) |
| **Relic** | "Final stack state (2026-01-15): toolchain v2.1" when v3 shipped | audit (relic) + drift STALE |
| **90% rule** | "NEVER use `git stash`" → becomes a condition | audit (90%-rule) |
| **Conflict** | Gateway `10.0.0.42` in AGENTS.md vs `10.0.0.99` in a skill | audit (conflict) + blame (fresher provenance wins) |
| **Stale fact** | "curl cannot write to disk" — refuted by three other files | drift |
| **Dead rule** | safety line deleted by a "cleanup" PR | constitution FAIL |
| **Context tax** | 2 MCP servers costing 2,400 tokens every session | meters |
| **Lost origin** | "who wrote this rule and why?" | blame: ledger + session-log mining |

---

## 📊 The Numbers

From this repo's committed test rig. Every number is reproducible with `python tests/run.py --t1` (free, seconds) and `--t2` (LLM, ~20 min).

| What | Measured on | Result |
|---|---|---|
| **Audit recall** | realistic sandbox corpus: 21 vendored popular skills (superpowers, anthropics) + planted smells | **8/8 planted smells found**; also flagged macOS-only commands inside superpowers as platform debt |
| **Apply safety** | same corpus, deterministic decisions | planted lines gone, **all safety lines survived**, control skill byte-identical, 5 backups, probes quoted the rules |
| **Drift engine** | fixture registry, 7 planted facts | exact statuses: 4 OK · 2 STALE · 1 UNVERIFIABLE, 0.15 s, no LLM |
| **Constitution runner** | 6 verdict classes incl. FLAKY-by-retry and ORPHANED | all reproduced deterministically against a fake harness; live run vs sandbox: 3/3 PASS in 13 s |
| **Translator roundtrip** | omp → IR → omp, probe-checked | first run **caught a line genuinely lost in translation** (2/3 → FAIL), after IR fix 3/3 green |
| **Real-world cleanup** (maintainer's own harness) | AGENTS.md + skills + MCP | AGENTS.md −65% · 17 low-quality skills removed · MCP surface 4.0k → 2.4k tokens/session |

> The translator row is the product demo: the FAIL was a line the IR author actually lost. No probe, no catch. Where a number is red, it stays red.

---

## Commands

| Command (Claude Code / Codex) | What it does |
|---|---|
| `/exuvia-audit` | 5-category revision of your instruction corpus → report + decisions file (you decide) |
| `/exuvia-apply` | executes exactly your decisions: backups, edits, ledger, probes proving nothing was lost |
| `/exuvia-drift` | facts-vs-environment diff: which standing facts are STALE |
| `/exuvia-test` | constitution tests: prove rules are LIVE in fresh sessions |
| `/exuvia-translate` | migrate the corpus between harnesses (omp↔Claude↔Codex↔Cursor), equivalence proven by probes |

omp / Cursor / OpenCode: the audit skill auto-triggers on *"audit my prompt debt"*; drift/constitution/blame/translate install as skills too — ask for them by name. Engines: `~/.exuvia/engines` (python stdlib, zero dependencies).

### Where things live

In your project, `.exuvia/`: `report.md` + `decisions.md` (audit), `probes-*.md` (apply proof), `ledger.jsonl` (provenance), `facts.toml` (drift registry), `tests/*.toml` (constitution), `mcp_footprint.json` (meters). On your machine: adapters inside each agent's config dir, engines in `~/.exuvia/engines`. Nothing else, nowhere else.

---

## 🚫 What it never does

The five invariants are the product. Breaking any of them is a semver-major decision.

1. **Never rewrites during audit.** Analysis and action are separate sessions; decisions are yours.
2. **Never deletes safety lines.** Secrets, access, prod, commit/push gates are marked invariants — dedup/move only.
3. **Never edits without a `.bak-<date>` backup** next to the file.
4. **Never adds anything of its own.** Apply performs exactly the approved decisions, word for word.
5. **Never claims a rule survived without a probe.** Verification = a fresh headless session quoting the rule.

---

## 📄 License

MIT — see [LICENSE](./LICENSE). Vendored test fixtures (superpowers, anthropics/skills) keep their own licenses.

