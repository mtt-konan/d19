from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_summary_to_json_dict_serializes_ratios_and_hits() -> None:
    from rational_distance.concordant.fixed_ratio_exact import collect_fixed_ratio_ratios
    from scripts.theory.scan_fixed_ratio_exact import summary_to_json_dict

    summary = collect_fixed_ratio_ratios(k=7, max_b=30)
    payload = summary_to_json_dict(summary)

    assert payload["k"] == 7
    assert payload["max_b"] == 30
    assert payload["ratios"] == ["12/5", "35/12"]
    assert payload["ratio_count"] == 2
    assert payload["noncenter_hits"] == []
    assert payload["centerline_hits"] == []


def test_scan_fixed_ratios_returns_one_summary_per_k() -> None:
    from scripts.theory.scan_fixed_ratio_exact import scan_fixed_ratios

    rows = scan_fixed_ratios(k_min=7, k_max=8, max_b=30)

    assert [row.k for row in rows] == [7, 8]
    assert rows[0].ratio_count == 2
    assert rows[1].ratio_count == 0
