---
id: QUAL-001
title: DOD — Definition of Done
type: quality
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [FORGE-001]
implements: []
traces_to: []
tags: [quality, dod]
confidence: high
---

# Definition of Done

## A **task** is DONE when ALL are true

- [ ] Every AC in scope has a test named `test_ac_<n>_<slug>`, and it passes
- [ ] Full suite passes (`make test` exit 0) — no `skip`/`xfail` added without a task id in the reason
- [ ] `make lint && make typecheck` exit 0
- [ ] `make forge-lint` exit 0 and `make secret-scan` reports no new findings
- [ ] Spec status advanced (only within the transitions an agent is allowed to make)
- [ ] `.forge/TRACE.md` updated for everything touched
- [ ] `ops/ENV.md` updated if any env var was added/changed
- [ ] PR opened with the template filled and **actual verification output pasted**
- [ ] `.forge/STATE.md` overwritten and `.forge/LEDGER.md` appended in the final commit

## A **spec** is VERIFIED when

A human has exercised the ACs on a deployed build and flipped the status. An agent may never do this.

## A **plan** is COMPLETE when

Every task in it is `DONE` and its §2 exit criteria are demonstrably met by pasted command output.

## A **session** is finished when

The handoff commit `chore(forge): handoff <session-id>` is the last commit on the branch, and
`.forge/STATE.md` names the next concrete step for an agent with zero context.

## What "done" never means

- "It works on my machine" without a pasted command.
- "Tests pass" when the suite was modified to make them pass.
- A spec moved to `VERIFIED` by the agent that implemented it.
