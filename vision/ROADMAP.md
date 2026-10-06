---
id: VISION-003
title: ROADMAP — Milestones M0..M4
type: vision
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [VISION-001, VISION-002]
implements: []
traces_to: []
tags: [vision, roadmap, milestones]
confidence: medium
---

# ROADMAP

| Milestone | Theme | Exit criteria |
|---|---|---|
| **M0** | Methodology adoption | A brand-new agent reads `AGENTS.md`, runs `make bootstrap && make test`, gets a green baseline, and can name the next task without asking anyone. `forge-lint` runs in CI. Write credential active and logged in `ops/KEYS.md`. |
| **M1** | Opportunity dashboard, spec'd and shipped | `knowledge/examples/opportunity-dashboard-v3.md` promoted into `src/` behind an APPROVED spec; ≥1 AC per spec section covered by `test_ac_*`; deployed to a public URL; a human has exercised it and flipped the spec to `VERIFIED`. |
| **M2** | First semi-manual MVP: order tracking | A seller can log an order, see its status, and get a follow-up reminder — run by an operator with no API. 5 real sellers use it for 14 days. Spec APPROVED → IMPLEMENTED → VERIFIED. |
| **M3** | Receipt verification + paid-member renewals | Two more slices, each its own spec, each proven with paying or committing users. |
| **M4** | Micro-SaaS consolidation | The proven slices merge into one subscription product with a shared data model; pricing validated. |

## Sequencing rules

- M1 must finish before M2 starts: we need one complete spec→test→deploy→verify cycle to calibrate
  the methodology before we bet real users on it.
- Each milestone's exit criteria are checked by a human, not by the agent that did the work.
- A milestone can be *descoped* (by a human, via a new ADR) but never silently slipped.

## Current position

**M0 — 95%.** Everything except human activation of the deploy key (T-005) and branch protection
(T-006) is done. See `.forge/STATE.md`.
