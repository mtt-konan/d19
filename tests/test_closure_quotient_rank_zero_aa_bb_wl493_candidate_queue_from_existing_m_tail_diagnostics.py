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


def _route_inputs() -> dict[str, dict[str, object]]:
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
    return {
        "wl481": wl481,
        "wl482": wl482,
        "wl490": wl490,
        "wl491": wl491,
        "wl492": wl492,
    }


def _wl493() -> dict[str, object]:
    inputs = _route_inputs()
    return build_wl493_candidate_queue_from_existing_m_tail_diagnostics(
        wl481=inputs["wl481"],
        wl482=inputs["wl482"],
        wl490=inputs["wl490"],
        wl491=inputs["wl491"],
        wl492=inputs["wl492"],
    )


def test_wl493_builds_filter_aware_queue_from_existing_wl481_kernel_diagnostics() -> None:
    audit = _wl493()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL493_candidate_queue_from_existing_M_tail_diagnostics"
    assert audit["work_log"] == "wl493"
    assert audit["input_work_logs"] == ["wl481", "wl482", "wl490", "wl491", "wl492"]
    assert audit["queue_summary"] == {
        "kernel_support_entry_count_from_wl481": 1,
        "active_unprocessed_candidate_count": 0,
        "deprioritized_or_excluded_candidate_count": 1,
        "ordered_active_queue_empty_because": (
            "The only existing wl481 kernel support is u_3, and wl490/wl491 "
            "already route it as globally soluble but not AA+BB-admissible."
        ),
    }
    assert audit["ordered_active_candidate_queue"] == []


def test_wl493_deprioritizes_u3_with_sample_metadata_row_coverage_and_next_gate() -> None:
    audit = _wl493()
    [entry] = audit["deprioritized_or_excluded_candidates"]

    assert entry["queue_rank"] == 1
    assert entry["queue_status"] == "deprioritized_already_processed_not_admissible"
    assert entry["candidate_id"] == "AA_A3_B1_u_3_complete_d_candidate"
    assert entry["candidate_support"] == ["u_3"]
    assert entry["sample"] == {
        "side": "AA",
        "A": 3,
        "B": 1,
        "L": 3,
        "T": 4,
        "sqrt_q": 52,
        "primitive": True,
    }
    assert entry["family_metadata"] == {
        "pattern": "AA+BB",
        "source_quotient": "AA",
        "m_tail_object": "M_tail",
        "complete_d_coordinate_route": True,
        "old_package_x_s_tilde_bridge_used": False,
    }
    assert entry["known_row_coverage_status"] == {
        "wl481_computed_rank_status": "kernel_found_for_this_finite_sample",
        "wl482_final_classification": (
            "genuine_parameter_specialized_tail_obstruction_candidate"
        ),
        "known_row_ids_covering_sample": [
            "odd_L_3_equal_d_minus_p_d_pos_2sqrt_q",
            "odd_sqrt_q_13_equal_d_pos_2sqrt_q_d_neg_2sqrt_q",
            "dyadic_ordinary_d_neg_2sqrt_q_sign_character",
        ],
        "known_rows_with_nonzero_entry_on_support": [],
        "known_local_row_coverage_decision": (
            "no_known_wl475_wl478_or_wl481_row_missing_that_kills_u_3"
        ),
    }
    assert entry["routing_state"] == {
        "ambient_c_d_global_solubility_status": "globally_soluble",
        "aa_bb_admissibility_status": "not_admissible",
        "ledger_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
        "blocking_reasons": [
            "BB_common_source_product_not_square",
            "M_not_positive",
        ],
    }
    assert entry["required_next_gate"] == (
        "do_not_reenter_current_candidate_queue; extend_or_refresh_M_tail_diagnostics"
    )
    assert entry["why_queued"] == (
        "Kept only as an ordered processed/deprioritized entry so the queue "
        "audit records that the wl481 u_3 support has already become an "
        "ambient global C_d point and failed the wl491 AA+BB admissibility "
        "filter."
    )


def test_wl493_stops_at_queue_audit_and_keeps_forbidden_claims_false() -> None:
    audit = _wl493()

    assert audit["candidate_queue_built_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["ambient_c_d_solubility_proved_for_new_candidate_here"] is False
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
    assert audit["stop_after_current_task"] is True
    assert audit["advance_to_wl494"] is False


def test_wl493_cli_writes_result_json(tmp_path: Path) -> None:
    inputs = _route_inputs()
    wl481 = tmp_path / "wl481.json"
    wl482 = tmp_path / "wl482.json"
    wl490 = tmp_path / "wl490.json"
    wl491 = tmp_path / "wl491.json"
    wl492 = tmp_path / "wl492.json"
    out = tmp_path / "wl493.json"
    for name, path in [
        ("wl481", wl481),
        ("wl482", wl482),
        ("wl490", wl490),
        ("wl491", wl491),
        ("wl492", wl492),
    ]:
        path.write_text(json.dumps(inputs[name]), encoding="utf-8")

    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl493_candidate_queue_from_existing_m_tail_diagnostics.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl481",
            str(wl481),
            "--wl482",
            str(wl482),
            "--wl490",
            str(wl490),
            "--wl491",
            str(wl491),
            "--wl492",
            str(wl492),
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
    assert "work_log=wl493" in result.stdout
    assert "active_unprocessed_candidate_count=0" in result.stdout
    assert payload["work_log"] == "wl493"
    assert payload["candidate_queue_built_here"] is True
