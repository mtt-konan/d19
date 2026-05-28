#!/usr/bin/env python3
"""partner BFS 连通分量可视化（matplotlib + networkx）。

用法（不需要项目添加 networkx/matplotlib 依赖，临时引入）:
  uv run --with networkx --with matplotlib python scripts/partner_bfs_plot.py \
    results/partner_bfs_root264_420_M100000.jsonl

输出: results/partner_bfs_root264_420_M100000.png
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    import matplotlib  # type: ignore[import-not-found]
    matplotlib.use("Agg")  # type: ignore[attr-defined]
    import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    import networkx as nx  # type: ignore[import-not-found]

    ap = argparse.ArgumentParser(description=__doc__)
    _ = ap.add_argument("nodes_file", type=Path)
    _ = ap.add_argument("--layout", default="kamada_kawai",
                        choices=["spring", "kamada_kawai", "circular", "spectral"])
    _ = ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    nodes_path: Path = args.nodes_file
    edges_path = nodes_path.with_name(nodes_path.stem + "_edges.jsonl")
    if not edges_path.exists():
        print(f"边文件不存在: {edges_path}", file=sys.stderr)
        return 1

    rows = [json.loads(line) for line in nodes_path.open()]
    edges = [json.loads(line) for line in edges_path.open()]

    G: "nx.Graph" = nx.Graph()  # type: ignore[name-defined]
    pair_keys: set[tuple[int, int]] = set()
    for r in rows:
        a, b = int(r["pair"][0]), int(r["pair"][1])
        pair_keys.add((a, b))
        G.add_node((a, b),
                   k=int(r.get("k", 0)),
                   depth=int(r["depth"]))
    for e in edges:
        u = (int(e["u"][0]), int(e["u"][1]))
        v = (int(e["v"][0]), int(e["v"][1]))
        if u in pair_keys and v in pair_keys:
            G.add_edge(u, v)

    print(f"图: {G.number_of_nodes()} 节点, {G.number_of_edges()} 边")

    layout_fn = {
        "spring": nx.spring_layout,
        "kamada_kawai": nx.kamada_kawai_layout,
        "circular": nx.circular_layout,
        "spectral": nx.spectral_layout,
    }[args.layout]
    pos = layout_fn(G, seed=42) if args.layout == "spring" else layout_fn(G)

    fig, ax = plt.subplots(figsize=(16, 12))

    # 节点颜色按 k
    color_map = {1: "#cccccc", 2: "#ffffff", 3: "#fff7b3",
                 4: "#ff9999", 5: "#ff5555", 6: "#cc0000", 7: "#990000", 8: "#660066"}
    node_colors = [color_map.get(int(G.nodes[n]["k"]), "#ffffff") for n in G.nodes]
    node_sizes = [400 + 200 * int(G.nodes[n]["k"]) for n in G.nodes]

    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4, edge_color="#666666")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,  # type: ignore[arg-type]
                           node_size=node_sizes, edgecolors="#222", linewidths=0.7)

    # 标签：高 k (k>=3) 节点显示完整 (a, b) k=…，k=2 节点只显示 (a, b)
    labels = {}
    for n in G.nodes:
        a, b = n
        k = int(G.nodes[n]["k"])
        if k >= 3:
            labels[n] = f"({a},{b})\nk={k}"
        else:
            labels[n] = f"({a},{b})"
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7)

    # 标题
    root_pair = next((n for n in G.nodes if int(G.nodes[n]["depth"]) == 0), None)
    title = f"Partner graph BFS from {root_pair}"
    title += f"  |  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
    title += f"  |  layout={args.layout}"
    ax.set_title(title, fontsize=12)
    ax.axis("off")

    out = args.out or nodes_path.with_suffix(".png")
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches="tight")
    print(f"输出: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
