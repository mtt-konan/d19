#!/usr/bin/env python3
"""Choose the post-wl525 AA+BB route without entering the chosen gate."""

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
    "This audits only wl526 / post_wl525_route_choice_audit. It uses wl525 "
    "as immediate input, observes that the attempted finite-taxonomy promotion "
    "to a uniform cover-family squareclass theorem failed for lack of "
    "function-field squareclass proof data, compares exactly four next-route "
    "families, chooses a later minimal function-field proof-data scoping gate, "
    "and stops before entering it. It does not execute shell 11, compute new "
    "M_tail supports, test new ambient C_d solubility, apply wl491 to a new "
    "point, build function-field models, prove the uniform lemma, run broad "
    "rank or Selmer diagnostics, use the old package-x S~ bridge, abandon the "
    "obstruction line, select a different candidate, or claim a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform "
    "M_tail full rank, theorem-level progress, or any family exclusion."
)


def _wl525_ready(wl525: dict[str, Any]) -> bool:
    decision = wl525.get("attempt_decision", {})
    finite = wl525.get("finite_input_snapshot", {})
    return (
        wl525.get("status") == "ok"
        and wl525.get("ready") is True
        and wl525.get("lemma_id")
        == "WL525_attempt_uniform_cover_family_squareclass_obstruction_lemma"
        and wl525.get("work_log") == "wl525"
        and wl525.get("input_work_logs") == ["wl523", "wl524"]
        and wl525.get("object_layer") == "cover_family_statement_layer"
        and wl525.get("selected_gate_entered_here") is True
        and wl525.get("attempted_uniform_cover_family_lemma_here") is True
        and decision.get("uniform_cover_family_lemma_status")
        == "not_proved_from_wl523_wl524_inputs"
        and decision.get("finite_taxonomy_promotion_status") == "refuted"
        and decision.get("mathematical_uniform_lemma_refuted") is False
        and decision.get("failure_point")
        == "missing_function_field_squareclass_certificate"
        and wl525.get("finite_taxonomy_is_theorem_proof") is False
        and wl525.get("uniform_cover_family_lemma_proved_here") is False
        and wl525.get("mathematical_uniform_lemma_refuted_here") is False
        and wl525.get("precise_failure_point")
        == "finite_taxonomy_has_no_uniform_squareclass_certificate"
        and finite.get("globally_soluble_but_not_aa_bb_admissible_cover_family_count")
        == 15
        and finite.get("globally_soluble_but_not_aa_bb_admissible_entry_count")
        == 29
        and finite.get("used_as_uniform_proof") is False
        and finite.get("audit_snapshot_only") is True
        and wl525.get("shell11_executed_here") is False
        and wl525.get("m_tail_diagnostics_extended_here") is False
        and wl525.get("new_supports_computed_here") is False
        and wl525.get("new_c_d_solubility_tested_here") is False
        and wl525.get("wl491_filter_applied_to_new_point_here") is False
        and wl525.get("final_obstruction_candidate_selected_here") is False
        and wl525.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl525.get("old_package_x_coordinate_collapse_used") is False
        and wl525.get("package_x_s_tilde_bridge_used") is False
        and wl525.get("advance_to_next_roadmap_step") is False
        and wl525.get("stop_after_current_task") is True
        and not _claims_forbidden_bound(wl525)
    )


def _post_wl525_route_state_summary(wl525: dict[str, Any]) -> dict[str, Any]:
    decision = wl525["attempt_decision"]
    finite = wl525["finite_input_snapshot"]
    return {
        "uniform_cover_family_lemma_status": decision[
            "uniform_cover_family_lemma_status"
        ],
        "finite_taxonomy_promotion_status": decision[
            "finite_taxonomy_promotion_status"
        ],
        "mathematical_uniform_lemma_refuted": decision[
            "mathematical_uniform_lemma_refuted"
        ],
        "failure_point": decision["failure_point"],
        "precise_failure_point": wl525["precise_failure_point"],
        "finite_taxonomy_is_theorem_proof": wl525[
            "finite_taxonomy_is_theorem_proof"
        ],
        "uniform_cover_family_lemma_proved_here": wl525[
            "uniform_cover_family_lemma_proved_here"
        ],
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": finite[
            "globally_soluble_but_not_aa_bb_admissible_cover_family_count"
        ],
        "globally_soluble_but_not_aa_bb_admissible_entry_count": finite[
            "globally_soluble_but_not_aa_bb_admissible_entry_count"
        ],
    }


def _route_families() -> dict[str, dict[str, Any]]:
    return {
        "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families": {
            "decision": "selected_next_narrow_gate",
            "entered_here": False,
            "reason": (
                "This is the smallest route that addresses the exact wl525 "
                "failure point. Before another proof attempt, the route needs "
                "only to scope whether the named cover families have models, "
                "source-side maps, candidate N,M function-field elements, and "
                "a squareclass or divisor-parity certificate target. It does "
                "not build those models or prove the lemma in wl526."
            ),
        },
        "return_to_finite_shell_m_tail_diagnostics": {
            "decision": "defer",
            "entered_here": False,
            "reason": (
                "Finite M_tail diagnostics can still find more finite support "
                "data, but wl525 failed at the cover-family proof-data layer. "
                "More finite supports would not by itself produce a uniform "
                "squareclass theorem, complete Selmer upper bound, or uniform "
                "M_tail full-rank proof."
            ),
        },
        "name_theorem_level_complete_selmer_local_hilbert_row_obligation": {
            "decision": "defer_until_cover_family_obstruction_line_is_scoped_or_refuted",
            "entered_here": False,
            "reason": (
                "A theorem-level complete-Selmer local or Hilbert row is the "
                "right level only when a specific row obligation is isolated. "
                "wl525 names a missing cover-family squareclass certificate, "
                "not an odd-prime, dyadic, Hilbert-symbol, or global Selmer "
                "dimension row ready to state here."
            ),
        },
        "abandon_this_obstruction_line_and_select_different_candidate": {
            "decision": "reject_for_now",
            "entered_here": False,
            "reason": (
                "wl525 refutes only the finite-taxonomy promotion, not the "
                "mathematical uniform lemma. Abandoning the obstruction line "
                "or selecting a different candidate now would skip the minimal "
                "data-scoping step that could prove the line viable or refute "
                "it cleanly."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families",
        "entered_here": False,
        "input_work_log_to_use_later": "wl525",
        "object_layer": "cover_family_function_field_proof_data_scoping",
        "purpose": (
            "Scope the minimum function-field proof data needed before any "
            "later uniform cover-family squareclass proof attempt can be "
            "entered or refuted."
        ),
        "minimum_later_question": (
            "For each named globally soluble but not AA+BB-admissible cover "
            "family, is there enough explicit function-field data to state "
            "the opposite-side product and seek a squareclass or divisor-parity "
            "certificate, while separating exceptional positivity and "
            "degeneracy failures?"
        ),
        "minimum_later_data_to_scope": [
            "named cover-family model inventory",
            "rational source-side map inventory",
            "N and M as candidate function-field elements",
            "opposite-side product squareclass or divisor-parity certificate target",
            "exceptional specialization and positivity-separation checklist",
        ],
        "not_a_selmer_upper_bound": True,
        "not_a_finite_taxonomy_count_claim": True,
        "builds_function_field_models_here": False,
        "proves_uniform_lemma_here": False,
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_here": False,
        "candidate_selected_here": False,
    }


def build_wl526_post_wl525_route_choice_audit(
    *,
    wl525: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl525_ready(wl525):
        violations.append("wl525_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl525 failed finite-taxonomy promotion after uniform lemma attempt",
        "pattern": "AA+BB",
        "lemma_id": "WL526_post_wl525_route_choice_audit",
        "work_log": "wl526",
        "input_work_log": "wl525",
        "object_layer": "post_wl525_route_choice_layer",
        "post_wl525_route_state_summary": (
            _post_wl525_route_state_summary(wl525) if status == "ok" else {}
        ),
        "route_families": _route_families(),
        "selected_next_gate": (
            _selected_next_gate()
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl525_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "selected_route_entered_here": False,
        "function_field_models_built_here": False,
        "function_field_squareclass_certificate_proved_here": False,
        "uniform_cover_family_lemma_proved_here": False,
        "complete_selmer_local_hilbert_row_obligation_named_here": False,
        "proof_level_local_or_hilbert_row_proved_here": False,
        "abandoned_obstruction_line_here": False,
        "different_candidate_selected_here": False,
        "finite_shell_m_tail_diagnostics_selected_here": False,
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
        "advance_to_wl527": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Later scope the minimum function-field squareclass proof data for "
            "the named cover families. wl526 chooses that gate only; it does "
            "not build function-field models, prove the uniform lemma, execute "
            "shell 11, compute supports, test C_d solubility, apply wl491 to "
            "new points, select a candidate, abandon the obstruction line, or "
            "claim theorem-level Selmer progress."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl525", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl526_post_wl525_route_choice_audit(wl525=load_json(args.wl525))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl526 post-wl525 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
