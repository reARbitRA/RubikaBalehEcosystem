---
id: FORGE-003
title: CONVENTIONS — Code, Docs, Git and Test Rules
type: forge
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [FORGE-001]
implements: []
traces_to: []
tags: [forge, conventions, style]
confidence: high
---

# CONVENTIONS

## 1. Where things go (the rule of thumb)

> If you are unsure where something goes, it goes in `brainstorm/`. Promotion to `specs/` is a
> deliberate act, performed by a human or an ARCHITECT-role session, and it must be reviewed.

| Kind of content | Destination |
|---|---|
| Why we exist, who for, what we won't do | `vision/VISION.md` |
| Tie-breaker values | `vision/PRINCIPLES.md` |
| Milestones + exit criteria | `vision/ROADMAP.md` |
| Raw, unfiltered, low-ceremony thinking | `brainstorm/YYYY-MM-DD-slug.md` |
| Behavioural contract | `specs/<area>/SPEC-###-slug.md` |
| One decision + context + consequences | `decisions/ADR-####-slug.md` |
| Spec → ordered sized tasks | `plans/PLAN-###-slug.md` |
| One mergeable unit of work | `tasks/T-###-slug.md` |
| Vetted patterns, worked examples, API quirks, research | `knowledge/{snippets,examples,apis,research}/` |
| Done/test/security policy | `quality/` |
| Deploy, env, runbooks, keys | `ops/` |
| Product code | `src/` (must trace to a SPEC) |
| Methodology machinery | `.forge/` (never product code) |

## 2. Document frontmatter

Every `.md` outside `src/` **except** `README.md` and `.forge/templates/**` carries the universal
frontmatter defined in the methodology:

```yaml
---
id: SPEC-012          # globally unique; prefix encodes type (see §3)
title: Human readable title
type: spec            # see §3
status: APPROVED      # see §4
version: 1.2.0        # semver; MINOR on scope change, MAJOR on breaking
owner: human          # human | agent | pair
created: 2025-01-14   # ISO date, never changes
updated: 2025-01-20   # ISO date, bumped on every edit
supersedes: []        # IDs this replaces
depends_on: [SPEC-001]
implements: []        # plans/tasks: which spec(s)
traces_to: []         # commits, PRs, tests (free-form, not validated for existence)
tags: [auth, mvp, m1]
confidence: high      # low | medium | high
---
```

`forge-lint` enforces: required keys present, `version` is semver, dates are ISO, `type` matches the
`id` prefix, `status` is legal for that type, and all IDs are unique across the repo.

## 3. ID scheme

| Type | Prefix | Example |
|---|---|---|
| forge | `FORGE-###` | `FORGE-001` |
| vision | `VISION-###` | `VISION-001` |
| brainstorm | `BRAIN-###` | `BRAIN-001` |
| spec | `SPEC-###` | `SPEC-012` |
| adr | `ADR-####` | `ADR-0007` |
| plan | `PLAN-###` | `PLAN-004` |
| task | `T-###` | `T-032` |
| knowledge | `KNOW-###` | `KNOW-003` |
| quality | `QUAL-###` | `QUAL-001` |
| ops | `OPS-###` | `OPS-001` |
| state | `STATE-###` | `STATE-001` |
| ledger | `LEDGER-###` | `LEDGER-001` |

## 4. Lifecycles (extended from the base methodology)

```
forge:     ACTIVE | ARCHIVED
vision:    ACTIVE | SUPERSEDED | ARCHIVED
brainstorm: SEED → GROWING → PROMOTED | ABANDONED
spec:      DRAFT → REVIEW → APPROVED → IMPLEMENTING → IMPLEMENTED → VERIFIED → DEPRECATED
adr:       PROPOSED → ACCEPTED → SUPERSEDED
plan:      DRAFT → ACTIVE → COMPLETE → ARCHIVED
task:      OPEN → DOING → REVIEW → DONE | BLOCKED
knowledge: DRAFT → CURRENT → SUPERSEDED | ARCHIVED
quality:   DRAFT → ACTIVE → SUPERSEDED
ops:       DRAFT → ACTIVE → SUPERSEDED
state:     ACTIVE (overwritten)
ledger:    ACTIVE (append-only)
```

## 5. Git

### Branches
```
main                      protected; humans merge only; always deployable
feat/T-###-slug           one task, one branch, one PR
spec/SPEC-###-slug        agent-drafted specs for human review (docs-only PRs)
chore/forge-*             methodology-only changes
```

### Commits
`<type>(<scope>): <summary> [<TASK-ID>] [<SPEC-ID>]`
types: `feat fix test docs refactor chore spec adr`

Examples:
- `feat(orders): add order status transitions [T-014] [SPEC-003]`
- `spec(orders): draft order tracking contract [T-002] [SPEC-003]`
- `chore(forge): handoff 2026-10-06-01`

### Commit identity
Set per workspace, before the first commit:
```bash
git config user.name  "forge-agent"
git config user.email "forge-agent@users.noreply.github.com"
```
**In this workspace** the identity is the authenticated account
(`reARbitRA <129707861+reARbitRA@users.noreply.github.com>`), so agent commits are attributable to
the human owner rather than a bot user. If you want a distinguishable bot author, switch to the
deploy-key flow in `ops/KEYS.md` (T-005) and re-set the identity then.

### Handoff commit
`chore(forge): handoff <session-id>` is always the **last** commit of a session.

## 6. Code style (applies to `src/`, currently empty)

- **HTML/CSS/JS only, no build step** (see `ADR-0002`). A single self-contained `index.html` is a
  valid deliverable.
- 2-space indent, UTF-8, LF line endings, trailing newline at EOF.
- Semicolons in JS; single quotes; `const`/`let`, never `var`.
- Persian-facing UI text lives in the document as UTF-8 (no escaped entities); `dir="rtl"` on
  Persian containers, `lang` attributes set correctly.
- No external CDN, no runtime network calls, no tracking pixels (see `ADR-0002`,
  `quality/SECURITY-BASELINE.md` §5).
- Every file under `src/` starts with a header comment naming its spec:
  `/* SPEC-003 §5.2 — order status transitions */` (or `<!-- SPEC-003 -->` for HTML).
- Data tables embedded in artefacts must cite their source document in a comment.

## 7. Test style

- One test per AC, named `test_ac_<n>_<slug>`, e.g. `test_ac_2_expired_token_410`.
- Tests must run under **both** `pytest` and stdlib `unittest` (plain `unittest.TestCase`, no pytest
  fixtures) so `make test` stays green with zero installs.
- No `skip`/`xfail` without a task ID in the reason string.
- Flaky policy: 3 failures → quarantine + open a task (see `quality/TEST-STRATEGY.md`).

## 8. Secrets

- Never commit private keys, `.env`, tokens, cookies, or credentials. `make secret-scan` enforces it.
- Public keys and *metadata only* go in `ops/KEYS.md`.
- Key material is generated outside the repo tree (`~/.forge-keys/`) and ignored via `.gitignore`.
