"""Tests for selecting primitive hotspots for rank audit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_rank_audit import (  # noqa: E402
    select_primitives,
    summarize_rank_rows,
)


def test_select_primitives_keeps_order_and_deduplicates_across_layers() -> None:
    summary = {
        "top_primitives": [
            {"primitive": [25, 91], "incident_edges": 100},
            {"primitive": [70, 117], "incident_edges": 90},
        ],
        "by_layer": {
            "giant": {
                "top_primitives": [
                    {"primitive": [25, 91], "incident_edges": 80},
                    {"primitive": [11, 45], "incident_edges": 50},
                ]
            },
            "island": {
                "top_primitives": [
                    {"primitive": [2, 19], "incident_edges": 10},
                ]
            },
        },
    }

    selected = select_primitives(summary, limit=4)

    assert selected == [
        ((25, 91), "global", 100),
        ((70, 117), "global", 90),
        ((11, 45), "giant", 50),
        ((2, 19), "island", 10),
    ]


def test_summarize_rank_rows_includes_pool_stats_when_present() -> None:
    rows = [
        {"source": "global", "rank_lower": 3, "rank_certified": True, "rational_n_pool_size": 262},
        {"source": "global", "rank_lower": 2, "rank_certified": True, "rational_n_pool_size": 80},
        {"source": "island", "rank_lower": 1, "rank_certified": True, "rational_n_pool_size": 6},
    ]

    summary = summarize_rank_rows(rows)

    assert summary["pool_size_min"] == 6
    assert summary["pool_size_max"] == 262
    assert summary["pool_size_avg"] == 116.0
