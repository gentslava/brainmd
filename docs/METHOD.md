# brainmd Method

A structured approach to building an LLM-readable second brain: typed knowledge graph, provenance discipline, and dense-but-navigable notes.

---

## The 3-Graph Model

Every note in the vault lives in one of three layers:

| Layer | Purpose | Examples |
|---|---|---|
| **Navigation** | Entry points and wayfinding | `index.md`, MOC files (`04_MOC/`), dashboards (`05_Dashboards/`) |
| **Knowledge** | Stable compiled knowledge | `03_Wiki/` — products, metrics, processes, synthesis, decisions, strategy |
| **Ephemeral** | Transient buffers | Agent reports (`06_Agents/Agent Reports`), Insight Inbox (`02_Sources/Extracted Facts/`) |

Navigation → Knowledge → Ephemeral is a one-way promotion path. Ephemeral material gets compiled into Knowledge; Knowledge gets surfaced via Navigation. The ephemeral layer is hidden from the graph view (`-tag:#meta` filter) to keep the visual graph clean.

---

## Typed Edges

Plain wikilinks are untyped. brainmd adds explicit edge types in the `## Связи` section of each page:

```markdown
## Связи

part_of:: [[MOC - Metrics]]
measures:: [[Process - Checkout]]
causes:: [[Metric - Conversion Rate]]
affects:: [[Decision - Pricing 2026-Q1]]
derived_from:: [[Source - Q4 Revenue Report]]
evidence:: [[Agent Report - Cohort Analysis 2026-05]]
depends_on:: [[Metric - Traffic]]
example_of:: [[Synthesis - Funnel Degradation Pattern]]
```

The vocabulary is intentionally small so queries stay simple. These edge types power Dataview lenses (see `canon/Knowledge Graph Queries.md`).

---

## Dandelion Rule

Each stable page (`03_Wiki`) carries exactly **one primary claim** in frontmatter:

```yaml
claim: "<the key takeaway in one sentence, with a number if there is one>"
```

This is the "dandelion head" — a tight summary that lets an LLM agent decide in one token whether the full page is relevant, without reading it. Supporting evidence hangs off the stem (the page body). Without a claim, the page is a blob; with it, the page is a queryable node.

---

## Provenance → Zero Hallucinations

Every number on a stable page must trace to a source:

1. `source:` in frontmatter lists the data origin (DB, spreadsheet, document, code path).
2. Key figures in the body reference `derived_from::` or carry an inline `(source: ...)` note.
3. Uncertain claims are flagged `(inferred)` or `(ambiguous)`.
4. Contradictions go to `Contradiction Register.md` — never silently overwritten.
5. `confidence: high` is reserved for DB/document/code-confirmed facts; unverified claims get `confidence: low` + `to verify` marker.

The discipline is simple: if you cannot cite it, you cannot assert it as fact.

---

## Dense Graph, Read via Lenses

The knowledge graph is intentionally dense — business entities are genuinely interconnected. The solution is not to cut links but to **read through lenses** (filtered Dataview queries or Obsidian graph filters), not to stare at the full hairball.

Lens patterns (see `canon/Knowledge Graph Queries.md`):
- By edge type: show only `measures` edges → see which pages quantify which processes.
- By domain: `FROM "03_Wiki/Metrics"` — isolate one folder.
- Local graph (depth 1–2): navigate from a single open page.
- Graph filter by path: `path:"03_Wiki/Synthesis"` in Obsidian.

---

## Claim / Entity Sub-Document Nodes

Two sub-document constructs extend the graph without adding full pages:

**claim::** (frontmatter) — the single-sentence summary that makes pages queryable at retrieval time.

**entity::** (in `## Связи`) — a named concept that is important enough to reference but too small for its own page:

```markdown
entity:: segment-B-partners
entity:: channel-X-suspended
```

Agents and Dataview queries can find these without the concept needing its own file.

---

## Lifecycle

```
Raw source
  → 02_Sources/Source Summaries/   (cleaned summary)
  → 02_Sources/Extracted Facts/Insight Inbox  (quick buffer)
  → 03_Wiki/<domain>/              (compiled stable page, with claim + typed edges)
  → 04_MOC/<domain>                (registered in relevant MOC)
  → 05_Dashboards/                 (surfaced if signal is recurring)
```

Agents run `brain gate` (ingest gate — validates frontmatter, claim, source) and `brain diagnose` (graph health — broken links, orphans, overloaded hubs) to keep the graph valid. See `scripts/` for tooling.
