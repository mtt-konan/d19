#!/usr/bin/env python3
"""阶段 3c: CRT-style enumeration of (a, b) mod M classes.

Replaces brute O(M_full²) enumeration in :mod:`enumerate_mod_p2_classes` with
CRT factorisation: since 4 and each prime² in :data:`STANDARD_MODULI` are
pairwise coprime, the safe-pass-and-primary-survival predicate is a product
predicate, so

    |surviving mod M_full| = |safe_4| * Π_m |S_m|

where
  - |safe_4| = #{(a, b) ∈ (Z/4Z)² : a odd, b odd, a+b ≡ 0 mod 4} = 2
  - S_m = {(a, b) ∈ (Z/mZ)² : ¬killed_at_modulus(a, b, m)}.

Run cost: O(Σ m²) per modulus rather than O((Π m)²) joint, so we can scale
to {9, 25, 49, 121, 169, ...}.

Optionally CRT-sample N surviving (a, b) mod M_full and report dual-sieve
auxiliary checks against larger moduli set.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import asdict, dataclass
from math import lcm
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.chain_closure_sieve import (
    STANDARD_MODULI,
    killed_at_modulus,
)


@dataclass
class PerModulusStat:
    m: int
    total_pairs: int
    survived: int
    killed: int
    survival_fraction: float


@dataclass
class CRTEnumerationResult:
    moduli: tuple[int, ...]
    M_full: int
    safe_4: int
    per_modulus: list[PerModulusStat]
    surviving_total: int
    safe_pass_total: int
    surviving_fraction_of_safe_pass: float


def safe_pass_mod4_count() -> int:
    """Count (a, b) ∈ (Z/4Z)² with a odd, b odd, (a+b) ≡ 0 mod 4."""
    cnt = 0
    for a in range(4):
        if a % 2 == 0:
            continue
        for b in range(4):
            if b % 2 == 0:
                continue
            if (a + b) % 4 == 0:
                cnt += 1
    return cnt


def per_modulus_stats(m: int) -> PerModulusStat:
    """Compute |S_m| = #{(a, b) ∈ (Z/mZ)² : ¬killed_at_modulus(a, b, m)}."""
    total = m * m
    killed = 0
    for a in range(m):
        for b in range(m):
            if killed_at_modulus(a, b, m):
                killed += 1
    survived = total - killed
    return PerModulusStat(
        m=m,
        total_pairs=total,
        survived=survived,
        killed=killed,
        survival_fraction=survived / total,
    )


def survived_set(m: int) -> list[tuple[int, int]]:
    """Return the surviving (a, b) ∈ (Z/mZ)²."""
    out: list[tuple[int, int]] = []
    for a in range(m):
        for b in range(m):
            if not killed_at_modulus(a, b, m):
                out.append((a, b))
    return out


def crt_lift(remainders: list[tuple[int, int, int]]) -> tuple[int, int]:
    """Given list of (a_m, b_m, m) with pairwise-coprime m, return (a, b)
    mod prod(m)."""
    a = 0
    b = 0
    cur = 1
    for a_m, b_m, m in remainders:
        # standard incremental CRT: find inverse of cur mod m
        inv = pow(cur, -1, m) if cur > 1 else 1
        diff_a = (a_m - a % m) * inv % m
        diff_b = (b_m - b % m) * inv % m
        a += cur * diff_a
        b += cur * diff_b
        cur *= m
    return a % cur, b % cur


def main() -> None:
    parser = argparse.ArgumentParser(
        description="阶段 3c: CRT-style enumeration of (a, b) mod p² classes."
    )
    parser.add_argument(
        "--moduli",
        type=int,
        nargs="+",
        default=[9, 25, 49, 121, 169],
        help="Moduli to use (default: 9 25 49 121 169).",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=0,
        help="If > 0, CRT-lift this many random surviving (a, b) mod M_full "
             "and dump them for downstream dual-sieve check.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional JSON output path.",
    )
    args = parser.parse_args()

    moduli: tuple[int, ...] = tuple(int(m) for m in args.moduli)
    for m in moduli:
        if m not in STANDARD_MODULI:
            print(f"warning: M={m} not in STANDARD_MODULI; continuing anyway")

    M_full = lcm(4, *moduli)
    safe_4 = safe_pass_mod4_count()
    print(f"moduli = {moduli}")
    print(f"M_full = lcm(4, {moduli}) = {M_full}")
    print(f"safe_4 = {safe_4}")

    per_m: list[PerModulusStat] = []
    sm_lists: dict[int, list[tuple[int, int]]] = {}
    for m in moduli:
        stat = per_modulus_stats(m)
        per_m.append(stat)
        print(
            f"  m={m:>4}  total={stat.total_pairs:>8}  "
            f"survived={stat.survived:>8}  killed={stat.killed:>8}  "
            f"frac={stat.survival_fraction:.4f}"
        )
        if args.sample > 0:
            sm_lists[m] = survived_set(m)

    surviving_total = safe_4
    for stat in per_m:
        surviving_total *= stat.survived
    safe_pass_total = safe_4
    for m in moduli:
        safe_pass_total *= m * m
    surviving_fraction = surviving_total / safe_pass_total

    print("=" * 72)
    print(f"M_full:              {M_full}")
    print(f"safe-pass classes:   {safe_pass_total}")
    print(f"surviving classes:   {surviving_total}")
    print(f"  fraction of safe-pass: {surviving_fraction * 100:.4f}%")
    print(f"  fraction of total:     {surviving_total / (M_full * M_full) * 100:.4f}%")

    samples: list[dict[str, int]] = []
    if args.sample > 0 and surviving_total > 0:
        rng = random.Random(20260527)
        # pick mod 4 safe pair
        safe4_pairs = [
            (a, b)
            for a in range(4)
            for b in range(4)
            if a % 2 == 1 and b % 2 == 1 and (a + b) % 4 == 0
        ]
        for _ in range(args.sample):
            a4, b4 = rng.choice(safe4_pairs)
            rems = [(a4, b4, 4)]
            for m in moduli:
                a_m, b_m = rng.choice(sm_lists[m])
                rems.append((a_m, b_m, m))
            a_full, b_full = crt_lift(rems)
            # sanity check
            assert a_full % 2 == 1 and b_full % 2 == 1
            assert (a_full + b_full) % 4 == 0
            for m in moduli:
                assert not killed_at_modulus(a_full % m, b_full % m, m)
            samples.append({"a": a_full, "b": b_full})
        print()
        print(f"sampled {len(samples)} surviving CRT lifts (mod {M_full}):")
        for s in samples[:10]:
            print(f"  a={s['a']}, b={s['b']}")

    result = CRTEnumerationResult(
        moduli=moduli,
        M_full=M_full,
        safe_4=safe_4,
        per_modulus=per_m,
        surviving_total=surviving_total,
        safe_pass_total=safe_pass_total,
        surviving_fraction_of_safe_pass=surviving_fraction,
    )

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(result)
        payload["samples"] = samples
        out_path.write_text(json.dumps(payload, indent=2, default=str))
        print(f"\nresults written to {out_path}")


if __name__ == "__main__":
    main()
