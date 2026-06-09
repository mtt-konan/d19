from __future__ import annotations

import json
import math
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


def test_crt_summary_multiplies_stage_counts_for_coprime_moduli() -> None:
    summary = probe.crt_summary([3, 5], sample_limit=0)
    rows = summary["single_modulus_summaries"]

    assert summary["combined_modulus"] == 15
    assert summary["mode"] == "residue"
    assert summary["kind"] == "count_level_crt_diagnostic"
    assert summary["total_assignments"] == math.prod(
        row["total_assignments"] for row in rows
    )
    assert summary["side_condition_pass"] == math.prod(
        row["side_condition_pass"] for row in rows
    )
    assert summary["shared_constraint_pass"] == math.prod(
        row["shared_constraint_pass"] for row in rows
    )
    assert summary["closure_pass"] == math.prod(row["closure_pass"] for row in rows)
    assert summary["missing_square_pass"] == math.prod(
        row["missing_square_pass"] for row in rows
    )
    assert summary["missing_square_obstructed"] == (
        summary["closure_pass"] - summary["missing_square_pass"]
    )


def test_crt_summary_rejects_non_coprime_moduli() -> None:
    try:
        probe.crt_summary([3, 9], sample_limit=0)
    except ValueError as error:
        assert "pairwise coprime" in str(error)
    else:
        raise AssertionError("expected non-coprime moduli to be rejected")


def test_crt_summary_rejects_strict_residue_units_mode() -> None:
    try:
        probe.crt_summary([3, 5], sample_limit=0, mode="strict_residue_units")
    except ValueError as error:
        assert "residue mode" in str(error)
    else:
        raise AssertionError("expected strict CRT mode to be rejected")


def test_crt_summary_from_rows_rejects_mismatched_modes() -> None:
    row = probe.probe_modulus(3, sample_limit=0, mode="strict_residue_units")

    try:
        probe.crt_summary_from_rows([row], mode="residue")
    except ValueError as error:
        assert "row modes" in str(error)
    else:
        raise AssertionError("expected mismatched row modes to be rejected")


def test_cli_can_emit_crt_summary(capsys) -> None:  # type: ignore[no-untyped-def]
    exit_code = probe.main(["3", "5", "--sample-limit", "0", "--crt-summary"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["crt_summary"]["combined_modulus"] == 15
    assert payload["crt_summary"]["kind"] == "count_level_crt_diagnostic"
    assert [row["modulus"] for row in payload["moduli"]] == [3, 5]


def test_probe_many_rejects_strict_crt_before_enumerating() -> None:
    try:
        probe.probe_many(
            [3, 5],
            sample_limit=0,
            mode="strict_residue_units",
            include_crt_summary=True,
        )
    except ValueError as error:
        assert "residue mode" in str(error)
    else:
        raise AssertionError("expected strict CRT mode to be rejected")
