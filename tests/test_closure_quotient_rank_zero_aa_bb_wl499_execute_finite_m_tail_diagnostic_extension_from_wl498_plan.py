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
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support import (
    build_wl495_route_refreshed_support_through_ambient_c_d_solubility_then_wl491_filter,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers import (  # noqa: E501
    build_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl497_post_wl496_route_choice_audit import (  # noqa: E501
    build_wl497_post_wl496_route_choice_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan import (  # noqa: E501
    build_wl498_structure_next_m_tail_diagnostic_extension_plan,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan import (  # noqa: E501
    build_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan,
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


def _wl498() -> dict[str, object]:
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
    wl493 = build_wl493_candidate_queue_from_existing_m_tail_diagnostics(
        wl481=wl481,
        wl482=wl482,
        wl490=wl490,
        wl491=wl491,
        wl492=wl492,
    )
    wl494 = build_wl494_extend_or_refresh_m_tail_diagnostics(
        wl480=_wl480_input(),
        wl493=wl493,
        grid_bound=4,
    )
    wl495 = build_wl495_route_refreshed_support_through_ambient_c_d_solubility_then_wl491_filter(
        wl491=wl491,
        wl494=wl494,
    )
    wl496 = build_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers(
        wl495=wl495,
    )
    wl497 = build_wl497_post_wl496_route_choice_audit(
        wl493=wl493,
        wl494=wl494,
        wl495=wl495,
        wl496=wl496,
    )
    return build_wl498_structure_next_m_tail_diagnostic_extension_plan(wl497=wl497)


def _wl499() -> dict[str, object]:
    return build_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan(
        wl480=_wl480_input(),
        wl498=_wl498(),
        shell_bound=5,
    )


def test_wl499_executes_exactly_one_declared_primitive_shell() -> None:
    audit = _wl499()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL499_execute_finite_M_tail_diagnostic_extension_from_wl498_plan"
    assert audit["work_log"] == "wl499"
    assert audit["input_work_logs"] == ["wl480", "wl498"]
    assert audit["declared_extension_scope"] == {
        "extension_unit": "finite_primitive_shell",
        "shell_bound": 5,
        "shell_axis": "max(A,B)",
        "sides": ["AA", "BB"],
        "primitive_condition": "gcd(A,B)=1",
        "sample_order": "side, then A ascending, then B ascending",
        "sample_count": 16,
        "uses_existing_wl481_matrix_builder": True,
    }
    assert audit["sample_summary"] == {
        "sample_count": 16,
        "full_rank_sample_count": 14,
        "kernel_sample_count": 2,
        "kernel_support_entry_count": 2,
        "active_new_support_entry_count": 2,
        "excluded_duplicate_or_processed_support_entry_count": 0,
        "unique_active_supports": ["u_5"],
    }


def test_wl499_reports_only_m_tail_diagnostic_outputs_for_new_shell_supports() -> None:
    audit = _wl499()

    active_ids = [entry["candidate_id"] for entry in audit["active_new_kernel_supports"]]
    assert active_ids == [
        "AA_A5_B3_u_5_m_tail_shell5_candidate",
        "BB_A3_B5_u_5_m_tail_shell5_candidate",
    ]
    assert audit["excluded_duplicate_or_processed_supports"] == []

    first = audit["active_new_kernel_supports"][0]
    assert first["candidate_support"] == ["u_5"]
    assert first["sample"] == {
        "side": "AA",
        "A": 5,
        "B": 3,
        "L": 5,
        "T": 8,
        "sqrt_q": 164,
        "primitive": True,
    }
    assert first["route_key"] == {
        "source_quotient": "AA",
        "A": 5,
        "B": 3,
        "L": 5,
        "T": 8,
        "candidate_support": ["u_5"],
    }
    assert first["duplicate_guard_result"] == {
        "route_key": first["route_key"],
        "is_duplicate_route_key": False,
        "matches_processed_support_family": False,
        "matches_bounded_disposed_entry": False,
        "genuinely_new_support": True,
        "guard_action": "record_active_new_kernel_support",
        "support_family_status": "new_support_family",
    }
    assert first["routing_state"] == {
        "ambient_c_d_global_solubility_status": "not_tested_here",
        "aa_bb_admissibility_status": "not_applied_here",
        "ledger_route": "m_tail_shell_support_pending_ambient_C_d_solubility",
        "blocking_reasons": [],
    }
    assert first["required_next_gate"] == (
        "route_active_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter"
    )


def test_wl499_uses_wl498_duplicate_guard_without_testing_c_d_or_wl491() -> None:
    audit = _wl499()

    assert audit["duplicate_support_guard_summary"] == {
        "route_key_fields": [
            "source_quotient",
            "A",
            "B",
            "L",
            "T",
            "candidate_support",
        ],
        "processed_support_family_exclusion_count": 1,
        "bounded_route_key_exclusion_count": 6,
        "candidate_id_collision_exclusion_count": 6,
        "active_new_support_entry_count": 2,
        "excluded_duplicate_or_processed_support_entry_count": 0,
    }
    assert audit["m_tail_diagnostics_extended_here"] is True
    assert audit["new_supports_computed_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_here"] is False
    assert audit["aa_bb_admissibility_proved_for_new_candidate_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl500"] is False
    assert audit["stop_after_current_task"] is True


def test_wl499_cli_writes_result_json(tmp_path: Path) -> None:
    wl480 = tmp_path / "wl480.json"
    wl498 = tmp_path / "wl498.json"
    out = tmp_path / "wl499.json"
    wl480.write_text(json.dumps(_wl480_input()), encoding="utf-8")
    wl498.write_text(json.dumps(_wl498()), encoding="utf-8")

    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl480",
            str(wl480),
            "--wl498",
            str(wl498),
            "--shell-bound",
            "5",
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
    assert "work_log=wl499" in result.stdout
    assert "active_new_support_entry_count=2" in result.stdout
    assert "excluded_duplicate_or_processed_support_entry_count=0" in result.stdout
    assert payload["work_log"] == "wl499"
    assert payload["active_new_kernel_supports"][0]["candidate_support"] == ["u_5"]
