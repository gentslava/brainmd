---
name: brain-query
description: Answer a question over the brain WITH full provenance and anti-hallucination discipline. Cite source pages and numbers. Say "not found" rather than invent. The retrieval skill.
---

# brain-query

**Purpose:** Answer a domain question using only what is in the vault, with full provenance. The answer must be traceable to source pages. If the vault does not contain the answer, say so — do not invent.

---

## When to invoke

- A user asks a question that should be answerable from vault knowledge
- A decision needs to be made and the relevant facts should be retrieved
- An agent needs to check what is known before starting an ingest or synthesis
- Verifying whether a claim is already documented before adding it

---

## Steps

### 1. Parse the question

Identify:
- **Domain:** what area of the vault is this about?
- **Specific entity:** which metric, product, process, decision?
- **Time scope:** is this historical, current, or trend?
- **Answer type:** a number, a yes/no, a process description, a decision rationale?

### 2. Navigate to the relevant pages

Start from the vault's index or the relevant MOC. Do not search randomly.

Navigation path:
```
index.md
  → domain MOC (metrics, products, processes, finance, etc.)
    → relevant wiki page
      → source summary or evidence page if more detail needed
```

Read the `claim:` field of each candidate page before reading the full content. `claim` is the fast filter.

### 3. Collect answer components

For each relevant page:
- Note the `claim`
- Note the specific fact or number needed
- Note the `source` and `confidence` from frontmatter
- Note the `updated` date (is this current?)
- Check for `status: outdated` or `status: deprecated` — do not use deprecated knowledge without noting it

### 4. Synthesize the answer

Compose the answer with full provenance:

**Format:**
```
<Answer statement> [source: [[Page Name]], confidence: high, updated: YYYY-MM-DD]

If inferred from multiple sources:
<Answer> (inferred from: [[Page A]], [[Page B]])

If uncertain:
<Best available answer> — however, this is marked `to verify` on [[Page Name]] and may not be current.

If not found:
This information is not in the vault. The closest related page is [[Page Name]] which covers <related topic>.
```

### 5. Apply the anti-hallucination rules

Before delivering the answer:

1. **Is every claim traced to a vault page?** If not, mark it `(inferred)` or `to verify`.
2. **Is every number attached to a source?** No number without `derived_from` or `evidence`.
3. **Is the source page current?** Check `status` and `updated`. Flag if outdated.
4. **Does the answer contradict any other vault page?** If yes, note the contradiction and do not resolve it yourself.
5. **Is any part of this answer a reasonable guess rather than a vault fact?** If yes, either remove it or clearly label it as `(not in vault, inferred from context)`.

**The rule:** "I don't know" or "not found in vault" is always a valid and correct answer. It is never acceptable to fill a gap with a plausible-sounding fabrication.

### 6. Confidence rating

Every answer should include an overall confidence:
- **high** — all claims confirmed by high-confidence vault pages with strong sources
- **medium** — one or more medium-confidence pages, or some inference involved
- **low** — mostly inferred, sources are old or weak
- **not found** — the vault does not contain the answer

### 7. Capture new knowledge if query reveals a gap

If the query reveals that:
- Important knowledge is missing from the vault → brain-capture or brain-ingest
- A synthesis page should exist but doesn't → flag for brain-synthesize
- An existing page needs updating → log as a review item

---

## Answer template

```
## Answer

**Question:** <restate the question>
**Confidence:** high / medium / low / not found

<Answer text with inline citations: [source: [[Page Name]]>

**Caveats:**
- <any outdated info, low-confidence pages, or inferences noted here>

**Not found:**
- <list of sub-questions for which no vault page exists>

**Suggested follow-up:**
- <brain-ingest if source is available>
- <brain-synthesize if enough related pages exist>
```

---

## What this skill does NOT do

- It does not answer from training data when vault knowledge is absent. It says "not found".
- It does not fill gaps with domain common knowledge. It says "to verify" or "not in vault".
- It does not resolve contradictions between vault pages. It surfaces them.
- It does not update vault pages. To update, hand off to brain-capture or brain-ingest.
