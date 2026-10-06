---
id: QUAL-003
title: SECURITY-BASELINE — Minimum Security Posture
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
tags: [quality, security]
confidence: high
---

# SECURITY-BASELINE

## 1. Secrets

- No private keys, tokens, `.env` files, cookies or credentials in the repo, ever.
- `make secret-scan` runs on every push and in CI; it fails on private-key blocks, `.env` files, and
  common token shapes.
- Key material is generated **outside** the repo tree (`~/.forge-keys/`) and ignored by `.gitignore`
  (`*.pem`, `id_*`, `*_ed25519*`, `.forge-keys/`, `.env*`).
- Only public keys and *metadata* are recorded, in `ops/KEYS.md`.

## 2. Credentials

- One credential per agent workspace, scoped to this single repository, revocable per key.
- Rotation every 30 days or on any unexpected session behaviour. Rotation procedure:
  `ops/KEYS.md` §Rotation.
- Branch protection (no force push, PR required, required checks) is the real safety net — see
  `tasks/OPEN/T-006-branch-protection-and-required-checks.md`.

## 3. Data handling

- The corpus contains **no personal data** and must stay that way. No customer names, phone numbers,
  chat screenshots, or message contents enter the repository.
- Opportunity/persona descriptions must stay aggregated and anonymised.
- If a future spec needs real user data, it needs its own ADR covering storage, retention and
  deletion before it is APPROVED.

## 4. Platform terms

- No scraping, no automated account behaviour, no collection of data that violates Rubika's or
  Baleh's terms of service. This is a product constraint (`ADR-0003`) *and* a security one: a banned
  account is an availability incident.
- Any integration work starts by writing down the platform's current API/automation limits in
  `knowledge/apis/` with a date, because they change.

## 5. Client-side artefacts

- No runtime network requests in shipped artefacts (`ADR-0002`): no CDN, no fonts, no analytics, no
  tracking pixels, no third-party scripts.
- No `eval`, no inline event handlers built from user data, no `innerHTML` with unsanitised input.
- All Persian/user-supplied text rendered through text nodes or an explicit escape helper.

## 6. Supply chain

- No npm/pip dependencies in the repo today. Adding one requires a note in `ops/ENV.md` §Dependencies
  and a reason it cannot be done in stdlib.
- CI installs nothing; it runs `python3 -m unittest` and `tools/forge_lint.py` only.

## 7. Incident response

If a secret is ever committed: rotate first, then purge history, then write a ledger entry naming the
commit range and the rotation timestamp. Do not "just delete the file" in a follow-up commit.
