---
id: T-005
title: Activate the deploy key
type: task
status: BLOCKED
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
tags: [ops, security, keys]
confidence: high
---

# T-005 — Activate the deploy key

## Goal
Give the agent workspace a revocable, single-repo, auditable write credential instead of relying on
the ambient `gh` token.

## Files (expected)
`ops/KEYS.md` (status flip to ACTIVE), `~/.ssh/config` (host alias), git remote (optional switch).

## Steps
1. The keypair already exists **outside the repo tree** at
   `~/.forge-keys/RubikaBalehEcosystem_20261006` (private) / `.pub` (public).
2. Human: repo → *Settings → Deploy keys → Add* → paste the public key from `ops/KEYS.md` → enable
   **Allow write access** → title it `forge-agent 2026-10-06`.
3. Verify: `ssh -T git@github-forge-RubikaBalehEcosystem` should print
   `Hi reARbitRA/RubikaBalehEcosystem! You've successfully authenticated`.
4. Optional: `git remote set-url origin git@github-forge-RubikaBalehEcosystem:reARbitRA/RubikaBalehEcosystem.git`
   — **only after step 3 succeeds**. Until then, HTTPS + `gh` remains the working push path.
5. Flip the key row in `ops/KEYS.md` from `PENDING ACTIVATION` to `ACTIVE`.
6. Rotate every 30 days, or immediately if a session behaves unexpectedly.

## Verification
Output of `ssh -T git@github-forge-RubikaBalehEcosystem` pasted into the closing PR, plus a test push
to a scratch branch that is then deleted.

## Out of scope
Anything that touches product code.

## Notes / blockers
**BLOCKED: the public key must be added by a human in GitHub settings — an agent cannot do this.**
Until then, all pushes go over HTTPS with the authenticated `gh` session.
