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
            "audit_closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction()


def test_wl533_reduces_wl532_to_one_parameter_obstruction() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl533"
    assert audit["object_layer"] == "m2_one_parameter_conic_quartic_obstruction_after_wl532"
    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "parameter_restrictions": [
            "ell is an odd prime with ell ≡ 1 mod 4",
            "choose integers a,b with a^2+b^2=ell",
            "u is rational",
            "0 < X(u) < ell^2",
            "C^2 = ell*N(u)^2 + 4*(1+u^2)^2",
            "2*Y^2 = A(u)^2 + B(u)^2",
        ],
        "touches_only_M2_for_the_wl532_pure_family": True,
    }


def test_wl533_records_the_one_parameter_identities() -> None:
    audit = _audit()

    reduction = audit["one_parameter_reduction"]
    assert reduction["classical_input"] == "Fermat_two_squares_for_primes_1_mod_4"
    assert reduction["definitions"] == {
        "D(u)": "1 + u^2",
        "N(u)": "b*(1-u^2) + 2*a*u",
        "P(u)": "a*(1-u^2) - 2*b*u",
        "q(u)": "N(u) / D(u)",
        "Q(u)": "(N(u) / D(u))^2",
        "A(u)": "-N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4",
        "B(u)": "N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4",
        "Y_definition": "Y = V*D(u)^4",
    }
    assert all(check["verified"] is True for check in reduction["identity_checks"])
    assert {
        "circle_parameterization_on_ell",
        "ell_q_square_plus_4_clears_to_one_quartic",
        "v_quartic_becomes_two_square_sum_in_q",
        "v_relation_clears_to_one_u_sum_of_squares",
        "first_inverse_denominator",
        "second_inverse_denominator",
    }.issubset({check["check_id"] for check in reduction["identity_checks"]})

    inverse = reduction["inverse_and_branch_analysis"]
    assert inverse["all_q_values_covered"] is True
    assert "(-a,b)" in inverse["inverse_formula"]
    assert "(a,-b)" in inverse["inverse_formula"]
    assert "removable 0/0" in inverse["antipodal_branch"]
    assert "same Q=q^2=b^2 as the visible basepoint" in inverse["antipodal_branch"]
    assert "strictly positive right-hand side" in inverse["c_nonzero"]
    assert "forces N(u) != 0" in inverse["positivity_cross_multiplication"]
    assert "Q=(N(u)/(1+u^2))^2 nonzero" in inverse["positivity_cross_multiplication"]


def test_wl533_states_the_exact_smaller_obstruction() -> None:
    audit = _audit()

    proposition = audit["exact_smaller_obstruction"]
    assert proposition["handoff_name"] == (
        "wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction_stop"
    )
    assert "a^2+b^2=ell" in proposition["statement"]
    assert "C^2 = ell*N(u)^2 + 4*D(u)^2" in proposition["statement"]
    assert "2*Y^2 = A(u)^2 + B(u)^2" in proposition["statement"]
    assert "absorbs the Q-square and ell-Q-square constraints" in proposition[
        "strictly_smaller_reason"
    ]


def test_wl533_boundary_examples_capture_the_new_behavior() -> None:
    audit = _audit()

    examples = audit["boundary_examples"]
    assert examples["prime_5_basepoint_fails_at_the_remaining_c_quartic"] == {
        "ell": 5,
        "a": 1,
        "b": 2,
        "u": "0",
        "Q(u)": "4",
        "cleared_c_quartic_value": "24",
        "cleared_c_quartic_is_rational_square": False,
        "meaning": (
            "The one-parameter reduction is real: the q and ell-q square conditions "
            "are already absorbed at u=0, and the first remaining failure can occur "
            "immediately at the cleared ell*q(u)^2+4 quartic."
        ),
    }
    assert examples["prime_13_recovers_the_wl532_boundary_q_value"] == {
        "ell": 13,
        "a": 2,
        "b": 3,
        "u": "0",
        "Q(u)": "9",
        "cleared_c_quartic_value": "121",
        "C(u)": "11",
        "X(u)": "484/9",
        "A(u)": "751",
        "B(u)": "113",
        "two_g_value": "576770",
        "g_value_is_rational_square": False,
        "meaning": (
            "At ell=13 with a^2+b^2=13 given by 2^2+3^2, the new parameter u=0 "
            "recovers the old Q=9 boundary point exactly. The remaining failure is "
            "now only the denominator-cleared two-square V-condition."
        ),
    }


def test_wl533_proves_only_the_strictly_smaller_obstruction_and_stops() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "wl532_reduced_to_one_parameter_exact_obstruction_here": True,
        "q_and_ell_minus_q_square_conditions_absorbed_here": True,
        "remaining_ell_q_plus_4_and_v_obstructions_recorded_here": True,
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


def test_wl533_status_fails_when_an_identity_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_identity_checks",
        lambda: [{"check_id": "broken", "identity": "0 = 1", "verified": False}],
    )

    audit = module.build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "one_parameter_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl533_status_fails_when_inverse_coverage_is_missing(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_inverse_and_branch_analysis",
        lambda: {"all_q_values_covered": False},
    )

    audit = module.build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "one_parameter_inverse_not_recorded" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl533_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl533.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction.py"
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
    assert "work_log=wl533" in result.stdout
    assert "wl532_reduced_to_one_parameter_exact_obstruction_here=True" in result.stdout
    assert "advance_to_m3=False" in result.stdout
    assert payload["work_log"] == "wl533"
