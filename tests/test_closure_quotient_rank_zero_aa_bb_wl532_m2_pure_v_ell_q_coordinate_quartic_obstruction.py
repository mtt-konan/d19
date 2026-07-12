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
            "audit_closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()


def test_wl532_reduces_wl531_to_a_strictly_smaller_q_coordinate_obstruction() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl532"
    assert audit["object_layer"] == (
        "m2_strictly_smaller_q_coordinate_quartic_obstruction_after_wl531"
    )
    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "parameter_restrictions": [
            "ell is an odd prime",
            "0 < X(Q) < ell^2",
            "Q is a rational square",
            "ell - Q is a rational square",
            "ell*Q + 4 is a rational square",
        ],
        "touches_only_M2_for_the_wl531_pure_family": True,
    }


def test_wl532_records_the_q_coordinate_formulas_and_mod_4_cut() -> None:
    audit = _audit()

    reduction = audit["q_coordinate_reduction"]
    assert reduction["Q_definition"] == "Q = 16 / A_ell(X,z)"
    assert reduction["derived_square_relations"] == {
        "ell - Q": "B_ell(X,z) / A_ell(X,z)",
        "X(Q)": "((ell - Q)*(ell*Q + 4)) / Q",
        "G_ell(Q)": (
            "Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2 + "
            "(32*ell - 64)Q + 16"
        ),
        "completed_square_form": "(Q^2 + (8 - 4*ell)Q - 4)^2 + 16*(ell - 1)^2*Q^2",
        "V_definition": "V = U*Q/ell",
        "z(Q)": "ell^2 - 4 + 8*ell/Q - X(Q)",
    }
    assert all(check["verified"] is True for check in reduction["identity_checks"])
    assert {
        "q_definition_from_wl531_lift_square",
        "x_formula_in_q_coordinate",
        "opposite_square_becomes_q_quartic",
        "converse_source_quadratic_from_q",
    }.issubset({check["check_id"] for check in reduction["identity_checks"]})

    mod_4 = reduction["mod_4_obstruction"]
    assert mod_4["primes_3_mod_4_excluded"] is True
    assert mod_4["remaining_prime_congruence_class"] == "ell ≡ 1 mod 4"
    certificate = mod_4["certificate"]
    assert "ell=p^2+q^2" in certificate["rational_to_primitive_integer_step"]
    assert "Euler's criterion" in certificate["mod_ell_step"]
    assert "ell divides v" in certificate["descent_step"]
    assert "pure v_ell M2 point-existence proposition" in certificate["conclusion"]

    nonzero = reduction["nonzero_analysis"]
    assert nonzero["all_nonzero_branches_excluded"] is True
    assert "B_ell(X,z)=0" in nonzero["ell_minus_Q_nonzero"]
    assert "divide the square identity" in nonzero["square_factor_inference"]
    assert "X(Q)=0" in nonzero["converse_denominators"]


def test_wl532_states_the_exact_smaller_obstruction() -> None:
    audit = _audit()

    proposition = audit["exact_smaller_obstruction"]
    assert proposition["handoff_name"] == (
        "wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction_stop"
    )
    assert "ell congruent to 1 mod 4" in proposition["statement"]
    assert "ell*Q+4 is a rational square" in proposition["statement"]
    assert "V^2 = Q^4 + (16 - 8*ell)Q^3" in proposition["statement"]
    assert "whole ell congruent to 3 mod 4 prime class" in proposition["strictly_smaller_reason"]


def test_wl532_boundary_examples_capture_the_new_behavior() -> None:
    audit = _audit()

    examples = audit["boundary_examples"]
    assert examples["prime_7_immediate_exclusion"] == {
        "ell": 7,
        "reason": (
            "Any wl531 point would force ell to be a sum of two rational squares. "
            "The odd prime 7 is congruent to 3 mod 4, so the new Q-coordinate "
            "reduction excludes it immediately."
        ),
    }
    assert examples["prime_13_recovered_source_lift_point"] == {
        "ell": 13,
        "Q": "9",
        "ell_minus_Q": "4",
        "ell_Q_plus_4": "121",
        "X(Q)": "484/9",
        "z(Q)": "1105/9",
        "quartic_value_G_13(Q)": "288385",
        "quartic_value_is_rational_square": False,
        "meaning": (
            "The wl531 source-side lift example at ell=13 becomes the single "
            "Q-value Q=9. The remaining failure is now only the new quartic "
            "square condition G_13(9)."
        ),
    }


def test_wl532_proves_only_the_strictly_smaller_obstruction_and_stops() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "wl531_shrunk_to_strictly_smaller_exact_obstruction_here": True,
        "primes_3_mod_4_excluded_here": True,
        "remaining_case_is_q_coordinate_quartic_here": True,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "advance_to_m3": False,
        "stop_after_exact_smaller_obstruction": True,
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


def test_wl532_status_fails_when_an_identity_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_identity_checks",
        lambda: [{"check_id": "broken", "identity": "0 = 1", "verified": False}],
    )

    audit = module.build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "q_coordinate_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl532_status_fails_when_the_mod_4_obstruction_is_not_recorded(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_mod_4_obstruction",
        lambda: {"primes_3_mod_4_excluded": False},
    )

    audit = module.build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "mod_4_obstruction_not_recorded" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl532_status_fails_when_a_q_coordinate_nonzero_branch_is_not_excluded(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_q_coordinate_nonzero_analysis",
        lambda: {"all_nonzero_branches_excluded": False},
    )

    audit = module.build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "q_coordinate_nonzero_branch_not_excluded" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl532_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl532.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction.py"
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
    assert "work_log=wl532" in result.stdout
    assert "wl531_shrunk_to_strictly_smaller_exact_obstruction_here=True" in result.stdout
    assert "advance_to_m3=False" in result.stdout
    assert payload["work_log"] == "wl532"
