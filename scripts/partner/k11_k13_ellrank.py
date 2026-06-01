#!/usr/bin/env python3
"""对 wl085 D-scaling 生成的 K_11/K_12/K_13 hub 直接跑 PARI ellrank。

E.2 延伸：wl094 已验证 catalog/partner-web 内的 K_9/K_10 全部 rank ≤ 4。
wl085 用 D-scaling 在 max_value=1M BFS 范围外造出了 K_11–K_13 hub
(全来自 primitive (91,990) rank=4 与 (221,704) rank=3 的放大)。

D-scaling 理论 (wl065/wl085): E_{a₀,b₀} ≅ E_{d·a₀, d·b₀} over ℚ ⟹ rank 不变。
本脚本直接对放大后的大 (a, b) 跑 compute_rank, 双重验证:
  1. 放大 hub 的 rank == primitive rank (D-scaling rank 不变性的算术验证)
  2. rank ≤ 4 在 k=11–13 仍成立

输入: results/multi_n/dscale_kn_smoke.jsonl (wl085 生成, k>=11 行)
输出: results/partner/k11_k13_ellrank.jsonl
"""

from __future__ import annotations

import json
import sys
import time
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.concordant.analysis import compute_rank
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    smoke_path = ROOT / "results/multi_n/dscale_kn_smoke.jsonl"

    # 1. 抽 k>=11 的唯一 hub (按 (a,b) 取最大 k)
    best: dict[tuple[int, int], dict[str, object]] = {}
    with smoke_path.open() as f:
        for line in f:
            r = json.loads(line)
            if int(r["k"]) >= 11:
                key = (int(r["a"]), int(r["b"]))
                if key not in best or int(r["k"]) > int(best[key]["k"]):
                    best[key] = r
    hubs = sorted(best.values(), key=lambda r: (-int(r["k"]), int(r["a"])))
    print(f"读到 {len(hubs)} 个唯一 K_11+ hub (来源: {smoke_path.name})")
    print()

    # 2. primitive rank 缓存 (交叉验证 D-scaling 不变性)
    prim_rank: dict[tuple[int, int], int] = {}

    print(
        f"{'class':<6}{'pair (scaled)':<26}{'k':<4}{'rank':<10}{'deficit':<8}"
        f"{'sha2':<6}{'prim':<12}{'prim_rk':<8}{'match':<7}{'time':<9}"
    )
    print("-" * 120)

    rows: list[dict[str, object]] = []
    for r in hubs:
        a, b = int(r["a"]), int(r["b"])
        pa, pb = int(r["primitive_a"]), int(r["primitive_b"])
        k = int(r["k"])

        # primitive rank (算一次缓存)
        if (pa, pb) not in prim_rank:
            _pr, (plo, phi), _ps, _pg = compute_rank(pa, pb, effort=1)
            prim_rank[(pa, pb)] = plo if plo == phi else -1
        prk = prim_rank[(pa, pb)]

        # 直接对放大 hub 跑 ellrank
        t1 = time.time()
        try:
            _rank, (lo, hi), sha2, gens = compute_rank(a, b, effort=1)
        except Exception as e:
            print(f"K_{k:<4}({a:>8}, {b:>9})  ERROR: {e}")
            continue
        dt = time.time() - t1

        # closure 检查 (反例条件, 期望 0)
        ns = find_concordant_by_factorization(a, b)
        target = a + b
        closure = [
            (ns[i], ns[j])
            for i in range(len(ns))
            for j in range(i + 1, len(ns))
            if ns[i] + ns[j] == target
        ]

        rank_str = f"{lo}" if lo == hi else f"{lo}..{hi}"
        deficit = k - lo
        match = "yes" if (lo == hi and lo == prk) else "NO"
        flag = ""
        if lo > 4:
            flag = " !! rank>4 (违反假设)"
        if closure:
            flag += f" !! CLOSURE {closure}"
        print(
            f"K_{k:<4}({a:>8}, {b:>9})  {k:<4}{rank_str:<10}{deficit:<8}{sha2:<6}"
            f"({pa},{pb})".ljust(12)
            + f"{prk:<8}{match:<7}{dt:>6.1f}s{flag}"
        )
        rows.append(
            {
                "class": f"K_{k}",
                "a": a,
                "b": b,
                "d": int(r["d"]),
                "primitive_a": pa,
                "primitive_b": pb,
                "primitive_rank": prk,
                "gcd": gcd(a, b),
                "k": k,
                "k_factorization": len(ns),
                "concordant_N": ns,
                "rank_lower": lo,
                "rank_upper": hi,
                "rank_certified": lo == hi,
                "rank_matches_primitive": lo == hi and lo == prk,
                "deficit": deficit,
                "sha2_lower": sha2,
                "n_gens": len(gens),
                "generators": [list(g) for g in gens],
                "closure_pairs": closure,
                "elapsed_s": round(dt, 2),
            }
        )

    out_path = ROOT / "results/partner/k11_k13_ellrank.jsonl"
    with out_path.open("w") as f:
        for row in rows:
            _ = f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # 3. 聚合
    print()
    print("聚合:")
    from collections import Counter, defaultdict

    by_cls: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        by_cls[str(row["class"])].append(int(row["rank_lower"]))
    for cls in sorted(by_cls, key=lambda c: -int(c.split("_")[1])):
        ranks = by_cls[cls]
        rc = Counter(ranks)
        rgt4 = sum(1 for x in ranks if x > 4)
        print(
            f"  {cls}: n={len(ranks)}  rank 分布={dict(sorted(rc.items()))}  "
            f"rank>4={rgt4}"
        )
    n_total = len(rows)
    n_cert = sum(1 for r in rows if r["rank_certified"])
    n_match = sum(1 for r in rows if r["rank_matches_primitive"])
    n_clo = sum(1 for r in rows if r["closure_pairs"])
    n_gt4 = sum(1 for r in rows if int(r["rank_lower"]) > 4)
    print()
    print(f"  certified (lo==hi):        {n_cert}/{n_total}")
    print(f"  rank == primitive rank:    {n_match}/{n_total}")
    print(f"  rank > 4:                  {n_gt4}/{n_total}")
    print(f"  closure hits:              {n_clo}/{n_total}")
    print(f"\nresult: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
