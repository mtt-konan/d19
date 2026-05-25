#!/usr/bin/env python3
"""Batch-run PARI ``ell2cover`` (and ``ellrank`` for sha2) on every hard_case
``(A, B)`` pair in ``results/proof_status.db``.

For each pair we record:
- ``rank_lower / rank_upper / sha2_lower`` from ``ellrank(E, 1)``
- the quartic Selmer covers from ``ell2cover(E)``, as integer coefficient lists
- timing information

Output: ``results/ell2cover_hard_cases.jsonl``  (one row per pair)

This is the worklog 036 analog of Peschmann 2026 §7's "42 of E_A and 54 of
E'_A certified rank-0" verification: we want to see whether the Selmer
structure on d19 hard_case curves shows any uniform pattern (number of
covers, sha2_lower distribution, etc.) and whether any cover gives a
non-trivial obstruction.

This script depends on the worklog 036 fix to ``compute_rank`` (full 4-tuple
return; ``effort=1`` default). Run ``uv run pytest tests/test_concordant.py``
to confirm before running this batch.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

import cypari2  # noqa: E402

from rational_distance.proof_status import schema  # noqa: E402


def parse_quartic(quartic) -> list:
    """Convert a PARI polynomial of degree <= 4 into a list of coefficients
    [a0, a1, a2, a3, a4]  (constant term first). Coefficients are int when
    integral, else str fallback (rational coefficients keep PARI's printable
    form)."""
    # PARI polynomial: extract coefficients via Vec(g). Vec returns
    # high-degree-first; reverse to constant-first.
    coeffs = list(quartic.Vec())
    rev = list(reversed(coeffs))
    out: list = []
    for c in rev:
        try:
            out.append(int(c))
        except (TypeError, ValueError):
            out.append(str(c))
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
        default="results/ell2cover_hard_cases.jsonl",
        help="Output JSONL path (default: results/ell2cover_hard_cases.jsonl)",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of pairs (default: all hard_case pairs)",
    )
    ap.add_argument(
        "--effort",
        type=int,
        default=1,
        help="ellrank effort (default: 1, matching compute_rank's new default)",
    )
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: {db_path} not found. Run prove_no_solution.py first.")
        return 1

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)
    pairs = list(schema.iter_hard_cases(conn, limit=args.limit))
    print(f"Loaded {len(pairs)} hard_case pairs from {db_path}")

    pari = cypari2.Pari()
    pari.allocatemem(128 * 1024 * 1024)  # 128 MB

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"{'idx':>4} {'A':>10} {'B':>10}  "
        f"{'rank':<7} {'sha2':<5} {'n_cov':<5}  "
        f"{'t_rank':>7} {'t_cov':>7}  status"
    )
    print("-" * 90)

    t_total_start = time.perf_counter()
    n_processed = 0
    n_covers_distribution: dict[int, int] = {}
    sha2_distribution: dict[int, int] = {}
    rank_distribution: dict[int, int] = {}

    with open(out_path, "w", encoding="utf-8") as fh:
        for idx, pair in enumerate(pairs):
            A = int(pair["A"])
            B = int(pair["B"])
            a2, b2 = A * A, B * B
            E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")

            t0 = time.perf_counter()
            try:
                rank_result = pari.ellrank(E, args.effort)
                rank_lower = int(rank_result[0])
                rank_upper = int(rank_result[1])
                sha2_lower = int(rank_result[2]) if len(rank_result) > 2 else 0
                rank_err = None
            except Exception as exc:
                rank_lower = -2
                rank_upper = -2
                sha2_lower = -2
                rank_err = str(exc)
            t_rank = time.perf_counter() - t0

            t0 = time.perf_counter()
            try:
                covers = pari.ell2cover(E)
                cover_polys: list[list] = []
                for i in range(len(covers)):
                    cover_polys.append(parse_quartic(covers[i]))
                cover_err = None
            except Exception as exc:
                cover_polys = []
                cover_err = str(exc)
            t_cov = time.perf_counter() - t0

            n_cov = len(cover_polys)
            n_covers_distribution[n_cov] = n_covers_distribution.get(n_cov, 0) + 1
            sha2_distribution[sha2_lower] = sha2_distribution.get(sha2_lower, 0) + 1
            rank_distribution[rank_lower] = rank_distribution.get(rank_lower, 0) + 1

            status = "OK"
            if rank_err is not None:
                status = f"RANK_ERR: {rank_err[:40]}"
            elif cover_err is not None:
                status = f"COVER_ERR: {cover_err[:40]}"

            print(
                f"{idx:>4} {A:>10} {B:>10}  "
                f"[{rank_lower},{rank_upper}]   {sha2_lower:<5} {n_cov:<5}  "
                f"{t_rank:>6.3f}s {t_cov:>6.3f}s  {status}",
                flush=True,
            )

            fh.write(
                json.dumps(
                    {
                        "A": A,
                        "B": B,
                        "rank_lower": rank_lower,
                        "rank_upper": rank_upper,
                        "sha2_lower": sha2_lower,
                        "n_quartic_covers": n_cov,
                        "quartic_covers": cover_polys,
                        "rank_err": rank_err,
                        "cover_err": cover_err,
                        "time_rank_s": round(t_rank, 4),
                        "time_cover_s": round(t_cov, 4),
                        "effort": args.effort,
                    }
                )
                + "\n"
            )
            n_processed += 1

    t_total = time.perf_counter() - t_total_start
    print()
    print("=" * 72)
    print(f"Processed {n_processed} hard_case pairs in {t_total:.1f}s")
    print(f"Wrote {out_path}")
    print()
    print("Rank distribution (lower bound):")
    for rk, cnt in sorted(rank_distribution.items()):
        print(f"  rank={rk:>3}: {cnt:>4}")
    print()
    print("sha2_lower distribution (Sha[2] / E[2](Q) lower bound):")
    for sha2, cnt in sorted(sha2_distribution.items()):
        print(f"  sha2={sha2:>3}: {cnt:>4}")
    print()
    print("Number of quartic covers per curve:")
    for n_cov, cnt in sorted(n_covers_distribution.items()):
        print(f"  n_covers={n_cov:>3}: {cnt:>4}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
