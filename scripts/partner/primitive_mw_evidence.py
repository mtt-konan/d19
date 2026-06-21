#!/usr/bin/env python3
"""Emit compact MW-coordinate evidence rows for D-scaling primitives."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.partner.primitive_scaling_audit import (  # noqa: E402
    group_vertices_by_primitive,
    iter_component_vertices,
    load_rank_audit_primitives,
)

Pair = tuple[int, int]


def select_representative_vertices(
    vertices: Iterable[Pair],
    exact_ns: dict[Pair, list[int]],
    *,
    limit: int,
) -> list[Pair]:
    """Pick representative scaled vertices by highest exact k, then smaller size."""
    return sorted(
        vertices,
        key=lambda pair: (-len(exact_ns[pair]), max(pair), sum(pair), pair),
    )[:limit]


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def evidence_rows_for_vertex(
    *,
    primitive: Pair,
    vertex: Pair,
    exact_ns: list[int],
    pool_ns: Iterable[Fraction],
    mw_result: Any,
    source: str | None = None,
    incident_edges: int | None = None,
) -> list[dict[str, object]]:
    """Return one compact evidence row per exact N on a scaled vertex."""
    d = gcd(*vertex)
    pool_set = set(pool_ns)
    point_by_n = {int(point.N): point for point in mw_result.point_coords}
    rows: list[dict[str, object]] = []
    for N in sorted(exact_ns):
        rational_n = Fraction(N, d)
        point = point_by_n[N]
        row: dict[str, object] = {
            "primitive": list(primitive),
            "a": vertex[0],
            "b": vertex[1],
            "d": d,
            "source": source,
            "incident_edges": incident_edges,
            "exact_k": len(exact_ns),
            "N": N,
            "rational_n": _fraction_text(rational_n),
            "rational_n_numerator": rational_n.numerator,
            "rational_n_denominator": rational_n.denominator,
            "pool_contains_rational_n": rational_n in pool_set,
            "mw_rank": mw_result.rank,
            "mw_rank_bounds": list(mw_result.rank_bounds)
            if mw_result.rank_bounds is not None
            else None,
            "mw_coord_matrix_rank": mw_result.coord_matrix_rank,
            "mw_all_verified": mw_result.all_verified,
            "mw_coords": list(point.coords),
            "torsion_order": point.torsion_order,
            "two_divisible": point.two_divisible,
            "point_verified": point.verified,
            "generator_count": len(mw_result.generators),
        }
        rows.append({key: value for key, value in row.items() if value is not None})
    return rows


def _pct(part: int, whole: int) -> float:
    if whole == 0:
        return 0.0
    return round(100 * part / whole, 2)


def summarize_evidence_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    """Summarize pool/scaling and MW-coordinate verification separately."""
    total = len(rows)
    pool_hits = sum(1 for row in rows if bool(row["pool_contains_rational_n"]))
    point_verified = sum(1 for row in rows if bool(row["point_verified"]))
    mw_all_verified = sum(1 for row in rows if bool(row["mw_all_verified"]))
    two_divisible = sum(1 for row in rows if bool(row["two_divisible"]))
    unverified = sorted(
        {
            tuple(int(x) for x in row["primitive"])
            for row in rows
            if not bool(row["point_verified"])
        }
    )
    max_abs_coord = 0
    for row in rows:
        coords = row.get("mw_coords", [])
        if isinstance(coords, list) and coords:
            max_abs_coord = max(max_abs_coord, max(abs(int(c)) for c in coords))
    return {
        "evidence_rows": total,
        "pool_hit_rows": pool_hits,
        "pool_hit_pct": _pct(pool_hits, total),
        "point_verified_rows": point_verified,
        "point_verified_pct": _pct(point_verified, total),
        "mw_all_verified_rows": mw_all_verified,
        "mw_all_verified_pct": _pct(mw_all_verified, total),
        "two_divisible_rows": two_divisible,
        "two_divisible_pct": _pct(two_divisible, total),
        "max_abs_mw_coord": max_abs_coord,
        "max_rational_n_denominator": max(
            (int(row["rational_n_denominator"]) for row in rows),
            default=0,
        ),
        "unverified_primitives": [list(pair) for pair in unverified],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--rank-audit",
        type=Path,
        default=Path("results/partner/primitive_rank_audit_top.jsonl"),
    )
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner/primitive_mw_evidence_top.jsonl"),
    )
    _ = parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner/primitive_mw_evidence_top_summary.json"),
    )
    _ = parser.add_argument("--limit-primitives", type=int, default=6)
    _ = parser.add_argument("--vertices-per-primitive", type=int, default=1)
    _ = parser.add_argument("--max-depth", type=int, default=50)
    _ = parser.add_argument("--ratpoints-bound", type=int, default=200_000)
    _ = parser.add_argument("--rank-combo-bound", type=int, default=5)
    _ = parser.add_argument("--effort", type=int, default=1)
    return parser.parse_args()


def main() -> int:
    from rational_distance.concordant.cycle_relations import mw_coordinates
    from rational_distance.concordant.dscale_kn import enumerate_rational_n
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    args = parse_args()
    selected = load_rank_audit_primitives(args.rank_audit, limit=args.limit_primitives)
    vertices_by_primitive = group_vertices_by_primitive(
        iter_component_vertices(args.components)
    )

    all_rows: list[dict[str, object]] = []
    primitive_summaries: list[dict[str, object]] = []
    for meta in selected:
        primitive = meta["primitive"]
        if not isinstance(primitive, tuple):
            raise TypeError("primitive metadata must contain a tuple")
        vertices = sorted(vertices_by_primitive.get(primitive, []))
        exact_by_vertex = {
            vertex: exact_concordant_pair(*vertex)
            for vertex in vertices
        }
        reps = select_representative_vertices(
            vertices,
            exact_by_vertex,
            limit=args.vertices_per_primitive,
        )
        pool = enumerate_rational_n(
            primitive[0],
            primitive[1],
            max_depth=args.max_depth,
            ratpoints_bound=args.ratpoints_bound,
            rank_combo_bound=args.rank_combo_bound,
            effort=args.effort,
        )
        before_count = len(all_rows)
        for vertex in reps:
            mw_result = mw_coordinates(
                vertex[0],
                vertex[1],
                exact_by_vertex[vertex],
                effort=args.effort,
            )
            all_rows.extend(
                evidence_rows_for_vertex(
                    primitive=primitive,
                    vertex=vertex,
                    exact_ns=exact_by_vertex[vertex],
                    pool_ns=pool.rational_ns,
                    mw_result=mw_result,
                    source=str(meta.get("source")) if meta.get("source") else None,
                    incident_edges=int(meta["incident_edges"])
                    if "incident_edges" in meta
                    else None,
                )
            )
        primitive_summaries.append(
            {
                "primitive": list(primitive),
                "source": meta.get("source"),
                "rank_lower": meta.get("rank_lower"),
                "rank_upper": meta.get("rank_upper"),
                "representative_vertices": [list(vertex) for vertex in reps],
                "evidence_rows": len(all_rows) - before_count,
                "pool_size": pool.n_count,
                "denominator_count": len(pool.denominators),
            }
        )

    summary = {
        "primitive_count": len(selected),
        "vertices_per_primitive": args.vertices_per_primitive,
        "primitives": primitive_summaries,
    }
    summary.update(summarize_evidence_rows(all_rows))
    summary["all_pool_hits"] = summary["pool_hit_rows"] == summary["evidence_rows"]
    summary["all_mw_verified"] = (
        summary["point_verified_rows"] == summary["evidence_rows"]
    )
    summary["all_two_divisible"] = (
        summary["two_divisible_rows"] == summary["evidence_rows"]
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        for row in all_rows:
            _ = f.write(json.dumps(row, ensure_ascii=False) + "\n")
    args.summary_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
