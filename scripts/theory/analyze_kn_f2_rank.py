#!/usr/bin/env python3
"""通用 F₂-rank of half-point 2-descent images for k=n multi-N pairs.

For each multi-N pair (A, B) with concordant_N(A, B) = {N_1, ..., N_k}:
  1. Take positive-sig half-point Q_{N_i} for each N_i.
  2. Compute δ(Q_{N_i}) = (sf(x), sf(x + A²)) ∈ (ℚ*/ℚ*²)².
  3. Stack k images + α(T_A) as F₂-vectors; compute F₂-rank.

Conjecture A_n (k=n ⟹ rank ≥ n): if F₂-rank{Q_1,...,Q_k, T_A} = k+1 universal,
that's strong evidence (mechanism upgrade for n ≥ 3).

期望 (based on dim image α = rank + 1):
  F₂-rank{Q_1,...,Q_k, T_A} = k+1  ⟺  rank ≥ k.

usage:
  uv run python scripts/analyze_kn_f2_rank.py --max-hyp 1000000 --target-k 4
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.half_points import (
    enumerate_half_points_for_concordant_N,
    squarefree_part,
)
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


F2Vector = dict[tuple[int, int], int]


def _factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    if n == 0:
        return out
    if n < 0:
        out[-1] = 1
        n = -n
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def _sf_to_f2(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for p, e in _factor(n).items():
        if e % 2 == 1:
            out[p] = 1
    return out


def _signature_to_f2_vector(sig_first: int, sig_second: int) -> F2Vector:
    vec: F2Vector = {}
    for p, e in _sf_to_f2(sig_first).items():
        vec[(p, 0)] = e
    for p, e in _sf_to_f2(sig_second).items():
        vec[(p, 1)] = e
    return vec


def _f2_xor(a: F2Vector, b: F2Vector) -> F2Vector:
    out: F2Vector = dict(a)
    for k, v in b.items():
        out[k] = (out.get(k, 0) + v) % 2
    return {k: v for k, v in out.items() if v == 1}


def _f2_rank(vectors: list[F2Vector]) -> int:
    pivots: dict[tuple[int, int], F2Vector] = {}
    for vec in vectors:
        v: F2Vector = dict(vec)
        while v:
            pivot = max(v.keys())
            if pivot in pivots:
                v = _f2_xor(v, pivots[pivot])
            else:
                pivots[pivot] = v
                break
    return len(pivots)


def _pick_positive_halfpoint(A: int, B: int, N: int):
    halves = enumerate_half_points_for_concordant_N(A, B, N)
    positive = [h for h in halves if h.signature[0] > 0]
    if not positive:
        return halves[0]
    return positive[0]


def analyze_kn(A: int, B: int, ns: list[int]) -> dict:
    """For a pair (A, B) with k=len(ns) concordant N values, compute F₂-ranks."""
    qs = [_pick_positive_halfpoint(A, B, n) for n in ns]
    sigs = [q.signature for q in qs]
    vectors = [_signature_to_f2_vector(s[0], s[1]) for s in sigs]

    rank_pure = _f2_rank(vectors)

    D = B * B - A * A
    v_T = _signature_to_f2_vector(-1, -D)
    rank_with_t2 = _f2_rank([*vectors, v_T])

    return {
        "A": A,
        "B": B,
        "k": len(ns),
        "ns": ns,
        "f2_rank_pure": rank_pure,
        "f2_rank_with_T_A": rank_with_t2,
        "qs_x": [q.x for q in qs],
        "qs_sig": [list(s) for s in sigs],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-hyp", type=int, default=1_000_000)
    parser.add_argument("--target-k", type=int, default=None,
                        help="Only analyze pairs with this k (default: all k≥3)")
    parser.add_argument("--min-k", type=int, default=3)
    parser.add_argument("--jsonl-out", default=None)
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--no-safe-pass", action="store_true",
                        help="Skip safe sieve filter (include unsafe pairs).")
    args = parser.parse_args()

    print(f"[phase] enumerating multi-N pairs at max_hyp={args.max_hyp}")
    t0 = time.time()
    pairs_data = fast_multi_concordant_pairs(args.max_hyp)
    print(f"[done] {len(pairs_data)} multi-N pairs in {time.time()-t0:.1f}s")

    # filter
    if args.target_k is not None:
        filtered = [(A, B, ns) for (A, B), ns in pairs_data.items() if len(ns) == args.target_k]
        print(f"[filter] target_k={args.target_k}: {len(filtered)} pairs")
    else:
        filtered = [(A, B, ns) for (A, B), ns in pairs_data.items() if len(ns) >= args.min_k]
        print(f"[filter] min_k={args.min_k}: {len(filtered)} pairs")

    # safe-pass filter (off by default; use --no-safe-pass to disable)
    if args.no_safe_pass:
        safe = filtered
        print(f"[no-safe-pass] using all {len(safe)} filtered pairs")
    else:
        safe = [(A, B, ns) for (A, B, ns) in filtered if allow_reduced_pair(A, B)]
        print(f"[safe-pass] {len(safe)}/{len(filtered)} pass safe sieve")

    if args.limit:
        safe = safe[: args.limit]

    out_rows = []
    rank_dist: Counter[tuple[int, int]] = Counter()  # (k, f2_rank_with_T_A)
    rank_pure_dist: Counter[tuple[int, int]] = Counter()
    t0 = time.time()
    for i, (A, B, ns) in enumerate(safe):
        row = analyze_kn(A, B, sorted(ns))
        out_rows.append(row)
        rank_dist[(row["k"], row["f2_rank_with_T_A"])] += 1
        rank_pure_dist[(row["k"], row["f2_rank_pure"])] += 1
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(safe)}  elapsed {time.time()-t0:.1f}s")

    print(f"\n=== F₂-rank distribution by k ===")
    print(f"{'k':>3} {'rank_pure':>10} {'rank_with_T_A':>14} {'count':>6}")
    all_keys = sorted(set(rank_dist.keys()) | set(rank_pure_dist.keys()))
    for (k, _) in sorted(rank_dist.keys()):
        cnt_with = rank_dist[(k, _)]
        print(f"{k:>3} {'-':>10} {_:>14} {cnt_with:>6}")
    print()

    print("=== Conjecture A_n check (rank_with_T_A == k + 1) ===")
    for k in sorted({k for k, _ in rank_dist.keys()}):
        total_k = sum(c for (kk, _), c in rank_dist.items() if kk == k)
        good = rank_dist.get((k, k + 1), 0)
        print(f"  k={k}: {good}/{total_k} satisfy F₂-rank{{Qs,T_A}} = k+1 ({'★' if good == total_k else 'PARTIAL'})")

    if args.jsonl_out:
        out_path = PROJECT_ROOT / args.jsonl_out
        with open(out_path, "w") as f:
            for row in out_rows:
                f.write(json.dumps(row) + "\n")
        print(f"\n[dump] {len(out_rows)} rows → {out_path}")


if __name__ == "__main__":
    main()
