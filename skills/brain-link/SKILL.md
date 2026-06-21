---
name: brain-link
description: Grow connections from a new or recently updated page to existing knowledge. Attach derived_from/evidence to every number. The edge-growing pass that makes the graph dense and navigable.
---

# brain-link

**Purpose:** After a page is created or updated, scan the vault for relevant existing pages and add typed edges between them. Prevent isolated nodes. Ensure every number has provenance.

---

## When to invoke

- After brain-ingest creates a new page
- After a page is significantly updated
- During periodic graph health review (orphan reduction pass)
- When a new concept emerges that likely connects to many existing pages

---

## Steps

### 1. Read the new or updated page

Identify:
- Key topics, metrics, processes, products the page covers
- Numbers that need provenance
- Concepts that might exist elsewhere in the vault

### 2. Search the vault for connection candidates

Search by:
- Metric, process, and product names mentioned on the page
- Key domain terms from the page's title and opening section

For each candidate, confirm it is a real vault page (not a broken link) before adding an edge.

### 3. Assign typed edges in `## Links`

Choose the correct edge type for each connection:

| Edge type | When to use |
|---|---|
| `measures::` | This page is about a metric that tracks something |
| `part_of::` | This page is a component/sub-topic of the target |
| `causes::` | This page describes something that causes the target |
| `affects::` | This page influences the target (without strict causation) |
| `depends_on::` | This page's claims require the target to be true/active |
| `segments::` | This page segments or classifies the target population |
| `evidence::` | The target is a source/report supporting claims on this page |
| `derived_from::` | Numbers on this page are computed from the target source |

Do not use flat `[[wikilink]]` in `## Links`. Use typed edges only there.

### 4. Add provenance to every number

For each key number on the page:
- If it came from a source document → add `derived_from:: [[Source Page]]` or inline `[source: X]`
- If it was computed → add `derived_from:: [[Source]]` with the formula noted
- If it was inferred → mark `(inferred from: <page A>, <page B>)`
- If the source is unknown → mark `to verify`

No key number should appear without one of the above.

### 5. Check for reverse link opportunity (within limits)

For 1–3 existing stable pages that strongly relate to the new page, check whether they should add an outgoing link to the new page. If yes, update their `## Links` section.

**Do not** add the new page to every loosely related page. The dandelion rule: fewer strong links beat many weak ones.

### 6. Run untangle (optional)

```bash
brain untangle manifest.txt
```

Reports dandelion-rule violations: ephemeral pages receiving links from stable pages, or other link-hygiene issues.

---

## Anti-patterns

- Adding `[[page]]` to `## Links` without a type prefix → use typed edges
- Adding a number without `derived_from` or `evidence` → provenance required
- Adding links to every page that mentions the same keyword → be selective
- Adding back-links from every related stable page to the new page → route through MOC/registry instead
