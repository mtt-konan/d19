#!/usr/bin/env python3
"""Finite-descent / modular obstruction search on hard_case (A, B) pairs.

This is the d19 analog of Peschmann 2026 §7(2): for each hard_case we ask
whether there exists any integer ``N`` such that both ``N²+A²`` and
``N²+B²`` are perfect squares.

The cheap layer (this script's main output) checks, for each prime ``p`` in
a chosen prime set, whether there exists *any* residue ``n mod p`` satisfying
both congruence conditions:

    n² + A² is a quadratic residue mod p
    AND
    n² + B² is a quadratic residue mod p

If for some prime ``p`` no such residue exists, then no integer ``N`` can
satisfy both squareness conditions — this is a *universal blocker prime*
and gives a finite-descent obstruction.

If every prime admits at least one allowed residue, we report the joint
density (product of |allowed| / p over all primes), which is a Hardy-
Littlewood-style estimate of how many ``N`` should give chain candidates
in a given range.

The expensive layer (lattice enumeration of N up to some bound, intersected
with the union of allowed residue classes via CRT) is deferred to a follow-up
script — this one is the "is there any cheap obstruction at all?" probe.

Output: ``results/finite_descent_hard_cases.jsonl``  (one row per pair).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.proof_status import schema  # noqa: E402


def primes_up_to(limit: int) -> list[int]:
    """Sieve of Eratosthenes."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]


def quadratic_residues(p: int) -> set[int]:
    """Return quadratic residues mod p (including 0)."""
    return {(x * x) % p for x in range(p)}


def allowed_n_residues(A: int, B: int, p: int, qr_p: set[int]) -> set[int]:
    """Return residues ``n mod p`` such that both n²+A² and n²+B² are QR mod p."""
    A2 = (A * A) % p
    B2 = (B * B) % p
    out: set[int] = set()
    for n in range(p):
        n2 = (n * n) % p
        if (n2 + A2) % p in qr_p and (n2 + B2) % p in qr_p:
            out.add(n)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--db",
        default="results/proof_status.db",
        help="proof_status SQLite database (default: results/proof_status.db)",
    )
    ap.add_argument(
        "--out",
        default="results/finite_descent_hard_cases.jsonl",
        help="Output JSONL path (default: results/finite_descent_hard_cases.jsonl)",
    )
    ap.add_argument(
        "--prime-bound",
        type=int,
        default=200,
        help="Largest prime to use in modular check (default: 200, ~46 primes)",
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
        help="Print per-pair detailed allowed-residue counts",
    )
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: {db_path} not found. Run prove_no_solution.py first.")
        return 1

    primes = primes_up_to(args.prime_bound)
    qr_per_p = {p: quadratic_residues(p) for p in primes}
    print(f"Using {len(primes)} primes <= {args.prime_bound}: {primes[:10]}...")

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)
    pairs = list(schema.iter_hard_cases(conn, limit=args.limit))
    print(f"Loaded {len(pairs)} hard_case pairs from {db_path}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print()
    print(
        f"{'idx':>4} {'A':>10} {'B':>10}  "
        f"{'min_p':>6} {'min_allow':>10} {'log_density':>12}  status"
    )
    print("-" * 80)

    t_start = time.perf_counter()
    n_blocked = 0
    n_passing = 0
    blocked_pairs: list[tuple[int, int, int]] = []
    log_density_distribution: list[float] = []

    with open(out_path, "w", encoding="utf-8") as fh:
        for idx, pair in enumerate(pairs):
            A = int(pair["A"])
            B = int(pair["B"])

            # Phase 1: per-prime allowed residue count
            min_allow = None
            min_p = None
            log_density = 0.0  # sum of log(|allowed_p|/p)
            per_prime: list[dict] = []
            blocked = False
            blocker_p = None

            for p in primes:
                allowed = allowed_n_residues(A, B, p, qr_per_p[p])
                count = len(allowed)
                per_prime.append({"p": p, "n_allowed": count})
                if count == 0:
                    blocked = True
                    blocker_p = p
                    break  # no need to keep checking
                if min_allow is None or count < min_allow:
                    min_allow = count
                    min_p = p
                # log_density: log(count) - log(p) ; we use natural log
                import math

                log_density += math.log(count) - math.log(p)

            if blocked:
                n_blocked += 1
                blocked_pairs.append((A, B, blocker_p))
                status = f"BLOCKED@p={blocker_p}"
            else:
                n_passing += 1
                log_density_distribution.append(log_density)
                status = f"pass (log_density={log_density:.2f})"

            if args.verbose or blocked:
                print(
                    f"{idx:>4} {A:>10} {B:>10}  "
                    f"{min_p if min_p is not None else '-':>6} "
                    f"{min_allow if min_allow is not None else '-':>10} "
                    f"{log_density:>12.3f}  {status}",
                    flush=True,
                )

            fh.write(
                json.dumps(
                    {
                        "A": A,
                        "B": B,
                        "blocked": blocked,
                        "blocker_p": blocker_p,
                        "min_allow_count": min_allow,
                        "min_allow_p": min_p,
                        "log_density": log_density,
                        "per_prime": per_prime,
                    }
                )
                + "\n"
            )

    elapsed = time.perf_counter() - t_start

    print()
    print("=" * 72)
    print(f"Processed {len(pairs)} hard_case pairs in {elapsed:.1f}s")
    print(f"  blocked (universal obstruction): {n_blocked}")
    print(f"  passing                        : {n_passing}")
    print(f"Wrote {out_path}")

    if blocked_pairs:
        print()
        print("Blocked pairs (and the smallest blocker prime found):")
        for A, B, p in blocked_pairs[:20]:
            print(f"  (A={A}, B={B}) blocked by p={p}")
        if len(blocked_pairs) > 20:
            print(f"  ... and {len(blocked_pairs) - 20} more")

    if log_density_distribution:
        log_density_distribution.sort()
        n = len(log_density_distribution)
        print()
        print("log_density distribution among passing pairs:")
        print(f"  min:    {log_density_distribution[0]:.3f}")
        print(f"  10 %ile: {log_density_distribution[n // 10]:.3f}")
        print(f"  median: {log_density_distribution[n // 2]:.3f}")
        print(f"  90 %ile: {log_density_distribution[9 * n // 10]:.3f}")
        print(f"  max:    {log_density_distribution[-1]:.3f}")
        print()
        print("Interpretation:")
        print("  log_density ~ sum log(|allowed_p|/p) over all primes p < bound.")
        print("  More negative -> fewer surviving N residue classes.")
        print("  This is a Hardy-Littlewood-style heuristic, not a proof.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
