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
            "audit_closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction()


def test_wl534_reduces_wl533_to_square_predicates() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl534"
    assert audit["object_layer"] == "m2_one_parameter_square_predicate_obstruction_after_wl533"
    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "parameter_restrictions": [
            "ell is an odd prime with ell ≡ 1 mod 4",
            "choose integers a,b with a^2+b^2=ell",
            "u is rational",
            "S(u) = ell*N(u)^2 + 4*D(u)^2 is a rational square",
            "R(u) = ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4 is positive",
            "T(u) = (A(u)^2 + B(u)^2)/2 is a rational square",
        ],
        "touches_only_M2_for_the_wl533_pure_family": True,
    }


def test_wl534_records_the_square_predicate_identities() -> None:
    audit = _audit()

    reduction = audit["one_parameter_square_predicate_reduction"]
    assert reduction["definitions"] == {
        "D(u)": "1 + u^2",
        "N(u)": "b*(1-u^2) + 2*a*u",
        "P(u)": "a*(1-u^2) - 2*b*u",
        "S(u)": "ell*N(u)^2 + 4*D(u)^2",
        "R(u)": "ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4",
        "A(u)": "-N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4",
        "B(u)": "N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4",
        "T(u)": "(A(u)^2 + B(u)^2) / 2",
    }
    assert all(check["verified"] is True for check in reduction["identity_checks"])
    assert {
        "p_n_norm_identity",
        "upper_positivity_difference",
        "range_quartic_in_q",
        "a_plus_b_positive_identity",
        "t_is_half_sum_of_squares",
    } == {check["check_id"] for check in reduction["identity_checks"]}

    zero_branch = reduction["zero_branch_analysis"]
    assert zero_branch == {
        "P(u)_quadratic": "a*u^2 + 2*b*u - a = 0",
        "N(u)_quadratic": "b*u^2 - 2*a*u - b = 0",
        "P(u)_discriminant": "4*ell",
        "N(u)_discriminant": "4*ell",
        "discriminants_equal_4ell": True,
        "reason": (
            "For an odd prime ell, sqrt(ell) is not rational. Therefore a quadratic "
            "with discriminant 4*ell has no rational root. So P(u)=0 and N(u)=0 are "
            "impossible for rational u."
        ),
        "P(u)_has_rational_root": False,
        "N(u)_has_rational_root": False,
        "lower_positivity_branch_automatic": True,
        "hidden_q_zero_branch_automatic": True,
    }


def test_wl534_states_the_exact_smaller_obstruction() -> None:
    audit = _audit()

    proposition = audit["exact_smaller_obstruction"]
    assert proposition["handoff_name"] == (
        "wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction_stop"
    )
    assert "S(u) is a rational square" in proposition["statement"]
    assert "R(u) > 0" in proposition["statement"]
    assert "T(u) is a rational square" in proposition["statement"]
    assert "removes the auxiliary square-root variables C and Y" in proposition[
        "strictly_smaller_reason"
    ]


def test_wl534_boundary_examples_capture_the_new_behavior() -> None:
    audit = _audit()

    examples = audit["boundary_examples"]
    assert examples["prime_5_basepoint_fails_at_s_square_predicate"] == {
        "ell": 5,
        "a": 1,
        "b": 2,
        "u": "0",
        "S(u)": "24",
        "S(u)_is_rational_square": False,
        "R(u)": "76",
        "R(u)_is_positive": True,
        "T(u)": "5392",
        "T(u)_is_rational_square": False,
        "meaning": (
            "At ell=5 and u=0, the new upper range already holds, but the first "
            "remaining failure is exactly the square predicate S(u)."
        ),
    }
    assert examples["prime_13_basepoint_fails_at_t_square_predicate"] == {
        "ell": 13,
        "a": 2,
        "b": 3,
        "u": "0",
        "S(u)": "121",
        "S(u)_is_rational_square": True,
        "R(u)": "1037",
        "R(u)_is_positive": True,
        "T(u)": "288385",
        "T(u)_is_rational_square": False,
        "meaning": (
            "At ell=13 and u=0, the conic-quartic part and the strict range both hold, "
            "but the remaining failure is exactly the square predicate T(u)."
        ),
    }


def test_wl534_proves_only_the_strictly_smaller_obstruction_and_stops() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "wl533_reduced_to_one_parameter_square_predicate_obstruction_here": True,
        "auxiliary_C_and_Y_variables_eliminated_here": True,
        "lower_positivity_and_zero_branches_automatic_here": True,
        "remaining_problem_is_two_square_predicates_plus_one_inequality": True,
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


def test_wl534_status_fails_when_an_identity_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_identity_checks",
        lambda: [{"check_id": "broken", "identity": "0 = 1", "verified": False}],
    )

    audit = module.build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "square_predicate_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl534_status_fails_when_zero_branch_analysis_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_zero_branch_analysis",
        lambda: {"discriminants_equal_4ell": False},
    )

    audit = module.build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "zero_branch_discriminant_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl534_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl534.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction.py"
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
    assert "work_log=wl534" in result.stdout
    assert "wl533_reduced_to_one_parameter_square_predicate_obstruction_here=True" in result.stdout
    assert "advance_to_m3=False" in result.stdout
    assert payload["work_log"] == "wl534"
