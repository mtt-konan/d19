#!/usr/bin/env python3
"""Analyze concordant N half-points and squarefree signatures for a pair."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze half-points for all concordant N of a pair"
    )
    _ = parser.add_argument("A", type=int)
    _ = parser.add_argument("B", type=int)
    return parser.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.concordant.half_points import enumerate_half_points_for_concordant_N

    args = parse_args()
    A = cast(int, args.A)
    B = cast(int, args.B)
    concordant = sorted(find_concordant_by_factorization(A, B))
    payload: dict[str, object] = {"A": A, "B": B, "concordant_N": concordant, "half_points": {}}
    half_points: dict[str, object] = {}
    for N in concordant:
        half_points[str(N)] = [
            {"x": point.x, "y": point.y, "signature": list(point.signature)}
            for point in enumerate_half_points_for_concordant_N(A, B, N)
        ]
    payload["half_points"] = half_points
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
