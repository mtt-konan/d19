#!/usr/bin/env python3
r"""阶段 4a (深入): 分析 S_m 中未被 multi-N 触及的 classes 的代数特征.

For each m ∈ moduli, partition S_m^surviving \ T_m^multi-N into:
  - primitivity-excluded: p | a AND p | b  (where m = p²)
  - real obstruction: NOT (p | a AND p | b) but still unused

The "real obstruction" classes are the algebraic core to characterise for
Conjecture B' proof.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.chain_closure_sieve import killed_at_modulus


def s_m_surviving(m: int) -> set[tuple[int, int]]:
    return {
        (a, b)
        for a in range(m)
        for b in range(m)
        if not killed_at_modulus(a, b, m)
    }


def root_p(m: int) -> int:
    p = int(m**0.5)
    if p * p == m:
        return p
    return m


def analyze_unused(recs: list, m: int) -> None:  # type: ignore[type-arg]
    used: Counter[tuple[int, int]] = Counter()
    for r in recs:
        primary_killers = set(r.get("primary_killers") or [])
        if m in primary_killers:
            continue
        used[(int(r["A"]) % m, int(r["B"]) % m)] += 1

    s_m = s_m_surviving(m)
    unused = s_m - set(used.keys())
    p = root_p(m)
    prim_excluded = {(a, b) for (a, b) in unused if a % p == 0 and b % p == 0}
    real_obstruction = unused - prim_excluded

    print(f"m={m:>4}  |S_m|={len(s_m):>6}  used={len(used):>5}  unused={len(unused):>5}")
    print(f"     primitivity-excluded (p|a AND p|b): {len(prim_excluded):>4}")
    print(f"     REAL OBSTRUCTION (not primitivity): {len(real_obstruction):>4}")
    if real_obstruction and len(real_obstruction) <= 80:
        print(f"     classes: {sorted(real_obstruction)}")
    elif real_obstruction:
        print(f"     sample (first 20): {sorted(real_obstruction)[:20]}")

    # Algebraic check on real obstruction
    if real_obstruction:
        invariants: dict[str, set[int]] = {
            "a mod p": set(),
            "b mod p": set(),
            "(a+b) mod p": set(),
            "(b-a) mod p": set(),
            "(b²-a²) mod p²": set(),
            "(a²+b²) mod p²": set(),
        }
        for a, b in real_obstruction:
            invariants["a mod p"].add(a % p)
            invariants["b mod p"].add(b % p)
            invariants["(a+b) mod p"].add((a + b) % p)
            invariants["(b-a) mod p"].add((b - a) % p)
            invariants["(b²-a²) mod p²"].add((b * b - a * a) % m)
            invariants["(a²+b²) mod p²"].add((a * a + b * b) % m)
        for k, v in invariants.items():
            if len(v) < p + 1 or len(v) < 20:
                print(f"     {k:<20}: {sorted(v)}")
            else:
                print(f"     {k:<20}: {len(v)} distinct values")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="分析 mod p² unused classes 的 primitivity vs real obstruction."
    )
    parser.add_argument(
        "--audit", default="results/uniform_mod_p2_max1m.jsonl",
    )
    parser.add_argument(
        "--moduli", type=int, nargs="+", default=[9, 25, 49, 121, 169],
    )
    args = parser.parse_args()

    audit_path = PROJECT_ROOT / args.audit
    with open(audit_path) as f:
        recs = [json.loads(line) for line in f]
    print(f"loaded {len(recs)} multi-N pairs from {audit_path}\n")

    for m in args.moduli:
        analyze_unused(recs, m)
        print()


if __name__ == "__main__":
    main()
