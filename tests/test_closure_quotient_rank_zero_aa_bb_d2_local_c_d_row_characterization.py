from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d2_local_c_d_row_characterization import (  # noqa: E501
    BOUNDARY,
    audit_rank_zero_aa_bb_d2_local_c_d_row_characterization,
)


def _d0_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D0_complete_d_container_definition",
        "d0_status": "framed_definition",
        "complete_d_container": {
            "name": "D0_complete_d_prelocal_container",
            "coordinate_tuple_order": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ],
            "coordinate_definitions": {
                "d_minus_p": "X-(-p)=X+p",
                "d_pos_2sqrt_q": "X-(2*sqrt_q)",
                "d_neg_2sqrt_q": "X-(-2*sqrt_q)=X+2*sqrt_q",
            },
            "defining_relation": (
                "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2"
            ),
            "local_c_d_rows_built": False,
            "package_x_coordinates_used": False,
            "old_s_tilde_used_as_container": False,
        },
        "local_c_d_rows_built": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d1_support() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D1_relevant_place_support_confinement",
        "d1_status": "framed_and_proved_support_confinement",
        "candidate_support": {
            "name": "S_D1_relevant_places",
            "equivalent_finite_set": (
                "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
            ),
        },
        "support_only_not_row_classification": True,
        "local_c_d_rows_built": False,
        "next_lemma": "D2_local_C_d_row_characterization",
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def test_d2_records_complete_d_equations_and_candidate_row_domain() -> None:
    audit = audit_rank_zero_aa_bb_d2_local_c_d_row_characterization(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D2_local_C_d_row_characterization"
    assert audit["d2_status"] == "row_obligations_framed"
    assert audit["complete_d_coordinate_frame"] == {
        "curve": "E_L: Y^2=(X+p)*(X^2-4*q)",
        "coordinate_order": [
            "d_minus_p",
            "d_pos_2sqrt_q",
            "d_neg_2sqrt_q",
        ],
        "product_relation": (
            "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2"
        ),
        "covering_equations": [
            "d_minus_p*u_minus_p^2 = X+p",
            "d_pos_2sqrt_q*u_pos_2sqrt_q^2 = X-2*sqrt_q",
            "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = X+2*sqrt_q",
        ],
        "difference_equations": [
            "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2",
            "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2",
            "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q",
        ],
        "package_x_coordinates_used": False,
    }
    assert audit["candidate_row_domain"] == {
        "source": "D1_relevant_place_support_confinement",
        "places": "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}",
        "odd_place_types": ["ell|L", "ell|T", "ell|sqrt_q"],
        "row_characterization_only": True,
    }


def test_d2_frames_one_minimal_obligation_for_each_d1_place_type() -> None:
    audit = audit_rank_zero_aa_bb_d2_local_c_d_row_characterization(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
    )

    rows = audit["local_row_obligations"]
    assert [row["place_type"] for row in rows] == [
        "ell|L",
        "ell|T",
        "ell|sqrt_q",
        "ell=2",
        "infinity",
    ]
    assert rows[0] == {
        "id": "D2a_odd_L_collision_row",
        "place_type": "ell|L",
        "prime_condition": "ell odd and ell | L",
        "colliding_roots": ["e_minus=-p", "e_pos=2*sqrt_q"],
        "vanishing_root_difference": "e_pos-e_minus = 16*L^2",
        "unit_root_difference_obligations": [
            "check whether e_minus-e_neg=4*T^2 is an ell-adic unit in the active parameter stratum",
            (
                "check whether e_pos-e_neg=4*sqrt_q is an ell-adic unit in "
                "the active parameter stratum"
            ),
        ],
        "local_equation_to_characterize": (
            "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2"
        ),
        "minimal_output_needed": (
            "allowed squareclass pairs for (d_minus_p,d_pos_2sqrt_q), then "
            "d_neg_2sqrt_q from the product relation"
        ),
        "status": "obligation_framed_not_solved",
    }
    assert rows[1]["id"] == "D2b_odd_T_collision_row"
    assert rows[1]["local_equation_to_characterize"] == (
        "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2"
    )
    assert rows[2]["id"] == "D2c_odd_sqrt_q_collision_row"
    assert rows[2]["local_equation_to_characterize"] == (
        "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q"
    )
    assert rows[3]["id"] == "D2d_dyadic_complete_row"
    assert rows[3]["status"] == "obligation_framed_not_solved"
    assert rows[4] == {
        "id": "D2e_real_sign_row",
        "place_type": "infinity",
        "root_order": [
            "e_neg=-2*sqrt_q",
            "e_minus=-p",
            "e_pos=2*sqrt_q",
        ],
        "allowed_sign_classes": [["+", "+", "+"], ["-", "-", "+"]],
        "forbidden_sign_classes": [["+", "-", "-"], ["-", "+", "-"]],
        "minimal_output_needed": (
            "record the real sign row only; do not combine it with finite rows into a rank bound"
        ),
        "status": "symbolically_characterized",
    }


def test_d2_keeps_row_obligations_separate_from_matrix_and_selmer_claims() -> None:
    audit = audit_rank_zero_aa_bb_d2_local_c_d_row_characterization(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
    )

    assert audit["row_obligations_framed"] is True
    assert audit["local_c_d_rows_solved"] is False
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d3_entered"] is False
    assert audit["d4_entered"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["boundary"] == BOUNDARY


def test_d2_rejects_unready_d0_or_d1_inputs() -> None:
    d0 = _d0_container()
    d0["ready"] = False
    d0["complete_d_container"] = {"package_x_coordinates_used": True}
    d1 = _d1_support()
    d1["candidate_support"] = {"equivalent_finite_set": "too small"}
    d1["local_c_d_rows_built"] = True

    audit = audit_rank_zero_aa_bb_d2_local_c_d_row_characterization(
        d0_container=d0,
        d1_support=d1,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "d0_container_not_ready",
        "d0_complete_d_container_missing",
        "d0_product_relation_missing",
        "d0_uses_package_x_coordinates",
        "d1_support_not_exact_S_D1",
        "d1_already_built_local_rows",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d2_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    d1 = tmp_path / "d1.json"
    out = tmp_path / "d2.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    d1.write_text(json.dumps(_d1_support()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d2_local_c_d_row_characterization.py",
            "--d0-container",
            str(d0),
            "--d1-support",
            str(d1),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d2_status=row_obligations_framed" in result.stdout
    assert "local_c_d_rows_solved=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["local_row_obligations"][0]["place_type"] == "ell|L"
    assert payload["full_c_d_matrix_built"] is False
