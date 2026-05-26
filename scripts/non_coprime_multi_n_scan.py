#!/usr/bin/env python3
"""直接扫描所有 gcd > 1 的 (a, b) 跑 factor_search，对比 partner 全扫集合，
量化 "partner 反推漏了多少非互素 multi-N pair"。

输入:
  results/partner_pair_k_distribution.jsonl     已知 partner 集（10,533 个非互素 multi-N）

输出:
  results/non_coprime_scan_max{M}.jsonl                  在 [1, M]² 内所有 k>=2 实例
  results/non_coprime_scan_max{M}_summary.json           覆盖率统计 + 漏掉的实例

约定: a < b, gcd(a, b) > 1, 1 <= a, b <= M。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument("--max", dest="max_v", type=int, default=500,
                       help="扫描上界 M (a, b ∈ [1, M])")
    _ = p.add_argument("--partner-set", type=Path,
                       default=Path("results/partner_pair_k_distribution.jsonl"))
    _ = p.add_argument("--out", type=Path, default=None)
    _ = p.add_argument("--progress-every", type=int, default=50,
                       help="每多少行 a 报告一次进度")
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()
    M = args.max_v

    if args.out is None:
        args.out = Path(f"results/non_coprime_scan_max{M}.jsonl")

    # 加载 partner 集
    partner_k: dict[tuple[int, int], int] = {}
    with args.partner_set.open() as f:
        for line in f:
            r = json.loads(line)
            partner_k[(int(r["a"]), int(r["b"]))] = int(r["k"])

    print(f"partner 集: {len(partner_k)} 条")
    print(f"扫描范围: 1 <= a < b <= {M}, gcd > 1")
    print()

    rows: list[dict[str, object]] = []
    total_pairs = 0
    multi_pairs = 0
    not_in_partner = 0
    start = time.time()

    for a in range(1, M + 1):
        for b in range(a + 1, M + 1):
            if gcd(a, b) == 1:
                continue
            total_pairs += 1
            ns = find_concordant_by_factorization(a, b)
            k = len(ns)
            if k >= 2:
                multi_pairs += 1
                in_partner = (a, b) in partner_k
                if not in_partner:
                    not_in_partner += 1
                rows.append(
                    {
                        "a": a,
                        "b": b,
                        "gcd": gcd(a, b),
                        "k": k,
                        "concordant_N": ns,
                        "in_partner_set": in_partner,
                        "partner_k_recorded": partner_k.get((a, b)),
                    }
                )
        if a % args.progress_every == 0:
            dt = time.time() - start
            eta = dt * (M - a) / a if a > 0 else 0
            print(f"  a={a:>4}/{M}  pairs_scanned={total_pairs:>7}  "
                  f"multi={multi_pairs:>5}  miss_in_partner={not_in_partner:>4}  "
                  f"({dt:.0f}s eta {eta:.0f}s)")

    dt = time.time() - start
    print()
    print(f"完成: 扫描 {total_pairs:,} 对 gcd>1 pair")
    print(f"  multi-N (k>=2):                  {multi_pairs:,}")
    print(f"  in partner 集:                    {multi_pairs - not_in_partner:,}")
    print(f"  not in partner 集 (漏掉):         {not_in_partner:,}")
    if multi_pairs > 0:
        cov = (multi_pairs - not_in_partner) / multi_pairs * 100
        print(f"  partner 集覆盖率:                 {cov:.2f}%")
    print(f"  用时 {dt:.1f}s")
    print()

    # 漏掉的实例样本（按 k 降序）
    missing = [r for r in rows if not r["in_partner_set"]]
    missing.sort(key=lambda r: (-int(r["k"]), int(r["a"]), int(r["b"])))  # type: ignore[arg-type]
    if missing:
        print(f"漏掉的非互素 multi-N pair（前 20 个，按 k 降序）:")
        for r in missing[:20]:
            print(f"  ({int(r['a']):>4}, {int(r['b']):>4})  "  # type: ignore[arg-type]
                  f"gcd={int(r['gcd']):>4}  k={int(r['k'])}  N={r['concordant_N']}")  # type: ignore[arg-type]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        for r in rows:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary_path = args.out.with_name(args.out.stem + "_summary.json")
    # k 分布 (扫描得到的 vs partner 集)
    from collections import Counter
    scan_k_dist = Counter(int(r["k"]) for r in rows)  # type: ignore[arg-type]
    miss_k_dist = Counter(int(r["k"]) for r in missing)  # type: ignore[arg-type]

    summary = {
        "max_v": M,
        "total_non_coprime_pairs": total_pairs,
        "multi_n_pairs_total": multi_pairs,
        "in_partner_set": multi_pairs - not_in_partner,
        "not_in_partner_set": not_in_partner,
        "coverage_pct": round(
            (multi_pairs - not_in_partner) / multi_pairs * 100, 2
        ) if multi_pairs > 0 else 0.0,
        "scan_k_distribution": dict(sorted(scan_k_dist.items())),
        "missing_k_distribution": dict(sorted(miss_k_dist.items())),
        "missing_top20": [
            {
                "a": int(r["a"]),  # type: ignore[arg-type]
                "b": int(r["b"]),  # type: ignore[arg-type]
                "gcd": int(r["gcd"]),  # type: ignore[arg-type]
                "k": int(r["k"]),  # type: ignore[arg-type]
                "N": r["concordant_N"],
            }
            for r in missing[:20]
        ],
        "elapsed_s": round(dt, 1),
    }
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"输出: {args.out}")
    print(f"摘要: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
