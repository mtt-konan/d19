from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype as wl528_module,
)

build_wl528_v5_l1_t5_function_field_prototype = (
    wl528_module.build_wl528_v5_l1_t5_function_field_prototype
)


def _wl495() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json"
        ).read_text(encoding="utf-8")
    )


def _wl528() -> dict[str, object]:
    return build_wl528_v5_l1_t5_function_field_prototype(wl495=_wl495())


def test_wl528_builds_only_the_selected_v5_l1_t5_prototype() -> None:
    audit = _wl528()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl528"
    assert audit["object_layer"] == "single_cover_family_function_field_prototype"

    scope = audit["prototype_scope"]
    assert scope == {
        "support": "v_5",
        "L": 1,
        "T": 5,
        "d_vector": {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5},
        "candidate_ids": [
            "AA_A1_B4_v_5_m_tail_refresh_candidate",
            "BB_A4_B1_v_5_m_tail_refresh_candidate",
        ],
        "touches_only_one_cover_family": True,
    }

    assert [entry["candidate_id"] for entry in audit["selected_wl495_entries"]] == [
        "AA_A1_B4_v_5_m_tail_refresh_candidate",
        "BB_A4_B1_v_5_m_tail_refresh_candidate",
    ]


def test_wl528_reconstructs_reviewable_function_field_model_and_maps() -> None:
    audit = _wl528()

    model = audit["function_field_model"]
    assert model["function_field"] == "Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))"
    assert model["cover_maps"]["u_minus_p"] == "(r^2 - 20)/(2*r)"
    assert model["cover_maps"]["u_pos_2sqrt_q"] == "y/(2*r)"
    assert model["cover_maps"]["u_neg_2sqrt_q"] == "(r^2 + 20)/(2*r)"
    assert all(check["verified_in_function_field"] is True for check in model["identity_checks"])

    maps = audit["source_side_maps_and_N_M"]
    assert maps["shared_centered_even_map"]["source_leg"] == 1
    assert maps["shared_centered_even_map"]["N"].startswith("(5 + y*(r^2+20)")
    assert maps["AA_source"]["opposite_side_product"] == "(N^2+B^2)(M^2+B^2)"
    assert maps["BB_source"]["opposite_side_product"] == "(N^2+A^2)(M^2+A^2)"


def test_wl528_proves_function_field_nonsquare_but_not_uniform_family_obstruction() -> None:
    audit = _wl528()

    product = audit["opposite_side_product"]
    certificate = product["function_field_nonsquare_certificate"]
    assert product["opposite_product_in_N_M"] == "(N^2+16)(M^2+16)"
    assert certificate["status"] == "proved"
    assert certificate["specialization"]["r"] == 10
    assert certificate["specialization"]["t"] == 6
    assert certificate["specialized_value"] == "12025/16"
    assert certificate["specialized_value_is_rational_square"] is False
    assert product["divisor_parity_certificate"]["status"] == "not_proved_here"

    proof = audit["proof_status"]
    assert proof["function_field_nonsquare_certificate_proved_here"] is True
    assert proof["divisor_parity_certificate_proved_here"] is False
    assert proof["uniform_specialization_survival_proved_here"] is False
    assert proof["uniform_cover_family_obstruction_proved_here"] is False
    assert proof["ready_as_reviewable_single_prototype"] is True
    assert proof["ready_as_uniform_cover_family_theorem"] is False


def test_wl528_specialization_certificate_prerequisites_are_executable_checks() -> None:
    audit = _wl528()

    certificate = audit["opposite_side_product"]["function_field_nonsquare_certificate"]
    checks = certificate["certificate_prerequisite_checks"]
    by_id = {check["check_id"]: check for check in checks}
    assert set(by_id) == {
        "specialization_lies_on_quartic",
        "specialization_is_smooth",
        "chart_open_denominators_nonzero",
        "maps_to_recorded_cover_point",
        "maps_to_recorded_e_point",
        "specialized_t_n_m_match_recorded_values",
        "opposite_product_matches_recorded_value",
        "opposite_product_regular_and_nonzero_at_specialization",
        "specialized_value_is_not_rational_square",
    }
    assert all(check["passed"] is True for check in checks)
    assert certificate["smooth_at_specialization"] is True
    assert certificate["nonexceptional_at_specialization"] is True
    assert certificate["regular_nonzero_at_specialization"] is True
    assert certificate["specialized_value_is_rational_square"] is False
    assert "regular and nonzero" in certificate["logic"]


def test_wl528_status_fails_when_function_field_identity_prerequisite_fails(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        wl528_module,
        "_identity_checks",
        lambda: [
            {
                "check_id": "broken_identity",
                "identity": "0 = 1",
                "verified_in_function_field": False,
            }
        ],
    )

    audit = _wl528()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "function_field_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl528_status_fails_when_recorded_specialization_data_is_inconsistent() -> None:
    wl495 = deepcopy(_wl495())
    for entry in wl495["routed_refreshed_supports"]:
        if entry["candidate_id"] in wl528_module.TARGET_CANDIDATE_IDS:
            entry["ambient_c_d_global_solubility"]["induced_point_on_E_L"]["Y"] = 961

    audit = build_wl528_v5_l1_t5_function_field_prototype(wl495=wl495)

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "specialization_certificate_prerequisite_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl528_keeps_route_boundaries_and_forbidden_claims_false() -> None:
    audit = _wl528()

    assert audit["shell11_executed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_next_cover_family"] is False
    assert audit["advance_to_next_roadmap_step"] is False
    assert audit["stop_after_current_task"] is True


def test_wl528_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl528.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl495",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json"
            ),
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
    assert "work_log=wl528" in result.stdout
    assert "function_field_nonsquare_certificate_proved_here=True" in result.stdout
    assert "uniform_cover_family_obstruction_proved_here=False" in result.stdout
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl528"
