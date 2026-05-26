#!/usr/bin/env python3
"""对所有 partner pair 跑 factor_search，拿到完整 k 分布。

按 partner 恒等式：catalog 行 (A, B) 的 concordant N 列表里每对 (N_i, N_j) 都是
multi-N pair。把所有这些 partner pair（unreduced sorted）收集起来，逐个跑权威
factor_search，得到它们各自的 concordant_N，从而：

  1) 每个 partner 自身的 k = K_k 的"阶数"（用户在 wl055 讨论中确立的等价）。
  2) k=6, 7, ... 的实例就是 K_6, K_7, ... 子图候选。
  3) 顺便枚举出所有"非互素 multi-N pair"（catalog 在 coprime 约定下漏掉的那一类）。

输入  results/multi_concordant_N_max100000_fast.jsonl
输出  results/partner_pair_k_distribution.jsonl
      results/partner_pair_k_distribution_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from math import gcd
from pathlib import Path

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
        default=Path("results/partner_pair_k_distribution.jsonl"),
    )
    _ = p.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner_pair_k_distribution_summary.json"),
    )
    _ = p.add_argument(
        "--progress-every",
        type=int,
        default=1000,
        help="每多少个 partner 报告一次进度",
    )
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()

    catalog: dict[tuple[int, int], list[int]] = {}
    with args.in_path.open() as f:
        for line in f:
            r = json.loads(line)
            catalog[(int(r["A"]), int(r["B"]))] = [int(n) for n in r["concordant_N"]]
    print(f"catalog: {len(catalog)} 行")

    # 收集所有 partner pair（unreduced sorted）
    partners: set[tuple[int, int]] = set()
    for (_a, _b), Ns in catalog.items():
        for i in range(len(Ns)):
            for j in range(i + 1, len(Ns)):
                partners.add(sorted_pair(Ns[i], Ns[j]))

    print(f"unique partner pairs: {len(partners)}")
    print()

    # 对每个 partner 跑 / 取 factor_search
    print("跑 factor_search ...")
    rows: list[dict[str, object]] = []
    start = time.time()
    for idx, (a, b) in enumerate(sorted(partners), 1):
        # catalog 命中（partner 也是 catalog 行）→ 直接取
        if (a, b) in catalog:
            ns = catalog[(a, b)]
            source = "catalog"
        else:
            ns = find_concordant_by_factorization(a, b)
            source = "factor_search"
        g = gcd(a, b)
        rows.append(
            {
                "a": a,
                "b": b,
                "gcd": g,
                "coprime": g == 1,
                "k": len(ns),
                "concordant_N": ns,
                "source": source,
                "in_catalog": (a, b) in catalog,
            }
        )
        if idx % args.progress_every == 0:
            dt = time.time() - start
            print(f"  {idx:>6} / {len(partners)}  ({idx/dt:.1f}/s, eta {dt*(len(partners)-idx)/idx:.0f}s)")

    dt = time.time() - start
    print(f"完成 {len(rows)} 个 partner，用时 {dt:.1f}s ({len(rows)/dt:.1f}/s)")
    print()

    # 按 k 降序排
    rows.sort(key=lambda r: (-int(r["k"]), int(r["a"]), int(r["b"])))  # type: ignore[arg-type]

    # 直方图
    k_dist = Counter(int(r["k"]) for r in rows)  # type: ignore[arg-type]
    coprime_k_dist = Counter(int(r["k"]) for r in rows if bool(r["coprime"]))  # type: ignore[arg-type]
    noncoprime_k_dist = Counter(int(r["k"]) for r in rows if not bool(r["coprime"]))  # type: ignore[arg-type]
    in_cat_k_dist = Counter(int(r["k"]) for r in rows if bool(r["in_catalog"]))  # type: ignore[arg-type]

    print("=== partner k 分布（全部）===")
    for k in sorted(k_dist):
        print(f"  k={k:>2}  total={k_dist[k]:>6}  coprime={coprime_k_dist.get(k, 0):>5}  "
              f"non-coprime={noncoprime_k_dist.get(k, 0):>5}  in_catalog={in_cat_k_dist.get(k, 0):>4}")

    # K_6+ 高亮
    print()
    print("=== K_5+ 实例（partner 自身 k>=5，对应 K_k）===")
    high_k = [r for r in rows if int(r["k"]) >= 5]  # type: ignore[arg-type]
    for r in high_k[:20]:
        tag = "C" if r["in_catalog"] else "P"
        print(f"  K_{r['k']}  [{tag}]  ({int(r['a']):>5}, {int(r['b']):>5})  "  # type: ignore[arg-type]
              f"gcd={r['gcd']:>4}  N={r['concordant_N']}")
    if len(high_k) > 20:
        print(f"  ... 共 {len(high_k)} 个 K_5+")

    # 输出
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        for r in rows:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary = {
        "catalog_rows": len(catalog),
        "unique_partner_pairs": len(partners),
        "k_distribution_total": dict(sorted(k_dist.items())),
        "k_distribution_coprime": dict(sorted(coprime_k_dist.items())),
        "k_distribution_non_coprime": dict(sorted(noncoprime_k_dist.items())),
        "k_distribution_in_catalog": dict(sorted(in_cat_k_dist.items())),
        "K5_count": sum(c for k, c in k_dist.items() if k == 5),
        "K6_count": sum(c for k, c in k_dist.items() if k == 6),
        "K7plus_count": sum(c for k, c in k_dist.items() if k >= 7),
        "max_k": max(k_dist.keys()) if k_dist else 0,
        "top_k5plus": [
            {
                "a": int(r["a"]),  # type: ignore[arg-type]
                "b": int(r["b"]),  # type: ignore[arg-type]
                "gcd": int(r["gcd"]),  # type: ignore[arg-type]
                "k": int(r["k"]),  # type: ignore[arg-type]
                "N": r["concordant_N"],
                "in_catalog": bool(r["in_catalog"]),
            }
            for r in high_k[:30]
        ],
    }
    with args.summary_out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"输出: {args.out}")
    print(f"摘要: {args.summary_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
