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


def _wl484_input() -> dict[str, object]:
    wl481 = build_wl481_m_tail_audit(wl480=_wl480_input())
    wl482 = build_wl482_m_tail_kernel_classification_gate(wl481=wl481)
    wl483 = build_wl483_local_hilbert_row_decision_gate(wl482=wl482)
    return build_wl484_u3_obstruction_route_entry_audit(wl483=wl483)


def test_wl485_records_root_data_and_x_coordinate_relations() -> None:
    audit = build_wl485_explicit_cd_cover_equation_instantiation(
        wl484=_wl484_input()
    )
    cover = audit["explicit_c_d_cover"]

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL485_explicit_C_d_cover_equation_instantiation"
    assert audit["work_log"] == "wl485"
    assert audit["input_work_log"] == "wl484"
    assert cover["candidate_id"] == "AA_A3_B1_u_3_complete_d_candidate"
    assert cover["root_data"] == {
        "e_minus": {"symbolic": "-p", "value": -40},
        "e_pos": {"symbolic": "2*sqrt_q", "value": 104},
        "e_neg": {"symbolic": "-2*sqrt_q", "value": -104},
    }
    assert cover["x_coordinate_relations"] == [
        {
            "coordinate": "d_minus_p",
            "root": "e_minus",
            "general_equation": "X - e_minus = d_minus_p*u_minus_p^2",
            "instantiated_equation": "X + 40 = 3*u_minus_p^2",
        },
        {
            "coordinate": "d_pos_2sqrt_q",
            "root": "e_pos",
            "general_equation": "X - e_pos = d_pos_2sqrt_q*u_pos_2sqrt_q^2",
            "instantiated_equation": "X - 104 = 3*u_pos_2sqrt_q^2",
        },
        {
            "coordinate": "d_neg_2sqrt_q",
            "root": "e_neg",
            "general_equation": "X - e_neg = d_neg_2sqrt_q*u_neg_2sqrt_q^2",
            "instantiated_equation": "X + 104 = u_neg_2sqrt_q^2",
        },
    ]


def test_wl485_instantiates_three_differences_and_two_independent_equations() -> None:
    audit = build_wl485_explicit_cd_cover_equation_instantiation(
        wl484=_wl484_input()
    )
    cover = audit["explicit_c_d_cover"]

    assert cover["three_difference_equations"] == [
        {
            "id": "minus_minus_pos",
            "general_equation": (
                "d_minus_p*u_minus_p^2 - "
                "d_pos_2sqrt_q*u_pos_2sqrt_q^2 = e_pos - e_minus"
            ),
            "instantiated_equation": (
                "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144"
            ),
        },
        {
            "id": "minus_minus_neg",
            "general_equation": (
                "d_minus_p*u_minus_p^2 - "
                "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = e_neg - e_minus"
            ),
            "instantiated_equation": "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
        },
        {
            "id": "pos_minus_neg",
            "general_equation": (
                "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - "
                "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = e_neg - e_pos"
            ),
            "instantiated_equation": (
                "3*u_pos_2sqrt_q^2 - u_neg_2sqrt_q^2 = -208"
            ),
        },
    ]
    assert cover["two_independent_equations"] == [
        "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144",
        "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
    ]
    assert cover["normalized_independent_equations"] == [
        "u_minus_p^2 - u_pos_2sqrt_q^2 = 48",
        "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
    ]
    assert cover["dependency_check"] == {
        "dependent_equation": "pos_minus_neg",
        "derived_as": "minus_minus_neg - minus_minus_pos",
        "rhs_check": "-64 - 144 = -208",
        "solubility_decided_here": False,
    }


def test_wl485_records_next_gate_local_checklist_without_deciding_solubility() -> None:
    audit = build_wl485_explicit_cd_cover_equation_instantiation(
        wl484=_wl484_input()
    )
    checklist = audit["narrow_local_solubility_checklist_for_next_gate"]

    assert audit["relevant_places"] == ["infinity", "2", "3", "13"]
    assert [item["place"] for item in checklist] == ["infinity", "2", "3", "13"]
    assert all(item["status"] == "not_checked_here" for item in checklist)
    assert all(item["local_solubility_decided_here"] is False for item in checklist)
    assert audit["local_solubility_decided_here"] is False
    assert audit["global_solubility_decided_here"] is False
    assert audit["explicit_c_d_cover_solved_here"] is False


def test_wl485_keeps_boundary_flags_and_uses_complete_d_coordinates_only() -> None:
    audit = build_wl485_explicit_cd_cover_equation_instantiation(
        wl484=_wl484_input()
    )

    assert audit["equation_instantiation_only"] is True
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["obstruction_proved_here"] is False
    assert audit["search_count_used_as_progress"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False


def test_wl485_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl485.json"
    wl484 = tmp_path / "wl484.json"
    wl484.write_text(json.dumps(_wl484_input()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl485_explicit_cd_cover_equation_instantiation.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl484",
            str(wl484),
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
    assert payload["work_log"] == "wl485"
    assert payload["input_work_log"] == "wl484"
    assert payload["explicit_c_d_cover"]["two_independent_equations"] == [
        "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144",
        "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
    ]
    assert payload["local_solubility_decided_here"] is False
