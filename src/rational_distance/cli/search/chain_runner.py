"""Chain CLI runner."""

from __future__ import annotations

import argparse
import json
import time


def _run_chain(args: argparse.Namespace) -> None:
    from rational_distance.search_chain import find_chains, results_to_json

    print("=" * 72)
    print("Pythagorean 4-cycle search — rectangle / unit-square problem")
    print(f"  max_val={args.max_val}, require_square={args.require_square}")
    print("=" * 72)

    t0 = time.perf_counter()
    results = find_chains(
        max_val=args.max_val,
        require_square=args.require_square,
        canonical=True,
        progress=not args.no_progress,
    )
    elapsed = time.perf_counter() - t0

    n_sq = sum(1 for result in results if result.square_ok)
    print(f"\nFound {len(results)} canonical 4-cycles in {elapsed:.1f}s")
    print(f"  {n_sq} satisfy unit-square constraint (a+c == b+d)")
    print(f"  {len(results) - n_sq} are rectangle-only solutions")

    top = args.top if args.top > 0 else len(results)
    if results:
        print()
        for result in results[:top]:
            print(str(result))
            print()
        if len(results) > top:
            print(f"  ... {len(results) - top} more rows suppressed (use --top 0 to show all)")

    if args.out:
        data = results_to_json(results, args.max_val, args.require_square, elapsed)
        with open(args.out, "w") as handle:
            json.dump(data, handle, indent=2)
        print(f"\nResults saved to {args.out}")


__all__ = ["_run_chain"]
