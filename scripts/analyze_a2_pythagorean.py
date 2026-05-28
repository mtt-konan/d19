#!/usr/bin/env python3
"""阶段 A2: Conjecture A2 的 Pythagorean parameterization 实证分析.

Setup. 对 concordant (A, B, N):  r₂² = N²+A², r₃² = N²+B².

由 (r₂+N)(r₂-N) = A² 知 sf(r₂+N) = sf(r₂-N) := d_2 (因两 squarefree 部分
的乘积是 A² 的平方部分, 必须相等).

⟹ Pythagorean parametrization:
    r₂ + N = s² d_2,   r₂ - N = u² d_2,   A = s u d_2,  2N = (s²-u²) d_2
同理:
    r₃ + N = p² d_3,   r₃ - N = q² d_3,   B = p q d_3,  2N = (p²-q²) d_3

⟹ 在 ℚ*/ℚ*² 中:
    (r₂ + r₃)(r₂ + N) ≡ d_2 · sf(r₂ + r₃)

Conjecture A2 ⟺ d_2 · sf(r₂ + r₃) ≢ 1 mod sq
              ⟺ sf(r₂ + r₃) ≢ d_2 mod sq

本脚本 audit 全 max_hyp=1M:
    - (d_2, d_3) 分布, gcd(d_2, d_3) 与 gcd(A, B)
    - sf(r₂ + r₃) vs d_2 (是否 ≢)
    - 在 d_2 = d_3 case 上特殊讨论
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def squarefree(n: int) -> int:
    if n == 0:
        return 0
    sign = -1 if n < 0 else 1
    n = abs(n)
    out = 1
    p = 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e & 1:
            out *= p
        p += 1 if p == 2 else 2
    if n > 1:
        out *= n
    return sign * out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/k2_f2_rank_max1m.jsonl")
    args = parser.parse_args()

    inp = PROJECT_ROOT / args.input
    rows = [json.loads(line) for line in open(inp)]
    print(f"loaded {len(rows)} k=2 multi-N pair rows from {inp}\n")

    d2_d3_eq = 0
    d2_eq_1 = 0
    d3_eq_1 = 0
    a2_violations = 0  # cases where sf(r2+r3) == d_2 mod sq (would break A2)
    d_dist: Counter[tuple[int, int]] = Counter()

    for r in rows:
        A = r["A"]
        B = r["B"]
        for N in (r["N_1"], r["N_2"]):
            r2 = isqrt(N * N + A * A)
            r3 = isqrt(N * N + B * B)
            d_2 = squarefree(r2 + N)  # = squarefree(r2 - N) by Pythagoras
            d_3 = squarefree(r3 + N)
            sf_sum = squarefree(r2 + r3)

            d_dist[(d_2, d_3)] += 1
            if d_2 == d_3:
                d2_d3_eq += 1
            if d_2 == 1:
                d2_eq_1 += 1
            if d_3 == 1:
                d3_eq_1 += 1
            # A2: sf((r2+r3)(r2+N)) ≠ 1  ⟺  d_2 · sf_sum ∉ □  ⟺  sf_sum ≠ d_2 mod sq
            if squarefree(d_2 * sf_sum) == 1:
                a2_violations += 1

    total = 2 * len(rows)
    print(f"=== Pythagorean parameter distribution (3758 chosen N) ===")
    print(f"  d_2 = d_3 cases:           {d2_d3_eq}/{total} ({d2_d3_eq/total*100:.2f}%)")
    print(f"  d_2 = 1:                   {d2_eq_1}/{total} ({d2_eq_1/total*100:.2f}%)")
    print(f"  d_3 = 1:                   {d3_eq_1}/{total} ({d3_eq_1/total*100:.2f}%)")
    print()

    print(f"=== Conjecture A2 audit ===")
    print(f"  A2 violations (sf(r2+r3) ≡ d_2): {a2_violations}/{total}")
    if a2_violations == 0:
        print(f"  ★ A2 holds universal on max_hyp=1M")
    print()

    print(f"=== 最常见的 (d_2, d_3) 配对 (前 10) ===")
    for (d2, d3), count in d_dist.most_common(10):
        print(f"  ({d2}, {d3}): {count}")


if __name__ == "__main__":
    main()
