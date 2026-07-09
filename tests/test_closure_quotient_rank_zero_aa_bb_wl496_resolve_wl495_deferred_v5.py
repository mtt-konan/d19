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


def _wl495() -> dict[str, object]:
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
    return build_wl495_route_refreshed_support_through_ambient_c_d_solubility_then_wl491_filter(
        wl491=wl491,
        wl494=wl494,
    )


def _wl496() -> dict[str, object]:
    return build_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers(
        wl495=_wl495()
    )


def test_wl496_explicitly_resolves_both_wl495_deferred_entries() -> None:
    audit = _wl496()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL496_resolve_wl495_deferred_v5_ambient_C_d_global_solubility_ledgers"
    )
    assert audit["work_log"] == "wl496"
    assert audit["input_work_log"] == "wl495"
    assert audit["resolution_summary"] == {
        "wl495_deferred_entry_count": 2,
        "explicitly_classified_entry_count": 2,
        "ambient_globally_soluble_count": 0,
        "ambient_global_solubility_refuted_count": 2,
        "ambient_global_solubility_still_deferred_count": 0,
        "wl491_filter_applied_count": 0,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 0,
        "aa_bb_filter_not_applied_count": 2,
    }
    assert [entry["candidate_id"] for entry in audit["resolved_deferred_entries"]] == [
        "AA_A4_B1_v_5_m_tail_refresh_candidate",
        "BB_A1_B4_v_5_m_tail_refresh_candidate",
    ]


def test_wl496_records_the_common_l4_t5_d515_cover_and_refutation_certificate() -> None:
    audit = _wl496()

    for entry in audit["resolved_deferred_entries"]:
        assert entry["sample"]["L"] == 4
        assert entry["sample"]["T"] == 5
        assert entry["complete_c_d_cover"]["d_vector"] == {
            "d_minus_p": 5,
            "d_pos_2sqrt_q": 1,
            "d_neg_2sqrt_q": 5,
        }
        assert entry["complete_c_d_cover"]["parameters"] == {
            "p": 78,
            "q": 7921,
            "sqrt_q": 89,
        }
        assert entry["ambient_c_d_global_solubility"]["status"] == (
            "globally_not_soluble"
        )
        assert entry["ambient_c_d_global_solubility"]["certificate_type"] == (
            "targeted_mordell_weil_torsion_lift_refutation"
        )
        assert entry["ambient_c_d_global_solubility"]["elliptic_curve_model"] == {
            "equation": "V^2 = (X + 78)*(X - 178)*(X + 178)",
            "expanded_equation": "V^2 = X^3 + 78*X^2 - 31684*X - 2471352",
        }
        assert entry["ambient_c_d_global_solubility"]["rank_zero_certificate"] == {
            "rank": 0,
            "torsion_points": ["O", "(-178,0)", "(-78,0)", "(178,0)"],
            "scope": "single instantiated curve E_{L=4,T=5}, not a family theorem",
        }
        assert entry["ambient_c_d_global_solubility"]["cover_lift_summary"][
            "torsion_lift_count"
        ] == 0


def test_wl496_does_not_apply_wl491_to_refuted_ambient_c_d_ledgers() -> None:
    audit = _wl496()

    for entry in audit["resolved_deferred_entries"]:
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


def test_wl496_stops_without_new_route_or_forbidden_claims() -> None:
    audit = _wl496()

    assert audit["resolved_wl495_deferred_ledgers_here"] is True
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
    assert audit["advance_to_wl497"] is False
    assert audit["stop_after_current_task"] is True


def test_wl496_cli_writes_result_json(tmp_path: Path) -> None:
    wl495 = _wl495()
    wl495_path = tmp_path / "wl495.json"
    out = tmp_path / "wl496.json"
    wl495_path.write_text(json.dumps(wl495), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl495",
            str(wl495_path),
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
    assert "work_log=wl496" in result.stdout
    assert "ambient_global_solubility_refuted_count=2" in result.stdout
    assert "advance_to_wl497=False" in result.stdout
    assert payload["work_log"] == "wl496"
