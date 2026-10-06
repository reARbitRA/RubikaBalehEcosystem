---
id: T-002
title: Retro-spec the opportunity dashboard and promote it into src/
type: task
status: OPEN
version: 1.0.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [T-001]
implements: []
traces_to: [KNOW-003]
acs: []
plan: PLAN-001
size: M
branch: spec/SPEC-001-opportunity-dashboard
tags: [m1, frontend, spec]
confidence: high
---

# T-002 — Retro-spec the opportunity dashboard and promote it into `src/`

## Goal
The dashboard in `knowledge/examples/opportunity-dashboard-v3.md` is currently product code living in
the wrong folder with no spec. Give it a spec, then move the artefact to `src/` where it belongs.

## Files (expected)
`specs/SPEC-001-opportunity-dashboard.md` (DRAFT), `src/index.html` (moved artefact),
`tests/test_dashboard.py`, `.forge/TRACE.md`.

## Steps
1. Read `knowledge/examples/opportunity-dashboard-v3.md` and both audits
   (`knowledge/research/audit-dashboard-v{2,3}.md`).
2. Draft `specs/SPEC-001-opportunity-dashboard.md` with numbered rules (data source, filter
   dimensions, score dimensions, RTL/mobile behaviour, export, offline constraint) and Given/When/Then
   ACs for each. Status `DRAFT`.
3. Move the spec to `REVIEW` and **stop** — a human must flip `REVIEW → APPROVED`.
4. After approval: move the artefact to `src/index.html`, add the `<!-- SPEC-001 -->` header.
5. Extract the pure logic (filtering, sorting, scoring) into functions that `tests/test_dashboard.py`
   can exercise, one `test_ac_<n>_<slug>` per AC.
6. Update `.forge/TRACE.md`, `.forge/STATE.md`, append to `.forge/LEDGER.md`.

## Verification
`make test` (all `test_ac_*` for SPEC-001 pass) · `make forge-lint` exit 0 ·
`python3 -m http.server` smoke check that `src/index.html` opens with no console errors.

## Out of scope
Redesigning the dashboard (that is a new spec, not this task); adding new data columns; any backend.

## Notes / blockers
Blocked on the human `REVIEW → APPROVED` gate after step 3. Do not implement before that.
