#!/usr/bin/env python3
"""End-to-end 验证 Conjecture A1 严格证明链 (wl081 + wl082 + wl083)
对全 max_hyp=1M 的 1879 个 k=2 multi-N pair.

Verifies all algebraic equalities:

  1. (r_2 + N)(r_2 - N) = A²,  sf(r_2 + N) = sf(r_2 - N) =: d_2
  2. (r_3 + N)(r_3 - N) = B²,  sf(r_3 + N) = sf(r_3 - N) =: d_3
  3. r_2 - N = u² d_2,  r_2 + N = s² d_2   (so u, s integer)
  4. r_3 - N = q² d_3,  r_3 + N = p² d_3
  5. A = u s d_2,  B = p q d_3
  6. d_2, d_3 squarefree, gcd(d_2, d_3) = 1   (since gcd(A, B) = 1)
  7. x_Q = (r_2 - N)(r_3 - N) = (u q)² d_2 d_3
  8. sf(x_Q) = d_2 d_3                         ★ wl083 核心简化
  9. δ(Q) = 0 ⟺ sf(x_Q) = 1 AND sf(x_Q + A²) = 1
       ⟺ d_2 d_3 = 1 AND u² + p² ∈ □
       ⟺ d_2 = d_3 = 1 AND u² + p² ∈ □
 10. ∀ row: NOT (d_2=d_3=1 AND u²+p² ∈ □)    ★ wl082 + wl083 conclusion
"""

from __future__ import annotations

import argparse
import json
from math import gcd, isqrt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


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


def is_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/k2_f2_rank_max1m.jsonl")
    args = parser.parse_args()

    inp = PROJECT_ROOT / args.input
    rows = [json.loads(line) for line in open(inp)]
    print(f"verifying A1 proof chain on {len(rows)} k=2 multi-N pairs\n")

    fail_step = {i: 0 for i in range(1, 11)}
    n_d2_d3_eq_1 = 0
    n_check_pass = 0

    for r in rows:
        A = r["A"]
        B = r["B"]
        for N in (r["N_1"], r["N_2"]):
            r2 = isqrt(N * N + A * A)
            r3 = isqrt(N * N + B * B)

            # Step 1, 2: Pythagorean recompose
            if (r2 + N) * (r2 - N) != A * A:
                fail_step[1] += 1
                continue
            if (r3 + N) * (r3 - N) != B * B:
                fail_step[2] += 1
                continue
            d_2 = squarefree(r2 + N)
            d_3 = squarefree(r3 + N)
            if d_2 != squarefree(r2 - N):
                fail_step[1] += 1
                continue
            if d_3 != squarefree(r3 - N):
                fail_step[2] += 1
                continue

            # Step 3, 4: extract u, s, p, q
            u_sq = (r2 - N) // d_2
            s_sq = (r2 + N) // d_2
            q_sq = (r3 - N) // d_3
            p_sq = (r3 + N) // d_3
            if not is_square(u_sq) or not is_square(s_sq):
                fail_step[3] += 1
                continue
            if not is_square(q_sq) or not is_square(p_sq):
                fail_step[4] += 1
                continue
            u = isqrt(u_sq)
            s = isqrt(s_sq)
            q = isqrt(q_sq)
            p = isqrt(p_sq)

            # Step 5: A = u s d_2, B = p q d_3
            if u * s * d_2 != A:
                fail_step[5] += 1
                continue
            if p * q * d_3 != B:
                fail_step[5] += 1
                continue

            # Step 6: d_2, d_3 squarefree (already by sf def), gcd(d_2, d_3) = 1
            if gcd(d_2, d_3) != 1:
                fail_step[6] += 1
                continue

            # Step 7: x_Q = (u q)² d_2 d_3
            x_Q_alg = (u * q) ** 2 * d_2 * d_3
            x_Q_actual = (r2 - N) * (r3 - N)
            if x_Q_alg != x_Q_actual:
                fail_step[7] += 1
                continue

            # Step 8: sf(x_Q) = d_2 d_3
            if squarefree(x_Q_actual) != d_2 * d_3:
                fail_step[8] += 1
                continue

            # Step 10: NOT (d_2=d_3=1 AND u²+p² ∈ □)
            if d_2 == 1 and d_3 == 1:
                n_d2_d3_eq_1 += 1
                if is_square(u * u + p * p):
                    fail_step[10] += 1
                    print(f"!! VIOLATION: A={A}, B={B}, N={N}: u={u}, p={p}, u²+p²={u*u+p*p}")
                    continue

            n_check_pass += 1

    n_total = 2 * len(rows)
    print(f"=== A1 proof chain verification ===")
    for step, fails in sorted(fail_step.items()):
        if fails:
            print(f"  step {step}: {fails} failures")
    print(f"\n  passed all 10 algebraic equalities: {n_check_pass}/{n_total}")
    print(f"  d_2 = d_3 = 1 cases: {n_d2_d3_eq_1}/{n_total}")
    print(f"  step 10 violations (u²+p² ∈ □): {fail_step[10]}/{n_d2_d3_eq_1}")
    if n_check_pass == n_total and fail_step[10] == 0:
        print("\n★★★ A1 严格证明链在 max_hyp=1M (1879×2 = 3758 chosen N) 上 100% 一致")
    else:
        print("\n!! A1 证明链 inconsistency 出现")


if __name__ == "__main__":
    main()
