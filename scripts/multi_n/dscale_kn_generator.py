#!/usr/bin/env python3
"""D-scaling K_n fast generator CLI (wl085, OPEN_DIRECTIONS A.7).

Usage:
    uv run python scripts/multi_n/dscale_kn_generator.py [options]

Algorithm (see src/rational_distance/concordant/dscale_kn.py for full theory):

  1. Read primitive (a₀, b₀) pairs from a multi-N catalog (default
     results/multi_n/multi_concordant_N_max10000.jsonl).
  2. For each primitive, PARI ellrank + ellratpoints to enumerate the
     rational n pool.
  3. For each pool, scan d ∈ [d_min, d_max] and collect K_t hub candidates
     where t ≥ target_k.
  4. Output JSONL with one line per K_t candidate.

Each output line:
  {
    "a": int, "b": int, "d": int,
    "primitive_a": int, "primitive_b": int,
    "k": int, "concordant_N": [N_1, ..., N_k],
    "rank_lower": int, "rank_upper": int
  }

This is **much faster** than scanning (a, b) ≤ max_hyp because primitives are
few (a few hundred for max_hyp=10000) and the d enumeration is linear.

Example (find K_9+ candidates from 4 wl065 primitives):

    uv run python scripts/multi_n/dscale_kn_generator.py \\
        --primitives 25,91 70,117 91,990 221,704 \\
        --target-k 9 --d-max 10000 \\
        --out results/multi_n/dscale_kn_smoke.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.dscale_kn import (  # noqa: E402
    enumerate_rational_n,
    scan_d_for_target_k,
)


def _load_primitives_from_catalog(
    catalog_path: Path,
    *,
    max_primitive: int | None = None,
) -> list[tuple[int, int]]:
    """Load (A, B) pairs from a multi-N JSONL catalog as primitive candidates.

    Filters: only pairs with gcd(A, B) = 1 (primitive itself) and k ≥ 1.
    """
    primitives: list[tuple[int, int]] = []
    from math import gcd

    with open(catalog_path) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            a = row.get("A") or row.get("a")
            b = row.get("B") or row.get("b")
            if a is None or b is None:
                continue
            a, b = int(a), int(b)
            if a <= 0 or b <= 0 or a == b:
                continue
            if gcd(a, b) != 1:
                continue
            if max_primitive is not None and max(a, b) > max_primitive:
                continue
            primitives.append((a, b))
    return primitives


def _parse_primitives_arg(values: list[str]) -> list[tuple[int, int]]:
    out = []
    for v in values:
        parts = v.split(",")
        if len(parts) != 2:
            raise ValueError(f"primitive must be 'a,b', got {v!r}")
        out.append((int(parts[0]), int(parts[1])))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=ROOT / "results/multi_n/multi_concordant_N_max10000.jsonl",
        help="multi-N JSONL catalog to seed primitives (default: max10000)",
    )
    parser.add_argument(
        "--primitives",
        nargs="+",
        default=None,
        help="Explicit list of primitives 'a,b' (overrides --catalog)",
    )
    parser.add_argument(
        "--max-primitive",
        type=int,
        default=1000,
        help="Skip primitives with max(a, b) > this (default: 1000)",
    )
    parser.add_argument(
        "--target-k", type=int, default=4,
        help="Minimum k value to emit candidates (default: 4)",
    )
    parser.add_argument(
        "--d-min", type=int, default=1, help="Minimum d (default: 1)",
    )
    parser.add_argument(
        "--d-max", type=int, default=10_000,
        help="Maximum d to scan (default: 10000)",
    )
    parser.add_argument(
        "--max-depth", type=int, default=50,
        help="Per-generator multiple depth for ellrank enumeration (default: 50)",
    )
    parser.add_argument(
        "--ratpoints-bound", type=int, default=200_000,
        help="ellratpoints naive height bound (default: 200000; 0 disables)",
    )
    parser.add_argument(
        "--rank-combo-bound", type=int, default=5,
        help="Linear-combination box size for rank ≥ 2 (default: 5)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="JSONL output path (default: print to stdout)",
    )
    parser.add_argument(
        "--summary-only", action="store_true",
        help="Don't dump all candidates; only print per-primitive summary",
    )

    args = parser.parse_args()
    os.environ.setdefault("PARI_MT_ENGINE", "single")

    # Determine primitive set
    if args.primitives:
        primitives = _parse_primitives_arg(args.primitives)
        print(f"[seed] {len(primitives)} primitives from --primitives arg")
    else:
        if not args.catalog.exists():
            print(f"[err] catalog not found: {args.catalog}", file=sys.stderr)
            sys.exit(1)
        primitives = _load_primitives_from_catalog(
            args.catalog, max_primitive=args.max_primitive
        )
        print(
            f"[seed] {len(primitives)} primitives from {args.catalog.name} "
            f"(max(a,b) <= {args.max_primitive})"
        )

    # Run
    out_lines: list[str] = []
    total_candidates = 0
    t_start = time.time()
    from rational_distance.concordant.analysis import _ensure_pari
    pari = _ensure_pari()

    for idx, (a0, b0) in enumerate(primitives):
        t0 = time.time()
        try:
            pool = enumerate_rational_n(
                a0, b0,
                max_depth=args.max_depth,
                ratpoints_bound=args.ratpoints_bound,
                rank_combo_bound=args.rank_combo_bound,
                pari=pari,
            )
        except Exception as exc:
            print(
                f"  [{idx+1}/{len(primitives)}] ({a0}, {b0}): "
                f"PARI failure {exc!r}",
                file=sys.stderr,
            )
            continue
        elapsed_pool = time.time() - t0
        if pool.n_count == 0:
            print(
                f"  [{idx+1}/{len(primitives)}] ({a0}, {b0}): "
                f"rank=[{pool.rank_lower},{pool.rank_upper}], 0 rational n, skip"
            )
            continue

        candidates = scan_d_for_target_k(
            pool,
            target_k=args.target_k,
            d_max=args.d_max,
            d_min=args.d_min,
        )
        total_candidates += len(candidates)

        # show per-primitive max k achievable
        if candidates:
            max_k = max(c.k for c in candidates)
        else:
            max_k = 0
        print(
            f"  [{idx+1}/{len(primitives)}] ({a0}, {b0}): "
            f"rank=[{pool.rank_lower},{pool.rank_upper}], "
            f"{pool.n_count} rational n, "
            f"{len(candidates)} candidates (k≥{args.target_k}, max k={max_k}), "
            f"pool {elapsed_pool:.1f}s"
        )

        if not args.summary_only:
            for c in candidates:
                out_lines.append(json.dumps(c.to_dict()))

    elapsed_total = time.time() - t_start

    # Output
    if not args.summary_only:
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with open(args.out, "w") as f:
                for line in out_lines:
                    f.write(line + "\n")
            print(f"\n[out] {len(out_lines)} lines → {args.out}")
        else:
            for line in out_lines:
                print(line)

    print(
        f"\n[done] {total_candidates} K_{args.target_k}+ candidates from "
        f"{len(primitives)} primitives in {elapsed_total:.1f}s"
    )


if __name__ == "__main__":
    main()
