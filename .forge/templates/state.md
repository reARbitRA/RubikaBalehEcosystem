---
id: TEMPLATE-STATE
title: TEMPLATE — STATE (overwritten each session)
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
tags: [forge, template, state]
confidence: high
---

<!-- TEMPLATE — overwrite .forge/STATE.md with this shape at the end of every session. -->

---
id: STATE-###
title: STATE — Current Snapshot
type: state
status: ACTIVE
version: 1.0.0
owner: agent
created: <first-ever date>
updated: <today>
supersedes: []
depends_on: []
implements: []
traces_to: []
tags: [forge, state]
confidence: high
---

# STATE — as of <ISO8601> · session <id> · HEAD <sha>

## Milestone: <M# name> — <%> by task count
## Green baseline: YES|NO (`make test` N passed, 0 failed)
## In progress
- T-### (SPEC-### AC-#, AC-#) — branch <name> — <%> — next: <next concrete step>
## Blocked
- T-### — <what is missing, who must act>
## Next up (ordered)
1. T-###  2. T-###  3. <other>
## Known debt / warnings
- <flaky test, debt, doc that needs review>
## Env/infra changes this session
- <env vars added, keys rotated, workflows added>
