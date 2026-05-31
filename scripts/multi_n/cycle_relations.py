#!/usr/bin/env python3
"""Cycle linear-relation tracker CLI (wl086, OPEN_DIRECTIONS A.2 / E.3).

For each multi-N pair ``(A, B)`` it expresses the concordant points ``Q_{N_i}``
as integer combinations of the Mordell-Weil generators (modulo torsion) and
extracts a basis of the integer relation lattice, verifying every relation
exactly with PARI point arithmetic.

It also records, per point, whether ``Q_N`` is divisible by 2 in ``E(Q)``
(PARI ``ellisdivisible``) -- the structural fact that explains the relations.

Usage:
    uv run python scripts/multi_n/cycle_relations.py --pairs 420,1344 264,420
    uv run python scripts/multi_n/cycle_relations.py \\
        --catalog results/partner/cycle_ellrank_wl058_6cycle.jsonl \\
        --out results/multi_n/cycle_relations_wl058.jsonl

When a catalog row carries a ``concordant_N`` list it is used directly (no
search).  Otherwise N are found via ``ellratpoints`` up to ``--ec-bound``
(keep this small to avoid long runs).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.analysis import _ensure_pari  # noqa: E402
from rational_distance.concordant.cycle_relations import (  # noqa: E402
    CycleRelationResult,
    analyze_cycle_relations,
)


def _parse_pairs(values: list[str]) -> list[tuple[int, int, list[int] | None]]:
    out: list[tuple[int, int, list[int] | None]] = []
    for v in values:
        a, b = v.split(",")
        out.append((int(a), int(b), None))
    return out


def _load_catalog(path: Path) -> list[tuple[int, int, list[int] | None]]:
    out: list[tuple[int, int, list[int] | None]] = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            a = row.get("A") or row.get("a")
            b = row.get("B") or row.get("b")
            if a is None or b is None:
                continue
            ns = row.get("concordant_N")
            out.append((int(a), int(b), [int(n) for n in ns] if ns else None))
    return out


def _result_to_dict(res: CycleRelationResult) -> dict:
    return {
        "A": res.A,
        "B": res.B,
        "k": res.k,
        "rank": res.rank,
        "rank_bounds": list(res.rank_bounds) if res.rank_bounds else None,
        "k_minus_rank": res.k_minus_rank,
        "coord_matrix_rank": res.coord_matrix_rank,
        "concordant_N": res.concordant_n,
        "relation_count": res.relation_count,
        "all_two_divisible": res.all_two_divisible,
        "all_verified": res.all_verified,
        "skipped_reason": res.skipped_reason,
        "point_coords": [
            {
                "N": p.N,
                "coords": list(p.coords),
                "torsion_order": p.torsion_order,
                "two_divisible": p.two_divisible,
                "verified": p.verified,
            }
            for p in res.point_coords
        ],
        "relations": [
            {
                "coeffs": list(r.coeffs),
                "residual_torsion_order": r.residual_torsion_order,
                "verified": r.verified,
            }
            for r in res.relations
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", nargs="*", default=[], help="explicit pairs A,B")
    parser.add_argument(
        "--catalog", type=Path, help="JSONL catalog with A/B (+ optional concordant_N)"
    )
    parser.add_argument("--max-pairs", type=int, default=None, help="limit number of catalog pairs")
    parser.add_argument("--effort", type=int, default=1, help="PARI ellrank effort")
    parser.add_argument(
        "--ec-bound", type=int, default=100000, help="ellratpoints bound when N unknown"
    )
    parser.add_argument("--out", type=Path, help="write JSONL results here")
    parser.add_argument("--quiet", action="store_true", help="suppress per-pair summary")
    args = parser.parse_args()

    pairs = _parse_pairs(args.pairs)
    if args.catalog:
        pairs.extend(_load_catalog(args.catalog))
    if args.max_pairs is not None:
        pairs = pairs[: args.max_pairs]
    if not pairs:
        parser.error("provide --pairs and/or --catalog")

    pari = _ensure_pari()
    results: list[CycleRelationResult] = []

    n_pairs = 0
    n_all_two_div = 0
    n_all_verified = 0
    total_relations = 0
    deficit_explained = 0  # pairs where #relations == k - coord_matrix_rank
    for A, B, ns in pairs:
        res = analyze_cycle_relations(
            A, B, ns, pari=pari, effort=args.effort, ec_bound=args.ec_bound
        )
        results.append(res)
        n_pairs += 1
        if res.skipped_reason is None:
            if res.all_two_divisible:
                n_all_two_div += 1
            if res.all_verified:
                n_all_verified += 1
            total_relations += res.relation_count
            if res.coord_matrix_rank is not None:
                expected = res.k - res.coord_matrix_rank
                if res.relation_count == expected:
                    deficit_explained += 1
        if not args.quiet:
            print(res.summary())

    if args.out:
        with open(args.out, "w") as out_f:
            for res in results:
                out_f.write(json.dumps(_result_to_dict(res)) + "\n")

    print("\n=== summary ===")
    print(f"pairs analyzed:                 {n_pairs}")
    print(f"all Q_N divisible by 2 in E(Q): {n_all_two_div}/{n_pairs}")
    print(f"all relations verified exactly: {n_all_verified}/{n_pairs}")
    print(f"relations found (total):        {total_relations}")
    print(f"#relations == k - coord_rank:   {deficit_explained}/{n_pairs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
