---
type: graph-rules
status: draft
owner: your-org
updated: 2026-06-20
confidence: medium
source:
  - AGENTS.md
tags:
  - graph
  - rules
---

# Graph Rules

## Naming

Use explicit prefixes for important entities:

- `Product - ...`
- `Process - ...`
- `Metric - ...`
- `Decision - ...`
- `AI Agent - ...`
- `Risk - ...`

## Link Types

Represent relationships through `wikilinks` and section context:

- product -> process;
- process -> role;
- process -> metric;
- product -> metric;
- decision -> process;
- decision -> product;
- risk -> process;
- hypothesis -> metric;
- agent -> process;
- agent -> source;
- department -> role;
- role -> responsibility.

## Иерархия навигации (tiered)

Навигация идёт по уровням: `index.md` → MOC (`04_MOC` + `MOC - Synthesis`) → листовая страница.

- `index.md` держать тонким (~уровень MOC): обзорные карты + MOC + ключевые точки входа + правила. НЕ добавлять в index каждую новую страницу.
- Новую содержательную страницу вешать вверх — на профильный MOC (метрика → MOC - Metrics, процесс → MOC - Processes и т.д.), а не в `index`.
- Кросс-связи между сущностями (продукт↔метрика↔процесс) оставлять — это знаниевый слой; для чтения графа использовать линзы (`-tag:#meta`, локальный граф, группы).
- Машинерия (setup-доки, граф-заметки, шаблоны, архив, эфемерные отчёты, tooling-summaries) помечается тегом `meta` и скрыта из вида графа фильтром `-tag:#meta`.
- Периодические разборы (P&L/мес, воронка/конверсия/мес, дневные/недельные продажи) оформлять паттерном **индекс-реестр (`type: moc`) → листы `YYYY-MM`**: листы одного ряда не ссылаются друг на друга, кросс-периодные сравнения — в индексе. Канон — [[SCHEMA]] §10.1–10.4.
- Проверка покрытия: `python3 scripts/graph_diagnostics.py` — раздел «ПОКРЫТИЕ MOC» показывает листья, не привязанные ни к одному MOC; раздел «хабы» — перегруженные узлы.

## Tags

Use tags for broad filtering, not as a replacement for links.

Examples:

- `#product`
- `#process`
- `#metric`
- `#ai-agent`
- `#risk`
- `#source-summary`

## Frontmatter

Every graph-relevant page must include:

- `type`
- `status`
- `owner`
- `updated`
- `confidence`
- `source`
- `tags`

## Obsidian Graph View

Use Graph View to inspect:

- orphan pages;
- overconnected hub pages;
- missing links between products/processes/metrics;
- duplicate entities.

### Рекомендуемый фильтр — скрыть эфемерный слой

В Obsidian Graph View → Filter (поле "Files to exclude") использовать:

```
-["06_Agents/Agent Reports"] -["02_Sources/Extracted Facts"]
```

Этот фильтр убирает из вида:
- `06_Agents/Agent Reports` — одноразовые отчёты агентов (эфемерный буфер, не знаниевый слой).
- `02_Sources/Extracted Facts` — в т.ч. **Insight Inbox** (out=32): это временный буфер входящих инсайтов, а не узел знаниевого графа. После маршрутизации инсайты переходят в `03_Wiki`; оставаться в графе должны только стабилизированные знания.

> **Правило**: эфемерные страницы (`06_Agents/Agent Reports`, `02_Sources/Extracted Facts`) не являются узлами знаниевого графа. Связи на них оформлять через тип `evidence::`, не как прямые peer-ссылки из `03_Wiki`.

## См. также

- [[Knowledge Graph Queries]] — запросы к графу знаний.
- [[Graphify Notes]] — заметки по queryable knowledge graph.
- [[Smart Connections Notes]] — заметки по semantic layer.
- `scripts/graph_diagnostics.py` — диагностика топологии графа (степени, хабы, orphans, community detection).
