# brainmd — Living LLM Wiki Builder

> **A top implementation of a second brain / LLM Wiki — and it earns the claim with evidence, not adjectives.** Across multiple blind A/B retrieval experiments (up to 135 anonymized solver agents), brainmd's typed-edge markdown matches or beats GraphRAG tools (graphify, understand-anything) on accuracy with fewer hallucinations and faster retrieval — and, crucially, we *measured what does NOT work* and removed it. Three isolating A/B runs proved that sub-document "fact nodes" (claim/entity) do not help retrieval and can hurt it. What remains is a tested, minimal core: typed edges + separated ephemeral layer + provenance discipline.

A distributable kit for building and evolving a **living knowledge brain** — not a dump, but a navigable, self-growing graph where new knowledge compounds on what's already there.

---

## Philosophy: why "living brain", not a dump

A knowledge base dies when it becomes a flat pile of notes. It lives when:

- **Every fact links to its provenance.** Near-zero hallucinations follow from zero unsourced assertions — each number carries `derived_from`/`evidence` to its single source.
- **Links are typed, not flat.** `measures::`, `part_of::`, `causes::`, `affects::`, `depends_on::`, `segments::`, `evidence::`, `derived_from::` — eight edge types let agents navigate by relationship kind, not just adjacency.
- **Knowledge links are never cut.** Density equals value. Severing links degrades retrieval (proven by A/B — the "cut to ≤3 links" variant lost accuracy).
- **Ephemeral is separated.** One-off agent reports and raw inboxes stay outside the stable graph — they're buffers, not knowledge nodes.
- **One fact lives in one place.** No sub-document "fact node" that duplicates a number from its source page. Duplicated facts create competing authorities that pull retrieval to the wrong copy (see *What we tested and removed*).
- **The graph is read through lenses.** The same graph looks different filtered by domain, type, or recency. No single view shows everything; that's correct.

These principles are encoded as reproducible skills and CLI tools in this kit.

---

## Proven principles (the core)

| Principle | Evidence |
|---|---|
| **Typed edges** | 8 types; graphify/understand can't parse them — they're our exclusive precision layer for navigation by relationship kind |
| **Dandelion / ephemeral separation** | Ephemeral pages (inbox, agent reports) link into the stable graph but don't receive links back — keeps the graph clean without losing signal |
| **Provenance → near-zero hallucinations** | Mandatory `derived_from`/`evidence` per number; isolated runs scored 0.04–0.05 hallucination rate (0.00 under earlier calibration) — lower than GraphRAG tools |
| **Density is value** | Cutting knowledge links to make the graph visually sparse *lost* accuracy in A/B; keep all knowledge links, read via lenses instead |
| **Community naming** | CNM communities in diagnostics get LLM-readable names ("OSAGO KV & Margin Economics") for navigation and onboarding |
| **Semantic surprising** | Periodic LLM pass finds cross-domain bridges missed by topology (e.g. a Contradiction ↔ a Metric without a link) |

---

## What we tested and removed (honest negative result)

Two practices were tried as "improvements" and **removed after isolating A/B disproved them**:

- **claim nodes** (one key assertion per page in frontmatter) and **entity pages** (sub-document nodes for named concepts).
- **What is statistically solid (the reason for removal):** on a number-heavy question where an entity page fixed a *competing* value, accuracy collapsed **0.95 → 0.48** with the entity page and recovered to **0.97** once removed. Pooled across two independent runs (n=6/arm), the entity effect is **+0.48, 95% CI [+0.42, +0.54]** — large, tight, reproduced, and the mechanism was traced by hand (every solver took the entity's value over the canonical one). This is observed causation, not just a mean.
- **What is NOT claimed:** the *overall* mean accuracy differences between arms (≈ −0.04 with claim/entity; ≈ +0.01 after rollback) were **within noise** — their 95% CIs include 0 at n=3/question. So claim/entity are **neutral on average, catastrophic at the specific spot** where a sub-node fixes a competing number — not "uniformly worse".
- A separate **powered study** (300 solvers, n=10/question, bootstrap CI, placebo control) tested *adding* provenance (`derived_from` to canonical pages): **no effect** — every CI includes 0, the touched-pages segment is indistinguishable from the placebo segment. The core is on a plateau.

**Lesson encoded in the method:** don't introduce sub-document fact-nodes that duplicate a number from a source page — a number lives in exactly one place. And validate structural "improvements" with an *isolating, powered* A/B (placebo control + bootstrap CI), not a point estimate at small n — small mean deltas are usually noise; trust large reproduced effects with a traced mechanism.

---

## Status

**Validated on a real ~200-page business vault.** Tested against graphify 0.8.44 and understand-anything 2.8.1 (3-way blind A/B, up to 135 solvers), then three isolating A/B runs to pin down what actually drives retrieval quality. Result: typed-edge core at accuracy parity-or-better, near-zero hallucinations, 1.5–2× faster retrieval than untyped/GraphRAG approaches — with sub-document fact-nodes proven counterproductive and removed.

---

## Install

```bash
# 1. Clone brainmd somewhere on your machine
git clone https://github.com/gentslava/brainmd.git ~/brainmd

# 2. Copy the canon scaffold into your Obsidian vault
python3 ~/brainmd/scripts/brain init /path/to/your/vault

# 3. (Optional) add skills to your AI assistant
#    Copy skills/* into .claude/skills/ or set the skills path to brainmd/skills/

# No external dependencies — pure Python stdlib + Node.js for brain lint (wiki-lint.mjs)
```

---

## Quick start

```bash
# Run the CLI (vault via env var or --vault flag)
python3 scripts/brain diagnose --vault /path/to/your/vault
python3 scripts/brain lint     --vault /path/to/your/vault
python3 scripts/brain gate     manifest.txt

# Or set BRAINMD_VAULT to avoid repeating --vault
export BRAINMD_VAULT=/path/to/your/vault
python3 scripts/brain diagnose
python3 scripts/brain lint

# Use skills (via Claude Code or any Claude agent)
# brain-capture, brain-ingest, brain-link, brain-synthesize,
# brain-name-clusters, brain-surprising, brain-query, brain-review
```

---

## Lifecycle

```
New information
  → brain-capture    (route to the right layer: inbox / wiki / decision / source)
  → brain-ingest     (source → wiki pages + typed edges + provenance per number)
  → brain-link       (grow connections to existing knowledge; attach derived_from/evidence per number)
  → brain-synthesize (when a topic matures → compile a synthesis page)
  → brain-surprising (periodic: find non-obvious cross-domain bridges)
  → brain-name-clusters (periodic: give CNM communities readable names)
  → brain-review     (periodic: orphans, drift, contradictions, what to synthesize next)
  → brain gate/lint  (mechanics: structure is healthy, ephemeral separated)
```

Each step **grows** the graph. Links are never cut. Provenance keeps hallucinations near zero.

---

## Package layout

```
brainmd/
├── README.md                  # this file
├── canon/                     # scaffold copied into each vault
│   ├── SCHEMA.md              # page types, edge vocabulary, navigation/dandelion rule
│   ├── Graph Rules.md         # naming, link types, tiered navigation, graph view filters
│   ├── Knowledge Graph Queries.md  # query patterns for diagnostics
│   ├── AGENTS.md              # agent operating instructions (project-agnostic)
│   └── templates/             # synthesis, metric, decision, source
├── skills/                    # agent processes
│   ├── brain-capture/
│   ├── brain-ingest/
│   ├── brain-link/
│   ├── brain-synthesize/
│   ├── brain-name-clusters/
│   ├── brain-surprising/
│   ├── brain-query/
│   └── brain-review/
└── scripts/                   # deterministic mechanics (pure stdlib)
    ├── graph_common.py        # typed-edge parser, ephemeral filter
    ├── graph_diagnostics.py   # gate, CNM communities, surprising (topological), Gini
    ├── untangle.py            # dandelion-rule violation detector
    ├── wiki-lint.mjs          # lint (edge types, up-link, ephemeral)
    └── brain                  # CLI wrapper
```

---

## Benchmark evidence

Validated on ~200 pages of a corporate knowledge vault against graphify 0.8.44 and understand-anything 2.8.1 (3-way blind A/B, 135 solvers at peak), plus three isolating A/B runs (90 solvers each) to isolate cause:

- **Accuracy:** typed-edge core at parity with graphify and understand (no significant difference observed).
- **Hallucinations:** near-zero (0.00–0.05 depending on judge calibration) via provenance discipline; lower than GraphRAG tools.
- **Speed:** 1.5–2× faster (typed edges allow direct navigation vs. LLM traversal) — a large, stable difference (≈35s vs 55–75s), not a noise-level one.
- **Sub-document fact-nodes (claim/entity): tested and removed.** The *significant* finding is local, not global: where an entity node fixed a competing number, accuracy dropped 0.95 → 0.48 and recovered to 0.97 on removal — pooled effect **+0.48, 95% CI [+0.42, +0.54]** (n=6/arm, reproduced, mechanism traced). The *overall* mean deltas (≈ −0.04) were within noise (CI includes 0). So: neutral on average, catastrophic at the duplicated-number spot.
- **Adding provenance: no effect** (powered study, 300 solvers, bootstrap CI, placebo control — every CI includes 0). The core is on a plateau; further structural tweaks don't pay off.
- A caution on method: small mean deltas at n=3/question are not decisive — several early point estimates were noise. Decisions here rest on large reproduced effects with a traced mechanism, and on the powered study.
- graphify and understand remain useful for *different* things (Leiden/CNM community naming, semantic surprising connections) — those ideas are adopted as periodic skills, not as sub-document fact-nodes.

Experiment write-ups live in the source project under `docs/superpowers/plans/ab-*` (verdicts per run).

---

## License

MIT 2026 brainmd contributors
