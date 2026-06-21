# brainmd — Living LLM Wiki Builder

A distributable kit for building and evolving a **living knowledge brain** — not a dump, but a navigable, self-growing graph where new knowledge compounds on what's already there.

Validated by 3× blind A/B experiments (24 → 72 → 120 → 135 solvers). Matches graphify and understand-anything on accuracy, beats them on speed, complements via claim/concept nodes.

---

## Philosophy: why "living brain", not a dump

A knowledge base dies when it becomes a flat pile of notes. It lives when:

- **Every fact links to its provenance.** Zero hallucinations follow from zero unsourced claims (our V3 scored 0.00 hallucination rate with strong provenance).
- **Links are typed, not flat.** `measures::`, `part_of::`, `causes::`, `evidence::` — eight edge types let agents navigate by relationship kind, not just adjacency.
- **Knowledge links are never cut.** Density equals value. Severing links degrades retrieval.
- **Ephemeral is separated.** One-off agent reports and raw inboxes stay outside the stable graph — they're buffers, not knowledge nodes.
- **The graph is read through lenses.** The same graph looks different filtered by domain, type, or recency. No single view shows everything; that's correct.

These principles are encoded as reproducible skills and CLI tools in this kit.

---

## Proven principles

| Principle | Evidence |
|---|---|
| Typed edges | 8 types (measures/part_of/causes/affects/depends_on/segments/evidence/derived_from); graphify/understand can't parse them — they're our exclusive precision layer |
| Dandelion rule | Ephemeral pages (inbox, agent reports) link into the stable graph but don't receive links back — keeps graph clean without losing signal |
| Provenance → 0 hallucinations | V3 scored 0.00; claim field + `derived_from`/`evidence` per number is mandatory |
| Claim nodes | One key assertion per page in frontmatter; agents read `claim` first, fetch full page only if needed — 1.5–2× faster retrieval |
| Concept/entity nodes | Named concepts without their own page (`entity::`) enrich retrieval granularity (graphify: 96 concept nodes; understand: 30 entity nodes) |
| Community naming | CNM communities in diagnostics get LLM-readable names ("OSAGO KV & Margin Economics") for navigation and onboarding |
| Semantic surprising | Periodic LLM pass finds cross-domain bridges missed by topology (e.g. Contradiction Register ↔ Metric without a link) |

---

## Status

**Validated on a real business vault (3-way blind A/B, 135 solvers).** Tested against graphify 0.8.44 and understand-anything 2.8.1. Results: 0.00 hallucination rate (V3 gate), 1.5–2× faster retrieval than untyped approaches, accuracy at parity.

---

## Install

```bash
# 1. Clone brainmd somewhere on your machine
git clone https://github.com/your-org/brainmd.git ~/brainmd

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
  → brain-ingest     (source → wiki pages + typed edges + claim + provenance)
  → brain-link       (grow connections to existing knowledge; attach derived_from/evidence per number)
  → brain-synthesize (when a topic matures → compile a synthesis page)
  → brain-surprising (periodic: find non-obvious cross-domain bridges)
  → brain-name-clusters (periodic: give CNM communities readable names)
  → brain-review     (periodic: orphans, drift, contradictions, what to synthesize next)
  → brain gate/lint  (mechanics: structure is healthy, ephemeral separated)
```

Each step **grows** the graph. Links are never cut. Provenance keeps hallucinations at zero.

---

## Package layout

```
brainmd/
├── README.md                  # this file
├── canon/                     # scaffold copied into each vault
│   ├── SCHEMA.md              # page types, edge vocabulary, dandelion rule, claim/concept
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

Validated on ~200 pages of a corporate knowledge vault against graphify 0.8.44 and understand-anything 2.8.1 (3× blind A/B, 135 solvers at peak):

- **Accuracy:** parity with graphify and understand
- **Hallucinations:** 0.00 (strong provenance + claim discipline; graphify/understand: higher)
- **Speed:** 1.5–2× faster (typed edges allow direct navigation vs. LLM traversal)
- **Completeness gap closed** by adding claim/concept nodes (was 0.92 vs. 0.95; now converging)
- graphify adds: Leiden communities with LLM names, semantic surprising connections, concept nodes — complement, not replacement
- understand adds: claim nodes, entity nodes — complement, not replacement
- All three are non-exclusive; the hybrid (our typed base + graphify layer + claim/concept nodes) is strictly better than any single approach

---

## License

MIT 2026 brainmd contributors
