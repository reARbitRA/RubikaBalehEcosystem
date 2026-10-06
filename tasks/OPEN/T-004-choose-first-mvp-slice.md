---
id: T-004
title: Decide the first real MVP slice (ADR)
type: task
status: OPEN
version: 1.0.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [T-003]
implements: []
traces_to: []
acs: []
plan: PLAN-001
size: S
branch: adr/0004-first-mvp-slice
tags: [decision, m2]
confidence: medium
---

# T-004 — Decide the first real MVP slice

## Goal
Produce `decisions/ADR-0004-first-mvp-slice.md` (PROPOSED) that picks **one** slice to build in M2 and
states the kill criteria.

## Files (expected)
`decisions/ADR-0004-first-mvp-slice.md`, `vision/ROADMAP.md` (M2 entry refined),
`.forge/TRACE.md`.

## Steps
1. Use the promoted specs from T-003 as the option set.
2. Score each against `vision/PRINCIPLES.md` (revenue-loss-first, manual-first, zero-API, spec-able).
3. Draft the ADR with: context, decision, consequences, alternatives, kill criteria (borrow the
   inventory's own "Kill Criteria" column).
4. Mark it `PROPOSED` and stop — a human accepts it.

## Verification
`make forge-lint` exit 0 · the ADR names exactly one slice, one owner, and a measurable kill criterion.

## Out of scope
Any planning of the build itself (that is a new PLAN after the ADR is ACCEPTED).

## Notes / blockers
Depends on T-003's specs existing.
