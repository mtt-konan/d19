#!/usr/bin/env python3
"""对 wl055 发现的 K_8/K_7/K_6 顶级 hub 跑 PARI ellrank。

预期（按 wl059 deficit 猜想）：
  k=8 hub 应有 deficit ≥ 3（即 rank ≤ 5）
  k=7 hub 应有 deficit ≥ 2（即 rank ≤ 5）

实证后看是否成立。
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.concordant.analysis import compute_rank
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    # K_8 顶端 (wl055 发现)
    k8 = [
        (55440, 445536),
        (58800, 98280),
    ]
    # K_7 (wl055 全部 4 个)
    k7 = [
        (10200, 37128),
        (10920, 118800),
        (50160, 403104),
        (102000, 303600),
    ]
    # K_6 取样（wl055 顶 5 个）
    k6 = [
        (2640, 21216),
        (3696, 8160),
        (4680, 95760),
        (5304, 27300),
        (5460, 59400),
    ]
    targets = [("K_8", p) for p in k8] + [("K_7", p) for p in k7] + [("K_6", p) for p in k6]

    print(f"{'class':<6}{'pair':<24}{'k':<4}{'rank':<14}{'deficit':<8}{'sha2':<6}{'#gens':<6}{'time':<10}")
    print("-" * 110)

    rows: list[dict[str, object]] = []
    for cls, (a, b) in targets:
        ns = find_concordant_by_factorization(a, b)
        k = len(ns)
        t0 = time.time()
        try:
            _rank, (lo, hi), sha2, gens = compute_rank(a, b, effort=1)
        except Exception as e:
            print(f"{cls:<6}({a:>5}, {b:>6})  {k:<4}ERROR: {e}")
            continue
        dt = time.time() - t0
        rank_str = f"{lo}" if lo == hi else f"{lo}..{hi}"
        deficit = k - lo
        flag = " ⚠⚠" if deficit >= 3 else (" ⚠" if deficit >= 2 else "")
        print(f"{cls:<6}({a:>5}, {b:>6})  {k:<4}{rank_str:<14}{deficit:<8}{sha2:<6}"
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

    out_path = ROOT / "results/k8_ellrank_wl055_top_hubs.jsonl"
    with out_path.open("w") as f:
        for r in rows:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nrank 数据: {out_path}")

    # 简单聚合
    print()
    print("按 K_n 聚合 deficit:")
    from collections import defaultdict
    by_class: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_class[str(r["class"])].append(int(r["deficit"]))  # type: ignore[arg-type]
    for cls in ("K_8", "K_7", "K_6"):
        ds = by_class[cls]
        if ds:
            print(f"  {cls}:  min={min(ds)}  max={max(ds)}  avg={sum(ds)/len(ds):.1f}  count={len(ds)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
