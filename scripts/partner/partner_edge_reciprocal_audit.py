#!/usr/bin/env python3
"""Audit partner-graph edges against the R_lambda translation target.

Each row in ``partner_full_bfs_edges.jsonl`` is an undirected edge between two
multi-N pairs ``u=(A,B)`` and ``v=(N_i,N_j)``.  The correct empirical check for
the translation / reciprocal theorem is:

    use the two concordant values ``N_i, N_j`` from the edge data,
    not a constructed mate ``lambda/r``.

For every valid orientation ``(A,B) -- (N_i,N_j)`` we record:

1. both ``N_i/B`` and ``N_j/B`` lie in ``R_lambda``;
2. whether any full-plane closure relation holds;
3. if closure holds with both true members, whether ``N_i * N_j == A * B``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from rational_distance.concordant.rational_ratio import (  # noqa: E402
    REL_DIFF_AB,
    REL_DIFF_DIFF,
    REL_SUM_AB,
    REL_SUM_DIFF,
    full_plane_true_closure_relation,
    is_rational_ratio_member,
    reciprocal_ratio,
)

FULL_PLANE_RELATIONS = (
    REL_SUM_AB,
    REL_SUM_DIFF,
    REL_DIFF_AB,
    REL_DIFF_DIFF,
)

Pair = tuple[int, int]
Quartet = tuple[int, int, int, int]


@dataclass(frozen=True)
class PartnerEdgeOrientation:
    """One audit orientation extracted from a partner-graph edge."""

    a: int
    b: int
    n_i: int
    n_j: int
    lambda_ratio: Fraction
    r_i: Fraction
    r_j: Fraction
    r_i_member: bool
    r_j_member: bool
    both_members: bool
    reciprocal: bool
    constructed_reciprocal: Fraction
    uses_data_n_j: bool
    closing_relations: tuple[str, ...]
    true_reciprocal_relations: tuple[str, ...]
    true_nonreciprocal_relations: tuple[str, ...]
    false_closure_relations: tuple[str, ...]


def _as_pair(value: tuple[int, int] | list[int]) -> Pair:
    a, b = int(value[0]), int(value[1])
    if a <= 0 or b <= 0:
        raise ValueError(f"pair entries must be positive: {value!r}")
    return a, b


def partner_edge_quartets(u: Pair, v: Pair) -> tuple[Quartet, ...]:
    """Return the canonical ``(A,B,N_i,N_j)`` orientation for one edge."""
    left, right = (u, v) if u <= v else (v, u)
    a, b = left
    n_i, n_j = right
    if n_i == n_j:
        return ()
    return ((a, b, n_i, n_j),)


def audit_partner_orientation(a: int, b: int, n_i: int, n_j: int) -> PartnerEdgeOrientation:
    """Audit one oriented partner edge against R_lambda closure branches."""
    lam = Fraction(a, b)
    r_i = Fraction(n_i, b)
    r_j = Fraction(n_j, b)
    constructed = reciprocal_ratio(lam, r_i)

    r_i_member = is_rational_ratio_member(lam, r_i)
    r_j_member = is_rational_ratio_member(lam, r_j)
    both_members = r_i_member and r_j_member
    reciprocal = r_i * r_j == lam

    closing: list[str] = []
    true_reciprocal: list[str] = []
    true_nonreciprocal: list[str] = []
    false_closure: list[str] = []

    for relation in FULL_PLANE_RELATIONS:
        try:
            row = full_plane_true_closure_relation(
                lambda_ratio=lam,
                r=r_i,
                s=r_j,
                relation=relation,
            )
        except ValueError:
            continue
        if not row.closes_relation:
            continue
        closing.append(relation)
        if row.branch == "true-reciprocal":
            true_reciprocal.append(relation)
        elif row.branch == "true-nonreciprocal":
            true_nonreciprocal.append(relation)
        else:
            false_closure.append(relation)

    return PartnerEdgeOrientation(
        a=a,
        b=b,
        n_i=n_i,
        n_j=n_j,
        lambda_ratio=lam,
        r_i=r_i,
        r_j=r_j,
        r_i_member=r_i_member,
        r_j_member=r_j_member,
        both_members=both_members,
        reciprocal=reciprocal,
        constructed_reciprocal=constructed,
        uses_data_n_j=r_j == Fraction(n_j, b),
        closing_relations=tuple(closing),
        true_reciprocal_relations=tuple(true_reciprocal),
        true_nonreciprocal_relations=tuple(true_nonreciprocal),
        false_closure_relations=tuple(false_closure),
    )


def audit_partner_edge_row(row: dict[str, Any]) -> tuple[PartnerEdgeOrientation, ...]:
    """Audit one JSON edge row, deduplicating symmetric orientations."""
    u = _as_pair(row["u"])
    v = _as_pair(row["v"])
    return tuple(
        audit_partner_orientation(a, b, n_i, n_j)
        for a, b, n_i, n_j in partner_edge_quartets(u, v)
    )


def summarize_partner_edge_reciprocal_audit(
    rows: Iterable[dict[str, Any]],
    *,
    limit: int | None = None,
) -> dict[str, Any]:
    """Summarize closure / reciprocal statistics over partner-graph edges."""
    edges_scanned = 0
    orientations = 0
    both_member = 0
    member_miss = 0
    closure_any = 0
    closure_true_reciprocal = 0
    closure_true_nonreciprocal = 0
    closure_false_only = 0
    relation_counts: Counter[str] = Counter()
    branch_examples: dict[str, list[dict[str, Any]]] = {
        "true-nonreciprocal": [],
        "true-reciprocal": [],
    }

    for row in rows:
        if limit is not None and edges_scanned >= limit:
            break
        edges_scanned += 1
        for item in audit_partner_edge_row(row):
            orientations += 1
            if item.both_members:
                both_member += 1
            else:
                member_miss += 1

            if not item.closing_relations:
                continue

            closure_any += 1
            for rel in item.closing_relations:
                relation_counts[rel] += 1

            if item.true_nonreciprocal_relations:
                closure_true_nonreciprocal += 1
                bucket = branch_examples["true-nonreciprocal"]
                if len(bucket) < 10:
                    bucket.append(_orientation_example(item))
            elif item.true_reciprocal_relations:
                closure_true_reciprocal += 1
                bucket = branch_examples["true-reciprocal"]
                if len(bucket) < 10:
                    bucket.append(_orientation_example(item))
            else:
                closure_false_only += 1

    closure_reciprocal_only = closure_true_reciprocal
    return {
        "edges_scanned": edges_scanned,
        "orientations_audited": orientations,
        "both_members": both_member,
        "member_misses": member_miss,
        "closure_any": closure_any,
        "closure_true_reciprocal": closure_true_reciprocal,
        "closure_true_nonreciprocal": closure_true_nonreciprocal,
        "closure_false_only": closure_false_only,
        "closure_reciprocal_only": closure_reciprocal_only,
        "closure_nonreciprocal_among_true_members": closure_true_nonreciprocal,
        "relation_counts": dict(relation_counts),
        "examples": branch_examples,
    }


def _orientation_example(item: PartnerEdgeOrientation) -> dict[str, Any]:
    return {
        "A": item.a,
        "B": item.b,
        "N_i": item.n_i,
        "N_j": item.n_j,
        "lambda": str(item.lambda_ratio),
        "r_i": str(item.r_i),
        "r_j": str(item.r_j),
        "reciprocal": item.reciprocal,
        "closing_relations": list(item.closing_relations),
        "true_reciprocal_relations": list(item.true_reciprocal_relations),
        "true_nonreciprocal_relations": list(item.true_nonreciprocal_relations),
    }


def iter_edge_rows(path: Path) -> Iterable[dict[str, Any]]:
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--edges",
        type=Path,
        default=Path("results/partner/partner_full_bfs_edges.jsonl"),
        help="partner BFS edge file",
    )
    _ = parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="scan at most this many edge rows",
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="optional JSON summary output path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    edges_path: Path = args.edges
    if not edges_path.exists():
        print(f"edge file not found: {edges_path}", file=sys.stderr)
        return 1

    summary = summarize_partner_edge_reciprocal_audit(
        iter_edge_rows(edges_path),
        limit=args.limit,
    )

    print("Partner edge reciprocal audit")
    print(f"  edges scanned:                 {summary['edges_scanned']}")
    print(f"  orientations audited:          {summary['orientations_audited']}")
    print(f"  both R_lambda members:         {summary['both_members']}")
    print(f"  member misses:                 {summary['member_misses']}")
    print(f"  any full-plane closure:        {summary['closure_any']}")
    print(f"  closure + true reciprocal:     {summary['closure_true_reciprocal']}")
    print(f"  closure + true nonreciprocal:  {summary['closure_true_nonreciprocal']}")
    print(f"  closure + false members only:  {summary['closure_false_only']}")
    if summary["relation_counts"]:
        print("  closure relation counts:")
        for relation, count in sorted(summary["relation_counts"].items()):
            print(f"    {relation}: {count}")

    if summary["examples"]["true-nonreciprocal"]:
        print("  examples (true-nonreciprocal):")
        for example in summary["examples"]["true-nonreciprocal"]:
            print(f"    {example}")

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote summary: {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
