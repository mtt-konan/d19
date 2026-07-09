#!/usr/bin/env python3
"""Re-check unproven rank=0 candidates from probe_dual_ec.py with deeper PARI.

Reads the JSONL produced by probe_dual_ec.py, picks all rows where either
rank_ac_bounds or rank_bd_bounds has lower=0 but upper>0 (i.e. rank=0 is
plausible but not certified), then re-runs:

  1.  ellrank(E, 4)            -- effort=4 deeper 2-descent
  2.  ellanalyticrank(E)       -- analytic rank (Sha-conditional)

Output: per-candidate certification status.

Usage:
    uv run python scripts/deep_rank_recheck.py results/dual_ec_probe.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

try:
    import cypari2
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "cypari2 is required.  Install via 'uv sync' or 'uv pip install cypari2'."
    ) from exc


def deep_rank(pari, A: int, B: int, effort: int = 4,
              include_analytic: bool = False) -> dict:
    """Run deeper PARI rank machinery on E: Y^2=X(X+A^2)(X+B^2).

    WARNING: ``include_analytic=True`` invokes ``ellanalyticrank`` which can
    take hours per curve at large conductor (empirically 906s ~ 6929s on
    moderate-sized chain candidates).  Keep it off unless you have a budget.
    """
    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")

    t0 = time.perf_counter()
    rr = pari.ellrank(E, effort)
    t_rank = time.perf_counter() - t0

    ana_rank: int | None = None
    ana_err: str | None = None
    t_ana = 0.0
    if include_analytic:
        t0 = time.perf_counter()
        try:
            ana = pari.ellanalyticrank(E)
            ana_rank = int(ana[0])
        except Exception as exc:  # pragma: no cover - defensive
            ana_err = str(exc)
        t_ana = time.perf_counter() - t0

    return {
        "rank_lower": int(rr[0]),
        "rank_upper": int(rr[1]),
        "analytic_rank": ana_rank,
        "analytic_error": ana_err,
        "time_rank_s": round(t_rank, 3),
        "time_ana_s": round(t_ana, 3),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("jsonl", help="Probe JSONL produced by probe_dual_ec.py")
    ap.add_argument(
        "--effort",
        type=int,
        default=2,
        help="PARI ellrank effort parameter (default: 2; 4 is much slower)",
    )
    ap.add_argument(
        "--max-magnitude",
        type=int,
        default=2_000_000,
        help="Skip candidates where max(A, B) exceeds this (default: 2_000_000 "
        "to keep total runtime under a few minutes; pass 0 for no limit)",
    )
    ap.add_argument(
        "--analytic-rank",
        action="store_true",
        help="Also compute ellanalyticrank (WARNING: can take 15min~2h per "
        "curve at moderate conductor; default OFF)",
    )
    ap.add_argument(
        "--out",
        default=None,
        help="Optional JSON output of the deep recheck results",
    )
    args = ap.parse_args()

    path = Path(args.jsonl)
    rows = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    candidates = []
    for r in rows:
        ac_lo, ac_hi = r["rank_ac_bounds"]
        bd_lo, bd_hi = r["rank_bd_bounds"]
        ac_unproven_zero = ac_lo == 0 and ac_hi > 0
        bd_unproven_zero = bd_lo == 0 and bd_hi > 0
        if ac_unproven_zero or bd_unproven_zero:
            candidates.append((r, ac_unproven_zero, bd_unproven_zero))

    print(
        f"Loaded {len(rows)} rows; {len(candidates)} have unproven rank=0 "
        f"on at least one diagonal."
    )

    if args.max_magnitude > 0:
        before = len(candidates)
        kept = []
        for r, ac_un, bd_un in candidates:
            if ac_un and max(r["a"], r["c"]) > args.max_magnitude:
                ac_un = False
            if bd_un and max(r["b"], r["d"]) > args.max_magnitude:
                bd_un = False
            if ac_un or bd_un:
                kept.append((r, ac_un, bd_un))
        candidates = kept
        dropped = before - len(candidates)
        print(
            f"After max-magnitude<={args.max_magnitude}: "
            f"{len(candidates)} candidates (dropped {dropped})."
        )

    # Sort by max magnitude ascending so the easy ones run first
    def _magnitude(item):
        r, ac_un, bd_un = item
        mags = []
        if ac_un:
            mags.append(max(r["a"], r["c"]))
        if bd_un:
            mags.append(max(r["b"], r["d"]))
        return min(mags) if mags else 0

    candidates.sort(key=_magnitude)

    if not candidates:
        print("Nothing to recheck.")
        return 0

    pari = cypari2.Pari()
    pari.allocatemem(128 * 1024 * 1024)

    deep_results = []
    print()
    if args.analytic_rank:
        print(
            f"{'id':>4} {'side':<3} {'A':>11} {'B':>11}  "
            f"{'old':<8} {'deep[lo,hi]':<11}  {'ana_r':<5}  "
            f"{'t_rank':>6} {'t_ana':>6}  status"
        )
    else:
        print(
            f"{'id':>4} {'side':<3} {'A':>11} {'B':>11}  "
            f"{'old':<8} {'deep[lo,hi]':<11}  {'t_rank':>6}  status"
        )
    print("-" * 100)

    for r, ac_un, bd_un in candidates:
        for which, A, B in (
            ("ac", r["a"], r["c"]) if ac_un else (None, None, None),
            ("bd", r["b"], r["d"]) if bd_un else (None, None, None),
        ):
            if which is None:
                continue
            old_lo, old_hi = r[f"rank_{which}_bounds"]
            deep = deep_rank(pari, A, B, args.effort,
                             include_analytic=args.analytic_rank)
            lo, hi = deep["rank_lower"], deep["rank_upper"]

            if lo == hi == 0:
                status = "CERTIFIED rank=0"
            elif lo == hi:
                status = f"CERTIFIED rank={lo}"
            elif lo > old_lo or hi < old_hi:
                status = f"tighter [{lo},{hi}]"
            else:
                status = f"still [{lo},{hi}]"

            if args.analytic_rank:
                ana_str = (
                    str(deep["analytic_rank"])
                    if deep["analytic_rank"] is not None
                    else "ERR"
                )
                print(
                    f"{r['id']:>4} {which:<3} {A:>11} {B:>11}  "
                    f"[{old_lo},{old_hi}]    [{lo},{hi}]        {ana_str:<5}  "
                    f"{deep['time_rank_s']:>6.2f} {deep['time_ana_s']:>6.2f}  "
                    f"{status}",
                    flush=True,
                )
            else:
                print(
                    f"{r['id']:>4} {which:<3} {A:>11} {B:>11}  "
                    f"[{old_lo},{old_hi}]    [{lo},{hi}]        "
                    f"{deep['time_rank_s']:>6.2f}  {status}",
                    flush=True,
                )

            deep_results.append(
                {
                    "id": r["id"],
                    "side": which,
                    "A": A,
                    "B": B,
                    "abcd": [r["a"], r["b"], r["c"], r["d"]],
                    "old_bounds": [old_lo, old_hi],
                    "deep": deep,
                    "status": status,
                }
            )

    if args.out:
        Path(args.out).write_text(json.dumps(deep_results, indent=2))
        print()
        print(f"Saved deep recheck to {args.out}")

    print()
    print("=" * 72)
    n_certified_zero = sum(1 for d in deep_results if d["status"] == "CERTIFIED rank=0")
    n_certified_pos = sum(1 for d in deep_results if d["status"].startswith("CERTIFIED rank=") and d["status"] != "CERTIFIED rank=0")
    n_tighter = sum(1 for d in deep_results if d["status"].startswith("tighter"))
    n_unchanged = sum(1 for d in deep_results if d["status"].startswith("still"))
    print(f"CERTIFIED rank=0 :  {n_certified_zero}")
    print(f"CERTIFIED rank>0 :  {n_certified_pos}")
    print(f"Tighter bounds   :  {n_tighter}")
    print(f"Unchanged        :  {n_unchanged}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
