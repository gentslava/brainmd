---
name: brain-surprising
description: Semantic pass over the graph to find non-obvious cross-domain links missed by topology alone. Surfaces insights like "Contradiction Register entry C1 has no link to the Metric it contradicts." The insight-generator skill.
---

# brain-surprising

**Purpose:** Find connections that the topology cannot see — semantically related pages from different domains that are not yet linked but should be. These cross-domain bridges are often the most valuable insights in a knowledge graph.

Inspired by graphify's semantic surprising connections pass (e.g. it found a Contradiction Register entry and a Metric page that both described the same phenomenon with no cross-link).

---

## When to invoke

- Monthly or after every 3–5 significant ingests
- When you suspect the vault is siloed (different domains with no cross-links)
- After brain-name-clusters reveals clusters with no bridge pages
- When generating novel hypotheses or strategy inputs

---

## Steps

### 1. Run topological surprising first

```bash
brain diagnose
```

The diagnostics output includes a **surprising connections (topological)** section: pairs of pages that are close in the graph but not directly linked. Collect these candidates.

### 2. Expand with a semantic pass

For each pair of domains (clusters) in the vault, generate candidate cross-links by asking:

> "Is there any page in Cluster A whose claim is semantically related to any page in Cluster B, even though they are not linked?"

Focus on:
- Contradiction Register entries ↔ Metric pages (same phenomenon, different angles)
- Decision pages ↔ Process pages (decision affects a process not yet linked)
- Risk pages ↔ Dashboard pages (risk not reflected in monitoring)
- Synthesis pages ↔ Source pages (synthesis uses data not yet attributed)
- Hypothesis pages ↔ Evidence pages (evidence that confirms or refutes a hypothesis)

### 3. Read candidates' `claim` fields

For each candidate pair, read their `claim:` fields. If the claims are semantically related (same metric, same phenomenon, same entity, same root cause), the pages should be linked.

Do not read the full page for initial screening — `claim` is sufficient for 80% of cases.

### 4. Evaluate each candidate

For each candidate pair, decide:

| Assessment | Action |
|---|---|
| Strong semantic connection (same metric/entity/cause) | Add typed edge immediately |
| Likely connection but need to verify | Mark `to verify`; add to open questions |
| Interesting but tenuous | Log as a hypothesis in brain-capture |
| No real connection on inspection | Discard |

### 5. Add typed edges for confirmed connections

Use the correct edge type (see brain-link for the full vocabulary). For surprising connections, the most common types are:
- `affects::` — one page's domain affects another's outcome
- `evidence::` — one page is evidence for or against another's claim
- `causes::` — causal link across domains
- `depends_on::` — one domain's conclusions depend on the other

### 6. Surface as insights

Create a brief note of the most surprising or valuable connections found:

```markdown
## Surprising connections found — YYYY-MM-DD

1. [[Contradiction Register - Entry C1]] ↔ [[Metric - Conversion OSAGO]]
   - The contradiction describes the same June drop the metric tracks. Neither linked to the other.
   - Action: added `affects::` edge from Contradiction to Metric; added `evidence::` from Metric to Contradiction.

2. [[Decision - Channel Prioritization]] ↔ [[Process - Broker Onboarding]]
   - The decision changed broker priority but the process page was never updated.
   - Action: added `affects::` edge; opened review_after on the process page.
```

Log this in the operation log and/or in the vault's graph notes.

### 7. Flag structural gaps

If the pass reveals systematic gaps (e.g. "no Risk page links to any Dashboard" or "synthesis pages never cite their source summaries"), flag these as structural issues for brain-review.

---

## Quality notes

- This skill is generative, not definitive. Not every candidate is a real connection.
- False positives are harmless (a wrong edge can be removed). False negatives (missed connections) are the real cost.
- Bias toward linking: when in doubt, add the edge with the appropriate type and let brain-review prune it if wrong.
- Run this skill with a fresh perspective — semantic similarity is sometimes invisible when you're deep in a single domain.
