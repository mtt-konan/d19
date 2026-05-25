#!/usr/bin/env python3
"""Idea 4 probe: dual EC rank distribution on chain near-miss candidates.

For each near-miss (a, b, c, d) from chain.db (where a+c=b+d holds by the §7
reduction, C1, C2, C3 all succeed, but C4 fails), this script computes the
ranks of both diagonal elliptic curves:

    E_{a,c}: Y^2 = X(X + a^2)(X + c^2)   <-- d19 main-line direction
    E_{b,d}: Y^2 = X(X + b^2)(X + d^2)   <-- dual direction (Idea 4)

Goal: how often is rank(E_{b,d}) = 0?

Each rank-0 dual is a "free obstruction": E_{b,d} only has 6 torsion X-coords
(0, -b^2, -d^2, +-bd), and the chain-closing condition C4 = (a^2 + d^2 is a
square) is equivalent to X = a^2 lying on E_{b,d}.  With rank = 0 the only way
to satisfy that is a^2 in {0, -b^2, -d^2, bd, -bd}, which forces a^2 = bd
(impossible unless bd is a perfect square -- extremely rare).

References:
    docs/CHAIN_STRUCTURE_IDEAS.md  section 5 (Idea 4)
    docs/MATH.md                   section 7 (chain reduction)
    docs/MATH.md                   section 8 (concordant EC)

Usage:
    uv run python scripts/probe_dual_ec.py --limit 5      # smoke test
    uv run python scripts/probe_dual_ec.py --limit 50     # main probe
    uv run python scripts/probe_dual_ec.py --no-dedup     # all 202 rows
    uv run python scripts/probe_dual_ec.py --out-jsonl results/dual_ec_probe.jsonl
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant import compute_rank  # noqa: E402

try:
    import cypari2  # noqa: F401
except ImportError as exc:  # pragma: no cover - exercised only without cypari2
    raise SystemExit(
        "cypari2 is required.  Install via 'uv sync' or 'uv pip install cypari2'."
    ) from exc


# D4 acts on the cyclic quadrilateral (a, b, c, d) via 4 rotations + 4
# reflections.  The orbit always has size <= 8; minima are taken in lex order.
_D4_PERMS: tuple[tuple[int, int, int, int], ...] = (
    (0, 1, 2, 3),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
    (0, 3, 2, 1),
    (1, 0, 3, 2),
    (2, 1, 0, 3),
    (3, 2, 1, 0),
)


def d4_canonical(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    """Lexicographically-smallest D4 image of the cycle (a, b, c, d)."""
    q = (a, b, c, d)
    return min(tuple(q[i] for i in perm) for perm in _D4_PERMS)


def read_near_misses(db_path: str | Path) -> list[dict]:
    """Read all chain_near_misses rows from the database."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT id, run_id, a, b_val AS b, c, d, h3, h4,
               sq3_deficit, sq4_deficit
        FROM chain_near_misses
        ORDER BY sq4_deficit ASC, id ASC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def deduplicate_d4(rows: list[dict]) -> list[dict]:
    """Keep one representative per D4 orbit (smallest sq4_deficit wins)."""
    best: dict[tuple[int, int, int, int], dict] = {}
    for row in rows:
        canon = d4_canonical(row["a"], row["b"], row["c"], row["d"])
        kept = best.get(canon)
        if kept is None or row["sq4_deficit"] < kept["sq4_deficit"]:
            best[canon] = row
    return sorted(best.values(), key=lambda r: (r["sq4_deficit"], r["id"]))


def safe_rank(pari, A: int, B: int) -> tuple[int, int, int, int, float]:
    """Wrap compute_rank with timing; never raises -- returns -2 on failure.

    Returns (rank, lower, upper, sha2_lower, time_s).
    """
    started = time.perf_counter()
    try:
        rank, bounds, sha2_lower, _gens = compute_rank(A, B, pari=pari)
        return rank, bounds[0], bounds[1], sha2_lower, time.perf_counter() - started
    except Exception:  # pragma: no cover - defensive: PARI can blow up
        return -2, -2, -2, -2, time.perf_counter() - started


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--db",
        default="results/chain.db",
        help="Chain SQLite database (default: results/chain.db)",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of samples to probe (default: 50)",
    )
    ap.add_argument(
        "--no-dedup",
        action="store_true",
        help="Skip D4 deduplication and probe every row",
    )
    ap.add_argument(
        "--max-magnitude",
        type=int,
        default=None,
        help="Skip samples where max(a, b, c, d) exceeds this bound "
        "(useful to avoid very long PARI rank computations)",
    )
    ap.add_argument(
        "--out-jsonl",
        default=None,
        help="Optional per-sample JSONL output path",
    )
    args = ap.parse_args()

    rows = read_near_misses(args.db)
    print(f"Loaded {len(rows)} near-miss rows from {args.db}", flush=True)

    if not args.no_dedup:
        rows = deduplicate_d4(rows)
        print(
            f"After D4 deduplication: {len(rows)} distinct chain candidates",
            flush=True,
        )

    if args.max_magnitude is not None:
        before = len(rows)
        rows = [
            r
            for r in rows
            if max(r["a"], r["b"], r["c"], r["d"]) <= args.max_magnitude
        ]
        print(
            f"After max-magnitude<={args.max_magnitude}: "
            f"{len(rows)} samples (dropped {before - len(rows)})",
            flush=True,
        )

    sample = rows[: args.limit]
    print(
        f"Probing {len(sample)} samples (sorted by sq4_deficit asc)",
        flush=True,
    )
    if not sample:
        print("No samples to probe; exiting.")
        return 0

    pari = cypari2.Pari()
    pari.allocatemem(64 * 1024 * 1024)

    print()
    header = (
        f"{'idx':>3}  {'a':>7} {'b':>7} {'c':>7} {'d':>7}  "
        f"{'rk(E_ac)':>9} {'rk(E_bd)':>9}  "
        f"{'sq4_def':>10}  {'t_ac':>5} {'t_bd':>5}"
    )
    print(header)
    print("-" * len(header))

    joint: Counter[tuple[int, int]] = Counter()
    samples_by_class: dict[tuple[int, int], list[dict]] = {}

    out_fh = open(args.out_jsonl, "w", encoding="utf-8") if args.out_jsonl else None

    overall_started = time.perf_counter()
    for i, row in enumerate(sample):
        a, b, c, d = row["a"], row["b"], row["c"], row["d"]
        rk_ac, lo_ac, hi_ac, sha_ac, t_ac = safe_rank(pari, a, c)
        rk_bd, lo_bd, hi_bd, sha_bd, t_bd = safe_rank(pari, b, d)

        joint[(rk_ac, rk_bd)] += 1
        samples_by_class.setdefault((rk_ac, rk_bd), []).append(row)

        print(
            f"{i:>3}  {a:>7} {b:>7} {c:>7} {d:>7}  "
            f"{rk_ac:>9} {rk_bd:>9}  "
            f"{row['sq4_deficit']:>10}  {t_ac:>5.2f} {t_bd:>5.2f}",
            flush=True,
        )

        if out_fh is not None:
            out_fh.write(
                json.dumps(
                    {
                        "id": row["id"],
                        "run_id": row["run_id"],
                        "a": a,
                        "b": b,
                        "c": c,
                        "d": d,
                        "rank_ac": rk_ac,
                        "rank_ac_bounds": [lo_ac, hi_ac],
                        "sha2_ac": sha_ac,
                        "rank_bd": rk_bd,
                        "rank_bd_bounds": [lo_bd, hi_bd],
                        "sha2_bd": sha_bd,
                        "sq3_deficit": row["sq3_deficit"],
                        "sq4_deficit": row["sq4_deficit"],
                        "time_ac_s": round(t_ac, 4),
                        "time_bd_s": round(t_bd, 4),
                    }
                )
                + "\n"
            )

    elapsed = time.perf_counter() - overall_started
    if out_fh is not None:
        out_fh.close()

    total = sum(joint.values())
    print()
    print("=" * 72)
    print("Joint rank distribution (rank_ac, rank_bd) -> count")
    print("-" * 72)
    for key in sorted(joint):
        rk_ac, rk_bd = key
        count = joint[key]
        pct = 100 * count / total
        print(f"  rank_ac={rk_ac:>2}, rank_bd={rk_bd:>2}: {count:>4}  ({pct:>5.1f}%)")

    bd_zero = sum(n for (_r1, r2), n in joint.items() if r2 == 0)
    bd_one = sum(n for (_r1, r2), n in joint.items() if r2 == 1)
    bd_zero_pct = 100 * bd_zero / total if total else 0.0
    bd_one_pct = 100 * bd_one / total if total else 0.0

    print()
    print(
        f"Dual E_bd rank=0:   {bd_zero:>4}/{total}  ({bd_zero_pct:.1f}%) "
        "<-- free obstruction candidates"
    )
    print(f"Dual E_bd rank=1:   {bd_one:>4}/{total}  ({bd_one_pct:.1f}%)")
    print(
        f"Total runtime:      {elapsed:.1f}s "
        f"({(elapsed / total if total else 0.0):.2f}s per sample)"
    )

    if bd_zero > 0:
        print()
        print("E_bd rank=0 samples (potential obstructions):")
        for key in sorted(samples_by_class):
            if key[1] != 0:
                continue
            for row in samples_by_class[key][:10]:
                a, b, c, d = row["a"], row["b"], row["c"], row["d"]
                bd = b * d
                a2 = a * a
                marker = "  <-- a^2 == bd (still possible)" if a2 == bd else ""
                print(
                    f"  (a,b,c,d)=({a},{b},{c},{d})  "
                    f"a^2={a2}  bd={bd}{marker}"
                )

    return 0


if __name__ == "__main__":
    sys.exit(main())
