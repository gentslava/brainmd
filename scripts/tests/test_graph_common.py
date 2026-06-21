import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import graph_common as gc

FIX = os.path.join(os.path.dirname(__file__), "fixtures", "mini")

def test_parse_typed_edges():
    text = open(os.path.join(FIX, "leaf.md"), encoding="utf-8").read()
    edges = gc.parse_typed_edges(text)
    assert ("part_of", "hub", "") in edges
    assert ("measures", "hub", "") in edges
    assert ("causes", "missing-target", "inferred") in edges

def test_build_graph_resolves_and_types():
    g = gc.build_graph(FIX)
    # leaf->hub присутствует как ненаправленное ребро
    leaf = next(n for n in g.nodes if n.endswith("leaf"))
    hub = next(n for n in g.nodes if n.endswith("hub"))
    assert hub in g.undirected[leaf]
    # типизированный слой содержит part_of leaf->hub
    assert any(s.endswith("leaf") and t.endswith("hub") for (s, t) in g.typed["part_of"])
    # битая ссылка на missing-target учтена
    assert any("missing-target" in raw for (_, raw) in g.broken)

def test_typed_edge_broken_link_recorded():
    """Fix I2: typed edge whose target appears only in a typed edge (no bare [[wikilink]]
    anywhere else) must be recorded in broken exactly once.

    We create a two-file vault: source.md has an 'affects::' typed edge pointing to
    'only-typed-missing', which does not exist as a file and is not referenced by any
    bare [[wikilink]]. We confirm the entry appears in broken and appears only once
    (dedup guard works)."""
    with tempfile.TemporaryDirectory() as vault:
        # source note: typed edge target is absent from the vault
        with open(os.path.join(vault, "source.md"), "w", encoding="utf-8") as f:
            f.write("---\ntype: concept\n---\n# Source\naffects:: [[only-typed-missing]]\n")
        g = gc.build_graph(vault)
        broken_raws = [raw for (_, raw) in g.broken]
        # must be recorded
        assert "only-typed-missing" in broken_raws, (
            f"Expected 'only-typed-missing' in broken, got: {g.broken}"
        )
        # must appear exactly once (dedup guard)
        assert broken_raws.count("only-typed-missing") == 1, (
            f"Expected exactly 1 entry, got {broken_raws.count('only-typed-missing')}: {g.broken}"
        )
