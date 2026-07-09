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


def _wl491_input() -> dict[str, object]:
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
    return build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(wl490=wl490)


def test_wl492_audits_known_ambient_ledgers_after_filter() -> None:
    audit = build_wl492_route_selection_after_admissibility_filter(wl491=_wl491_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL492_route_selection_after_reusable_admissibility_filter"
    assert audit["work_log"] == "wl492"
    assert audit["input_work_log"] == "wl491"
    assert audit["known_ambient_filter_status"] == {
        "known_filtered_point_count": 1,
        "admissible_point_count": 0,
        "not_admissible_point_count": 1,
        "missing_pullback_data_count": 0,
        "invalid_input_count": 0,
        "unfiltered_already_known_ambient_c_d_point_count": 0,
        "current_admissible_point_ledger_entries": [],
        "globally_soluble_but_not_aa_bb_admissible_entries": [
            {
                "candidate_id": "AA_A3_B1_u_3_complete_d_candidate",
                "output_class": "not_admissible",
                "ledger_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
                "blocking_reasons": [
                    "BB_common_source_product_not_square",
                    "M_not_positive",
                ],
            }
        ],
    }


def test_wl492_selects_candidate_queue_before_direct_new_candidate_discovery() -> None:
    audit = build_wl492_route_selection_after_admissibility_filter(wl491=_wl491_input())

    assert audit["route_options"] == {
        "first_apply_filter_to_already_known_ambient_C_d_point_ledgers": {
            "decision": "already_exhausted_for_current_inputs",
            "reason": (
                "The only currently known ambient C_d point in the wl491 input "
                "is the u_3 regression, and wl491 already routes it as "
                "not_admissible."
            ),
        },
        "return_directly_to_M_tail_kernel_candidate_discovery": {
            "decision": "defer",
            "reason": (
                "Direct discovery is allowed later, but after one killed "
                "ambient point the next controllable unit is an ordered queue "
                "from existing M_tail diagnostics, not an unscoped new pick."
            ),
        },
        "build_candidate_queue_from_existing_M_tail_diagnostics": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "The reusable filter is available and no unfiltered known "
                "ambient C_d points remain, so the next route should organize "
                "existing M_tail kernel diagnostics into a queue whose entries "
                "must still prove ambient C_d solubility and then pass the "
                "wl491 admissibility filter."
            ),
        },
    }
    assert audit["selected_next_gate"] == {
        "gate": "build_candidate_queue_from_existing_M_tail_diagnostics",
        "entered_here": False,
        "candidate_queue_built_here": False,
        "candidate_selected_here": False,
        "required_source_inputs_for_next_gate": [
            "wl481_sample_matrices_kernel_diagnostics",
            "wl482_classified_u3_support_as_already_disposed",
            "wl491_classify_ambient_c_d_point_for_aa_bb_admissibility",
        ],
        "minimum_later_question": (
            "Which existing M_tail kernel diagnostics should be queued next, "
            "with u_3 excluded or deprioritized as already globally soluble "
            "but not AA+BB-admissible?"
        ),
    }


def test_wl492_is_routing_only_and_keeps_forbidden_claims_false() -> None:
    audit = build_wl492_route_selection_after_admissibility_filter(wl491=_wl491_input())

    assert audit["routing_audit_only"] is True
    assert audit["admissibility_filter_defined_here"] is False
    assert audit["point_level_admissibility_decided_here"] is False
    assert audit["candidate_queue_built_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl493"] is False
    assert audit["stop_after_current_task"] is True


def test_wl492_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl492.json"
    wl491 = tmp_path / "wl491.json"
    wl491.write_text(json.dumps(_wl491_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl492_route_selection_after_admissibility_filter.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491),
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
    assert "selected_gate=build_candidate_queue_from_existing_M_tail_diagnostics" in result.stdout
    assert "advance_to_wl493=False" in result.stdout
    assert payload["work_log"] == "wl492"
    assert payload["input_work_log"] == "wl491"
