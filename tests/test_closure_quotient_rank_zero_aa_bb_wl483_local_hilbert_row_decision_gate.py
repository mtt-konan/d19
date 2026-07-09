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


def _wl482_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    return build_wl482_m_tail_kernel_classification_gate(wl481=wl481)


def test_wl483_records_no_justified_new_row_for_u3() -> None:
    audit = build_wl483_local_hilbert_row_decision_gate(wl482=_wl482_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL483_local_Hilbert_row_decision_gate"
    assert audit["work_log"] == "wl483"
    assert audit["input_work_log"] == "wl482"
    assert audit["target_kernel"]["support"] == ["u_3"]
    assert audit["decision"]["additional_local_hilbert_row_available"] is False
    assert audit["decision"]["row_that_kills_u_3"] is None
    assert audit["decision"]["decision"] == (
        "no_justified_additional_local_hilbert_character_row_available"
    )
    assert audit["decision"]["route_must_pivot_to_obstruction_handling"] is True
    assert audit["wl481_wl482_change"] == {
        "wl481_matrix_changed": False,
        "wl482_classification_changed": False,
        "reason": "No new justified row was found, so wl481 and wl482 remain unchanged.",
    }


def test_wl483_audits_only_relevant_places() -> None:
    audit = build_wl483_local_hilbert_row_decision_gate(wl482=_wl482_input())
    checks = audit["place_decision_checks"]

    assert [check["place"] for check in checks] == ["infinity", "2", "3", "13"]
    assert {check["row_available"] for check in checks} == {False}
    assert {check["kills_u_3"] for check in checks} == {False}
    assert checks[0]["current_framework_status"] == (
        "real sign row already quotiented as tau_minus; u_3 has positive real support"
    )
    assert checks[1]["current_framework_status"] == (
        "ordinary wl478 Q_2 row already instantiated and has zero u_3 entry"
    )
    assert checks[2]["current_framework_status"] == (
        "wl475 odd L row at 3 already instantiated and has zero u_3 entry"
    )
    assert checks[3]["current_framework_status"] == (
        "wl477 odd sqrt_q row at 13 already instantiated and has zero u_3 entry"
    )


def test_wl483_records_source_lemma_obligations_without_claiming_them() -> None:
    audit = build_wl483_local_hilbert_row_decision_gate(wl482=_wl482_input())

    assert audit["new_row_source_lemma_obligation"] == {
        "required_if_yes": (
            "A complete C_d local-solubility lemma at one of infinity, 2, 3, "
            "or 13 giving a well-defined Hilbert/character row whose u_3 entry "
            "is 1 and whose row is not already part of wl475-wl478/wl481."
        ),
        "satisfied_now": False,
        "satisfied_by": None,
    }
    assert audit["obstruction_pivot"] == {
        "next_route_status": "pivot_to_obstruction_handling",
        "examples_not_proved_here": [
            "explicit C_d cover local/global solubility for the u_3 class",
            "Cassels-Tate pairing or second descent",
            "L-value or analytic-rank evidence",
        ],
        "obstruction_proved_here": False,
    }


def test_wl483_keeps_boundary_flags() -> None:
    audit = build_wl483_local_hilbert_row_decision_gate(wl482=_wl482_input())

    assert audit["symbolic_rank_status"] == "uniform_full_rank_not_proved"
    assert audit["computed_rank_status"] == "finite_sample_kernel_decision_only"
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["search_count_used_as_progress"] is False


def test_wl483_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl483.json"
    wl482 = tmp_path / "wl482.json"
    wl482.write_text(json.dumps(_wl482_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl483_local_hilbert_row_decision_gate.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl482",
            str(wl482),
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
    assert payload["work_log"] == "wl483"
    assert payload["input_work_log"] == "wl482"
    assert payload["decision"]["additional_local_hilbert_row_available"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
