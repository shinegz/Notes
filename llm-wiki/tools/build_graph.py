#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Build knowledge graph from wiki wikilinks (EXTRACTED edges only).
Inspired by llm-wiki-agent build_graph.py; semantic inference omitted (no API key).

Usage:
  python3 build_graph.py --wiki-root /path/to/llm-wiki
  python3 build_graph.py --wiki-root ... --open
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import webbrowser
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    import networkx as nx
    from networkx.algorithms import community as nx_community

    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

SKIP_NAMES = {"log.md", "lint-report.md"}
TYPE_COLORS = {
    "source": "#4CAF50",
    "entity": "#2196F3",
    "concept": "#FF9800",
    "synthesis": "#9C27B0",
    "unknown": "#9E9E9E",
}
EDGE_COLOR = "#555555"
COMMUNITY_COLORS = [
    "#E91E63",
    "#00BCD4",
    "#8BC34A",
    "#FF5722",
    "#673AB7",
    "#FFC107",
    "#009688",
    "#F44336",
    "#3F51B5",
    "#CDDC39",
]


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def norm_target(raw: str) -> str:
    t = raw.strip()
    if "|" in t:
        t = t.split("|", 1)[0].strip()
    if "#" in t:
        t = t.split("#", 1)[0].strip()
    return t


def extract_wikilinks(content: str) -> list[str]:
    return [norm_target(m.group(1)) for m in re.finditer(r"\[\[([^\]]+)\]\]", content)]


def extract_frontmatter_type(content: str) -> str:
    m = re.search(r"^type:\s*(\S+)", content, re.MULTILINE)
    return m.group(1).strip("\"'") if m else "unknown"


def extract_title(content: str, stem: str) -> str:
    m = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
    return m.group(1).strip() if m else stem


def all_wiki_pages(wiki_dir: Path) -> list[Path]:
    return [
        p
        for p in wiki_dir.rglob("*.md")
        if p.is_file() and p.name not in SKIP_NAMES
    ]


def page_id(p: Path, wiki_dir: Path) -> str:
    return p.relative_to(wiki_dir).with_suffix("").as_posix()


def build_indexes(pages: list[Path], wiki_dir: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    id_lower: dict[str, str] = {}
    stem_to: dict[str, list[str]] = defaultdict(list)
    for p in pages:
        pid = page_id(p, wiki_dir)
        id_lower[pid.lower()] = pid
        stem_to[p.stem.lower()].append(pid)
    return id_lower, dict(stem_to)


def resolve_link(target: str, id_lower: dict[str, str], stem_to: dict[str, list[str]]) -> str | None:
    t = norm_target(target)
    if not t or t.startswith("http"):
        return None
    tl = t.lower()
    if tl in id_lower:
        return id_lower[tl]
    if "/" in t:
        suf = t.split("/")[-1].lower()
        if suf in stem_to and len(stem_to[suf]) == 1:
            return stem_to[suf][0]
    if tl in stem_to and len(stem_to[tl]) == 1:
        return stem_to[tl][0]
    return None


def build_nodes(pages: list[Path], wiki_dir: Path, repo_root: Path) -> list[dict]:
    nodes = []
    for p in pages:
        content = read_file(p)
        node_type = extract_frontmatter_type(content)
        label = extract_title(content, p.stem)
        pid = page_id(p, wiki_dir)
        nodes.append(
            {
                "id": pid,
                "label": label,
                "type": node_type,
                "color": TYPE_COLORS.get(node_type, TYPE_COLORS["unknown"]),
                "path": str(p.relative_to(repo_root)),
            }
        )
    return nodes


def build_edges(pages: list[Path], wiki_dir: Path, id_lower: dict[str, str], stem_to: dict[str, list[str]]) -> list[dict]:
    edges = []
    seen: set[tuple[str, str]] = set()
    for p in pages:
        content = read_file(p)
        src = page_id(p, wiki_dir)
        for link in extract_wikilinks(content):
            tgt = resolve_link(link, id_lower, stem_to)
            if not tgt or tgt == src:
                continue
            key = (src, tgt)
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                {
                    "from": src,
                    "to": tgt,
                    "type": "EXTRACTED",
                    "color": EDGE_COLOR,
                    "confidence": 1.0,
                }
            )
    return edges


def detect_communities(nodes: list[dict], edges: list[dict]) -> dict[str, int]:
    if not HAS_NETWORKX:
        return {}
    g = nx.Graph()
    for n in nodes:
        g.add_node(n["id"])
    for e in edges:
        g.add_edge(e["from"], e["to"])
    if g.number_of_edges() == 0:
        return {}
    try:
        communities = nx_community.louvain_communities(g, seed=42)
        out: dict[str, int] = {}
        for i, comm in enumerate(communities):
            for node in comm:
                out[node] = i
        return out
    except Exception:
        return {}


def render_html(nodes: list[dict], edges: list[dict]) -> str:
    nodes_json = json.dumps(nodes, indent=2)
    edges_json = json.dumps(edges, indent=2)
    legend = "".join(
        f'<span style="background:{c};padding:3px 8px;margin:2px;border-radius:3px;font-size:12px">{t}</span>'
        for t, c in TYPE_COLORS.items()
        if t != "unknown"
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>LLM Wiki — Graph</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  body {{ margin: 0; background: #1a1a2e; font-family: sans-serif; color: #eee; }}
  #graph {{ width: 100vw; height: 100vh; }}
  #controls {{
    position: fixed; top: 10px; left: 10px; background: rgba(0,0,0,0.7);
    padding: 12px; border-radius: 8px; z-index: 10; max-width: 280px;
  }}
  #controls h3 {{ margin: 0 0 8px; font-size: 14px; }}
  #search {{ width: 100%; padding: 4px; margin-bottom: 8px; background: #333; color: #eee; border: 1px solid #555; border-radius: 4px; }}
  #info {{
    position: fixed; bottom: 10px; left: 10px; background: rgba(0,0,0,0.8);
    padding: 12px; border-radius: 8px; z-index: 10; max-width: 360px; display: none;
  }}
  #stats {{ position: fixed; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 8px; font-size: 12px; }}
</style>
</head>
<body>
<div id="controls">
  <h3>LLM Wiki</h3>
  <input id="search" type="text" placeholder="筛选节点..." oninput="searchNodes(this.value)">
  <div>{legend}</div>
  <div style="margin-top:8px;font-size:11px;color:#aaa">边仅来自显式 [[wikilink]]</div>
</div>
<div id="graph"></div>
<div id="info">
  <b id="info-title"></b><br>
  <span id="info-type" style="font-size:12px;color:#aaa"></span><br>
  <span id="info-path" style="font-size:11px;color:#666"></span>
</div>
<div id="stats"></div>
<script>
const nodes = new vis.DataSet({nodes_json});
const edges = new vis.DataSet({edges_json});
const container = document.getElementById("graph");
const network = new vis.Network(container, {{ nodes, edges }}, {{
  nodes: {{ shape: "dot", size: 12, font: {{ color: "#eee", size: 13 }}, borderWidth: 2 }},
  edges: {{ width: 1.2, smooth: {{ type: "continuous" }}, arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }} }},
  physics: {{ stabilization: {{ iterations: 150 }}, barnesHut: {{ gravitationalConstant: -8000, springLength: 120 }} }},
  interaction: {{ hover: true, tooltipDelay: 200 }},
}});
network.on("click", params => {{
  if (params.nodes.length > 0) {{
    const node = nodes.get(params.nodes[0]);
    document.getElementById("info").style.display = "block";
    document.getElementById("info-title").textContent = node.label;
    document.getElementById("info-type").textContent = node.type;
    document.getElementById("info-path").textContent = node.path;
  }} else {{
    document.getElementById("info").style.display = "none";
  }}
}});
document.getElementById("stats").textContent = `${{nodes.length}} nodes · ${{edges.length}} edges`;
function searchNodes(q) {{
  const lower = q.toLowerCase();
  nodes.forEach(n => {{
    nodes.update({{ id: n.id, opacity: (!q || n.label.toLowerCase().includes(lower)) ? 1 : 0.15 }});
  }});
}}
</script>
</body>
</html>"""


def prepend_log(wiki_dir: Path, line: str) -> None:
    log_path = wiki_dir / "log.md"
    prev = read_file(log_path)
    log_path.write_text(line.rstrip() + "\n\n" + prev, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-root", required=True)
    ap.add_argument("--open", action="store_true")
    args = ap.parse_args()

    repo_root = Path(args.wiki_root).expanduser().resolve()
    wiki_dir = repo_root / "wiki"
    graph_dir = repo_root / "graph"
    if not wiki_dir.is_dir():
        print("wiki/ missing", file=sys.stderr)
        return 1

    pages = all_wiki_pages(wiki_dir)
    today = date.today().isoformat()
    if not pages:
        print("no wiki pages")
        return 0

    id_lower, stem_to = build_indexes(pages, wiki_dir)
    nodes = build_nodes(pages, wiki_dir, repo_root)
    edges = build_edges(pages, wiki_dir, id_lower, stem_to)

    communities = detect_communities(nodes, edges)
    for node in nodes:
        cid = communities.get(node["id"], -1)
        if cid >= 0:
            node["color"] = COMMUNITY_COLORS[cid % len(COMMUNITY_COLORS)]
        node["group"] = cid

    graph_dir.mkdir(parents=True, exist_ok=True)
    graph_json = graph_dir / "graph.json"
    graph_html = graph_dir / "graph.html"
    payload = {
        "nodes": nodes,
        "edges": edges,
        "built": today,
        "content_hash": sha256_text(json.dumps([n["id"] for n in nodes], sort_keys=True)),
    }
    graph_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    graph_html.write_text(render_html(nodes, edges), encoding="utf-8")
    print(f"wrote {graph_json} ({len(nodes)} nodes, {len(edges)} edges)")

    prepend_log(
        wiki_dir,
        f"## [{today}] graph | rebuilt (wikilink-only)\n\n{len(nodes)} nodes, {len(edges)} edges.",
    )

    if args.open:
        webbrowser.open(f"file://{graph_html.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
