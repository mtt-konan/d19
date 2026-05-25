"""Tests for multi-concordant ground-truth lookup helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.results.multi_concordant import lookup_multi_concordant_pair


def test_lookup_multi_concordant_pair_matches_pair_ignoring_order(tmp_path: Path) -> None:
    dataset = tmp_path / "multi.jsonl"
    rows = [
        {
            "A": 27,
            "B": 160,
            "n_concordant": 2,
            "concordant_N": [36, 120],
            "A_plus_B": 187,
            "closure_pairs": [],
        },
        {
            "A": 153,
            "B": 560,
            "n_concordant": 3,
            "concordant_N": [204, 420, 3900],
            "A_plus_B": 713,
            "closure_pairs": [],
        },
    ]
    _ = dataset.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )

    row = lookup_multi_concordant_pair(560, 153, dataset_path=dataset)

    assert row is not None
    assert row.A == 153
    assert row.B == 560
    assert row.n_concordant == 3
    assert row.concordant_N == [204, 420, 3900]
