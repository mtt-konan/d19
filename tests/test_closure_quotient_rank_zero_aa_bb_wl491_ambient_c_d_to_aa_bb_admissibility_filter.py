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


def _wl490_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    wl484 = build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)
    wl485 = build_wl485_explicit_cd_cover_equation_instantiation(wl484=wl484)
    wl486 = build_wl486_local_solubility_gate(wl485=wl485)
    wl487 = build_wl487_route_impact_of_global_point(wl486=wl486)
    wl488 = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(wl487=wl487)
    wl489 = build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point(wl488=wl488)
    return build_wl490_route_impact_after_wl489_admissibility_failure(wl489=wl489)


def test_wl491_defines_reusable_point_level_filter_contract() -> None:
    audit = build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(wl490=_wl490_input())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == ("WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter")
    assert audit["work_log"] == "wl491"
    assert audit["input_work_log"] == "wl490"
    assert audit["admissibility_filter_defined_here"] is True

    contract = audit["point_level_filter_contract"]
    assert contract["required_inputs"] == {
        "ambient_global_c_d_point": [
            "candidate_id",
            "quotient in {AA, BB}",
            "A",
            "B",
            "L matching the source quotient leg",
            "point_on_E_L.X",
            "point_on_E_L.Y",
            "parameters.p",
            "parameters.q",
            "complete_d_squareclass",
        ],
        "route_context": [
            "ambient_global_C_d_solubility_already_established",
            "old_package_x_S_tilde_bridge_not_used",
        ],
    }
    assert contract["checks_in_order"] == [
        "input_shape_and_scope",
        "centered_even_pullback",
        "AA_common_source_square_product",
        "BB_common_source_square_product",
        "positivity_and_nondegeneracy",
    ]
    assert contract["output_classes"] == {
        "admissible": "all checks pass",
        "not_admissible": "pullback exists but a square or positivity/nondegeneracy check fails",
        "missing_pullback_data": (
            "input is scoped but the centered-even pullback cannot be certified"
        ),
        "invalid_input": "required point-level data or route context is missing",
    }


def test_wl491_applies_filter_to_u3_sample_as_not_admissible_regression() -> None:
    audit = build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(wl490=_wl490_input())
    regression = audit["u3_regression"]

    assert regression["candidate_id"] == "AA_A3_B1_u_3_complete_d_candidate"
    assert regression["output_class"] == "not_admissible"
    assert regression["can_enter_admissible_point_ledger"] is False
    assert regression["ledger_route"] == ("globally_soluble_but_not_aa_bb_admissible_ledger")
    assert regression["centered_even_pullback_check"]["values"] == {
        "t": "4",
        "z": "60",
        "N": "4",
        "M": "0",
        "quartic_y": "15",
    }
    assert regression["centered_even_pullback_check"]["passed"] is True
    assert regression["common_source_square_checks"]["AA"]["product_is_square"] is True
    assert regression["common_source_square_checks"]["BB"]["product"] == "17"
    assert regression["common_source_square_checks"]["BB"]["product_is_square"] is False
    assert regression["positivity_nondegeneracy_checks"] == {
        "A_positive": True,
        "B_positive": True,
        "N_positive": True,
        "M_positive": False,
        "nondegenerate_positive_closure_point": False,
    }
    assert regression["blocking_reasons"] == [
        "BB_common_source_product_not_square",
        "M_not_positive",
    ]


def test_wl491_routes_ledgers_and_keeps_boundaries_narrow() -> None:
    audit = build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(wl490=_wl490_input())

    assert audit["ledger_routing_semantics"] == {
        "admissible": {
            "can_enter_admissible_point_ledger": True,
            "ledger_route": "admissible_point_ledger",
        },
        "not_admissible": {
            "can_enter_admissible_point_ledger": False,
            "ledger_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
        },
        "missing_pullback_data": {
            "can_enter_admissible_point_ledger": False,
            "ledger_route": "missing_pullback_data_ledger",
        },
        "invalid_input": {
            "can_enter_admissible_point_ledger": False,
            "ledger_route": "invalid_or_unscoped_input_ledger",
        },
    }
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl492"] is False
    assert audit["stop_after_current_task"] is True


def test_wl491_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl491.json"
    wl490 = tmp_path / "wl490.json"
    wl490.write_text(json.dumps(_wl490_input()), encoding="utf-8")
    script = (
        ROOT / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl490",
            str(wl490),
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
    assert "u3_output_class=not_admissible" in result.stdout
    assert "advance_to_wl492=False" in result.stdout
    assert payload["work_log"] == "wl491"
    assert payload["input_work_log"] == "wl490"
