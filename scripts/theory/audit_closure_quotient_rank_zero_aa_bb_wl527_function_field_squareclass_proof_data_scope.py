#!/usr/bin/env python3
"""Scope wl527 function-field squareclass proof data for named cover families."""

from __future__ import annotations

import argparse
from collections import Counter
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
    "This audits only wl527 / function_field_squareclass_proof_data_scope. "
    "It uses wl526 as immediate input and wl522 only as the named finite "
    "cover-family inventory. It enters the wl526-selected proof-data scoping "
    "gate at the cover-family function-field proof-data layer, inventories "
    "the minimum data needed for a later uniform squareclass proof attempt, "
    "and stops after deciding whether the current data is ready. It does not "
    "prove the uniform lemma, build a function-field engine, execute shell "
    "11, compute new M_tail supports, test new ambient C_d solubility, apply "
    "wl491 to a new point, run broad rank or Selmer diagnostics, use the old "
    "package-x S~ bridge, name a theorem-level Selmer row, select a final "
    "obstruction candidate, or claim complete Sel_2(E) upper bound, dim "
    "Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, theorem-level "
    "progress, or family exclusion."
)

MISSING_DATA_CLASSES = [
    "explicit_cover_family_function_field_model",
    "rational_source_side_maps_on_family",
    "N_M_as_function_field_elements",
    "opposite_side_product_squareclass_or_divisor_parity_certificate",
    "exceptional_specialization_and_positivity_separation",
]

EXCEPTIONAL_SPECIALIZATION_CHECKLIST = [
    "separate poles and zeroes of N, M, and the opposite-side product",
    "separate exceptional divisors where the source-side pullback is undefined",
    "separate specializations where centered-even or rationality hypotheses fail",
    "separate N_not_positive and M_not_positive from squareclass failure",
    "separate degeneracy of A, B, N, M, or source-side products from squareclass failure",
    "record positivity domain before any later uniform proof attempt",
]


def _wl526_ready(wl526: dict[str, Any]) -> bool:
    selected = wl526.get("selected_next_gate", {})
    return (
        wl526.get("status") == "ok"
        and wl526.get("ready") is True
        and wl526.get("lemma_id") == "WL526_post_wl525_route_choice_audit"
        and wl526.get("work_log") == "wl526"
        and wl526.get("input_work_log") == "wl525"
        and selected.get("gate")
        == "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families"
        and selected.get("entered_here") is False
        and selected.get("object_layer")
        == "cover_family_function_field_proof_data_scoping"
        and selected.get("builds_function_field_models_here") is False
        and selected.get("proves_uniform_lemma_here") is False
        and wl526.get("selected_route_entered_here") is False
        and wl526.get("function_field_models_built_here") is False
        and wl526.get("function_field_squareclass_certificate_proved_here") is False
        and wl526.get("uniform_cover_family_lemma_proved_here") is False
        and wl526.get("advance_to_wl527") is False
        and wl526.get("shell11_executed_here") is False
        and wl526.get("m_tail_diagnostics_extended_here") is False
        and wl526.get("new_supports_computed_here") is False
        and wl526.get("new_c_d_solubility_tested_here") is False
        and wl526.get("wl491_filter_applied_to_new_point_here") is False
        and wl526.get("final_obstruction_candidate_selected_here") is False
        and wl526.get("old_package_x_coordinate_collapse_used") is False
        and wl526.get("package_x_s_tilde_bridge_used") is False
        and not _claims_forbidden_bound(wl526)
    )


def _wl522_ready(wl522: dict[str, Any]) -> bool:
    summary = wl522.get("taxonomy_summary", {})
    selected = wl522.get("selected_next_proof_level_lemma_candidate", {})
    return (
        wl522.get("status") == "ok"
        and wl522.get("ready") is True
        and wl522.get("lemma_id")
        == "WL522_support_cover_taxonomy_to_lemma_candidate_checkpoint"
        and wl522.get("work_log") == "wl522"
        and wl522.get("support_cover_taxonomy_built_here") is True
        and summary.get("globally_soluble_but_not_aa_bb_admissible_cover_family_count")
        == 15
        and summary.get("globally_soluble_but_not_aa_bb_admissible_entry_count")
        == 29
        and summary.get("genuinely_deferred_cover_family_count") == 0
        and summary.get("aa_bb_admissible_cover_family_count") == 0
        and selected.get("lemma_candidate_id")
        == "common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
        and selected.get("entered_here") is False
        and wl522.get("shell11_executed_here") is False
        and wl522.get("m_tail_diagnostics_extended_here") is False
        and wl522.get("new_supports_computed_here") is False
        and wl522.get("new_c_d_solubility_tested_here") is False
        and wl522.get("wl491_filter_applied_to_new_point_here") is False
        and wl522.get("final_obstruction_candidate_selected_here") is False
        and wl522.get("old_package_x_coordinate_collapse_used") is False
        and wl522.get("package_x_s_tilde_bridge_used") is False
        and not _claims_forbidden_bound(wl522)
    )


def _named_not_admissible_rows(wl522: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in wl522.get("support_cover_taxonomy", [])
        if row.get("classification") == "globally_soluble_but_not_aa_bb_admissible"
        and row.get("failure_mode") == "common_source_aa_bb_admissibility_failure"
        and row.get("lemma_candidate_status") == "theorem-candidate"
    ]


def _source_sides(candidate_ids: list[str]) -> list[str]:
    sides = {
        candidate_id.split("_", 1)[0]
        for candidate_id in candidate_ids
        if candidate_id.startswith(("AA_", "BB_"))
    }
    return sorted(sides)


def _model_availability(row: dict[str, Any]) -> dict[str, Any]:
    cover_summary = row.get("cover_summary", {})
    d_vector = cover_summary.get("d_vector") or {}
    if d_vector:
        return {
            "status": "label_and_l_t_d_vector_only_no_explicit_function_field_model",
            "has_cover_family_label": True,
            "has_l_t_parameters": True,
            "has_explicit_d_vector": True,
            "has_explicit_equation": False,
            "has_function_field_coordinates": False,
            "available_data": {
                "L": cover_summary.get("L"),
                "T": cover_summary.get("T"),
                "d_vector": d_vector,
            },
        }
    return {
        "status": "cover_label_only_missing_explicit_d_vector_and_equation",
        "has_cover_family_label": True,
        "has_l_t_parameters": True,
        "has_explicit_d_vector": False,
        "has_explicit_equation": False,
        "has_function_field_coordinates": False,
        "available_data": {
            "L": cover_summary.get("L"),
            "T": cover_summary.get("T"),
            "d_vector": {},
        },
    }


def _opposite_side_target() -> dict[str, str]:
    return {
        "status": "formula_target_only_not_a_certificate",
        "AA_source_target": "(N^2 + B^2)(M^2 + B^2)",
        "BB_source_target": "(N^2 + A^2)(M^2 + A^2)",
        "certificate_needed": (
            "non-square in the cover-family function field, or equivalent "
            "divisor-parity squareclass obstruction surviving specialization"
        ),
    }


def _inventory_row(row: dict[str, Any]) -> dict[str, Any]:
    candidate_ids = list(row.get("candidate_ids", []))
    missing_data_classes = list(MISSING_DATA_CLASSES)
    if not (row.get("cover_summary", {}).get("d_vector") or {}):
        missing_data_classes.append("explicit_d_vector_for_family_label")

    return {
        "cover_family": row["cover_family"],
        "support_family": row["support_family"],
        "classification": row["classification"],
        "failure_mode": row["failure_mode"],
        "ambient_c_d_global_solubility_status": row[
            "ambient_c_d_global_solubility_status"
        ],
        "lemma_candidate_status": row["lemma_candidate_status"],
        "entry_count": row["entry_count"],
        "candidate_ids": candidate_ids,
        "source_sides_to_map": _source_sides(candidate_ids),
        "work_logs": row.get("work_logs", []),
        "blocking_reasons_seen_at_point_level": row.get("blocking_reasons", []),
        "cover_family_model_availability": _model_availability(row),
        "rational_source_side_maps": {
            "status": "missing_uniform_maps",
            "point_level_wl491_failures_available": True,
            "uniform_family_maps_available": False,
            "needed": (
                "rational maps from the cover-family function field to the "
                "AA/BB source-side variables before N and M can be functions"
            ),
        },
        "candidate_function_field_elements": {
            "status": "missing_N_M_as_function_field_elements",
            "point_level_formula_template_only": {
                "N": "(A+B+t)/2",
                "M": "A+B-N",
            },
            "N_in_function_field_available": False,
            "M_in_function_field_available": False,
        },
        "opposite_side_target": _opposite_side_target(),
        "exceptional_specialization_positivity_checklist": list(
            EXCEPTIONAL_SPECIALIZATION_CHECKLIST
        ),
        "readiness": "not_ready_for_later_uniform_squareclass_proof_attempt",
        "missing_data_classes": missing_data_classes,
    }


def _missing_data_class_counts(
    inventory: list[dict[str, Any]],
) -> dict[str, int]:
    counts = Counter(
        missing
        for row in inventory
        for missing in row.get("missing_data_classes", [])
    )
    return dict(sorted(counts.items()))


def _scope_summary(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    ready_count = sum(
        row["readiness"] == "ready_for_later_uniform_squareclass_proof_attempt"
        for row in inventory
    )
    complete_label_count = sum(
        row["cover_family_model_availability"]["has_explicit_d_vector"]
        for row in inventory
    )
    entry_count = sum(int(row["entry_count"]) for row in inventory)
    return {
        "named_cover_family_count": len(inventory),
        "named_entry_count": entry_count,
        "ready_for_later_uniform_squareclass_proof_attempt": ready_count
        == len(inventory),
        "ready_cover_family_count": ready_count,
        "not_ready_cover_family_count": len(inventory) - ready_count,
        "cover_families_with_label_and_l_t_d_data_count": complete_label_count,
        "cover_families_missing_explicit_d_vector_count": len(inventory)
        - complete_label_count,
        "exact_missing_data_class": (
            "uniform_function_field_model_maps_and_squareclass_certificate"
        ),
        "decision": (
            "Current wl522/wl526 data is not ready for a later uniform "
            "squareclass proof attempt. The exact missing class is explicit "
            "cover-family function-field models with rational source-side maps, "
            "N,M as function-field elements, and an opposite-side product "
            "squareclass or divisor-parity certificate with exceptional "
            "specialization and positivity separated."
        ),
    }


def build_wl527_function_field_squareclass_proof_data_scope(
    *,
    wl522: dict[str, Any],
    wl526: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl526_ready(wl526):
        violations.append("wl526_input_not_ready_or_not_scoped")
    if not _wl522_ready(wl522):
        violations.append("wl522_named_cover_family_inventory_not_ready")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    inventory = (
        [_inventory_row(row) for row in _named_not_admissible_rows(wl522)]
        if ready
        else []
    )

    if ready and len(inventory) != 15:
        violations.append("named_cover_family_inventory_count_mismatch")
        status = "issues"
        ready = False
        inventory = []

    return {
        "status": status,
        "ready": ready,
        "source": "wl526 selected minimal function-field proof-data scoping",
        "pattern": "AA+BB",
        "lemma_id": "WL527_function_field_squareclass_proof_data_scope",
        "work_log": "wl527",
        "input_work_logs": ["wl526", "wl522"],
        "immediate_input_work_log": "wl526",
        "object_layer": "cover_family_function_field_proof_data_scoping",
        "selected_gate_entered_here": ready,
        "function_field_proof_data_scoped_here": ready,
        "scope_summary": _scope_summary(inventory) if ready else {},
        "minimum_data_classes_scoped": list(MISSING_DATA_CLASSES),
        "cover_family_proof_data_inventory": inventory,
        "missing_data_class_counts": (
            _missing_data_class_counts(inventory) if ready else {}
        ),
        "proof_data_readiness_decision": (
            {
                "ready_for_later_uniform_squareclass_proof_attempt": False,
                "uniform_lemma_proved_here": False,
                "mathematical_uniform_lemma_refuted_here": False,
                "finite_taxonomy_promoted_here": False,
                "exact_missing_data_class": (
                    "uniform_function_field_model_maps_and_squareclass_certificate"
                ),
            }
            if ready
            else {}
        ),
        "next_gap_not_entered": (
            "A later step would have to supply explicit function-field models "
            "and rational source-side maps for the named cover families, then "
            "state N,M and the opposite-side product in those function fields "
            "and prove a squareclass or divisor-parity certificate. wl527 "
            "does not enter that proof attempt."
        ),
        "function_field_models_built_here": False,
        "function_field_engine_built_here": False,
        "function_field_squareclass_certificate_proved_here": False,
        "uniform_cover_family_lemma_proved_here": False,
        "complete_selmer_local_hilbert_row_obligation_named_here": False,
        "proof_level_local_or_hilbert_row_proved_here": False,
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
        "final_obstruction_candidate_selected_here": False,
        "candidate_selected_here": False,
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
    parser.add_argument("--wl522", type=Path, required=True)
    parser.add_argument("--wl526", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl527_function_field_squareclass_proof_data_scope(
        wl522=load_json(args.wl522),
        wl526=load_json(args.wl526),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl527 function-field proof-data scope to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    summary = audit.get("scope_summary", {})
    print(f"named_cover_family_count={summary.get('named_cover_family_count')}")
    print(
        "ready_for_later_uniform_squareclass_proof_attempt="
        f"{summary.get('ready_for_later_uniform_squareclass_proof_attempt')}"
    )
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
