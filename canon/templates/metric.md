---
type: metric
status: draft
owner: <owner>
updated: YYYY-MM-DD
confidence: medium
metric_owner: <team or person responsible>
data_source: <PostgreSQL | ClickHouse | Google Sheets | API | manual>
source:
  - <source document or database>
review_after: YYYY-MM-DD
tags:
  - metric
---

# Metric — <Metric Name>

## Definition

<What does this metric measure? One precise sentence. Include the unit.>

**Unit:** <unit>
**Grain:** <row-level grain — e.g. per policy, per day, per user>
**Period:** <typical reporting period>

## Calculation

```
<formula or pseudocode>
```

**Filters / exclusions:** <describe any>
**Known caveats:** <describe edge cases>

## Current benchmark

| Period | Value | Source | Confidence |
|---|---|---|---|
| <YYYY-MM> | <value> | <source> | high / medium / low |

## History / trend

<!-- Add rows as data accumulates -->

| Period | Value | Notes |
|---|---|---|

## Targets / thresholds

| Threshold | Value | Meaning |
|---|---|---|
| Green | >X | Normal |
| Yellow | X–Y | Attention |
| Red | <Y | Action required |

## Open questions

- [ ] <question about this metric> `to verify`

## Links

```
measures::    [[<product or process this metric tracks>]]
part_of::     [[<parent metric or MOC>]]
depends_on::  [[<upstream metric or process>]]
affects::     [[<downstream outcome>]]
derived_from:: [[<source page>]]
evidence::    [[<report or query page>]]
```
