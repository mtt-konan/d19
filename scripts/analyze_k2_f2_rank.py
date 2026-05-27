#!/usr/bin/env python3
"""F₂-rank of half-point 2-descent images for k=2 multi-N pairs.

For each k=2 multi-N pair (A, B, N_1, N_2) with safe sieve passed:

  1. Take a positive-signature half-point Q_{N_i} for each N_i
     (via enumerate_half_points_for_concordant_N).
  2. Compute its 2-descent image
       δ(Q_{N_i}) = (sf(x), sf(x + A²)) ∈ (ℚ*/ℚ*²)²
     (third coordinate is determined by first two via the curve equation;
      following the wl048 convention.)
  3. Stack the 2 images as F₂-vectors keyed by primes (with sign tracked).
  4. Compute F₂-rank via Gauss elimination.

Conjecture A1 mechanism prediction:
  rank({δ(Q_{N_1}), δ(Q_{N_2})}) = 2 for all k=2 pairs (or at most a few
  imprecise cases with mod E[2] complications).

Sanity-check: if any pair gives F₂-rank < 2, that's the *first* potential
counterexample to A1's mechanism — closely audit it.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
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
    """Return prime factorization of |n|; sign tracked separately via key (-1, _)."""
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
    """Return {prime: 1} or {-1: 1, prime: 1} representing sf(n) over F₂."""
    out: dict[int, int] = {}
    factors = _factor(n)
    for p, e in factors.items():
        if e % 2 == 1:
            out[p] = 1
    return out


def _signature_to_f2_vector(sig_first: int, sig_second: int) -> F2Vector:
    """Combine (sf_first, sf_second) into one F₂-vector keyed by (prime, slot)."""
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
    """Gauss elimination over F₂ on dict-vectors."""
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


@dataclass
class K2F2Row:
    A: int
    B: int
    N_1: int
    N_2: int
    Q1_x: int
    Q1_sig: tuple[int, int, int]
    Q2_x: int
    Q2_sig: tuple[int, int, int]
    f2_rank_pure: int  # rank({δ(Q_1), δ(Q_2)}) without E[2] images
    # Rank including E[2](ℚ) images via Silverman §X.4 special formulas:
    #   α(T_0 = (0,0))      = (1, 1)            ≡ trivial
    #   α(T_A = (-A², 0))   = (sf(-A²), sf(-A²·D)) = (-1, -D mod sq)
    #   α(T_B = (-B², 0))   = (sf(-B²), sf(A²-B²)) = (-1, -D mod sq)  (same as T_A
    #                          because T_0 = T_A + T_B ∈ 2 E(ℚ) generically for
    #                          E_{A,B} which has Z/4Z torsion)
    # So E[2] image占 dim 1 in (ℚ*/ℚ*²)². 我们 stack {δ(Q_1), δ(Q_2), α(T_A)}
    # 看 F₂-rank：rank ≥ 2 ⟺ F₂-rank{Q_1, Q_2, T_A} = 3.
    f2_rank_with_t2: int


def _pick_positive_halfpoint(A: int, B: int, N: int):
    """Pick the positive-signature representative half-point for concordant N."""
    halves = enumerate_half_points_for_concordant_N(A, B, N)
    positive = [h for h in halves if h.signature[0] > 0]
    if not positive:
        # fallback: take first
        return halves[0]
    return positive[0]


def analyze_k2(A: int, B: int, N_1: int, N_2: int) -> K2F2Row:
    Q1 = _pick_positive_halfpoint(A, B, N_1)
    Q2 = _pick_positive_halfpoint(A, B, N_2)

    v1 = _signature_to_f2_vector(Q1.signature[0], Q1.signature[1])
    v2 = _signature_to_f2_vector(Q2.signature[0], Q2.signature[1])
    rank_pure = _f2_rank([v1, v2])

    # E[2](ℚ) image: α(T_A = (-A², 0)) = (sf(-A²), sf(-A²·D)) = (-1, -D mod sq)
    # We use this single representative (T_B 给出同 image; T_0 trivial 在 image)。
    D = B * B - A * A
    v_T = _signature_to_f2_vector(-1, -D)

    rank_with_t2 = _f2_rank([v1, v2, v_T])

    return K2F2Row(
        A=A,
        B=B,
        N_1=N_1,
        N_2=N_2,
        Q1_x=Q1.x,
        Q1_sig=Q1.signature,
        Q2_x=Q2.x,
        Q2_sig=Q2.signature,
        f2_rank_pure=rank_pure,
        f2_rank_with_t2=rank_with_t2,
    )


def collect_k2_pairs(max_hyp: int) -> list[tuple[int, int, int, int]]:
    pairs = fast_multi_concordant_pairs(max_hyp)
    out: list[tuple[int, int, int, int]] = []
    for (a, b), ns in pairs.items():
        if len(ns) != 2:
            continue
        if not allow_reduced_pair(a, b):
            continue
        out.append((a, b, ns[0], ns[1]))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="F₂-rank of {δ(Q_{N_1}), δ(Q_{N_2})} for k=2 multi-N pairs."
    )
    parser.add_argument("--max-hyp", type=int, default=200000)
    parser.add_argument("--jsonl-out", type=Path, default=None)
    args = parser.parse_args()

    t0 = time.perf_counter()
    pairs = collect_k2_pairs(args.max_hyp)
    print(f"[phase] {len(pairs)} k=2 safe-pass pairs at max_hyp={args.max_hyp}")

    rows: list[K2F2Row] = []
    pure_counter: Counter[int] = Counter()
    with_t2_counter: Counter[int] = Counter()
    suspect_rows: list[K2F2Row] = []

    t1 = time.perf_counter()
    for i, (a, b, n1, n2) in enumerate(pairs, 1):
        try:
            row = analyze_k2(a, b, n1, n2)
        except Exception as exc:
            print(f"  [{i}] ({a},{b}) FAIL: {exc}")
            continue
        rows.append(row)
        pure_counter[row.f2_rank_pure] += 1
        with_t2_counter[row.f2_rank_with_t2] += 1
        # rank ≥ 2 ⟺ F₂-rank{Q_1, Q_2, T_A} = 3
        if row.f2_rank_with_t2 < 3:
            suspect_rows.append(row)
    elapsed = time.perf_counter() - t1

    print("=" * 72)
    print(f"analyzed: {len(rows)} pairs in {elapsed:.2f}s")
    print(f"F₂-rank pure {{Q_1, Q_2}}: {dict(sorted(pure_counter.items()))}")
    print(
        f"F₂-rank with T_A {{Q_1, Q_2, T_A}}: "
        f"{dict(sorted(with_t2_counter.items()))}"
    )
    print(f"f2_rank_with_t2 < 3 (potential A1 mechanism flaw): {len(suspect_rows)}")
    for r in suspect_rows[:10]:
        print(
            f"  ({r.A},{r.B}) N=[{r.N_1},{r.N_2}] "
            f"Q1.sig={r.Q1_sig} Q2.sig={r.Q2_sig} "
            f"pure={r.f2_rank_pure} with_t2={r.f2_rank_with_t2}"
        )

    if args.jsonl_out is not None:
        args.jsonl_out.parent.mkdir(parents=True, exist_ok=True)
        with args.jsonl_out.open("w") as fh:
            for row in rows:
                fh.write(json.dumps(asdict(row)) + "\n")
        print(f"wrote {len(rows)} rows to {args.jsonl_out}")

    print(f"[phase] total elapsed: {time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    main()
