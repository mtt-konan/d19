#!/usr/bin/env python3
"""Tabulate squarefree signatures of half-points for the three k=4 pairs.

Aims at the question raised in wl048: do the four concordant N's of a k=4
pair fall into four distinct 2-descent / homogeneous-space classes, or do
some N's collide?
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


K4_PAIRS: tuple[tuple[int, int], ...] = (
    (11776, 17199),
    (6669, 26656),
    (7337, 28288),
)


def _normalize_sig(sig: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = sorted((abs(sig[0]), abs(sig[1]), abs(sig[2])))
    return (a, b, c)


def main() -> int:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.concordant.half_points import enumerate_half_points_for_concordant_N

    for a, b in K4_PAIRS:
        ns = sorted(find_concordant_by_factorization(a, b))
        print(f"=== ({a}, {b})  A+B = {a + b} ===")
        print(f"concordant N: {ns}")
        for n in ns:
            halves = enumerate_half_points_for_concordant_N(a, b, n)
            sigs = sorted({half.signature for half in halves})
            sig_classes = sorted({_normalize_sig(s) for s in sigs})
            print(
                f"  N={n:>7}: {len(halves)} half-points, "
                + f"{len(sigs)} raw sigs, "
                + f"{len(sig_classes)} class(es) up to sign"
            )
            for s in sigs:
                print(f"      sig {s}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
