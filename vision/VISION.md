---
id: VISION-001
title: VISION — Product Thesis, Users, Non-Goals
type: vision
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: [BRAIN-001, BRAIN-002, BRAIN-005]
tags: [vision, strategy]
confidence: medium
---

# VISION — RubikaBalehEcosystem

## 1. Thesis

Millions of Iranian sellers, channel admins and community operators run real businesses inside
**Rubika** and **Baleh** — and run them out of DMs, voice notes, screenshots and memory. The
platforms give them reach but no operating system. The result is measurable, daily revenue loss:
forgotten customers, lost payment status, wrong addresses, unanswered questions, expired members who
were never removed, and renewals nobody chased.

**RubikaBalehEcosystem exists to give those operators a lightweight operating layer that works
today, with or without platform APIs.**

The bet is deliberately staged: start with products a human operator can run by hand (forms,
spreadsheets, reminders, SOPs), prove people pay for the *outcome*, then automate the winning slice
into a Micro-SaaS.

## 2. Who it is for

| Persona | What they run | The daily pain |
|---|---|---|
| **Informal seller** | Channel + DMs | Orders scattered across chats; payment/shipping status lives in memory |
| **Channel admin (paid content)** | Paid/exclusive channel | Members added/removed by hand; renewals forgotten; expired members stay |
| **Service provider** | DM-based consulting/classes | Low-quality leads eat the day; no screening, no scheduling, no follow-up |
| **Community operator** | Group with an admin team | Spam, repeat questions, no shift handover, no record of offenders |

## 3. What "success" looks like

- A seller can answer "where is my order?" in under 10 seconds without scrolling.
- No paid member stays inside a channel after their expiry.
- No receipt sits unverified for more than one working day.
- Every product ships as either a self-contained artefact or a semi-manual process that an operator
  can run on day one.

## 4. Non-goals (explicit)

- **No dependence on a platform bot/API being available or stable.** Anything requiring deep
  messenger integration is designed to degrade to a manual operator workflow.
- **No scraping, automation, or data collection that violates the platforms' terms.**
- **No native payment gateway dependency.** Payments are assumed to happen off-platform
  (card-to-card, receipt in chat); we verify, we do not process.
- **No "AI-first" features.** AI is a later accelerator on a workflow that already works manually.
- **No multi-platform expansion** (Eitaa, Soroush, international messengers) until one slice is
  proven on Rubika/Baleh.
- **No enterprise/agency features** (SSO, permissions, audit exports) in the first two milestones.

## 5. Why now

The opportunity inventory (`brainstorm/BRAIN-001-master-opportunity-table.md`) scores 56 candidate
products. The highest-scoring cluster — order tracking, receipt verification, paid-member renewals —
combines pain severity 5/5, frequency 5/5, willingness to pay 5/5 and zero-budget feasibility 4–5/5.
Nothing in that cluster requires an API to start.

## 6. Provenance

This vision was synthesised from the legacy corpus migrated on 2026-10-06:
`brainstorm/BRAIN-001..005` (opportunity inventories and persona/JTBD analyses),
`knowledge/research/audit-dashboard-v2.md`, `knowledge/research/audit-dashboard-v3.md`.
Confidence is `medium`: it is a faithful compression of the corpus, but it has not yet been reviewed
line-by-line by the human owner. T-003 covers that review.
