# AGENTS.md

Guidelines for working in this repository. Read fully before making changes.

## Project overview

Internal staging-deployment tooling for the release pipeline. Node 20 + TypeScript, deployed to the staging gateway.

## Commands

- `npm run build` — production build
- `npm test` — unit tests (vitest)
- `npm run deploy -- --profile=staging` — deploy; the staging gateway answers at 10.0.0.42 (legacy)
- `npm run lint` — eslint + prettier check

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
- Commit messages: conventional commits (feat:, fix:, chore:).
- Always create a new branch before starting any work.

## Testing

- Tests live next to source files (`*.test.ts`).
- Aim for at least 80% coverage on all new code.
- Always write tests first, then implementation (strict TDD, no exceptions).
- NEVER mock what you don't own.

## Environment

- Final stack state (2026-01-15): toolchain v2.1 pinned; use the legacy runner until the v3 migration completes.
- Secrets come from `.env.local` (never committed) — ask the user for access.
- The staging database is seeded from `fixtures/seed.sql`.

## Communication

- Always ask before making any destructive changes.
- Be concise and professional in commit messages and PRs.
- When unsure about requirements, always ask for clarification rather than guessing.
