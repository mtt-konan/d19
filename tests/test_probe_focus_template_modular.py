from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import probe_focus_template_modular as probe


def test_probe_focus_template_modular_tracks_survivors() -> None:
    summary = probe.probe_modulus(5)

    assert summary["modulus"] == 5
    assert summary["total_assignments"] == 5**9
    assert summary["side_condition_pass"] > 0
    assert summary["shared_constraint_pass"] > 0
    assert summary["closure_pass"] > 0
    assert summary["missing_square_pass"] > 0
    assert summary["missing_square_pass"] <= summary["closure_pass"]
    assert summary["missing_square_obstructed"] == (
        summary["closure_pass"] - summary["missing_square_pass"]
    )
    assert summary["sample_survivors"]
    assert set(summary["sample_survivors"][0]) == {
        "u",
        "p",
        "q",
        "v",
        "r",
        "s",
        "w",
        "x",
        "y",
        "A",
        "B",
        "N1",
        "N2",
        "missing_value",
    }


def test_probe_many_reports_all_moduli() -> None:
    payload = probe.probe_many([3, 5], sample_limit=2)

    assert [row["modulus"] for row in payload["moduli"]] == [3, 5]
    assert payload["moduli"][0]["sample_limit"] == 2
