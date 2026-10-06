---
id: ADR-0002
title: Ship artefacts as a single self-contained HTML file with no build step
type: adr
status: ACCEPTED
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: [KNOW-003]
tags: [frontend, delivery, offline]
confidence: high
---

# ADR-0002 — Single self-contained HTML file, no build step

## Status
ACCEPTED — restates a decision already visible in the legacy material; recorded here so it stops
being re-litigated every session.

## Context
Three iterations of the opportunity dashboard were produced (`knowledge/examples/` v1, v2, v3) and
audited twice (`knowledge/research/`). Every iteration converged on the same constraint set:
self-contained, no CDN, no npm, no external asset, runs offline, mobile-first, RTL, KONKRED-branded.
The v3 audit explicitly frames the goal as a "KONKRED-grade market intelligence product" delivered
as one file the user can open directly in a browser.

The audience is Iranian founders/strategists on mobile connections where a CDN dependency is both a
reliability and a censorship-surface risk.

## Decision
Product artefacts are delivered as a **single self-contained `index.html`**: inline CSS, inline JS,
inline data, no external requests at runtime, no build tooling, no framework. If a future artefact
genuinely needs a build step, that requires a new ADR.

## Consequences

### Positive
- Zero install, zero network, zero supply-chain risk; the file is the deployment.
- Diffable and reviewable as one artefact; trivially hostable (GitHub Pages, any static host, a USB stick).
- Works for an agent session: no `npm install` step to fail or drift.

### Negative / costs
- No module system, no tree-shaking, no TypeScript, no component reuse across files.
- Large single files (v3 is ~53 KB of markdown containing the HTML) become awkward to edit.
- Testing a single HTML file requires either a headless browser or extracted pure functions.

### Neutral
- Test strategy for HTML artefacts is defined in `quality/TEST-STRATEGY.md` §4 (extract pure logic
  into testable functions; assert on data, not pixels).

## Alternatives considered

| Option | Why rejected |
|---|---|
| Vite/React SPA with CDN | Violates offline/no-dependency constraint; adds a build step the operator cannot run. |
| Multiple HTML/CSS/JS files | Breaks "one file you can open and send to someone". |
| Server-rendered app | Contradicts the static, zero-infra deployment goal for M1. |

## Evidence / provenance
`knowledge/examples/opportunity-dashboard-v1.md`, `-v2.md`, `-v3.md`;
`knowledge/research/audit-dashboard-v2.md`; `knowledge/research/audit-dashboard-v3.md`.

## Supersession
None.
