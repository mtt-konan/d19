#!/usr/bin/env python3
"""State the wl523 common-source square obstruction lemma candidate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (  # noqa: E501
        _claims_forbidden_bound,
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (
        _claims_forbidden_bound,
    )
    from json_io import load_json, write_json


BOUNDARY = (
    "This audits only wl523 / try_common_source_square_obstruction_lemma_candidate. "
    "It uses wl522 as input and works only at the proof/statement layer: it "
    "states the reusable point-level AA+BB common-source square obstruction "
    "already implicit in wl491, separates squareclass failures from positivity "
    "or nondegeneracy failures, and decides whether the wl522 theorem-candidate "
    "is proved by existing machinery or needs new proof. It does not execute "
    "shell 11, compute new M_tail supports, test new ambient C_d solubility, "
    "apply wl491 to a new point, run broad rank or Selmer diagnostics, select "
    "a final obstruction candidate, use the old package-x S~ bridge, or claim "
    "a complete Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, "
    "uniform M_tail full rank, or any family exclusion."
)

LEMMA_CANDIDATE_ID = (
    "common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
)

SQUARECLASS_FAILURE_REASONS = [
    "AA_common_source_product_not_square",
    "BB_common_source_product_not_square",
]

POSITIVITY_FAILURE_REASONS = [
    "A_not_positive",
    "B_not_positive",
    "N_not_positive",
    "M_not_positive",
]


def _wl522_ready(wl522: dict[str, Any]) -> bool:
    selected = wl522.get("selected_next_gate", {})
    taxonomy = wl522.get("taxonomy_summary", {})
    selected_lemma = wl522.get("selected_next_proof_level_lemma_candidate", {})
    return (
        wl522.get("status") == "ok"
        and wl522.get("ready") is True
        and wl522.get("lemma_id") == "WL522_support_cover_taxonomy_to_lemma_candidate_checkpoint"
        and wl522.get("work_log") == "wl522"
        and wl522.get("input_work_log") == "wl521"
        and wl522.get("support_cover_taxonomy_built_here") is True
        and selected.get("gate") == "try_common_source_square_obstruction_lemma_candidate"
        and selected.get("entered_here") is False
        and selected.get("lemma_candidate_id") == LEMMA_CANDIDATE_ID
        and selected_lemma.get("lemma_candidate_id") == LEMMA_CANDIDATE_ID
        and taxonomy.get("globally_soluble_but_not_aa_bb_admissible_cover_family_count") == 15
        and taxonomy.get("globally_soluble_but_not_aa_bb_admissible_entry_count") == 29
        and taxonomy.get("genuinely_deferred_cover_family_count") == 0
        and taxonomy.get("aa_bb_admissible_cover_family_count") == 0
        and wl522.get("shell11_executed_here") is False
        and wl522.get("new_supports_computed_here") is False
        and wl522.get("new_c_d_solubility_tested_here") is False
        and wl522.get("wl491_filter_applied_to_new_point_here") is False
        and wl522.get("final_obstruction_candidate_selected_here") is False
        and wl522.get("old_package_x_coordinate_collapse_used") is False
        and wl522.get("package_x_s_tilde_bridge_used") is False
        and not _claims_forbidden_bound(wl522)
    )


def _lemma_statement() -> dict[str, Any]:
    return {
        "lemma_id": LEMMA_CANDIDATE_ID,
        "scope": "point_level_aa_bb_admissibility_obstruction",
        "object_layer": "complete_d_coordinate_ambient_C_d_point_after_wl491_pullback",
        "hypotheses": [
            "A and B are positive rational AA+BB legs.",
            "The input is an ambient global C_d point in the complete d-coordinate route.",
            "The source quotient is AA with L=A, or BB with L=B.",
            "The wl491 centered-even pullback is certified and gives rational N and M.",
            "The old package-x / S~ bridge is not used.",
            "The opposite-side common-source product is not a rational square.",
        ],
        "centered_even_pullback_quantities": {
            "t": "Y/(2*(X+p))",
            "z": "X/2 - t^2",
            "N": "(A+B+t)/2",
            "M": "A+B-N",
            "quartic_y": "z/4",
        },
        "source_side_product": {
            "AA": "(N^2 + A^2)(M^2 + A^2)",
            "BB": "(N^2 + B^2)(M^2 + B^2)",
        },
        "opposite_side_product": {
            "AA_source": "(N^2 + B^2)(M^2 + B^2)",
            "BB_source": "(N^2 + A^2)(M^2 + A^2)",
        },
        "conclusion": (
            "If the opposite-side product is not a rational square, the ambient "
            "C_d point is not AA+BB-admissible and must stay in the globally "
            "soluble but not AA+BB-admissible ledger."
        ),
        "non_conclusions": [
            "This does not refute ambient C_d global solubility.",
            "This does not prove the same obstruction for every rational point on a cover family.",
            "This does not prove a Selmer upper bound or rank-zero theorem.",
        ],
    }


def _failure_separation() -> dict[str, Any]:
    return {
        "squareclass_failure_reasons": list(SQUARECLASS_FAILURE_REASONS),
        "positivity_or_nondegeneracy_reasons": list(POSITIVITY_FAILURE_REASONS),
        "M_not_positive_is_squareclass_failure": False,
        "squareclass_failure_alone_blocks_admissibility": True,
        "positivity_failure_alone_is_same_lemma": False,
        "interpretation": (
            "AA_common_source_product_not_square and "
            "BB_common_source_product_not_square are failures in Q*/Q*2. "
            "A_not_positive, B_not_positive, N_not_positive, and M_not_positive "
            "are sign or nondegeneracy failures. They can independently block "
            "AA+BB admissibility, but they are not the common-source square "
            "obstruction lemma."
        ),
    }


def _common_source_pattern(wl522: dict[str, Any]) -> dict[str, Any]:
    for pattern in wl522.get("lemma_candidate_patterns", []):
        if pattern.get("pattern_id") == (
            "common_source_square_obstruction_across_not_admissible_cover_families"
        ):
            return pattern
    return {}


def _wl522_taxonomy_application(wl522: dict[str, Any]) -> dict[str, Any]:
    taxonomy = wl522.get("taxonomy_summary", {})
    pattern = _common_source_pattern(wl522)
    reason_counts = pattern.get("blocking_reason_counts", {})
    aa_square_failures = int(reason_counts.get("AA_common_source_product_not_square", 0))
    bb_square_failures = int(reason_counts.get("BB_common_source_product_not_square", 0))
    positivity_failures = sum(
        int(reason_counts.get(reason, 0)) for reason in POSITIVITY_FAILURE_REASONS
    )
    return {
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": taxonomy.get(
            "globally_soluble_but_not_aa_bb_admissible_cover_family_count", 0
        ),
        "globally_soluble_but_not_aa_bb_admissible_entry_count": taxonomy.get(
            "globally_soluble_but_not_aa_bb_admissible_entry_count", 0
        ),
        "opposite_side_squareclass_failure_entry_count": aa_square_failures
        + bb_square_failures,
        "squareclass_failure_reason_counts": {
            "AA_common_source_product_not_square": aa_square_failures,
            "BB_common_source_product_not_square": bb_square_failures,
        },
        "positivity_failure_entry_count": positivity_failures,
        "positivity_failure_reason_counts": {
            reason: int(reason_counts.get(reason, 0)) for reason in POSITIVITY_FAILURE_REASONS
        },
        "genuinely_deferred_cover_family_count": taxonomy.get(
            "genuinely_deferred_cover_family_count", 0
        ),
        "aa_bb_admissible_cover_family_count": taxonomy.get(
            "aa_bb_admissible_cover_family_count", 0
        ),
        "application_status": (
            "all recorded globally soluble not-admissible entries are explained "
            "by the point-level opposite-side squareclass obstruction; the "
            "cover-family count remains finite taxonomy data."
        ),
    }


def _proof_decision() -> dict[str, Any]:
    return {
        "point_level_lemma_status": "provable_from_existing_wl491_machinery",
        "new_point_level_lemma_needed": False,
        "cover_family_uniform_theorem_status": "needs_new_uniform_squareclass_lemma",
        "finite_taxonomy_count_is_proof": False,
        "too_finite_if_read_as_family_theorem": True,
        "false_as_stated_for_all_future_ambient_points": "not_decided_here",
        "reason": (
            "wl491 already proves the point-level obstruction after a certified "
            "centered-even pullback. The wl522 taxonomy only shows that the "
            "recorded globally soluble not-admissible ledger entries fail this "
            "check; it does not prove a uniform statement for every rational "
            "point on those cover families."
        ),
    }


def _proof_sketch() -> list[str]:
    return [
        (
            "Use the complete d-coordinate ambient C_d point only after global "
            "solubility is established."
        ),
        "Apply the wl491 centered-even inverse map to certify rational N and M.",
        "The certified source quotient identity makes the source-side product square.",
        (
            "AA+BB admissibility requires the same N,M to make both AA and BB "
            "products rational squares."
        ),
        (
            "If the opposite-side product is not a rational square, the common "
            "source cannot close on both AA and BB."
        ),
        (
            "Therefore wl491 routes the point to not_admissible; positivity "
            "failures are recorded separately."
        ),
    ]


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "post_wl523_route_choice_not_entered_here",
        "entered_here": False,
        "minimum_later_question": (
            "Decide whether to attempt a new uniform cover-family squareclass "
            "obstruction lemma, or return later to the finite-shell route. Do "
            "not execute shell 11 or claim theorem-level Selmer progress as "
            "part of wl523."
        ),
        "shell11_executed_here": False,
    }


def build_wl523_try_common_source_square_obstruction_lemma_candidate(
    *,
    wl522: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl522_ready(wl522):
        violations.append("wl522_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl522 selected common-source square obstruction lemma candidate",
        "pattern": "AA+BB",
        "lemma_id": "WL523_try_common_source_square_obstruction_lemma_candidate",
        "work_log": "wl523",
        "input_work_log": "wl522",
        "proof_statement_layer_only": True,
        "lemma_statement": _lemma_statement() if status == "ok" else {},
        "failure_separation": _failure_separation() if status == "ok" else {},
        "wl522_taxonomy_application": _wl522_taxonomy_application(wl522)
        if status == "ok"
        else {},
        "proof_decision": _proof_decision() if status == "ok" else {},
        "proof_sketch": _proof_sketch() if status == "ok" else [],
        "selected_next_gate": _selected_next_gate() if status == "ok" else {},
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
        "final_obstruction_candidate_selected_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "advance_to_wl524": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl522", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl523_try_common_source_square_obstruction_lemma_candidate(
        wl522=load_json(args.wl522)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl523 common-source obstruction audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    decision = audit.get("proof_decision", {})
    print(f"point_level_lemma_status={decision.get('point_level_lemma_status')}")
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
