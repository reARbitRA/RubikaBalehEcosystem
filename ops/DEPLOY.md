---
id: OPS-002
title: DEPLOY — Deployment and Branch Protection
type: ops
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [ADR-0002]
implements: []
traces_to: []
tags: [ops, deploy, ci]
confidence: high
---

# DEPLOY

## 1. What we deploy

A static single-file artefact (`ADR-0002`). There is no server, no database, no build step. Deployment
is "put the file somewhere that serves it".

## 2. Target

**GitHub Pages from `main`**, serving the repository root (or `/src` once the dashboard is promoted by
T-002).

```bash
# one-time, human action
gh api -X POST repos/reARbitRA/RubikaBalehEcosystem/pages \
  -f source='{"branch":"main","path":"/"}'
```

Until Pages is enabled, the artefact is verifiable locally:

```bash
python3 -m http.server 8000        # then open http://127.0.0.1:8000/src/index.html
```

## 3. Pipeline

```
push to feat/* ──▶ .github/workflows/ci.yml   (currently staged at ops/ci-workflow.yml — see §3.1)
                      ├─ test          (python3 -m unittest)
                      ├─ lint          (no-op while src/ is empty)
                      ├─ typecheck     (no-op while src/ is empty)
                      ├─ secret-scan   (tools/forge_lint.py --secrets-only)
                      └─ forge-lint    (tools/forge_lint.py --base-ref origin/main)
                          │
                          ▼
                   PR (template filled, verification pasted)
                          │
                   human review + APPROVED/VERIFIED gates
                          ▼
                   merge to main ──▶ Pages redeploys automatically
```

Job names in the workflow are exactly `test`, `lint`, `typecheck`, `secret-scan`, `forge-lint` so they
can be listed as required status checks verbatim.

### 3.1 Where the workflow file lives right now

The workflow is committed at **`ops/ci-workflow.yml`** rather than
`.github/workflows/ci.yml`, because the GitHub App the agent workspace authenticates as does not hold
the `workflows` permission and GitHub rejects any push that creates a file under
`.github/workflows/`.

**One human step finishes it:**

```bash
git mv ops/ci-workflow.yml .github/workflows/ci.yml
```

(or grant the App `workflows: write`, then an agent can do the same). Note that GitHub rejects *any*
new file under `.github/workflows/`, including a `.gitkeep`, so the directory itself does not exist in
git yet — the `git mv` creates it.

Until that happens, run the identical gate locally with `make check` — CI is a convenience, the gate is
not optional. `forge-lint` reports the missing directory as warning `T3` so it cannot be forgotten.

## 4. Branch protection (required settings)

Apply to `main` — task `tasks/OPEN/T-006-branch-protection-and-required-checks.md`:

- [x] Require a pull request before merging
- [x] Require status checks: `test`, `lint`, `typecheck`, `secret-scan`, `forge-lint`
- [x] Require linear history
- [x] **Disallow force pushes**
- [x] Require 1 human review

Record the date these were applied here: `______________`.

## 5. Rollback

Because the artefact is one file, rollback is `git revert <merge-commit>` on `main` and a Pages
rebuild. No data migration, no cache invalidation beyond CDN TTL.

## 6. Release cadence

No formal releases until M2. When they start, tag `v<semver>` on `main` and write a ledger entry
naming the tag and the specs that reached `VERIFIED`.
