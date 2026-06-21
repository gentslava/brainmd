---
name: brain-ingest
description: Transform a source (document, database query, meeting notes, report) into stable wiki pages with typed edges and full provenance. The core pipeline for growing the brain.
---

# brain-ingest

**Purpose:** Turn a raw source into stable, navigable, provenance-tracked knowledge. Output: one or more wiki pages, a source summary, and typed `## Links` edges.

---

## When to invoke

- A new document, report, database output, or meeting notes needs to be absorbed
- A source has been registered but not yet compiled into wiki pages
- An existing wiki page needs to be updated with new source evidence

---

## Steps

### 1. Read SCHEMA.md

Before any ingest, confirm you know the vault's page types, frontmatter requirements, and routing rules. If SCHEMA.md has changed since last session, re-read it.

### 2. Register the source

Check the Source Registry. If this source is not registered:
- Add it to the Source Registry with: type, location/path, date, status
- Copy or reference the raw content into the vault's raw layer (immutable; do not edit)

### 3. Create a source summary

Using `canon/templates/source.md`:
- Summarize what the source is and what it establishes
- Extract all key facts, numbers, entities, and open questions
- Note caveats: scope, grain, date, sampling, known gaps
- List what needs to be compiled into stable wiki pages

### 4. Identify target wiki pages

For each extracted fact/insight/entity:
- Does a relevant wiki page already exist? If yes, update it.
- Does a new page need to be created? Create it using the appropriate template.
- Is there a metric? Create or update a metric page.
- Is there a decision? Log to Decision Log.
- Is there a contradiction? Log to Contradiction Register.

### 5. Write / update wiki pages

For each page:

**Frontmatter (required):**
```yaml
type: <wiki page type>
status: draft | active
owner: <owner>
updated: YYYY-MM-DD
confidence: high | medium | low | unknown
source:
  - <source name or path>
```

**Content structure:**
- State facts with inline source reference: `[source: <source name>]`
- Mark inferred conclusions: `(inferred)`
- Mark uncertain claims: `to verify`
- Use knowledge level labels: **fact**, **insight**, **hypothesis**, **decision**, **risk**, **open question**

### 6. Add typed edges

In each page's `## Links` section, add typed edges to connect new knowledge to existing:

```
measures::    [[Metric Page]]      # this page measures a metric
part_of::     [[Parent Page]]      # this is a component of something larger
causes::      [[Effect Page]]      # causal relationship
affects::     [[Influenced Page]]  # influence without strict causation
depends_on::  [[Dependency Page]]  # requires this to be true/active
evidence::    [[Source Page]]      # this page is supported by that source
derived_from:: [[Source Page]]     # numbers/claims derived from this source
```

Never use flat wikilinks in `## Links`. Navigation prose can use `[[page]]` freely; `## Links` must be typed.

### 7. Update navigation

- Add the new page(s) to the relevant MOC (map of contents) or domain index
- Do not add to the top-level index unless it is a major entry point
- Check whether any existing pages should now link to the new page(s)

### 8. Run lint (optional but recommended)

```bash
brain lint          # check edge types, frontmatter, up-links
brain gate <file>   # gate the new manifest before considering ingest complete
```

### 9. Log the ingest

Add a brief entry to the vault's operation log: source name, pages created/updated, key facts captured.

---

## Provenance rules (hard constraints)

- Every key number → `derived_from::` or `evidence::` edge to the source, or inline `[source: X]`
- No claim without a source unless explicitly marked `to verify` or `(inferred)`
- `confidence: high` only if confirmed by a document, database, or two independent sources
- If a source contradicts an existing wiki claim: log to Contradiction Register, mark the old claim `outdated`, do not silently overwrite

---

## Quality checklist before closing ingest

- [ ] Source registered in Source Registry
- [ ] Source summary created
- [ ] Each extracted fact has provenance
- [ ] Each new/updated wiki page has valid frontmatter (type, status, owner, updated, confidence, source)
- [ ] Typed edges added in `## Links`
- [ ] New pages added to relevant MOC
- [ ] Contradictions logged if any
- [ ] Operation log updated
