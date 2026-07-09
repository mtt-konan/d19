from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

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


def _build_wl489(wl488: dict[str, Any]) -> dict[str, Any]:
    try:
        from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl489_closure_pullback_common_source_constraints_for_global_c_d_point import (  # noqa: E501
            build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point,
        )
    except ModuleNotFoundError as exc:
        raise AssertionError("wl489 builder is missing") from exc

    return build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point(
        wl488=wl488
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


def _wl488_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    wl485 = build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)
    wl486 = build_wl486_local_solubility_gate(wl485=wl485)
    wl487 = build_wl487_route_impact_of_global_point(wl486=wl486)
    return build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
        wl487=wl487
    )


def test_wl489_pulls_back_the_global_e_l_point_to_the_aa_quartic() -> None:
    audit = _build_wl489(_wl488_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL489_closure_pullback_common_source_constraints_for_global_C_d_point"
    )
    assert audit["work_log"] == "wl489"
    assert audit["input_work_log"] == "wl488"
    assert audit["explicit_global_point"] == {
        "candidate_id": "AA_A3_B1_u_3_complete_d_candidate",
        "quotient": "AA",
        "A": 3,
        "B": 1,
        "total": 4,
        "L": 3,
        "E_L_model": "Y^2=(X+p)*(X^2-4*q)",
        "parameters": {"p": 40, "q": 2704, "sqrt_q": 52},
        "point_on_E_L": {"X": 152, "Y": 1536},
        "complete_d_squareclass": {
            "d_minus_p": 3,
            "d_pos_2sqrt_q": 3,
            "d_neg_2sqrt_q": 1,
        },
    }
    assert audit["aa_pullback"] == {
        "map_source": "centered even AA/BB quotient inverse map",
        "formulas": {
            "t": "Y/(2*(X+p))",
            "z": "X/2 - t^2",
            "N": "(A+B+t)/2",
            "M": "A+B-N",
            "quartic_y": "z/4",
        },
        "values": {
            "t": "4",
            "z": "60",
            "N": "4",
            "M": "0",
            "quartic_y": "15",
        },
        "checks": {
            "denominator_nonzero": True,
            "even_quartic_identity": "60^2 = 4^4 + 40*4^2 + 2704",
            "aa_quotient_identity": "15^2 = (4^2+3^2)*(0^2+3^2)",
            "aa_pullback_proved_for_this_point": True,
        },
    }


def test_wl489_proves_the_explicit_pullback_fails_aa_bb_common_source() -> None:
    audit = _build_wl489(_wl488_input())

    assert audit["common_source_constraint_audit"] == {
        "same_source_variables": {"N": "4", "M": "0", "A": 3, "B": 1},
        "aa_side": {
            "N2_plus_A2": 25,
            "M2_plus_A2": 9,
            "product": 225,
            "product_is_square": True,
            "individual_square_flags": {
                "N2_plus_A2": True,
                "M2_plus_A2": True,
            },
        },
        "bb_side": {
            "N2_plus_B2": 17,
            "M2_plus_B2": 1,
            "product": 17,
            "product_is_square": False,
            "individual_square_flags": {
                "N2_plus_B2": False,
                "M2_plus_B2": True,
            },
        },
        "closure_positivity_checks": {
            "N_positive": True,
            "M_positive": False,
        },
        "failing_constraints": [
            "BB quotient product is not a rational square",
            "N^2+B^2 is not a rational square",
            "M is not positive for a nondegenerate closure point",
        ],
    }
    assert audit["wl489_verdict"] == {
        "status": "proved_fails_for_this_explicit_point",
        "proved_satisfies_AA_BB_constraints": False,
        "proved_fails_AA_BB_constraints": True,
        "missing_pullback_data_gate_triggered": False,
        "reason": (
            "The explicit AA ambient E_L point pulls back to N=4, M=0 on the "
            "AA closure quotient, but the same common-source values give "
            "(N^2+B^2)*(M^2+B^2)=17, not a square."
        ),
    }


def test_wl489_keeps_the_boundary_narrow_and_stops() -> None:
    audit = _build_wl489(_wl488_input())

    assert audit["routing_audit_only"] is True
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
    assert audit["advance_to_wl490"] is False


def test_wl489_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl489.json"
    wl488 = tmp_path / "wl488.json"
    wl488.write_text(json.dumps(_wl488_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl489_closure_pullback_common_source_constraints_for_global_c_d_point.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl488",
            str(wl488),
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
    assert "wl489_status=proved_fails_for_this_explicit_point" in result.stdout
    assert "advance_to_wl490=False" in result.stdout
    assert payload["work_log"] == "wl489"
    assert payload["input_work_log"] == "wl488"
