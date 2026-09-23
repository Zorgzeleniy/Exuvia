# AGENTS.md — Julep AI

Purpose: onboarding manual for AI assistants and humans editing this repo. Humans own architecture, tests, and domain judgment; the AI implements.

## Golden rules

- When unsure about implementation details or requirements — ask the developer before making changes. Never guess project-specific decisions.
- Generate code only inside the relevant component's source directories (or explicitly pointed files). Never touch `tests/`, `SPEC.md`, `*_spec.py`, `*.ward` — humans own tests & specs.
- For changes >300 LOC or >3 files, ask for confirmation before starting.
- Stay within the current task; suggest a fresh session if the request belongs to a different context.
- Never modify `.agentignore` / `.agentindexignore` without explicit permission.

## Commands

`poe` tasks (they guarantee correct env vars and configuration):

```bash
poe format    # ruff format
poe lint      # ruff check
poe typecheck # pytype --config pytype.toml (agents-api) / pyright (cli)
poe test      # ward test --exclude .venv (pytest for integrations-service)
poe test --search "pattern"  # filter tests — do NOT use -p (ward, not pytest)
poe check     # format + lint + type + SQL validation
poe codegen   # generate API code (OpenAPI from TypeSpec)
```

Quick script test: `PYTHONPATH=$PWD python tests/test_file.py` (ensure correct CWD).

## Layout

| Directory | What |
|---|---|
| `src/agents-api/` | FastAPI service & Temporal activities |
| `src/memory-store/` | PostgreSQL + TimescaleDB schemas & migrations |
| `src/blob-store/` | S3-compatible object storage |
| `src/integrations-service/` | Adapters for external services |
| `src/scheduler/` | Temporal workflow engine |
| `src/gateway/` | API gateway (routing, request handling) |
| `src/llm-proxy/` | LiteLLM proxy for language models |
| `src/monitoring/` | Prometheus & Grafana |
| `src/typespec/` | **Source-of-truth** API specifications (TypeSpec) |
| `sdks/` | Node.js & Python client SDKs |

Only the `cli` component has a `src/` directory; `agents-api` code sits directly in `agents_api/`. Full architecture diagram: `.github/CONTRIBUTING.md`.

## Domain models

Defined in TypeSpec (`src/typespec/<model>/models.tsp`), generated into Pydantic: **Agent** (instructions + tools), **Task** (workflow of steps), **Tool** (capability/integration), **Session** (interaction container), **Entry** (message/event), **Execution** (task run state).

## API & codegen

- To change API models: edit TypeSpec files in `src/typespec/`, then `bash src/scripts/generate_openapi_code.sh` from project root.
- Never manually edit generated files (`autogen/` directories) — they get overwritten.

## Python expressions in tasks

- Evaluated by `simpleeval` in a sandbox; validate with `validate_py_expression()` from `agents_api.activities.task_steps.base_evaluate`.
- Expression input is `_`; standard library modules available.
- In `task_to_spec`-converted tasks the step type is in `kind_`; raw tasks use step-type keys; "if_else" conditions live in `if_`.

## AIDEV anchors

- Add `AIDEV-NOTE:` / `AIDEV-TODO:` / `AIDEV-QUESTION:` comments (≤120 chars) near non-trivial code: long, complex, important, confusing, or bug-adjacent.
- Before scanning files, locate existing `AIDEV-*` anchors in the relevant subdirectory first; update them together with the code.
- Never remove `AIDEV-NOTE`s without explicit human instruction.

## Commits

- One logical change per commit; explain the *why*.
- Tag AI-generated commits: `feat: optimise feed query [AI]`.
- Use `git worktree` for parallel/long-running AI branches.

## Style

Python 3.12+, async/await, strict typing with Pydantic v2, Google-style docstrings on public APIs. The ruff config in `pyproject.toml` (96-char, double quotes) is the authority — don't re-format to any other style.

## Pitfalls

- Ward uses `@test()` decorators — not pytest fixtures/classes.
- `source .venv/bin/activate` first; correct CWD per component.
- Don't delegate test/spec writing entirely to AI — it breeds false confidence.

Components version independently (SemVer per `pyproject.toml`).

## Directory AGENTS.md files

Check for a directory-level `AGENTS.md` before working in it. After significant changes to a directory's structure or patterns, update it — or suggest creating one.
