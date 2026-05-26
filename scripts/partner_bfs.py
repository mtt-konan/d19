#!/usr/bin/env python3
"""partner graph G_M 上从给定根节点 (A, B) 出发的 BFS。

每访问一个 multi-N pair (X, Y)，跑权威 find_concordant_by_factorization 拿
concordant_N，把所有 C(k, 2) 个 partner pair 加入 frontier。

约束：
  - max(X, Y) <= max-value  (避免向上无限发散)
  - 已访问的 pair 不重复展开
  - 可选 max-visited 截断，防止意外爆炸

输出：
  results/partner_bfs_root{A}_{B}_M{max_value}.jsonl       全部节点 + 各自的 N 与邻居
  results/partner_bfs_root{A}_{B}_M{max_value}_summary.json 节点数、深度分布、k 分布等
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, deque
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def sorted_pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument("root", type=str, help="根节点，格式 a,b（例如 264,420）")
    _ = p.add_argument("--max-value", type=int, default=10000,
                       help="限制节点 max(a, b) 的上界")
    _ = p.add_argument("--max-visited", type=int, default=20000,
                       help="访问节点数上限（防爆炸）")
    _ = p.add_argument("--out-dir", type=Path, default=Path("results"))
    _ = p.add_argument("--progress-every", type=int, default=200)
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()

    a_str, b_str = args.root.split(",")
    root = sorted_pair(int(a_str.strip()), int(b_str.strip()))

    print(f"BFS root          : {root}")
    print(f"max_value         : {args.max_value}")
    print(f"max_visited       : {args.max_visited}")
    print()

    # 节点表：pair -> {depth, k, N, source (parent), out_of_range_neighbors}
    nodes: dict[tuple[int, int], dict[str, object]] = {}
    edges: list[tuple[tuple[int, int], tuple[int, int]]] = []

    queue: deque[tuple[tuple[int, int], int, tuple[int, int] | None]] = deque()
    queue.append((root, 0, None))
    nodes[root] = {"depth": 0, "parent": None}

    start = time.time()
    leaves = 0  # k=1 节点
    out_of_range = 0  # 邻居越界数
    expansions = 0  # 实际跑 factor_search 的次数

    while queue and len(nodes) < args.max_visited:
        cur, depth, parent = queue.popleft()
        a, b = cur

        ns = find_concordant_by_factorization(a, b)
        expansions += 1
        k = len(ns)
        nodes[cur].update({
            "k": k,
            "concordant_N": ns,
            "gcd": gcd(a, b),
        })

        if k < 2:
            leaves += 1
            continue

        # 把 C(k, 2) 个 partner pair 加入 frontier
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                neighbor = sorted_pair(ns[i], ns[j])
                edges.append((cur, neighbor))
                if max(neighbor) > args.max_value:
                    out_of_range += 1
                    continue
                if neighbor in nodes:
                    continue
                nodes[neighbor] = {"depth": depth + 1, "parent": list(cur)}
                queue.append((neighbor, depth + 1, cur))

        if expansions % args.progress_every == 0:
            dt = time.time() - start
            print(f"  expanded {expansions:>5}  visited {len(nodes):>5}  "
                  f"queue {len(queue):>5}  edges {len(edges):>6}  "
                  f"leaves {leaves:>4}  oor {out_of_range:>5}  ({dt:.1f}s)")

    dt = time.time() - start
    print()
    print(f"完成: 访问 {len(nodes)} 节点, 展开 {expansions} 次 factor_search, "
          f"{len(edges)} 条边")
    print(f"  叶节点 (k=1):           {leaves}")
    print(f"  截断 (max_visited 上限): {'是' if len(nodes) >= args.max_visited else '否'}")
    print(f"  出界邻居 (max_value 限): {out_of_range}")
    print(f"  用时:                   {dt:.1f}s")
    print()

    # 深度分布
    depth_dist = Counter(int(n["depth"]) for n in nodes.values())  # type: ignore[arg-type]
    k_dist = Counter(int(n.get("k", 0)) for n in nodes.values() if "k" in n)  # type: ignore[arg-type]

    print("深度分布:")
    for d in sorted(depth_dist):
        print(f"  depth={d:>2}  {depth_dist[d]:>5} nodes")
    print()
    print("k 分布（已展开节点）:")
    for kv in sorted(k_dist):
        print(f"  k={kv:>2}    {k_dist[kv]:>5} nodes")
    print()

    # 顶点最高 k
    top = sorted(
        ((p, int(n["k"])) for p, n in nodes.items() if "k" in n),  # type: ignore[arg-type]
        key=lambda x: -x[1],
    )[:10]
    print("Top-10 高 k 顶点:")
    for p, kv in top:
        print(f"  {p}  k={kv}  depth={nodes[p]['depth']}")
    print()

    # 输出
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"partner_bfs_root{root[0]}_{root[1]}_M{args.max_value}"
    nodes_path = args.out_dir / f"{stem}.jsonl"
    summary_path = args.out_dir / f"{stem}_summary.json"
    edges_path = args.out_dir / f"{stem}_edges.jsonl"

    with nodes_path.open("w") as f:
        for p, info in nodes.items():
            row = {"pair": list(p), **info}
            _ = f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with edges_path.open("w") as f:
        for u, v in edges:
            _ = f.write(json.dumps({"u": list(u), "v": list(v)},
                                   ensure_ascii=False) + "\n")

    summary = {
        "root": list(root),
        "max_value": args.max_value,
        "max_visited": args.max_visited,
        "visited_count": len(nodes),
        "edge_count": len(edges),
        "expansions": expansions,
        "leaves_k1": leaves,
        "out_of_range_neighbors": out_of_range,
        "truncated_by_max_visited": len(nodes) >= args.max_visited,
        "elapsed_s": round(dt, 2),
        "depth_distribution": dict(sorted(depth_dist.items())),
        "k_distribution": dict(sorted(k_dist.items())),
        "top_high_k": [
            {"pair": list(p), "k": kv, "depth": nodes[p]["depth"]}
            for p, kv in top
        ],
    }
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"节点输出: {nodes_path}")
    print(f"边输出  : {edges_path}")
    print(f"摘要    : {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
