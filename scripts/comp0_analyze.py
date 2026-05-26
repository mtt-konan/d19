#!/usr/bin/env python3
"""分析 wl061 找到的 comp 0 (309,689 节点超级 component)。

输出：
1. degree 分布 (histogram + power-law fit)
2. Top 30 高度数顶点（真 super-hub）
3. catalog vs partner-only 度数对比
4. comp 0 抽取 top-K 高度数顶点的诱导子图，渲染 PNG
5. 全 comp 0 force-directed 渲染（如果可能）

使用：
  uv run --extra viz python scripts/comp0_analyze.py --top 30 --plot
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner_full_bfs_components.jsonl"),
    )
    _ = p.add_argument(
        "--edges",
        type=Path,
        default=Path("results/partner_full_bfs_edges.jsonl"),
    )
    _ = p.add_argument(
        "--catalog",
        type=Path,
        default=Path("results/multi_concordant_N_max100000_fast.jsonl"),
    )
    _ = p.add_argument("--top", type=int, default=30, help="top-K hub")
    _ = p.add_argument("--plot", action="store_true", help="渲染 PNG 子图")
    _ = p.add_argument(
        "--out-dir", type=Path, default=Path("results"), help="output directory"
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    t0 = time.time()

    # 1. 读 comp 0 顶点集
    comp0_vertices: set[tuple[int, int]] = set()
    with cast(Path, args.components).open() as f:
        for line in f:
            c = json.loads(line)
            if c["component_id"] == 0:
                for v in c["vertices"]:
                    comp0_vertices.add((int(v[0]), int(v[1])))
                comp0_size = c["size"]
                comp0_edges = c["edges"]
                comp0_cycles = c["circuit_rank"]
                break
    print(f"[{time.time()-t0:.1f}s] comp 0: {len(comp0_vertices)} vertices, "
          f"{comp0_edges} edges, circuit_rank={comp0_cycles}")

    # 2. 读 catalog set（互素行）
    catalog_set: set[tuple[int, int]] = set()
    with cast(Path, args.catalog).open() as f:
        for line in f:
            row = json.loads(line)
            catalog_set.add((int(row["A"]), int(row["B"])))

    # 3. 读 edges, 只保留 comp 0 内部的边
    edges_inside: list[tuple[tuple[int, int], tuple[int, int]]] = []
    with cast(Path, args.edges).open() as f:
        for line in f:
            e = json.loads(line)
            u = (int(e["u"][0]), int(e["u"][1]))
            v = (int(e["v"][0]), int(e["v"][1]))
            if u in comp0_vertices and v in comp0_vertices:
                edges_inside.append((u, v))
    print(f"[{time.time()-t0:.1f}s] comp 0 内部 edges: {len(edges_inside)}")

    # 4. 算 degree
    degree: dict[tuple[int, int], int] = {v: 0 for v in comp0_vertices}
    for u, v in edges_inside:
        degree[u] += 1
        degree[v] += 1

    # 5. degree 分布
    deg_values = list(degree.values())
    deg_hist = Counter(deg_values)
    print()
    print("Degree 分布 (前 30 个 deg + 总占比):")
    print(f"  {'deg':<6}{'count':<10}{'占比':<10}{'cumulative':<10}")
    cum = 0
    total_deg = sum(deg_values)
    for d in sorted(deg_hist.keys()):
        cnt = deg_hist[d]
        cum += cnt
        pct = 100 * cnt / len(comp0_vertices)
        cum_pct = 100 * cum / len(comp0_vertices)
        if d <= 30 or cnt >= 100:
            print(f"  {d:<6}{cnt:<10}{pct:>5.2f}%   {cum_pct:>5.2f}%")
    print(f"\nmax degree = {max(deg_values)}, mean = {total_deg/len(comp0_vertices):.2f}")

    # 6. Top-K 高度数顶点
    top_k = cast(int, args.top)
    top_vertices = sorted(degree.items(), key=lambda kv: -kv[1])[:top_k]
    print()
    print(f"Top {top_k} 高度数顶点（comp 0 的 super-hub）:")
    print(f"  {'rank':<5}{'pair':<22}{'degree':<8}{'in_cat':<8}")
    print("  " + "-" * 50)
    for i, ((a, b), d) in enumerate(top_vertices):
        in_cat = "Y" if (a, b) in catalog_set else "N"
        print(f"  {i+1:<5}({a:>7}, {b:>7})  {d:<8}{in_cat:<8}")

    # 7. catalog vs partner-only 度数对比
    cat_degs = [degree[v] for v in comp0_vertices if v in catalog_set]
    part_degs = [degree[v] for v in comp0_vertices if v not in catalog_set]
    print()
    print("catalog vs partner-only 度数:")
    print(f"  catalog (in comp 0):     {len(cat_degs)} 顶点，"
          f"avg deg={sum(cat_degs)/len(cat_degs):.2f}, max={max(cat_degs)}")
    print(f"  partner-only (in comp 0): {len(part_degs)} 顶点，"
          f"avg deg={sum(part_degs)/len(part_degs):.2f}, max={max(part_degs)}")

    out_dir = cast(Path, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 8. 持久化分析摘要
    summary = {
        "component_id": 0,
        "size": len(comp0_vertices),
        "edges_inside": len(edges_inside),
        "circuit_rank": comp0_cycles,
        "degree_max": max(deg_values),
        "degree_mean": round(sum(deg_values) / len(comp0_vertices), 3),
        "degree_histogram": {str(d): deg_hist[d] for d in sorted(deg_hist.keys())},
        "top_hubs": [
            {"a": a, "b": b, "degree": d, "in_catalog": (a, b) in catalog_set}
            for (a, b), d in top_vertices
        ],
        "catalog_vertices_in_comp0": len(cat_degs),
        "partner_only_vertices_in_comp0": len(part_degs),
        "catalog_avg_degree": round(sum(cat_degs) / len(cat_degs), 3),
        "partner_only_avg_degree": round(sum(part_degs) / len(part_degs), 3),
    }
    summary_path = out_dir / "comp0_analyze_summary.json"
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n[{time.time()-t0:.1f}s] 摘要写入: {summary_path}")

    # 9. 可视化（可选）
    if cast(bool, args.plot):
        plot_subgraphs(comp0_vertices, edges_inside, degree, top_vertices,
                       catalog_set, out_dir, t0)

    return 0


def plot_subgraphs(
    comp0_vertices: set[tuple[int, int]],
    edges_inside: list[tuple[tuple[int, int], tuple[int, int]]],
    degree: dict[tuple[int, int], int],
    top_vertices: list[tuple[tuple[int, int], int]],
    catalog_set: set[tuple[int, int]],
    out_dir: Path,
    t0: float,
) -> None:
    """绘制 top-K hub 诱导子图 + degree 直方图。"""
    import matplotlib.pyplot as plt
    import networkx as nx

    # 9a. degree 直方图（log-log 看是否 power-law）
    fig, ax = plt.subplots(figsize=(8, 5))
    deg_values = list(degree.values())
    deg_hist = Counter(deg_values)
    xs = sorted(deg_hist.keys())
    ys = [deg_hist[x] for x in xs]
    ax.loglog(xs, ys, "o-", markersize=4, alpha=0.7)
    ax.set_xlabel("degree")
    ax.set_ylabel("count")
    ax.set_title(f"comp 0 degree distribution (V={len(comp0_vertices)})")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    deg_path = out_dir / "comp0_degree_distribution.png"
    fig.savefig(deg_path, dpi=120)
    plt.close(fig)
    print(f"[{time.time()-t0:.1f}s] degree 直方图: {deg_path}")

    # 9b. top-30 hub 诱导子图
    top30_vs = {v for v, _ in top_vertices[:30]}
    sub_edges = [(u, v) for u, v in edges_inside if u in top30_vs and v in top30_vs]

    G = nx.Graph()
    for v in top30_vs:
        G.add_node(v)
    G.add_edges_from(sub_edges)

    fig, ax = plt.subplots(figsize=(14, 14))
    pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)
    cat_nodes = [v for v in G.nodes() if v in catalog_set]
    part_nodes = [v for v in G.nodes() if v not in catalog_set]
    if cat_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=cat_nodes,
                               node_color="tab:orange", node_size=500,
                               ax=ax, label=f"catalog (n={len(cat_nodes)})")
    if part_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=part_nodes,
                               node_color="tab:blue", node_size=500,
                               ax=ax, label=f"partner-only (n={len(part_nodes)})")
    nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
    labels = {v: f"({v[0]},{v[1]})\\nd={degree[v]}" for v in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
    ax.set_title(f"comp 0 top-30 hub 诱导子图 ({G.number_of_edges()} edges)")
    ax.legend(loc="upper right")
    ax.axis("off")
    fig.tight_layout()
    sub_path = out_dir / "comp0_top30_subgraph.png"
    fig.savefig(sub_path, dpi=140)
    plt.close(fig)
    print(f"[{time.time()-t0:.1f}s] top-30 子图: {sub_path}")

    # 9c. top-K hubs + 1-hop neighbors (看 hub 怎么连接到中介)
    K9_hubs = [v for v, d in top_vertices if d == 36][:4]  # K_9 hubs (degree=36)
    print(f"[{time.time()-t0:.1f}s] K_9 hubs (degree=36): {K9_hubs}")

    neighbors: set[tuple[int, int]] = set(K9_hubs)
    for u, v in edges_inside:
        if u in K9_hubs:
            neighbors.add(v)
        if v in K9_hubs:
            neighbors.add(u)

    sub_edges = [(u, v) for u, v in edges_inside if u in neighbors and v in neighbors]
    Gn = nx.Graph()
    for v in neighbors:
        Gn.add_node(v)
    Gn.add_edges_from(sub_edges)

    fig, ax = plt.subplots(figsize=(18, 18))
    pos = nx.spring_layout(Gn, k=1.0, iterations=200, seed=42)
    is_hub = lambda v: v in K9_hubs
    sizes = [800 if is_hub(v) else max(60, degree[v] * 25) for v in Gn.nodes()]
    colors = ["red" if is_hub(v) else ("tab:orange" if v in catalog_set else "tab:blue")
              for v in Gn.nodes()]
    nx.draw_networkx_nodes(Gn, pos, node_color=colors, node_size=sizes, ax=ax, alpha=0.85)
    nx.draw_networkx_edges(Gn, pos, alpha=0.4, ax=ax, width=0.5)
    # 只标 hub
    hub_labels = {v: f"({v[0]},{v[1]})" for v in K9_hubs}
    nx.draw_networkx_labels(Gn, pos, labels=hub_labels, font_size=10, ax=ax,
                             font_weight="bold")
    ax.set_title(
        f"comp 0: 4 K_9 hubs (red) + 1-hop neighbors (blue=partner, orange=catalog)\n"
        f"V={Gn.number_of_nodes()}, E={Gn.number_of_edges()}"
    )
    ax.axis("off")
    fig.tight_layout()
    nbr_path = out_dir / "comp0_k9_neighborhood.png"
    fig.savefig(nbr_path, dpi=140)
    plt.close(fig)
    print(f"[{time.time()-t0:.1f}s] K_9 neighborhood: {nbr_path}")


if __name__ == "__main__":
    raise SystemExit(main())
