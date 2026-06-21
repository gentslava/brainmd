"""Общий парсер графа Vault: сбор .md, разрешение [[wikilink]], типизированные
rel:: [[..]] рёбра, frontmatter/meta. Чистый stdlib, детерминированный."""
import os, re
from collections import defaultdict, namedtuple


def default_vault(calling_file):
    """Return the vault path for a script that lives inside <vault>/scripts/.

    Resolution order (first wins):
      1. BRAINMD_VAULT environment variable
      2. parent directory of the directory containing ``calling_file``
         (i.e. <calling_file>/../..)

    Pass ``__file__`` of the caller so each script can find its own default.
    """
    env = os.environ.get("BRAINMD_VAULT", "")
    if env:
        return os.path.abspath(env)
    return os.path.dirname(os.path.dirname(os.path.abspath(calling_file)))

SKIP_DIRS = {".obsidian", ".git", "scripts", "__pycache__", ".trash"}
# Каркас/мета (обходим для разрешения ссылок, но не узлы графа знаний):
# 08_Graph/07_Templates/09_Archive — мета; эфемерный слой (черновики процесса,
# одноразовые отчёты, буфер инсайтов, сырьё) — НЕ узлы графа знаний: их исходящие
# ссылки не должны раздувать граф. Ссылки НА них из знаниевых страниц остаются
# резолвимыми (не битыми), но сами они вне графа.
OUT_OF_SCOPE = ("09_Archive", "07_Templates", "08_Graph",
                "06_Agents/Agent Reports", "06_Agents/Agent Memory",
                "06_Agents/Agent Contexts", "06_Agents/Agent Prompts",
                "02_Sources/Extracted Facts", "01_Raw")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
TYPE_RE = re.compile(r"^type:\s*(.+)$", re.MULTILINE)
# Inline Dataview поле на своей строке: "relation:: [[Target]] (confidence)"
# NOTE: TYPED intentionally captures ALL rel:: types including out-of-vocabulary ones.
# The parser returns them as-is so that graph_diagnostics.py can report a "ВНЕ СЛОВАРЯ"
# block and wiki-lint.mjs can flag unknown_edge_type. Filtering here would blind those
# detectors. Vocabulary validation is the responsibility of diagnostics/lint, not the
# parser. Canonical vocabulary: part_of, measures, derived_from, causes, affects,
# depends_on, segments, evidence.
TYPED = re.compile(r"^\s*([a-z_]+)::\s*\[\[([^\]]+)\]\](?:\s*\((inferred|ambiguous)\))?",
                   re.MULTILINE)

Graph = namedtuple("Graph", "nodes undirected out_edges in_edges typed broken type_of meta_files")

def collect_md(vault):
    files = []
    for root, dirs, names in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".md"):
                files.append(os.path.join(root, n))
    return sorted(files)

def parse_typed_edges(text):
    return [(m.group(1), m.group(2).split("|")[0].split("#")[0].strip(), m.group(3) or "")
            for m in TYPED.finditer(text)]

def _read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def _note_type(text):
    m = TYPE_RE.search(text)
    return m.group(1).strip() if m else "?"

def _norm(raw):
    t = raw.split("|")[0].split("#")[0].strip()
    return t[:-3] if t.endswith(".md") else t

def _has_meta(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    return bool(re.search(r"(?m)^\s*-\s*meta\s*$", fm) or re.search(r"tags:\s*\[[^\]]*\bmeta\b", fm))

def build_graph(vault):
    files = collect_md(vault)
    all_rel = [os.path.relpath(p, vault)[:-3] for p in files]
    by_base = defaultdict(list); by_path = {}
    for r in all_rel:
        by_base[os.path.basename(r).lower()].append(r); by_path[r.lower()] = r
    text_of = {os.path.relpath(p, vault)[:-3]: _read(p) for p in files}
    type_of = {k: _note_type(v) for k, v in text_of.items()}
    meta_files = {r for r in all_rel if _has_meta(text_of.get(r, ""))}

    def in_scope(r):
        return not any(r == d or r.startswith(d + os.sep) for d in OUT_OF_SCOPE)
    def scoped(r):
        return in_scope(r) and r not in meta_files

    def resolve(link, src):
        t = _norm(link)
        if not t: return None
        low = t.lower()
        cand = os.path.normpath(os.path.join(os.path.dirname(src), t)).lstrip("./")
        if cand.lower() in by_path: return by_path[cand.lower()]
        if low in by_path: return by_path[low]
        base = os.path.basename(low)
        if base in by_base:
            ms = by_base[base]
            if len(ms) == 1: return ms[0]
            for mm in ms:
                if mm.lower().endswith(low): return mm
            return ms[0]
        return None

    nodes = [r for r in all_rel if scoped(r)]
    out_edges = defaultdict(set); in_edges = defaultdict(set); undirected = defaultdict(set)
    typed = defaultdict(set); broken = []
    for r in nodes:
        txt = text_of[r]
        for raw in WIKILINK.findall(txt):
            tgt = resolve(raw, r)
            if tgt is None: broken.append((r, raw.strip())); continue
            if tgt == r or not scoped(tgt): continue
            out_edges[r].add(tgt); in_edges[tgt].add(r)
            undirected[r].add(tgt); undirected[tgt].add(r)
        for etype, raw, _conf in parse_typed_edges(txt):
            tgt = resolve(raw, r)
            if tgt and tgt != r and scoped(tgt):
                typed[etype].add((r, tgt))
            elif tgt is None:
                entry = (r, raw.strip())
                if entry not in broken:
                    broken.append(entry)
    return Graph(nodes, dict(undirected), dict(out_edges), dict(in_edges),
                 dict(typed), broken, type_of, meta_files)
