"""Tests for checking D-scaling predictions against exact integer k."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_scaling_audit import compare_scaled_vertices  # noqa: E402
from scripts.partner.primitive_scaling_audit import load_rank_audit_primitives  # noqa: E402
from scripts.partner.primitive_scaling_audit import summarize_batch  # noqa: E402


def test_compare_scaled_vertices_reports_pool_lower_bound_and_missing_count() -> None:
    rows = compare_scaled_vertices(
        primitive=(5, 7),
        vertices=[(10, 14), (30, 42)],
        rational_ns=[Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)],
        exact_ns={(10, 14): [1, 2], (30, 42): [3, 6, 7, 18]},
    )

    assert rows == [
        {
            "a": 10,
            "b": 14,
            "d": 2,
            "exact_k": 2,
            "pool_k": 1,
            "pool_covers_exact": False,
            "pool_matches_exact_set": False,
            "missing_k": 1,
        },
        {
            "a": 30,
            "b": 42,
            "d": 6,
            "exact_k": 4,
            "pool_k": 3,
            "pool_covers_exact": False,
            "pool_matches_exact_set": False,
            "missing_k": 1,
        },
    ]


def test_load_rank_audit_primitives_keeps_compact_metadata(tmp_path: Path) -> None:
    path = tmp_path / "rank.jsonl"
    path.write_text(
        "\n".join(
            [
                (
                    '{"primitive_a": 5, "primitive_b": 7, "source": "global", '
                    '"incident_edges": 12, "rank_lower": 2, "rank_upper": 2, '
                    '"rank_certified": true, "rational_n_pool_size": 10, '
                    '"denominator_count": 9, "denominators": [1, 2, 3]}'
                ),
                (
                    '{"primitive_a": 11, "primitive_b": 13, "source": "branch", '
                    '"incident_edges": 3, "rank_lower": 1, "rank_upper": 1}'
                ),
            ]
        )
        + "\n"
    )

    selected = load_rank_audit_primitives(path, limit=2)

    assert selected == [
        {
            "primitive": (5, 7),
            "source": "global",
            "incident_edges": 12,
            "rank_lower": 2,
            "rank_upper": 2,
            "rank_certified": True,
            "rational_n_pool_size": 10,
            "denominator_count": 9,
        },
        {
            "primitive": (11, 13),
            "source": "branch",
            "incident_edges": 3,
            "rank_lower": 1,
            "rank_upper": 1,
        },
    ]


def test_summarize_batch_aggregates_exact_set_match_rate() -> None:
    summary = summarize_batch(
        [
            {
                "primitive": [5, 7],
                "scaled_vertices": 2,
                "covered_vertices": 2,
                "exact_set_matched_vertices": 1,
                "max_exact_k": 4,
                "max_pool_k": 5,
                "total_missing_k": 0,
            },
            {
                "primitive": [11, 13],
                "scaled_vertices": 3,
                "covered_vertices": 2,
                "exact_set_matched_vertices": 2,
                "max_exact_k": 6,
                "max_pool_k": 6,
                "total_missing_k": 1,
            },
        ]
    )

    assert summary == {
        "audited_primitives": 2,
        "total_scaled_vertices": 5,
        "total_covered_vertices": 4,
        "overall_coverage_pct": 80.0,
        "total_exact_set_matched_vertices": 3,
        "overall_exact_set_match_pct": 60.0,
        "max_exact_k": 6,
        "max_pool_k": 6,
        "total_missing_k": 1,
    }
