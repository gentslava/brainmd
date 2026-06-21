import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import untangle

FIX = os.path.join(os.path.dirname(__file__), "fixtures", "mini")

def test_leaf_missing_up_link_flagged(tmp_path):
    # leaf.md имеет part_of -> ok; создадим нарушителя без part_of
    bad = tmp_path / "v"; bad.mkdir()
    (bad / "hub.md").write_text("---\ntype: product\n---\n# Hub\n", encoding="utf-8")
    (bad / "bad.md").write_text("---\ntype: metric\n---\n# Bad\n\n## Связи\nmeasures:: [[hub]]\n", encoding="utf-8")
    man = tmp_path / "m.txt"; man.write_text("bad\nhub\n", encoding="utf-8")
    viol = untangle.find_violations(str(bad), str(man))
    names = {v["node"]: v["reasons"] for v in viol}
    assert any(n.endswith("bad") for n in names)
    assert "no_up_link" in next(r for n, r in names.items() if n.endswith("bad"))
