"""Распутыватель: находит листья кластера, нарушающие правило одуванчика.
Помощник миграции и continuous maintenance. Чистый stdlib."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph_common as gc

def _load_manifest(p):
    return set(l.strip() for l in open(p, encoding="utf-8")
               if l.strip() and not l.startswith("#"))

def find_violations(vault, manifest, max_side=3):
    G = gc.build_graph(vault)
    cluster = _load_manifest(manifest)
    outdeg = {r: len(G.out_edges.get(r, ())) for r in G.nodes}
    indeg = {r: len(G.in_edges.get(r, ())) for r in G.nodes if r in cluster}
    ranked = sorted(indeg, key=lambda r: indeg[r], reverse=True)
    hubs = set(ranked[:max(1, len(ranked)//5)])
    up = {s for (s, _t) in G.typed.get("part_of", ())}
    typed_pairs = {(s, t) for et, pairs in G.typed.items() for (s, t) in pairs}
    out = []
    for r in sorted(n for n in G.nodes if n in cluster and n not in hubs):
        reasons = []
        if r not in up:
            reasons.append("no_up_link")
        if outdeg[r] > max_side + 1:  # исходящие листа: 1 part_of вверх + ≤max_side вбок
            reasons.append("degree_over")
        for t in G.out_edges.get(r, ()):
            if "/Agent Reports/" in t:
                reasons.append("report_link"); break
        for t in G.out_edges.get(r, ()):
            if (r, t) not in typed_pairs:
                reasons.append("untyped_peer"); break
        if reasons:
            out.append({"node": r, "reasons": sorted(set(reasons))})
    return out

if __name__ == "__main__":
    vault = gc.default_vault(__file__)
    man = sys.argv[1] if len(sys.argv) > 1 else "scripts/cluster-osago.txt"
    viol = find_violations(vault, man)
    for v in sorted(viol, key=lambda x: x["node"]):
        print(f"   {v['node']}  ->  {', '.join(v['reasons'])}")
    print(f"ИТОГО нарушителей: {len(viol)}")
    sys.exit(0 if not viol else 1)
