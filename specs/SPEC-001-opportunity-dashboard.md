---
id: SPEC-001
title: Opportunity dashboard — offline Rubika and Baleh opportunity explorer
type: spec
status: REVIEW
version: 0.1.0
owner: agent
created: 2026-10-06
updated: 2026-10-06
supersedes: []
depends_on: [ADR-0002, ADR-0003]
implements: []
traces_to: [BRAIN-001, KNOW-003, KNOW-004, KNOW-005, T-002]
tags: [dashboard, opportunity, m1, offline, rtl]
confidence: medium
---

# SPEC-001 — Opportunity dashboard

> **Human gate:** this draft was advanced from `DRAFT` to `REVIEW` on 2026-10-06. A human must
> approve it before any artefact is written under `src/`.

## 1. Summary

The opportunity dashboard is a single, self-contained browser artefact for exploring the 56
Rubika/Baleh business opportunities in `BRAIN-001`. It gives a Persian-speaking, mobile-first user a
local-only way to understand the inventory, narrow it with transparent filters, inspect the source
facts behind a row, and export the current result set without depending on a messenger API, backend,
or network connection.

The dashboard is an exploration and validation aid, not a live market-data product or a promise of
revenue. It preserves the inventory's hypotheses and makes their stated validation tests and risks
visible.

## 2. Motivation and kill criterion

Messaging-led sellers, channel admins, tutors, and community operators need a fast way to compare
candidate problems before they commit time or money. `BRAIN-001` contains the needed evidence but
its wide 56-row table is difficult to explore on a phone; `KNOW-003` demonstrates an offline dashboard
shape, while `KNOW-004` and `KNOW-005` identify the need for transparent filtering, mobile use, and
decision context.

**Kill criterion.** After implementation, run an observed usability check with five representative
target users. If fewer than three can, unaided and within two minutes, (a) find a named opportunity
using search and at least one filter and (b) export the resulting list, do not invest in further M1
dashboard polish. Preserve the inventory as knowledge and create a new DRAFT spec before changing
this contract.

## 3. User Stories

- **US-1:** As a Persian-speaking founder or operator, I can open the dashboard directly from a file
  on my phone or desktop so that I can inspect the opportunity inventory without installing software
  or connecting to the internet.
- **US-2:** As a strategist, I can search, combine platform/category/verdict/score filters, and sort
  the results so that I can reduce 56 opportunities to a relevant shortlist.
- **US-3:** As a decision-maker, I can open a row's detail panel so that I can see its target customer,
  pain, monetization hypothesis, validation test, risk, and source verdict before acting on it.
- **US-4:** As an operator, I can export the currently visible shortlist as CSV so that I can discuss
  or analyze the same rows elsewhere without copying data by hand.

## 4. Scope

### In scope

- A single `src/index.html` after approval, with inline HTML, CSS, JavaScript, and the embedded
  56-row dataset.
- Persian-first, RTL-native presentation that remains usable at mobile widths.
- Derived KPI, category-distribution, top-opportunity, and score-heatmap views calculated only from
  the embedded data.
- Free-text search; platform, category, verdict, and score-band filters; deterministic sorting;
  cards and table views; detail dialog; reset; and client-side CSV export.
- The original inventory's overall score, realistic monthly revenue estimate, first validation test,
  main risk, and verdict, presented as hypotheses with a source disclaimer.

### Out of scope (explicit)

- Live data, scraping, platform bots, Rubika/Baleh APIs, payment handling, authentication, storage,
  telemetry, or any network service.
- New opportunity rows, new source columns, an invented score formula, or a claim that an inventory
  score/revenue estimate is measured customer evidence.
- A multi-file app, framework, build step, CDN, external font, external image, or runtime dependency.
- Automated recommendations, investment advice, or a replacement for the manual validation tests in
  `BRAIN-001`.

## 5. Behavioral Contract

### 5.1 Interfaces

The approved implementation exposes one directly openable `src/index.html` document with these
interfaces:

1. a Persian-first RTL command area with the dashboard purpose and derived KPI summary;
2. an opportunity explorer with search, platform, category, verdict, score-band, sort, reset,
   card/table-view, and CSV-export controls;
3. cards and a horizontally scrollable table that render the same filtered result set;
4. a dismissible detail dialog for a selected opportunity; and
5. insight panels for category distribution, top opportunities, and one cell per source row in the
   score heatmap.

No interface may require a server, account, browser extension, or network request.

### 5.2 Rules (numbered, testable)

- **R1. Self-contained artefact.** The dashboard SHALL be one UTF-8 `src/index.html` file with all
  data, styles, and scripts inline. It SHALL open and remain functional from `file://` and from a
  basic static HTTP server.
- **R2. Canonical dataset.** The embedded dataset SHALL contain exactly 56 rows corresponding to
  source IDs 1 through 56 in `BRAIN-001`. Each row SHALL retain at least: source ID, idea name,
  category, platform fit, target customer, customer pain, product/service description, monetization,
  realistic monthly revenue, overall score, verdict, first validation test, and main risk.
- **R3. Source fidelity.** `overall score` and `realistic monthly revenue` SHALL be displayed as
  source-inventory values. The dashboard SHALL NOT silently recompute, normalize, or present either
  value as verified market evidence. A visible disclaimer SHALL link the values to the opportunity
  inventory and distinguish hypotheses from validated results.
- **R4. Derived insights.** KPI totals, average score, score-band counts, category counts, top rows,
  and heatmap cells SHALL be derived from the embedded rows at render time. A heatmap cell SHALL
  identify its source row and open that row's detail dialog.
- **R5. Search.** Free-text search SHALL match case-insensitively against the row's idea name,
  category, platform fit, target customer, customer pain, description, verdict, and main risk. An
  empty query SHALL not exclude a row.
- **R6. Combined filters.** Platform, category, verdict, and score-band filters SHALL be combinable
  with AND semantics. A `Both` platform row SHALL match either the Rubika or Baleh platform filter;
  a Baleh-specific row SHALL not match a Rubika-only selection. The score bands SHALL be `80+`,
  `75+`, `70+`, and `below 70` based on the raw overall score.
- **R7. Deterministic sorting and reset.** The default result ordering SHALL be descending overall
  score. The user SHALL be able to sort by ascending score, descending realistic monthly revenue,
  and original source ID. Reset SHALL clear search and every filter, restore descending-score sort,
  and render the full 56-row result set.
- **R8. Equivalent views.** Card and table views SHALL render the same filtered and sorted rows. Each
  row representation SHALL expose the source ID, name, category, platform fit, score, realistic
  monthly revenue, verdict, and a control that opens the detail dialog. A zero-result state SHALL
  clearly state that no rows match and provide a reset path.
- **R9. Detail dialog.** Opening a row SHALL show its source ID and the row's target customer,
  customer pain, product/service description, monetization, first validation test, main risk,
  verdict, score, realistic monthly revenue, and an explicitly labelled execution-path interpretation.
  Escape and an explicit close control SHALL close the dialog without changing filters.
- **R10. CSV export.** Export SHALL create a UTF-8 CSV download containing exactly the current
  filtered-and-sorted rows, in their visible order, with the fields preserved by R2. CSV values SHALL
  be escaped correctly; the export SHALL happen locally and SHALL not upload data or contact a
  network service.
- **R11. Persian-first responsive use.** Primary controls, labels, empty states, and detail labels
  SHALL be Persian and the primary document direction SHALL be RTL (`lang="fa"`, `dir="rtl"`). At a
  320 CSS-pixel viewport, controls and cards SHALL remain operable without page-level horizontal
  scrolling; the data table may scroll inside its own labelled container.
- **R12. Accessible and safe rendering.** Interactive controls SHALL have discernible labels and
  keyboard access. Dataset text SHALL be rendered as text rather than executable markup, so a source
  value cannot create HTML/script content. The implementation SHALL use no third-party runtime
  resources, tracking pixels, remote fetches, or API calls.

### 5.3 Data

| Field | Source | Presentation rule |
|---|---|---|
| `id` | `BRAIN-001` table row number | Unique integer 1–56; retained in views, dialog, and export. |
| `name`, `category`, `platform` | `BRAIN-001` | Retain the source value; use Persian UI labels around it. |
| `target`, `pain`, `description` | `BRAIN-001` | Preserve as row detail and include in free-text matching. |
| `monetization`, `realisticRevenueM`, `score`, `verdict` | `BRAIN-001` | Present as source hypotheses; revenue is millions of toman per month. |
| `validation`, `risk` | `BRAIN-001` | Present in row details and include in free-text matching. |

The canonical source is `BRAIN-001-master-opportunity-table.md`. `KNOW-003` is the legacy visual
reference, not an authority to add data or change inventory values.

### 5.4 Errors and empty states

| Condition | Required behaviour |
|---|---|
| No rows match the current controls | Render a Persian empty state with an accessible reset control; retain the selected controls until reset. |
| A requested source ID is absent | Do not open a blank dialog; leave the current view intact and surface a non-destructive local error message. |
| CSV generation is unavailable in the browser | Keep the dashboard usable, do not send data elsewhere, and show a Persian explanation that local export is unavailable. |
| A dataset field is missing | Render a Persian “source value unavailable” label rather than `undefined`, null, or executable markup. |

## 6. Acceptance Criteria (Given/When/Then — each maps to a test)

- **AC-1:** Given `src/index.html` is opened with no network access, when the dashboard initializes,
  then it renders exactly 56 unique source rows with IDs 1–56 and no external resource request is
  needed. (`test_ac_1_embedded_dataset_and_offline_structure`)
- **AC-2:** Given the full dataset, when a user combines a free-text query with platform, category,
  verdict, and score-band filters, then only rows satisfying every selected constraint are returned
  and `Both` rows match either platform selection. (`test_ac_2_combined_filtering`)
- **AC-3:** Given a filtered result set, when the user selects each supported sort and then Reset,
  then ordering follows the named field, Reset restores descending-score order, and all 56 rows return.
  (`test_ac_3_sorting_and_reset`)
- **AC-4:** Given any filtered result set, when the user switches between cards and table, then both
  views contain the same rows in the same order and expose the required summary fields. (`test_ac_4_equivalent_card_and_table_views`)
- **AC-5:** Given a visible row, when the user opens and closes its detail dialog, then the dialog
  contains the source facts required by R9, Escape/close dismiss it, and filter state is unchanged.
  (`test_ac_5_detail_dialog`)
- **AC-6:** Given a filtered and sorted result set, when the user exports it, then a correctly escaped
  UTF-8 CSV contains exactly those rows in that order and no network request occurs. (`test_ac_6_local_csv_export`)
- **AC-7:** Given a 320 CSS-pixel viewport, when a user opens the Persian RTL dashboard, then primary
  controls and cards remain operable without page-level horizontal scrolling and the table is confined
  to its own scroll container. (`test_ac_7_rtl_mobile_structure`)
- **AC-8:** Given a data field containing markup-like text or a missing value, when it is rendered,
  then it is shown safely as text or as the Persian unavailable-value label, never as executable HTML.
  (`test_ac_8_safe_data_rendering`)

## 7. Non-Functional Requirements

- The artefact uses no build step and no dependency installation, per `ADR-0002`.
- All filtering, sorting, insight derivation, modal display, and export execute in the browser against
  in-memory embedded data.
- The primary interface is RTL and Persian-first; English product names/source values may remain where
  they are the canonical inventory values.
- The page must be valid UTF-8 and remain useful on current mobile and desktop browsers without a
  network connection.
- Visual assessment is human-owned; automated tests verify the structural and decision logic rather
  than pixel output, per `QUAL-002` §4.

## 8. Security Considerations

- No private, customer, payment, account, or messenger data belongs in the embedded dataset.
- The dashboard makes no runtime network request, sends no telemetry, stores no credential, and does
  not invoke platform APIs.
- Data values must be escaped before insertion into HTML; dataset text is treated as untrusted source
  content even when checked into the repository.
- CSV export is generated locally from the visible dataset only. The implementation must mitigate CSV
  formula injection for values beginning with `=`, `+`, `-`, or `@`.
- Source scores and revenues are hypotheses, not investment, financial, or customer evidence; this
  must be clear in the interface.

## 9. Open Questions

None that change this v0.1.0 contract. Any future score formula, live integration, additional
opportunity field, automated recommendation, or product scope change requires a new DRAFT spec (and
an ADR when it changes architecture or product direction).

## 10. Verification Plan

After human approval and implementation:

- `make check` — all repository gates pass.
- `python3 -m unittest discover -s tests -v` — includes the eight `test_ac_<n>_*` tests named in §6.
- `python3 -m http.server 8000 --directory src` — human smoke test of direct static hosting; visual
  and usability verification remains a human gate.
- A local structural test verifies UTF-8, expected controls, inline resources only, no `http://` or
  `https://` runtime resource reference, and the 56-row dataset.

## 11. Trace

plans: `PLAN-001` · tasks: `T-002` · ADRs: `ADR-0002`, `ADR-0003` · sources: `BRAIN-001`,
`KNOW-003`, `KNOW-004`, `KNOW-005`, `QUAL-002`
