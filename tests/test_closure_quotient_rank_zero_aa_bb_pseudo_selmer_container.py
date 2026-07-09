from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_pseudo_selmer_container import (
    BOUNDARY,
    audit_rank_zero_aa_bb_pseudo_selmer_container,
    load_jsonl,
    write_json,
)


def _complete_two_descent_recast() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "forced_dim_sel2_eq_2": False,
        "complete_two_descent_coordinates": {
            "ambient_relation": (
                "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q = 1 "
                "in Q*/Q*2"
            )
        },
        "isogeny_to_complete_coordinate_relation": {
            "x_minus_p": "d_pos_2sqrt_q * d_neg_2sqrt_q / d_minus_p",
            "x_pos_2sqrt_q": "d_minus_p * d_neg_2sqrt_q / d_pos_2sqrt_q",
            "x_neg_2sqrt_q": "d_minus_p * d_pos_2sqrt_q / d_neg_2sqrt_q",
        },
    }


def _diagnostic_rows() -> list[dict[str, object]]:
    return [
        {
            "A": 3,
            "B": 7,
            "curve": "AA",
            "status": "ok",
            "rank_bounds": [0, 2],
            "selmer_rank_pari": 4,
            "selmer_rank_mwrank": 4,
            "torsion_two_dimension": 2,
        },
        {
            "A": 5,
            "B": 9,
            "curve": "BB",
            "status": "ok",
            "rank_bounds": [0, 0],
            "selmer_rank_pari": 2,
            "selmer_rank_mwrank": 2,
            "torsion_two_dimension": 2,
        },
        {
            "A": 4,
            "B": 9,
            "curve": "BB",
            "status": "ok",
            "rank_bounds": [0, 0],
            "selmer_rank_pari": 4,
            "selmer_rank_mwrank": 4,
            "torsion_two_dimension": 2,
        },
        {
            "A": 2,
            "B": 5,
            "curve": "AA",
            "status": "error",
        },
    ]


def test_pseudo_selmer_container_classifies_wl457_wl463_quantifiers() -> None:
    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=_complete_two_descent_recast(),
        diagnostic_rows=_diagnostic_rows(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["quantifier_audit"] == [
        {
            "source": "wl457",
            "statement": "AA+BB kernel_neg_2sqrt_q has no odd-prime valuation support",
            "quantifier_kind": "mixed",
            "direct_transfer_to_sel2": False,
            "usable_in_pseudo_container": True,
            "reason": "uses local image rows plus AA/BB primitive common-source intersection",
        },
        {
            "source": "wl458",
            "statement": "AA+BB kernel_minus_p has no odd-prime valuation support",
            "quantifier_kind": "mixed",
            "direct_transfer_to_sel2": False,
            "usable_in_pseudo_container": True,
            "reason": "uses local image rows plus disjointness of D_A and D_B",
        },
        {
            "source": "wl459",
            "statement": "AA+BB kernel_pos_2sqrt_q has odd support only at ell | T, ell == 1 mod 4",
            "quantifier_kind": "mixed",
            "direct_transfer_to_sel2": False,
            "usable_in_pseudo_container": True,
            "reason": "uses local image rows and leaves the shared T tail",
        },
        {
            "source": "wl460",
            "statement": "opposite-mod-4 dyadic branch forces x_minus_p in {1}",
            "quantifier_kind": "local-point",
            "direct_transfer_to_sel2": True,
            "usable_in_pseudo_container": True,
            "reason": "Q_2 local image statement for one branch",
        },
        {
            "source": "wl461",
            "statement": "same-mod-4 dyadic branch has local x_minus_p class 2",
            "quantifier_kind": "local-point",
            "direct_transfer_to_sel2": True,
            "usable_in_pseudo_container": True,
            "reason": "Q_2 local image non-exclusion statement",
        },
        {
            "source": "wl462",
            "statement": (
                "same-mod-4 x_minus_p=2 is incompatible with the other two "
                "local kernel coordinates"
            ),
            "quantifier_kind": "local-common-source",
            "direct_transfer_to_sel2": True,
            "usable_in_pseudo_container": True,
            "reason": "the complete 2-descent local point carries all three root coordinates",
        },
        {
            "source": "wl463",
            "statement": "genuine AA+BB rational points collapse to (1,1,1)",
            "quantifier_kind": "global-point-summary",
            "direct_transfer_to_sel2": False,
            "usable_in_pseudo_container": False,
            "reason": "global rational-point conclusion, not a Sel_2 local membership row",
        },
    ]


def test_pseudo_selmer_container_defines_s_tilde_and_dimension_bound() -> None:
    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=_complete_two_descent_recast(),
        diagnostic_rows=_diagnostic_rows(),
    )

    assert audit["pseudo_selmer_container"] == {
        "name": "S_tilde_AA_BB",
        "contained_object": "AA+BB common-source Selmer-candidate upper-bound container",
        "ambient_coordinates": ["d_minus_p", "d_pos_2sqrt_q", "d_neg_2sqrt_q"],
        "constraints": [
            "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
            "kernel_minus_p odd-prime support is trivial in the pseudo-container",
            "kernel_neg_2sqrt_q odd-prime support is trivial in the pseudo-container",
            (
                "kernel_pos_2sqrt_q odd-prime support is contained in primes "
                "ell | T with ell == 1 mod 4"
            ),
            (
                "wl460-wl463 dyadic rows collapse the rational 2-primary "
                "local common-source branch to (1,1,1)"
            ),
            "archimedean sign row is kept as a possible one-dimensional tail until checked",
        ],
        "common_source_candidate_subset_status": "proved-for-container-definition",
        "single_curve_full_sel2_subset_status": "not-claimed",
        "subset_reason": (
            "S~ is deliberately an upper-bound container for AA+BB common-source "
            "Selmer candidates: local-point rows are direct constraints, mixed "
            "odd-prime rows are used only as support bounds, and unresolved "
            "sign/T-tail classes are retained rather than cut."
        ),
    }
    assert audit["dimension_bound"] == {
        "torsion_baseline_dimension": 2,
        "symbolic_tail_terms": ["omega_{1 mod 4}(T)", "epsilon_sign"],
        "epsilon_sign_values": [0, 1],
        "upper_bound": "dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign",
        "forces_dim_2": False,
        "why_not_forced_dim_2": (
            "The current pseudo-container still allows a T-prime tail and an "
            "unresolved archimedean sign bit."
        ),
    }
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0


def test_pseudo_selmer_container_summarizes_existing_selmer_diagnostics() -> None:
    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=_complete_two_descent_recast(),
        diagnostic_rows=_diagnostic_rows(),
    )

    assert audit["diagnostic_summary"] == {
        "diagnostic_object": {
            "measured_object": "single_curve_full_2_selmer",
            "source_tool": "Sage EllipticCurve(model).selmer_rank on the row's AA or BB curve",
            "not_measured": [
                "AA side only inside S_tilde_AA_BB",
                "BB side only inside S_tilde_AA_BB",
                "AA+BB common-source pseudo-container S_tilde_AA_BB",
                "complete C_d local matrix for S_tilde_AA_BB",
            ],
        },
        "container_comparison": {
            "comparison_status": "not_comparable",
            "reason": (
                "The symbolic bound is for the AA+BB common-source pseudo-container S~, "
                "while diagnostics measure full 2-Selmer dimensions of individual AA/BB "
                "elliptic curves."
            ),
            "full_curve_rows_exceeding_symbolic_tail_capacity_count": 0,
            "omega_zero_full_curve_excess_rows": 0,
            "max_full_curve_excess_over_symbolic_tail_capacity": 0,
        },
        "diagnostic_row_count": 4,
        "ok_row_count": 3,
        "selmer_dim_eq_torsion_count": 1,
        "selmer_dim_gt_torsion_count": 2,
        "proved_rank_zero_and_selmer_gt_torsion_count": 1,
        "rank_zero_frontier_selmer_gt_torsion_count": 1,
        "max_selmer_rank_minus_torsion": 2,
        "t_tail_histogram": {"0": 1, "1": 2},
        "sample_rows": [
            {
                "A": 3,
                "B": 7,
                "curve": "AA",
                "T": 10,
                "omega_1mod4_T": 1,
                "rank_bounds": [0, 2],
                "selmer_rank": 4,
                "torsion_two_dimension": 2,
                "selmer_rank_minus_torsion": 2,
                "rank_zero_proved": False,
                "diagnostic_object": "single_curve_full_2_selmer",
                "symbolic_container_tail_capacity": 2,
                "comparison_to_s_tilde_bound": "not_comparable_full_curve_diagnostic",
            },
            {
                "A": 5,
                "B": 9,
                "curve": "BB",
                "T": 14,
                "omega_1mod4_T": 0,
                "rank_bounds": [0, 0],
                "selmer_rank": 2,
                "torsion_two_dimension": 2,
                "selmer_rank_minus_torsion": 0,
                "rank_zero_proved": True,
                "diagnostic_object": "single_curve_full_2_selmer",
                "symbolic_container_tail_capacity": 1,
                "comparison_to_s_tilde_bound": "not_comparable_full_curve_diagnostic",
            },
            {
                "A": 4,
                "B": 9,
                "curve": "BB",
                "T": 13,
                "omega_1mod4_T": 1,
                "rank_bounds": [0, 0],
                "selmer_rank": 4,
                "torsion_two_dimension": 2,
                "selmer_rank_minus_torsion": 2,
                "rank_zero_proved": True,
                "diagnostic_object": "single_curve_full_2_selmer",
                "symbolic_container_tail_capacity": 2,
                "comparison_to_s_tilde_bound": "not_comparable_full_curve_diagnostic",
            },
        ],
    }


def test_pseudo_selmer_container_frames_diagnostics_as_full_curve_not_container() -> None:
    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=_complete_two_descent_recast(),
        diagnostic_rows=[
            {
                "A": 115,
                "B": 297,
                "curve": "AA",
                "status": "ok",
                "rank_bounds": [0, 2],
                "selmer_rank_mwrank": 4,
                "torsion_two_dimension": 2,
            },
        ],
    )

    assert audit["diagnostic_summary"]["diagnostic_object"] == {
        "measured_object": "single_curve_full_2_selmer",
        "source_tool": "Sage EllipticCurve(model).selmer_rank on the row's AA or BB curve",
        "not_measured": [
            "AA side only inside S_tilde_AA_BB",
            "BB side only inside S_tilde_AA_BB",
            "AA+BB common-source pseudo-container S_tilde_AA_BB",
            "complete C_d local matrix for S_tilde_AA_BB",
        ],
    }
    assert audit["diagnostic_summary"]["container_comparison"] == {
        "comparison_status": "not_comparable",
        "reason": (
            "The symbolic bound is for the AA+BB common-source pseudo-container S~, "
            "while diagnostics measure full 2-Selmer dimensions of individual AA/BB "
            "elliptic curves."
        ),
        "full_curve_rows_exceeding_symbolic_tail_capacity_count": 1,
        "omega_zero_full_curve_excess_rows": 1,
        "max_full_curve_excess_over_symbolic_tail_capacity": 1,
    }
    assert audit["diagnostic_summary"]["sample_rows"][0]["diagnostic_object"] == (
        "single_curve_full_2_selmer"
    )
    assert audit["diagnostic_summary"]["sample_rows"][0]["symbolic_container_tail_capacity"] == 1
    assert audit["diagnostic_summary"]["sample_rows"][0]["comparison_to_s_tilde_bound"] == (
        "not_comparable_full_curve_diagnostic"
    )


def test_pseudo_selmer_container_selects_route_without_overclaiming() -> None:
    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=_complete_two_descent_recast(),
        diagnostic_rows=_diagnostic_rows(),
    )

    assert audit["route_decision"] == {
        "decision": "sha2_obstruction_candidate_after_rank_zero_confirmation",
        "reason": (
            "At least one diagnostic row has proved rank zero and Sel_2 dimension "
            "larger than the 2-torsion baseline, so extra Selmer classes cannot "
            "be removed by a rank bound alone."
        ),
        "next_action": "separate Sha[2] via Cassels-Tate pairing, second descent, or L-value route",
    }
    assert audit["boundary"] == BOUNDARY


def test_pseudo_selmer_container_selects_t_tail_route_when_no_rank0_sha2_sample() -> None:
    rows = [
        {
            "A": 3,
            "B": 7,
            "curve": "AA",
            "status": "ok",
            "rank_bounds": [0, 2],
            "selmer_rank_pari": 4,
            "torsion_two_dimension": 2,
        }
    ]

    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=_complete_two_descent_recast(),
        diagnostic_rows=rows,
    )

    assert audit["route_decision"] == {
        "decision": "joint_local_condition_at_T_tail",
        "reason": (
            "S~ does not force dimension 2; full-curve diagnostics show extra "
            "Selmer dimension but no proved rank-zero Sha[2] witness."
        ),
        "next_action": (
            "kill or account for the ell | T, ell == 1 mod 4 tail and the "
            "archimedean sign bit"
        ),
    }


def test_pseudo_selmer_container_requires_ready_recast() -> None:
    recast = _complete_two_descent_recast()
    recast["ready"] = False

    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=recast,
        diagnostic_rows=_diagnostic_rows(),
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["complete_two_descent_recast_not_ready"]


def test_pseudo_selmer_container_cli_writes_audit(tmp_path: Path) -> None:
    recast = tmp_path / "recast.json"
    diagnostics = tmp_path / "diagnostics.jsonl"
    out = tmp_path / "pseudo_selmer.json"
    recast.write_text(json.dumps(_complete_two_descent_recast()), encoding="utf-8")
    diagnostics.write_text(
        "\n".join(json.dumps(row) for row in _diagnostic_rows()) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_pseudo_selmer_container.py",
            "--complete-two-descent-recast",
            str(recast),
            "--diagnostics-jsonl",
            str(diagnostics),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "forces_dim_2=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["diagnostic_summary"]["ok_row_count"] == 3


def test_load_jsonl_and_write_json_helpers(tmp_path: Path) -> None:
    source = tmp_path / "rows.jsonl"
    out = tmp_path / "out.json"
    source.write_text('{"b": 1}\n\n{"a": 2}\n', encoding="utf-8")

    assert load_jsonl(source) == [{"b": 1}, {"a": 2}]

    write_json(out, {"b": 1, "a": 2})
    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
