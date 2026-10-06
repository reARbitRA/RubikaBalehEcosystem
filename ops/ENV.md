---
id: OPS-001
title: ENV — Environment Variables and Dependencies
type: ops
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: []
implements: []
traces_to: []
tags: [ops, env]
confidence: high
---

# ENV — every environment variable, its purpose, where it is set, and an example

## 1. Runtime environment variables

| Name | Purpose | Where set | Example | Required |
|---|---|---|---|---|
| _none_ | The current artefact is a static single-file HTML dashboard (`ADR-0002`). It reads no env vars and makes no network calls. | — | — | — |

Any future variable must be added here **in the same commit** that introduces it (DOD checklist).
Never put a real secret in the *Example* column.

## 2. Local development variables (never committed)

| Name | Purpose | Where set | Example |
|---|---|---|---|
| `FORGE_SESSION_ID` | Optional label used in handoff commits and ledger entries | shell profile | `2026-10-06-01` |
| `FORGE_KEY_DATE` | Date suffix used when generating deploy keys | shell profile | `20261006` |

`.env` files are git-ignored (`.gitignore` → `.env*`). Copy `.env.example` if one is ever added; do not
create `.env` inside the repository tree — keep it in your home directory.

## 3. Dependencies

| Tool | Version used here | Why | Pinned? |
|---|---|---|---|
| `python3` | 3.11.2 | test runner + `forge-lint` + secret scan | system |
| `make` | GNU make 4.x | task entry points (`make test`, …) | system |
| `git` | ≥ 2.30 | branch/commit protocol | system |
| `gh` | latest | PRs, branch protection queries | system |
| `pytest` | **not installed** | preferred test runner when present; suite is runner-agnostic (`quality/TEST-STRATEGY.md` §3) | — |
| `node` | present in workspace | not used by the product (`ADR-0002`: no build step) | — |

Adding a runtime dependency (npm/pip) requires: a line in this table, a reason it cannot be done with
the stdlib, and a mention in `quality/SECURITY-BASELINE.md` §6.

## 4. Toolchain bootstrap on a fresh machine

```bash
git clone <repo> && cd RubikaBalehEcosystem
make bootstrap     # verifies the tree and tooling
make test          # green baseline, zero installs
```
