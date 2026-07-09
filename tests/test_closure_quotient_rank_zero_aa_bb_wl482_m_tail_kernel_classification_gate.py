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


def _wl481_input() -> dict[str, object]:
    return build_wl481_m_tail_audit(wl480=_wl480_input())


def test_wl482_classifies_aa_3_1_u3_kernel_as_tail_candidate() -> None:
    audit = build_wl482_m_tail_kernel_classification_gate(wl481=_wl481_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL482_M_tail_kernel_classification_gate"
    assert audit["work_log"] == "wl482"
    assert audit["input_work_log"] == "wl481"
    assert audit["target_kernel"]["sample"] == {
        "side": "AA",
        "A": 3,
        "B": 1,
        "L": 3,
        "T": 4,
        "sqrt_q": 52,
        "primitive": True,
    }
    assert audit["target_kernel"]["support"] == ["u_3"]
    assert audit["classification"]["final_classification"] == (
        "genuine_parameter_specialized_tail_obstruction_candidate"
    )
    assert audit["classification"]["not_a_complete_selmer_bound"] is True


def test_wl482_rules_out_omitted_torsion_pivot_artifact_for_u3() -> None:
    audit = build_wl482_m_tail_kernel_classification_gate(wl481=_wl481_input())
    check = audit["omitted_torsion_pivot_check"]

    assert check["raw_column_ids_before_tau_sqrt_q_quotient"] == ["u_3", "w_13"]
    assert check["omitted_baseline_pivot_column"] == "w_13"
    assert check["visible_tau_sqrt_q_support"] == ["w_13"]
    assert check["target_support_intersects_omitted_pivot"] is False
    assert check["target_support_equals_visible_tau_sqrt_q"] is False
    assert check["raw_lift_entries_for_target_support"] == [0, 0, 0]
    assert check["decision"] == "not_an_omitted_torsion_pivot_artifact"


def test_wl482_records_known_row_coverage_without_inventing_missing_row() -> None:
    audit = build_wl482_m_tail_kernel_classification_gate(wl481=_wl481_input())
    check = audit["known_local_row_coverage_check"]

    assert check["relevant_places_for_sample"] == ["infinity", "2", "3", "13"]
    assert check["included_row_ids"] == [
        "odd_L_3_equal_d_minus_p_d_pos_2sqrt_q",
        "odd_sqrt_q_13_equal_d_pos_2sqrt_q_d_neg_2sqrt_q",
        "dyadic_ordinary_d_neg_2sqrt_q_sign_character",
    ]
    assert check["known_wl481_row_with_nonzero_target_entry"] == []
    assert check["missing_known_local_or_hilbert_row_found"] is False
    assert check["decision"] == (
        "no_known_wl475_wl478_or_wl481_row_missing_that_kills_u_3"
    )


def test_wl482_keeps_boundary_flags() -> None:
    audit = build_wl482_m_tail_kernel_classification_gate(wl481=_wl481_input())

    assert audit["symbolic_rank_status"] == "uniform_full_rank_not_proved"
    assert audit["computed_rank_status"] == "finite_sample_kernel_classified_only"
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False


def test_wl482_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl482.json"
    wl481 = tmp_path / "wl481.json"
    wl481.write_text(json.dumps(_wl481_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl482_m_tail_kernel_classification_gate.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl481",
            str(wl481),
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
    assert payload["work_log"] == "wl482"
    assert payload["input_work_log"] == "wl481"
    assert payload["classification"]["final_classification"] == (
        "genuine_parameter_specialized_tail_obstruction_candidate"
    )
    assert payload["complete_selmer_upper_bound_proved"] is False
