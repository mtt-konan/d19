from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_route_pivot import (
    BOUNDARY,
    audit_rank_zero_aa_bb_route_pivot,
)


def _complete_two_descent_recast() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "complete_two_descent_coordinates": {
            "ambient_relation": "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 in Q*/Q*2",
            "difference_equations": [
                "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = p+2*sqrt_q",
                "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = p-2*sqrt_q",
                "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q",
            ],
        },
    }


def _theorem_bridge() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "bridge_summary": {
            "s_tilde_is_valid_upper_bound_for_complete_selmer": False,
            "complete_selmer_upper_bound_proved": False,
            "theorem_candidate_promotable": False,
        },
        "formal_gaps": [
            "No proved inclusion Sel_2(E_L/Q) subset S_tilde_AA_BB.",
        ],
    }


def _h2_coordinate_equivalence() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "h2_verdict": {
            "status": "refuted",
            "coordinate_equivalence_proved": False,
            "coordinate_equivalence_refuted": True,
        },
        "squareclass_linear_algebra": {
            "rank_on_complete_relation_plane": 0,
            "kernel_dimension_on_complete_relation_plane": 2,
            "injective_on_complete_d_data": False,
        },
    }


def _pseudo_selmer_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pseudo_selmer_container": {
            "name": "S_tilde_AA_BB",
            "contained_object": "AA+BB common-source Selmer-candidate upper-bound container",
            "single_curve_full_sel2_subset_status": "not-claimed",
        },
        "quantifier_audit": [
            {"source": "wl457", "direct_transfer_to_sel2": False},
            {"source": "wl458", "direct_transfer_to_sel2": False},
            {"source": "wl459", "direct_transfer_to_sel2": False},
            {"source": "wl460", "direct_transfer_to_sel2": True},
            {"source": "wl461", "direct_transfer_to_sel2": True},
            {"source": "wl462", "direct_transfer_to_sel2": True},
            {"source": "wl463", "direct_transfer_to_sel2": False},
        ],
    }


def _t_tail_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "t_tail": {"status": "killed", "tail_dimension": 0},
        "dimension_bound_update": {
            "upper_bound": "dim_F2 S~ <= 2",
            "complete_selmer_bound_proved": False,
        },
    }


def test_route_pivot_selects_minimal_c_d_matrix_after_h2_failure() -> None:
    audit = audit_rank_zero_aa_bb_route_pivot(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=_t_tail_audit(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["route_decision"] == {
        "selected_route": "build_minimal_C_d_local_solubility_matrix",
        "why": (
            "H2 refutes the package x-triple as complete coordinate data, so the "
            "only bridge route still aimed at a Sel_2 upper bound must work in "
            "complete d-coordinates and test local solubility of C_d directly."
        ),
        "redefine_d_container_only": "necessary_as_setup_but_not_sufficient",
        "pivot_to_other_obstruction_route": (
            "defer_until_C_d_matrix_fails_or_exhibits_surviving_classes"
        ),
        "stop_after_route_pivot_audit": True,
    }
    assert audit["matrix_scope"]["builds_matrix_now"] is False
    assert audit["matrix_scope"]["minimal_matrix_target"] == (
        "local rows for C_d in complete d-coordinates over the relation "
        "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1"
    )


def test_route_pivot_records_exact_next_lemmas_without_overclaiming() -> None:
    audit = audit_rank_zero_aa_bb_route_pivot(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=_t_tail_audit(),
    )

    assert [lemma["id"] for lemma in audit["next_lemmas"]] == [
        "D0_complete_d_container_definition",
        "D1_relevant_place_support_confinement",
        "D2_local_C_d_row_characterization",
        "D3_torsion_baseline_in_d_coordinates",
        "D4_AA_BB_uniform_matrix_rank_bound",
    ]
    assert audit["next_lemmas"][0]["status"] == "next_to_prove"
    assert audit["next_lemmas"][1]["claim_status"] == "not_proved_here"
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_route_pivot_reuse_ledger_keeps_old_s_tilde_evidence_scoped() -> None:
    audit = audit_rank_zero_aa_bb_route_pivot(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
        h2_coordinate_equivalence=_h2_coordinate_equivalence(),
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=_t_tail_audit(),
    )

    assert audit["old_s_tilde_evidence_reuse"] == {
        "reusable_as_boundary_evidence": [
            "wl465 object consistency: S~ is a pseudo-container, not Sel_2(E_L/Q)",
            "wl468 theorem bridge audit: Sel_2(E_L/Q) subset S~ is not proved",
            "wl469 H2 audit: package x-triple cannot replace complete d-data",
        ],
        "reusable_inside_old_container_only": [
            "wl466 sign-tail kill inside S~",
            "wl467 T-tail kill inside S~",
            "dim_F2 S~ <= 2 as a pseudo-container statement",
        ],
        "reusable_as_d_matrix_templates_only": [
            "wl457-wl459 odd-prime support rows, after re-proving them as C_d local rows",
            "wl460-wl462 dyadic local computations, after rewriting them in d-coordinates",
            "wl463 point-level collapse, only as a sanity check on rational-point images",
        ],
        "not_reusable_as_selmer_bridge": [
            "package x-coordinate equivalence",
            "direct transfer of mixed AA+BB common-source rows to all complete Selmer classes",
            "single-curve sample Selmer diagnostics as proof of a family bound",
        ],
    }


def test_route_pivot_rejects_non_refuted_h2_input() -> None:
    h2 = _h2_coordinate_equivalence()
    h2["h2_verdict"] = {
        "status": "open",
        "coordinate_equivalence_proved": False,
        "coordinate_equivalence_refuted": False,
    }

    audit = audit_rank_zero_aa_bb_route_pivot(
        complete_two_descent_recast=_complete_two_descent_recast(),
        theorem_bridge=_theorem_bridge(),
        h2_coordinate_equivalence=h2,
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=_t_tail_audit(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["h2_coordinate_equivalence_not_refuted"]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_route_pivot_cli_writes_audit(tmp_path: Path) -> None:
    recast = tmp_path / "recast.json"
    bridge = tmp_path / "bridge.json"
    h2 = tmp_path / "h2.json"
    pseudo = tmp_path / "pseudo.json"
    t_tail = tmp_path / "t_tail.json"
    out = tmp_path / "route_pivot.json"
    recast.write_text(json.dumps(_complete_two_descent_recast()), encoding="utf-8")
    bridge.write_text(json.dumps(_theorem_bridge()), encoding="utf-8")
    h2.write_text(json.dumps(_h2_coordinate_equivalence()), encoding="utf-8")
    pseudo.write_text(json.dumps(_pseudo_selmer_container()), encoding="utf-8")
    t_tail.write_text(json.dumps(_t_tail_audit()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_route_pivot.py",
            "--complete-two-descent-recast",
            str(recast),
            "--theorem-bridge",
            str(bridge),
            "--h2-coordinate-equivalence",
            str(h2),
            "--pseudo-selmer-container",
            str(pseudo),
            "--t-tail-audit",
            str(t_tail),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "selected_route=build_minimal_C_d_local_solubility_matrix" in result.stdout
    assert "complete_selmer_upper_bound_proved=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["route_decision"]["stop_after_route_pivot_audit"] is True
