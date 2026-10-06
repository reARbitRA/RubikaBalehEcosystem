---
id: PLAN-001
title: PLAN-001 — Methodology adoption and retro-spec of the legacy corpus
type: plan
status: ACTIVE
version: 1.0.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [ADR-0001, ADR-0002, ADR-0003]
implements: []
traces_to: [T-001]
tags: [m0, m1, forge]
confidence: high
---

# PLAN-001 — Methodology adoption and retro-spec of the legacy corpus

## 1. Source specs
None. This plan is methodology work: it exists to make specs possible. It deliberately implements no
SPEC (there are none yet) — that is the point of M0.

## 2. Goal / exit criteria
The plan is COMPLETE when all of the following are true:

1. `make bootstrap && make test && make lint && make typecheck && make forge-lint && make secret-scan`
   all exit 0 on a clean clone.
2. A brand-new agent can follow `AGENTS.md` §1 and print a correct Session Plan without human input.
3. The 10 legacy documents live in the taxonomy with valid frontmatter and provenance.
4. The first product artefact (`knowledge/examples/opportunity-dashboard-v3.md`) has an APPROVED spec
   and a home in `src/` — or an explicit human decision that it stays out of `src/`.
5. Write credential is active and logged in `ops/KEYS.md`; branch protection + required checks are on.

## 3. Ordered tasks

| # | Task | Size | Depends on | ACs | Notes |
|---|---|---|---|---|---|
| 1 | T-001 — scaffold the SPEC-FORGE structure | M | — | — | DONE in session `2026-10-06-01` |
| 2 | T-002 — retro-spec the opportunity dashboard | M | T-001 | — | ends at a human APPROVED gate |
| 3 | T-003 — promote brainstorm corpus into specs | L | T-001 | — | split per area if it grows |
| 4 | T-004 — decide the first real MVP slice | S | T-003 | — | output is an ADR, not code |
| 5 | T-005 — activate the deploy key | XS | T-001 | — | human action; currently BLOCKED |
| 6 | T-006 — branch protection + required status checks | XS | T-001 | — | human action in GitHub settings |

## 4. Risks / sequencing notes

- **T-002/T-003 gate on a human.** An agent may draft, but only a human moves `REVIEW → APPROVED`.
  If no human is available, the correct agent behaviour is to stop and say so.
- **T-003 is size L** if done in one pass across five brainstorm documents; split it by area
  (orders / receipts / memberships / support) rather than doing it monolithically.
- The legacy corpus overlaps (`روبیکابله.md` vs `روبیکابله۱.md`); dedupe during promotion, and mark
  the loser `ABANDONED` with a `supersedes`-style note in its body rather than deleting it.

## 5. Verification
`make forge-lint` (structure + frontmatter + traceability) and, once T-002 lands,
`make test` covering the dashboard spec's ACs.
