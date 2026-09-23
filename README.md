<div align="center">

# 🐍 EXUVIA

**The shed skin of your AI agent. Collected.**

**Your agent's instruction files (`CLAUDE.md`, `AGENTS.md`, skills, MCP configs) rot. Exuvia catches the rot — and proves the cleanup lost nothing.**

<a href="https://www.npmjs.com/package/exuvia"><img src="https://img.shields.io/npm/v/exuvia?style=flat-square&color=orange&label=npm" alt="exuvia on npm"></a>
<a href="https://github.com/Zorgzeleniy/Exuvia/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT"></a>
<a href="#-quick-start"><img src="https://img.shields.io/badge/works_with-Claude_Code_·_Codex_·_omp_·_Cursor_·_OpenCode-blue?style=flat-square" alt="5 harnesses"></a>
<img src="https://img.shields.io/badge/engines-python_stdlib-teal?style=flat-square" alt="stdlib only">
<img src="https://img.shields.io/badge/LLM_judgment-optional__and_separated-purple?style=flat-square" alt="human decides">

**One command, no account, no extra API key.** `npx exuvia init` **[→ Quick Start](#-quick-start)**

</div>

---

<div align="center">

**[See it](#-see-it) · [Quick Start](#-quick-start) · [What it catches](#-what-it-catches) · [The Numbers](#-the-numbers) · [Commands](#commands) · [What it never does](#-what-it-never-does) · [Glossary](#-words-we-use) · [License](#-license)**

</div>

---

## 🐍 See it

Every agent accumulates instructions that outlived the truth. Here is a real `CLAUDE.md` from a popular 41.6k-star repo, before and after exuvia — as the diff the apply actually produced:

```
# CLAUDE.md

-Tutorial repo. Output is markdown in numbered modules `01-` through `10-`, not an app.
-Scripts in `scripts/` exist only to validate docs and build the EPUB.
-
-See also `.claude/CLAUDE.md` for stack/commands and `STYLE_GUIDE.md` for lesson structure.
-
-## Critical commands
-
-```bash
-# Quality gate (also runs on commit via pre-commit hooks)
-pre-commit run --all-files
-
-# Tests
-pytest scripts/tests/ -v
-
-# EPUB build (renders Mermaid with the local mmdc CLI — no network, needs mmdc on PATH)
-uv run scripts/build_epub.py
-
-# Python tooling
-ruff check scripts/ && ruff format scripts/
-mypy scripts/ --ignore-missing-imports
-bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/
-```
-
-## Architecture map
-
-- `01-` … `10-` — tutorial modules. **Numbered prefix = learning order**, not alphabetical. Do not reorganize.
-- Each module: `README.md` + copy-paste templates (`.md`, `.json`, `.sh`).
-- `scripts/` — utilities (EPUB builder, link/mermaid/cross-ref validators). Not the product.
-- `02-memory/*.md` — CLAUDE.md templates users copy into their own projects. Don't confuse with this file.
-- `openspec/` — spec-driven change proposals.
-
 ## Hard rules

 - **YOU MUST NOT commit or push without explicit user request.**

```
**3,577 → 1,561 bytes (−56%).** What went away: an architecture map for a repo that doesn't exist here (8 dead path references), commands that can't run, trained duplicates the model does anyway. What stayed: every hard rule, every safety invariant, every workflow preference. And in the [A/B benchmark](#-the-numbers), the cleaned corpus cut input tokens **−95%** on the first task — quality flat.

```
P1 committing → alive — "MUST NOT commit or push without explicit user request" quoted
P2 markdown  → alive — "code fences must declare a language" quoted
```

> **What's a probe?** The whole proof mechanism, in three sentences. Exuvia opens a brand-new agent session in the background — no chat, just a question — and asks it to quote a rule ("what are your directives about secrets?"). If the fresh session still quotes the rule, the rule is alive, no matter which file it lives in. That's a probe; every "alive" above is one.

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

**Constitution tests** — rules that exist in the file but stopped *binding* the model:

```
PASS   commit-gate        "NEVER commit… without an explicit request" — quoted by a fresh session
PASS   secrets-verbatim   "redact them" — quoted
FLAKY  language-default   failed once, passed on retry — reported, not hidden
```

**MCP footprint + usage** — what your MCP servers cost every session, and whether anything ever calls them:

```
| server     | harnesses             | tools |  bytes | tokens | calls | last used  |
|------------|-----------------------|------:|-------:|-------:|------:|------------|
| code-index | omp/default,omp/parse |    14 |  6,510 |  1,430 |     0 | never      |
| crawler    | omp/parse             |     4 |  4,881 |  1,125 |    91 | 2026-09-17 |
| context7   | omp/default,omp/parse |    2 |  4,596 |    989 |    48 | 2026-09-20 |
```

Fourteen tools, 1,430 tokens, every single session, zero invocations ever. That number is the case for disabling it.

## 🌍 Why this exists

In July 2026, Anthropic engineers reported removing over 80% of Claude Code's system prompt for the newest models — coding evals didn't move. OpenAI's guidance now says overloaded prompts **hurt more than help**: new models follow instructions literally, so two conflicting rules destabilize behavior more than no rule at all.

Meanwhile your `CLAUDE.md`, skills, subagents and MCP configs keep growing. Every "add a line to fix it" is a loan. The interest compounds as duplicates diverge and facts rot.

Linters see file structure. Exuvia sees the loop: **what the instructions claim vs what the machine says vs what the model actually does** — and closes all three gaps with evidence, not vibes. The taxonomy matches the first academic catalog of AGENTS.md smells ([arXiv 2606.15828](https://arxiv.org/abs/2606.15828)).

A preregistered 4,643-run study put numbers on the mechanism ([arXiv 2608.01347](https://arxiv.org/abs/2608.01347)): prompt **length** is nearly free — verbose repetition measures ~1.0× — while phrases that **order extra work** are not. "Compare several approaches" multiplies reasoning 2.4–7.4× at zero correctness gain; certainty language ("make absolutely sure") inflates output up to 4.1×, buying re-verification loops, not success. The most dangerous line in your config isn't the verbose one — it's the *plausible wrong hint*: misleading architectural hints raised reasoning 2.61× — the costliest input defect measured — while irrelevant noise measured nearly free (1.03×). And the harness amplifies all of it: a heavy standing prefix replays those consequences every single turn.

---

## 📈 It compounds

Everything exuvia does leaves working material behind — and nothing gets lost between runs:

- After an audit you keep the report, your decisions file, a facts checklist, and a change log. The next audit starts from them, not from zero.
- While you work, exuvia counts which MCP tools actually get called and remembers where every instruction line came from. The longer you've been running agents, the better it can answer "is this instruction earning its tokens?"
- When you switch tools (Claude Code → Codex → Cursor), it carries your instructions over and checks nothing got lost on the way.

It starts as a linter. It grows into the history of every rule you approved, tested, and shed.

---

## ⚡ Quick Start

Detects every supported agent on your machine, installs the right adapter into each, deploys the python engines to `~/.exuvia/engines`. Safe to re-run.

**Requirements:** Node ≥ 16 (installer) · Python ≥ 3.11 (engines). The audit and apply run inside YOUR agent session on your existing plan — no extra API keys; the deterministic engines (drift, meters, blame) call no model at all. Changed your mind: `npx exuvia uninstall`. Windows gotchas live in the [RUNBOOK](./RUNBOOK.md).

```bash
npx exuvia init
```

### 🕐 The first five minutes

1. **Run the audit.** `/exuvia-audit` (Claude Code, Codex) or just ask *"audit my prompt debt"*. You get a report: every line categorized — invariant / trained-duplicate / relic / 90%-rule / conflict — with a recommendation each.
2. **Decide.** Fill the DECISION column in `.exuvia/decisions.md`: yes / no / as-condition / merge. Exuvia never decides for you — analysis and action are separate sessions, on purpose.
3. **Apply.** `/exuvia-apply` executes exactly your decisions: `.bak` backups first, then edits, then fresh headless probes quoting each surviving rule. A probe that fails restores the line from backup.
4. **Check drift.** `/exuvia-drift` diffs your facts registry against the live machine — milliseconds, no LLM, and half of real-world findings.
5. **Test your constitution.** `/exuvia-test` runs probe tests for your load-bearing rules. Wire it into CI: a PR that breaks a standing rule's binding goes red.

---

## 🧩 What it catches

| Smell | Example from the wild | Caught by |
|---|---|---|
| **Trained duplicate** | "Write clean code, follow best practices" | audit (trained-duplicate) |
| **Relic** | "Final stack state (2026-01-15): toolchain v2.1" when v3 shipped | audit (relic) + drift STALE |
| **Context tax** | 2 MCP servers costing 2,400 tokens every session | meters (internal engine, runs inside audit) |
| **Conflict** | Gateway `10.0.0.42` in AGENTS.md vs `10.0.0.99` in a skill | audit (conflict) + blame (fresher provenance wins) |
| **Stale fact** | "curl cannot write to disk" — refuted by three other files | drift |
| **Dead rule** | safety line deleted by a "cleanup" PR | constitution FAIL |
| **Lost origin** | "who wrote this rule and why?" | blame: ledger + session-log mining |

---

## 📊 The Numbers

From this repo. The A/B row is reproducible with `python bench/run_ab.py` (LLM, ~30 min); the suite itself is `python tests/run.py --t1` (free, seconds) and `--t2` (LLM, ~20 min).

| What | Measured on | Result |
|---|---|---|
| **Real-world cleanup** (maintainer's own harness) | AGENTS.md + skills + MCP | AGENTS.md −65% · 17 low-quality skills removed · MCP surface 4.0k → 2.4k tokens/session |
| **A/B shed-bench** | real popular config (41.6k★ CLAUDE.md + 23 skills incl. 2 viral) · 4 deterministic tasks × 3 repeats × 2 arms, same model | **−95% input tokens** on the first coding task (64,545 → 3,169 median) · **−63% cost** on that task · **−40% cost** on Q&A · quality flat or better (one task improved 0% → 67%) |
| **Translator roundtrip** | omp → neutral intermediate format → omp, probe-checked | first run **caught a line genuinely lost in migration** (2/3 → FAIL); after the fix, 3/3 green |

---

## Commands

| Command (Claude Code / Codex) | What it does |
|---|---|
| `/exuvia-audit` | 5-category revision of your instruction corpus → report + decisions file (you decide) |
| `/exuvia-apply` | executes exactly your decisions: backups, edits, ledger, probes that quote every surviving rule |
| `/exuvia-drift` | facts-vs-environment diff: which standing facts are STALE |
| `/exuvia-test` | constitution tests: prove rules are LIVE in fresh sessions |
| `/exuvia-translate` | migrate the corpus between harnesses (omp↔Claude↔Codex↔Cursor), probe-checked equivalence |
| `/exuvia-blame` | provenance for any instruction line: ledger + session-log mining — who wrote it, when, why |

omp: all five install as skills and auto-trigger on plain asks (*"audit my prompt debt"*) — they wake when you ask, never on their own. Cursor / OpenCode: a single audit adapter (audit + apply). Engines: `~/.exuvia/engines` (python stdlib, zero dependencies).

### Where things live

In your project, `.exuvia/`: `report.md` + `decisions.md` (audit), `probes-*.md` (apply proof), `ledger.jsonl` (change log), `facts.toml` (drift checklist), `tests/*.toml` (constitution), `mcp_footprint.json` (meters) — plus the reports each engine emits (`drift-report.md`, `constitution.json`, `report.html`, `ir.jsonl` — the intermediate format), all in the same place. On your machine: adapters inside each agent's config dir, engines in `~/.exuvia/engines`. Nothing lands anywhere else.

---

## 🚫 What it never does

The five invariants are the product. Breaking any of them is a semver-major decision.

1. **Never rewrites during audit.** Analysis and action are separate sessions; decisions are yours.
2. **Never deletes safety lines.** Secrets, access, prod, commit/push gates are marked invariants — dedup/move only.
3. **Never edits without a `.bak-<date>` backup** next to the file.
4. **Never adds anything of its own.** Apply performs exactly the approved decisions, word for word.
5. **Never claims a rule survived without a probe.** Verification = a fresh headless session quoting the rule.

---

## 📖 Words we use

| Term | Plain meaning |
|---|---|
| **probe** | a background agent session asked to quote one rule — if it quotes, the rule is alive |
| **AGENTS.md / CLAUDE.md** | the file where your agent's standing instructions live; same role, different tool names |
| **harness** | the agent tool itself (Claude Code, Codex, Cursor, omp, OpenCode) |
| **instruction corpus** | all your standing instructions together: CLAUDE.md/AGENTS.md, skills, subagent prompts, MCP tool descriptions |
| **drift** | a standing instruction that no longer matches the actual machine (path moved, tool updated, port closed) |
| **ledger** | a local change log exuvia keeps: who wrote/changed which line, when, and why |
| **omp** | Oh My Pi — an open-source terminal coding agent, one of the five supported tools |
| **headless session** | an agent run with no interactive chat — a question in, an answer out, used for probes |

---

## 📄 License

MIT — see [LICENSE](./LICENSE). Vendored test fixtures (superpowers, anthropics/skills) keep their own licenses.

