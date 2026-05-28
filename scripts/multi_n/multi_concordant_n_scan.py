#!/usr/bin/env python3
"""Multi-concordant-N scanner (wl045).

For all reduced coprime (A, B) with 1 <= A < B <= max_hyp, enumerate the full
concordant-N set via `find_concordant_by_factorization(A, B)`. Output:

1. Total pairs scanned
2. Pairs with >= 2 concordant N (multi-N pairs)
3. Pairs with N1+N2 = A+B (square-closure candidate, would be a counterexample)
4. Maximum N count seen across all pairs
5. JSONL of all multi-N pairs with their full N list

This implements the user-suggested sieve at wl045: "counterexamples must
come from pairs with >= 2 concordant N". By definition every Harborth
4-chain (a, b, c, d) gives the pair (A, B) = (b, d) at least 2 concordant N
(namely N = a and N = c). So multi-N is a necessary condition for a
counterexample.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.factor_search import find_concordant_by_factorization  # noqa: E402
from rational_distance.parallel import add_parallel_args, get_parallel_config_from_args  # noqa: E402


def process_pair(ab: tuple[int, int]) -> tuple[int, int, int, list[int], list[tuple[int, int]]]:
    """Worker: returns (A, B, k, sorted_Ns, closure_pairs)."""
    A, B = ab
    Ns = find_concordant_by_factorization(A, B)
    k = len(Ns)
    closure_pairs: list[tuple[int, int]] = []
    if k >= 2:
        target = A + B
        Ns_set = set(Ns)
        for N1 in Ns:
            N2 = target - N1
            if N2 != N1 and N2 in Ns_set and N2 > 0:
                closure_pairs.append((N1, N2))
    return (A, B, k, sorted(Ns) if k >= 2 else [], closure_pairs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-hyp", type=int, default=2000)
    ap.add_argument("--out", default=None,
                    help="Output JSONL of multi-N pairs (default: "
                         "results/multi_concordant_N_max{max_hyp}.jsonl)")
    ap.add_argument("--progress-every", type=int, default=200000)
    # 使用公共并行工具添加标准参数
    add_parallel_args(ap)
    args = ap.parse_args()
    pcfg = get_parallel_config_from_args(args)

    max_hyp = int(args.max_hyp)
    out_path = Path(args.out) if args.out else \
        ROOT / "results" / f"multi_concordant_N_max{max_hyp}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate reduced pairs
    pairs: list[tuple[int, int]] = []
    for a in range(1, max_hyp + 1):
        for b in range(a + 1, max_hyp + 1):
            if gcd(a, b) == 1:
                pairs.append((a, b))
    total = len(pairs)
    print(f"max_hyp={max_hyp}, reduced (A, B) pairs: {total}")
    print(f"workers: {pcfg.workers}  chunksize: {pcfg.chunksize}")
    print(f"output: {out_path}")
    print()

    t0 = time.perf_counter()
    n_count_hist: Counter[int] = Counter()
    n_multi = 0
    n_closure = 0
    max_n_count = 0
    max_n_count_pair: tuple[int, int] | None = None
    processed = 0

    # 使用公共并行工具
    from rational_distance.parallel import parallel_map

    with open(out_path, "w", encoding="utf-8") as fh:
        def handle_result(result: tuple[int, int, int, list[int], list[tuple[int, int]]]) -> None:
            nonlocal n_multi, n_closure, max_n_count, max_n_count_pair, processed
            A, B, k, Ns, closure_pairs = result
            n_count_hist[k] += 1
            if k > max_n_count:
                max_n_count = k
                max_n_count_pair = (A, B)
            if k >= 2:
                n_multi += 1
                row = {
                    "A": A, "B": B,
                    "n_concordant": k,
                    "concordant_N": Ns,
                    "A_plus_B": A + B,
                    "closure_pairs": closure_pairs,
                }
                fh.write(json.dumps(row) + "\n")
                if closure_pairs:
                    n_closure += 1
                    print(f"*** COUNTEREXAMPLE: A={A}, B={B}, N pairs={closure_pairs} ***",
                          flush=True)
            processed += 1
            if processed % args.progress_every == 0 or processed == total:
                elapsed = time.perf_counter() - t0
                rate = processed / elapsed if elapsed > 0 else 0
                eta = (total - processed) / rate if rate > 0 else float("inf")
                print(f"[{processed:>10}/{total}] {elapsed:>6.1f}s  {rate:>6.0f}/s  "
                      f"ETA {eta:>5.0f}s  multi={n_multi}  closure={n_closure}  "
                      f"max_k={max_n_count}",
                      flush=True)
                fh.flush()

        parallel_map(
            process_pair,
            pairs,
            workers=pcfg.workers,
            chunksize=pcfg.chunksize,
            on_result=handle_result,
        )
    elapsed = time.perf_counter() - t0
    print()
    print("=" * 60)
    print(f"Done. {total} pairs in {elapsed:.1f}s.")
    print(f"  multi-N pairs (>= 2 concordant N): {n_multi}")
    print(f"  pairs with N1+N2 = A+B (counterexample): {n_closure}")
    print(f"  max N count: {max_n_count} at {max_n_count_pair}")
    print(f"  N-count distribution:")
    for k in sorted(n_count_hist):
        print(f"    {k} concordant N: {n_count_hist[k]:>10} pairs")
    print(f"  output: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
