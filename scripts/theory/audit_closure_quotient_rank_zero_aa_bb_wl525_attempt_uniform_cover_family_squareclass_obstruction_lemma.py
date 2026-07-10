#!/usr/bin/env python3
"""Audit the wl525 uniform cover-family squareclass obstruction attempt."""

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
    "This audits only wl525 / attempt_uniform_cover_family_squareclass_"
    "obstruction_lemma. It uses wl523 and wl524 as inputs and works only at "
    "the cover-family statement layer. It attempts to promote the point-level "
    "wl491 opposite-side squareclass obstruction to a uniform statement over "
    "the wl522 globally soluble but not AA+BB-admissible cover families, and "
    "records the precise failure point: the finite taxonomy has no "
    "function-field squareclass certificate or specialization argument. It "
    "does not execute shell 11, compute new M_tail supports, test new ambient "
    "C_d solubility, apply wl491 to a new point, run broad rank or Selmer "
    "diagnostics, select a final obstruction candidate, use the old package-x "
    "S~ bridge, or claim a complete Sel_2(E) upper bound, dim Sel_2(E)=2, "
    "rank zero, Sha[2]=0, uniform M_tail full rank, or any family exclusion."
)


UNIFORM_LEMMA_CANDIDATE_ID = (
    "uniform_cover_family_opposite_side_squareclass_obstruction_for_"
    "globally_soluble_not_admissible_cover_families"
)


def _wl523_ready(wl523: dict[str, Any]) -> bool:
    decision = wl523.get("proof_decision", {})
    taxonomy = wl523.get("wl522_taxonomy_application", {})
    return (
        wl523.get("status") == "ok"
        and wl523.get("ready") is True
        and wl523.get("lemma_id")
        == "WL523_try_common_source_square_obstruction_lemma_candidate"
        and wl523.get("work_log") == "wl523"
        and wl523.get("input_work_log") == "wl522"
        and wl523.get("proof_statement_layer_only") is True
        and decision.get("point_level_lemma_status")
        == "provable_from_existing_wl491_machinery"
        and decision.get("cover_family_uniform_theorem_status")
        == "needs_new_uniform_squareclass_lemma"
        and decision.get("finite_taxonomy_count_is_proof") is False
        and taxonomy.get("globally_soluble_but_not_aa_bb_admissible_cover_family_count")
        == 15
        and taxonomy.get("globally_soluble_but_not_aa_bb_admissible_entry_count")
        == 29
        and taxonomy.get("opposite_side_squareclass_failure_entry_count") == 29
        and taxonomy.get("genuinely_deferred_cover_family_count") == 0
        and taxonomy.get("aa_bb_admissible_cover_family_count") == 0
        and wl523.get("shell11_executed_here") is False
        and wl523.get("m_tail_diagnostics_extended_here") is False
        and wl523.get("new_supports_computed_here") is False
        and wl523.get("new_c_d_solubility_tested_here") is False
        and wl523.get("wl491_filter_applied_to_new_point_here") is False
        and wl523.get("final_obstruction_candidate_selected_here") is False
        and wl523.get("old_package_x_coordinate_collapse_used") is False
        and wl523.get("package_x_s_tilde_bridge_used") is False
        and not _claims_forbidden_bound(wl523)
    )


def _wl524_ready(wl524: dict[str, Any]) -> bool:
    selected = wl524.get("selected_next_gate", {})
    return (
        wl524.get("status") == "ok"
        and wl524.get("ready") is True
        and wl524.get("lemma_id") == "WL524_post_wl523_route_choice_audit"
        and wl524.get("work_log") == "wl524"
        and wl524.get("input_work_log") == "wl523"
        and selected.get("gate") == "attempt_uniform_cover_family_squareclass_obstruction_lemma"
        and selected.get("entered_here") is False
        and selected.get("input_work_log_to_use_later") == "wl523"
        and selected.get("object_layer") == "cover_family_statement_layer"
        and selected.get("not_a_selmer_upper_bound") is True
        and selected.get("not_a_finite_taxonomy_count_claim") is True
        and wl524.get("selected_route_entered_here") is False
        and wl524.get("uniform_cover_family_lemma_proved_here") is False
        and wl524.get("advance_to_wl525") is False
        and wl524.get("shell11_executed_here") is False
        and wl524.get("m_tail_diagnostics_extended_here") is False
        and wl524.get("new_supports_computed_here") is False
        and wl524.get("new_c_d_solubility_tested_here") is False
        and wl524.get("wl491_filter_applied_to_new_point_here") is False
        and wl524.get("final_obstruction_candidate_selected_here") is False
        and wl524.get("old_package_x_coordinate_collapse_used") is False
        and wl524.get("package_x_s_tilde_bridge_used") is False
        and not _claims_forbidden_bound(wl524)
    )


def _finite_input_snapshot(wl523: dict[str, Any]) -> dict[str, Any]:
    taxonomy = wl523["wl522_taxonomy_application"]
    return {
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": taxonomy[
            "globally_soluble_but_not_aa_bb_admissible_cover_family_count"
        ],
        "globally_soluble_but_not_aa_bb_admissible_entry_count": taxonomy[
            "globally_soluble_but_not_aa_bb_admissible_entry_count"
        ],
        "opposite_side_squareclass_failure_entry_count": taxonomy[
            "opposite_side_squareclass_failure_entry_count"
        ],
        "squareclass_failure_reason_counts": taxonomy[
            "squareclass_failure_reason_counts"
        ],
        "positivity_failure_entry_count": taxonomy[
            "positivity_failure_entry_count"
        ],
        "genuinely_deferred_cover_family_count": taxonomy[
            "genuinely_deferred_cover_family_count"
        ],
        "aa_bb_admissible_cover_family_count": taxonomy[
            "aa_bb_admissible_cover_family_count"
        ],
        "used_as_uniform_proof": False,
        "audit_snapshot_only": True,
    }


def _uniform_lemma_target(wl523: dict[str, Any]) -> dict[str, Any]:
    snapshot = _finite_input_snapshot(wl523)
    return {
        "lemma_candidate_id": UNIFORM_LEMMA_CANDIDATE_ID,
        "scope": "cover_family_statement",
        "object_layer": "cover_family_statement_layer",
        "covered_cover_family_count": snapshot[
            "globally_soluble_but_not_aa_bb_admissible_cover_family_count"
        ],
        "covered_entry_count": snapshot[
            "globally_soluble_but_not_aa_bb_admissible_entry_count"
        ],
        "claim_to_prove": (
            "For every rational ambient C_d point on each named wl522 globally "
            "soluble but not AA+BB-admissible cover family that has a certified "
            "wl491 centered-even pullback, the opposite-side common-source product "
            "is non-square in Q*/Q*2."
        ),
        "would_imply_only": (
            "a cover-family AA+BB non-admissibility obstruction, not a Selmer "
            "upper bound, rank-zero theorem, Sha[2] statement, or family exclusion"
        ),
        "not_claiming": [
            "ambient C_d global non-solubility",
            "AA+BB admissibility for any point",
            "complete Sel_2(E_L/Q) upper bound",
            "rank zero",
            "Sha[2]=0",
            "family exclusion",
        ],
    }


def _uniform_proof_obligations() -> list[str]:
    return [
        "Give a cover-family model and rational source-side map for each named cover family.",
        "Express N and M as rational functions on the cover-family function field.",
        "Express the opposite-side product as a rational function on that function field.",
        (
            "Prove that rational function is not a square in the relevant function field, "
            "or prove an equivalent squareclass obstruction that survives specialization "
            "to every rational point under consideration."
        ),
        (
            "Control exceptional divisors, poles, zeroes, and positivity or "
            "nondegeneracy failures separately from squareclass failure."
        ),
        (
            "Show the proof is uniform for all rational points on the family, "
            "not just for the finite wl522 ledger entries."
        ),
    ]


def _proof_obligation_audit() -> list[dict[str, str]]:
    return [
        {
            "obligation": "cover_family_models_and_maps",
            "status": "missing_from_wl523_wl524_inputs",
            "effect": "cannot state the function-field object whose squareclass is to be proved",
        },
        {
            "obligation": "N_M_as_function_field_elements",
            "status": "missing_from_wl523_wl524_inputs",
            "effect": "point-level centered-even pullbacks do not provide a uniform family map",
        },
        {
            "obligation": "opposite_product_squareclass_certificate",
            "status": "missing_from_wl523_wl524_inputs",
            "effect": "finite nonsquare evaluations do not prove nonsquareness in Q(C)^*/Q(C)^*2",
        },
        {
            "obligation": "exceptional_specialization_control",
            "status": "missing_from_wl523_wl524_inputs",
            "effect": (
                "positivity and degeneracy failures cannot be merged with "
                "squareclass failure"
            ),
        },
    ]


def _attempt_decision() -> dict[str, Any]:
    return {
        "uniform_cover_family_lemma_status": "not_proved_from_wl523_wl524_inputs",
        "finite_taxonomy_promotion_status": "refuted",
        "mathematical_uniform_lemma_refuted": False,
        "failure_point": "missing_function_field_squareclass_certificate",
        "reason": (
            "wl523 supplies a point-level wl491 obstruction and wl524 selects "
            "this proof attempt, but neither input supplies cover-family "
            "function-field squareclass data, divisor parity data, or a "
            "specialization argument. The 15 cover-family / 29 entry taxonomy "
            "therefore cannot be promoted to a uniform theorem."
        ),
    }


def build_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma(
    *,
    wl523: dict[str, Any],
    wl524: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl523_ready(wl523):
        violations.append("wl523_input_not_ready_or_not_scoped")
    if not _wl524_ready(wl524):
        violations.append("wl524_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    return {
        "status": status,
        "ready": ready,
        "source": "wl523 point-level obstruction plus wl524 selected uniform lemma attempt",
        "pattern": "AA+BB",
        "lemma_id": "WL525_attempt_uniform_cover_family_squareclass_obstruction_lemma",
        "work_log": "wl525",
        "input_work_logs": ["wl523", "wl524"],
        "object_layer": "cover_family_statement_layer",
        "selected_gate_entered_here": ready,
        "attempted_uniform_cover_family_lemma_here": ready,
        "uniform_lemma_target": _uniform_lemma_target(wl523) if ready else {},
        "uniform_proof_obligations": _uniform_proof_obligations() if ready else [],
        "proof_obligation_audit": _proof_obligation_audit() if ready else [],
        "finite_input_snapshot": _finite_input_snapshot(wl523) if ready else {},
        "attempt_decision": _attempt_decision() if ready else {},
        "finite_taxonomy_is_theorem_proof": False,
        "uniform_cover_family_lemma_proved_here": False,
        "mathematical_uniform_lemma_refuted_here": False,
        "precise_failure_point": "finite_taxonomy_has_no_uniform_squareclass_certificate",
        "next_gap_not_entered": (
            "A later route would need new proof data: cover-family models, "
            "function-field N,M maps, and squareclass/divisor certificates. "
            "wl525 stops after identifying that proof gap and does not advance "
            "to another roadmap step."
        ),
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
        "advance_to_next_roadmap_step": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl523", type=Path, required=True)
    parser.add_argument("--wl524", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma(
        wl523=load_json(args.wl523),
        wl524=load_json(args.wl524),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl525 uniform cover-family squareclass audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    decision = audit.get("attempt_decision", {})
    print(
        "uniform_cover_family_lemma_status="
        f"{decision.get('uniform_cover_family_lemma_status')}"
    )
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
