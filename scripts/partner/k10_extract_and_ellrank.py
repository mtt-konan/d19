#!/usr/bin/env python3
"""1. 从 wl061 components 数据找出全部 k_real=10 + k_real=9 实例
2. 对每个跑 PARI ellrank，验证 wl060 "rank ≤ 4" 假设

K_10: 全 6 个跑
K_9:  全 42 个里抽 sample（前 10 个）
K_8:  跳过（wl060 已跑）

并行用 rational_distance.parallel.parallel_map。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def _scan_k(p: tuple[int, int]) -> tuple[tuple[int, int], int]:
    """worker: 算 (a, b) 的 k_real."""
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )
    a, b = p
    return p, len(find_concordant_by_factorization(a, b))


def main() -> int:
    from rational_distance.concordant.analysis import compute_rank
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )
    from rational_distance.parallel import (
        add_parallel_args,
        get_parallel_config_from_args,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--k9-limit",
        type=int,
        default=0,
        help="K_9 hub 上限 (0 = 全部 42 个; >0 取前 N 个 sample)",
    )
    add_parallel_args(parser)
    args = parser.parse_args()
    cfg = get_parallel_config_from_args(args)
    k9_limit = int(args.k9_limit)

    # 1. 加载 wl061 components 全部顶点
    comps_path = ROOT / "results/partner/partner_full_bfs_components.jsonl"
    all_pairs: list[tuple[int, int]] = []
    with comps_path.open() as f:
        for line in f:
            c = json.loads(line)
            for v in c["vertices"]:
                all_pairs.append((int(v[0]), int(v[1])))
    print(f"加载 {len(all_pairs)} G_M 顶点", flush=True)
    print(f"workers={cfg.workers}, chunksize={cfg.chunksize}", flush=True)

    # 2. 并行扫 k_real >= 9
    print("\n并行扫描 k_real ...", flush=True)
    high_k: list[tuple[int, tuple[int, int]]] = []
    t0 = time.time()
    last_t = t0
    n_done = 0

    def on_result(r):
        nonlocal n_done, last_t
        p, k = r
        n_done += 1
        if k >= 9:
            high_k.append((k, p))
        if time.time() - last_t > 5:
            rate = n_done / (time.time() - t0)
            eta = (len(all_pairs) - n_done) / rate if rate > 0 else 0
            print(f"  [{time.time()-t0:.0f}s] {n_done}/{len(all_pairs)} "
                  f"({rate:.0f}/s, ETA {eta:.0f}s), k>=9 found={len(high_k)}",
                  flush=True)
            last_t = time.time()

    _ = cfg.map(_scan_k, all_pairs, on_result=on_result, collect_results=False)
    high_k.sort(reverse=True)
    print(f"\n[{time.time()-t0:.1f}s] 扫描完成: {len(high_k)} 个 k>=9 顶点",
          flush=True)

    k10 = [p for k, p in high_k if k == 10]
    k9 = [p for k, p in high_k if k == 9]
    print(f"  k=10: {len(k10)}")
    print(f"  k=9 : {len(k9)}")

    # K_9: 默认全跑 (k9_limit=0); 否则取前 k9_limit 个
    k9_sorted = sorted(k9)
    k9_targets = k9_sorted if k9_limit <= 0 else k9_sorted[:k9_limit]

    targets: list[tuple[str, tuple[int, int]]] = (
        [("K_10", p) for p in k10] + [("K_9", p) for p in k9_targets]
    )
    k9_desc = "全" if k9_limit <= 0 else f"sample={len(k9_targets)}"
    print(f"\n准备跑 ellrank: {len(targets)} pairs (K_10 全, K_9 {k9_desc})")
    print()

    # 3. 跑 ellrank
    print(f"{'class':<6}{'pair':<24}{'k':<4}{'rank':<14}{'deficit':<8}"
          f"{'sha2':<6}{'#gens':<6}{'time':<10}")
    print("-" * 110)

    rows: list[dict[str, object]] = []
    for cls, (a, b) in targets:
        ns = find_concordant_by_factorization(a, b)
        k = len(ns)
        t1 = time.time()
        try:
            _rank, (lo, hi), sha2, gens = compute_rank(a, b, effort=1)
        except Exception as e:
            print(f"{cls:<6}({a:>6}, {b:>7})  {k:<4}ERROR: {e}")
            continue
        dt = time.time() - t1
        rank_str = f"{lo}" if lo == hi else f"{lo}..{hi}"
        deficit = k - lo
        flag = ""
        if lo > 4:
            flag = " !! rank>4 (违反 wl060 假设)"
        elif deficit >= 5:
            flag = " ⚠ high deficit"
        print(f"{cls:<6}({a:>6}, {b:>7})  {k:<4}{rank_str:<14}{deficit:<8}{sha2:<6}"
              f"{len(gens):<6}{dt:>6.1f}s{flag}")
        rows.append({
            "class": cls, "a": a, "b": b, "k": k,
            "concordant_N": ns,
            "rank_lower": lo, "rank_upper": hi,
            "rank_certified": lo == hi,
            "deficit": deficit,
            "sha2_lower": sha2,
            "n_gens": len(gens),
            "generators": [list(g) for g in gens],
            "elapsed_s": round(dt, 2),
        })

    out_path = ROOT / "results/partner/k9k10_ellrank_full.jsonl"
    with out_path.open("w") as f:
        for r in rows:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 4. 聚合
    print()
    print("聚合统计:")
    from collections import defaultdict
    by_cls: dict[str, list[int]] = defaultdict(list)
    by_cls_def: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_cls[str(r["class"])].append(int(cast(int, r["rank_lower"])))
        by_cls_def[str(r["class"])].append(int(cast(int, r["deficit"])))
    for cls in ("K_10", "K_9"):
        ranks = by_cls[cls]
        defs = by_cls_def[cls]
        if ranks:
            print(f"  {cls}:  rank min={min(ranks)} max={max(ranks)} "
                  f"avg={sum(ranks)/len(ranks):.2f}  "
                  f"deficit min={min(defs)} max={max(defs)} avg={sum(defs)/len(defs):.2f}  "
                  f"count={len(ranks)}")
            rank_gt_4 = sum(1 for r in ranks if r > 4)
            print(f"         rank > 4: {rank_gt_4} / {len(ranks)}")

    print(f"\nresult: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
