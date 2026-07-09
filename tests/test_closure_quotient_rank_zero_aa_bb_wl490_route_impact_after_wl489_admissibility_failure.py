from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

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


def _wl489_input() -> dict[str, Any]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    wl485 = build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)
    wl486 = build_wl486_local_solubility_gate(wl485=wl485)
    wl487 = build_wl487_route_impact_of_global_point(wl486=wl486)
    wl488 = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
        wl487=wl487
    )
    return build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point(
        wl488=wl488
    )


def test_wl490_removes_u3_from_obstruction_and_admissible_ledgers() -> None:
    audit = build_wl490_route_impact_after_wl489_admissibility_failure(
        wl489=_wl489_input()
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL490_route_impact_after_wl489_admissibility_failure"
    )
    assert audit["work_log"] == "wl490"
    assert audit["input_work_log"] == "wl489"
    assert audit["ledger_update"] == {
        "killed_candidate": {
            "candidate_id": "AA_A3_B1_u_3_complete_d_candidate",
            "d_vector": {
                "d_minus_p": 3,
                "d_pos_2sqrt_q": 3,
                "d_neg_2sqrt_q": 1,
            },
            "reason": (
                "wl489 proves this ambient global C_d point fails AA+BB "
                "common-source constraints."
            ),
        },
        "remove_from_current_obstruction_candidate_ledger": True,
        "remove_from_admissible_point_ledger": True,
        "current_obstruction_candidate_ledger_after_wl490": [],
        "admissible_point_ledger_after_wl490": [],
        "globally_soluble_but_not_aa_bb_admissible_ledger": [
            {
                "candidate_id": "AA_A3_B1_u_3_complete_d_candidate",
                "d_vector": {
                    "d_minus_p": 3,
                    "d_pos_2sqrt_q": 3,
                    "d_neg_2sqrt_q": 1,
                },
                "wl489_status": "proved_fails_for_this_explicit_point",
            }
        ],
    }


def test_wl490_selects_reusable_admissibility_filter_before_more_candidates() -> None:
    audit = build_wl490_route_impact_after_wl489_admissibility_failure(
        wl489=_wl489_input()
    )

    assert audit["route_options"] == {
        "define_reusable_ambient_C_d_to_AA_BB_admissibility_filter": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl489 killed the first ambient global C_d point by "
                "AA+BB common-source constraints, so the next controllable "
                "unit is a reusable filter that every later ambient C_d point "
                "must pass before it enters the admissible ledger."
            ),
        },
        "return_to_M_tail_kernel_classification_for_another_candidate": {
            "decision": "defer",
            "reason": (
                "Allowed later, but choosing another candidate before a "
                "reusable admissibility filter would repeat the wl489 "
                "point-specific check and blur ambient solubility with "
                "AA+BB admissibility."
            ),
        },
    }
    assert audit["selected_next_gate"] == {
        "gate": "define_reusable_ambient_C_d_to_AA_BB_admissibility_filter",
        "entered_here": False,
        "input_to_later_gate": [
            "wl489_pullback_values_N_4_M_0",
            "wl489_common_source_failure_on_BB_side",
            "complete_d_coordinate_class_(3,3,1)",
            "AA_BB_common_source_closure_equations",
        ],
        "minimum_later_question": (
            "Given an ambient global C_d point, decide whether its pullback "
            "satisfies the AA+BB common-source closure constraints before "
            "recording it as admissible."
        ),
    }


def test_wl490_is_route_impact_only_and_keeps_forbidden_claims_false() -> None:
    audit = build_wl490_route_impact_after_wl489_admissibility_failure(
        wl489=_wl489_input()
    )

    assert audit["routing_audit_only"] is True
    assert audit["point_level_admissibility_decided_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["admissibility_filter_defined_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl491"] is False
    assert audit["stop_after_current_task"] is True


def test_wl490_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl490.json"
    wl489 = tmp_path / "wl489.json"
    wl489.write_text(json.dumps(_wl489_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl490_route_impact_after_wl489_admissibility_failure.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl489",
            str(wl489),
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
    assert (
        "selected_gate=define_reusable_ambient_C_d_to_AA_BB_admissibility_filter"
        in result.stdout
    )
    assert "advance_to_wl491=False" in result.stdout
    assert payload["work_log"] == "wl490"
    assert payload["input_work_log"] == "wl489"
