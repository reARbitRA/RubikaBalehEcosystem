---
id: T-001
title: Scaffold the SPEC-FORGE structure
type: task
status: DONE
version: 1.0.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: [ADR-0001]
acs: []
plan: PLAN-001
size: M
branch: chore/forge-scaffold
tags: [forge, m0]
confidence: high
---

# T-001 — Scaffold the SPEC-FORGE structure

## Goal
Turn a flat markdown dump into a self-bootstrapping repository: entry point, memory, taxonomy,
templates, CI gate, test suite, key protocol.

## Files (expected)
`AGENTS.md`, `.forge/{STATE,LEDGER,GLOSSARY,CONVENTIONS,TRACE}.md`, `.forge/templates/*` (8),
`vision/*`, `decisions/ADR-000{1,2,3}`, `plans/PLAN-001`, `tasks/**`, `specs/INDEX.md`,
`quality/{DOD,TEST-STRATEGY,SECURITY-BASELINE}.md`, `ops/{ENV,DEPLOY,KEYS,RUNBOOK}.md`,
`tools/forge_lint.py`, `tests/*`, `Makefile`, `.gitignore`, `.github/{workflows/,PULL_REQUEST_TEMPLATE.md,CODEOWNERS}` + `ops/ci-workflow.yml`.

## Steps
1. Write `AGENTS.md` (constitution + bootstrap + rules).
2. Write `.forge/` memory files and 8 templates.
3. Create the folder tree with `.gitkeep` in the empty dirs.
4. Write `tools/forge_lint.py` and wire `make forge-lint` + CI.
5. Write the stdlib-unittest suite so `make test` is meaningful and green.
6. Migrate the 10 legacy documents into `brainstorm/` and `knowledge/` with frontmatter + provenance.
7. Author vision/decisions/quality/ops documents from the corpus.
8. Generate the ed25519 deploy key outside the repo tree; record only the public fingerprint.

## Verification
```
make bootstrap && make test && make lint && make typecheck && make forge-lint && make secret-scan
```
All exit 0. Output pasted in the PR and in `.forge/LEDGER.md`.

## Out of scope
Any product code in `src/`; any spec authoring (T-002/T-003); any GitHub settings change (T-005/T-006).

## Notes / blockers
None. Completed in session `2026-10-06-01`.
