#!/usr/bin/env python3
"""阶段 4b 实证: 分析 multi-N pair 的 D = B²-A² 的 p-adic valuation 分布.

For each prime p ∈ {3, 5, 7, 11, 13, 17, 19, 23, 29, 31}, compute v_p(D)
distribution across multi-N pairs. Particularly check empirical claim:

    "primitive multi-N (A, B) ⟹ v_5(B² - A²) ≠ 1"

(Lemma B.25 conjecture from wl079.) If 0% of multi-N pairs has v_5(D)=1,
this is empirically a true obstruction.

Also reports v_p(B-A), v_p(B+A) since D = (B-A)(B+A).
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def v_p(n: int, p: int) -> int:
    """p-adic valuation: largest k with p^k | n. v_p(0) = ∞ (return -1)."""
    if n == 0:
        return -1
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def analyze_pair(A: int, B: int, primes: list[int]) -> dict[int, dict[str, int]]:
    D = B * B - A * A
    out: dict[int, dict[str, int]] = {}
    for p in primes:
        out[p] = {
            "v_p(D)": v_p(D, p),
            "v_p(B-A)": v_p(B - A, p),
            "v_p(B+A)": v_p(B + A, p),
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audit",
        default="results/uniform_mod_p2_max2m.jsonl",
    )
    parser.add_argument(
        "--primes",
        type=int,
        nargs="+",
        default=[3, 5, 7, 11, 13, 17, 19, 23, 29, 31],
    )
    args = parser.parse_args()

    audit_path = PROJECT_ROOT / args.audit
    with open(audit_path) as f:
        recs = [json.loads(line) for line in f]
    print(f"loaded {len(recs)} multi-N pairs from {audit_path}\n")

    for p in args.primes:
        v_d_counter: Counter[int] = Counter()
        v_diff_counter: Counter[int] = Counter()
        v_sum_counter: Counter[int] = Counter()
        for r in recs:
            A = int(r["A"])
            B = int(r["B"])
            D = B * B - A * A
            v_d_counter[v_p(D, p)] += 1
            v_diff_counter[v_p(B - A, p)] += 1
            v_sum_counter[v_p(B + A, p)] += 1

        total = len(recs)
        print(f"p = {p}:")
        print(f"  v_{p}(D) = v_{p}(B²-A²) distribution:")
        for v in sorted(v_d_counter.keys()):
            count = v_d_counter[v]
            print(f"    v={v:>3}: {count:>5} ({count/total*100:5.2f}%)")
        # check Conjecture B.p²: v_p(D) ≠ 1?
        v1_count = v_d_counter.get(1, 0)
        if v1_count == 0:
            print(f"  ★ Conjecture B.{p}²: v_{p}(D) ≠ 1  HOLDS (0/{total} violations)")
        else:
            print(
                f"  ✗ Conjecture B.{p}²: v_{p}(D) ≠ 1  FAILS "
                f"({v1_count}/{total} = {v1_count/total*100:.2f}% have v_{p}(D)=1)"
            )
        print()


if __name__ == "__main__":
    main()
