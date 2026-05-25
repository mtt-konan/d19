#!/usr/bin/env python3
"""Compute PARI ellrank for the three k=4 pairs found by the fast scanner.

For each pair (A, B):
  - call `rational_distance.concordant.analysis.compute_rank`
  - print rank lower / upper bounds, Sha[2] lower bound, generators
  - compare against the F2-rank found in `scripts/k4_two_descent_rank.py`

Side-effect: confirms (or refutes) whether the F2-rank on the 4 half-points
matches the actual Mordell-Weil rank.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


K4_PAIRS: tuple[tuple[int, int, int], ...] = (
    # (A, B, F2-rank from k4_two_descent_rank.py)
    (11776, 17199, 3),
    (6669, 26656, 3),
    (7337, 28288, 4),
)


def main() -> int:
    from rational_distance.concordant.analysis import compute_rank

    for a, b, f2_rank in K4_PAIRS:
        print(f"=== ({a}, {b})  F2-rank on 4 half-points = {f2_rank} ===")
        t0 = time.perf_counter()
        try:
            _, (lower, upper), sha2_lower, gens = compute_rank(a, b, effort=1)
        except Exception as exc:
            print(f"  PARI ellrank failed: {exc}")
            print()
            continue
        elapsed = time.perf_counter() - t0
        print(f"  rank lower / upper:   {lower} / {upper}")
        print(f"  sha2_lower:           {sha2_lower}")
        print(f"  generators:           {len(gens)} returned")
        for idx, gen in enumerate(gens[:6]):
            print(f"    gen[{idx}] = {gen}")
        print(f"  elapsed:              {elapsed:.2f}s")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
