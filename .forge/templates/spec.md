---
id: TEMPLATE-SPEC
title: TEMPLATE — Spec (RFC-style behavioural contract)
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
tags: [forge, template, spec]
confidence: high
---

<!-- TEMPLATE — copy to specs/<area>/SPEC-###-<slug>.md and replace every <...> placeholder. -->

---
id: SPEC-###
title: <title>
type: spec
status: DRAFT                # DRAFT → REVIEW → APPROVED → IMPLEMENTING → IMPLEMENTED → VERIFIED → DEPRECATED
version: 1.0.0
owner: <human|agent|pair>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
supersedes: []
depends_on: [<SPEC-ids>]
implements: []
traces_to: []
tags: [<area>, <milestone>]
confidence: <low|medium|high>
---

# SPEC-### — <Title>

## 1. Summary (≤3 sentences)

## 2. Motivation
Links to vision/brainstorm. Why now, why this shape.

## 3. User Stories
- US-1: As a <role>, I can <capability> so that <benefit>.

## 4. Scope
### In scope
### Out of scope (explicit)

## 5. Behavioral Contract
### 5.1 Interfaces
### 5.2 Rules (numbered, testable)
- R1. <rule>
### 5.3 Data
### 5.4 Errors
| Code | When | Body |
|---|---|---|

## 6. Acceptance Criteria (Given/When/Then — each maps to a test)
- AC-1: Given <state>, when <action>, then <observable outcome>.

## 7. Non-Functional

## 8. Security Considerations

## 9. Open Questions
- OQ-1: <question> → DECIDE via ADR before IMPLEMENTING.

## 10. Verification Plan
`<command>` — all AC-n have a test named `test_ac_n_*`.

## 11. Trace
plans: PLAN-### · tasks: T-###, T-### · ADRs: ADR-####
