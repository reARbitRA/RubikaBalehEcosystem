---
id: T-002
title: Retro-spec the opportunity dashboard and promote it into src/
type: task
status: REVIEW
version: 1.1.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [T-001]
implements: [SPEC-001]
traces_to: [KNOW-003, SPEC-001]
acs: [AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8]
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
`specs/SPEC-001-opportunity-dashboard.md` (REVIEW), then—only after human approval—`src/index.html`,
`tests/test_dashboard.py`, and `.forge/TRACE.md`.

## Steps
1. **Done:** read `knowledge/examples/opportunity-dashboard-v3.md`, both dashboard audits
   (`knowledge/research/audit-dashboard-v{2,3}.md`), the canonical 56-row inventory (`BRAIN-001`),
   and the single-file HTML/test decisions.
2. **Done:** draft `SPEC-001` with source-fidelity, filter, score, RTL/mobile, local CSV-export,
   offline, safe-rendering, and kill-criterion rules plus AC-1..AC-8.
3. **Done:** advance `SPEC-001` from DRAFT to REVIEW. Stop at the human `REVIEW → APPROVED` gate.
4. After approval: promote the artefact into `src/index.html` and add the `<!-- SPEC-001 -->` header.
5. Extract the pure logic (filtering, sorting, derived insights, CSV escaping) into functions that
   `tests/test_dashboard.py` can exercise, one `test_ac_<n>_<slug>` per AC.
6. Update `.forge/TRACE.md`, `.forge/STATE.md`, and append to `.forge/LEDGER.md` during the
   implementation handoff.

## Verification
`make test` (all `test_ac_*` for SPEC-001 pass) · `make forge-lint` exit 0 ·
`python3 -m http.server` smoke check that `src/index.html` opens with no console errors.

## Out of scope
Redesigning the dashboard (that is a new spec, not this task); adding new data columns; any backend.

## Notes / blockers
**REVIEW gate:** A human must decide whether the proposed Persian-first RTL presentation and local
CSV export belong in M1, then flip `SPEC-001` from `REVIEW → APPROVED` before any file under `src/`
is written. No implementation work is authorised before that transition.
