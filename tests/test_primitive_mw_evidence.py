"""Tests for compact MW evidence rows behind D-scaling."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_mw_evidence import (  # noqa: E402
    evidence_rows_for_vertex,
    select_representative_vertices,
    summarize_evidence_rows,
)


class FakePointCoord:
    def __init__(
        self,
        *,
        N: int,
        coords: tuple[int, ...],
        torsion_order: int,
        two_divisible: bool,
        verified: bool,
    ) -> None:
        self.N = N
        self.coords = coords
        self.torsion_order = torsion_order
        self.two_divisible = two_divisible
        self.verified = verified


class FakeMwResult:
    rank = 2
    rank_bounds = (2, 2)
    coord_matrix_rank = 2
    all_verified = True
    generators = [("1", "2"), ("3", "4")]
    point_coords = [
        FakePointCoord(
            N=6,
            coords=(1, 0),
            torsion_order=1,
            two_divisible=True,
            verified=True,
        ),
        FakePointCoord(
            N=10,
            coords=(-1, 2),
            torsion_order=4,
            two_divisible=False,
            verified=True,
        ),
    ]


def test_select_representative_vertices_prefers_high_k_then_small_coordinates() -> None:
    exact_ns = {
        (10, 14): [1, 2],
        (20, 28): [1, 2, 3],
        (30, 42): [1, 2, 3],
    }

    reps = select_representative_vertices([(30, 42), (10, 14), (20, 28)], exact_ns, limit=2)

    assert reps == [(20, 28), (30, 42)]


def test_evidence_rows_for_vertex_records_scaling_and_mw_coordinates() -> None:
    rows = evidence_rows_for_vertex(
        primitive=(5, 7),
        vertex=(10, 14),
        exact_ns=[6, 10],
        pool_ns=[Fraction(3, 1), Fraction(5, 1)],
        mw_result=FakeMwResult(),
        source="global",
        incident_edges=12,
    )

    assert rows == [
        {
            "primitive": [5, 7],
            "a": 10,
            "b": 14,
            "d": 2,
            "source": "global",
            "incident_edges": 12,
            "exact_k": 2,
            "N": 6,
            "rational_n": "3",
            "rational_n_numerator": 3,
            "rational_n_denominator": 1,
            "pool_contains_rational_n": True,
            "mw_rank": 2,
            "mw_rank_bounds": [2, 2],
            "mw_coord_matrix_rank": 2,
            "mw_all_verified": True,
            "mw_coords": [1, 0],
            "torsion_order": 1,
            "two_divisible": True,
            "point_verified": True,
            "generator_count": 2,
        },
        {
            "primitive": [5, 7],
            "a": 10,
            "b": 14,
            "d": 2,
            "source": "global",
            "incident_edges": 12,
            "exact_k": 2,
            "N": 10,
            "rational_n": "5",
            "rational_n_numerator": 5,
            "rational_n_denominator": 1,
            "pool_contains_rational_n": True,
            "mw_rank": 2,
            "mw_rank_bounds": [2, 2],
            "mw_coord_matrix_rank": 2,
            "mw_all_verified": True,
            "mw_coords": [-1, 2],
            "torsion_order": 4,
            "two_divisible": False,
            "point_verified": True,
            "generator_count": 2,
        },
    ]


def test_summarize_evidence_rows_counts_unverified_primitives() -> None:
    rows = [
        {
            "primitive": [5, 7],
            "pool_contains_rational_n": True,
            "point_verified": True,
            "mw_all_verified": True,
            "two_divisible": True,
            "mw_coords": [2, 0],
            "rational_n_denominator": 3,
        },
        {
            "primitive": [11, 13],
            "pool_contains_rational_n": True,
            "point_verified": False,
            "mw_all_verified": False,
            "two_divisible": True,
            "mw_coords": [1, -1],
            "rational_n_denominator": 5,
        },
    ]

    summary = summarize_evidence_rows(rows)

    assert summary == {
        "evidence_rows": 2,
        "pool_hit_rows": 2,
        "pool_hit_pct": 100.0,
        "point_verified_rows": 1,
        "point_verified_pct": 50.0,
        "mw_all_verified_rows": 1,
        "mw_all_verified_pct": 50.0,
        "two_divisible_rows": 2,
        "two_divisible_pct": 100.0,
        "max_abs_mw_coord": 2,
        "max_rational_n_denominator": 5,
        "unverified_primitives": [[11, 13]],
    }
