"""Search for points with rational distances to ≥3 (or all 4) vertices of the
unit square A(0,0), B(1,0), C(1,1), D(0,1).

Usage
─────
    uv run python scripts/search_3vertex.py              # sensible defaults
    uv run python scripts/search_3vertex.py --min-rational 4  # hunt for 4-vertex
    uv run python scripts/search_3vertex.py --max-m 100 --max-k-num 1000 \\
        --max-k-den 500 --workers 8 --out results.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.search import brute_force_search, dedup_by_symmetry, merge_results, parametric_search_fast
from rational_distance.square import RationalPoint


# ── Formatting helpers ────────────────────────────────────────────────────────

def _header() -> str:
    return f"{'cnt':>3}  {'den':>7}  {'x':>14}  {'y':>14}  {'d(A)':>10}  {'d(B)':>10}  {'d(C)':>10}  {'d(D)':>10}"


def _row(pt: RationalPoint) -> str:
    def fmt(d):
        return f"{str(d):>10}" if d is not None else f"{'?':>10}"
    dA, dB, dC, dD = pt.distances
    return (
        f"{pt.rational_count:>3}  {pt.denominator:>7}  {str(pt.x):>14}  {str(pt.y):>14}  "
        f"{fmt(dA)}  {fmt(dB)}  {fmt(dC)}  {fmt(dD)}"
    )


def _size_estimate(max_m: int, max_k_num: int, max_k_den: int) -> str:
    """Rough estimate of search space size."""
    from math import gcd
    n_triples = sum(
        1 for m in range(2, max_m + 1) for n in range(1, m)
        if (m - n) % 2 == 1 and gcd(m, n) == 1
    ) * 2  # both orientations
    n_pairs = sum(
        1 for b in range(1, max_k_den + 1)
        for a in range(1, max_k_num + 1)
        if gcd(a, b) == 1
    )
    total = n_triples * n_pairs
    if total >= 1_000_000_000:
        return f"{total/1e9:.1f}B"
    if total >= 1_000_000:
        return f"{total/1e6:.1f}M"
    return f"{total:,}"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--scale",       type=int, default=None,
                        help="Set max_m=N, max_k_den=4N, max_k_num=8N at once")
    parser.add_argument("--max-m",       type=int, default=60,
                        help="Max m for Pythagorean triple generation (default 60)")
    parser.add_argument("--max-k-num",   type=int, default=300,
                        help="Max numerator of scale k (default 300)")
    parser.add_argument("--max-k-den",   type=int, default=150,
                        help="Max denominator of scale k (default 150)")
    parser.add_argument("--min-rational",type=int, default=3, choices=[2,3,4],
                        help="Minimum rational distances to report (default 3)")
    parser.add_argument("--brute-den",   type=int, default=0,
                        help="Also brute-force with this max denominator (0=skip)")
    parser.add_argument("--workers",     type=int, default=0,
                        help="Worker processes (0=auto, 1=single-process)")
    parser.add_argument("--out",         type=str, default=None,
                        help="Write JSON results to this file")
    parser.add_argument("--top",         type=int, default=50,
                        help="Max rows to print (0=all, default 50)")
    parser.add_argument("--no-dedup-symmetry", action="store_true",
                        help="Show all symmetric copies; default deduplicates to one per D4 orbit")
    args = parser.parse_args()

    if args.scale is not None:
        args.max_m     = args.scale
        args.max_k_den = 4 * args.scale
        args.max_k_num = 8 * args.scale

    dedup_sym = not args.no_dedup_symmetry

    print("=" * 72)
    print("Rational distance search — unit square A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den},",
          f"min_rational={args.min_rational}")
    est = _size_estimate(args.max_m, args.max_k_num, args.max_k_den)
    print(f"  search space ≈ {est} (triple × k combinations)")
    if args.brute_den:
        print(f"  + brute-force denominator ≤ {args.brute_den}")
    print("=" * 72)

    t0 = time.perf_counter()

    results = parametric_search_fast(
        max_m=args.max_m,
        max_k_num=args.max_k_num,
        max_k_den=args.max_k_den,
        min_rational=args.min_rational,
        workers=args.workers,
        progress=True,
    )

    if args.brute_den:
        bf = list(brute_force_search(max_den=args.brute_den, min_rational=args.min_rational))
        results = list(merge_results(iter(results), iter(bf)))

    raw_count = len(results)
    if dedup_sym:
        results = dedup_by_symmetry(results)

    elapsed = time.perf_counter() - t0

    # ── Summary ───────────────────────────────────────────────────────────
    count_by_n: dict[int, int] = {}
    for pt in results:
        count_by_n[pt.rational_count] = count_by_n.get(pt.rational_count, 0) + 1

    print(f"\n{'─'*72}")
    if dedup_sym:
        print(f"Found {raw_count} points → {len(results)} orbits after D4 dedup  ({elapsed:.2f}s)")
    else:
        print(f"Found {len(results)} unique points in {elapsed:.2f}s")
    print(f"Sorted by: rational_count DESC, denominator ASC")
    for n in sorted(count_by_n, reverse=True):
        marker = " ◄ 4-VERTEX SOLUTION!" if n == 4 else ""
        print(f"  {count_by_n[n]:6d}  points with {n}/4 rational distances{marker}")
    print(f"{'─'*72}\n")

    # ── Table ─────────────────────────────────────────────────────────────
    display = results if args.top == 0 else results[: args.top]
    print(_header())
    print("─" * 85)
    for pt in display:
        print(_row(pt))
    if args.top and len(results) > args.top:
        print(f"  … {len(results) - args.top} more rows omitted (use --top 0 to see all)")

    # ── Highlight any 4-vertex solutions ──────────────────────────────────
    four = [pt for pt in results if pt.rational_count == 4]
    if four:
        print(f"\n{'!'*72}")
        print(f"  {len(four)} POINT(S) WITH ALL FOUR RATIONAL DISTANCES:")
        for pt in four:
            print(f"  {pt}")
        print(f"{'!'*72}")
    else:
        if args.min_rational <= 3:
            print("\n(No 4-vertex solutions found in this search range.)")

    # ── JSON output ───────────────────────────────────────────────────────
    if args.out:
        out_path = Path(args.out)
        payload = {
            "search_params": vars(args),
            "elapsed_seconds": round(elapsed, 3),
            "total_found": len(results),
            "count_by_rational": {str(k): v for k, v in count_by_n.items()},
            "points": [pt.as_dict() for pt in results],
        }
        out_path.write_text(json.dumps(payload, indent=2))
        print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
