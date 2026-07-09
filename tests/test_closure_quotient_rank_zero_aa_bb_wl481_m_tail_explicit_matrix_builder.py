from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (  # noqa: E501
    build_sample_m_tail_matrix,
    build_wl481_m_tail_audit,
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


def test_sample_builder_outputs_explicit_columns_rows_and_full_sample_rank() -> None:
    sample = build_sample_m_tail_matrix(side="AA", A=5, B=1)

    assert sample["sample"] == {
        "side": "AA",
        "A": 5,
        "B": 1,
        "L": 5,
        "T": 6,
        "sqrt_q": 136,
        "primitive": True,
    }
    assert sample["coordinate_order"] == [
        "d_minus_p",
        "d_pos_2sqrt_q",
        "d_neg_2sqrt_q",
    ]
    assert [column["id"] for column in sample["columns"]] == ["u_5", "v_3", "w_17"]
    assert sample["torsion_quotient"]["omitted_baseline_pivot_column"] == "w_2"
    assert [row["id"] for row in sample["rows"]] == [
        "odd_L_5_equal_d_minus_p_d_pos_2sqrt_q",
        "odd_T_3_equal_d_minus_p_d_neg_2sqrt_q",
        "odd_sqrt_q_17_equal_d_pos_2sqrt_q_d_neg_2sqrt_q",
        "dyadic_balanced_d_minus_p_five_character",
        "dyadic_balanced_d_neg_2sqrt_q_sign_character",
    ]
    assert sample["matrix"] == [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 0],
        [0, 1, 0],
    ]
    assert sample["rank_needed"] == 3
    assert sample["computed_rank"] == 3
    assert sample["computed_rank_status"] == "full_for_this_finite_sample"
    assert sample["kernel_diagnostics"] == {
        "kernel_dimension": 0,
        "basis_vectors": [],
        "basis_supports": [],
    }


def test_sample_builder_reports_kernel_without_promoting_to_theorem() -> None:
    sample = build_sample_m_tail_matrix(side="AA", A=3, B=1)

    assert [column["id"] for column in sample["columns"]] == ["u_3"]
    assert sample["rank_needed"] == 1
    assert sample["computed_rank"] == 0
    assert sample["computed_rank_status"] == "kernel_found_for_this_finite_sample"
    assert sample["symbolic_rank_status"] == "not_proved_uniformly_by_wl481"
    assert sample["kernel_diagnostics"] == {
        "kernel_dimension": 1,
        "basis_vectors": [[1]],
        "basis_supports": [["u_3"]],
    }
    assert sample["complete_selmer_upper_bound_proved"] is False
    assert sample["rank_zero_claimed"] is False


def test_wl481_audit_uses_wl480_input_and_keeps_boundary_flags() -> None:
    audit = build_wl481_m_tail_audit(wl480=_wl480_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL481_M_tail_explicit_matrix_builder"
    assert audit["work_log"] == "wl481"
    assert audit["input_work_log"] == "wl480"
    assert audit["matrix_object"]["id"] == "M_tail"
    assert audit["matrix_object"]["object_scope"] == (
        "complete d-coordinate tail matrix for E_L: Y^2=(X+p)*(X^2-4*q)"
    )
    assert audit["sample_summary"]["sample_count"] >= 4
    assert audit["sample_summary"]["full_rank_sample_count"] >= 1
    assert audit["sample_summary"]["kernel_sample_count"] >= 1
    assert audit["symbolic_rank_status"] == "uniform_full_rank_not_proved"
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0


def test_wl481_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl481.json"
    wl480 = tmp_path / "wl480.json"
    wl480.write_text(json.dumps(_wl480_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl480",
            str(wl480),
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
    assert payload["work_log"] == "wl481"
    assert payload["input_work_log"] == "wl480"
    assert payload["complete_selmer_upper_bound_proved"] is False
