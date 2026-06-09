from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import probe_focus_template_modular as probe


def test_probe_focus_template_modular_tracks_survivors() -> None:
    summary = probe.probe_modulus(5)

    assert summary["modulus"] == 5
    assert summary["mode"] == "residue"
    assert summary["total_assignments"] == 5**9
    assert summary["side_condition_pass"] < 5**9
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


def test_strict_residue_units_mode_is_a_stronger_diagnostic() -> None:
    loose = probe.probe_modulus(3)
    strict = probe.probe_modulus(3, mode="strict_residue_units")

    assert loose["side_condition_pass"] < loose["total_assignments"]
    assert strict["side_condition_pass"] < loose["side_condition_pass"]
    assert strict["mode"] == "strict_residue_units"


def test_residue_mode_allows_single_zero_but_not_common_zero_pair() -> None:
    assert probe.residue_pair_can_lift_primitive(0, 1, 5)
    assert probe.residue_pair_can_lift_primitive(1, 0, 5)
    assert not probe.residue_pair_can_lift_primitive(0, 0, 5)
