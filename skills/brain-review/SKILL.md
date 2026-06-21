---
name: brain-review
description: Periodic health review of the brain. Finds orphans, drift, contradictions, stale pages, and what to synthesize next. Uses brain gate, brain lint, and brain untangle. The maintenance skill.
---

# brain-review

**Purpose:** Keep the vault healthy over time. Detect and triage: orphan pages, stale content, broken links, uncompiled knowledge, dandelion violations, drift between pages, and synthesis opportunities. Produce a prioritized action list.

---

## When to invoke

- Monthly (or after every 20+ new pages)
- Before a major decision or synthesis pass
- When the vault feels "heavy" or navigation feels slow
- After a large ingest to check structural integrity

---

## Steps

### 1. Run the diagnostics suite

```bash
brain gate manifest.txt     # gate on all pages (or a subset)
brain lint                  # edge types, frontmatter, up-links, ephemeral
brain diagnose              # orphans, hubs, communities, Gini, surprising (topological)
brain untangle manifest.txt # dandelion rule violations
```

Collect all output. Classify findings by priority.

### 2. Triage findings

**P0 — Fix immediately:**
- Broken wikilinks
- Missing frontmatter on stable pages
- `secret`, `password`, `token`, `PII` in any page
- A critical page with no source (high-confidence claims without evidence)
- Dandelion violations: ephemeral page receiving links from stable pages

**P1 — Fix this session:**
- Stable business pages with no outgoing links (isolated nodes)
- Decisions without `review_after` date
- Key knowledge stuck in Insight Inbox (not compiled into wiki)
- Outdated pages without `status: outdated` marking
- Contradictions not logged in Contradiction Register

**P2 — Backlog for next session:**
- Draft pages not updated in 30+ days
- Low-confidence pages without `to verify` note
- Pages >200 lines that should be split
- Style/formatting cleanup
- Source registry gaps (sources used but not registered)

### 3. Check for drift

Drift = a stable wiki page whose `claim` or facts contradict a more recent source.

For each domain's key metrics pages:
- Compare `updated` date to the most recent source in the Source Registry
- If the metric page is significantly older, flag for update
- If there is a newer Insight Inbox entry that contradicts the metric page, log to Contradiction Register

### 4. Identify synthesis opportunities

From the diagnostics output, look for:
- Clusters with 3+ wiki pages and no synthesis page → candidate for brain-synthesize
- Insight Inbox entries older than 2 weeks that are not yet compiled → compile or discard
- Decision Log entries whose outcomes have now been observed → synthesis opportunity
- Open questions on multiple pages that point at the same gap → synthesis or new ingest target

List: "The following topics are ready for a synthesis pass: <topic A>, <topic B>"

### 5. Check orphan pages

Orphan pages = pages with no incoming links and no outgoing typed edges.

For each orphan:
- Is it intentionally standalone (a template, a schema file)? → Tag `meta`, no action needed
- Is it a real knowledge page that got stranded? → Run brain-link to connect it
- Is it outdated and superseded? → Mark `deprecated`, archive

The diagnostics `--orphans` output gives the list. Target: <5% of total pages as true orphans (excluding templates, schemas, and ephemeral buffers).

### 6. Check hub pages

Hub = page with unusually high in-degree (many pages link to it).

From diagnostics hub output:
- Is it a legitimate MOC or index? → Fine
- Is it a regular wiki page that has become a de facto hub? → Consider splitting or promoting to MOC
- Is it the Insight Inbox (expected high out-degree)? → Fine; monitor

### 7. Check Gini coefficient

The diagnostics report includes a Gini coefficient for link distribution. Higher Gini = more unequal distribution = fewer hubs absorbing most links.

- Gini < 0.5: relatively flat, well-distributed
- Gini 0.5–0.7: some hubs, healthy for a structured wiki
- Gini > 0.7: high concentration; check hub pages for splitting

### 8. Compile the review output

Create a brief review note (or add to operation log):

```markdown
## Brain Review — YYYY-MM-DD

**Vault stats:** N pages, M edges, K orphans (P%), Gini: G

**P0 fixes:** <list or "none">
**P1 fixes:** <list>
**P2 backlog:** <list>

**Synthesis candidates:** <list>
**Stale pages to update:** <list>
**Orphans to connect:** <list>
**Clusters found:** N (see Knowledge Clusters page)

**Next review:** YYYY-MM-DD
```

### 9. Execute P0 and P1 fixes

Fix P0 immediately. Fix P1 in the same session if possible; if not, create explicit backlog items so they are not lost.

P2 goes to backlog — do not block the review on cleanup.

### 10. Log the review

Operation log entry: date, vault size, Gini, orphan count, P0/P1/P2 counts, synthesis candidates identified, next review date.

---

## Scripts reference

| Command | What it checks |
|---|---|
| `brain gate <manifest>` | Gate: frontmatter completeness, claim presence, source presence |
| `brain lint` | Edge types valid, up-links present, ephemeral not receiving stable links |
| `brain diagnose` | Orphans, hubs, communities, Gini, topological surprising connections |
| `brain untangle <manifest>` | Dandelion rule violations (ephemeral ↔ stable link direction) |
