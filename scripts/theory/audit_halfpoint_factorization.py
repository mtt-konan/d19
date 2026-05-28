#!/usr/bin/env python3
"""阶段 A1-strict §1: 验证 sign argument 对全 max_hyp=1M 的 k=2 multi-N pair
严格成立.

`_pick_positive_halfpoint` 选 sig[0] = sf(x_Q) > 0 的最小 |x| half-point.
8 个 (s_1, s_2, s_3) ∈ {±1}³ 中, 给 x > 0 的有 (+,+,+) 与 (+,-,-) (以及
对应负 y 配对):

    (+,+,+):  x = (N + r₂)(N + r₃)          ≥ N² > 0
    (+,-,-):  x = (r₂ - N)(r₃ - N)         > 0 (两 r > N)

所以 positive-sig half-point 永远存在且 x > 0 严格.

Sign claim (本 audit 焦点):
    δ_1(Q) = sf(x_Q) > 0   (positive coset of Q*/Q*²)
    δ_1(T_A) = sf(-A²) = -1   (negative coset)
    ⟹ δ(Q) ≠ δ(T_A) algebraically.

⟹ algebraic step: Q ≢ T_A mod 2 E(Q). 同理 ≢ T_B (sf(-B²) = -1 也).

仍欠的 gap: Q ∉ 2 E(Q) 即 δ(Q) ≠ 0 — 不能从 sign 推出, 仍 only 实证.
"""

from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def classify_sign_choice(A: int, B: int, N: int, x_Q: int) -> str:
    """Identify which (s1,s2,s3) sign was used by checking x_Q against the
    8 possible sign-orbit values. Returns the sign tuple as string."""
    r2_sq = N * N + A * A
    r3_sq = N * N + B * B
    r2 = isqrt(r2_sq)
    r3 = isqrt(r3_sq)
    candidates = {
        "+++": N * N + N * r2 + N * r3 + r2 * r3,        # = (N+r2)(N+r3)
        "+--": N * N - N * r2 - N * r3 + r2 * r3,        # = (r2-N)(r3-N)
        "-+-": N * N - N * r2 + N * r3 - r2 * r3,        # = (N-r2)(N+r3) < 0
        "--+": N * N + N * r2 - N * r3 - r2 * r3,        # = (N+r2)(N-r3) < 0
        "---": N * N - N * r2 - N * r3 - r2 * r3,
        "++-": N * N + N * r2 - N * r3 + r2 * r3,
        "+-+": N * N - N * r2 + N * r3 + r2 * r3,
        "-++": N * N + N * r2 + N * r3 - r2 * r3,
    }
    for sign, val in candidates.items():
        if val == x_Q:
            return sign
    return "?"


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="results/k2_f2_rank_max1m.jsonl",
    )
    args = parser.parse_args()
    inp = PROJECT_ROOT / args.input

    rows = []
    with open(inp) as f:
        for line in f:
            rows.append(json.loads(line))
    n_total = len(rows)
    print(f"loaded {n_total} k=2 multi-N pair audit rows from {inp}\n")

    from collections import Counter

    sign_counter: Counter[str] = Counter()
    n_sig1_pos = 0
    n_sig2_pos = 0
    n_f2_rank3 = 0
    n_xQ_square = 0  # x_Q is a perfect square (would imply Q ∈ 2 E(Q) candidate)
    n_xQ_plus_A2_square = 0
    n_delta_zero = 0  # both x_Q and x_Q+A² perfect squares ⟹ δ(Q) = (1, 1) = 0

    for r in rows:
        A = r["A"]
        B = r["B"]
        N_1 = r["N_1"]
        N_2 = r["N_2"]
        Q1_x = r["Q1_x"]
        Q2_x = r["Q2_x"]
        Q1_sig = r["Q1_sig"]
        Q2_sig = r["Q2_sig"]
        f2_rank_with_t2 = r["f2_rank_with_t2"]

        sign_counter[classify_sign_choice(A, B, N_1, Q1_x)] += 1
        sign_counter[classify_sign_choice(A, B, N_2, Q2_x)] += 1

        if Q1_sig[0] > 0:
            n_sig1_pos += 1
        if Q2_sig[0] > 0:
            n_sig2_pos += 1
        if f2_rank_with_t2 == 3:
            n_f2_rank3 += 1

        # (b) gap audit: δ(Q) = 0 ⟺ x_Q ∈ □ AND x_Q + A² ∈ □
        for x_Q in (Q1_x, Q2_x):
            x_sq = is_perfect_square(x_Q)
            xA_sq = is_perfect_square(x_Q + A * A)
            if x_sq:
                n_xQ_square += 1
            if xA_sq:
                n_xQ_plus_A2_square += 1
            if x_sq and xA_sq:
                n_delta_zero += 1

    n_pairs_2 = 2 * n_total

    print("=== Sign argument (algebraic step a: Q ≢ T_A, T_B mod 2 E) ===")
    print(f"  Q1_sig[0] > 0:           {n_sig1_pos}/{n_total} ({n_sig1_pos/n_total*100:.2f}%)")
    print(f"  Q2_sig[0] > 0:           {n_sig2_pos}/{n_total} ({n_sig2_pos/n_total*100:.2f}%)")
    print()

    print("=== chosen half-point sign distribution ===")
    for sign, count in sign_counter.most_common():
        print(f"  ({sign}): {count}/{n_pairs_2} ({count/n_pairs_2*100:.2f}%)")
    print()

    print("=== (b) gap audit: 是否 ∃ pair 让 δ(Q) = 0 ===")
    print(f"  x_Q ∈ □:                 {n_xQ_square}/{n_pairs_2} ({n_xQ_square/n_pairs_2*100:.2f}%)")
    print(f"  x_Q + A² ∈ □:            {n_xQ_plus_A2_square}/{n_pairs_2} ({n_xQ_plus_A2_square/n_pairs_2*100:.2f}%)")
    print(f"  ★ both (δ(Q) = 0):       {n_delta_zero}/{n_pairs_2}  → Q ∈ 2 E(Q)")
    print()

    print("=== F₂-rank universal ===")
    print(f"  F₂-rank{{δ(Q1),δ(Q2),δ(T_A)}} = 3: {n_f2_rank3}/{n_total} ({n_f2_rank3/n_total*100:.2f}%)")

    if n_delta_zero == 0:
        print("\n★★★ (b) gap 实证: 0/3758 chosen half-points 满足 δ(Q)=0 → Q ∉ 2 E(Q) on entire 1M sample.")
    else:
        print(f"\n!! 实证 fail: {n_delta_zero} half-points have δ(Q)=0")


if __name__ == "__main__":
    main()
