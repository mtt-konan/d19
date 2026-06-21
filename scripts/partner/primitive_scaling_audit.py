#!/usr/bin/env python3
"""Compare D-scaling rational-n predictions against real G_M vertices."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

Pair = tuple[int, int]


def compare_scaled_vertices(
    *,
    primitive: Pair,
    vertices: Iterable[Pair],
    rational_ns: Iterable[Fraction],
    exact_ns: dict[Pair, list[int]],
) -> list[dict[str, object]]:
    """Compare exact integer k with the lower-bound k from rational n pool."""
    from rational_distance.concordant.dscale_kn import k_for_d

    a0, b0 = primitive
    rows: list[dict[str, object]] = []
    for a, b in sorted(vertices):
        d = gcd(a, b)
        if (a // d, b // d) != (a0, b0):
            continue
        pool_ns = k_for_d(rational_ns, d)
        pool_k = len(pool_ns)
        ns = sorted(exact_ns[(a, b)])
        k = len(ns)
        rows.append(
            {
                "a": a,
                "b": b,
                "d": d,
                "exact_k": k,
                "pool_k": pool_k,
                "pool_covers_exact": pool_k >= k,
                "pool_matches_exact_set": pool_ns == ns,
                "missing_k": max(0, k - pool_k),
            }
        )
    return rows


def iter_component_vertices(path: Path) -> Iterable[Pair]:
    with path.open() as f:
        for line in f:
            component = json.loads(line)
            for vertex in component["vertices"]:
                yield int(vertex[0]), int(vertex[1])


def primitive_of(pair: Pair) -> Pair:
    d = gcd(pair[0], pair[1])
    return pair[0] // d, pair[1] // d


def group_vertices_by_primitive(vertices: Iterable[Pair]) -> dict[Pair, list[Pair]]:
    grouped: dict[Pair, list[Pair]] = {}
    for pair in vertices:
        grouped.setdefault(primitive_of(pair), []).append(pair)
    return grouped


def load_rank_audit_primitives(path: Path, *, limit: int | None = None) -> list[dict[str, Any]]:
    """Load compact primitive metadata from primitive_rank_audit.py JSONL output."""
    selected: list[dict[str, Any]] = []
    with path.open() as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            compact = {
                "primitive": (int(row["primitive_a"]), int(row["primitive_b"])),
                "source": row.get("source"),
                "incident_edges": row.get("incident_edges"),
                "rank_lower": row.get("rank_lower"),
                "rank_upper": row.get("rank_upper"),
                "rank_certified": row.get("rank_certified"),
                "rational_n_pool_size": row.get("rational_n_pool_size"),
                "denominator_count": row.get("denominator_count"),
            }
            selected.append({key: value for key, value in compact.items() if value is not None})
            if limit is not None and len(selected) >= limit:
                break
    return selected


def summarize_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        return {
            "scaled_vertices": 0,
            "covered_vertices": 0,
            "coverage_pct": 0.0,
            "max_exact_k": 0,
            "max_pool_k": 0,
        }
    covered = sum(1 for row in rows if bool(row["pool_covers_exact"]))
    matched = sum(1 for row in rows if bool(row.get("pool_matches_exact_set")))
    return {
        "scaled_vertices": len(rows),
        "covered_vertices": covered,
        "coverage_pct": round(100 * covered / len(rows), 2),
        "exact_set_matched_vertices": matched,
        "exact_set_match_pct": round(100 * matched / len(rows), 2),
        "max_exact_k": max(int(row["exact_k"]) for row in rows),
        "max_pool_k": max(int(row["pool_k"]) for row in rows),
        "total_missing_k": sum(int(row["missing_k"]) for row in rows),
    }


def summarize_batch(rows: list[dict[str, object]]) -> dict[str, object]:
    total_vertices = sum(int(row["scaled_vertices"]) for row in rows)
    total_covered = sum(int(row["covered_vertices"]) for row in rows)
    total_matched = sum(int(row.get("exact_set_matched_vertices", 0)) for row in rows)
    return {
        "audited_primitives": len(rows),
        "total_scaled_vertices": total_vertices,
        "total_covered_vertices": total_covered,
        "overall_coverage_pct": round(100 * total_covered / total_vertices, 2)
        if total_vertices
        else 0.0,
        "total_exact_set_matched_vertices": total_matched,
        "overall_exact_set_match_pct": round(100 * total_matched / total_vertices, 2)
        if total_vertices
        else 0.0,
        "max_exact_k": max((int(row["max_exact_k"]) for row in rows), default=0),
        "max_pool_k": max((int(row["max_pool_k"]) for row in rows), default=0),
        "total_missing_k": sum(int(row["total_missing_k"]) for row in rows),
    }


def audit_one_primitive(
    *,
    primitive: Pair,
    scaled_vertices: Iterable[Pair],
    max_depth: int,
    ratpoints_bound: int,
    rank_combo_bound: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    from rational_distance.concordant.dscale_kn import enumerate_rational_n
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    vertices = sorted(scaled_vertices)
    pool = enumerate_rational_n(
        primitive[0],
        primitive[1],
        max_depth=max_depth,
        ratpoints_bound=ratpoints_bound,
        rank_combo_bound=rank_combo_bound,
    )
    exact_ns = {pair: exact_concordant_pair(*pair) for pair in vertices}
    rows = compare_scaled_vertices(
        primitive=primitive,
        vertices=vertices,
        rational_ns=pool.rational_ns,
        exact_ns=exact_ns,
    )
    summary = summarize_rows(rows)
    summary.update(
        {
            "primitive": list(primitive),
            "rank_lower": pool.rank_lower,
            "rank_upper": pool.rank_upper,
            "rational_n_pool_size": pool.n_count,
            "denominator_count": len(pool.denominators),
        }
    )
    return rows, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    _ = source.add_argument("--primitive", help="primitive a,b")
    _ = source.add_argument("--rank-audit", type=Path, help="primitive_rank_audit.py JSONL")
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner/primitive_scaling_audit.jsonl"),
    )
    _ = parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner/primitive_scaling_audit_summary.json"),
    )
    _ = parser.add_argument("--max-depth", type=int, default=50)
    _ = parser.add_argument("--ratpoints-bound", type=int, default=200_000)
    _ = parser.add_argument("--rank-combo-bound", type=int, default=5)
    _ = parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vertices_by_primitive = group_vertices_by_primitive(
        iter_component_vertices(args.components)
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.primitive:
        a0_s, b0_s = str(args.primitive).split(",", 1)
        primitive = (int(a0_s), int(b0_s))
        rows, summary = audit_one_primitive(
            primitive=primitive,
            scaled_vertices=vertices_by_primitive.get(primitive, []),
            max_depth=int(args.max_depth),
            ratpoints_bound=int(args.ratpoints_bound),
            rank_combo_bound=int(args.rank_combo_bound),
        )
        summary["components"] = str(args.components)
        with args.out.open("w") as f:
            for row in rows:
                _ = f.write(json.dumps(row, ensure_ascii=False) + "\n")
        args.summary_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    selected = load_rank_audit_primitives(args.rank_audit, limit=args.limit)
    summaries: list[dict[str, object]] = []
    with args.out.open("w") as f:
        for meta in selected:
            primitive = meta["primitive"]
            if not isinstance(primitive, tuple):
                raise TypeError("primitive metadata must contain a tuple")
            _rows, summary = audit_one_primitive(
                primitive=primitive,
                scaled_vertices=vertices_by_primitive.get(primitive, []),
                max_depth=int(args.max_depth),
                ratpoints_bound=int(args.ratpoints_bound),
                rank_combo_bound=int(args.rank_combo_bound),
            )
            for key, value in meta.items():
                if key != "primitive" and value is not None:
                    summary[key] = value
            summaries.append(summary)
            _ = f.write(json.dumps(summary, ensure_ascii=False) + "\n")
    batch_summary = summarize_batch(summaries)
    batch_summary.update(
        {
            "rank_audit": str(args.rank_audit),
            "components": str(args.components),
            "limit": args.limit,
        }
    )
    args.summary_out.write_text(json.dumps(batch_summary, indent=2, ensure_ascii=False))
    print(json.dumps(batch_summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
