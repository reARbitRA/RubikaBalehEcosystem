---
id: OPS-004
title: RUNBOOK — Operational Procedures
type: ops
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [OPS-001, OPS-002, OPS-003]
implements: []
traces_to: []
tags: [ops, runbook]
confidence: high
---

# RUNBOOK

Each entry: **symptom → diagnose → fix → record**.

---

## RB-1 — Fresh clone does not bootstrap

**Symptom:** `make bootstrap` fails on a new machine.
**Diagnose:** run `make bootstrap` and read which check failed (directory tree, tooling, or document
inventory).
**Fix:**
- Missing directory → `mkdir -p` it and add a `.gitkeep`; check `tools/forge_lint.py`'s expected tree.
- Missing tool → install `python3` ≥ 3.11 and GNU make (`ops/ENV.md` §3).
- Broken frontmatter → `make forge-lint` names the file and the key.
**Record:** append to `.forge/LEDGER.md` under *Learned*.

## RB-2 — Red baseline (`make test` fails on a clean checkout)

**Symptom:** tests fail before you changed anything.
**Rule:** this is your **first task**. Do not work around it, do not delete the test.
**Diagnose:** `python3 -m unittest discover -s tests -v` for the failing test name; check whether the
last ledger entry mentions it as flaky.
**Fix:** fix it, or open a task and move the flaky test to quarantine **with the task id in the skip
reason** (`quality/TEST-STRATEGY.md` §5).
**Record:** ledger entry; `.forge/STATE.md` → "Green baseline: NO" until it is green again.

## RB-3 — `forge-lint` fails

**Symptom:** CI or `make forge-lint` exits non-zero.
**Diagnose:** each error names the file, the rule id (`F1..F8`) and the fix.
**Fix by rule:**
- `F1` frontmatter → add/repair the YAML block per `.forge/CONVENTIONS.md` §2.
- `F2` lifecycle → the `status` is not legal for that `type` (§4).
- `F3` id prefix → the `id` does not match the `type` (§3).
- `F4` duplicate id → rename; ids are globally unique.
- `F5` dangling reference → `depends_on`/`implements`/`supersedes` points at an id that does not exist.
- `F6` src traceability → add a `# SPEC-###` header to the file, or a row in `.forge/TRACE.md`.
- `F7` stale DOING task → finish it, move it, or move it to `tasks/REVIEW/` with a `BLOCKED:` note.
- `F8` ledger missing → a PR touching `src/` must also append to `.forge/LEDGER.md`.
**Record:** nothing extra; the fix commit is the record.

## RB-4 — A secret was committed

**Symptom:** `make secret-scan` (or a human) finds key material or a token in history.
**Order of operations — rotate first:**
1. Revoke/rotate the credential immediately (see `ops/KEYS.md` §4).
2. Purge history (`git filter-repo --path <file> --invert-paths`) or, if that is too risky, treat the
   credential as burned and move on.
3. Append a ledger entry naming the commit range and the rotation timestamp.
**Never:** just delete the file in a follow-up commit and call it done.

## RB-5 — Push fails with SSH permission denied

**Symptom:** `git push` fails after the remote was switched to the SSH alias.
**Diagnose:** `ssh -T git@github-forge-RubikaBalehEcosystem`.
- "Permission denied (publickey)" → the deploy key is not added, not writable, or `~/.ssh/config` is
  wrong. Revert the remote to HTTPS and continue:
  `git remote set-url origin https://github.com/reARbitRA/RubikaBalehEcosystem.git`
- Works → check the remote URL and that the key is the one listed in `ops/KEYS.md`.
**Record:** update `ops/KEYS.md` status column.

## RB-6 — A task has sat in `tasks/DOING/` for > 48h

**Symptom:** `forge-lint` rule `F7`.
**Fix:** either finish it, or write `BLOCKED: <question>` in the task, move it to `tasks/REVIEW/`, and
pick another task. Never leave a zombie DOING card.

## RB-7 — Dashboard looks wrong after an edit

**Symptom:** visual regression in the single-file artefact.
**Diagnose:** `python3 -m http.server 8000` and open it; check the browser console for errors; confirm
no `http(s)://` resource references were introduced (`ADR-0002`).
**Fix:** revert to the last `VERIFIED` commit; visual verification is a human gate
(`quality/DOD.md` — a spec is VERIFIED only by a human).
**Record:** ledger entry + a task if it needs a real fix.

## RB-8 — Platform API behaviour changed

**Symptom:** a documented Rubika/Baleh capability no longer works.
**Fix:** update `knowledge/apis/` with the new observation **and the date**, then re-run the affected
spec's ACs. If a spec's rule is now false, do not edit it — write a `-v2` DRAFT and an ADR.
**Record:** ledger entry; `vision/ROADMAP.md` if a milestone is affected.
