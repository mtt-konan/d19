#!/usr/bin/env python3
"""分析 partner_bfs.py 输出的连通分量。

功能：
  1. 加载多个 BFS 节点文件，对比各分量节点集合（是否相交）。
  2. 在每个分量内对所有 multi-N pair 检查 Harborth closure 条件
     N_i + N_j == A + B（即可能的反例）。
  3. 输出 graphviz .dot 文件用于可视化（.dot -> SVG/PNG via dot 命令）。

用法:
  uv run python scripts/partner_bfs_analyze.py \
    results/partner_bfs_root264_420_M100000.jsonl \
    results/partner_bfs_root153_560_M100000.jsonl
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


def load(p: Path) -> tuple[list[dict[str, Any]], dict[tuple[int, int], dict[str, Any]]]:
    rows = [json.loads(line) for line in p.open()]
    table: dict[tuple[int, int], dict[str, Any]] = {}
    for r in rows:
        a, b = int(r["pair"][0]), int(r["pair"][1])
        table[(a, b)] = r
    return rows, table


def closure_check(table: dict[tuple[int, int], dict[str, Any]]) -> list[tuple[tuple[int, int], int, int]]:
    """对每个 multi-N pair (A, B) 检查 N_i + N_j == A + B 的对子。"""
    hits: list[tuple[tuple[int, int], int, int]] = []
    for (a, b), r in table.items():
        ns = [int(x) for x in r.get("concordant_N", [])]
        if len(ns) < 2:
            continue
        target = a + b
        for ni, nj in combinations(ns, 2):
            if ni + nj == target:
                hits.append(((a, b), ni, nj))
    return hits


def write_dot(rows: list[dict[str, Any]], edges_path: Path, out_dot: Path) -> None:
    edges = [json.loads(line) for line in edges_path.open()]
    seen_edge: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    pair_keys = {(int(r["pair"][0]), int(r["pair"][1])) for r in rows}

    with out_dot.open("w") as f:
        _ = f.write("graph partner_bfs {\n")
        _ = f.write("  graph [layout=neato, overlap=false, splines=true];\n")
        _ = f.write("  node [shape=ellipse, fontsize=10];\n")
        for r in rows:
            a, b = int(r["pair"][0]), int(r["pair"][1])
            k = int(r.get("k", 0))
            depth = int(r["depth"])
            color = {0: "lightgray", 2: "white", 3: "lightyellow",
                     4: "lightcoral", 5: "tomato", 6: "red", 7: "darkred", 8: "purple"}.get(k, "white")
            label = f"({a},{b})\\nk={k} d={depth}"
            penwidth = 2.5 if k >= 4 else 1.0
            _ = f.write(f'  "{a},{b}" [label="{label}", style=filled, '
                        f'fillcolor={color}, penwidth={penwidth}];\n')
        for e in edges:
            u = (int(e["u"][0]), int(e["u"][1]))
            v = (int(e["v"][0]), int(e["v"][1]))
            if u not in pair_keys or v not in pair_keys:
                continue
            key = (u, v) if u < v else (v, u)
            if key in seen_edge:
                continue
            seen_edge.add(key)
            _ = f.write(f'  "{u[0]},{u[1]}" -- "{v[0]},{v[1]}";\n')
        _ = f.write("}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    _ = ap.add_argument("nodes_files", type=Path, nargs="+",
                        help="一个或多个 partner_bfs_*.jsonl 节点文件")
    _ = ap.add_argument("--out-dir", type=Path, default=Path("results"))
    args = ap.parse_args()

    components: list[tuple[Path, list[dict[str, Any]], dict[tuple[int, int], dict[str, Any]]]] = []
    for p in args.nodes_files:
        rows, table = load(p)
        components.append((p, rows, table))

    print("=== 各分量信息 ===")
    for p, rows, table in components:
        print(f"  {p.name}: {len(rows)} 节点")

    # 两两交集
    print()
    print("=== 分量节点集合两两交集 ===")
    for (p1, _r1, t1), (p2, _r2, t2) in combinations(components, 2):
        common = set(t1.keys()) & set(t2.keys())
        print(f"  {p1.stem} ∩ {p2.stem}: {len(common)} 个共同节点")
        if common and len(common) <= 20:
            print(f"    {sorted(common)}")

    # closure 检查
    print()
    print("=== closure 检查 (N_i + N_j == A + B) ===")
    for p, _rows, table in components:
        hits = closure_check(table)
        print(f"  {p.stem}: {len(hits)} 个 closure pair")
        for (a, b), ni, nj in hits[:10]:
            print(f"    (A, B) = ({a}, {b})  A+B = {a+b}  closure = ({ni}, {nj})  N_i+N_j = {ni+nj}")

    # 写 dot 文件
    print()
    print("=== 生成 graphviz dot 文件 ===")
    for p, rows, _table in components:
        edges_path = p.parent / (p.stem.replace(".jsonl", "") + "_edges.jsonl")
        if not edges_path.exists():
            edges_path = p.with_name(p.stem + "_edges.jsonl")
        out_dot = args.out_dir / (p.stem + ".dot")
        write_dot(rows, edges_path, out_dot)
        print(f"  {out_dot}")
        print(f"  → 渲染:  dot -Tsvg {out_dot} -o {out_dot.with_suffix('.svg')}")
        print(f"  → 或:    neato -Tpng {out_dot} -o {out_dot.with_suffix('.png')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
