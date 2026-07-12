from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))


def _module():
    return importlib.import_module("scripts.theory.aa_bb.wl586_route_selection")


def _wl505_input() -> dict[str, object]:
    rows = []
    for candidate_id, support, sample, params, d_vector, roots, point, y_coord in (
        (
            "AA_A7_B2_u_7_m_tail_shell7_candidate",
            ["u_7"],
            {"A": 7, "B": 2, "side": "AA"},
            {"p": 230},
            {"d_minus_p": 7, "d_pos_2sqrt_q": 7, "d_neg_2sqrt_q": 1},
            {"e_minus": -230, "e_pos": 554, "e_neg": -554},
            {"X": 1562, "u_minus_p": 16, "u_pos_2sqrt_q": 12, "u_neg_2sqrt_q": 46},
            61824,
        ),
        (
            "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
            ["u_3", "v_5", "w_17"],
            {"A": 3, "B": 7, "side": "AA"},
            {"p": -128},
            {"d_minus_p": 15, "d_pos_2sqrt_q": 51, "d_neg_2sqrt_q": 85},
            {"e_minus": 128, "e_pos": 272, "e_neg": -272},
            {"X": 1088, "u_minus_p": 8, "u_pos_2sqrt_q": 4, "u_neg_2sqrt_q": 4},
            32640,
        ),
    ):
        rows.append(
            {
                "candidate_id": candidate_id,
                "candidate_support": support,
                "sample": sample,
                "complete_c_d_cover": {
                    "parameters": params,
                    "d_vector": d_vector,
                    "root_data": {
                        key: {"value": value} for key, value in roots.items()
                    },
                },
                "ambient_c_d_global_solubility": {
                    "point_on_cover": point,
                    "induced_point_on_E_L": {"Y": y_coord},
                },
            }
        )
    return {
        "status": "ok",
        "ready": True,
        "work_log": "wl505",
        "route_summary": {"wl491_filter_applied_count": 8},
        "routed_active_shell7_supports": rows,
    }


def _inputs() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    module = _module()
    taxonomy = []
    inventory = []
    for row in module.REPRESENTATIVES:
        taxonomy.append(
            {
                "cover_family": row["cover_family"],
                "support_family": row["support_family"],
                "classification": "globally_soluble_but_not_aa_bb_admissible",
                "failure_mode": "common_source_aa_bb_admissibility_failure",
                "entry_count": 2,
                "cover_summary": {
                    "L": row["L"],
                    "T": row["T"],
                    "d_vector": row["d_vector"],
                },
            }
        )
        inventory.append(
            {
                "cover_family": row["cover_family"],
                "source_sides_to_map": ["AA", "BB"],
                "cover_family_model_availability": {
                    "status": "label_and_l_t_d_vector_only_no_explicit_function_field_model",
                    "available_data": {
                        "L": row["L"],
                        "T": row["T"],
                        "d_vector": row["d_vector"],
                    },
                },
            }
        )
    for index in range(12):
        inventory.append({"cover_family": f"unused-{index}"})
    wl522 = {
        "status": "ok",
        "ready": True,
        "work_log": "wl522",
        "taxonomy_summary": {
            "globally_soluble_but_not_aa_bb_admissible_cover_family_count": 15,
            "globally_soluble_but_not_aa_bb_admissible_entry_count": 29,
        },
        "support_cover_taxonomy": taxonomy,
    }
    wl527 = {
        "status": "ok",
        "ready": True,
        "work_log": "wl527",
        "cover_family_proof_data_inventory": inventory,
        "proof_data_readiness_decision": {
            "ready_for_later_uniform_squareclass_proof_attempt": False,
            "exact_missing_data_class": (
                "uniform_function_field_model_maps_and_squareclass_certificate"
            ),
        },
    }
    return _wl505_input(), wl522, wl527


def test_wl586_certifies_route_death_and_cross_family_switch() -> None:
    wl505, wl522, wl527 = _inputs()
    payload = _module().build_wl586_cross_family_truth_audit_and_pure_v_ell_route_death(
        wl505=wl505, wl522=wl522, wl527=wl527
    )
    assert payload["status"] == "ok"
    assert payload["accepted_outcome"] == "route_death_certificate"
    assert len(payload["representative_cover_family_comparison"]) == 3
    assert all(
        row["taxonomy_verified"]
        for row in payload["representative_cover_family_comparison"]
    )
    review = payload["quartic_refinement_read_only_review"]
    assert review["verdict"] == "automatic_collapse_to_existing_gaussian_data"
    assert review["independent_invariant"] is False
    assert review["wl588_permitted_by_stop_rule"] is False
    decision = payload["route_decision"]
    assert decision["reenter_wl535_now"] is False
    assert decision["pure_v_ell_equivalent_model_route"] == "route_dead"
    assert decision["pure_v_ell_parameter_character_route"] == "route_dead"
    assert (
        decision["representative_only_divisor_parity_route"]
        == "route_dead_as_uniform_exclusion"
    )
    assert decision["wl588_created"] is False
    assert decision["cross_family_generic_invariant_proved_here"] is True
    assert decision["selected_next_route"] == "none_without_parameterized_family_level_input"
    certificates = payload["cross_family_generic_squareclass_certificates"]
    assert len(certificates) == 2
    assert all(row["certified"] for row in certificates)
    assert all(row["geometrically_integral_biquadratic_cover"] for row in certificates)
    assert all(row["function_field_squareclass"] == "nonsquare" for row in certificates)
    assert payload["generic_vs_uniform_boundary"] == {
        "same_function_definition_on_two_cover_families": True,
        "function_field_nonsquare_on_two_cover_families": True,
        "all_rational_specializations_nonsquare_proved": False,
        "uniform_aa_bb_exclusion_invariant_proved": False,
        "reason": (
            "a nonsquare function-field element may specialize to a square; "
            "each square-specialization locus is a new double cover"
        ),
    }
    assert payload["equivalent_model_created_here"] is False
    assert payload["quotient_created_here"] is False
    assert payload["advance_to_m3"] is False


def test_wl586_fails_closed_on_representative_drift() -> None:
    wl505, wl522, wl527 = _inputs()
    wl522["support_cover_taxonomy"][0]["cover_summary"]["T"] = 999
    payload = _module().build_wl586_cross_family_truth_audit_and_pure_v_ell_route_death(
        wl505=wl505, wl522=wl522, wl527=wl527
    )
    assert payload["status"] == "issues"
    assert any(item.startswith("representative_mismatch:") for item in payload["violations"])


def test_wl586_cli_strict(tmp_path: Path) -> None:
    wl505, wl522, wl527 = _inputs()
    wl505_path = tmp_path / "wl505.json"
    wl522_path = tmp_path / "wl522.json"
    wl527_path = tmp_path / "wl527.json"
    out = tmp_path / "wl586.json"
    wl505_path.write_text(json.dumps(wl505), encoding="utf-8")
    wl522_path.write_text(json.dumps(wl522), encoding="utf-8")
    wl527_path.write_text(json.dumps(wl527), encoding="utf-8")
    script = ROOT / "scripts/theory/aa_bb/wl586_route_selection.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl505",
            str(wl505_path),
            "--wl522",
            str(wl522_path),
            "--wl527",
            str(wl527_path),
            "--out",
            str(out),
            "--strict",
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "status=ok" in result.stdout
    assert "accepted_outcome=route_death_certificate" in result.stdout
    assert out.exists()


def test_wl586_fails_closed_when_wl585_is_not_ready(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wl505, wl522, wl527 = _inputs()
    module = _module()
    monkeypatch.setattr(
        module.wl585_module,
        "build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient",
        dict,
    )
    payload = module.build_wl586_cross_family_truth_audit_and_pure_v_ell_route_death(
        wl505=wl505, wl522=wl522, wl527=wl527
    )
    assert payload["status"] == "issues"
    assert "wl585_input_not_ready" in payload["violations"]
