#!/usr/bin/env python3
"""Layer-2 finite-descent: enumerate N candidates via CRT-merged mod-p sieve.

Layer 1 (finite_descent_hard_cases.py) showed that no hard_case has a
*universal* blocker prime — every per-prime mod-p allowed-residue set is
non-empty. That rules out the cheapest finite-descent obstruction.

Layer 2 takes the next step: for a chosen small-prime set ``P_small``, build
the joint allowed residue set modulo ``M = lcm(P_small)`` via CRT — call
this ``allowed_M``. Then enumerate ``N`` in ``[1, N_max]`` restricted to
``allowed_M``, and for each ``N`` do an *exact* perfect-square test of both
``N²+A²`` and ``N²+B²``.

This mimics Peschmann 2026 §7(2)'s lattice search, with the advantage that
we never enumerate any ``N`` outside ``allowed_M``: the small-prime sieve
cuts most of the search space upfront.

For each hard_case we report:
- |allowed_M|              size of joint allowed residue set mod M
- density_M                = |allowed_M| / M
- n_passing_sieve          number of N in [1, N_max] that survived the mod-M sieve
- n_concordant             N's that genuinely make both N²+A² and N²+B² squares
- n_chain_compatible       N's that additionally pass the full 4-chain closure check
                           (b = A+B-N gives a positive integer and satisfies the
                           remaining two Pythagorean conditions)

Output: ``results/finite_descent_layer2.jsonl``  (one row per pair).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from math import isqrt, lcm
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.proof_status import schema  # noqa: E402


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, p in enumerate(sieve) if p]


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def build_allowed_residues_mod_M(
    A: int, B: int, primes: list[int], M: int
) -> list[int]:
    """Return all n in [0, M) such that for every prime p in `primes`,
    both n²+A² and n²+B² are quadratic residues mod p."""
    a2 = A * A
    b2 = B * B
    qr_table: dict[int, set[int]] = {p: {(x * x) % p for x in range(p)} for p in primes}
    a2_mod = {p: a2 % p for p in primes}
    b2_mod = {p: b2 % p for p in primes}
    out: list[int] = []
    for n in range(M):
        ok = True
        for p in primes:
            np_ = n % p
            n2_p = (np_ * np_) % p
            if (n2_p + a2_mod[p]) % p not in qr_table[p]:
                ok = False
                break
            if (n2_p + b2_mod[p]) % p not in qr_table[p]:
                ok = False
                break
        if ok:
            out.append(n)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="results/proof_status.db")
    ap.add_argument("--out", default="results/finite_descent_layer2.jsonl")
    ap.add_argument(
        "--small-prime-bound",
        type=int,
        default=30,
        help="Use primes < this bound for the joint mod-M sieve (default: 30 -> "
        "primes 2..29, M = 6469693230)",
    )
    ap.add_argument(
        "--n-max",
        type=int,
        default=1_000_000,
        help="Largest N to enumerate (default: 1,000,000)",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of hard_case pairs (default: all)",
    )
    ap.add_argument(
        "--verbose",
        action="store_true",
    )
    args = ap.parse_args()

    primes = primes_up_to(args.small_prime_bound - 1)
    M = 1
    for p in primes:
        M = lcm(M, p)

    if M > 10_000_000:
        print(
            f"WARNING: M = {M} is large; building allowed-residue table per pair "
            f"may take several seconds each. Consider --small-prime-bound <= 13 "
            f"(M = 30030)."
        )

    print(
        f"Using {len(primes)} primes < {args.small_prime_bound}: {primes}\n"
        f"Joint modulus M = {M}\n"
        f"N_max = {args.n_max:,}"
    )

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: {db_path} not found.")
        return 1

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)
    pairs = list(schema.iter_hard_cases(conn, limit=args.limit))
    print(f"Loaded {len(pairs)} hard_case pairs from {db_path}\n")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"{'idx':>4} {'A':>10} {'B':>10}  "
        f"{'|allow_M|':>10} {'density':>9}  "
        f"{'pass_sieve':>10} {'conc':>5} {'chain':>5}  status"
    )
    print("-" * 110)

    t_start = time.perf_counter()
    n_chain_solutions = 0
    n_pass_sieve_total = 0
    n_zero_after_sieve = 0  # pairs whose actual_n_passing_M == 0

    with open(out_path, "w", encoding="utf-8") as fh:
        for idx, pair in enumerate(pairs):
            A = int(pair["A"])
            B = int(pair["B"])

            t_build = time.perf_counter()
            allowed_residues = build_allowed_residues_mod_M(A, B, primes, M)
            t_build_s = time.perf_counter() - t_build

            n_allowed = len(allowed_residues)
            density_M = n_allowed / M

            # Enumerate N in [1, N_max] restricted to allowed residue classes.
            t_enum = time.perf_counter()
            n_passing_sieve = 0
            concordant_N: list[int] = []
            chain_compatible_N: list[int] = []
            for r in allowed_residues:
                # First N >= 1 with N ≡ r (mod M)
                if r == 0:
                    N_ = M
                else:
                    N_ = r
                while N_ <= args.n_max:
                    n_passing_sieve += 1
                    if is_perfect_square(N_ * N_ + A * A) and is_perfect_square(
                        N_ * N_ + B * B
                    ):
                        concordant_N.append(N_)
                        # Full 4-chain closure: b = A + B - N_ must be positive
                        # integer, and b²+A², b²+B² must be perfect squares too.
                        b = A + B - N_
                        if (
                            b > 0
                            and b != N_  # avoid degenerate
                            and is_perfect_square(b * b + A * A)
                            and is_perfect_square(b * b + B * B)
                        ):
                            chain_compatible_N.append(N_)
                    N_ += M
            t_enum_s = time.perf_counter() - t_enum

            n_concordant = len(concordant_N)
            n_chain = len(chain_compatible_N)
            n_chain_solutions += n_chain
            n_pass_sieve_total += n_passing_sieve
            if n_passing_sieve == 0:
                n_zero_after_sieve += 1

            expected = density_M * args.n_max

            status = "OK"
            if n_chain > 0:
                status = f"*** {n_chain} CHAIN: {chain_compatible_N[:3]}"
            elif n_concordant > 0:
                status = f"{n_concordant} concordant (no chain): N={concordant_N[:3]}"
            elif n_passing_sieve == 0:
                status = "BLOCKED (sieve killed every N)"
            elif args.verbose:
                status = f"sieve survived {n_passing_sieve} candidates"

            if args.verbose or n_chain > 0 or n_passing_sieve == 0 or idx < 3:
                print(
                    f"{idx:>4} {A:>10} {B:>10}  "
                    f"{n_allowed:>10} {density_M:>9.2e}  "
                    f"{n_passing_sieve:>10} {n_concordant:>5} {n_chain:>5}  {status}",
                    flush=True,
                )

            fh.write(
                json.dumps(
                    {
                        "A": A,
                        "B": B,
                        "primes_used": primes,
                        "M": M,
                        "n_allowed_residues_mod_M": n_allowed,
                        "density_M": density_M,
                        "expected_n_in_range": expected,
                        "n_max": args.n_max,
                        "n_passing_sieve": n_passing_sieve,
                        "n_concordant": n_concordant,
                        "n_chain_compatible": n_chain,
                        "concordant_N": concordant_N[:50],
                        "chain_compatible_N": chain_compatible_N[:50],
                        "time_build_s": round(t_build_s, 4),
                        "time_enum_s": round(t_enum_s, 4),
                    }
                )
                + "\n"
            )

    elapsed = time.perf_counter() - t_start

    print()
    print("=" * 72)
    print(f"Processed {len(pairs)} hard_case pairs in {elapsed:.1f}s")
    print(f"  Chain-compatible N found across all pairs: {n_chain_solutions}")
    print(f"  Pairs blocked by sieve (0 survivors): {n_zero_after_sieve}")
    print(f"  Total candidates surviving sieve: {n_pass_sieve_total:,}")
    print(f"Wrote {out_path}")
    if n_chain_solutions == 0:
        print()
        print(
            f"NO chain-compatible N found in [1, {args.n_max:,}] across any of the "
            f"{len(pairs)} hard_case pairs."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
