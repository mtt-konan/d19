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


def _wl497() -> dict[str, object]:
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
    return build_wl497_post_wl496_route_choice_audit(
        wl493=wl493,
        wl494=wl494,
        wl495=wl495,
        wl496=wl496,
    )


def _wl498() -> dict[str, object]:
    return build_wl498_structure_next_m_tail_diagnostic_extension_plan(wl497=_wl497())


def test_wl498_defines_allowed_parameter_axes_without_refreshing_grid() -> None:
    audit = _wl498()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL498_structure_next_M_tail_diagnostic_extension_plan"
    assert audit["work_log"] == "wl498"
    assert audit["input_work_log"] == "wl497"
    assert audit["extension_plan_built_here"] is True
    assert audit["allowed_parameter_axes"] == {
        "extension_unit": "finite_primitive_shell",
        "candidate_source": "future_M_tail_matrix_builder_only",
        "sides": ["AA", "BB"],
        "integer_parameters": ["A", "B"],
        "parameter_domain": {"A": "positive_integer", "B": "positive_integer"},
        "primitive_condition": "gcd(A,B)=1",
        "shell_axis": "max(A,B)",
        "prior_completed_shell_bound": 4,
        "allowed_future_shells": (
            "finite shells with max(A,B) > 4, declared before execution"
        ),
        "sample_order": "shell_bound ascending, side, then A ascending, then B ascending",
        "derived_fields_only_after_future_execution": [
            "L",
            "T",
            "sqrt_q",
            "M_tail_rows",
            "kernel_basis_supports",
            "complete_d_coordinate_cover_input",
        ],
    }
    assert audit["new_grid_refreshed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False


def test_wl498_records_exclusion_ledger_and_duplicate_support_guard() -> None:
    audit = _wl498()

    assert audit["exclusion_ledger"]["family_level_exclusions"] == [
        {
            "support": ["u_3"],
            "scope": "support_family",
            "reason": "already_processed_and_not_AA_BB_admissible_by_wl493_wl491",
            "future_action": "exclude_or_deprioritize_without_reentering",
        }
    ]
    assert [
        entry["candidate_id"]
        for entry in audit["exclusion_ledger"]["bounded_v5_entry_exclusions"]
    ] == [
        "AA_A1_B4_v_5_m_tail_refresh_candidate",
        "AA_A2_B3_v_5_m_tail_refresh_candidate",
        "AA_A4_B1_v_5_m_tail_refresh_candidate",
        "BB_A1_B4_v_5_m_tail_refresh_candidate",
        "BB_A3_B2_v_5_m_tail_refresh_candidate",
        "BB_A4_B1_v_5_m_tail_refresh_candidate",
    ]
    guard = audit["duplicate_support_guard"]
    assert guard["route_key_fields"] == [
        "source_quotient",
        "A",
        "B",
        "L",
        "T",
        "candidate_support",
    ]
    assert guard["duplicate_key_policy"] == (
        "same route key as exclusion ledger is not a genuinely new support"
    )
    assert guard["support_family_policy"]["u_3"] == "always_excluded_as_processed"
    assert guard["support_family_policy"]["v_5"] == (
        "exclude only bounded wl494-wl496 route keys; new shells must still "
        "be labeled existing_support_family_new_sample"
    )


def test_wl498_declares_future_schema_and_routing_contract_for_new_supports() -> None:
    audit = _wl498()

    assert audit["expected_future_extension_output_schema"] == {
        "top_level_required_fields": [
            "status",
            "ready",
            "work_log",
            "input_work_log",
            "declared_extension_scope",
            "sample_summary",
            "rank_kernel_summary_by_sample",
            "active_new_kernel_supports",
            "excluded_duplicate_or_processed_supports",
            "duplicate_support_guard_summary",
            "next_gate_after_extension",
        ],
        "candidate_entry_required_fields": [
            "candidate_id",
            "candidate_support",
            "sample",
            "route_key",
            "rank_and_row_status",
            "duplicate_guard_result",
            "routing_state",
            "required_next_gate",
        ],
        "required_false_claim_flags": [
            "candidate_selected_here",
            "new_local_row_proved_here",
            "new_c_d_solubility_tested_here",
            "complete_selmer_upper_bound_proved",
            "dim_sel2_eq_2_claimed",
            "rank_zero_claimed",
            "sha2_trivial_claimed",
        ],
    }
    assert audit["future_routing_contract_for_genuinely_new_support"] == [
        "M_tail_support",
        "ambient_C_d_global_solubility",
        "wl491_AA_BB_admissibility_filter",
        "admissible_or_not_admissible_or_refuted_ledger",
    ]
    assert audit["stop_conditions_for_future_extension"] == [
        "stop_after_finite_declared_shell_is_audited",
        "stop_if_only_duplicate_or_processed_supports_remain",
        "stop_immediately_after_recording_any_genuinely_new_support_queue",
        "do_not_test_ambient_C_d_solubility_inside_the_M_tail_extension",
        "do_not_apply_wl491_until_ambient_C_d_global_solubility_is_proved",
    ]


def test_wl498_stops_without_forbidden_work_or_wl499_advance() -> None:
    audit = _wl498()

    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_grid_refreshed_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl499"] is False
    assert audit["stop_after_current_task"] is True


def test_wl498_cli_writes_result_json(tmp_path: Path) -> None:
    wl497_path = tmp_path / "wl497.json"
    out = tmp_path / "wl498.json"
    wl497_path.write_text(json.dumps(_wl497()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl497",
            str(wl497_path),
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
    assert "work_log=wl498" in result.stdout
    assert "extension_plan_built_here=True" in result.stdout
    assert "advance_to_wl499=False" in result.stdout
    assert payload["work_log"] == "wl498"
