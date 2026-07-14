#!/usr/bin/env python3
"""Canonical C2 composition and strict CLI for wl542-wl568."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.theory.aa_bb.c1_pure_v_ell import build_c1
from scripts.theory.aa_bb.c2_allocation import build_c2_allocation
from scripts.theory.aa_bb.c2_character_system import build_c2_character_system
from scripts.theory.aa_bb.c2_global_descent import build_c2_global_descent

C2_STAGES = tuple(f"wl{number}" for number in range(542, 569))

_COMMON_TOP_LEVEL_KEYS = {
    "status",
    "work_log",
    "object_layer",
    "input_checkpoint",
    "proof_status",
    "complete_selmer_upper_bound_proved",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
    "advance_to_m3",
    "stop_after_current_task",
}

C2_ALLOWLISTS: dict[str, frozenset[str]] = {
    "wl542": frozenset(_COMMON_TOP_LEVEL_KEYS | {"denominator_support", "local_converse"}),
    "wl543": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "descent",
            "unit_squareclass_split",
            "symbolic_certificate",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl544": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "coordinate_forms",
            "explicit_system",
            "trivial_unit_branch",
            "symbolic_certificate",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl545": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "q_valuation_dichotomy",
            "descent_variable_parity",
            "residue_certificate",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl546": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "Gaussian_descent",
            "double_descent_system",
            "primitive_conditions",
            "symbolic_certificate",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl547": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "Gaussian_norm",
            "finite_support",
            "squareclass_equation",
            "symbolic_certificate",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl548": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {"valuation_certificate", "refined_support", "rational_wl535_point_produced_here"}
    ),
    "wl549": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {"identities_at_a_root", "classification", "rational_wl535_point_produced_here"}
    ),
    "wl550": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "certificate",
            "global_integer_candidate_produced_here",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl551": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"norm_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl552": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"parity_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl553": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "positivity_certificate",
            "full_coordinate_solution_produced_here",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl554": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"gcd_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl555": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"standard_equation", "rational_wl535_point_produced_here"}
    ),
    "wl556": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"orientation_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl557": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"valuation_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl558": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"character_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl559": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {"leading_character_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl560": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {"normalized_character_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl561": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "matrix_certificate",
            "theorem_level_selmer_matrix_claimed",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl562": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"witness_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl563": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"factorization_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl564": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"allocation_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl565": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"allocation_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl566": frozenset(
        _COMMON_TOP_LEVEL_KEYS | {"quartic_certificate", "rational_wl535_point_produced_here"}
    ),
    "wl567": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "affine_system_certificate",
            "theorem_level_selmer_matrix_claimed",
            "rational_wl535_point_produced_here",
        }
    ),
    "wl568": frozenset(
        _COMMON_TOP_LEVEL_KEYS
        | {
            "redundancy_certificate",
            "next_exact_lemma",
            "symbolic_certificate",
            "rational_wl535_point_produced_here",
        }
    ),
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_PROOF_KEYS: dict[str, set[str]] = {
    "wl542": {
        "global_denominator_is_odd_and_coprime_to_ell_here",
        "every_denominator_prime_splits_completely_here",
        "D_mod_ell_is_nonzero_square_here",
        "allowed_denominator_places_add_no_G_local_obstruction_here",
        "rational_wl535_point_produced_here",
    },
    "wl543": {
        "real_quadratic_alpha_is_totally_positive_integral_here",
        "principal_ideal_of_alpha_is_square_ideal_here",
        "ordinary_class_group_2_torsion_eliminated_by_genus_theory_here",
        "alpha_reduced_to_unit_times_element_square_here",
        "remaining_totally_positive_unit_squareclasses_at_most_two",
    },
    "wl544": {
        "abstract_unit_square_descent_expanded_here",
        "at_most_two_explicit_integer_quartic_branches_here",
        "Gaussian_G_and_positivity_pulled_back_exactly_here",
        "forward_and_converse_reconstruction_proved_here",
    },
    "wl545": {
        "trivial_unit_2_adic_q_valuation_classified_here",
        "ell_eq_5_mod_8_forces_u_v_odd_here",
        "ell_eq_1_mod_8_forces_even_halves_opposite_parity_here",
        "G_condition_adds_no_2_adic_obstruction_here",
    },
    "wl546": {
        "primitive_Gaussian_factors_proved_coprime_here",
        "Gaussian_square_reduced_to_two_orientations_here",
        "real_and_Gaussian_descents_coupled_here",
        "Gaussian_square_equation_eliminated_exactly_here",
    },
    "wl547": {
        "G_square_rewritten_as_Gaussian_norm_square_here",
        "common_odd_prime_support_bounded_by_ell_minus_1_here",
        "common_odd_primes_require_Legendre_2_eq_1_here",
        "G_square_reduced_to_finite_S_squareclasses_here",
        "theorem_level_Selmer_object_claimed_here",
    },
    "wl548": {
        "dyadic_delta_valuation_computed_exactly_here",
        "one_plus_i_squareclass_eliminated_here",
        "finite_support_reduced_to_odd_primes_here",
    },
    "wl549": {
        "root_square_condition_classified_here",
        "source_square_residues_automatic_at_square_root_here",
        "p_eq_7_mod_8_root_test_exhausted_here",
        "odd_Gaussian_class_equations_solved_here",
    },
    "wl550": {
        "both_wl546_orientations_locally_compatible_here",
        "quadratic_etale_hilbert_90_witness_given_here",
        "same_prime_orientation_route_exhausted_here",
        "global_odd_class_equation_solved_here",
    },
    "wl551": {
        "global_norm_square_parity_used_here",
        "split_Gaussian_primes_paired_here",
        "squarefree_factor_reduced_to_rational_integer_here",
        "global_rational_class_equations_solved_here",
    },
    "wl552": {
        "dyadic_parity_applied_to_global_class_equation_here",
        "Gaussian_unit_class_forced_to_i_here",
        "two_unit_classes_reduced_to_one_here",
        "remaining_eta_i_coordinate_system_solved_here",
    },
    "wl553": {
        "positivity_transferred_to_class_coordinates_here",
        "rational_squareclass_cancels_from_sign_here",
        "positivity_alone_exhausted_on_both_mod8_branches_here",
        "simultaneous_orientation_class_cone_system_solved_here",
    },
    "wl554": {
        "odd_coordinate_gcd_parity_of_Gaussian_square_proved_here",
        "rational_class_made_candidate_canonical_here",
        "independent_r_divisor_choice_eliminated_here",
        "canonical_class_equation_solved_here",
    },
    "wl555": {
        "standard_norm_element_identified_here",
        "Gaussian_unit_removed_uniformly_here",
        "branch_dependent_cone_signs_unified_here",
        "standard_orientation_square_system_solved_here",
    },
    "wl556": {
        "wl546_orientations_coupled_to_dyadic_branches_here",
        "one_complete_orientation_eliminated_per_branch_here",
        "ell_eq_5_mod_8_R_orientation_selected_here",
        "ell_eq_1_mod_8_B_orientation_selected_here",
        "surviving_orientation_systems_solved_here",
    },
    "wl557": {
        "surviving_orientations_stratified_2_adically_here",
        "real_and_Gaussian_descent_valuations_coupled_here",
        "ell_eq_5_mod_8_standalone_dyadic_route_exhausted_here",
        "ell_eq_1_mod_8_mixed_valuation_cases_eliminated_here",
        "surviving_valuation_strata_solved_here",
    },
    "wl558": {
        "global_class_equation_applied_at_odd_unit_places_here",
        "split_prime_character_condition_proved_here",
        "inert_prime_unit_condition_exhausted_here",
        "distinct_place_r_coupling_produced_here",
        "global_character_system_solved_here",
    },
    "wl559": {
        "positive_even_common_valuation_normalized_here",
        "split_prime_leading_character_classified_here",
        "inert_even_common_valuation_exhausted_here",
        "all_odd_places_not_in_r_classified_here",
        "global_character_system_solved_here",
    },
    "wl560": {
        "odd_common_leading_character_supplied_here",
        "all_valuation_parities_unified_here",
        "every_odd_ell_minus_one_place_fully_classified_here",
        "assembled_global_character_system_solved_here",
    },
    "wl561": {
        "split_prime_characters_assembled_as_F2_system_here",
        "reciprocity_product_over_odd_common_split_primes_proved_here",
        "split_split_pairwise_characters_cancelled_here",
        "reciprocity_matrix_uniform_contradiction_proved_here",
    },
    "wl562": {
        "opposite_leading_bits_with_same_local_stratum_proved_here",
        "both_Gaussian_orientations_locally_compatible_here",
        "local_orientation_determinacy_refuted_here",
        "global_integer_compatibility_resolved_here",
    },
    "wl563": {
        "global_product_coordinate_used_here",
        "coprime_squareclass_split_proved_here",
        "Gaussian_square_coordinates_reduced_to_fourth_powers_here",
        "orientation_product_scale_coupled_here",
        "complementary_divisor_split_systems_solved_here",
    },
    "wl564": {
        "dyadic_factor_in_complementary_split_allocated_here",
        "canonical_r_mod8_coupled_to_global_split_here",
        "binary_choice_at_2_removed_when_present_here",
        "odd_complementary_divisor_allocation_solved_here",
    },
    "wl565": {
        "real_coordinate_leading_unit_defined_here",
        "inert_odd_kappa_factors_assigned_here",
        "split_odd_kappa_square_unit_test_proved_here",
        "split_prime_binary_allocations_solved_here",
    },
    "wl566": {
        "quartic_sign_for_split_factor_defined_here",
        "alpha_side_quartic_character_proved_here",
        "beta_side_quartic_character_proved_here",
        "quartic_character_strictly_refines_split_allocation_here",
        "coupled_split_allocation_system_solved_here",
    },
    "wl567": {
        "quartic_allocation_linearized_over_F2_here",
        "affine_row_formula_proved_here",
        "exponential_case_split_removed_here",
        "affine_system_coupled_to_integer_equations_here",
    },
    "wl568": {
        "scale_is_exact_product_coordinate_rewrite_here",
        "cone_is_exact_original_positivity_rewrite_here",
        "affine_rows_automatic_for_actual_factorization_here",
        "allocation_route_independent_obstruction_refuted_here",
        "selected_orientation_norm_intersection_solved_here",
    },
}

_FALSE_TOP_LEVEL_STAGE_KEYS: dict[str, set[str]] = {
    "wl550": {"global_integer_candidate_produced_here"},
    "wl553": {"full_coordinate_solution_produced_here"},
    "wl561": {"theorem_level_selmer_matrix_claimed"},
    "wl567": {"theorem_level_selmer_matrix_claimed"},
}

_FALSE_PROOF_KEYS: dict[str, set[str]] = {
    "wl542": {"rational_wl535_point_produced_here"},
    "wl547": {"theorem_level_Selmer_object_claimed_here"},
    "wl549": {"odd_Gaussian_class_equations_solved_here"},
    "wl550": {"global_odd_class_equation_solved_here"},
    "wl551": {"global_rational_class_equations_solved_here"},
    "wl552": {"remaining_eta_i_coordinate_system_solved_here"},
    "wl553": {"simultaneous_orientation_class_cone_system_solved_here"},
    "wl554": {"canonical_class_equation_solved_here"},
    "wl555": {"standard_orientation_square_system_solved_here"},
    "wl556": {"surviving_orientation_systems_solved_here"},
    "wl557": {"surviving_valuation_strata_solved_here"},
    "wl558": {"global_character_system_solved_here"},
    "wl559": {"global_character_system_solved_here"},
    "wl560": {"assembled_global_character_system_solved_here"},
    "wl561": {"reciprocity_matrix_uniform_contradiction_proved_here"},
    "wl562": {"global_integer_compatibility_resolved_here"},
    "wl563": {"complementary_divisor_split_systems_solved_here"},
    "wl564": {"odd_complementary_divisor_allocation_solved_here"},
    "wl565": {"split_prime_binary_allocations_solved_here"},
    "wl566": {"coupled_split_allocation_system_solved_here"},
    "wl567": {"affine_system_coupled_to_integer_equations_here"},
    "wl568": {"selected_orientation_norm_intersection_solved_here"},
}


@dataclass(frozen=True)
class C2Evidence:
    """Computed C2 stages at the shared composition boundary."""

    stages: dict[str, dict[str, Any]]

    def __getitem__(self, work_log: str) -> dict[str, Any]:
        return self.stages[work_log]


def build_c2(c1: Any | None = None) -> C2Evidence:
    """Run the three canonical C2 slices exactly once in order."""
    if c1 is None:
        c1 = build_c1()
    global_stages = build_c2_global_descent(c1["wl541"])
    character_stages = build_c2_character_system(global_stages["wl552"])
    allocation_stages = build_c2_allocation(character_stages["wl562"])
    stages: dict[str, dict[str, Any]] = {}
    stages.update(global_stages)
    stages.update(character_stages)
    stages.update(allocation_stages)
    return C2Evidence(stages=stages)


def _stages_for(
    evidence: C2Evidence | Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Mapping[str, Any]]:
    return evidence.stages if isinstance(evidence, C2Evidence) else evidence


def project_stage(
    evidence: C2Evidence | Mapping[str, Mapping[str, Any]], work_log: str
) -> dict[str, Any]:
    """Return one stage after enforcing the exact 27-stage composition map."""
    if work_log not in C2_STAGES:
        raise KeyError(f"unknown C2 work log: {work_log}")
    stages = _stages_for(evidence)
    if work_log not in stages:
        raise KeyError(f"missing C2 work log: {work_log}")
    payload = stages[work_log]
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C2_STAGES:
        raise KeyError(f"unknown C2 work log: {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = C2_ALLOWLISTS[work_log]
    unknown = set(payload) - allowed - {"ready", "violations"}
    if unknown:
        raise ValueError(f"unallowlisted fields for {work_log}: {sorted(unknown)}")
    missing = allowed - set(payload)
    if missing:
        raise ValueError(f"missing allowlisted fields for {work_log}: {sorted(missing)}")
    proof = payload.get("proof_status")
    if not isinstance(proof, Mapping):
        raise ValueError(f"invalid proof_status for {work_log}")
    proof_allowed = _COMMON_PROOF_KEYS | _STAGE_PROOF_KEYS[work_log]
    unknown_proof = set(proof) - proof_allowed
    if unknown_proof:
        raise ValueError(f"unallowlisted proof fields for {work_log}: {sorted(unknown_proof)}")
    if payload.get("status") == "ok" and set(proof) != proof_allowed:
        raise ValueError(f"incomplete proof_status for {work_log}")
    projected = {key: payload[key] for key in allowed}
    projected["proof_status"] = dict(proof)
    return json.loads(json.dumps(projected, sort_keys=True))


def _strict_ready(evidence: C2Evidence | Mapping[str, Mapping[str, Any]]) -> bool:
    stages = _stages_for(evidence)
    if tuple(stages) != C2_STAGES:
        return False
    for work_log in C2_STAGES:
        try:
            stage = project_stage(evidence, work_log)
            semantic_projection(stage, work_log)
        except (KeyError, ValueError, TypeError):
            return False
        if (
            stage.get("status") != "ok"
            or stage.get("ready") is not True
            or stage.get("violations") != []
            or stage.get("work_log") != work_log
            or stage.get("complete_selmer_upper_bound_proved") is not False
            or stage.get("rank_zero_claimed") is not False
            or stage.get("sha2_trivial_claimed") is not False
            or stage.get("advance_to_m3") is not False
            or (
                work_log != "wl542" and stage.get("rational_wl535_point_produced_here") is not False
            )
            or stage["proof_status"].get("uniform_full_wl535_obstruction_proved_here") is not False
        ):
            return False
        if any(
            stage.get(key) is not False for key in _FALSE_TOP_LEVEL_STAGE_KEYS.get(work_log, ())
        ):
            return False
        if any(
            stage["proof_status"].get(key) is not False
            for key in _FALSE_PROOF_KEYS.get(work_log, ())
        ):
            return False
    return True


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    evidence = build_c2()
    payload = {"schema_version": 1, "stages": evidence.stages}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ok = _strict_ready(evidence)
    print(f"stage_count={len(evidence.stages)}")
    print(f"status={'ok' if ok else 'issues'}")
    return 1 if args.strict and not ok else 0


if __name__ == "__main__":
    raise SystemExit(main())
