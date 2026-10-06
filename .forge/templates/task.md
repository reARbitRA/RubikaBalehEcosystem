---
id: TEMPLATE-TASK
title: TEMPLATE — Task card (one mergeable unit of work)
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
tags: [forge, template, task]
confidence: high
---

<!-- TEMPLATE — copy to tasks/<FOLDER>/T-###-<slug>.md and replace every <...> placeholder. -->

---
id: T-###
title: <title>
type: task
status: OPEN                 # OPEN → DOING → REVIEW → DONE | BLOCKED
version: 1.0.0
owner: <human|agent|pair>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
supersedes: []
depends_on: [<TASK-ids>]
implements: [<SPEC-ids>]
traces_to: []
acs: [AC-#, AC-#]
plan: PLAN-###
size: S                      # XS ≤1h · S ≤3h · M ≤1 session · L = split it
branch: feat/T-###-<slug>
tags: [<area>]
confidence: high
---

# T-### — <Title>

## Goal

## Files (expected)

## Steps
1.

## Verification
`<command>` — paste output in the PR.

## Out of scope

## Notes / blockers
