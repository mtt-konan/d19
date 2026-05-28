#!/usr/bin/env python3
"""完整的 partner graph G_M：对所有已知顶点都算 N 列表。

修复 partner_pair_graph.py 的"只走 1 跳"问题。该脚本：

1. 加载 catalog 互素 multi-N pair (10333)
2. 对每个 pair 用 partner identity 推出 C(k, 2) 个 partner pair
3. 对所有 partner-only pair **也调用 find_concordant_by_factorization** 算 N
4. 加 edge (A, B) ↔ (N_i, N_j) for 全部 multi-N pair（互素+非互素）
5. Union-find 输出 connected component 分布
6. 报告每个大 component 的 size + circuit rank

跟 partner_pair_graph.py 区别：
  partner_pair_graph.py:  partner-only 顶点 N=[]，没继续展开 → 10104 components
  partner_full_graph.py:  partner-only 顶点也算 N，完整 closure → 真实 components

工期估算：
  ≈ 10533 partner-only × ~50ms/find_concordant ≈ 9 分钟（首次跑）
  之后可以缓存
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent
import sys
sys.path.insert(0, str(ROOT / "src"))


def sorted_pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--catalog",
        type=Path,
        default=Path("results/multi_concordant_N_max100000_fast.jsonl"),
        help="catalog of coprime multi-N pairs (jsonl with A, B, concordant_N)",
    )
    _ = p.add_argument(
        "--max-value",
        type=int,
        default=1_000_000,
        help="跳过 N > max_value 的 partner pair（避免 BFS 爆炸）",
    )
    _ = p.add_argument(
        "--progress-every",
        type=int,
        default=200,
        help="每 N 个 partner-only 输出一次进度",
    )
    _ = p.add_argument(
        "--out-edges",
        type=Path,
        default=Path("results/partner_full_graph_edges.jsonl"),
    )
    _ = p.add_argument(
        "--out-summary",
        type=Path,
        default=Path("results/partner_full_graph_summary.json"),
    )
    _ = p.add_argument(
        "--out-components",
        type=Path,
        default=Path("results/partner_full_graph_components.jsonl"),
        help="每个 component 的顶点列表 + circuit rank",
    )
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()

    # 1. 加载 catalog 互素 multi-N pair
    t0 = time.time()
    catalog: dict[tuple[int, int], list[int]] = {}
    with cast(Path, args.catalog).open() as f:
        for line in f:
            row = json.loads(line)
            catalog[(int(row["A"]), int(row["B"]))] = [int(n) for n in row["concordant_N"]]
    print(f"[{time.time()-t0:.1f}s] Catalog: {len(catalog)} coprime multi-N pairs", flush=True)

    # 2. 把 catalog 的 partner-only 收集
    max_value = cast(int, args.max_value)
    vertices_with_N: dict[tuple[int, int], list[int]] = dict(catalog)
    partner_only: set[tuple[int, int]] = set()
    for (a, b), ns in catalog.items():
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                p = sorted_pair(ns[i], ns[j])
                if p not in catalog and max(p) <= max_value:
                    partner_only.add(p)
    print(f"[{time.time()-t0:.1f}s] Partner-only (1-hop): {len(partner_only)}", flush=True)

    # 3. 对每个 partner-only pair 算 N 列表（如果 max(p) <= max_value）
    progress_every = cast(int, args.progress_every)
    print(f"[{time.time()-t0:.1f}s] 计算 partner-only N 列表（{len(partner_only)} pair）...", flush=True)
    computed = 0
    for p in sorted(partner_only):
        if computed % progress_every == 0 and computed > 0:
            rate = computed / (time.time() - t0)
            eta = (len(partner_only) - computed) / rate if rate > 0 else 0
            print(f"  [{time.time()-t0:.1f}s]   {computed}/{len(partner_only)}  ({rate:.0f}/s, ETA {eta:.0f}s)", flush=True)
        ns = find_concordant_by_factorization(p[0], p[1])
        vertices_with_N[p] = ns
        computed += 1
    print(f"[{time.time()-t0:.1f}s] 完成 partner-only N 列表计算", flush=True)

    # 4. 对每个顶点（含 partner-only）展开 partner identity，加 edge
    #    某些 partner-only 的 N 列表会引入"新的"partner pair (level-2)，也加入顶点集
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    new_partners: set[tuple[int, int]] = set()
    for v, ns in list(vertices_with_N.items()):
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                u = sorted_pair(ns[i], ns[j])
                if u == v:
                    continue
                if max(u) > max_value:
                    continue
                e = (v, u) if v < u else (u, v)
                edges.add(e)
                if u not in vertices_with_N:
                    new_partners.add(u)
    print(f"[{time.time()-t0:.1f}s] Level-1 edges: {len(edges)}, level-2 new partners: {len(new_partners)}", flush=True)

    # 5. 对 level-2 new partners 也算 N 列表 + 加 edges
    if new_partners:
        print(f"[{time.time()-t0:.1f}s] 计算 level-2 N 列表...", flush=True)
        for p in sorted(new_partners):
            ns = find_concordant_by_factorization(p[0], p[1])
            vertices_with_N[p] = ns
            for i in range(len(ns)):
                for j in range(i + 1, len(ns)):
                    u = sorted_pair(ns[i], ns[j])
                    if u == p:
                        continue
                    if max(u) > max_value:
                        continue
                    e = (p, u) if p < u else (u, p)
                    edges.add(e)
        print(f"[{time.time()-t0:.1f}s] Level-2 完成，edges = {len(edges)}, vertices = {len(vertices_with_N)}", flush=True)

    # 6. union-find on edges
    vertices = set(vertices_with_N.keys())
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)
    parent: dict[tuple[int, int], tuple[int, int]] = {v: v for v in vertices}

    def find(x: tuple[int, int]) -> tuple[int, int]:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: tuple[int, int], y: tuple[int, int]) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for u, v in edges:
        union(u, v)

    components: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for v in vertices:
        components.setdefault(find(v), []).append(v)

    print(f"[{time.time()-t0:.1f}s] union-find 完成: {len(components)} components", flush=True)

    # 7. 输出
    comp_list = sorted(components.values(), key=lambda c: -len(c))
    comp_edges_count: dict[tuple[int, int], int] = {}
    for u, v in edges:
        root = find(u)
        comp_edges_count[root] = comp_edges_count.get(root, 0) + 1

    # circuit rank per component = E - V + 1
    print("\n顶部 component 分布（按 size 降序）:")
    print(f"{'rank':<5}{'size':<6}{'edges':<7}{'circuit_rank':<13}{'例子':<30}")
    print("-" * 70)
    for i, c in enumerate(comp_list[:20]):
        size = len(c)
        eroot = find(c[0])
        e_count = comp_edges_count.get(eroot, 0)
        circuit = e_count - size + 1
        example = c[0]
        print(f"{i+1:<5}{size:<6}{e_count:<7}{circuit:<13}({example[0]}, {example[1]})")

    # size 分布
    sizes = [len(c) for c in comp_list]
    from collections import Counter
    size_hist = Counter(sizes)
    print("\nSize 分布 (前 10):")
    for s, cnt in sorted(size_hist.items()):
        if s <= 5 or cnt >= 5:
            print(f"  size = {s:<5}  count = {cnt}")

    # 8. 持久化
    cast(Path, args.out_edges).parent.mkdir(parents=True, exist_ok=True)
    with cast(Path, args.out_edges).open("w") as f:
        for u, v in sorted(edges):
            _ = f.write(json.dumps({"u": list(u), "v": list(v)}, ensure_ascii=False) + "\n")

    with cast(Path, args.out_components).open("w") as f:
        for i, c in enumerate(comp_list):
            eroot = find(c[0])
            e_count = comp_edges_count.get(eroot, 0)
            _ = f.write(json.dumps({
                "component_id": i,
                "size": len(c),
                "edges": e_count,
                "circuit_rank": e_count - len(c) + 1,
                "vertices": [list(v) for v in sorted(c)],
            }, ensure_ascii=False) + "\n")

    summary = {
        "catalog_size": len(catalog),
        "vertices": len(vertices),
        "edges": len(edges),
        "components": len(components),
        "max_value": max_value,
        "largest_component_size": sizes[0] if sizes else 0,
        "elapsed_s": round(time.time() - t0, 1),
        "size_histogram_truncated": {str(s): c for s, c in sorted(size_hist.items())[:30]},
    }
    with cast(Path, args.out_summary).open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n[{time.time()-t0:.1f}s] 总耗时")
    print(f"edges:      {args.out_edges}")
    print(f"components: {args.out_components}")
    print(f"summary:    {args.out_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
