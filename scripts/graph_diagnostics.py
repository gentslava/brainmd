#!/usr/bin/env python3
"""
Диагностика графа знаний Vault: степени, хабы, orphans, битые ссылки,
компоненты связности, community detection (greedy modularity) и метрики
"hairball от супер-хабов vs неоднородность степеней (scale-free)".

Чистый Python, без внешних зависимостей. Детерминированный.
Запуск: python3 scripts/graph_diagnostics.py
"""
import os
import sys
from collections import defaultdict

import graph_common as gc

VAULT = gc.default_vault(__file__)

def top_folder(relpath):
    parts = relpath.split(os.sep)
    return parts[0] if len(parts) > 1 else "(root)"

def main():
    G = gc.build_graph(VAULT)
    rel_files = G.nodes
    out_edges, in_edges, undirected = G.out_edges, G.in_edges, G.undirected
    broken, type_of = G.broken, G.type_of

    N = len(rel_files)
    uniq_und = set()
    for a, ns in undirected.items():
        for b in ns:
            uniq_und.add(tuple(sorted((a, b))))
    M = len(uniq_und)
    directed_E = sum(len(v) for v in out_edges.values())

    deg = {r: len(undirected.get(r, ())) for r in rel_files}
    indeg = {r: len(in_edges.get(r, ())) for r in rel_files}
    outdeg = {r: len(out_edges.get(r, ())) for r in rel_files}

    orphans = [r for r in rel_files if deg[r] == 0]

    # ---- метрики неоднородности ----
    degs = sorted(deg.values(), reverse=True)
    mean_deg = (2 * M / N) if N else 0
    median_deg = degs[len(degs) // 2] if degs else 0
    max_deg = degs[0] if degs else 0
    # Gini по степеням
    def gini(xs):
        xs = sorted(xs)
        n = len(xs)
        s = sum(xs)
        if s == 0:
            return 0.0
        cum = sum((i + 1) * x for i, x in enumerate(xs))
        return (2 * cum) / (n * s) - (n + 1) / n
    g = gini(list(deg.values()))
    # доля концов рёбер, инцидентных топ-K хабам
    def endpoint_share(k):
        topk = set(sorted(rel_files, key=lambda r: deg[r], reverse=True)[:k])
        inc = sum(1 for (a, b) in uniq_und if a in topk or b in topk)
        return inc / M if M else 0
    share5 = endpoint_share(5)
    share10 = endpoint_share(10)

    # ---- компоненты связности (undirected, без orphans) ----
    seen = set()
    comps = []
    for r in rel_files:
        if r in seen or deg[r] == 0:
            continue
        stack = [r]
        comp = []
        seen.add(r)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in undirected.get(x, ()):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    comps.sort(key=len, reverse=True)

    # ---- community detection: greedy modularity (CNM) ----
    nodes = [r for r in rel_files if deg[r] > 0]
    comm = {r: i for i, r in enumerate(nodes)}            # node -> comm id
    members = {i: {r} for i, r in enumerate(nodes)}
    ksum = {i: deg[nodes_i] for i, nodes_i in enumerate(nodes)}  # sum deg in comm
    # inter-community edge counts
    between = defaultdict(int)   # (min,max) -> edges
    for (a, b) in uniq_und:
        ca, cb = comm[a], comm[b]
        if ca != cb:
            between[(min(ca, cb), max(ca, cb))] += 1
    two_m = 2 * M if M else 1

    def best_merge():
        best, bg = None, 1e-12
        for (i, j), e in sorted(between.items()):   # sorted for deterministic tie-break
            dq = e / M - 2 * (ksum[i] / two_m) * (ksum[j] / two_m)
            if dq > bg:                              # strictly greater → keep lex-first on ties
                bg, best = dq, (i, j)
        return best, bg

    while True:
        pair, gain = best_merge()
        if pair is None:
            break
        i, j = pair                      # сливаем j в i
        members[i] |= members[j]
        for n in members[j]:
            comm[n] = i
        ksum[i] += ksum[j]
        del members[j]
        del ksum[j]
        # пересобрать between
        nb = defaultdict(int)
        for (x, y), e in between.items():
            x = i if x == j else x
            y = i if y == j else y
            if x == y:
                continue
            nb[(min(x, y), max(x, y))] += e
        between = nb

    communities = sorted(members.values(), key=len, reverse=True)

    # ---- surprising connections: cross-community edges ranked by unexpectedness ----
    def top_folder_of(r):
        parts = r.split(os.sep)
        return parts[0] if len(parts) > 1 else "(root)"

    surprising = []
    for (a, b) in uniq_und:
        if comm.get(a) != comm.get(b):
            rarity = 1.0 / (deg[a] + deg[b])
            cross_folder = 1.0 if top_folder_of(a) != top_folder_of(b) else 0.4
            surprising.append((rarity * cross_folder, a, b))
    # stable sort: descending score, then lexicographic on node names
    surprising.sort(key=lambda t: (-t[0], t[1], t[2]))

    def dom_folder(group):
        c = defaultdict(int)
        for r in group:
            c[top_folder(r)] += 1
        # stable tie-break: highest count, then lex-smallest folder name
        return max(sorted(c.items()), key=lambda kv: kv[1])

    def hub_of(group):
        # stable tie-break: highest degree, then lex-smallest node name
        return max(sorted(group), key=lambda r: deg[r])

    # ---- покрытие MOC (tiered-навигация index -> MOC -> лист) ----
    def is_moc(r):
        return (type_of.get(r) == "moc" or r.startswith("04_MOC" + os.sep)
                or os.path.basename(r).startswith("MOC -"))
    moc_nodes = [r for r in rel_files if is_moc(r)]
    moc_covered = set()
    for m in moc_nodes:
        moc_covered |= out_edges.get(m, set())
    # Source Registry — хаб слоя источников (его summaries покрыты им, а не MOC)
    for r in rel_files:
        if type_of.get(r) in ("source-registry",):
            moc_covered |= out_edges.get(r, set())
    def is_entry(r):  # точки входа верхнего уровня — не обязаны быть «под MOC»
        return (r == "index" or r.startswith("00_Home" + os.sep) or is_moc(r)
                or r in ("README", "AGENTS")
                or type_of.get(r) in ("source-registry", "insight-inbox", "capture-channels"))
    uncovered_by_moc = [r for r in rel_files if r not in moc_covered and not is_entry(r)]

    # ---------------- ВЫВОД ----------------
    P = print
    P("=" * 72)
    P("ДИАГНОСТИКА ГРАФА VAULT")
    P("=" * 72)
    P(f"Заметок (нод):                {N}")
    P(f"Связей wikilink (направл.):   {directed_E}")
    P(f"Уникальных рёбер (ненапр.):   {M}")
    P(f"Битых ссылок:                 {len(broken)}")
    P(f"Orphans (степень 0):          {len(orphans)}  ({100*len(orphans)/N:.0f}%)")
    if orphans:
        for r in sorted(orphans):
            P(f"      orphan: [{type_of[r]}] {r}")
    P("")
    P("--- РАСПРЕДЕЛЕНИЕ СТЕПЕНЕЙ (неоднородность) ---")
    P(f"средняя:{mean_deg:.1f}  медиана:{median_deg}  макс:{max_deg}  (макс/средн = {max_deg/mean_deg:.1f}x)")
    P(f"Gini степеней:                {g:.2f}   (0=равномерно, →1 = сильные хабы/scale-free)")
    P(f"Доля рёбер у топ-5 хабов:     {100*share5:.0f}%")
    P(f"Доля рёбер у топ-10 хабов:    {100*share10:.0f}%")
    P("гистограмма степеней (deg: кол-во нод):")
    hist = defaultdict(int)
    for d in deg.values():
        b = d if d <= 10 else (20 if d <= 20 else (40 if d <= 40 else 999))
        hist[b] += 1
    labels = {999: "40+", 40: "21-40", 20: "11-20"}
    for b in sorted(hist):
        lab = labels.get(b, str(b))
        P(f"   {lab:>6}: {'#'*min(hist[b],60)} {hist[b]}")
    P("")
    P("--- РЁБРА ПО ТИПАМ (типизированный слой) ---")
    VOCAB = ["part_of", "measures", "derived_from", "causes", "affects", "depends_on", "segments", "evidence"]
    total_typed = sum(len(G.typed.get(t, ())) for t in VOCAB)
    for t in VOCAB:
        P(f"   {t:>12}: {len(G.typed.get(t, ()))}")
    unknown = sorted(set(G.typed) - set(VOCAB))
    if unknown:
        P(f"   ВНЕ СЛОВАРЯ: {', '.join(unknown)}")
    P(f"   всего типизированных рёбер: {total_typed}")
    P("")
    P("--- ТОП-15 ХАБОВ по входящим ссылкам (на них ссылаются — настоящие центры) ---")
    for r in sorted(rel_files, key=lambda r: indeg[r], reverse=True)[:15]:
        P(f"   in={indeg[r]:>3} out={outdeg[r]:>3} [{type_of[r]:>14}] {r}")
    P("")
    P("--- ТОП-15 по исходящим ссылками (раздают связи — кандидаты на разгрузку) ---")
    for r in sorted(rel_files, key=lambda r: outdeg[r], reverse=True)[:15]:
        P(f"   out={outdeg[r]:>3} in={indeg[r]:>3} [{type_of[r]:>14}] {r}")
    P("")
    P("--- КОМПОНЕНТЫ СВЯЗНОСТИ ---")
    P(f"Компонент: {len(comps)}; крупнейшая: {len(comps[0]) if comps else 0} нод "
      f"({100*(len(comps[0]) if comps else 0)/max(N,1):.0f}% всех заметок)")
    for c in comps[1:6]:
        P(f"   побочная компонента: {len(c)} нод, напр.: {c[0]}")
    P("")
    P(f"--- ГРОЗДИ-КАНДИДАТЫ под MOC (community detection, modularity) — {len(communities)} сообществ ---")
    for idx, group in enumerate(communities, 1):
        if len(group) < 3:
            continue
        folder, fcount = dom_folder(group)
        P(f"  [{idx:>2}] {len(group):>3} нод | домин.папка: {folder} ({fcount}) | хаб: {hub_of(group)}")
    small = [gp for gp in communities if len(gp) < 3]
    if small:
        P(f"  (+ {len(small)} мелких сообществ <3 нод)")
    P("")
    P("--- SURPRISING CONNECTIONS (межсообщественные мосты, топ-10) ---")
    for score, a, b in surprising[:10]:
        P(f"   {score:.3f}  {a}  <->  {b}")
    P("")
    P(f"--- ПОКРЫТИЕ MOC: {len(uncovered_by_moc)} листьев НЕ в одном MOC (достижимы только папкой/поиском) ---")
    bf = defaultdict(list)
    for r in uncovered_by_moc:
        bf[top_folder(r)].append(r)
    for folder in sorted(bf):
        P(f"  {folder} ({len(bf[folder])}):")
        for r in sorted(bf[folder]):
            P(f"      [{type_of[r]:>16}] {r}")
    P("")
    if broken:
        P("--- ПРИМЕРЫ БИТЫХ ССЫЛОК (первые 15) ---")
        for s, raw in broken[:15]:
            P(f"   [{s}] -> [[{raw}]]")
    P("")
    P("ИНТЕРПРЕТАЦИЯ:")
    P(f"  • Если доля рёбер у топ-5 ≳40% и max/средн ≳10x → 'клубок' держат немного")
    P(f"    супер-хабов (index/dashboards/reports) → лечится их разгрузкой (P1-P2).")
    P(f"  • Gini ≳0.5 → степени уже неоднородны (есть хабы) → структура ближе к")
    P(f"    'грозди', чем кажется; проблема в отображении (линзы, P3), не в контенте.")
    P(f"  • Крупнейшая компонента ~100% → нет изолированных тем; community-грозди")
    P(f"    выше — естественные кандидаты на отдельные MOC.")

def health_gate(G, manifest_path, mode="dandelion"):
    """mode='dandelion' — пилот NEW: лимит ИСХОДЯЩЕЙ степени листа ≤3 (резка связей).
    mode='v3' — улучшенный: НЕ лимитирует знаниевые связи; вместо этого требует полноту
    типизации (нет нетипизированных вбок-ссылок). Общее для обоих: up-link, эфемерный слой
    отделён, нет битых. Медиана листьев печатается информационно в обоих режимах."""
    cluster = set(l.strip() for l in open(manifest_path, encoding="utf-8")
                  if l.strip() and not l.startswith("#"))
    outdeg = {r: len(G.out_edges.get(r, ())) for r in G.nodes}
    in_cluster = [r for r in G.nodes if r in cluster]
    indeg = {r: len(G.in_edges.get(r, ())) for r in in_cluster}
    ranked = sorted(in_cluster, key=lambda r: indeg[r], reverse=True)
    hubs = set(ranked[:max(1, len(ranked)//5)])
    leaves = [r for r in in_cluster if r not in hubs]
    leaf_degs = sorted(outdeg[r] for r in leaves)
    median_leaf = leaf_degs[len(leaf_degs)//2] if leaf_degs else 0
    report_links = sum(
        1 for r in in_cluster for t in G.out_edges.get(r, ())
        if "/Agent Reports/" in t and t.endswith(("report", "executive-summary", "data-map")))
    typed_pairs = {(s, t) for pairs in G.typed.values() for (s, t) in pairs}
    untyped_leaves = sum(1 for r in leaves
                         if any((r, t) not in typed_pairs for t in G.out_edges.get(r, ())))
    no_up = sum(1 for r in leaves if not any(s == r for (s, _t) in G.typed.get("part_of", ())))
    common = [
        ("битых ссылок == 0", len(G.broken) == 0, len(G.broken)),
        ("прямых ссылок в reports == 0", report_links == 0, report_links),
        ("каждый лист имеет part_of вверх", no_up == 0, no_up),
    ]
    if mode == "v3":
        checks = common + [("вбок-связи листьев типизированы (untyped==0)", untyped_leaves == 0, untyped_leaves)]
    else:
        checks = [("медиана исходящей степени листьев ≤3", median_leaf <= 3, median_leaf)] + common
    ok = all(c[1] for c in checks)
    print(f"\n--- HEALTH-GATE (кластер, режим {mode}) ---")
    for name, passed, val in checks:
        print(f"   [{'PASS' if passed else 'FAIL'}] {name} (={val})")
    print(f"   (инфо) медиана исходящей степени листьев = {median_leaf}; нетипизированных листьев = {untyped_leaves}")
    print(f"   ИТОГ: {'PASS' if ok else 'FAIL'}")
    return ok


def compare_vaults(vault_a, vault_b):
    import statistics

    def metrics(vault_path):
        G = gc.build_graph(vault_path)
        N = len(G.nodes)
        und = set()
        for a, ns in G.undirected.items():
            for b in ns:
                und.add(tuple(sorted((a, b))))
        M = len(und)
        degs = sorted(len(G.undirected.get(r, ())) for r in G.nodes)
        mean_deg = (2 * M / N) if N else 0
        median_deg = degs[len(degs) // 2] if degs else 0

        def gini(xs):
            xs = sorted(xs)
            n = len(xs)
            s = sum(xs)
            if s == 0:
                return 0.0
            cum = sum((i + 1) * x for i, x in enumerate(xs))
            return (2 * cum) / (n * s) - (n + 1) / n

        g = gini(degs)
        deg_map = {r: len(G.undirected.get(r, ())) for r in G.nodes}
        top5 = set(sorted(G.nodes, key=lambda r: deg_map[r], reverse=True)[:5])
        top5_edges = sum(1 for (a, b) in und if a in top5 or b in top5)
        share5 = top5_edges / M if M else 0
        return {
            "N": N, "M": M, "gini": g,
            "median_deg": median_deg, "share5": share5,
            "broken": len(G.broken),
        }

    ma = metrics(vault_a)
    mb = metrics(vault_b)

    label_a = os.path.basename(vault_a.rstrip("/"))
    label_b = os.path.basename(vault_b.rstrip("/"))
    col_w = max(len(label_a), len(label_b), 20)

    print("\n--- СРАВНЕНИЕ VAULT'ОВ ---")
    header = f"{'Метрика':<26}  {label_a:>{col_w}}  {label_b:>{col_w}}"
    print(header)
    print("-" * len(header))
    rows = [
        ("Заметок (N)", "N", lambda v: str(v)),
        ("Рёбер (undirected)", "M", lambda v: str(v)),
        ("Gini степеней", "gini", lambda v: f"{v:.3f}"),
        ("Медиана степени", "median_deg", lambda v: str(v)),
        ("Доля рёбер топ-5 хабов", "share5", lambda v: f"{100*v:.1f}%"),
        ("Битых ссылок", "broken", lambda v: str(v)),
    ]
    for label, key, fmt in rows:
        va, vb = fmt(ma[key]), fmt(mb[key])
        print(f"  {label:<24}  {va:>{col_w}}  {vb:>{col_w}}")


if __name__ == "__main__":
    if "--gate-v3" in sys.argv:
        mp = sys.argv[sys.argv.index("--gate-v3") + 1]
        G = gc.build_graph(VAULT)
        sys.exit(0 if health_gate(G, mp, mode="v3") else 1)
    if "--gate" in sys.argv:
        mp = sys.argv[sys.argv.index("--gate") + 1]
        G = gc.build_graph(VAULT)
        sys.exit(0 if health_gate(G, mp) else 1)
    if "--compare" in sys.argv:
        other_dir = sys.argv[sys.argv.index("--compare") + 1]
        compare_vaults(VAULT, other_dir)
        sys.exit(0)
    main()
