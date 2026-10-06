---
id: TEMPLATE-ADR
title: TEMPLATE — Architecture Decision Record
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
tags: [forge, template, adr]
confidence: high
---

<!-- TEMPLATE — copy to decisions/ADR-####-<slug>.md and replace every <...> placeholder. -->

---
id: ADR-####
title: <decision in one line>
type: adr
status: PROPOSED             # PROPOSED → ACCEPTED → SUPERSEDED
version: 1.0.0
owner: <human|agent|pair>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
supersedes: []
depends_on: []
implements: []
traces_to: []
tags: [<area>]
confidence: <low|medium|high>
---

# ADR-#### — <Title>

## Status
PROPOSED — awaiting human acceptance.

## Context
What forces are in play? What problem, what constraints, what evidence?

## Decision
The change we are making, stated as a rule.

## Consequences
### Positive
### Negative / costs
### Neutral

## Alternatives considered
| Option | Why rejected |
|---|---|

## Evidence / provenance
Where in the repo does the justification live (brainstorm IDs, benchmarks, audits)?

## Supersession
If this ADR is later replaced, the replacing ADR lists this one in `supersedes:` and this file's
status becomes `SUPERSEDED`. Never edit the decision text.
