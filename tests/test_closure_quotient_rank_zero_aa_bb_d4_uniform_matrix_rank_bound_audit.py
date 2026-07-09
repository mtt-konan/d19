from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d4_uniform_matrix_rank_bound_audit import (  # noqa: E501
    BOUNDARY,
    audit_rank_zero_aa_bb_d4_uniform_matrix_rank_bound,
    f2_rank,
    tail_dimension_formula,
)


def _d3_baseline() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D3_torsion_baseline_in_d_coordinates",
        "d3_status": "torsion_baseline_recorded_in_complete_d_coordinates",
        "rational_two_torsion_baseline": {
            "baseline_dimension": 2,
            "baseline_not_quotiented_out": True,
        },
        "baseline_comparison_contract": {
            "comparison_status": "pending_until_local_c_d_rows_are_solved",
            "quotient_baseline_here": False,
        },
        "local_c_d_rows_solved": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _row(
    lemma_id: str,
    status_key: str,
    status_value: str,
    *,
    solved_all: bool = False,
) -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": lemma_id,
        status_key: status_value,
        "local_c_d_rows_partially_solved": not solved_all,
        "local_c_d_rows_solved": solved_all,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2a_row() -> dict[str, object]:
    return _row(
        "D2a_odd_L_collision_row",
        "d2a_status",
        "pure_L_collision_row_solved",
    )


def _d2b_row() -> dict[str, object]:
    return _row(
        "D2b_odd_T_collision_row",
        "d2b_status",
        "pure_T_collision_row_solved",
    )


def _d2c_row() -> dict[str, object]:
    return _row(
        "D2c_odd_sqrt_q_collision_row",
        "d2c_status",
        "pure_sqrt_q_collision_row_solved",
    )


def _d2d_row() -> dict[str, object]:
    return _row(
        "D2d_dyadic_complete_row",
        "d2d_status",
        "dyadic_complete_row_solved",
    )


def _d2_multi_row() -> dict[str, object]:
    row = _row(
        "D2_multi_collision_overlaps",
        "d2_multi_status",
        "odd_multi_collision_overlaps_impossible_under_primitive_normalization",
        solved_all=True,
    )
    row["remaining_d2_obligations"] = []
    row["multi_collision_overlaps_possible_under_aa_bb_inputs"] = False
    row["complete_local_c_d_row_for_overlaps"] = "vacuous_empty_row"
    return row


def _audit() -> dict[str, object]:
    return audit_rank_zero_aa_bb_d4_uniform_matrix_rank_bound(
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=_d2b_row(),
        d2c_row=_d2c_row(),
        d2d_row=_d2d_row(),
        d2_multi_row=_d2_multi_row(),
    )


def test_f2_rank_and_tail_dimension_formula() -> None:
    assert f2_rank([[1, 1, 0], [0, 1, 1], [1, 0, 1]]) == 2
    assert f2_rank([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert tail_dimension_formula(
        omega_L=2,
        omega_T=1,
        omega_sqrt_q=3,
        epsilon_balanced_2=1,
        tail_matrix_rank=4,
    ) == {
        "ambient_row_ledger_dimension_formula": (
            "1 + omega_L + omega_T + omega_sqrt_q + epsilon_balanced_2 - "
            "rank(M_tail)"
        ),
        "torsion_baseline_dimension": 2,
        "tail_dimension_formula": (
            "omega_L + omega_T + omega_sqrt_q + epsilon_balanced_2 - 1 - "
            "rank(M_tail)"
        ),
        "numeric_ambient_row_ledger_dimension": 4,
        "numeric_tail_dimension_after_torsion": 2,
        "rank_needed_for_uniform_dim2_bound": 6,
        "provided_tail_matrix_rank": 4,
        "uniform_dim2_bound_for_these_counts": False,
    }


def test_d4_audit_isolates_tail_instead_of_claiming_selmer_bound() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D4_AA_BB_uniform_matrix_rank_bound_audit"
    assert audit["d4_status"] == "uniform_dim2_bound_not_forced_by_solved_rows"
    assert audit["global_f2_dimension_ledger_built"] is True
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["surviving_obstruction"]["id"] == "M_tail_uniform_full_rank_missing"
    assert audit["surviving_obstruction"]["tail_dimension_formula"] == (
        "dim(tail)=omega_L+omega_T+omega_sqrt_q+epsilon_balanced_2-1-rank(M_tail)"
    )
    assert audit["uniform_bound_decision"] == {
        "complete_selmer_upper_bound_dimension_2_forced": False,
        "reason": (
            "The solved rows reduce D4 to a parameter-dependent F2 character "
            "matrix M_tail, but the ledger contains no uniform proof that "
            "M_tail has the required full rank."
        ),
        "rank_condition_needed": (
            "rank(M_tail)=omega_L+omega_T+omega_sqrt_q+"
            "epsilon_balanced_2-1"
        ),
    }


def test_d4_records_row_generators_and_boundary() -> None:
    audit = _audit()

    assert audit["row_generator_ledger"] == [
        {
            "source": "real sign row",
            "generator_family": "tau_minus",
            "coordinate_pattern": "(-1,-1,+1)",
            "role": "one rational 2-torsion baseline generator",
        },
        {
            "source": "pure odd ell|L rows",
            "generator_family": "u_ell for ell|L",
            "coordinate_pattern": "(ell,ell,1)",
            "free_count_symbol": "omega_L",
        },
        {
            "source": "pure odd ell|T rows",
            "generator_family": "v_ell for ell|T",
            "coordinate_pattern": "(ell,1,ell)",
            "free_count_symbol": "omega_T",
        },
        {
            "source": "pure odd ell|sqrt_q rows",
            "generator_family": "w_ell for ell|sqrt_q",
            "coordinate_pattern": "(1,ell,ell)",
            "free_count_symbol": "omega_sqrt_q",
        },
        {
            "source": "dyadic row",
            "generator_family": "w_2",
            "coordinate_pattern": "(1,2,2)",
            "free_count_symbol": "epsilon_balanced_2",
            "ordinary_even_sqrt_q_value": 0,
            "balanced_odd_sqrt_q_value": 1,
        },
    ]
    assert audit["baseline_quotient_ledger"] == {
        "baseline_dimension": 2,
        "baseline_generators": [
            "tau_minus=(-1,-1,+1)",
            "tau_sqrt_q=product_{ell|sqrt_q} w_ell times w_2 when v2(sqrt_q) is odd",
        ],
        "baseline_contained_in_row_ledger": True,
        "baseline_quotiented_for_tail_formula": True,
    }
    assert BOUNDARY in audit["boundary"]


def test_d4_cli_writes_scoped_result_json(tmp_path: Path) -> None:
    out = tmp_path / "d4.json"
    results_dir = ROOT / "results"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_d4_uniform_matrix_rank_bound_audit.py"
    )
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--d3-baseline",
            str(
                results_dir
                / "closure_quotient_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates.json"
            ),
            "--d2a-row",
            str(results_dir / "closure_quotient_rank_zero_aa_bb_d2a_odd_l_collision_row.json"),
            "--d2b-row",
            str(results_dir / "closure_quotient_rank_zero_aa_bb_d2b_odd_t_collision_row.json"),
            "--d2c-row",
            str(results_dir / "closure_quotient_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row.json"),
            "--d2d-row",
            str(results_dir / "closure_quotient_rank_zero_aa_bb_d2d_dyadic_complete_row.json"),
            "--d2-multi-row",
            str(results_dir / "closure_quotient_rank_zero_aa_bb_d2_multi_collision_overlaps.json"),
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
    assert payload["work_log"] == "wl480"
    assert payload["complete_selmer_upper_bound_proved"] is False
    assert payload["surviving_obstruction"]["id"] == "M_tail_uniform_full_rank_missing"
