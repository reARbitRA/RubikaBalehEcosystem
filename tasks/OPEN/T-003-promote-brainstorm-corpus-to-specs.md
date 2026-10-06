---
id: T-003
title: Promote the brainstorm corpus into specs
type: task
status: OPEN
version: 1.0.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [T-001]
implements: []
traces_to: []
acs: []
plan: PLAN-001
size: L
branch: spec/brainstorm-promotion
tags: [spec, m1, m2]
confidence: medium
---

# T-003 — Promote the brainstorm corpus into specs

## Goal
Convert the five migrated opportunity documents into a small number of precise, implementable specs,
and retire the overlap between them.

## Files (expected)
`specs/<area>/SPEC-###-*.md` (DRAFT), `specs/INDEX.md`, `brainstorm/BRAIN-*.md` (status → `PROMOTED`),
`.forge/TRACE.md`.

## Steps
1. Read `brainstorm/BRAIN-001..005` end to end.
2. Cluster the 56 opportunities into 3–5 candidate product areas. Recommended starting cluster
   (from `vision/ROADMAP.md`): order tracking, receipt verification, paid-member renewals.
3. For each cluster, write one spec with numbered rules and Given/When/Then ACs. Status `DRAFT`.
4. Flag every open question in §9 of each spec; where a question is really a decision, draft an ADR.
5. Mark each promoted brainstorm `PROMOTED` and record the target SPEC id in its *Promotion path*.
6. Deduplicate: `BRAIN-002` and `BRAIN-003` restate the same "top 3 opportunities" thesis — keep the
   richer one, mark the other `ABANDONED` with a pointer.
7. Move specs to `REVIEW` and stop for human approval.

## Verification
`make forge-lint` exit 0 (frontmatter, unique ids, referential integrity) · every promoted brainstorm
has a `PROMOTED` status and a named target spec · human review recorded in `.forge/LEDGER.md`.

## Out of scope
Implementing any of the specs. Choosing which one to build first (that is T-004, an ADR).

## Notes / blockers
Size L if done monolithically — split by area. Human gate at the end.
