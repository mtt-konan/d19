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


def _route_state() -> dict[str, dict[str, object]]:
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
    return {"wl493": wl493, "wl494": wl494, "wl495": wl495, "wl496": wl496}


def _wl497() -> dict[str, object]:
    state = _route_state()
    return build_wl497_post_wl496_route_choice_audit(
        wl493=state["wl493"],
        wl494=state["wl494"],
        wl495=state["wl495"],
        wl496=state["wl496"],
    )


def test_wl497_summarizes_disposed_u3_and_bounded_v5_route_state() -> None:
    audit = _wl497()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL497_post_wl496_route_choice_audit"
    assert audit["work_log"] == "wl497"
    assert audit["input_work_logs"] == ["wl493", "wl494", "wl495", "wl496"]
    assert audit["post_wl496_route_state_summary"] == {
        "u3_active_unprocessed_candidate_count_after_wl493": 0,
        "u3_processed_or_deprioritized_count_after_wl493": 1,
        "bounded_v5_active_support_entry_count_from_wl494": 6,
        "bounded_v5_routed_not_admissible_count_from_wl495": 4,
        "bounded_v5_refuted_ambient_count_from_wl496": 2,
        "bounded_v5_still_deferred_count_after_wl496": 0,
        "aa_bb_admissible_count_after_wl496": 0,
        "active_candidate_count_after_wl496": 0,
    }


def test_wl497_selects_structured_m_tail_extension_and_does_not_enter_it() -> None:
    audit = _wl497()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "structure_next_M_tail_diagnostic_extension"
    assert selected["entered_here"] is False
    assert selected["new_grid_refreshed_here"] is False
    assert selected["m_tail_diagnostics_extended_here"] is False
    assert selected["required_exclusions"] == [
        "do_not_reenter_u_3",
        "do_not_reopen_bounded_v_5_entries_from_wl494_wl496",
    ]
    assert selected["required_route_for_future_new_support"] == [
        "M_tail_support",
        "ambient_C_d_global_solubility",
        "wl491_AA_BB_admissibility_filter",
        "admissible_or_not_admissible_or_refuted_ledger",
    ]
    assert audit["route_options"]["structure_or_extend_M_tail_diagnostics"][
        "decision"
    ] == "selected_next_narrow_gate"
    assert audit["route_options"]["summarize_current_route_impact"][
        "decision"
    ] == "defer_as_documentation_only"
    assert audit["route_options"]["return_to_theorem_level_local_row_work"][
        "decision"
    ] == "defer_until_a_structured_M_tail_gap_or_candidate_requires_it"


def test_wl497_stops_without_executing_wl498_or_forbidden_work() -> None:
    audit = _wl497()

    assert audit["post_wl496_route_choice_made_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_grid_refreshed_here"] is False
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
    assert audit["advance_to_wl498"] is False
    assert audit["stop_after_current_task"] is True


def test_wl497_cli_writes_result_json(tmp_path: Path) -> None:
    state = _route_state()
    paths: dict[str, Path] = {}
    for name, payload in state.items():
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        paths[name] = path
    out = tmp_path / "wl497.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl497_post_wl496_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl493",
            str(paths["wl493"]),
            "--wl494",
            str(paths["wl494"]),
            "--wl495",
            str(paths["wl495"]),
            "--wl496",
            str(paths["wl496"]),
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
    assert "work_log=wl497" in result.stdout
    assert "selected_gate=structure_next_M_tail_diagnostic_extension" in result.stdout
    assert "advance_to_wl498=False" in result.stdout
    assert payload["work_log"] == "wl497"
