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


def _wl483_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    return build_wl483_local_hilbert_row_decision_gate(wl482=wl482)


def test_wl484_records_explicit_u3_obstruction_candidate_datum() -> None:
    audit = build_wl484_u3_obstruction_route_entry_audit(wl483=_wl483_input())
    datum = audit["obstruction_candidate_datum"]

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL484_u3_obstruction_route_entry_audit"
    assert audit["work_log"] == "wl484"
    assert audit["input_work_log"] == "wl483"
    assert datum["id"] == "AA_A3_B1_u_3_complete_d_candidate"
    assert datum["sample"] == {
        "side": "AA",
        "A": 3,
        "B": 1,
        "L": 3,
        "T": 4,
        "sqrt_q": 52,
        "p": 40,
        "q": 2704,
        "primitive": True,
    }
    assert datum["support"] == ["u_3"]
    assert datum["coordinate_order"] == [
        "d_minus_p",
        "d_pos_2sqrt_q",
        "d_neg_2sqrt_q",
    ]
    assert datum["d_vector"] == {
        "d_minus_p": 3,
        "d_pos_2sqrt_q": 3,
        "d_neg_2sqrt_q": 1,
    }
    assert datum["d_vector_pattern"] == "(3,3,1)"
    assert datum["relevant_places"] == ["infinity", "2", "3", "13"]


def test_wl484_closes_m_tail_full_rank_rescue_for_now() -> None:
    audit = build_wl484_u3_obstruction_route_entry_audit(wl483=_wl483_input())

    assert audit["m_tail_full_rank_rescue_status"] == {
        "decision": "M_tail_full_rank_rescue_closed_for_now",
        "wl483_decision": (
            "no_justified_additional_local_hilbert_character_row_available"
        ),
        "wl481_matrix_changed": False,
        "wl482_classification_changed": False,
        "reason": (
            "wl483 found no currently justified additional local/Hilbert row "
            "at infinity, 2, 3, or 13 that kills u_3, so wl484 enters the "
            "obstruction workflow instead of trying another M_tail row rescue."
        ),
    }


def test_wl484_selects_explicit_cd_cover_gate_and_defers_deeper_routes() -> None:
    audit = build_wl484_u3_obstruction_route_entry_audit(wl483=_wl483_input())
    gate = audit["next_obstruction_workflow_gate"]

    assert gate["selected_gate"] == "explicit_C_d_cover_local_global_solubility"
    assert gate["available_gates"] == [
        "explicit_C_d_cover_local_global_solubility",
        "Cassels_Tate_or_second_descent",
        "L_value_or_analytic_rank_route",
    ]
    assert gate["why_selected"] == (
        "The u_3 datum is already explicit in complete d-coordinates and wl483 "
        "closed the row-rescue path. The next narrow controllable question is "
        "whether the concrete C_d cover for d=(3,3,1) is locally soluble at the "
        "recorded places and globally soluble or obstructed."
    )
    assert gate["deferred_gates"] == [
        {
            "gate": "Cassels_Tate_or_second_descent",
            "reason": (
                "Defer until the explicit C_d cover is certified as the relevant "
                "locally soluble Selmer-class representative or obstruction."
            ),
        },
        {
            "gate": "L_value_or_analytic_rank_route",
            "reason": (
                "Defer because analytic-rank evidence would not by itself be the "
                "minimal certificate for this concrete d-cover routing question."
            ),
        },
    ]
    assert gate["proof_started_here"] is False


def test_wl484_keeps_boundary_flags() -> None:
    audit = build_wl484_u3_obstruction_route_entry_audit(wl483=_wl483_input())

    assert audit["obstruction_proved_here"] is False
    assert audit["explicit_c_d_cover_solved_here"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["search_count_used_as_progress"] is False


def test_wl484_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl484.json"
    wl483 = tmp_path / "wl483.json"
    wl483.write_text(json.dumps(_wl483_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl484_u3_obstruction_route_entry_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl483",
            str(wl483),
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
    assert payload["work_log"] == "wl484"
    assert payload["input_work_log"] == "wl483"
    assert payload["next_obstruction_workflow_gate"]["selected_gate"] == (
        "explicit_C_d_cover_local_global_solubility"
    )
    assert payload["obstruction_proved_here"] is False
