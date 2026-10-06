---
id: OPS-003
title: KEYS — Credential Inventory (public parts and metadata ONLY)
type: ops
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [QUAL-003]
implements: []
traces_to: [T-005]
tags: [ops, security, keys]
confidence: high
---

# KEYS — key inventory

> **Public keys and metadata only.** Private key material never enters this repository
> (`quality/SECURITY-BASELINE.md` §1). `make secret-scan` fails the build if it ever does.

## 1. Inventory

| Fingerprint | Created | Expires (policy) | Purpose | Status |
|---|---|---|---|---|
| `SHA256:aAqKQTngZhOFHJ1zbSBCygLkVYvIW9jI4TlfnkNKrf4` | 2026-10-06 | 2026-11-06 (30-day rotation) | arena.ai agent push, this repo only | PENDING ACTIVATION |

Public key to paste into *Settings → Deploy keys* (enable **Allow write access**):

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGF5sPF8bzAzlpUwTgrBX934KJskC6gIHwt8uWXWDjGx forge-agent@RubikaBalehEcosystem-20261006
```

Suggested key title on GitHub: `forge-agent 2026-10-06`.

## 2. Where the private key lives

```
~/.forge-keys/RubikaBalehEcosystem_20261006        # private — mode 600, NEVER in the repo
~/.forge-keys/RubikaBalehEcosystem_20261006.pub    # public
```

`~/.forge-keys/` is ignored by `.gitignore` (`.forge-keys/`, `*_ed25519*`, `*.pem`, `id_*`) so even a
mistaken `git add -A` cannot stage it.

## 3. Protocol (generation → activation)

```bash
# 1. Generate OUTSIDE the repo tree
mkdir -p ~/.forge-keys && chmod 700 ~/.forge-keys
ssh-keygen -t ed25519 -a 100 \
  -C "forge-agent@RubikaBalehEcosystem-$(date -u +%Y%m%d)" \
  -f ~/.forge-keys/RubikaBalehEcosystem_$(date -u +%Y%m%d) -N ""

# 2. Print ONLY the public key for the human
cat ~/.forge-keys/RubikaBalehEcosystem_*.pub

# 3. Scope SSH to this repo only
cat >> ~/.ssh/config <<EOF
Host github-forge-RubikaBalehEcosystem
  HostName github.com
  User git
  IdentityFile ~/.forge-keys/RubikaBalehEcosystem_$(date -u +%Y%m%d)
  IdentitiesOnly yes
EOF

# 4. Verify (expected: "Hi reARbitRA/RubikaBalehEcosystem! You've successfully authenticated")
ssh -T git@github-forge-RubikaBalehEcosystem

# 5. Only then, point the remote at the alias
git remote set-url origin git@github-forge-RubikaBalehEcosystem:reARbitRA/RubikaBalehEcosystem.git
```

**Status in this workspace:** steps 1–3 are done. Step 4 has **not** succeeded yet because the human
has not added the key, so step 5 has **not** been run — pushes still go over HTTPS with the
authenticated `gh` session. Do not switch the remote before step 4 succeeds, or every push will fail.

## 4. Rotation (every 30 days, or on unexpected behaviour)

1. Generate a new key per §3 step 1.
2. Add the new public key as a second deploy key.
3. Confirm a push works with the new key.
4. Delete the old deploy key in GitHub settings.
5. Update the table above: old row → `REVOKED <date>`, new row → `ACTIVE`.

Never delete the old key before the new one has pushed successfully.

## 5. Rules

- One key per agent/workspace. Never share a key across tools or people.
- Scope: this repository only. No organisation-wide keys.
- The key is a convenience, not a safety mechanism. Branch protection (no force push, PR required,
  required checks) is what actually bounds the damage of a leaked key — see `ops/DEPLOY.md` §4.
- Commit identity for key-based pushes is set per `.forge/CONVENTIONS.md` §5.
