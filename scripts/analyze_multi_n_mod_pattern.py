#!/usr/bin/env python3
"""阶段 4a: 分析真实 multi-N pair 在 mod p² surviving classes 上的分布.

For each m ∈ moduli, project all multi-N pairs (max_hyp ≤ 1M) to (A mod m,
B mod m), restrict to those NOT primary-killed at m (so they live inside
S_m^surviving), and report:

  - distinct (A mod m, B mod m) classes used by multi-N (T_m^multi-N)
  - |T_m^multi-N| / |S_m^surviving|
  - frequency table

This gives empirical evidence of "multi-N → strict subset of S_m^surviving":
the fundamental leverage for proving Conjecture B'.

Optionally prints algebraic invariants of the used classes (a mod p, b mod p,
(a+b) mod m, (b-a)(b+a) mod m, ...) to aid algebraic characterisation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.chain_closure_sieve import killed_at_modulus


def s_m_surviving(m: int) -> set[tuple[int, int]]:
    """Return {(a, b) ∈ (Z/mZ)² : ¬killed_at_modulus(a, b, m)}."""
    return {
        (a, b)
        for a in range(m)
        for b in range(m)
        if not killed_at_modulus(a, b, m)
    }


def analyze_modulus(
    recs: list[dict],  # type: ignore[type-arg]
    m: int,
    show_invariants: bool = False,
    show_unused: bool = False,
) -> None:
    used: Counter[tuple[int, int]] = Counter()
    killed = 0
    not_killed = 0
    for r in recs:
        primary_killers = set(r.get("primary_killers") or [])
        a = int(r["A"]) % m
        b = int(r["B"]) % m
        if m in primary_killers:
            killed += 1
        else:
            not_killed += 1
            used[(a, b)] += 1

    s_m = s_m_surviving(m)
    print(
        f"m={m:>4}  killed={killed:>4}  not_killed={not_killed:>4}  "
        f"distinct_used={len(used):>4}  |S_m|={len(s_m):>4}  "
        f"used/|S_m|={len(used)/len(s_m)*100:5.1f}%"
    )

    if show_invariants and used:
        used_keys = list(used.keys())
        invariants = {
            "(a mod p)": sorted({a % _root_p(m) for a, _ in used_keys}),
            "(b mod p)": sorted({b % _root_p(m) for _, b in used_keys}),
            "(a+b) mod m": sorted({(a + b) % m for a, b in used_keys}),
            "(b²-a²) mod m": sorted({(b * b - a * a) % m for a, b in used_keys}),
            "(a*b) mod m": sorted({(a * b) % m for a, b in used_keys}),
            "(a²+b²) mod m": sorted({(a * a + b * b) % m for a, b in used_keys}),
        }
        for k, v in invariants.items():
            print(f"     {k:<18}: {v}")

    if show_unused:
        unused = s_m - set(used.keys())
        print(f"     unused S_m classes ({len(unused)}): {sorted(unused)[:30]}")


def _root_p(m: int) -> int:
    """Return p where m = p²."""
    p = int(m**0.5)
    if p * p == m:
        return p
    return m  # not a perfect square; just return m


def main() -> None:
    parser = argparse.ArgumentParser(
        description="阶段 4a: 分析 multi-N pair 在 mod p² surviving classes 的分布."
    )
    parser.add_argument(
        "--audit",
        type=str,
        default="results/uniform_mod_p2_max1m.jsonl",
        help="JSONL audit dump (from uniform_mod_p2_audit).",
    )
    parser.add_argument(
        "--moduli",
        type=int,
        nargs="+",
        default=[9, 25, 49, 121, 169, 289, 361, 529, 841, 961],
        help="Moduli to analyze (default: 5²–31² primes squared).",
    )
    parser.add_argument(
        "--invariants",
        action="store_true",
        help="Show algebraic invariants of used classes for each modulus.",
    )
    parser.add_argument(
        "--unused",
        action="store_true",
        help="Show S_m classes NOT used by any multi-N (sample).",
    )
    args = parser.parse_args()

    audit_path = PROJECT_ROOT / args.audit
    if not audit_path.is_absolute():
        audit_path = PROJECT_ROOT / args.audit
    print(f"loading {audit_path}")
    with open(audit_path) as f:
        recs = [json.loads(line) for line in f]
    print(f"total multi-N pairs: {len(recs)}")
    print()

    for m in args.moduli:
        analyze_modulus(recs, m, show_invariants=args.invariants, show_unused=args.unused)


if __name__ == "__main__":
    main()
