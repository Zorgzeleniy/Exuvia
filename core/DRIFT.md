# Exuvia Drift Procedure

Drift = standing instructions that no longer match the environment. This
procedure is deterministic-first: the machine judges, the model only drafts.

## 1. Run the registry
```
python <exuvia>/drift/check.py --facts .exuvia/facts.toml --base <repo-or-profile-root>
```

`<exuvia>` = the repo checkout or the installed engines dir (`~/.exuvia/engines`).

Statuses: `OK` (fact holds) · `STALE` (fact contradicts the environment — this
is prompt debt) · `UNVERIFIABLE` (no checker) · `ERROR` (checker broke).

## 2. Read the STALE table, propose resolutions

For every STALE row: find the instruction lines that assume this fact (grep the
corpus for the fact's keywords), and write the contradiction explicitly:

> instruction says: <line, file>
> environment says: <checker detail>

Propose ONE of: update the instruction line · delete it · update the fact
checker (if the environment, not the instruction, is the anomaly). **Do not
apply anything** — output the table plus proposals to `.exuvia/drift-report.md`.

## 3. Draft facts for UNVERIFIABLE assumptions (ingest)

Scan instruction surfaces for environment assumptions that have no registry
entry (paths, versions, ports, installed tools, host addresses). For each,
append a draft to `.exuvia/facts.toml`:

```toml
[facts.<kebab-id>]
description = "<what the instructions assume>"
check = { type = "file_exists|file_contains|dir_glob|shell|port_open", ... }
```

Draft conservative checkers (shell only when a cheaper type cannot express it).
Then re-run step 1 and show the new table. Never invent facts about the
environment you have not checked.

## 4. Human decides

The drift report is a decision table like any other audit: the user approves
each proposal; applying goes through the apply procedure (backups, probes).
