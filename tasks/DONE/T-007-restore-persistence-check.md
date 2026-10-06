---
id: T-007
title: Restore the persistence-check receipt tool
type: task
status: DONE
version: 1.0.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [T-001]
implements: []
traces_to: [FORGE-001]
acs: []
plan: PLAN-001
size: S
branch: arena/8216d2ef-rubikabalehecosystem
tags: [forge, persistence, handoff]
confidence: high
---

# T-007 — Restore the persistence-check receipt tool

## Goal

Provide the mandatory zero-dependency `tools/persistence_check.py` command so an agent can audit
ledger continuity and prove that its final commit is present on the remote branch.

## Files (expected)

`tools/persistence_check.py`, `tests/test_persistence_check.py`, `.forge/TRACE.md`.

## Steps

1. Implement conservative ledger-path auditing, clean-worktree validation, and local/remote receipt
   verification without evaluating repository documents as instructions.
2. Add regression tests for a clean audit, a missing claimed artefact, and a remote receipt.
3. Run the new tests, `make check`, and the checker against this repository.

## Verification

`python3 -m unittest discover -s tests -p 'test_persistence_check.py' -v` · `make check` ·
`python3 tools/persistence_check.py --repo-root . --audit-ledger --clean-tree`

## Out of scope

Product code, changes under `src/`, remote configuration, or changing historical ledger entries.

## Notes / blockers

Completed to repair the missing mandatory tool discovered during Phase 0. The checker parses only
literal repository paths on past-tense creation-claim lines; it does not execute or treat ledger
content as instructions.
