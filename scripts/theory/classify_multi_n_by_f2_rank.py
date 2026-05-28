#!/usr/bin/env python3
"""F₂-rank classifier over a multi-concordant-N catalog.

For every pair `(A, B)` with its concordant N list, compute the F₂-rank of
the half-point images and emit a new JSONL with the rank field attached.

Usage::

    uv run python scripts/classify_multi_n_by_f2_rank.py \
        --in results/multi_concordant_N_max50000_fast.jsonl \
        --out results/multi_concordant_N_max50000_classified.jsonl

Prints a histogram of `(k, F₂-rank)` and the top high-rank candidates.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        required=True,
        help="Multi-N catalog JSONL produced by the fast scanner",
    )
    p.add_argument(
        "--out",
        dest="out_path",
        type=Path,
        required=True,
        help="Destination JSONL path (will be overwritten)",
    )
    p.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top high-F₂-rank candidates to print",
    )
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.two_descent_rank import (
        f2_rank_of_concordant_pair,
    )

    args = parse_args()
    if not args.in_path.exists():
        print(f"Input not found: {args.in_path}", file=sys.stderr)
        return 2

    args.out_path.parent.mkdir(parents=True, exist_ok=True)

    pair_count = 0
    histogram: Counter[tuple[int, int]] = Counter()
    f2_rank_count: Counter[int] = Counter()
    candidates: list[dict[str, object]] = []
    started = time.perf_counter()

    with (
        args.in_path.open("r", encoding="utf-8") as fin,
        args.out_path.open("w", encoding="utf-8") as fout,
    ):
        for raw_line in fin:
            line = raw_line.strip()
            if not line:
                continue
            entry = json.loads(line)
            a = int(entry["A"])
            b = int(entry["B"])
            ns = [int(n) for n in entry["concordant_N"]]
            k = len(ns)
            result = f2_rank_of_concordant_pair(a, b, ns)
            histogram[(k, result.f2_rank)] += 1
            f2_rank_count[result.f2_rank] += 1
            pair_count += 1

            out_entry = {
                **entry,
                "f2_rank": result.f2_rank,
                "minimal_relation": (
                    list(result.minimal_relation)
                    if result.minimal_relation is not None
                    else None
                ),
            }
            fout.write(json.dumps(out_entry) + "\n")

            candidates.append(
                {
                    "A": a,
                    "B": b,
                    "k": k,
                    "f2_rank": result.f2_rank,
                    "concordant_N": ns,
                }
            )

    elapsed = time.perf_counter() - started
    print(f"processed: {pair_count} pairs in {elapsed:.1f}s")
    print(f"output:    {args.out_path}")
    print()
    print("F₂-rank distribution:")
    for rank in sorted(f2_rank_count):
        share = 100.0 * f2_rank_count[rank] / pair_count
        print(f"  F₂-rank = {rank}: {f2_rank_count[rank]:>5}  ({share:5.1f}%)")
    print()
    print("Joint distribution (k, F₂-rank):")
    for k_val, rank in sorted(histogram):
        marker = " ←" if rank == k_val and k_val >= 3 else ""
        print(f"  k={k_val} F₂-rank={rank}: {histogram[(k_val, rank)]:>5}{marker}")
    print()

    candidates.sort(key=lambda c: (-int(c["f2_rank"]), -int(c["k"]), int(c["A"])))
    top = [c for c in candidates if int(c["f2_rank"]) >= 3][: args.top]
    if top:
        print(f"Top {len(top)} high-rank candidates (F₂-rank ≥ 3):")
        for c in top:
            saturated = "*" if c["f2_rank"] == c["k"] else " "
            print(
                f"  {saturated} A={c['A']:>6} B={c['B']:>6}  "
                f"k={c['k']}  F₂-rank={c['f2_rank']}  N={c['concordant_N']}"
            )
        print("  '*' marks pairs where F₂-rank == k (no torsion fold).")
    else:
        print("No pairs with F₂-rank ≥ 3 in input.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
