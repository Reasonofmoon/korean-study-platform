from __future__ import annotations

from hashlib import sha1
import json
from pathlib import Path
import re
import sys
import unicodedata

import networkx as nx

try:
    from graphify.exporters.html import to_html
except ImportError as exc:
    raise SystemExit("Graphify is required. Install graphifyy, then rerun this script.") from exc


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "source"
OUTPUT = SOURCE / "ontology" / "graphify"
GUIDES = [
    SOURCE / "high-2028" / "literature-2015" / "index.md",
    SOURCE / "high-2028" / "literature-reading-2" / "index.md",
    SOURCE / "high-2028" / "literature-reading-3" / "index.md",
    SOURCE / "high-2028" / "literature-reading-4" / "index.md",
    SOURCE / "high-2028" / "literature-exploration" / "index.md",
    SOURCE / "high-2028" / "descriptive-response" / "index.md",
]
HEADING = re.compile(r"^##\s+\d+\.\s+(.+?)\s+·\s+\d+(?:편|개)\s*$", re.MULTILINE)
ARTICLE = re.compile(
    r'<article class="literature-note"><h3>(?P<title>.*?)</h3>'
    r'<p><strong>표기:</strong> (?P<creator>.*?)</p>',
    re.DOTALL,
)
PRACTICE_ARTICLE = re.compile(
    r'<article class="answer-practice"><h3>(?P<title>.*?)</h3>',
    re.DOTALL,
)


def stable_id(prefix: str, label: str) -> str:
    return f"{prefix}:{sha1(label.strip().casefold().encode()).hexdigest()[:12]}"


def normalized_work_label(label: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFC", label))


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def creator_names(value: str) -> list[str]:
    names = []
    for item in value.split("·"):
        name = re.sub(r"\s+(원작|그림|바디|옮김|각색)$", "", item.strip())
        if name and name not in {"작자 미상", "전승"}:
            names.append(name)
    return names


def add_node(nodes: dict[str, dict], node_id: str, label: str, kind: str, source_file: str) -> None:
    nodes.setdefault(node_id, {
        "id": node_id,
        "label": label,
        "file_type": "concept",
        "kind": kind,
    })


def add_edge(edges: dict[tuple[str, str, str], dict], source: str, target: str, relation: str) -> None:
    edges[(source, target, relation)] = {
        "source": source,
        "target": target,
        "relation": relation,
        "confidence": "EXTRACTED",
    }


def main() -> None:
    nodes: dict[str, dict] = {}
    edges: dict[tuple[str, str, str], dict] = {}
    communities = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    labels = {0: "학습 경로", 1: "학습 지도", 2: "읽기 관점", 3: "작품", 4: "창작자·전승", 5: "서술형 역량"}

    high_id = "path:high-2028"
    add_node(nodes, high_id, "고등 2028 문학", "path", "source/high-2028/index.md")
    communities[0].append(high_id)

    for guide_path in GUIDES:
        text = guide_path.read_text(encoding="utf-8")
        source_file = guide_path.relative_to(ROOT).as_posix()
        map_label = frontmatter_value(text, "title")
        map_id = stable_id("map", map_label)
        add_node(nodes, map_id, map_label, "learning_map", source_file)
        communities[1].append(map_id)
        add_edge(edges, high_id, map_id, "has_map")

        sections = list(HEADING.finditer(text))
        practice_map = 'class="answer-practice"' in text
        for index, section in enumerate(sections):
            lens_label = section.group(1)
            lens_id = stable_id("lens", lens_label)
            add_node(nodes, lens_id, lens_label, "reading_lens", source_file)
            if lens_id not in communities[2]:
                communities[2].append(lens_id)
            add_edge(edges, map_id, lens_id, "uses_lens")
            end = sections[index + 1].start() if index + 1 < len(sections) else text.find("## 스스로 확인하기", section.end())
            chunk = text[section.end(): end if end != -1 else len(text)]
            if practice_map:
                for article in PRACTICE_ARTICLE.finditer(chunk):
                    skill_label = article.group("title").strip()
                    skill_id = stable_id("answer_skill", skill_label)
                    add_node(nodes, skill_id, skill_label, "answer_skill", source_file)
                    if skill_id not in communities[5]:
                        communities[5].append(skill_id)
                    add_edge(edges, lens_id, skill_id, "trains_skill")
            else:
                for article in ARTICLE.finditer(chunk):
                    work_label = article.group("title").strip()
                    work_id = stable_id("work", normalized_work_label(work_label))
                    add_node(nodes, work_id, work_label, "work", source_file)
                    if work_id not in communities[3]:
                        communities[3].append(work_id)
                    add_edge(edges, lens_id, work_id, "contains_work")
                    for name in creator_names(article.group("creator")):
                        creator_id = stable_id("creator", name)
                        add_node(nodes, creator_id, name, "creator", source_file)
                        if creator_id not in communities[4]:
                            communities[4].append(creator_id)
                        add_edge(edges, work_id, creator_id, "created_by")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    node_list = sorted(nodes.values(), key=lambda node: (node["kind"], node["label"]))
    edge_list = sorted(edges.values(), key=lambda edge: (edge["relation"], edge["source"], edge["target"]))
    graph_json = OUTPUT / "graph.json"
    graph_html = OUTPUT / "graph.html"
    temp_json = OUTPUT / "graph.json.tmp"
    temp_html = OUTPUT / "graph.html.tmp"
    temp_json.write_text(
        json.dumps({"nodes": node_list, "edges": edge_list}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    graph = nx.DiGraph()
    for node in node_list:
        graph.add_node(node["id"], **{key: value for key, value in node.items() if key != "id"})
    for edge in edge_list:
        graph.add_edge(edge["source"], edge["target"], **{key: value for key, value in edge.items() if key not in {"source", "target"}}, _src=edge["source"], _tgt=edge["target"])
    to_html(graph, communities, str(temp_html), community_labels=labels)
    mobile_css = (
        "\n@media (max-width: 760px) {\n"
        "  #sidebar { width: 150px; }\n"
        "  #search-wrap { padding: 8px; }\n"
        "  #info-panel { padding: 10px; }\n"
        "  #legend-wrap { padding: 8px; }\n"
        "  .legend-item { gap: 5px; font-size: 11px; }\n"
        "}\n"
    )
    theme_css = (
        "\n:root { --graph-bg: #0f0f1a; --graph-panel: #1a1a2e; --graph-border: #2a2a4e; --graph-control: #3a3a5e; --graph-text: #e0e0e0; --graph-muted: #aaa; --graph-faint: #aaa; --graph-node-text: #ffffff; --graph-hover: #2a2a4e; --graph-accent: #4E79A7; }\n"
        "body, #graph { background: var(--graph-bg); color: var(--graph-text); }\n"
        "#sidebar { background: var(--graph-panel); border-left-color: var(--graph-border); }\n"
        "#search-wrap, #info-panel, #search-results { border-color: var(--graph-border); }\n"
        "#search, .legend-cb, #select-all-cb { background: var(--graph-bg); border-color: var(--graph-control); color: var(--graph-text); }\n"
        "#search:focus { border-color: var(--graph-accent); }\n"
        ".search-item:hover, .neighbor-link:hover, .legend-item:hover { background: var(--graph-hover); }\n"
        "#info-panel h3, #legend-wrap h3, #legend-controls label { color: var(--graph-muted); }\n"
        "#info-content, #info-content .field b, #legend-controls label:hover { color: var(--graph-text); }\n"
        "#info-content .empty, .legend-count, #stats { color: var(--graph-faint); }\n"
        "#stats { border-top-color: var(--graph-border); }\n"
        "#theme-toggle { width: 100%; margin-top: 8px; padding: 7px 10px; border: 1px solid var(--graph-control); border-radius: 6px; background: transparent; color: var(--graph-text); cursor: pointer; font: inherit; font-size: 12px; }\n"
        "#theme-toggle:hover { background: var(--graph-hover); }\n"
        "#theme-toggle:focus-visible { outline: 2px solid var(--graph-accent); outline-offset: 2px; }\n"
        "body[data-theme=\"light\"] { --graph-bg: #faf8f3; --graph-panel: #fffdf8; --graph-border: #d8d2c5; --graph-control: #a9b9ae; --graph-text: #1a2b25; --graph-muted: #52685d; --graph-faint: #52685d; --graph-node-text: #1a2b25; --graph-hover: #f1ede3; --graph-accent: #1e5244; }\n"
    )
    theme_script = (
        "\n<script>\n"
        "const themeToggle = document.createElement('button');\n"
        "themeToggle.id = 'theme-toggle';\n"
        "themeToggle.type = 'button';\n"
        "document.getElementById('search-wrap').appendChild(themeToggle);\n"
        "function applyTheme(theme) {\n"
        "  const light = theme === 'light';\n"
        "  document.body.dataset.theme = light ? 'light' : 'dark';\n"
        "  themeToggle.textContent = light ? '다크 모드' : '라이트 모드';\n"
        "  themeToggle.setAttribute('aria-pressed', String(light));\n"
        "  const nodeText = getComputedStyle(document.body).getPropertyValue('--graph-node-text').trim();\n"
        "  nodesDS.update(RAW_NODES.map(node => ({ id: node.id, font: { ...node.font, color: nodeText } })));\n"
        "  network.redraw();\n"
        "}\n"
        "applyTheme(localStorage.getItem('ontology-theme') === 'light' ? 'light' : 'dark');\n"
        "themeToggle.addEventListener('click', () => {\n"
        "  const nextTheme = document.body.dataset.theme === 'light' ? 'dark' : 'light';\n"
        "  localStorage.setItem('ontology-theme', nextTheme);\n"
        "  applyTheme(nextTheme);\n"
        "});\n"
        "</script>\n"
    )
    rendered_html = temp_html.read_text(encoding="utf-8")
    rendered_html = re.sub(r"<title>graphify - .*?</title>", "<title>학습 온톨로지 그래프</title>", rendered_html, count=1)
    rendered_html = rendered_html.replace("</style>", mobile_css + theme_css + "</style>", 1)
    temp_html.write_text(rendered_html.replace("</body>", theme_script + "</body>", 1), encoding="utf-8")
    temp_json.replace(graph_json)
    temp_html.replace(graph_html)
    print(f"Graphify ontology: {len(node_list)} nodes, {len(edge_list)} edges")


if __name__ == "__main__":
    main()
