---
name: brain-capture
description: Fixate an insight into the correct brain layer without losing it. Routes knowledge to inbox, wiki, decision, or source — whichever is appropriate — and writes it immediately.
---

# brain-capture

**Purpose:** Capture any valuable insight, fact, decision, risk, or open question that appears during any work. Nothing valuable should leave a session unrecorded.

---

## When to invoke

- A useful fact, metric, or conclusion surfaces mid-task
- A decision is made (even informally)
- A contradiction is noticed between two pieces of knowledge
- A risk or open question becomes clear
- Any domain knowledge that would be worth finding again in the future

---

## Steps

### 1. Identify what you have

Classify the knowledge:

| Type | Examples |
|---|---|
| **fact** | confirmed number, confirmed event, confirmed behavior |
| **insight** | derived conclusion from one or more facts |
| **hypothesis** | working assumption not yet confirmed |
| **decision** | a choice made or being made |
| **risk** | a threat or uncertainty with potential impact |
| **open question** | something that needs investigation |
| **source** | a new document, database, or data artifact |
| **contradiction** | conflict between this and existing knowledge |

### 2. Route to the correct layer

| Knowledge type | Destination |
|---|---|
| Quick insight, uncertain routing | **Insight Inbox** (ephemeral buffer) — add `to route` tag |
| New external source (doc, DB, file) | **Source Registry** — register it; create a source summary if substantial |
| Confirmed stable fact | **Wiki page** in the relevant domain folder |
| Metric or data model fact | **Metric page** |
| Management decision | **Decision Log** + decision page if significant |
| Contradiction with existing knowledge | **Contradiction Register** |
| Management signal worth watching regularly | **Dashboard** |

**Default when unsure:** write to the Insight Inbox. Never skip capture because routing is unclear.

### 3. Write it with provenance

Every captured item must include:
- **Source:** where this came from (document, database query, conversation, observation)
- **Confidence:** high / medium / low / unknown
- **Date**

For numbers specifically: attach `derived_from::` or `evidence::` to the source. No number without a source.

### 4. Mark uncertainty honestly

- Confirmed → state as fact with source
- Inferred → `(inferred from: <source>)`
- Unverified → `to verify`
- Unknown → `unknown`

Never promote a hypothesis to a fact without verification.

### 5. Log the capture

Add a brief entry to the vault's operation log: what was captured, where it went, why it matters.

---

## Anti-patterns to avoid

- Deferring capture because "I'll do it at the end" → end never comes
- Routing everything to the Inbox and never clearing it → Inbox becomes a dump
- Writing claims without sources → hallucination risk
- Overwriting old knowledge silently → use `outdated`/`deprecated` + Contradiction Register
