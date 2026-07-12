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
            "audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl530_m1_pure_v_ell_symbolic_family()


def test_wl530_builds_the_symbolic_pure_v_ell_family_and_exact_formulas() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl530"
    assert audit["object_layer"] == "symbolic_pure_support_function_field_family"

    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "source_leg": 1,
        "opposite_leg": "ell - 1",
        "parameter_restrictions": [
            "ell is an odd prime",
            "r != 0",
            "r^2 != 4*ell",
        ],
        "touches_only_M1_symbolic_derivation": True,
    }

    cover = audit["complete_d_family"]
    assert cover["parameters"] == {
        "p": "8 - 2*ell^2",
        "sqrt_q": "ell^2 + 4",
        "q": "(ell^2 + 4)^2",
    }
    assert cover["cover_equations"] == [
        "X - (2*ell^2 - 8) = ell*u_minus_p^2",
        "X - (2*ell^2 + 8) = u_pos_2sqrt_q^2",
        "X + (2*ell^2 + 8) = ell*u_neg_2sqrt_q^2",
    ]
    assert cover["difference_equations"] == [
        "ell*u_minus_p^2 - u_pos_2sqrt_q^2 = 16",
        "u_minus_p^2 - u_neg_2sqrt_q^2 = -4*ell",
    ]

    model = audit["function_field_model"]
    assert model["function_field"] == (
        "Q(ell)(r,y)/(y^2 - (ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3))"
    )
    assert model["cover_maps"] == {
        "u_minus_p": "(r^2 - 4*ell)/(2*r)",
        "u_pos_2sqrt_q": "y/(2*r)",
        "u_neg_2sqrt_q": "(r^2 + 4*ell)/(2*r)",
        "X": "2*ell^2 - 8 + ell*((r^2 - 4*ell)/(2*r))^2",
        "Y": "ell*y*(r^4 - 16*ell^2)/(8*r^3)",
    }
    assert all(check["verified"] is True for check in model["identity_checks"])

    maps = audit["source_side_maps_and_n_m"]
    assert maps["centered_even_map"] == {
        "t": "y*(r^2 + 4*ell)/(4*r*(r^2 - 4*ell))",
        "N": "(ell + t)/2",
        "M": "(ell - t)/2",
        "positivity_domain": "|t| < ell",
        "source_product_square_identity": "(N^2+1)(M^2+1) = (z/4)^2",
    }

    square_locus = audit["opposite_side_square_locus"]
    assert square_locus["opposite_side_product"] == "(N^2+(ell-1)^2)(M^2+(ell-1)^2)"
    assert square_locus["product_in_t"] == (
        "((t^2 + 5*ell^2 - 8*ell + 4)^2 - 4*ell^2*t^2)/16"
    )
    assert square_locus["square_locus_quartic"] == (
        "U^2 = t^4 + (6*ell^2 - 16*ell + 8)*t^2 + (5*ell^2 - 8*ell + 4)^2"
    )
    assert square_locus["elliptic_quotient"] == (
        "Y^2 = X^3 + (6*ell^2 - 16*ell + 8)*X^2 + (5*ell^2 - 8*ell + 4)^2*X"
    )
    assert square_locus["degree_two_map"] == "X = t^2, Y = t*U"
    assert square_locus["quartic_discriminant"] == (
        "65536*ell^4*(ell - 1)^4*(5*ell^2 - 8*ell + 4)^2"
    )
    assert square_locus["elliptic_rhs_cubic_discriminant"] == (
        "-64*ell^2*(ell - 1)^2*(5*ell^2 - 8*ell + 4)^4"
    )


def test_wl530_recovers_wl528_and_wl529_exactly_at_ell_5() -> None:
    audit = _audit()

    recovery = audit["ell_5_recovery"]
    assert recovery == {
        "ell": 5,
        "function_field_equation": "y^2 = 5*r^4 - 264*r^2 + 2000",
        "t_formula": "y*(r^2+20)/(4*r*(r^2-20))",
        "N_formula": "(5+t)/2",
        "M_formula": "(5-t)/2",
        "opposite_side_product": "(N^2+16)(M^2+16)",
        "square_locus_quartic": "U^2 = t^4 + 78*t^2 + 7921",
        "elliptic_quotient": "Y^2 = X^3 + 78*X^2 + 7921*X",
        "all_recovery_checks_passed": True,
    }


def test_wl530_proves_only_the_symbolic_m1_derivation_and_stops_before_m2() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "symbolic_complete_d_family_derived_here": True,
        "function_field_chart_derived_here": True,
        "rational_n_m_maps_derived_here": True,
        "opposite_side_square_product_derived_here": True,
        "square_specialization_elliptic_family_derived_here": True,
        "exact_ell_5_recovery_verified_here": True,
        "uniform_cover_family_obstruction_proved_here": False,
        "m2_entered_here": False,
        "stop_after_m1": True,
    }

    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["advance_to_m2"] is False


def test_wl530_status_fails_when_a_symbolic_identity_check_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_function_field_identity_checks",
        lambda: [
            {
                "check_id": "broken_identity",
                "identity": "0 = 1",
                "verified": False,
            }
        ],
    )

    audit = module.build_wl530_m1_pure_v_ell_symbolic_family()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "symbolic_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl530_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl530.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family.py"
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
    assert "work_log=wl530" in result.stdout
    assert "symbolic_complete_d_family_derived_here=True" in result.stdout
    assert "exact_ell_5_recovery_verified_here=True" in result.stdout
    assert "advance_to_m2=False" in result.stdout
    assert payload["work_log"] == "wl530"
