#!/usr/bin/env python3
"""CLI entry point for elliptic-curve guided rational-distance search.

This uses the algebraically-exact chord-tangent method on the quartic
elliptic curve associated with each Pythagorean triple to expand rational
orbits beyond the brute-force search range.

Example usage
-------------
    uv run python scripts/search_ec.py --max-m 30 --max-k-num 400 --max-k-den 800
    uv run python scripts/search_ec.py --max-m 50 --min-rational 4
    uv run python scripts/search_ec.py --inside --output ec_results.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.search_ec import ec_search


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Elliptic-curve guided search for rational-distance points "
            "on the unit square."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--max-m", type=int, default=30,
        help="Upper bound on the Pythagorean-triple generator m (default: 30).",
    )
    parser.add_argument(
        "--max-k-num", type=int, default=400,
        help="Max numerator for seed search k=a/b (default: 400).",
    )
    parser.add_argument(
        "--max-k-den", type=int, default=800,
        help="Max denominator for seed search k=a/b (default: 800).",
    )
    parser.add_argument(
        "--max-steps", type=int, default=20,
        help="Max chord-tangent steps per orbit (default: 20).",
    )
    parser.add_argument(
        "--min-rational", type=int, default=3, choices=[3, 4],
        help="Minimum rational distances required (3 or 4, default: 3).",
    )
    parser.add_argument(
        "--inside", action="store_true",
        help="Restrict to points strictly inside the unit square.",
    )
    parser.add_argument(
        "--output", default="ec_results.json",
        help="Output JSON file path (default: ec_results.json).",
    )
    parser.add_argument(
        "--top", type=int, default=0,
        help="Print only the top N results by denominator (0 = all).",
    )
    parser.add_argument(
        "--no-progress", action="store_true",
        help="Suppress the progress bar.",
    )
    args = parser.parse_args()

    header = "=" * 72
    print(header)
    print("EC rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  max_m={args.max_m}, max_k_num={args.max_k_num}, "
          f"max_k_den={args.max_k_den}")
    print(f"  max_steps={args.max_steps}, min_rational={args.min_rational}, "
          f"inside={args.inside}")
    print(header)

    t0 = time.perf_counter()
    results = ec_search(
        max_m=args.max_m,
        max_k_num=args.max_k_num,
        max_k_den=args.max_k_den,
        max_steps=args.max_steps,
        min_rational=args.min_rational,
        inside_only=args.inside,
        progress=not args.no_progress,
    )
    elapsed = time.perf_counter() - t0

    count_by_rational: dict[int, int] = {}
    for pt in results:
        n = pt.rational_count
        count_by_rational[n] = count_by_rational.get(n, 0) + 1

    print(f"\nFound {len(results)} unique points in {elapsed:.1f}s")
    for n in sorted(count_by_rational):
        print(f"  {n}/4 rational distances: {count_by_rational[n]}")

    display = results[:args.top] if args.top > 0 else results
    if display:
        print("\nTop results by denominator:")
        for pt in display:
            print(" ", pt)

    out = {
        "search_params": {
            "max_m": args.max_m,
            "max_k_num": args.max_k_num,
            "max_k_den": args.max_k_den,
            "max_steps": args.max_steps,
            "min_rational": args.min_rational,
            "inside": args.inside,
        },
        "elapsed_seconds": round(elapsed, 3),
        "total_found": len(results),
        "count_by_rational": {str(k): v for k, v in count_by_rational.items()},
        "points": [pt.as_dict() for pt in results],
    }
    Path(args.output).write_text(json.dumps(out, indent=2))
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
