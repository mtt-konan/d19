#!/usr/bin/env python3
"""完整 BFS 探索整个 G_M (partner graph)，使用并行 find_concordant。

跟 partner_full_graph.py 的区别：
  partner_full_graph.py:  只走 catalog → level-1 → level-2，不闭合
  partner_full_bfs.py:    BFS fixed-point，直到没有新顶点加入

策略：
  1. 种子 = catalog 互素 multi-N pair (10333)
  2. 每轮 frontier 用 parallel_map(find_concordant_by_factorization)
     批量算 N 列表（多核加速）
  3. 把新发现的 partner pair 加入 frontier
  4. 直到 frontier 空（G_M 在 max_value 范围内闭合）
  5. union-find 输出 component 分布

工期估算（基于 wl061 的 ~280/s 串行速度）:
  max_value = 1M:  10333 + ~16000 partner-only ≈ 27000 顶点 × 1/280s ≈ 1.5 min
                   并行 8 核 ≈ 10-20 秒
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import cast

import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def sorted_pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def _compute_ns(p: tuple[int, int]) -> tuple[tuple[int, int], list[int]]:
    """worker 函数：算 (a, b) 的 concordant N。必须 top-level 才能 pickle。"""
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )
    a, b = p
    return p, find_concordant_by_factorization(a, b)


def parse_args() -> argparse.Namespace:
    from rational_distance.parallel import add_parallel_args
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--catalog",
        type=Path,
        default=Path("results/multi_concordant_N_max100000_fast.jsonl"),
    )
    _ = p.add_argument(
        "--max-value",
        type=int,
        default=1_000_000,
        help="跳过 N > max_value 的 partner pair（避免 BFS 爆炸）",
    )
    _ = p.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("results/partner_full_bfs"),
    )
    add_parallel_args(p)
    return p.parse_args()


def main() -> int:
    from rational_distance.parallel import get_parallel_config_from_args

    args = parse_args()
    cfg = get_parallel_config_from_args(args)
    max_value = cast(int, args.max_value)

    t0 = time.time()

    # 1. 加载 catalog 作为种子
    seeds: set[tuple[int, int]] = set()
    catalog_set: set[tuple[int, int]] = set()
    with cast(Path, args.catalog).open() as f:
        for line in f:
            row = json.loads(line)
            ab = (int(row["A"]), int(row["B"]))
            if max(ab) <= max_value:
                seeds.add(ab)
                catalog_set.add(ab)
    print(f"[{time.time()-t0:.1f}s] Seeds (catalog): {len(seeds)} pairs", flush=True)
    print(f"  workers={cfg.workers}, chunksize={cfg.chunksize}, max_value={max_value}", flush=True)

    # 2. BFS fixed-point
    vertices_with_N: dict[tuple[int, int], list[int]] = {}
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    visited: set[tuple[int, int]] = set()
    frontier: set[tuple[int, int]] = seeds.copy()
    round_num = 0

    while frontier:
        round_num += 1
        batch = [p for p in frontier if p not in visited and max(p) <= max_value]
        if not batch:
            break

        t1 = time.time()
        # 并行算 N 列表
        results = cfg.map(_compute_ns, batch)
        compute_time = time.time() - t1

        # 单线程更新 visited + edges + 下轮 frontier
        next_frontier: set[tuple[int, int]] = set()
        for p, ns in results:
            visited.add(p)
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
                    if u not in visited:
                        next_frontier.add(u)

        print(
            f"[{time.time()-t0:.1f}s] round {round_num}: "
            f"processed {len(batch)}, edges={len(edges)}, "
            f"visited={len(visited)}, next_frontier={len(next_frontier)}, "
            f"compute={compute_time:.1f}s",
            flush=True,
        )
        frontier = next_frontier

    print(f"[{time.time()-t0:.1f}s] BFS 完成: {len(visited)} 顶点, {len(edges)} 边", flush=True)

    # 3. union-find on edges
    vertices = set(visited)
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)
    parent: dict[tuple[int, int], tuple[int, int]] = {v: v for v in vertices}

    def find(x: tuple[int, int]) -> tuple[int, int]:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv

    components: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for v in vertices:
        components.setdefault(find(v), []).append(v)

    print(f"[{time.time()-t0:.1f}s] union-find 完成: {len(components)} components", flush=True)

    # 4. 报告
    comp_list = sorted(components.values(), key=lambda c: -len(c))
    comp_edges: dict[tuple[int, int], int] = {}
    for u, v in edges:
        root = find(u)
        comp_edges[root] = comp_edges.get(root, 0) + 1

    print()
    print("顶部 20 components:")
    print(f"  {'rank':<5}{'size':<6}{'edges':<7}{'cycle':<7}{'in_cat':<7}{'代表顶点':<22}")
    print("  " + "-" * 60)
    for i, c in enumerate(comp_list[:20]):
        eroot = find(c[0])
        e_cnt = comp_edges.get(eroot, 0)
        circuit = e_cnt - len(c) + 1
        in_cat = sum(1 for v in c if v in catalog_set)
        ex = c[0]
        print(f"  {i+1:<5}{len(c):<6}{e_cnt:<7}{circuit:<7}{in_cat:<7}({ex[0]}, {ex[1]})")

    # size 分布
    sizes = sorted([len(c) for c in comp_list], reverse=True)
    from collections import Counter
    size_hist = Counter(sizes)
    print()
    print("Size 分布（>= 3 或 size <= 4）:")
    for s in sorted(size_hist.keys()):
        cnt = size_hist[s]
        if cnt >= 3 or s <= 4:
            print(f"  size = {s:<6}  count = {cnt}")

    # circuit rank 分布
    print()
    print("Circuit rank 总览:")
    total_circuit = sum(comp_edges.get(find(c[0]), 0) - len(c) + 1 for c in comp_list)
    n_tree_comps = sum(1 for c in comp_list if comp_edges.get(find(c[0]), 0) - len(c) + 1 == 0)
    print(f"  总 circuit rank (= E - V + components) = {len(edges) - len(vertices) + len(components)}")
    print(f"  sum of per-component circuit ranks    = {total_circuit}")
    print(f"  pure-tree components: {n_tree_comps} / {len(components)} = {100*n_tree_comps/len(components):.1f}%")
    print(f"  非 tree components:  {len(components) - n_tree_comps}")

    # 5. 持久化
    out_prefix = cast(Path, args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    with (out_prefix.parent / f"{out_prefix.name}_edges.jsonl").open("w") as f:
        for u, v in sorted(edges):
            _ = f.write(json.dumps({"u": list(u), "v": list(v)}, ensure_ascii=False) + "\n")

    with (out_prefix.parent / f"{out_prefix.name}_components.jsonl").open("w") as f:
        for i, c in enumerate(comp_list):
            eroot = find(c[0])
            e_cnt = comp_edges.get(eroot, 0)
            in_cat = sum(1 for v in c if v in catalog_set)
            _ = f.write(json.dumps({
                "component_id": i,
                "size": len(c),
                "edges": e_cnt,
                "circuit_rank": e_cnt - len(c) + 1,
                "in_catalog": in_cat,
                "vertices": [list(v) for v in sorted(c)],
            }, ensure_ascii=False) + "\n")

    summary = {
        "catalog_size": len(catalog_set),
        "max_value": max_value,
        "vertices": len(vertices),
        "edges": len(edges),
        "components": len(components),
        "largest_component_size": sizes[0] if sizes else 0,
        "pure_tree_components": n_tree_comps,
        "total_circuit_rank": len(edges) - len(vertices) + len(components),
        "round_count": round_num,
        "elapsed_s": round(time.time() - t0, 1),
        "workers": cfg.workers,
        "size_histogram": {str(s): c for s, c in sorted(size_hist.items())},
    }
    with (out_prefix.parent / f"{out_prefix.name}_summary.json").open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"[{time.time()-t0:.1f}s] 总耗时")
    print(f"summary: {out_prefix.parent / (out_prefix.name + '_summary.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
