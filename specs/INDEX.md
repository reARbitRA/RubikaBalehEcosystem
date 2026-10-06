---
id: QUAL-004
title: INDEX — All Specs
type: quality
status: ACTIVE
version: 1.1.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: []
tags: [specs, index]
confidence: high
---

# specs/INDEX.md — table of all specs

> The contract index. One row per spec. `status` is the control plane: humans own
> `REVIEW → APPROVED` and `IMPLEMENTED → VERIFIED`.
>
> *Typing note:* this index is typed `quality` (`QUAL-004`) rather than `spec`, because it is a gate
> document about specs, not a spec. Its id prefix therefore does not match its folder — the one
> deliberate exception, recorded here so it does not look like a bug.

| Spec | Title | Area | Status | Version | Plan | Tasks | ACs | Updated |
|---|---|---|---|---|---|---|---|---|
| [SPEC-001](SPEC-001-opportunity-dashboard.md) | Opportunity dashboard | dashboard | REVIEW | 0.1.0 | PLAN-001 | T-002 | AC-1..AC-8 | 2026-10-06 |

## Current approval state

`SPEC-001` is the first behavioural contract in the repository. It is in **REVIEW**, not
`APPROVED`: a human must approve it before product code may be written under `src/`. The repository
still contains only raw thinking (`brainstorm/`), reference output (`knowledge/`), methodology
(`.forge/`), and a reviewable contract. Therefore **no product code is authorised in `src/`** — see
`AGENTS.md` §2, rule 1.

## How a row gets added

1. An agent (or the human) writes `specs/<area>/SPEC-###-<slug>.md` using
   `.forge/templates/spec.md`, status `DRAFT`.
2. The author moves it to `REVIEW` and stops.
3. A human reads §5–6 of the spec and asks: *"could two agents produce materially different systems
   from this?"* If yes, it goes back to `DRAFT`.
4. The human flips `REVIEW → APPROVED`. Only then does the row above become real work.
5. `tools/forge_lint.py` fails the build if any file in `src/` lacks a spec header or a `TRACE.md`
   row, so the table cannot silently fall behind the code.

## Planned specs (from `plans/PLAN-001`)

| Intended spec | Source material | Task |
|---|---|---|
| SPEC-001 — opportunity dashboard | `BRAIN-001` + `knowledge/examples/opportunity-dashboard-v3.md` + audits | T-002 (REVIEW) |
| SPEC-002+ — order tracking / receipts / renewals | `brainstorm/BRAIN-001..005` | T-003 |
