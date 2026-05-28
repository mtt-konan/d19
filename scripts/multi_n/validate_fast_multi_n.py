#!/usr/bin/env python3
"""Validate fast pivot-on-N scanner against authoritative ground truth.

Compares the output of `fast_multi_concordant_pairs(max_hyp)` against
`results/multi_concordant_N_max{max_hyp}.jsonl` (assumed authoritative).
Exits 0 iff every pair and its concordant_N list match exactly.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diff fast pivot-on-N scanner output against ground truth"
    )
    _ = parser.add_argument("--max-hyp", type=int, default=10000)
    _ = parser.add_argument(
        "--ground-truth",
        type=Path,
        default=None,
        help="Path to authoritative JSONL (default: results/multi_concordant_N_max{max_hyp}.jsonl)",
    )
    return parser.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
    from rational_distance.results.multi_concordant import iter_multi_concordant_pairs

    args = parse_args()
    max_hyp = cast(int, args.max_hyp)
    ground_truth = cast(Path | None, args.ground_truth)
    if ground_truth is None:
        ground_truth = ROOT / "results" / f"multi_concordant_N_max{max_hyp}.jsonl"

    if not ground_truth.exists():
        print(f"ground truth missing: {ground_truth}")
        return 2

    print(f"max_hyp={max_hyp}")
    print(f"ground truth: {ground_truth}")
    print()

    expected: dict[tuple[int, int], list[int]] = {}
    for row in iter_multi_concordant_pairs(ground_truth):
        expected[(row.A, row.B)] = sorted(row.concordant_N)

    print(f"ground-truth pair count: {len(expected)}")

    t0 = time.perf_counter()
    fast = fast_multi_concordant_pairs(max_hyp=max_hyp)
    elapsed = time.perf_counter() - t0

    print(f"fast pair count:         {len(fast)}")
    print(f"fast elapsed:            {elapsed:.2f}s")
    print()

    missing = sorted(set(expected) - set(fast))
    extra = sorted(set(fast) - set(expected))
    mismatched: list[tuple[tuple[int, int], list[int], list[int]]] = []
    for key in sorted(set(expected) & set(fast)):
        if sorted(fast[key]) != expected[key]:
            mismatched.append((key, expected[key], sorted(fast[key])))

    if missing:
        print(f"missing in fast ({len(missing)}):")
        for key in missing[:20]:
            print(f"  expected {key} -> {expected[key]}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")

    if extra:
        print(f"extra in fast ({len(extra)}):")
        for key in extra[:20]:
            print(f"  fast {key} -> {fast[key]}")
        if len(extra) > 20:
            print(f"  ... and {len(extra) - 20} more")

    if mismatched:
        print(f"mismatched concordant_N ({len(mismatched)}):")
        for key, exp, got in mismatched[:20]:
            print(f"  {key}: expected={exp} got={got}")
        if len(mismatched) > 20:
            print(f"  ... and {len(mismatched) - 20} more")

    if not missing and not extra and not mismatched:
        print("OK: fast scanner matches ground truth exactly.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
