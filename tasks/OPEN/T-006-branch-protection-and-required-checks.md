---
id: T-006
title: Branch protection and required status checks
type: task
status: OPEN
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [T-001]
implements: []
traces_to: []
acs: []
plan: PLAN-001
size: XS
branch: main (settings only)
tags: [ops, security, ci]
confidence: high
---

# T-006 — Branch protection and required status checks

## Goal
Make `main` safe to hand a write credential to.

## Files (expected)
No repo files. GitHub UI: *Settings → Branches → Add rule for `main`*.

## Steps
1. Require a pull request before merging.
2. Require status checks: `test`, `lint`, `typecheck`, `secret-scan`, `forge-lint`.
3. Require linear history.
4. **Disallow force pushes.**
5. Require 1 human review (optional but recommended).
6. Record the applied settings in `ops/DEPLOY.md` §Branch protection with the date.

## Verification
Screenshot or `gh api repos/reARbitRA/RubikaBalehEcosystem/branches/main/protection` output pasted
into the PR that closes this task.

## Out of scope
Anything that changes repository code.

## Notes / blockers
Human-only action. `gh` is authenticated in the agent workspace, but changing protection rules is an
owner decision, not an agent one.
