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
            "audit_closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction()


def test_wl535_reduces_wl534_to_direct_q_root_coordinates() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl535"
    assert audit["object_layer"] == "m2_q_root_coordinate_square_quartic_obstruction_after_wl534"
    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "parameter_restrictions": [
            "ell is an odd prime with ell ≡ 1 mod 4",
            "q is rational",
            "ell-q^2 is a rational square",
            "ell*q^2+4 is a rational square",
            "ell*q^4+4*q^2-4*ell is positive",
            (
                "V^2 = q^8 + (16-8*ell)q^6 + (32*ell^2-96*ell+72)q^4 "
                "+ (32*ell-64)q^2 + 16"
            ),
        ],
        "touches_only_M2_for_the_wl534_pure_family": True,
    }


def test_wl535_records_the_q_root_coordinate_identities() -> None:
    audit = _audit()

    reduction = audit["q_root_coordinate_reduction"]
    assert reduction["definitions"] == {
        "q(u)": "N(u) / D(u)",
        "p(u)": "P(u) / D(u)",
        "D(u)": "1 + u^2",
        "N(u)": "b*(1-u^2) + 2*a*u",
        "P(u)": "a*(1-u^2) - 2*b*u",
        "G_ell(Q)": (
            "Q^4 + (16-8*ell)Q^3 + (32*ell^2-96*ell+72)Q^2 "
            "+ (32*ell-64)Q + 16"
        ),
        "V_definition": "V^2 = G_ell(q^2)",
    }
    assert all(check["verified"] is True for check in reduction["identity_checks"])
    assert {
        "circle_identity_in_q_root_coordinate",
        "ell_minus_q_square_is_automatic",
        "s_predicate_descends_to_q_root_coordinate",
        "r_predicate_descends_to_q_root_coordinate",
        "t_predicate_descends_to_q_root_quartic",
        "first_inverse_cross_product",
        "second_inverse_cross_product",
        "first_inverse_denominator",
        "second_inverse_denominator",
    } == {check["check_id"] for check in reduction["identity_checks"]}

    inverse = reduction["inverse_and_branch_analysis"]
    assert inverse["all_q_values_covered"] is True
    assert "neither a nor b can vanish" in inverse["nonzero_a_b_reason"]
    assert "switching the sign of p" in inverse["branch_summary"]
    assert all(
        check["verified"] is True
        for check in inverse["generic_patch_reconstruction_checks"]
    )
    assert {
        "first_patch_recovers_q",
        "first_patch_recovers_p",
        "second_patch_recovers_q",
        "second_patch_recovers_p",
    } == {check["check_id"] for check in inverse["generic_patch_reconstruction_checks"]}
    assert all(
        check["verified"] is True
        for check in inverse["q_sign_invariance_checks"]
    )
    assert {
        "ell_minus_q_square_even_in_q",
        "ell_q_square_plus_4_even_in_q",
        "positivity_polynomial_even_in_q",
        "quartic_curve_rhs_even_in_q",
    } == {check["check_id"] for check in inverse["q_sign_invariance_checks"]}

    branches = inverse["removable_branches"]
    assert branches["visible_branch_minus_a_b"] == {
        "branch_point": "(-a,b)",
        "branch_condition": "p+a = 0 and q+b != 0",
        "recovered_u": "a/b",
        "point_coordinates": {"q(a/b)": "b", "p(a/b)": "-a"},
        "alternate_denominator": "2*b",
        "alternate_formula_value": "a/b",
        "verified": True,
    }
    assert branches["visible_branch_a_minus_b"] == {
        "branch_point": "(a,-b)",
        "branch_condition": "q+b = 0 and p+a != 0",
        "recovered_u": "-b/a",
        "point_coordinates": {"q(-b/a)": "-b", "p(-b/a)": "a"},
        "alternate_denominator": "2*a",
        "alternate_formula_value": "-b/a",
        "verified": True,
    }
    assert inverse["antipode_sign_branch"] == {
        "missed_point": "(-a,-b)",
        "sign_switched_visible_point": "(a,-b)",
        "same_q_after_sign_switch": "-b",
        "recovered_u_after_sign_switch": "-b/a",
        "verified": True,
    }
    assert "u=(q-b)/(p+a)" in inverse["inverse_formula"]
    assert "D(u)=1+u^2 is never zero" in inverse["nonzero_denominator_reason"]
    assert "positive solution automatically has q != 0" in inverse["q_nonzero_from_positivity"]


def test_wl535_states_the_exact_coordinate_free_reformulation() -> None:
    audit = _audit()

    proposition = audit["exact_coordinate_free_reformulation"]
    assert proposition["handoff_name"] == (
        "wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop"
    )
    assert "ell-q^2 is a rational square" in proposition["statement"]
    assert "ell*q^2+4 is a rational square" in proposition["statement"]
    assert "ell*q^4+4*q^2-4*ell > 0" in proposition["statement"]
    assert "V^2 = q^8" in proposition["statement"]
    assert "a^2+b^2=ell" in proposition["coordinate_free_exact_reformulation_reason"]
    assert (
        "same exact arithmetic content"
        in proposition["coordinate_free_exact_reformulation_reason"]
    )


def test_wl535_boundary_examples_capture_the_new_behavior() -> None:
    audit = _audit()

    examples = audit["boundary_examples"]
    assert examples["prime_5_square_predicates_hold_but_positivity_fails"] == {
        "ell": 5,
        "q": "1",
        "ell-q^2": "4",
        "ell-q^2_is_rational_square": True,
        "ell*q^2+4": "9",
        "ell*q^2+4_is_rational_square": True,
        "ell*q^4+4*q^2-4*ell": "-11",
        "positivity_holds": False,
        "G_ell(q^2)": "481",
        "G_ell(q^2)_is_rational_square": False,
        "meaning": (
            "Both square predicates already hold at ell=5, q=1, but the strict positivity "
            "condition still fails."
        ),
    }
    assert examples["prime_13_only_the_q_root_quartic_square_condition_remains"] == {
        "ell": 13,
        "q": "3",
        "ell-q^2": "4",
        "ell-q^2_is_rational_square": True,
        "ell*q^2+4": "121",
        "ell*q^2+4_is_rational_square": True,
        "ell*q^4+4*q^2-4*ell": "1037",
        "positivity_holds": True,
        "G_ell(q^2)": "288385",
        "G_ell(q^2)_is_rational_square": False,
        "meaning": (
            "At ell=13, q=3 the two square predicates and the strict positivity condition "
            "all hold, but the remaining failure is exactly the direct q-coordinate "
            "quartic-square condition."
        ),
    }


def test_wl535_proves_only_the_coordinate_free_reformulation_and_stops() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "wl534_reduced_to_q_root_coordinate_exact_obstruction_here": True,
        "representation_choice_and_chart_removed_from_statement_here": True,
        "remaining_problem_is_direct_q_root_square_quartic_obstruction": True,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "advance_to_m3": False,
        "stop_after_coordinate_free_exact_reformulation": True,
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


def test_wl535_status_fails_when_an_identity_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_identity_checks",
        lambda: [{"check_id": "broken", "identity": "0 = 1", "verified": False}],
    )

    audit = module.build_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "q_root_coordinate_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl535_status_fails_when_inverse_analysis_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_inverse_and_branch_analysis",
        lambda: {"all_q_values_covered": False},
    )

    audit = module.build_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "q_root_coordinate_inverse_not_recorded" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl535_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl535.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction.py"
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
    assert "work_log=wl535" in result.stdout
    assert "wl534_reduced_to_q_root_coordinate_exact_obstruction_here=True" in result.stdout
    assert "stop_after_coordinate_free_exact_reformulation=True" in result.stdout
    assert "advance_to_m3=False" in result.stdout
    assert payload["work_log"] == "wl535"
