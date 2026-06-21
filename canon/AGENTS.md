---
type: agent-instructions
status: active
updated: 2026-06-21
confidence: high
source:
  - brainmd canon
tags:
  - agents
  - wiki-rules
  - second-brain
---

# AGENTS.md

Operating instructions for any AI agent working inside a brainmd vault.

Read this file before any ingest, query, capture, or modification. It is the operational contract — not a suggestion.

---

## What this vault is

A **living knowledge brain**: a typed-markdown graph of accumulated knowledge on a domain. It is not a dump. New knowledge is added, linked, and eventually synthesized. Old knowledge is deprecated with attribution, never silently overwritten.

---

## Core rules (non-negotiable)

1. **Read SCHEMA.md first.** Before any significant operation, read the vault's SCHEMA.md. It defines page types, frontmatter requirements, edge vocabulary, routing, and lint criteria.
2. **Never claim without a source.** No number, assertion, or conclusion without provenance (`source` in frontmatter, or `derived_from`/`evidence` in text). If you don't have a source, write `to verify` or `unknown` — not a plausible-sounding guess.
3. **Never cut knowledge links.** Removing links between stable wiki pages degrades retrieval. If a link is wrong, replace it with the correct one. Never just delete.
4. **Never silently overwrite contradictions.** If new information contradicts existing knowledge: note both, mark the old as `outdated` or `deprecated`, log the contradiction. The Contradiction Register is the right destination.
5. **Separate ephemeral from stable.** Inbox, agent reports, and raw sources are ephemeral buffers — not knowledge nodes. They link into the stable graph via `evidence::` edges but do not receive peer links back from stable pages.
6. **One claim per page.** Every stable wiki page carries a `claim:` in frontmatter — the single key assertion of that page. Agents read `claim` first, fetch full content only if needed.
7. **Confidence must be honest.** `confidence: high` only when confirmed by a document, database, code, or two independent sources. `low` or `unknown` requires an explicit `to verify` note.

---

## Capture discipline

When any information relevant to the domain appears during any work:

1. **Don't lose it.** If routing is unclear, write to the Insight Inbox with `to route`. Better a rough note than a lost insight.
2. **Route by layer:**
   - Quick insight / uncertain routing → Insight Inbox
   - New external source → Source Registry + summary if substantial
   - Confirmed fact / stable knowledge → relevant wiki page (`03_Wiki/` or equivalent)
   - Decision → Decision Log + decision page if significant
   - Contradiction → Contradiction Register
   - Management signal worth watching → Dashboard
3. **Be proactive.** Valuable knowledge emerging mid-task must be captured before the task ends — not deferred.

---

## Anti-hallucination discipline

The five rules that keep hallucination rate at zero:

1. **No number without provenance.** Every key number has `source` in frontmatter or `derived_from`/`evidence` inline.
2. **Mark uncertain explicitly.** Inferred conclusion → `(inferred)`. Ambiguous interpretation → `(ambiguous)`. No source → `to verify`.
3. **Contradictions go to the register.** New info contradicts existing → Contradiction Register first, not silent overwrite.
4. **"Not found" beats fabrication.** If data is absent, write "not found" or `unknown`. Never substitute "probably", "typically", "usually" without a source.
5. **Confidence must be earned.** `high` requires corroboration. When in doubt, go lower.

---

## Dandelion linking rule

Ephemeral pages (Insight Inbox, agent reports, raw sources) may link into stable wiki pages — but stable wiki pages must not link back to individual ephemeral items. Cross-reference is via the registry/MOC level, not directly.

Why: N ephemeral items × K stable pages = N×K manual links to maintain. The dandelion rule prevents link sprawl while preserving graph integrity.

---

## Typed edges — use them

Every `## Links` / `## Связи` section uses typed edges, not flat wikilinks:

```
measures::       [[Metric Page]]
part_of::        [[Parent Concept]]
causes::         [[Effect Page]]
affects::        [[Influenced Page]]
depends_on::     [[Dependency Page]]
segments::       [[Segment Page]]
evidence::       [[Source or Report Page]]
derived_from::   [[Source Page]]
entity::         Named Concept Without Its Own Page
claim::          "Key assertion for this inline claim"
```

Flat wikilinks are acceptable in running prose for navigation; `## Links` / `## Связи` must use typed edges.

---

## Delegation

Before starting any significant task:

1. Check whether there is a specialized skill or agent role that covers this task type.
2. If yes, delegate the relevant part. Do not replicate the skill's work manually.
3. If no, perform the task directly if it is straightforward; propose a new skill if it is complex and recurring.
4. After a delegated task completes: verify the result, compile important findings into stable wiki pages, update relevant index/MOC, log the operation.

Available skills: brain-capture, brain-ingest, brain-link, brain-synthesize, brain-name-clusters, brain-surprising, brain-query, brain-review.

---

## Git policy

When the vault is git-tracked:

- Commit wiki changes after each significant operation.
- Commit message format: `docs(wiki): <summary of change>`
- Never commit: raw PII, credentials, secrets, database dumps, local output files.
- Never stage unrelated changes. Check `git diff --cached --name-status` before committing.
- `git add .` only when the working tree contains only wiki changes.

---

## What agents may do

- Read any wiki page
- Create source summaries
- Create or update wiki pages
- Update MOC / index
- Add to the operation log
- Propose structure improvements
- Capture any domain insight to the Inbox or relevant wiki page

## What agents must not do

- Delete raw sources without explicit permission
- Delete decisions without archiving them
- Overwrite a fact without marking the old version deprecated/outdated
- Invent data or fill gaps with plausible-sounding content
- Hide contradictions
- Ignore a relevant skill/role and perform the full task manually without reason
- Store PII, secrets, passwords, or access tokens in the vault
