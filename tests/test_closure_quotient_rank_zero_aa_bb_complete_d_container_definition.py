from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_complete_d_container_definition import (
    BOUNDARY,
    audit_rank_zero_aa_bb_complete_d_container_definition,
)


def _route_pivot() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "route_decision": {
            "selected_route": "build_minimal_C_d_local_solubility_matrix",
            "stop_after_route_pivot_audit": True,
        },
        "next_lemmas": [
            {
                "id": "D0_complete_d_container_definition",
                "status": "next_to_prove",
                "claim_status": "not_proved_here",
            },
            {
                "id": "D1_relevant_place_support_confinement",
                "status": "next_to_prove",
                "claim_status": "not_proved_here",
            },
        ],
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "full_c_d_matrix_built": False,
    }


def _complete_two_descent_recast() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "complete_two_descent_coordinates": {
            "ambient_relation": (
                "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 "
                "in Q*/Q*2"
            ),
        },
        "torsion_kummer_images": {
            "O": ["1", "1", "1"],
            "T_minus_p": [
                "(-p-2*sqrt_q)*(-p+2*sqrt_q)",
                "-p-2*sqrt_q",
                "-p+2*sqrt_q",
            ],
            "T_pos_2sqrt_q": [
                "2*sqrt_q+p",
                "(2*sqrt_q+p)*(4*sqrt_q)",
                "4*sqrt_q",
            ],
            "T_neg_2sqrt_q": [
                "-2*sqrt_q+p",
                "-4*sqrt_q",
                "(-2*sqrt_q+p)*(-4*sqrt_q)",
            ],
        },
    }


def _h2_coordinate_equivalence() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "h2_verdict": {
            "status": "refuted",
            "coordinate_equivalence_proved": False,
            "coordinate_equivalence_refuted": True,
        },
        "torsion_and_exceptional_roots": {
            "torsion_representatives_checked": [
                "O",
                "T_minus_p",
                "T_pos_2sqrt_q",
                "T_neg_2sqrt_q",
            ],
            "exceptional_root_cases_rescue_equivalence": False,
        },
    }


def test_d0_defines_complete_d_container_with_product_relation_only() -> None:
    audit = audit_rank_zero_aa_bb_complete_d_container_definition(
        route_pivot=_route_pivot(),
        complete_two_descent_recast=_complete_two_descent_recast(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D0_complete_d_container_definition"
    assert audit["d0_status"] == "framed_definition"
    assert audit["complete_d_container"] == {
        "name": "D0_complete_d_prelocal_container",
        "ambient_squareclass_quotient": (
            "V = Q*/Q*2; triples are in V^3 and multiplied coordinatewise"
        ),
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
        "relation_plane_dimension": 2,
        "covers_represented_symbolically": "C_d",
        "local_c_d_rows_built": False,
        "package_x_coordinates_used": False,
        "old_s_tilde_used_as_container": False,
    }


def test_d0_places_rational_two_torsion_baseline_in_same_quotient() -> None:
    audit = audit_rank_zero_aa_bb_complete_d_container_definition(
        route_pivot=_route_pivot(),
        complete_two_descent_recast=_complete_two_descent_recast(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
    )

    assert audit["torsion_kummer_baseline"] == {
        "source": "E_L[2](Q) inside the complete d-coordinate quotient",
        "same_quotient_as_container": True,
        "baseline_dimension": 2,
        "representative_order": [
            "O",
            "T_minus_p",
            "T_pos_2sqrt_q",
            "T_neg_2sqrt_q",
        ],
        "representatives": {
            "O": ["1", "1", "1"],
            "T_minus_p": [
                "(-p-2*sqrt_q)*(-p+2*sqrt_q)",
                "-p-2*sqrt_q",
                "-p+2*sqrt_q",
            ],
            "T_pos_2sqrt_q": [
                "2*sqrt_q+p",
                "(2*sqrt_q+p)*(4*sqrt_q)",
                "4*sqrt_q",
            ],
            "T_neg_2sqrt_q": [
                "-2*sqrt_q+p",
                "-4*sqrt_q",
                "(-2*sqrt_q+p)*(-4*sqrt_q)",
            ],
        },
        "product_relation_verified_for_representatives": True,
        "baseline_generators": ["T_minus_p", "T_pos_2sqrt_q"],
        "generator_sum_relation": "T_minus_p*T_pos_2sqrt_q=T_neg_2sqrt_q in V^3",
        "baseline_not_quotiented_out": True,
    }


def test_d0_records_exceptional_root_representatives_without_package_x_collapse() -> None:
    audit = audit_rank_zero_aa_bb_complete_d_container_definition(
        route_pivot=_route_pivot(),
        complete_two_descent_recast=_complete_two_descent_recast(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
    )

    assert audit["exceptional_root_representatives"] == {
        "standard_rule": (
            "At X=e_i, replace the vanishing d_i coordinate by the product of "
            "the two nonzero root differences."
        ),
        "root_labels": {
            "T_minus_p": "e_minus=-p",
            "T_pos_2sqrt_q": "e_pos=2*sqrt_q",
            "T_neg_2sqrt_q": "e_neg=-2*sqrt_q",
        },
        "representatives_are_complete_d_data": True,
        "package_x_collapse_not_used": True,
        "root_cases_included": [
            "T_minus_p",
            "T_pos_2sqrt_q",
            "T_neg_2sqrt_q",
        ],
    }


def test_d0_stops_before_local_rows_and_selmer_claims() -> None:
    audit = audit_rank_zero_aa_bb_complete_d_container_definition(
        route_pivot=_route_pivot(),
        complete_two_descent_recast=_complete_two_descent_recast(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
    )

    assert audit["d1_entered"] is False
    assert audit["d2_entered"] is False
    assert audit["d3_entered"] is False
    assert audit["d4_entered"] is False
    assert audit["local_c_d_rows_built"] is False
    assert audit["full_c_d_matrix_built"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["do_not_proceed_to"] == [
        "D1_relevant_place_support_confinement",
        "D2_local_C_d_row_characterization",
        "D3_torsion_baseline_in_d_coordinates",
        "D4_AA_BB_uniform_matrix_rank_bound",
    ]
    assert audit["boundary"] == BOUNDARY


def test_d0_requires_ready_pivot_recast_and_h2_refutation() -> None:
    route_pivot = _route_pivot()
    route_pivot["ready"] = False
    recast = _complete_two_descent_recast()
    recast["complete_two_descent_coordinates"] = {}
    h2 = _h2_coordinate_equivalence()
    h2["h2_verdict"] = {"status": "open"}

    audit = audit_rank_zero_aa_bb_complete_d_container_definition(
        route_pivot=route_pivot,
        complete_two_descent_recast=recast,
        h2_coordinate_equivalence=h2,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "route_pivot_not_ready",
        "complete_d_product_relation_missing",
        "h2_coordinate_equivalence_not_refuted",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d0_cli_writes_scoped_result(tmp_path: Path) -> None:
    route_pivot = tmp_path / "route_pivot.json"
    recast = tmp_path / "recast.json"
    h2 = tmp_path / "h2.json"
    out = tmp_path / "d0.json"
    route_pivot.write_text(json.dumps(_route_pivot()), encoding="utf-8")
    recast.write_text(json.dumps(_complete_two_descent_recast()), encoding="utf-8")
    h2.write_text(json.dumps(_h2_coordinate_equivalence()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_complete_d_container_definition.py",
            "--route-pivot",
            str(route_pivot),
            "--complete-two-descent-recast",
            str(recast),
            "--h2-coordinate-equivalence",
            str(h2),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d0_status=framed_definition" in result.stdout
    assert "local_c_d_rows_built=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["complete_d_container"]["name"] == "D0_complete_d_prelocal_container"
    assert payload["torsion_kummer_baseline"]["same_quotient_as_container"] is True
