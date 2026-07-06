from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.summarize_mixed_closure_residual_covers import (
    summarize_cover_rows,
    write_json,
)


def test_summarize_cover_rows_aligns_no_point_covers_with_selmer_gap() -> None:
    cover_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "status": "ok",
            "cover_count": 4,
            "covers_without_points": 2,
            "covers": [
                {"index": 1, "quartic": "x^4 - 1", "point_count": 4},
                {"index": 2, "quartic": "x^4 + 1", "point_count": 2},
                {
                    "index": 3,
                    "quartic": "41*x^4 + 1025",
                    "covering_map_to_elliptic": "map-3",
                    "point_count": 0,
                },
                {
                    "index": 4,
                    "quartic": "-19*x^4 - 5",
                    "covering_map_to_elliptic": "map-4",
                    "point_count": 0,
                },
            ],
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "ok",
            "cover_count": 5,
            "covers_without_points": 3,
            "covers": [
                {"index": 1, "quartic": "x^4 - 4", "point_count": 12},
                {"index": 2, "quartic": "x^4 - 9", "point_count": 2},
                {"index": 3, "quartic": "x^4 + 2", "point_count": 0},
                {"index": 4, "quartic": "x^4 + 3", "point_count": 0},
                {"index": 5, "quartic": "x^4 + 5", "point_count": 0},
            ],
        },
    ]
    diagnostic_rows = [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "status": "ok",
            "selmer_rank_pari": 4,
            "torsion_two_dimension": 2,
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "status": "ok",
            "selmer_rank_pari": 5,
            "torsion_two_dimension": 2,
        },
    ]

    summary = summarize_cover_rows(cover_rows, diagnostic_rows=diagnostic_rows)

    assert summary["rows"] == 2
    assert summary["status_counts"] == {"ok": 2}
    assert summary["covers_without_points_counts"] == {"2": 1, "3": 1}
    assert summary["point_count_patterns"] == {"[4, 2, 0, 0]": 1, "[12, 2, 0, 0, 0]": 1}
    assert summary["selmer_gap_alignment_counts"] == {"match": 2}
    assert summary["evidence_level_counts"] == {
        "bounded-search-no-point-candidate": 2
    }
    assert summary["rows_by_curve"]["AA"]["covers_without_points_counts"] == {"2": 1}
    assert summary["no_point_cover_rows"] == [
        {
            "A": 115,
            "B": 297,
            "curve": "AA",
            "cover_count": 4,
            "covers_without_points": 2,
            "no_point_cover_indices": [3, 4],
            "no_point_covers": [
                {
                    "index": 3,
                    "quartic": "41*x^4 + 1025",
                    "covering_map_to_elliptic": "map-3",
                },
                {
                    "index": 4,
                    "quartic": "-19*x^4 - 5",
                    "covering_map_to_elliptic": "map-4",
                },
            ],
            "selmer_gap": 2,
            "selmer_gap_alignment": "match",
            "local_solubility_source": "PARI ell2cover",
            "evidence_level": "bounded-search-no-point-candidate",
        },
        {
            "A": 209,
            "B": 5355,
            "curve": "BB",
            "cover_count": 5,
            "covers_without_points": 3,
            "no_point_cover_indices": [3, 4, 5],
            "no_point_covers": [
                {"index": 3, "quartic": "x^4 + 2"},
                {"index": 4, "quartic": "x^4 + 3"},
                {"index": 5, "quartic": "x^4 + 5"},
            ],
            "selmer_gap": 3,
            "selmer_gap_alignment": "match",
            "local_solubility_source": "PARI ell2cover",
            "evidence_level": "bounded-search-no-point-candidate",
        },
    ]
    assert summary["boundary"] == (
        "PARI ell2cover returns everywhere locally soluble 2-covers. "
        "A no-point cover here means hyperellratpoints found no point up to "
        "the chosen height. It is an explicit Sha[2] candidate, not a proof "
        "that the cover has no rational point."
    )


def test_write_json_writes_sorted_summary(tmp_path: Path) -> None:
    out_path = tmp_path / "summary.json"

    write_json(out_path, {"b": 1, "a": 2})

    assert out_path.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
