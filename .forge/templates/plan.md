---
id: TEMPLATE-PLAN
title: TEMPLATE — Plan (spec → ordered, sized tasks)
type: forge
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: []
tags: [forge, template, plan]
confidence: high
---

<!-- TEMPLATE — copy to plans/PLAN-###-<slug>.md and replace every <...> placeholder. -->

---
id: PLAN-###
title: <title>
type: plan
status: DRAFT                # DRAFT → ACTIVE → COMPLETE → ARCHIVED
version: 1.0.0
owner: <human|agent|pair>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
supersedes: []
depends_on: [<SPEC-ids>]
implements: [<SPEC-ids>]
traces_to: []
tags: [<area>, <milestone>]
confidence: <low|medium|high>
---

# PLAN-### — <Title>

## 1. Source specs
SPEC-###, SPEC-###

## 2. Goal / exit criteria
A plan is COMPLETE when: <measurable condition>.

## 3. Ordered tasks
| # | Task | Size | Depends on | ACs | Notes |
|---|---|---|---|---|---|
| 1 | T-### | S | — | AC-1 | |
| 2 | T-### | M | 1 | AC-2, AC-3 | |

Size: `XS ≤1h · S ≤3h · M ≤1 session · L = split it`.

## 4. Risks / sequencing notes

## 5. Verification
`<command>` for the whole plan.
