---
name: brain-synthesize
description: When a topic has enough evidence, compile a synthesis page — a management-level conclusion that rises above individual facts. Produces a synthesis page with an evidence table and typed links.
---

# brain-synthesize

**Purpose:** When multiple source pages and wiki pages converge on a domain, compile a synthesis page that answers the key management question for that domain. Not a summary — a conclusion.

---

## When to invoke

- Three or more wiki pages in a domain share a common thread and no synthesis page exists yet
- The Insight Inbox contains multiple related entries pointing at a single conclusion
- A dashboard or decision page references a conclusion that isn't written down anywhere stable
- During brain-review when orphan clusters suggest an uncompiled synthesis

---

## Steps

### 1. Define the synthesis question

Before writing, state the question this synthesis answers. Example: "Why did conversion drop in June?" or "What is the true unit economics of product X?"

The question drives the synthesis. Without a clear question, you get a summary, not a synthesis.

### 2. Collect source material

Gather:
- Relevant wiki pages (metrics, products, processes, decisions)
- Source summaries and agent reports
- Insight Inbox entries in the domain
- Any existing partial synthesis or dashboard notes

List what you are working from before writing.

### 3. Assign knowledge levels to each claim

Every claim in the synthesis must be labeled:

- **fact** — confirmed by a source; cite it
- **insight** — derived from multiple facts; note the derivation
- **hypothesis** — working assumption; mark `to verify`
- **decision** — a choice made; cite who/when
- **risk** — a threat with evidence; note severity
- **open question** — unanswered; mark explicitly

Never blend levels without labeling them. A synthesis that mixes facts and hypotheses without labeling is actively harmful.

### 4. Write the synthesis page

Use `canon/templates/synthesis.md`. Required:

**Frontmatter:**
```yaml
type: synthesis
status: draft
confidence: medium  # rarely high until peer-reviewed
source:
  - <list each source wiki page or document>
```

**Body:**
- Context: why this synthesis exists
- Key findings: fact/insight/hypothesis/decision labeled bullets
- Evidence table: metric | value | source | confidence
- Open questions: what remains unresolved
- Links: typed edges to all source pages

### 5. Set confidence honestly

- `high`: multiple independent sources confirm the same conclusion, no material contradiction
- `medium`: one solid source or multiple weak ones; some inference
- `low`: mostly inferred; needs verification
- `unknown`: significant gaps; synthesis is exploratory

### 6. Wire typed edges

```
part_of::     [[Domain MOC]]
evidence::    [[Source Page A]]
evidence::    [[Source Page B]]
measures::    [[Metric Page]]
derived_from:: [[Database Query or Report]]
```

### 7. Check for contradictions

Before finalizing: search existing wiki pages for claims that contradict the synthesis. If found:
- Log to Contradiction Register
- Mark the contradicting old claim as `outdated` with a note
- Reference both in the synthesis's open questions if unresolved

### 8. Update navigation

- Add to relevant MOC
- Add `evidence::` or `part_of::` edges from the synthesis back to the supporting pages
- If this synthesis supersedes an older one: mark the old one `deprecated` + `superseded_by:`

### 9. Log the synthesis

Operation log entry: synthesis title, question answered, sources used, open questions remaining.

---

## Quality gate before marking active

- [ ] All findings labeled with knowledge level
- [ ] All numbers have provenance (inline or via `derived_from`/`evidence`)
- [ ] Contradictions logged if any
- [ ] Typed edges in `## Links`
- [ ] Added to domain MOC
- [ ] `confidence` is honest
