# brainmd Worked Example

A minimal 3-page vault showing the method in action. Domain: a fictional SaaS product with a conversion funnel.

---

## Page 1 — Product

**File:** `03_Wiki/Products/Product - Checkout Flow.md`

```markdown
---
type: product
status: active
owner: your-org
updated: 2026-06-01
confidence: high
source:
  - Product spec v3.2
  - Engineering ADR-17
tags:
  - product
---

# Product - Checkout Flow

The multi-step checkout flow converts trial users to paying customers.

## Ключевые факты

- **fact** — 78% of monthly orders originate from Checkout Flow (source: orders DB, 2026-05).
- **fact** — median completion time: 42 seconds (A/B test 2026-04, n=12 000).
- **insight** — Drop-off is concentrated at step 3 (payment entry); see [[Metric - Checkout Conversion]].

## Связи

part_of:: [[MOC - Products]]
measures:: [[Metric - Checkout Conversion]]
depends_on:: [[Process - Payment Gateway Integration]]
affects:: [[Metric - Monthly Revenue]]
```

---

## Page 2 — Metric

**File:** `03_Wiki/Metrics/Metric - Checkout Conversion.md`

```markdown
---
type: metric
status: active
owner: your-org
updated: 2026-06-01
confidence: high
source:
  - analytics DB (table: funnel_events, 2026-05)
  - Dashboard - Growth KPIs
data_source: PostgreSQL
tags:
  - metric
---

# Metric - Checkout Conversion

End-to-end funnel from landing on the checkout page to confirmed order.

## Определение

`conversion = confirmed_orders / checkout_page_starts`, rolling 30d.

## Текущие значения (2026-05)

| Step | Rate |
|---|---|
| Step 1 → Step 2 | 81% |
| Step 2 → Step 3 | 67% |
| Step 3 → Order  | 63% |
| **End-to-end**  | **34%** |

- **hypothesis** — Payment entry friction (step 3) accounts for ~40% of lost conversions. To verify: run UX session recordings.

## Связи

part_of:: [[MOC - Metrics]]
measures:: [[Product - Checkout Flow]]
derived_from:: [[Source - Funnel Analytics Export 2026-05]]
affects:: [[Metric - Monthly Revenue]]
```

---

## Page 3 — Synthesis

**File:** `03_Wiki/Synthesis/Synthesis - Step-3 Drop-Off Root Cause.md`

```markdown
---
type: synthesis
status: draft
owner: your-org
updated: 2026-06-05
confidence: medium
source:
  - Metric - Checkout Conversion
  - Agent Report - UX Session Analysis 2026-05
  - Decision - Payment UX Redesign
tags:
  - synthesis
---

# Synthesis - Step-3 Drop-Off Root Cause

## Вывод

Step 3 (payment entry) loses 37% of users who reach it. UX session recordings show:

1. **fact** — 62% of abandoners never interact with the CVV field (source: heatmap tool, session n=400).
2. **fact** — Mobile users drop at 2× the rate of desktop (source: funnel DB split, 2026-05).
3. **hypothesis** — Auto-fill suppression on the card form is causing mobile users to give up. (inferred from observation; not yet A/B confirmed.)

## Рекомендация

Enable browser auto-fill + add Apple/Google Pay as alternative. Expected lift: +8 pp end-to-end conversion based on [[Decision - Payment UX Redesign]] modelling.

## Связи

part_of:: [[MOC - Synthesis]]
causes:: [[Metric - Checkout Conversion]]
derived_from:: [[Agent Report - UX Session Analysis 2026-05]]
affects:: [[Product - Checkout Flow]]
```

---

## How `brain gate` and `brain diagnose` Validate This

### `brain gate` (ingest gate)

Run before committing new pages. It checks:

- All three pages have required frontmatter fields (`type`, `status`, `owner`, `updated`, `confidence`, `source`).
- `## Связи` section is present on each `03_Wiki` page.
- No `confidence: high` without at least one named `source`.

If Synthesis has `confidence: medium` with only one source: gate passes but flags it as `P1 — add second source or downgrade to low`.

### `brain diagnose` (graph health)

Run periodically on the vault. It detects:

- **Orphan check** — all three pages link upward to a MOC via `part_of::`, so none appear as orphans.
- **Hub check** — if `MOC - Metrics` had >30 inbound links it would be flagged as an overloaded hub; here it's fine.
- **Broken links** — `[[Agent Report - UX Session Analysis 2026-05]]` must exist in `06_Agents/Agent Reports/`; a missing file is a P0 error.
- **Low-confidence without `to verify`** — Synthesis step-3 hypothesis is marked `(inferred)` and the page body says "not yet A/B confirmed", satisfying the discipline.

The result: three pages, typed edges, every number traceable to a source — no hallucinations injected.
