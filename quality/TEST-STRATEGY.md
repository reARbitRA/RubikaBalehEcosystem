---
id: QUAL-002
title: TEST-STRATEGY — Pyramid, Coverage, Flaky Policy
type: quality
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [QUAL-001]
implements: []
traces_to: []
tags: [quality, testing]
confidence: high
---

# TEST-STRATEGY

## 1. Pyramid

| Layer | Share | What it covers | Where |
|---|---|---|---|
| Unit | ~70% | Pure logic: filtering, scoring, status transitions, date maths | `tests/test_*.py` |
| Integration | ~20% | A spec's rules exercised together against a real data file / DOM | `tests/` |
| End-to-end | ~10% | The journeys a human would actually perform (open dashboard → filter → export) | `tests/` (added when a browser harness exists) |

## 2. Coverage floor

- `src/` overall: **70% lines**.
- Anything under `src/auth/`, `src/payments/`, `src/orders/`: **90% lines**.
- New specs: **every AC has a `test_ac_<n>_<slug>` test** — this is a hard gate in
  `tools/forge_lint.py` for any spec at status `IMPLEMENTED` or `VERIFIED`.

## 3. Runner

- Preferred: `pytest`. **Not installed in the current workspace**, so the suite is written to run
  under stdlib `unittest` as well (`python3 -m unittest discover -s tests -v`).
- Rule: no pytest-only fixtures, no `conftest.py` magic. Plain `unittest.TestCase` classes, plain
  `assert*` methods, `tempfile` for anything filesystem-shaped.
- When `pytest` becomes available, `make test` prefers it automatically and nothing else changes.

## 4. Testing single-file HTML artefacts (`ADR-0002`)

We do not screenshot-test. Instead:

1. Keep the artefact's *decision logic* in small pure functions (filter, sort, score, format).
2. Test those functions directly against the embedded dataset.
3. Add a lightweight structural test: the file parses, contains the expected element ids, has no
   `http://`/`https://` resource references, and is valid UTF-8.
4. Anything visual is verified by a human and recorded in the spec's `VERIFIED` transition — that is
   exactly why that transition is human-owned.

## 5. Flaky-test policy

1. A test that fails intermittently is quarantined **with a task id in the skip reason** on the third
   occurrence.
2. A task is opened the same day; quarantine is never a permanent state.
3. `make test` output must state the quarantine count so it cannot be ignored.

## 6. Test data

- Fixture data lives next to the tests in `tests/data/` and is small, checked in, and deterministic.
- The 56-row opportunity dataset is treated as a fixture once SPEC-001 exists; its provenance is
  `brainstorm/BRAIN-001-master-opportunity-table.md`.
