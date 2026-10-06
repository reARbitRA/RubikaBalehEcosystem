---
id: VISION-002
title: PRINCIPLES — Values That Break Ties
type: vision
status: ACTIVE
version: 1.0.0
owner: human
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [VISION-001]
implements: []
traces_to: []
tags: [vision, principles]
confidence: high
---

# PRINCIPLES

> When two options are both defensible, these decide. Ordered by weight.

1. **Revenue-loss-first.** We build the thing that stops money leaking *this week* before the thing
   that is elegant. "Lost order = lost money" beats "nicer dashboard".
2. **Manual before automated.** If a human with a form and a spreadsheet can deliver the outcome,
   ship that first. Automation is earned by demand, not assumed by ambition.
3. **Works with zero API access.** Every product must have a coherent manual mode. Platform API
   changes must never be able to take the product offline.
4. **Self-contained artefacts.** Deliverables should run offline, from one file, with no build step
   and no CDN (see `ADR-0002`). Portability beats sophistication.
5. **Persian-first, RTL-native.** The user is Persian-speaking and mobile-first. Persian copy is the
   primary language, not a translation layer.
6. **Spec before code.** No line of `src/` exists without an APPROVED spec it traces to. This is not
   bureaucracy; it is what makes a stateless agent possible.
7. **Evidence over opinion.** A claim about customers needs a source: a DM, an interview, a number
   from the inventory. Otherwise it is a brainstorm, not a fact.
8. **Small, mergeable, verifiable.** One task, one branch, one PR, one pasted verification output.
   Big diffs are how context dies.
9. **Never guess.** Ambiguity becomes a `BLOCKED:` question in a task, not a silent assumption in
   the code.
10. **The repo is the brain.** Anything not written down did not happen.
