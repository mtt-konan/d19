from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (  # noqa: E501
    build_wl481_m_tail_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl482_m_tail_kernel_classification_gate import (  # noqa: E501
    build_wl482_m_tail_kernel_classification_gate,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl483_local_hilbert_row_decision_gate import (  # noqa: E501
    build_wl483_local_hilbert_row_decision_gate,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl484_u3_obstruction_route_entry_audit import (  # noqa: E501
    build_wl484_u3_obstruction_route_entry_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl485_explicit_cd_cover_equation_instantiation import (  # noqa: E501
    build_wl485_explicit_cd_cover_equation_instantiation,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl486_local_solubility_gate import (
    build_wl486_local_solubility_gate,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl487_route_impact_of_global_point import (  # noqa: E501
    build_wl487_route_impact_of_global_point,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl488_select_next_complete_d_coordinate_route_after_u3_global_point import (  # noqa: E501
    build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl489_closure_pullback_common_source_constraints_for_global_c_d_point import (  # noqa: E501
    build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl490_route_impact_after_wl489_admissibility_failure import (  # noqa: E501
    build_wl490_route_impact_after_wl489_admissibility_failure,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter import (  # noqa: E501
    build_wl491_ambient_c_d_to_aa_bb_admissibility_filter,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl492_route_selection_after_admissibility_filter import (  # noqa: E501
    build_wl492_route_selection_after_admissibility_filter,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl493_candidate_queue_from_existing_m_tail_diagnostics import (  # noqa: E501
    build_wl493_candidate_queue_from_existing_m_tail_diagnostics,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl494_extend_or_refresh_m_tail_diagnostics import (  # noqa: E501
    build_wl494_extend_or_refresh_m_tail_diagnostics,
)


def _wl480_input() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D4_AA_BB_uniform_matrix_rank_bound_audit",
        "work_log": "wl480",
        "d4_status": "uniform_dim2_bound_not_forced_by_solved_rows",
        "complete_d_coordinate_order": [
            "d_minus_p",
            "d_pos_2sqrt_q",
            "d_neg_2sqrt_q",
        ],
        "local_character_matrix": {"id": "M_tail"},
        "surviving_obstruction": {"id": "M_tail_uniform_full_rank_missing"},
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _wl493() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    wl485 = build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)
    wl486 = build_wl486_local_solubility_gate(wl485=wl485)
    wl487 = build_wl487_route_impact_of_global_point(wl486=wl486)
    wl488 = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(wl487=wl487)
    wl489 = build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point(wl488=wl488)
    wl490 = build_wl490_route_impact_after_wl489_admissibility_failure(wl489=wl489)
    wl491 = build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(wl490=wl490)
    wl492 = build_wl492_route_selection_after_admissibility_filter(wl491=wl491)
    return build_wl493_candidate_queue_from_existing_m_tail_diagnostics(
        wl481=wl481,
        wl482=wl482,
        wl490=wl490,
        wl491=wl491,
        wl492=wl492,
    )


def _wl494() -> dict[str, object]:
    return build_wl494_extend_or_refresh_m_tail_diagnostics(
        wl480=_wl480_input(),
        wl493=_wl493(),
        grid_bound=4,
    )


def test_wl494_refreshes_m_tail_on_bounded_primitive_aa_bb_grid() -> None:
    audit = _wl494()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL494_extend_or_refresh_M_tail_diagnostics"
    assert audit["work_log"] == "wl494"
    assert audit["input_work_logs"] == ["wl480", "wl493"]
    assert audit["refresh_method"] == {
        "kind": "deterministic_primitive_AA_BB_sample_grid",
        "grid_bound": 4,
        "sides": ["AA", "BB"],
        "primitive_condition": "gcd(A,B)=1",
        "sample_order": "side, then A ascending, then B ascending",
        "uses_existing_wl481_matrix_builder": True,
        "sample_expansion_is_not_uniform_proof": True,
    }
    assert audit["sample_summary"] == {
        "sample_count": 22,
        "full_rank_sample_count": 14,
        "kernel_sample_count": 8,
        "kernel_support_entry_count": 8,
        "active_new_support_entry_count": 6,
        "processed_or_excluded_u3_entry_count": 2,
        "unique_active_supports": ["v_5"],
    }


def test_wl494_reports_active_new_support_entries_without_routing_them() -> None:
    audit = _wl494()

    active_ids = [entry["candidate_id"] for entry in audit["active_new_kernel_supports"]]
    assert active_ids == [
        "AA_A1_B4_v_5_m_tail_refresh_candidate",
        "AA_A2_B3_v_5_m_tail_refresh_candidate",
        "AA_A4_B1_v_5_m_tail_refresh_candidate",
        "BB_A1_B4_v_5_m_tail_refresh_candidate",
        "BB_A3_B2_v_5_m_tail_refresh_candidate",
        "BB_A4_B1_v_5_m_tail_refresh_candidate",
    ]
    first = audit["active_new_kernel_supports"][0]
    assert first["candidate_support"] == ["v_5"]
    assert first["sample"] == {
        "side": "AA",
        "A": 1,
        "B": 4,
        "L": 1,
        "T": 5,
        "sqrt_q": 29,
        "primitive": True,
    }
    assert first["routing_state"] == {
        "ambient_c_d_global_solubility_status": "not_tested_here",
        "aa_bb_admissibility_status": "not_tested_here",
        "ledger_route": "refreshed_m_tail_support_pending_ambient_C_d_solubility",
        "blocking_reasons": [],
    }
    assert first["required_next_gate"] == (
        "route_refreshed_support_through_ambient_C_d_solubility_then_wl491_filter"
    )


def test_wl494_preserves_processed_u3_status_from_wl493() -> None:
    audit = _wl494()

    u3_ids = [entry["candidate_id"] for entry in audit["processed_or_excluded_u3_supports"]]
    assert u3_ids == [
        "AA_A3_B1_u_3_complete_d_candidate",
        "BB_A1_B3_u_3_m_tail_refresh_candidate",
    ]
    for entry in audit["processed_or_excluded_u3_supports"]:
        assert entry["queue_status"] == "processed_or_excluded_u3_support"
        assert entry["candidate_support"] == ["u_3"]
        assert entry["routing_state"]["ambient_c_d_global_solubility_status"] == (
            "globally_soluble"
        )
        assert entry["routing_state"]["aa_bb_admissibility_status"] == "not_admissible"
        assert entry["routing_state"]["ledger_route"] == (
            "globally_soluble_but_not_aa_bb_admissible_ledger"
        )


def test_wl494_stops_at_refresh_and_keeps_forbidden_claims_false() -> None:
    audit = _wl494()

    assert audit["diagnostic_refresh_built_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["ambient_c_d_solubility_proved_for_new_candidate_here"] is False
    assert audit["aa_bb_admissibility_proved_for_new_candidate_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["stop_after_current_task"] is True
    assert audit["advance_to_wl495"] is False


def test_wl494_cli_writes_result_json(tmp_path: Path) -> None:
    wl480 = tmp_path / "wl480.json"
    wl493 = tmp_path / "wl493.json"
    out = tmp_path / "wl494.json"
    wl480.write_text(json.dumps(_wl480_input()), encoding="utf-8")
    wl493.write_text(json.dumps(_wl493()), encoding="utf-8")

    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl494_extend_or_refresh_m_tail_diagnostics.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl480",
            str(wl480),
            "--wl493",
            str(wl493),
            "--grid-bound",
            "4",
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
    assert "work_log=wl494" in result.stdout
    assert "active_new_support_entry_count=6" in result.stdout
    assert payload["work_log"] == "wl494"
    assert payload["diagnostic_refresh_built_here"] is True
