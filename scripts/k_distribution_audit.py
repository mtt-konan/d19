#!/usr/bin/env python3
"""统计 reduced multi-N pair (max_hyp) 的 k 分布, 区分 safe-pass vs 否."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-hyp", type=int, default=2_000_000)
    args = parser.parse_args()

    print(f"[phase] enumerating multi-N pairs at max_hyp={args.max_hyp}")
    pairs_data = fast_multi_concordant_pairs(args.max_hyp)
    print(f"[done] {len(pairs_data)} multi-N pairs")

    k_safe: Counter[int] = Counter()
    k_unsafe: Counter[int] = Counter()
    for (A, B), ns in pairs_data.items():
        k = len(ns)
        if allow_reduced_pair(A, B):
            k_safe[k] += 1
        else:
            k_unsafe[k] += 1

    print(f"\n=== k 分布 (safe-pass vs unsafe) ===")
    print(f"{'k':>3} {'safe-pass':>10} {'unsafe':>10}")
    all_k = sorted(set(k_safe.keys()) | set(k_unsafe.keys()))
    for k in all_k:
        print(f"{k:>3} {k_safe.get(k, 0):>10} {k_unsafe.get(k, 0):>10}")
    print(f"\ntotal safe-pass: {sum(k_safe.values())}")
    print(f"total unsafe:    {sum(k_unsafe.values())}")


if __name__ == "__main__":
    main()
