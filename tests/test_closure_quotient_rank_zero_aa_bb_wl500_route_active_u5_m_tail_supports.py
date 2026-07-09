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
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter import (  # noqa: E501
    build_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter as build_wl500_route,  # noqa: E501
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
    wl498 = build_wl498_structure_next_m_tail_diagnostic_extension_plan(wl497=wl497)
    wl499 = build_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan(
        wl480=_wl480_input(),
        wl498=wl498,
        shell_bound=5,
    )
    return wl491, wl499


def _wl500() -> dict[str, object]:
    wl491, wl499 = _route_inputs()
    return build_wl500_route(
        wl491=wl491,
        wl499=wl499,
    )


def test_wl500_routes_exactly_the_two_active_u5_supports() -> None:
    audit = _wl500()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL500_route_active_u5_M_tail_supports_through_ambient_C_d_solubility_then_wl491_filter"
    )
    assert audit["work_log"] == "wl500"
    assert audit["input_work_logs"] == ["wl491", "wl499"]
    assert audit["route_summary"] == {
        "active_u5_support_entry_count": 2,
        "ambient_globally_soluble_count": 0,
        "ambient_global_solubility_refuted_count": 2,
        "ambient_global_solubility_still_deferred_count": 0,
        "wl491_filter_applied_count": 0,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 0,
        "aa_bb_missing_pullback_data_count": 0,
        "aa_bb_filter_not_applied_count": 2,
    }
    assert [entry["candidate_id"] for entry in audit["routed_active_u5_supports"]] == [
        "AA_A5_B3_u_5_m_tail_shell5_candidate",
        "BB_A3_B5_u_5_m_tail_shell5_candidate",
    ]


def test_wl500_records_the_common_l5_t8_d551_cover_refutation_certificate() -> None:
    audit = _wl500()

    for entry in audit["routed_active_u5_supports"]:
        assert entry["candidate_support"] == ["u_5"]
        assert entry["sample"]["L"] == 5
        assert entry["sample"]["T"] == 8
        assert entry["complete_c_d_cover"]["d_vector"] == {
            "d_minus_p": 5,
            "d_pos_2sqrt_q": 5,
            "d_neg_2sqrt_q": 1,
        }
        assert entry["complete_c_d_cover"]["parameters"] == {
            "p": 72,
            "q": 26896,
            "sqrt_q": 164,
        }
        assert entry["complete_c_d_cover"]["x_coordinate_relations"] == [
            {
                "coordinate": "d_minus_p",
                "root": "e_minus",
                "instantiated_equation": "X + 72 = 5*u_minus_p^2",
            },
            {
                "coordinate": "d_pos_2sqrt_q",
                "root": "e_pos",
                "instantiated_equation": "X - 328 = 5*u_pos_2sqrt_q^2",
            },
            {
                "coordinate": "d_neg_2sqrt_q",
                "root": "e_neg",
                "instantiated_equation": "X + 328 = u_neg_2sqrt_q^2",
            },
        ]
        assert entry["ambient_c_d_global_solubility"]["status"] == (
            "globally_not_soluble"
        )
        assert entry["ambient_c_d_global_solubility"]["certificate_type"] == (
            "targeted_mordell_weil_torsion_lift_refutation"
        )
        assert entry["ambient_c_d_global_solubility"]["elliptic_curve_model"] == {
            "equation": "V^2 = (X + 72)*(X - 328)*(X + 328)",
            "expanded_equation": "V^2 = X^3 + 72*X^2 - 107584*X - 7746048",
        }
        assert entry["ambient_c_d_global_solubility"]["rank_zero_certificate"] == {
            "rank": 0,
            "torsion_points": ["O", "(-328,0)", "(-72,0)", "(328,0)"],
            "scope": "single instantiated curve E_{L=5,T=8}, not a family theorem",
        }
        assert entry["ambient_c_d_global_solubility"]["cover_lift_summary"][
            "torsion_lift_count"
        ] == 0


def test_wl500_does_not_apply_wl491_to_refuted_u5_ledgers() -> None:
    audit = _wl500()

    for entry in audit["routed_active_u5_supports"]:
        assert entry["wl491_filter_input"] == {}
        assert entry["wl491_filter_result"] == {
            "output_class": "not_applied",
            "reason": "ambient_C_d_global_solubility_refuted",
            "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
        }
        assert entry["routing_state"] == {
            "ambient_c_d_global_solubility_status": "globally_not_soluble",
            "aa_bb_admissibility_status": "not_applied_ambient_global_solubility_refuted",
            "ledger_route": "ambient_c_d_global_solubility_refuted_ledger",
            "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
        }


def test_wl500_stops_without_candidate_selection_or_forbidden_claims() -> None:
    audit = _wl500()

    assert audit["route_audit_built_here"] is True
    assert audit["all_active_u5_entries_classified_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl501"] is False
    assert audit["stop_after_current_task"] is True


def test_wl500_cli_writes_result_json(tmp_path: Path) -> None:
    wl491, wl499 = _route_inputs()
    wl491_path = tmp_path / "wl491.json"
    wl499_path = tmp_path / "wl499.json"
    out = tmp_path / "wl500.json"
    wl491_path.write_text(json.dumps(wl491), encoding="utf-8")
    wl499_path.write_text(json.dumps(wl499), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491_path),
            "--wl499",
            str(wl499_path),
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
    assert "work_log=wl500" in result.stdout
    assert "ambient_global_solubility_refuted_count=2" in result.stdout
    assert "advance_to_wl501=False" in result.stdout
    assert payload["work_log"] == "wl500"
