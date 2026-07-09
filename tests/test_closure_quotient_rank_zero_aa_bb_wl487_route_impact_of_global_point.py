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


def _wl486_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    wl485 = build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)
    return build_wl486_local_solubility_gate(wl485=wl485)


def test_wl487_records_that_only_the_u3_obstruction_interpretation_is_refuted() -> None:
    audit = build_wl487_route_impact_of_global_point(wl486=_wl486_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL487_route_impact_of_global_point"
    assert audit["work_log"] == "wl487"
    assert audit["input_work_log"] == "wl486"
    assert audit["refutation_scope"] == {
        "candidate_id": "AA_A3_B1_u_3_complete_d_candidate",
        "d_vector": {
            "d_minus_p": 3,
            "d_pos_2sqrt_q": 3,
            "d_neg_2sqrt_q": 1,
        },
        "refuted_interpretation": (
            "this_specific_u3_as_locally_soluble_globally_pointless_obstruction"
        ),
        "refuted_here": True,
        "global_point_on_this_cover": True,
        "does_not_refute": [
            "M_tail_uniform_full_rank_missing_as_a_general_route_gap",
            "existence_of_other_complete_d_coordinate_obstructions",
            "need_for_a_complete_Selmer_upper_bound",
        ],
    }
    assert audit["candidate_obstruction_refuted_here"] is True
    assert audit["obstruction_proved_here"] is False


def test_wl487_classifies_the_global_point_against_visible_two_torsion_baseline() -> None:
    audit = build_wl487_route_impact_of_global_point(wl486=_wl486_input())

    assert audit["global_point_classification"] == {
        "curve_model": "E_L: Y^2=(X+p)*(X^2-4*q)",
        "parameters": {"p": 40, "q": 2704, "sqrt_q": 52},
        "point_on_cover": {
            "X": 152,
            "u_minus_p": 8,
            "u_pos_2sqrt_q": 4,
            "u_neg_2sqrt_q": 16,
        },
        "point_on_E_L": {"X": 152, "Y": 1536},
        "exact_checks": {
            "x_minus_roots": {
                "X_plus_p": 192,
                "X_minus_2sqrt_q": 48,
                "X_plus_2sqrt_q": 256,
            },
            "cover_relations": [
                "192 = 3*8^2",
                "48 = 3*4^2",
                "256 = 1*16^2",
            ],
            "curve_equation": "1536^2 = (152+40)*(152^2 - 4*2704)",
        },
        "complete_d_squareclass": {
            "coordinate_order": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ],
            "representative": {
                "d_minus_p": 3,
                "d_pos_2sqrt_q": 3,
                "d_neg_2sqrt_q": 1,
            },
            "product_relation_square": "3*3*1 = 3^2",
        },
        "visible_two_torsion_baseline_comparison": {
            "baseline_source": "wl474 D3 rational E_L[2](Q) baseline",
            "baseline_squareclass_representatives": {
                "O": [1, 1, 1],
                "T_minus_p": [-1, -1, 1],
                "T_pos_2sqrt_q": [1, 13, 13],
                "T_neg_2sqrt_q": [-1, -13, 13],
            },
            "point_squareclass_tuple": [3, 3, 1],
            "matches_visible_two_torsion_baseline": False,
            "not_a_visible_two_torsion_point_checks": {
                "Y_nonzero": True,
                "X_not_equal_to_roots": True,
            },
        },
        "classification": "non_torsion_candidate_not_visible_two_torsion_baseline",
        "full_mordell_weil_torsion_decided_here": False,
        "rank_decided_here": False,
    }


def test_wl487_records_m_tail_and_global_obstruction_route_impact_without_new_bounds() -> None:
    audit = build_wl487_route_impact_of_global_point(wl486=_wl486_input())

    assert audit["route_impact"] == {
        "m_tail_status_after_global_point": (
            "u3_no_longer_available_as_global_obstruction_candidate"
        ),
        "m_tail_full_rank_rescue_reopened_here": False,
        "new_local_or_hilbert_row_found_here": False,
        "global_obstruction_routing_status": (
            "current_explicit_C_d_obstruction_route_refuted_by_global_point"
        ),
        "ledger_update": (
            "mark d=(3,3,1) as globally soluble with a non-baseline "
            "complete d-coordinate point candidate; do not count it as an "
            "obstruction or as Selmer upper-bound progress"
        ),
    }
    assert audit["symbolic_rank_status"] == (
        "u3_global_point_recorded_no_rank_conclusion"
    )
    assert audit["computed_rank_status"] == "not_run_route_impact_only"
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0


def test_wl487_defines_next_narrow_gate_but_does_not_enter_it() -> None:
    audit = build_wl487_route_impact_of_global_point(wl486=_wl486_input())

    assert audit["next_narrow_gate"] == {
        "gate": "select_next_complete_d_coordinate_route_after_u3_global_point",
        "entry_condition": (
            "wl487 has marked the AA A=3,B=1 u_3 cover globally soluble and "
            "not a visible E_L[2](Q) baseline point"
        ),
        "allowed_next_actions": [
            "remove_this_u3_cover_from_the_obstruction_candidate_ledger",
            "choose_the_next_single_complete_d_coordinate_candidate_or_row_gap",
            "keep_M_tail_and_global_obstruction_ledgers_separate",
        ],
        "forbidden_next_actions_here": [
            "run_broad_rank_or_selmer_diagnostics",
            "claim_complete_selmer_upper_bound",
            "claim_rank_zero_or_sha2_triviality",
            "claim_family_exclusion",
        ],
        "entered_here": False,
    }
    assert audit["stop_after_current_task"] is True


def test_wl487_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl487.json"
    wl486 = tmp_path / "wl486.json"
    wl486.write_text(json.dumps(_wl486_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl487_route_impact_of_global_point.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl486",
            str(wl486),
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
    assert "classification=non_torsion_candidate_not_visible_two_torsion_baseline" in (
        result.stdout
    )
    assert payload["work_log"] == "wl487"
    assert payload["input_work_log"] == "wl486"
    assert payload["next_narrow_gate"]["entered_here"] is False
