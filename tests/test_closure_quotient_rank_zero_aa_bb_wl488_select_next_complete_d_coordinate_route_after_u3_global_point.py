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


def _wl487_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    wl485 = build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)
    wl486 = build_wl486_local_solubility_gate(wl485=wl485)
    return build_wl487_route_impact_of_global_point(wl486=wl486)


def test_wl488_classifies_what_the_u3_global_point_changes() -> None:
    audit = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
        wl487=_wl487_input()
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL488_select_next_complete_d_coordinate_route_after_u3_global_point"
    )
    assert audit["work_log"] == "wl488"
    assert audit["input_work_log"] == "wl487"
    assert audit["u3_global_point_impact"] == {
        "candidate_id": "AA_A3_B1_u_3_complete_d_candidate",
        "d_vector": {
            "d_minus_p": 3,
            "d_pos_2sqrt_q": 3,
            "d_neg_2sqrt_q": 1,
        },
        "point_classification": "non_torsion_candidate_not_visible_two_torsion_baseline",
        "changes": [
            "remove_u3_from_current_global_obstruction_candidate_ledger",
            "record_u3_as_globally_soluble_complete_d_coordinate_class_for_this_sample",
            "promote_the_next_question_from_local_obstruction_to_AA_BB_admissibility",
        ],
        "does_not_change": [
            "M_tail_uniform_full_rank_missing_remains_unproved",
            "no_new_local_or_hilbert_row_is_added",
            "visible_torsion_baseline_is_not_enlarged_here",
            "no_complete_selmer_upper_bound_or_rank_zero_conclusion_is_proved",
        ],
    }


def test_wl488_selects_closure_pullback_common_source_before_more_candidates() -> None:
    audit = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
        wl487=_wl487_input()
    )

    assert audit["route_options"] == {
        "inspect_AA_BB_closure_pullback_common_source_constraints": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "The failed u3 obstruction attempt produced a global "
                "non-baseline C_d point, so the next controllable question is "
                "whether such a point is admissible for the AA+BB common source "
                "and closure/pullback constraints."
            ),
        },
        "pick_another_M_tail_or_kernel_candidate": {
            "decision": "defer",
            "reason": (
                "wl487 did not reopen the M_tail full-rank rescue path or add a "
                "new row; moving to another kernel candidate would not explain "
                "what the global u3 point means."
            ),
        },
        "run_another_minimal_complete_C_d_obstruction_test": {
            "decision": "defer",
            "reason": (
                "Another obstruction test is allowed later, but first the route "
                "must separate globally soluble C_d classes that are AA+BB "
                "admissible from classes that only live on the ambient E_L."
            ),
        },
    }
    assert audit["selected_next_gate"] == {
        "gate": "AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point",
        "entered_here": False,
        "input_to_later_gate": [
            "wl487_u3_global_point_classification",
            "complete_d_coordinate_class_(3,3,1)",
            "AA_A3_B1_common_source_and_closure_equations",
        ],
        "minimum_later_question": (
            "Does the wl486/wl487 global point pull back to the AA+BB common "
            "source/closure constraints, or is it only an ambient E_L point?"
        ),
    }


def test_wl488_is_only_a_routing_audit_and_keeps_forbidden_claims_false() -> None:
    audit = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
        wl487=_wl487_input()
    )

    assert audit["routing_audit_only"] is True
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["stop_after_current_task"] is True


def test_wl488_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl488.json"
    wl487 = tmp_path / "wl487.json"
    wl487.write_text(json.dumps(_wl487_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl488_select_next_complete_d_coordinate_route_after_u3_global_point.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl487",
            str(wl487),
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
    assert "selected_gate=AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point" in (  # noqa: E501
        result.stdout
    )
    assert payload["work_log"] == "wl488"
    assert payload["input_work_log"] == "wl487"
    assert payload["selected_next_gate"]["entered_here"] is False
