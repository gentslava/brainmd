---
type: graph-queries
status: draft
owner: cvo
updated: 2026-06-20
confidence: medium
source:
  - graph rules
tags:
  - graph
  - queries
---

# Knowledge Graph Queries

## Business Queries

- Which products have no metrics?
- Which processes have no owner?
- Which metrics have no data source?
- Which decisions affect ОСАГО?
- Which AI agents touch support?
- Which risks affect margin?
- Which hypotheses have no validation metric?

## Knowledge Health Queries

- Pages with `confidence: low`.
- Pages with `status: draft`.
- Pages without outbound links.
- Pages not linked from any MOC.
- Source summaries not linked to Wiki pages.

## Линзы для чтения плотного графа

Граф знаний **плотный** — это отражение реальной связности бизнеса (метрики↔синтезы↔продукты↔решения, ОСАГО↔кроссы↔финансы). Доказано (3-way A/B): резать связи **нельзя** — это вредит извлекаемости. Поэтому плотный граф не читают целиком; в него входят **точечно через линзы**, фильтруя отображение, а не данные. Требуется плагин Dataview.

### Линзы по типу связи (один слой графа за раз)

```dataview
TABLE WITHOUT ID file.link AS "Лист", part_of AS "part_of → хаб"
FROM "03_Wiki" WHERE part_of SORT file.name
```
```dataview
TABLE WITHOUT ID file.link AS "Метрика", measures AS "measures →"
WHERE measures
```
```dataview
TABLE WITHOUT ID file.link AS "Источник", causes AS "causes →"
WHERE causes
```
```dataview
TABLE WITHOUT ID file.link AS "Решение/риск", affects AS "affects →"
WHERE affects
```
```dataview
TABLE WITHOUT ID file.link AS "Страница", derived_from AS "derived_from →"
WHERE derived_from
```
```dataview
TABLE WITHOUT ID file.link AS "Источник", depends_on AS "depends_on →"
WHERE depends_on
```
```dataview
TABLE WITHOUT ID file.link AS "Страница", evidence AS "provenance →"
WHERE evidence
```

### Линзы по домену (один проект изолированно)

```dataview
LIST FROM "03_Wiki/Metrics" SORT file.name
```
Замените папку на нужный домен: `03_Wiki/Synthesis`, `03_Wiki/Products`, `03_Wiki/Processes`, `03_Wiki/Strategy`, `03_Wiki/Decisions`, `03_Wiki/Finance`.

### Чтение через Obsidian Graph View

Плотный граф читают **не целиком**, а через фильтры отображения:
- **Local graph** (depth 1–2) от открытой страницы — её окрестность, а не весь клубок. Это основной способ навигации по плотному графу.
- **Graph filter по домену:** `path:"03_Wiki/Metrics"` — показать только метрики; добавьте `-path:"06_Agents/Agent Reports" -path:"Extracted Facts" -file:log` чтобы скрыть эфемерный слой (это уже зашито в `graph.json`).
- **Groups (раскраска по доменам)** настроены в `.obsidian/graph.json` — ОСАГО, Биржа, метрики, синтезы, стратегия, решения видны разными цветами; кластеры-домены различимы даже в плотном графе.

### Здоровье графа

```dataview
TABLE status, confidence FROM "03_Wiki" WHERE confidence = "low"
```
```dataview
TABLE WITHOUT ID file.link AS "Лист без part_of"
FROM "03_Wiki" WHERE !part_of AND type != "moc"
```

## Связанные страницы

[[Graph Rules]] · [[Smart Connections Notes]] · [[SCHEMA]]
