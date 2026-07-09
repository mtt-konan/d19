#!/usr/bin/env python3
"""Choose the post-wl523 AA+BB route without entering the chosen gate."""

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
    "This audits only wl524 / post_wl523_route_choice_audit. It uses wl523 "
    "as input, observes that the point-level common-source square obstruction "
    "is already provable from wl491 while the uniform cover-family theorem is "
    "still unproved, compares the next route options, chooses a later attempt "
    "at a new uniform cover-family squareclass obstruction lemma as the next "
    "narrow gate, and stops before entering that proof attempt, executing "
    "shell 11, computing new M_tail supports, testing new ambient C_d "
    "solubility, applying wl491 to a new point, selecting a final obstruction "
    "candidate, running broad rank or Selmer diagnostics, using the old "
    "package-x S~ bridge, or claiming a complete Sel_2(E) upper bound, dim "
    "Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, or any family "
    "exclusion."
)


def _wl523_ready(wl523: dict[str, Any]) -> bool:
    decision = wl523.get("proof_decision", {})
    taxonomy = wl523.get("wl522_taxonomy_application", {})
    selected = wl523.get("selected_next_gate", {})
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
        and selected.get("gate") == "post_wl523_route_choice_not_entered_here"
        and selected.get("entered_here") is False
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


def _post_wl523_route_state_summary(wl523: dict[str, Any]) -> dict[str, Any]:
    decision = wl523["proof_decision"]
    taxonomy = wl523["wl522_taxonomy_application"]
    return {
        "point_level_square_obstruction_status": decision[
            "point_level_lemma_status"
        ],
        "uniform_cover_family_squareclass_theorem_status": decision[
            "cover_family_uniform_theorem_status"
        ],
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": taxonomy[
            "globally_soluble_but_not_aa_bb_admissible_cover_family_count"
        ],
        "globally_soluble_but_not_aa_bb_admissible_entry_count": taxonomy[
            "globally_soluble_but_not_aa_bb_admissible_entry_count"
        ],
        "opposite_side_squareclass_failure_entry_count": taxonomy[
            "opposite_side_squareclass_failure_entry_count"
        ],
        "genuinely_deferred_cover_family_count": taxonomy[
            "genuinely_deferred_cover_family_count"
        ],
        "aa_bb_admissible_cover_family_count": taxonomy[
            "aa_bb_admissible_cover_family_count"
        ],
        "active_final_obstruction_candidate_count": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "attempt_new_uniform_cover_family_squareclass_obstruction_lemma": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl523 leaves exactly one named theorem-candidate gap: the "
                "point-level wl491 obstruction is already available, but no "
                "uniform statement has been proved for every rational point "
                "on the globally soluble but not AA+BB-admissible cover "
                "families. A later proof attempt is the narrowest route that "
                "could convert finite taxonomy into a reusable obstruction "
                "claim, if it succeeds."
            ),
        },
        "return_later_to_finite_shell11_m_tail_diagnostics": {
            "decision": "defer",
            "reason": (
                "Shell 11 remains a valid later finite diagnostic route from "
                "the wl498/wl521 line, but running it next would widen finite "
                "M_tail sampling before the named post-wl523 proof gap has "
                "been tested. It would not by itself prove a Selmer upper "
                "bound or uniform M_tail full rank."
            ),
        },
        "proof_level_local_or_hilbert_row_work": {
            "decision": "defer_until_named_selmer_row_gap",
            "reason": (
                "Local/Hilbert row work belongs to the theorem-level Selmer "
                "route only when a specific row obligation is named. wl523 "
                "names a squareclass cover-family obstruction gap, not a new "
                "odd-prime, dyadic, or Hilbert-symbol row to prove."
            ),
        },
        "final_obstruction_candidate_selection": {
            "decision": "reject",
            "reason": (
                "The wl522/wl523 state has no AA+BB-admissible cover family, "
                "no genuinely deferred cover family, and no active final "
                "obstruction candidate. Selecting one now would confuse "
                "not-admissible diagnostic ledgers with candidates."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "attempt_uniform_cover_family_squareclass_obstruction_lemma",
        "entered_here": False,
        "input_work_log_to_use_later": "wl523",
        "object_layer": "cover_family_statement_layer",
        "purpose": (
            "test whether the wl522 globally soluble but not AA+BB-admissible "
            "cover families admit a uniform opposite-side squareclass "
            "obstruction theorem"
        ),
        "not_a_selmer_upper_bound": True,
        "not_a_finite_taxonomy_count_claim": True,
        "uniform_cover_family_lemma_proved_here": False,
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_here": False,
        "candidate_selected_here": False,
        "minimum_later_question": (
            "Can the opposite-side common-source product be proved non-square "
            "uniformly on the named globally soluble but not AA+BB-admissible "
            "cover families, without using finite counts as proof and without "
            "claiming a Selmer upper bound?"
        ),
    }


def build_wl524_post_wl523_route_choice_audit(
    *,
    wl523: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl523_ready(wl523):
        violations.append("wl523_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl523 point-level obstruction and unproved cover-family theorem gap",
        "pattern": "AA+BB",
        "lemma_id": "WL524_post_wl523_route_choice_audit",
        "work_log": "wl524",
        "input_work_log": "wl523",
        "post_wl523_route_state_summary": (
            _post_wl523_route_state_summary(wl523) if status == "ok" else {}
        ),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate()
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl523_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "selected_route_entered_here": False,
        "uniform_cover_family_lemma_proved_here": False,
        "proof_level_local_or_hilbert_row_proved_here": False,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_shell_or_grid_refreshed_here": False,
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
        "shell11_executed_here": False,
        "advance_to_selected_next_gate": False,
        "advance_to_wl525": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Attempt a new uniform cover-family squareclass obstruction "
            "lemma later. wl524 selects that gate only; it does not prove the "
            "lemma, execute shell 11, compute supports, test C_d solubility, "
            "apply wl491 to new points, select a final obstruction candidate, "
            "or claim theorem-level Selmer progress."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl523", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl524_post_wl523_route_choice_audit(wl523=load_json(args.wl523))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl524 post-wl523 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
