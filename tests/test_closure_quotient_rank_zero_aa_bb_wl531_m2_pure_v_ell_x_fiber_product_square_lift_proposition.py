from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()


def test_wl531_reduces_m2_to_one_exact_x_fiber_product_square_lift_proposition() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl531"
    assert audit["object_layer"] == (
        "m2_exact_missing_proposition_after_square_x_and_complete_d_lift_reduction"
    )
    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "parameter_restrictions": [
            "ell is an odd prime",
            "0 < X < ell^2",
            "X is a rational square",
        ],
        "touches_only_M2_for_the_wl530_pure_family": True,
    }


def test_wl531_records_the_exact_fiber_product_and_square_lift_forms() -> None:
    audit = _audit()

    reduction = audit["fiber_product_reduction"]
    assert reduction["source_square_quadratic"] == (
        "z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2"
    )
    assert reduction["opposite_square_quadratic"] == (
        "U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2"
    )
    assert reduction["lift_square_forms"] == {
        "A_ell(X,z)": "2*(X - ell^2 + 4 + z)/ell",
        "B_ell(X,z)": "2*(X - ell^2 - 4 + z) = ell*A_ell(X,z) - 16",
    }
    assert all(check["verified"] is True for check in reduction["identity_checks"])
    assert {
        "b_zero_forces_x_zero_on_source_quadratic",
        "a_zero_forces_b_negative",
        "chosen_t_is_recovered_after_sign_choice",
    }.issubset({check["check_id"] for check in reduction["identity_checks"]})

    denominators = reduction["converse_denominator_analysis"]
    assert denominators["all_converse_denominators_excluded"] is True
    assert "-16*X=0" in denominators["B_nonzero"]
    assert "B_ell(X,z)=-16" in denominators["A_nonzero"]
    assert "r^2-4*ell=2*r*u_minus" in denominators["r_squared_minus_4ell_nonzero"]


def test_wl531_excludes_x_zero_and_identifies_the_first_missing_lemma() -> None:
    audit = _audit()

    t_zero = audit["fiber_product_reduction"]["t_zero_analysis"]
    assert t_zero["candidate_square_values"] == ["16/ell", "-4*ell"]
    assert t_zero["t_zero_can_satisfy_square_lift_conditions"] is False
    assert t_zero["positivity_domain_reduces_to"] == "0 < X < ell^2"

    proposition = audit["exact_missing_proposition"]
    assert proposition["handoff_name"] == (
        "wl531_m2_pure_v_ell_exact_x_fiber_product_square_lift_proposition_stop"
    )
    assert "0 < X < ell^2" in proposition["statement"]
    assert "A_ell(X,z)" in proposition["statement"]
    assert "B_ell(X,z)" in proposition["statement"]
    assert "only unresolved arithmetic step" in proposition["first_missing_lemma_reason"]


def test_wl531_uses_examples_to_show_each_layer_is_individually_insufficient() -> None:
    audit = _audit()

    examples = audit["boundary_examples"]
    opposite_only = examples["opposite_side_only_example"]
    assert opposite_only == {
        "ell": 7,
        "point_on_opposite_square_locus": {"X": "4", "U": "195"},
        "X_is_rational_square": True,
        "positivity_range": "0 < X < ell^2",
        "source_quadratic_value": "2465",
        "source_quadratic_is_rational_square": False,
        "meaning": (
            "The opposite-side elliptic quotient can contribute a square-X point in the "
            "positivity range without giving a source-side square lift."
        ),
    }

    source_only = examples["source_lift_only_example"]
    assert source_only["ell"] == 13
    assert source_only["quartic_point"] == {"r": "6", "y": "32"}
    assert source_only["induced_values"] == {"t": "-22/3", "X": "484/9", "z": "1105/9"}
    assert source_only["A_ell(X,z)"] == "16/9"
    assert source_only["B_ell(X,z)"] == "64/9"
    assert source_only["A_is_rational_square"] is True
    assert source_only["B_is_rational_square"] is True
    assert source_only["opposite_quadratic_value"] == "48737065/81"
    assert source_only["opposite_quadratic_is_rational_square"] is False


def test_wl531_proves_only_an_exact_missing_proposition_and_stops_before_m3() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "m2_reduced_to_exact_missing_proposition_here": True,
        "exact_x_fiber_product_square_lift_proposition_identified_here": True,
        "t_zero_excluded_from_the_missing_proposition_here": True,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "advance_to_m3": False,
        "stop_after_exact_missing_proposition": True,
    }

    assert audit["uniform_infinite_subfamily_exclusion_proved_here"] is False
    assert audit["strict_counterexample_found_here"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["advance_to_m3"] is False
    assert audit["stop_after_current_task"] is True


def test_wl531_status_fails_when_a_reduction_identity_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_identity_checks",
        lambda: [{"check_id": "broken", "identity": "0 = 1", "verified": False}],
    )

    audit = module.build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "reduction_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl531_status_fails_when_t_zero_is_not_excluded(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_t_zero_analysis",
        lambda: {"t_zero_can_satisfy_square_lift_conditions": True},
    )

    audit = module.build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "t_zero_not_excluded" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl531_status_fails_when_a_converse_denominator_is_not_excluded(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_converse_denominator_analysis",
        lambda: {"all_converse_denominators_excluded": False},
    )

    audit = module.build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "converse_denominator_not_excluded" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl531_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl531.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--out",
            str(out),
            "--strict",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "work_log=wl531" in result.stdout
    assert "m2_reduced_to_exact_missing_proposition_here=True" in result.stdout
    assert "advance_to_m3=False" in result.stdout
    assert payload["work_log"] == "wl531"
