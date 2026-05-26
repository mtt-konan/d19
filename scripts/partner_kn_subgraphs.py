#!/usr/bin/env python3
"""枚举 catalog 互素 multi-N 图中的 K_n 子图 (n >= 3)。

输入：results/multi_concordant_N_max100000_fast.jsonl

两条互补的路径：

A) 共享 partner —— 对每个 partner-only 顶点 P，把它的所有入边 source-pair
   并起来成节点集 S，验证 S 是否 K_|S|。覆盖 wl054 K_4 实例（共享 N 池）这类。

B) 一般 K_n —— 把 catalog 行视为 a-顶点图的一条边，跑 triangle 枚举，
   再扩展到 K_4、K_5。覆盖 "K_n 不必共享 N" 的一般情况。

两条路径都顺便记录每条边的 unreduced gcd 和 reduce 后的 k（multi-N 检验），
据此判断 "reduce 是否保 multi-N"。

输出:
  results/partner_kn_subgraphs.jsonl
  results/partner_kn_subgraphs_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from math import gcd
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def sorted_pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        default=Path("results/multi_concordant_N_max100000_fast.jsonl"),
    )
    _ = p.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner_kn_subgraphs.jsonl"),
    )
    _ = p.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner_kn_subgraphs_summary.json"),
    )
    _ = p.add_argument(
        "--min-n",
        type=int,
        default=3,
        help="只报告 |S| >= min-n 的子图（默认 3 = K_3 起）",
    )
    _ = p.add_argument(
        "--max-clique-size",
        type=int,
        default=6,
        help="K_n 枚举上限（默认 6）",
    )
    return p.parse_args()


def load_catalog(path: Path) -> dict[tuple[int, int], list[int]]:
    catalog: dict[tuple[int, int], list[int]] = {}
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            catalog[(int(r["A"]), int(r["B"]))] = [int(n) for n in r["concordant_N"]]
    return catalog


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()
    catalog = load_catalog(args.in_path)
    print(f"catalog 行数: {len(catalog)}")

    # === 建 a-顶点图（catalog 互素 multi-N 关系）===
    nodes: set[int] = set()
    edge_set: set[tuple[int, int]] = set()  # sorted (a, b)
    adj: dict[int, set[int]] = defaultdict(set)
    for (a, b), _ in catalog.items():
        e = sorted_pair(a, b)
        edge_set.add(e)
        adj[a].add(b)
        adj[b].add(a)
        nodes.add(a)
        nodes.add(b)

    print(f"a-顶点图: {len(nodes)} 个不同节点, {len(edge_set)} 条边")
    deg = {v: len(adj[v]) for v in nodes}
    deg_dist = Counter(deg.values())
    print("  度数分布 (前 20):")
    for d in sorted(deg_dist)[:20]:
        print(f"    degree={d:>3}  顶点数={deg_dist[d]}")
    print(f"  degree >= 2 节点数 = {sum(1 for v in nodes if deg[v] >= 2)}  (K_3 起步池)")
    print(f"  degree >= 3 节点数 = {sum(1 for v in nodes if deg[v] >= 3)}  (K_4)")
    print(f"  degree >= 4 节点数 = {sum(1 for v in nodes if deg[v] >= 4)}  (K_5)")

    # === 路径 B: 在 a-顶点图里枚举团 ===
    # 先列三角形：每个节点 v，其邻居中所有相邻对就是含 v 的三角形
    print()
    print("[路径 B] 枚举一般 K_n (catalog 互素 multi-N 图的团) ...")

    triangles: list[tuple[int, int, int]] = []
    # 为去重，仅枚举 v 是最小节点的三角形
    for v in sorted(nodes):
        nbrs = sorted(u for u in adj[v] if u > v)
        for i in range(len(nbrs)):
            for j in range(i + 1, len(nbrs)):
                u, w = nbrs[i], nbrs[j]
                if w in adj[u]:
                    triangles.append((v, u, w))

    print(f"  K_3 (triangle) = {len(triangles)} 个")

    # 由三角形扩展到 K_4：三个顶点的公共邻居
    k4s: list[tuple[int, int, int, int]] = []
    for t in triangles:
        v0, v1, v2 = t
        common = adj[v0] & adj[v1] & adj[v2]
        for x in common:
            if x > v2:  # 保证递增顺序去重
                k4s.append((v0, v1, v2, x))

    print(f"  K_4           = {len(k4s)} 个")

    # K_4 → K_5: 4 顶点公共邻居
    k5s: list[tuple[int, ...]] = []
    for q in k4s:
        common = adj[q[0]] & adj[q[1]] & adj[q[2]] & adj[q[3]]
        for x in common:
            if x > q[3]:
                k5s.append((*q, x))

    print(f"  K_5           = {len(k5s)} 个")

    # K_5 → K_6
    k6s: list[tuple[int, ...]] = []
    for q in k5s:
        common = adj[q[0]] & adj[q[1]] & adj[q[2]] & adj[q[3]] & adj[q[4]]
        for x in common:
            if x > q[4]:
                k6s.append((*q, x))

    print(f"  K_6           = {len(k6s)} 个")

    # === 路径 A: 共享 partner ===
    print()
    print("[路径 A] 共享 partner 的 K_n (来自 partner-only 顶点高入度) ...")

    # 对每个 partner 顶点收集它的入边 source-pair
    partner_sources: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for (A, B), Ns in catalog.items():
        for i in range(len(Ns)):
            for j in range(i + 1, len(Ns)):
                partner = sorted_pair(Ns[i], Ns[j])
                partner_sources[partner].append((A, B))

    shared_kn: list[dict[str, Any]] = []
    for partner, sources in partner_sources.items():
        if len(sources) < 3:
            continue  # K_3 至少需要 3 条 source 边围成
        # 节点集 = source-pair 涉及到的所有 a/b 值
        S: set[int] = set()
        for a, b in sources:
            S.add(a)
            S.add(b)
        if len(S) < args.min_n:
            continue
        # 验证 S 是否形成完全图
        S_sorted = sorted(S)
        all_pairs_multi_n = True
        edge_info: list[dict[str, Any]] = []
        for x, y in combinations(S_sorted, 2):
            # 检查 (x, y) 是否 multi-N
            xy = sorted_pair(x, y)
            if xy in catalog:
                k = len(catalog[xy])
                ns = catalog[xy]
                source = "catalog"
            else:
                # 跑权威验证（可能非互素）
                ns = find_concordant_by_factorization(x, y)
                k = len(ns)
                source = "factor_search"
            edge_info.append(
                {
                    "a": x,
                    "b": y,
                    "gcd": gcd(x, y),
                    "k": k,
                    "concordant_N": ns[:8],  # 截前 8 个
                    "source": source,
                }
            )
            if k < 2:
                all_pairs_multi_n = False
        if all_pairs_multi_n and len(S) >= args.min_n:
            shared_kn.append(
                {
                    "kind": "shared_partner",
                    "n": len(S),
                    "nodes": S_sorted,
                    "shared_partner": list(partner),
                    "source_pairs": [list(p) for p in sorted(sources)],
                    "edges": edge_info,
                }
            )

    shared_kn.sort(key=lambda r: (-r["n"], r["nodes"]))
    k4plus = sum(1 for r in shared_kn if r["n"] >= 4)
    print(f"  shared-partner K_3+ = {len(shared_kn)} 个 (其中 K_n n>=4 共 {k4plus} 个)")

    # === 输出 ===
    args.out.parent.mkdir(parents=True, exist_ok=True)

    # 一般 K_n 的边详细信息（标记是否互素 / k 值）
    def annotate_edges(node_tuple: tuple[int, ...]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for x, y in combinations(sorted(node_tuple), 2):
            xy = sorted_pair(x, y)
            ns = catalog.get(xy, [])
            out.append(
                {
                    "a": x,
                    "b": y,
                    "gcd": gcd(x, y),
                    "k": len(ns),
                    "concordant_N": ns[:8],
                }
            )
        return out

    rows_out: list[dict[str, Any]] = []
    for q in k6s:
        rows_out.append({"kind": "general", "n": 6, "nodes": list(q), "edges": annotate_edges(q)})
    for q in k5s:
        rows_out.append({"kind": "general", "n": 5, "nodes": list(q), "edges": annotate_edges(q)})
    for q in k4s:
        rows_out.append({"kind": "general", "n": 4, "nodes": list(q), "edges": annotate_edges(q)})
    # K_3 太多（每条 catalog 行附近都可能贡献）：只在 min-n <= 3 时输出
    if args.min_n <= 3:
        for q in triangles:
            rows_out.append({"kind": "general", "n": 3, "nodes": list(q), "edges": annotate_edges(q)})

    rows_out.extend(shared_kn)

    with args.out.open("w") as f:
        for r in rows_out:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary = {
        "catalog_rows": len(catalog),
        "graph_nodes": len(nodes),
        "graph_edges": len(edge_set),
        "general_K3": len(triangles),
        "general_K4": len(k4s),
        "general_K5": len(k5s),
        "general_K6": len(k6s),
        "shared_partner_K3plus": len(shared_kn),
        "shared_partner_K4plus": sum(1 for r in shared_kn if r["n"] >= 4),
        "shared_partner_K5plus": sum(1 for r in shared_kn if r["n"] >= 5),
        "top_general_K4": [
            {"nodes": list(q), "min_gcd": min(gcd(x, y) for x, y in combinations(q, 2))}
            for q in k4s[:20]
        ],
        "top_general_K5": [{"nodes": list(q)} for q in k5s[:20]],
        "top_shared_partner_kn": [
            {"n": r["n"], "nodes": r["nodes"], "shared_partner": r["shared_partner"]}
            for r in shared_kn[:20]
        ],
    }
    with args.summary_out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"  edges:   {args.out}")
    print(f"  summary: {args.summary_out}")

    # 高亮显示 K_5+
    if k5s:
        print()
        print(f"!!! 一般 K_5 命中 {len(k5s)} 个 !!!")
        for q in k5s[:5]:
            print(f"   nodes = {q}")
    if k6s:
        print()
        print(f"!!! 一般 K_6 命中 {len(k6s)} 个 !!!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
