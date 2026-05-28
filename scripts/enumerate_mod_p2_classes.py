#!/usr/bin/env python3
"""阶段 3b: enumerate (a, b) mod p² classes safe-pass + 未被任何 primary M kill.

For a given finite set of moduli M_0 ⊂ STANDARD_MODULI, enumerate:
  - All (a, b) ∈ (Z/MZ)² where M = lcm(4, M_0)
  - Safe-pass: a odd, b odd, (a+b) ≡ 0 mod 4
  - Not killed by primary chain_closure_mod_sieve at any M_i ∈ M_0

The surviving set gives the "mod-level closure-feasible" classes. If empty,
Conjecture B' is proven at this mod p² level (modulo Z-level multi-N
constraints). If non-empty, we list a sample and check Z-level multi-N
existence + dual sieve coverage.

For small M_0, brute enumeration is tractable.
"""

from __future__ import annotations

import argparse
import sys
from math import lcm
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.chain_closure_sieve import (
    STANDARD_MODULI,
    allowed_n_mod,
    killed_at_modulus,
)


from dataclasses import dataclass


@dataclass
class EnumerationResult:
    M_full: int
    moduli: tuple[int, ...]
    total_classes: int
    safe_pass_count: int
    killed_count: int
    surviving_count: int
    surviving_sample: list[tuple[int, int]]


def enumerate_classes(moduli: tuple[int, ...]) -> EnumerationResult:
    """Enumerate (a, b) ∈ (Z/MZ)² with M = lcm(4, moduli), safe-pass, not
    killed by any chain_closure_mod_sieve at moduli."""
    M_full = lcm(4, *moduli)
    total = M_full * M_full
    safe_pass_count = 0
    killed_count = 0
    surviving: list[tuple[int, int]] = []

    # Cache T(a mod m, b mod m, m) is per-m and per-(a mod m, b mod m).
    # killed_at_modulus 自身已经够快 (m ≤ ~3000). 我们直接调用即可.
    for a in range(M_full):
        if a % 2 == 0:
            continue
        for b in range(M_full):
            if b % 2 == 0:
                continue
            if (a + b) % 4 != 0:
                continue
            safe_pass_count += 1
            # Check primary kill at each m in moduli
            is_killed = False
            for m in moduli:
                if killed_at_modulus(a % m, b % m, m):
                    is_killed = True
                    break
            if is_killed:
                killed_count += 1
            elif len(surviving) < 50:
                surviving.append((a, b))

    surviving_count = safe_pass_count - killed_count
    return EnumerationResult(
        M_full=M_full,
        moduli=moduli,
        total_classes=total,
        safe_pass_count=safe_pass_count,
        killed_count=killed_count,
        surviving_count=surviving_count,
        surviving_sample=surviving,
    )


def check_multi_n_feasibility(a: int, b: int, moduli: tuple[int, ...]) -> dict[int, bool]:
    """For a surviving class (a, b), check if T(a mod m, b mod m, m) is non-empty
    for each m (i.e., locally multi-N feasible at each m)."""
    out: dict[int, bool] = {}
    for m in moduli:
        T = allowed_n_mod(a % m, b % m, m)
        out[m] = len(T) > 0
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="阶段 3b: enumerate (a, b) classes safe-pass + not killed by primary."
    )
    parser.add_argument(
        "--moduli",
        type=int,
        nargs="+",
        default=[9, 25],
        help="Moduli to use (default: 9 25 = 3², 5²)",
    )
    parser.add_argument(
        "--check-T",
        action="store_true",
        help="For surviving classes, also report T-emptiness per modulus.",
    )
    args = parser.parse_args()

    moduli = tuple(args.moduli)
    # Validate moduli ⊆ STANDARD_MODULI
    for m in moduli:
        if m not in STANDARD_MODULI:
            print(f"warning: M={m} not in STANDARD_MODULI; continuing anyway")

    print(f"moduli = {moduli}")
    print(f"M_full = lcm(4, {moduli}) = {lcm(4, *moduli)}")
    if lcm(4, *moduli) > 10000:
        print(
            f"warning: M_full = {lcm(4, *moduli)} > 10000, "
            "enumeration will be slow"
        )

    print("[phase] enumerating safe-pass + primary-kill classes...")
    result = enumerate_classes(moduli)

    print("=" * 72)
    print(f"M_full:              {result.M_full}")
    print(f"total classes:       {result.total_classes}")
    print(f"safe-pass classes:   {result.safe_pass_count}")
    sp = result.safe_pass_count or 1
    print(
        f"  killed by primary: {result.killed_count} "
        f"({100.0 * result.killed_count / sp:.2f}%)"
    )
    print(
        f"  surviving:         {result.surviving_count} "
        f"({100.0 * result.surviving_count / sp:.2f}%)"
    )

    print()
    print("First 20 surviving (a, b) classes:")
    surviving_sample = result.surviving_sample
    for a, b in surviving_sample[:20]:
        line = f"  (a={a}, b={b})"
        if args.check_T:
            T_check = check_multi_n_feasibility(a, b, moduli)
            T_str = "  T-non-empty at: " + ", ".join(
                f"M={m}" for m, ok in T_check.items() if ok
            )
            line += T_str
        print(line)


if __name__ == "__main__":
    main()
