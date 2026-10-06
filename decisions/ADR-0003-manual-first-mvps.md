---
id: ADR-0003
title: Manual-first MVPs — never block a product on a platform API
type: adr
status: ACCEPTED
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [ADR-0002]
implements: []
traces_to: [BRAIN-001, BRAIN-003, BRAIN-005]
tags: [product, risk, mvp]
confidence: medium
---

# ADR-0003 — Manual-first MVPs

## Status
ACCEPTED — 2026-10-06. `confidence: medium`: it is the strongest signal in the corpus, but it is a
strategic bet, not a measured fact.

## Context
The opportunity inventory repeatedly flags bot/API access on Rubika and Baleh as *"Requires
verification"* or *"Platform partnership likely required"*, and the corpus's own key assumption is
that "bot/API capability may be limited or unstable, so the MVP must be runnable semi-manually:
form, spreadsheet, simple dashboard, human operator".

Every high-scoring opportunity (order tracking, receipt verification, paid-member renewals) can be
delivered as a human-operated process. None of them *requires* automation to prove value.

## Decision
Every product must have a **coherent manual mode** that an operator can run on day one with no API,
no bot and no integration. Automation is added only after a human has verified demand for the manual
version. Product specs must therefore describe both the operator workflow and (optionally) the
automated one.

## Consequences

### Positive
- Removes the single biggest existential risk (platform dependency) from the critical path.
- Lets us charge money before writing integration code.
- Keeps agent-buildable scope small: forms, tables, reminders, checklists.

### Negative / costs
- Manual mode has weaker margins and worse scalability; it is a bridge, not a destination.
- Two implementations (manual SOP + later automation) can diverge if the spec is not written to
  cover both.
- "Semi-manual" can become a permanent excuse for not automating.

### Neutral
- Pricing model in the inventory (subscription + setup fee) fits a manual-first service well.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Wait for/negotiate platform API access before building | Puts the roadmap behind a third party we do not control. |
| Build the bot first and fall back to manual if blocked | Inverts the risk; the bot becomes the product. |
| Skip manual mode, target only technical users | Contradicts the persona set in `vision/VISION.md` §2. |

## Evidence / provenance
`brainstorm/BRAIN-001-master-opportunity-table.md` (API-risk column),
`brainstorm/BRAIN-003-rubika-baleh-top-opportunities.md` (key assumptions),
`brainstorm/BRAIN-005-low-friction-microsaas-analysis.md`.

## Supersession
None.
