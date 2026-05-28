#!/usr/bin/env python3
"""对 (153, 560) 6-cycle 上 6 个 multi-N pair 跑 PARI ellrank。

cycle:
  (560, 2925) — (420, 1344) — (1008, 2925) — (1344, 7020) — (2925, 9360) — (1344, 3900) —|
                                                                                           |
                  back to (560, 2925) ←--------------------------------------------------|
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.concordant.analysis import compute_rank
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    # 6-cycle from (153, 560) BFS (wl058 finding)
    cycle = [
        (560, 2925),
        (420, 1344),
        (1008, 2925),
        (1344, 7020),
        (2925, 9360),
        (1344, 3900),
    ]
    # 加上几个相关参考点
    extras = [
        (153, 560),    # BFS root
        (264, 420),    # 另一个 component 的 hub (作为对照)
    ]

    all_pairs = cycle + extras

    import json

    print(f"{'pair':<18}{'k':<4}{'rank':<14}{'k-rank':<8}{'sha2':<6}{'#gens':<6}{'time':<8}")
    print("-" * 100)

    rows: list[dict[str, object]] = []
    for a, b in all_pairs:
        ns = find_concordant_by_factorization(a, b)
        k = len(ns)
        t0 = time.time()
        try:
            _rank, (lo, hi), sha2, gens = compute_rank(a, b, effort=1)
        except Exception as e:
            print(f"({a:>5}, {b:>5})  {k:<4}ERROR: {e}")
            continue
        dt = time.time() - t0
        rank_str = f"{lo}" if lo == hi else f"{lo}..{hi}"
        deficit = k - lo  # k - rank_lower
        flag = " ⚠" if deficit >= 2 else ""
        print(f"({a:>5}, {b:>5})  {k:<4}{rank_str:<14}{deficit:<8}{sha2:<6}{len(gens):<6}{dt:>5.1f}s{flag}")
        print(f"                                                   N = {ns}")
        rows.append({
            "a": a, "b": b, "k": k, "concordant_N": ns,
            "rank_lower": lo, "rank_upper": hi,
            "rank_certified": lo == hi,
            "k_minus_rank": deficit,
            "sha2_lower": sha2,
            "n_gens_returned": len(gens),
            "generators": [list(g) for g in gens],
            "elapsed_s": round(dt, 2),
        })

    out_path = ROOT / "results/cycle_ellrank_wl058_6cycle.jsonl"
    with out_path.open("w") as f:
        for r in rows:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nrank 数据: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
