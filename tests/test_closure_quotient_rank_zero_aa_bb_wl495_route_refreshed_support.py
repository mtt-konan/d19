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


def _route_inputs() -> tuple[dict[str, object], dict[str, object]]:
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
    return wl491, wl494


def _wl495() -> dict[str, object]:
    wl491, wl494 = _route_inputs()
    return build_wl495_route_refreshed_support_through_ambient_c_d_solubility_then_wl491_filter(
        wl491=wl491,
        wl494=wl494,
    )


def test_wl495_routes_all_refreshed_v5_entries_in_wl494_order() -> None:
    audit = _wl495()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL495_route_refreshed_support_through_ambient_C_d_solubility_then_wl491_filter"
    )
    assert audit["work_log"] == "wl495"
    assert audit["input_work_logs"] == ["wl491", "wl494"]
    assert audit["route_summary"] == {
        "active_refreshed_support_entry_count": 6,
        "ambient_globally_soluble_count": 4,
        "ambient_global_solubility_refuted_count": 0,
        "ambient_global_solubility_deferred_count": 2,
        "wl491_filter_applied_count": 4,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 4,
        "aa_bb_missing_pullback_data_count": 0,
        "aa_bb_filter_deferred_count": 2,
    }
    assert [entry["candidate_id"] for entry in audit["routed_refreshed_supports"]] == [
        "AA_A1_B4_v_5_m_tail_refresh_candidate",
        "AA_A2_B3_v_5_m_tail_refresh_candidate",
        "AA_A4_B1_v_5_m_tail_refresh_candidate",
        "BB_A1_B4_v_5_m_tail_refresh_candidate",
        "BB_A3_B2_v_5_m_tail_refresh_candidate",
        "BB_A4_B1_v_5_m_tail_refresh_candidate",
    ]


def test_wl495_instantiates_complete_c_d_cover_data_for_each_support() -> None:
    audit = _wl495()
    first = audit["routed_refreshed_supports"][0]

    assert first["candidate_support"] == ["v_5"]
    assert first["complete_c_d_cover"]["d_vector"] == {
        "d_minus_p": 5,
        "d_pos_2sqrt_q": 1,
        "d_neg_2sqrt_q": 5,
    }
    assert first["complete_c_d_cover"]["parameters"] == {
        "p": -42,
        "q": 841,
        "sqrt_q": 29,
    }
    assert first["complete_c_d_cover"]["root_data"] == {
        "e_minus": {"symbolic": "-p", "value": 42},
        "e_pos": {"symbolic": "2*sqrt_q", "value": 58},
        "e_neg": {"symbolic": "-2*sqrt_q", "value": -58},
    }
    assert first["complete_c_d_cover"]["x_coordinate_relations"][0][
        "instantiated_equation"
    ] == "X - 42 = 5*u_minus_p^2"
    assert first["complete_c_d_cover"]["two_independent_equations"] == [
        "5*u_minus_p^2 - u_pos_2sqrt_q^2 = 16",
        "5*u_minus_p^2 - 5*u_neg_2sqrt_q^2 = -100",
    ]


def test_wl495_applies_wl491_only_after_exact_global_c_d_witness() -> None:
    audit = _wl495()
    first = audit["routed_refreshed_supports"][0]

    assert first["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
    assert first["ambient_c_d_global_solubility"]["certificate_type"] == (
        "exact_integral_point_on_C_d"
    )
    assert first["ambient_c_d_global_solubility"]["point_on_cover"] == {
        "X": 122,
        "u_minus_p": 4,
        "u_pos_2sqrt_q": 8,
        "u_neg_2sqrt_q": 6,
    }
    assert first["ambient_c_d_global_solubility"]["induced_point_on_E_L"] == {
        "X": 122,
        "Y": 960,
    }
    assert first["wl491_filter_result"]["output_class"] == "not_admissible"
    assert first["wl491_filter_result"]["centered_even_pullback_check"]["values"] == {
        "t": "6",
        "z": "25",
        "N": "11/2",
        "M": "-1/2",
        "quartic_y": "25/4",
    }
    assert first["routing_state"]["ledger_route"] == (
        "globally_soluble_but_not_aa_bb_admissible_ledger"
    )


def test_wl495_routes_unfinished_entries_to_deferred_ledgers_without_filtering() -> None:
    audit = _wl495()
    deferred = [
        entry
        for entry in audit["routed_refreshed_supports"]
        if entry["ambient_c_d_global_solubility"]["status"] == "global_solubility_deferred"
    ]

    assert [entry["candidate_id"] for entry in deferred] == [
        "AA_A4_B1_v_5_m_tail_refresh_candidate",
        "BB_A1_B4_v_5_m_tail_refresh_candidate",
    ]
    for entry in deferred:
        assert entry["wl491_filter_result"]["output_class"] == "not_applied"
        assert entry["routing_state"] == {
            "ambient_c_d_global_solubility_status": "global_solubility_deferred",
            "aa_bb_admissibility_status": "not_applied_ambient_global_solubility_unproved",
            "ledger_route": "ambient_c_d_solubility_deferred_ledger",
            "blocking_reasons": ["ambient_C_d_global_point_not_established"],
        }


def test_wl495_stops_before_wl496_and_keeps_forbidden_claims_false() -> None:
    audit = _wl495()

    assert audit["route_audit_built_here"] is True
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["candidate_selected_here"] is False
    assert audit["advance_to_wl496"] is False
    assert audit["stop_after_current_task"] is True


def test_wl495_cli_writes_result_json(tmp_path: Path) -> None:
    wl491, wl494 = _route_inputs()
    wl491_path = tmp_path / "wl491.json"
    wl494_path = tmp_path / "wl494.json"
    out = tmp_path / "wl495.json"
    wl491_path.write_text(json.dumps(wl491), encoding="utf-8")
    wl494_path.write_text(json.dumps(wl494), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491_path),
            "--wl494",
            str(wl494_path),
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
    assert "work_log=wl495" in result.stdout
    assert "ambient_globally_soluble_count=4" in result.stdout
    assert "advance_to_wl496=False" in result.stdout
    assert payload["work_log"] == "wl495"
