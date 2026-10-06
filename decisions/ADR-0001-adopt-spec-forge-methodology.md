---
id: ADR-0001
title: Adopt the SPEC-FORGE spec-driven methodology for this repository
type: adr
status: ACCEPTED
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: [T-001]
tags: [methodology, forge]
confidence: high
---

# ADR-0001 — Adopt the SPEC-FORGE spec-driven methodology

## Status
ACCEPTED — 2026-10-06, by the repository owner.

## Context
The repository started as ~100 KB of loose markdown: opportunity inventories, persona analyses,
three iterations of a dashboard HTML artefact, and two audits of it. There was no entry point, no
status information, no way for a new agent (or the owner, three weeks later) to tell what was
current, what was decided, or what was next. Every session began by re-reading everything.

Work is expected to be done by **stateless agent sessions** that die after each push. Continuity
therefore cannot live in a chat window; it has to live in the repository.

## Decision
Adopt SPEC-FORGE in full:

- `AGENTS.md` is the single entry point and constitution.
- Every document carries lifecycle `status` in frontmatter; humans own the `REVIEW → APPROVED` and
  `IMPLEMENTED → VERIFIED` transitions.
- Specs are RFCs with numbered rules and Given/When/Then ACs; each AC becomes a `test_ac_*` test.
- `.forge/{STATE,LEDGER,TRACE,GLOSSARY,CONVENTIONS}.md` plus `.forge/templates/` provide the memory.
- `tools/forge_lint.py` enforces the methodology in CI.
- Deploy-key credential protocol in `ops/KEYS.md`, with branch protection as the real safety net.

## Consequences

### Positive
- A brand-new agent can bootstrap from one file and know who it is, what is done, and what is next.
- Spec drift becomes detectable (`forge-lint`) instead of anecdotal.
- Decisions become immutable records (`decisions/`), so "why" survives.
- Verification is executed and pasted, not asserted.

### Negative / costs
- Ceremony overhead on small changes: every doc needs frontmatter, every task a card, every session
  a handoff.
- Two human gates (`APPROVED`, `VERIFIED`) can stall an agent that is otherwise ready to ship.
- The initial scaffold is a large docs-only diff (~40 files) with no product value by itself.

### Neutral
- `src/` stays empty until M1, which means `make lint`/`make typecheck` are no-ops for now.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Keep a flat markdown dump and prompt agents with prose | Reproduces the amnesia anti-pattern; no status, no traceability. |
| Issue tracker (GitHub Issues/Projects) as the source of truth | Not diffable with the code, not readable in a fresh clone, no spec format. |
| Full ADR + spec process but no CI gate | Rules decay within weeks without enforcement. |
| Heavy framework (e.g. arc42 + custom tooling) | Overkill for a single-repo, single-operator project. |

## Evidence / provenance
The methodology is documented in the owner's SPEC-FORGE brief (the source of `AGENTS.md`).

## Supersession
None.
