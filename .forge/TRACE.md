---
id: FORGE-004
title: TRACE — Traceability Matrix
type: forge
status: ACTIVE
version: 1.3.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: []
tags: [forge, trace, traceability]
confidence: high
---

# TRACE — bidirectional traceability matrix

> Walk it both ways: spec → plan → task → branch → commit → test → artefact, and back.
> A row is added when work starts and completed when the work merges. `commit` is filled in by the
> handoff commit of the session that produced the row.

| Spec | Plan | Task | Branch | Commit | Test | Artefact / code | Status |
|---|---|---|---|---|---|---|---|
| — (methodology, no spec) | PLAN-001 | T-001 | `chore/forge-scaffold` | `375edd5` | `tests/test_forge_integrity.py` | whole tree (`AGENTS.md`, `.forge/**`, `tools/forge_lint.py`) | DONE — PR #1 |
| SPEC-001 (REVIEW) | PLAN-001 | T-002 | `arena/8216d2ef-rubikabalehecosystem` | `37cd663` | planned `test_ac_1_*` … `test_ac_8_*` | `specs/SPEC-001-opportunity-dashboard.md`; `src/` remains empty | REVIEW — awaiting human `REVIEW → APPROVED` |
| — (methodology, no spec) | PLAN-001 | T-007 | `arena/8216d2ef-rubikabalehecosystem` | `820b50a` | `tests/test_persistence_check.py` | `tools/persistence_check.py` | DONE — local audit and regression tests pass |
| — (no spec exists yet) | PLAN-001 | T-003 | — | — | — | `brainstorm/BRAIN-001..005` → `specs/` | OPEN |
| — (decision record) | — | T-004 | — | — | — | `decisions/ADR-0004` (MVP slice choice) | OPEN |
| — (infra) | — | T-005 | — | — | — | `ops/KEYS.md` (deploy key activation) | BLOCKED |
| — (infra) | — | T-006 | — | — | — | `ops/ci-workflow.yml` → `.github/workflows/ci.yml` + branch protection | OPEN |

## Conventions for this file

- **Spec** is the SPEC id, or `—` when the work is methodology/infra (no product spec applies).
- **Test** names the exact test file or `test_ac_*` functions that prove the artefact.
- A code file in `src/` must appear in exactly one row, and must also carry its `# SPEC-###` header
  (`tools/forge_lint.py` enforces both).
- When a spec is DEPRECATED, its rows are struck through, never deleted.
