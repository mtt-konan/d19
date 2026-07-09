from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_theorem_bridge import (
    BOUNDARY,
    audit_rank_zero_aa_bb_theorem_bridge,
)


def _pseudo_selmer_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pattern": "AA+BB",
        "pseudo_selmer_container": {
            "name": "S_tilde_AA_BB",
            "contained_object": "AA+BB common-source Selmer-candidate upper-bound container",
            "common_source_candidate_subset_status": "proved-for-container-definition",
            "single_curve_full_sel2_subset_status": "not-claimed",
        },
        "dimension_bound": {
            "upper_bound": "dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign",
            "forces_dim_2": False,
        },
    }


def _t_tail_audit() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pattern": "AA+BB",
        "dimension_bound_update": {
            "upper_bound": "dim_F2 S~ <= 2",
            "pseudo_selmer_container_forces_torsion_baseline": True,
            "complete_selmer_bound_proved": False,
        },
        "t_tail": {"status": "killed", "tail_dimension": 0},
    }


def test_bridge_records_s_tilde_result_but_does_not_promote_to_complete_selmer() -> None:
    audit = audit_rank_zero_aa_bb_theorem_bridge(
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=_t_tail_audit(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["bridge_summary"] == {
        "cheap_container_result": "dim_F2 S_tilde_AA_BB <= 2",
        "relevant_complete_selmer_object": (
            "Sel_2(E_L/Q) for the complete full-rational-2-torsion curve "
            "E_L: Y^2=(X+p)*(X^2-4*q), with L=A on AA and L=B on BB"
        ),
        "s_tilde_is_valid_upper_bound_for_complete_selmer": False,
        "complete_selmer_upper_bound_proved": False,
        "theorem_candidate_promotable": False,
        "reason": (
            "The killed ledger bounds only the AA+BB common-source pseudo-container; "
            "it has not been proved to contain every class of the complete "
            "2-Selmer group Sel_2(E_L/Q)."
        ),
    }
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["boundary"] == BOUNDARY


def test_bridge_lists_exact_missing_obligations() -> None:
    audit = audit_rank_zero_aa_bb_theorem_bridge(
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=_t_tail_audit(),
    )

    assert audit["required_hypotheses"] == [
        {
            "id": "H1_complete_selmer_object",
            "needed": True,
            "status": "framed_not_proved",
            "statement": (
                "Fix the theorem object as Sel_2(E_L/Q) for each AA or BB side, "
                "not the AA+BB common-source pseudo-container and not sampled "
                "single-curve diagnostics."
            ),
        },
        {
            "id": "H2_coordinate_equivalence",
            "needed": True,
            "status": "partially_framed",
            "statement": (
                "Prove the complete-descent d-coordinates and the three package "
                "x-coordinates define equivalent squareclass data for every "
                "Selmer class, including torsion representatives and exceptional "
                "root cases."
            ),
        },
        {
            "id": "H3_uniform_local_containment",
            "needed": True,
            "status": "missing",
            "statement": (
                "For every place v and every complete 2-cover C_d locally soluble "
                "over Q_v, prove its translated x-data satisfies the constraints "
                "used to define S_tilde_AA_BB."
            ),
        },
        {
            "id": "H4_mixed_rows_upgrade",
            "needed": True,
            "status": "missing",
            "statement": (
                "Upgrade wl457-wl459 from AA+BB mixed common-source support rows "
                "to valid constraints on all complete Selmer classes, or prove a "
                "separate theorem that every relevant Selmer class is represented "
                "by such a common-source class."
            ),
        },
        {
            "id": "H5_dimension_and_torsion_identification",
            "needed": True,
            "status": "missing",
            "statement": (
                "After Sel_2(E_L/Q) subset S_tilde_AA_BB is proved, identify the "
                "two-dimensional torsion baseline inside the same ambient quotient "
                "and verify dim_F2 S_tilde_AA_BB <= 2 in that quotient."
            ),
        },
    ]
    assert audit["formal_gaps"] == [
        "No proved inclusion Sel_2(E_L/Q) subset S_tilde_AA_BB.",
        (
            "The support-killing rows wl457-wl459 are still mixed AA+BB "
            "common-source rows, not complete local matrix rows."
        ),
        (
            "The full C_d local-solubility matrix has not been built or shown "
            "redundant for all Selmer classes."
        ),
        "The killed T-tail and sign-tail remove symbolic tails only inside S_tilde_AA_BB.",
        (
            "Therefore dim_F2 S_tilde_AA_BB <= 2 is not yet a rigorous upper "
            "bound for dim_F2 Sel_2(E_L/Q)."
        ),
    ]


def test_bridge_rejects_unready_t_tail_input() -> None:
    t_tail = _t_tail_audit()
    t_tail["ready"] = False

    audit = audit_rank_zero_aa_bb_theorem_bridge(
        pseudo_selmer_container=_pseudo_selmer_container(),
        t_tail_audit=t_tail,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["t_tail_audit_not_ready"]
    assert audit["bridge_summary"]["complete_selmer_upper_bound_proved"] is False


def test_bridge_cli_writes_audit(tmp_path: Path) -> None:
    pseudo = tmp_path / "pseudo.json"
    t_tail = tmp_path / "t_tail.json"
    out = tmp_path / "bridge.json"
    pseudo.write_text(json.dumps(_pseudo_selmer_container()), encoding="utf-8")
    t_tail.write_text(json.dumps(_t_tail_audit()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_theorem_bridge.py",
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

    assert "complete_selmer_upper_bound_proved=False" in result.stdout
    assert "theorem_candidate_promotable=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["bridge_summary"]["s_tilde_is_valid_upper_bound_for_complete_selmer"] is False
