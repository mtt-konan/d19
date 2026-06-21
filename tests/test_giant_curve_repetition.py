"""Tests for repeated elliptic-curve classes inside a partner component."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.giant_curve_repetition import (  # noqa: E402
    component_curve_repetition,
    j_invariant_key,
    summarize_curve_repetition,
)


def test_j_invariant_key_merges_pythagorean_complement_primitives() -> None:
    assert j_invariant_key((3, 5)) == j_invariant_key((4, 5))
    assert j_invariant_key((3, 5)) != j_invariant_key((5, 12))


def test_component_curve_repetition_groups_scaled_vertices_by_primitive_curve() -> None:
    vertices = [
        [25, 91],
        [50, 182],
        [70, 117],
        [140, 234],
        [35, 288],
    ]

    summary = component_curve_repetition(
        {
            "component_id": 0,
            "size": len(vertices),
            "edges": 3,
            "vertices": vertices,
        },
        top=2,
    )

    assert summary["component_id"] == 0
    assert summary["vertex_count"] == 5
    assert summary["primitive_curve_count"] == 3
    assert summary["j_curve_count"] == 3
    assert summary["repeated_primitive_curve_count"] == 2
    assert summary["repeated_j_curve_count"] == 2
    assert summary["largest_primitive_class_size"] == 2
    assert summary["top_primitive_curves"] == [
        {
            "primitive": [25, 91],
            "scaled_vertex_count": 2,
            "share_pct": 40.0,
            "min_scale": 1,
            "max_scale": 2,
            "sample_vertices": [[25, 91], [50, 182]],
        },
        {
            "primitive": [70, 117],
            "scaled_vertex_count": 2,
            "share_pct": 40.0,
            "min_scale": 1,
            "max_scale": 2,
            "sample_vertices": [[70, 117], [140, 234]],
        },
    ]


def test_summarize_curve_repetition_compares_giant_and_other_components() -> None:
    components = [
        {
            "component_id": 0,
            "size": 4,
            "edges": 2,
            "vertices": [[25, 91], [50, 182], [75, 273], [70, 117]],
        },
        {
            "component_id": 1,
            "size": 2,
            "edges": 1,
            "vertices": [[35, 288], [70, 576]],
        },
    ]

    summary = summarize_curve_repetition(components, top=3)

    assert summary["component_count"] == 2
    assert summary["giant"]["component_id"] == 0
    assert summary["giant"]["vertex_count"] == 4
    assert summary["giant"]["primitive_curve_count"] == 2
    assert summary["giant"]["j_curve_count"] == 2
    assert summary["giant"]["primitive_reuse_ratio"] == 2.0
    assert summary["non_giant_totals"]["vertex_count"] == 2
    assert summary["non_giant_totals"]["primitive_curve_count"] == 1
    assert summary["non_giant_totals"]["j_curve_count"] == 1
