from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d1_relevant_place_support_confinement import (  # noqa: E501
    BOUNDARY,
    audit_rank_zero_aa_bb_d1_relevant_place_support_confinement,
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
        },
        "local_c_d_rows_built": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _complete_two_descent_recast() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "full_rational_2_torsion_model": {
            "parameters": {
                "T": "A+B",
                "p": "8*L^2 - 2*T^2",
                "sqrt_q": "T^2 + 4*L^2",
            },
            "root_labels": {
                "e_minus": "-p",
                "e_pos": "2*sqrt_q",
                "e_neg": "-2*sqrt_q",
            },
        },
        "complete_two_descent_coordinates": {
            "ambient_relation": (
                "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 "
                "in Q*/Q*2"
            ),
            "difference_equations": [
                "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = p+2*sqrt_q",
                "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = p-2*sqrt_q",
                "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q",
            ],
        },
    }


def test_d1_identifies_candidate_support_from_root_differences() -> None:
    audit = audit_rank_zero_aa_bb_d1_relevant_place_support_confinement(
        d0_container=_d0_container(),
        complete_two_descent_recast=_complete_two_descent_recast(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D1_relevant_place_support_confinement"
    assert audit["d1_status"] == "framed_and_proved_support_confinement"
    assert audit["candidate_support"] == {
        "name": "S_D1_relevant_places",
        "places": {
            "archimedean": ["infinity"],
            "dyadic": ["2"],
            "odd_bad_primes_general": (
                "odd ell dividing (e_minus-e_pos)*(e_minus-e_neg)*(e_pos-e_neg)"
            ),
            "odd_bad_primes_in_parameters": (
                "odd ell dividing (p+2*sqrt_q)*(p-2*sqrt_q)*(4*sqrt_q)"
            ),
            "odd_bad_primes_AA_BB_simplified": (
                "odd ell dividing L*T*sqrt_q"
            ),
        },
        "parameter_identities": {
            "p+2*sqrt_q": "16*L^2",
            "p-2*sqrt_q": "-4*T^2",
            "4*sqrt_q": "4*(T^2+4*L^2)",
        },
        "equivalent_finite_set": (
            "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
        ),
    }


def test_d1_proves_outside_support_confinement_only_not_local_rows() -> None:
    audit = audit_rank_zero_aa_bb_d1_relevant_place_support_confinement(
        d0_container=_d0_container(),
        complete_two_descent_recast=_complete_two_descent_recast(),
    )

    assert audit["outside_support_confinement"] == {
        "claim": (
            "For odd ell not in S_D1, C_d(Q_ell) forces each d-coordinate "
            "to have even ell-adic valuation."
        ),
        "reason": (
            "At good odd primes with distinct integral roots and unit root "
            "differences, the Kummer image for full rational 2-torsion is the "
            "unramified subgroup; ramified squareclasses cannot occur."
        ),
        "consequence": (
            "Global d-coordinate candidates may be represented by "
            "S_D1-supported squareclasses before D2 writes any local C_d rows."
        ),
    }
    assert audit["local_c_d_rows_built"] is False
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d2_entered"] is False
    assert audit["d3_entered"] is False
    assert audit["d4_entered"] is False


def test_d1_keeps_all_theorem_boundaries_false() -> None:
    audit = audit_rank_zero_aa_bb_d1_relevant_place_support_confinement(
        d0_container=_d0_container(),
        complete_two_descent_recast=_complete_two_descent_recast(),
    )

    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_d1_rejects_unready_or_post_d0_inputs() -> None:
    d0 = _d0_container()
    d0["ready"] = False
    d0["local_c_d_rows_built"] = True
    recast = _complete_two_descent_recast()
    recast["complete_two_descent_coordinates"] = {}

    audit = audit_rank_zero_aa_bb_d1_relevant_place_support_confinement(
        d0_container=d0,
        complete_two_descent_recast=recast,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "d0_container_not_ready",
        "d0_already_built_local_rows",
        "complete_d_difference_equations_missing",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d1_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    recast = tmp_path / "recast.json"
    out = tmp_path / "d1.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    recast.write_text(json.dumps(_complete_two_descent_recast()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d1_relevant_place_support_confinement.py",
            "--d0-container",
            str(d0),
            "--complete-two-descent-recast",
            str(recast),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d1_status=framed_and_proved_support_confinement" in result.stdout
    assert "local_c_d_rows_built=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["candidate_support"]["equivalent_finite_set"] == (
        "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
    )
    assert payload["d2_entered"] is False
