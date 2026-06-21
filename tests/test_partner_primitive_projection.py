"""Tests for primitive-template projection of partner graph edges."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_projection import (  # noqa: E402
    edge_template,
    primitive_pair,
    summarize_by_layer,
    summarize_templates,
)


def test_primitive_pair_removes_common_factor_and_sorts() -> None:
    assert primitive_pair((184800, 308880)) == (70, 117)
    assert primitive_pair((308880, 184800)) == (70, 117)
    assert primitive_pair((25, 91)) == (25, 91)


def test_edge_template_projects_scaled_edge_to_primitive_pairs() -> None:
    row = {"u": [184800, 308880], "v": [24750, 90090]}

    template = edge_template(row)

    assert template.source == (70, 117)
    assert template.target == (25, 91)
    assert template.source_scale == 2640
    assert template.target_scale == 990


def test_summarize_templates_counts_orientationless_templates() -> None:
    rows = [
        {"u": [184800, 308880], "v": [24750, 90090]},
        {"u": [24750, 90090], "v": [184800, 308880]},
        {"u": [61200, 222768], "v": [47424, 92820]},
    ]

    summary = summarize_templates(rows)

    assert summary["edges_scanned"] == 3
    assert summary["unique_templates"] == 2
    assert summary["unique_primitives"] == 3
    assert summary["top_templates_edge_share_pct"] == 100.0
    assert summary["top_templates"][0]["count"] == 2
    assert summary["top_templates"][0]["source_primitive"] == [25, 91]
    assert summary["top_templates"][0]["target_primitive"] == [70, 117]


def test_summarize_by_layer_groups_edges_by_endpoint_layer() -> None:
    rows = [
        {"u": [184800, 308880], "v": [24750, 90090]},
        {"u": [61200, 222768], "v": [47424, 92820]},
        {"u": [24, 60], "v": [32, 45]},
    ]
    layer_of = {
        (184800, 308880): "giant",
        (24750, 90090): "giant",
        (61200, 222768): "branch",
        (47424, 92820): "branch",
        (24, 60): "island",
        (32, 45): "island",
    }

    summary = summarize_by_layer(rows, layer_of=layer_of, top=5)

    assert summary["by_layer"]["giant"]["edges_scanned"] == 1
    assert summary["by_layer"]["branch"]["edges_scanned"] == 1
    assert summary["by_layer"]["island"]["edges_scanned"] == 1
    assert summary["cross_layer_edges"] == 0
