#!/usr/bin/env python3
"""全 G_M closure 扫描：把"反例搜索"从 catalog (10,333) 升级到 G_M (338,225)。

对 wl061 BFS 找到的全部 338,225 multi-N pair 检查 closure (N_i + N_j == A + B)。
之前所有 closure 扫描都限制在 catalog 互素行；本次第一次跑遍 G_M 全顶点
（含 ~327K 非互素 partner-only 顶点）。

并行化用 rational_distance.parallel.parallel_map (10 核)。
预计 ≈ 1-2 min for 338K vertices。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def _check_closure(p: tuple[int, int]) -> tuple[tuple[int, int], int, list[tuple[int, int]]]:
    """worker：对 (a, b) 算 N 列表 + 检查 closure。"""
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )
    a, b = p
    ns = find_concordant_by_factorization(a, b)
    target = a + b
    hits: list[tuple[int, int]] = []
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            if ns[i] + ns[j] == target:
                hits.append((ns[i], ns[j]))
    return p, len(ns), hits


def main() -> int:
    from rational_distance.parallel import add_parallel_args, get_parallel_config_from_args

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/full_gm_closure_scan.jsonl"),
    )
    _ = parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/full_gm_closure_scan_summary.json"),
    )
    add_parallel_args(parser)
    args = parser.parse_args()
    cfg = get_parallel_config_from_args(args)

    t0 = time.time()

    # 1. 加载所有 G_M 顶点
    all_pairs: list[tuple[int, int]] = []
    component_of: dict[tuple[int, int], int] = {}
    with cast(Path, args.components).open() as f:
        for line in f:
            c = json.loads(line)
            cid = int(c["component_id"])
            for v in c["vertices"]:
                p = (int(v[0]), int(v[1]))
                all_pairs.append(p)
                component_of[p] = cid
    print(f"[{time.time()-t0:.1f}s] 加载 {len(all_pairs)} 顶点", flush=True)
    print(f"  workers={cfg.workers}, chunksize={cfg.chunksize}", flush=True)

    # 2. 并行 closure 检查
    closure_hits: list[tuple[tuple[int, int], int, list[tuple[int, int]]]] = []
    k_counter: dict[int, int] = {}
    n_processed = 0
    last_report_t = t0

    def on_result(r):
        nonlocal n_processed, last_report_t
        p, k, hits = r
        n_processed += 1
        k_counter[k] = k_counter.get(k, 0) + 1
        if hits:
            closure_hits.append((p, k, hits))
        if time.time() - last_report_t > 5:
            rate = n_processed / (time.time() - t0)
            eta = (len(all_pairs) - n_processed) / rate if rate > 0 else 0
            print(f"  [{time.time()-t0:.1f}s] {n_processed}/{len(all_pairs)} "
                  f"({rate:.0f}/s, ETA {eta:.0f}s), closure hits={len(closure_hits)}",
                  flush=True)
            last_report_t = time.time()

    _ = cfg.map(_check_closure, all_pairs, on_result=on_result, collect_results=False)
    print(f"[{time.time()-t0:.1f}s] closure 检查完成", flush=True)

    # 3. 报告
    print()
    print(f"Total vertices scanned: {len(all_pairs)}")
    print(f"Total closure hits:     {len(closure_hits)}")
    print()
    print("k 分布:")
    for k in sorted(k_counter.keys()):
        if k_counter[k] > 0:
            print(f"  k = {k:<4}{k_counter[k]:>8}")

    if closure_hits:
        print()
        print(f"!!! CLOSURE HITS FOUND ({len(closure_hits)} pairs) !!!")
        for (a, b), k, hits in closure_hits[:20]:
            cid = component_of[(a, b)]
            print(f"  ({a:>7}, {b:>7})  k={k}  comp={cid}  hits={hits}")
        if len(closure_hits) > 20:
            print(f"  ... {len(closure_hits) - 20} more")
    else:
        print()
        print("NO closure hits — counterexample remains absent in G_M @ max_value=1M.")

    # 4. 持久化
    out_path = cast(Path, args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        for (a, b), k, hits in closure_hits:
            _ = f.write(json.dumps({
                "A": a, "B": b, "k": k,
                "component_id": component_of[(a, b)],
                "closure_pairs": [[ni, nj] for ni, nj in hits],
            }, ensure_ascii=False) + "\n")

    summary = {
        "total_vertices": len(all_pairs),
        "total_closure_hits": len(closure_hits),
        "k_distribution": {str(k): k_counter[k] for k in sorted(k_counter.keys())},
        "k_max": max(k_counter.keys()),
        "elapsed_s": round(time.time() - t0, 1),
        "workers": cfg.workers,
    }
    summary_path = cast(Path, args.summary_out)
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print()
    print(f"[{time.time()-t0:.1f}s] 总耗时")
    print(f"closure hits: {out_path}")
    print(f"summary:      {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
