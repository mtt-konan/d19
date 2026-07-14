#!/usr/bin/env python3
"""Canonical C3 composition and strict CLI for wl569-wl585."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.theory.aa_bb.c2_pure_v_ell import build_c2
from scripts.theory.aa_bb.c3_magnitude_descent import build_c3_magnitude_descent
from scripts.theory.aa_bb.c3_quotient_limits import build_c3_quotient_limits
from scripts.theory.aa_bb.c3_real_branch import build_c3_real_branch

C3_STAGES = tuple(f"wl{number}" for number in range(569, 586))

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
    "rational_wl535_point_produced_here",
}

_STAGE_TOP_LEVEL_KEYS: dict[str, set[str]] = {
    "wl569": {"branch_certificate", "next_exact_lemma", "symbolic_certificate"},
    "wl570": {"system_certificate", "symbolic_certificate"},
    "wl571": {"cover_certificate", "symbolic_certificate"},
    "wl572": {"integrality_certificate", "symbolic_certificate"},
    "wl573": {"denominator_certificate", "symbolic_certificate"},
    "wl574": {"double_split_certificate", "symbolic_certificate"},
    "wl575": {"rotation_certificate", "symbolic_certificate"},
    "wl576": {"transport_certificate", "symbolic_certificate"},
    "wl577": {"same_side_certificate", "symbolic_certificate"},
    "wl578": {"dyadic_certificate", "remaining_magnitude_system", "symbolic_certificate"},
    "wl579": {"magnitude_curve_certificate", "symbolic_certificate"},
    "wl580": {"reconstruction_certificate", "exact_missing_lemma", "symbolic_certificate"},
    "wl581": {"quotient_certificate", "symbolic_certificate"},
    "wl582": {"descent_certificate", "symbolic_certificate"},
    "wl583": {"fiber_product_certificate", "symbolic_certificate"},
    "wl584": {"intersection_certificate", "symbolic_certificate"},
    "wl585": {"cover_certificate", "symbolic_certificate"},
}

C3_ALLOWLISTS: dict[str, frozenset[str]] = {
    work_log: frozenset(_COMMON_TOP_LEVEL_KEYS | _STAGE_TOP_LEVEL_KEYS[work_log])
    for work_log in C3_STAGES
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_TRUE_PROOF_KEYS: dict[str, frozenset[str]] = {
    "wl569": frozenset(
        {
            "source_square_and_positivity_force_0_lt_X_lt_ell_here",
            "F_strictly_negative_on_candidate_range_here",
            "positive_ordered_norm_ratio_branch_unique_here",
            "strict_cone_ratio_interval_proved_here",
        }
    ),
    "wl570": frozenset(
        {
            "quartic_square_root_eliminated_by_unique_tau_here",
            "parameter_formula_in_X_tau_proved_here",
            "both_source_squares_factored_in_X_tau_here",
            "forward_and_converse_wl535_reconstruction_proved_here",
        }
    ),
    "wl571": frozenset(
        {
            "product_quartic_smooth_genus_one_for_all_admissible_tau_here",
            "full_source_square_cover_genus_five_for_tau_ne_half_here",
            "tau_half_unique_genus_drop_to_one_here",
            "product_plus_one_square_converse_proved_here",
        }
    ),
    "wl572": frozenset(
        {
            "integral_parameter_forces_q_denominator_one_here",
            "integral_parameter_forces_q_numerator_square_divides_four_here",
            "positivity_leaves_only_X_four_here",
            "tau_half_excluded_for_odd_prime_parameter_here",
        }
    ),
    "wl573": frozenset(
        {
            "q_numerator_square_supports_on_four_mn_here",
            "q_denominator_square_supports_on_mn_here",
            "Delta_coprime_to_mn_here",
            "Delta_divides_positive_quartic_form_here",
        }
    ),
    "wl574": frozenset(
        {
            "both_source_pairs_share_canonical_Delta_squareclass_here",
            "AB_common_gcd_supported_on_R1_here",
            "CD_common_gcd_supported_on_R2_here",
            "two_complementary_splits_of_same_k_proved_here",
        }
    ),
    "wl575": frozenset(
        {
            "exact_scaled_Gaussian_rotation_proved_here",
            "inverse_rotation_and_norm_identity_proved_here",
            "PK_primitive_away_from_two_here",
            "R1R2_primitive_away_from_two_here",
            "two_k_allocations_structurally_coupled_here",
        }
    ),
    "wl576": frozenset(
        {
            "odd_k_primes_force_two_quadratic_residue_here",
            "regular_same_side_transport_by_K_here",
            "regular_crossed_side_transport_by_P_here",
            "R1_singular_pair_vanishes_together_here",
            "R2_singular_pair_vanishes_together_here",
            "singular_side_requires_higher_valuation_here",
        }
    ),
    "wl577": frozenset(
        {
            "global_Delta_divisibility_forces_all_odd_k_primes_into_K_here",
            "odd_singular_determinant_cases_eliminated_here",
            "odd_crossed_transport_eliminated_here",
            "two_allocations_have_identical_odd_parts_here",
            "factor_two_is_only_remaining_transport_here",
        }
    ),
    "wl578": frozenset(
        {
            "normalized_rotation_is_diagonal_odd_offdiagonal_even_here",
            "two_adic_valuation_order_preserved_here",
            "factor_two_transports_same_side_here",
            "two_complementary_k_allocations_identical_here",
            "allocation_analysis_exhausted_here",
        }
    ),
    "wl579": frozenset(
        {
            "biquadratic_genus_one_curve_proved_here",
            "common_allocation_magnitude_reduced_to_Mobius_map_here",
            "projective_magnitude_converse_proved_here",
            "strict_normalized_magnitude_ordering_proved_here",
        }
    ),
    "wl580": frozenset(
        {
            "allocation_descent_exhausted_here",
            "canonical_squareclass_self_consistency_stated_here",
            "primitive_m_n_has_no_extra_branch_here",
            "source_squares_reconstructed_from_self_consistent_torsor_here",
            "tau_uniquely_reconstructed_from_X_z_here",
        }
    ),
    "wl581": frozenset(
        {
            "genus_two_character_quotient_proved_here",
            "quadratic_elliptic_quotient_over_q_i_proved_here",
            "restricted_affine_candidate_image_proved_here",
        }
    ),
    "wl582": frozenset(
        {
            "nonbranch_forward_and_inverse_bijection_proved_here",
            "q_i_real_coordinate_locus_split_here",
            "quadratic_lift_obstruction_shown_automatic_here",
            "rational_genus_two_lift_reconstructed_here",
            "wl581_unrestricted_elliptic_route_exhausted_here",
        }
    ),
    "wl583": frozenset(
        {
            "exceptional_tau_half_preserved_and_not_reopened_here",
            "full_cover_fiber_product_equivalence_proved_here",
            "individual_source_squares_retained_on_torsor_here",
            "source_square_torsor_genus_one_proved_here",
            "square_x_pullback_independent_and_connected_here",
            "unramified_degree_two_map_to_product_elliptic_proved_here",
        }
    ),
    "wl584": frozenset(
        {
            "final_norm_discriminant_equivalence_proved_here",
            "fixed_ell_source_curve_genus_one_proved_here",
            "prime_coupled_torsor_source_identities_proved_here",
            "square_x_source_cover_genus_one_proved_here",
            "unrestricted_source_elliptic_route_exhausted_here",
        }
    ),
    "wl585": frozenset(
        {
            "combined_rational_elliptic_quotient_proved_here",
            "combined_source_norm_genus_three_quotient_proved_here",
            "fixed_ell_full_cover_genus_seventeen_proved_here",
            "norm_bearing_character_quotients_classified_here",
            "selected_tau_interval_equivalent_to_positivity_here",
        }
    ),
}

_STAGE_FALSE_PROOF_KEYS: dict[str, frozenset[str]] = {
    "wl569": frozenset({"selected_orientation_norm_intersection_solved_here"}),
    "wl570": frozenset({"two_variable_square_system_solved_here"}),
    "wl571": frozenset({"exceptional_tau_half_branch_solved_here"}),
    "wl572": frozenset({"generic_tau_cover_solved_here"}),
    "wl573": frozenset({"generic_genus_five_cover_solved_here"}),
    "wl574": frozenset({"generic_genus_five_cover_solved_here"}),
    "wl575": frozenset({"generic_genus_five_cover_solved_here"}),
    "wl576": frozenset({"generic_genus_five_cover_solved_here"}),
    "wl577": frozenset({"generic_genus_five_cover_solved_here"}),
    "wl578": frozenset({"generic_genus_five_cover_solved_here"}),
    "wl579": frozenset(
        {"primitive_linear_form_reconstruction_proved_here", "generic_genus_five_cover_solved_here"}
    ),
    "wl580": frozenset({"self_consistent_genus_one_family_solved_here"}),
    "wl581": frozenset({"restricted_elliptic_image_locus_solved_here"}),
    "wl582": frozenset(),
    "wl583": frozenset({"square_x_torsor_points_solved_here"}),
    "wl584": frozenset({"final_norm_intersection_solved_here"}),
    "wl585": frozenset({"restricted_combined_elliptic_image_solved_here"}),
}

C3_PROOF_ALLOWLISTS: dict[str, frozenset[str]] = {
    work_log: frozenset(
        _COMMON_PROOF_KEYS | _STAGE_TRUE_PROOF_KEYS[work_log] | _STAGE_FALSE_PROOF_KEYS[work_log]
    )
    for work_log in C3_STAGES
}

_EXPECTED_PREDECESSOR = dict(
    zip(C3_STAGES, (f"wl{number}" for number in range(568, 585)), strict=True)
)
_NO_CLAIM_TOP_LEVEL = (
    "complete_selmer_upper_bound_proved",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
    "advance_to_m3",
    "rational_wl535_point_produced_here",
)


@dataclass(frozen=True)
class C3Evidence:
    """Computed C3 stages at the shared composition boundary."""

    stages: dict[str, dict[str, Any]]

    def __getitem__(self, work_log: str) -> dict[str, Any]:
        return self.stages[work_log]


def _c2_stages(c2: Any) -> Mapping[str, Any] | None:
    stages = getattr(c2, "stages", None)
    if isinstance(stages, Mapping):
        return stages
    if isinstance(c2, Mapping):
        nested = c2.get("stages")
        if isinstance(nested, Mapping):
            return nested
        return c2
    return None


def _c2_boundary_ready(payload: Any) -> bool:
    if not isinstance(payload, Mapping):
        return False
    proof = payload.get("proof_status")
    return (
        payload.get("work_log") == "wl568"
        and payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("violations") == []
        and isinstance(proof, Mapping)
        and proof.get("allocation_route_independent_obstruction_refuted_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and proof.get("advance_to_m3") is False
        and all(payload.get(key) is False for key in _NO_CLAIM_TOP_LEVEL)
        and payload.get("stop_after_current_task") is True
    )


def _canonical_wl568(c2: Any) -> Mapping[str, Any]:
    stages = _c2_stages(c2)
    payload = stages.get("wl568") if stages is not None else None
    return payload if _c2_boundary_ready(payload) else {}


def _stage_or_empty(stages: Any, work_log: str) -> Mapping[str, Any]:
    if isinstance(stages, Mapping):
        payload = stages.get(work_log)
        if isinstance(payload, Mapping):
            return payload
    return {}


def build_c3(c2: Any | None = None) -> C3Evidence:
    """Build the three canonical C3 slices exactly once and in order."""
    if c2 is None:
        c2 = build_c2()
    real_stages = build_c3_real_branch(_canonical_wl568(c2))
    magnitude_stages = build_c3_magnitude_descent(_stage_or_empty(real_stages, "wl574"))
    quotient_stages = build_c3_quotient_limits(_stage_or_empty(magnitude_stages, "wl580"))
    stages: dict[str, dict[str, Any]] = {}
    for slice_stages in (real_stages, magnitude_stages, quotient_stages):
        if isinstance(slice_stages, Mapping):
            stages.update(slice_stages)
    return C3Evidence(stages=stages)


def _stages_for(evidence: C3Evidence | Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    if isinstance(evidence, C3Evidence):
        return evidence.stages
    if isinstance(evidence, Mapping):
        return evidence
    raise TypeError("C3 evidence must be a C3Evidence or mapping")


def project_stage(
    evidence: C3Evidence | Mapping[str, Mapping[str, Any]], work_log: str
) -> dict[str, Any]:
    """Return one stage after enforcing the exact 17-stage composition map."""
    if work_log not in C3_STAGES:
        raise KeyError(f"unknown C3 work log: {work_log}")
    stages = _stages_for(evidence)
    if work_log not in stages:
        raise KeyError(f"missing C3 work log: {work_log}")
    payload = stages[work_log]
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def _validate_ready_semantics(
    payload: Mapping[str, Any], work_log: str, proof: Mapping[str, Any]
) -> None:
    if set(proof) != C3_PROOF_ALLOWLISTS[work_log]:
        raise ValueError(f"incomplete proof_status for {work_log}")
    for key in _STAGE_TRUE_PROOF_KEYS[work_log]:
        if proof.get(key) is not True:
            raise ValueError(f"required proof field changed for {work_log}: {key}")
    for key in _COMMON_PROOF_KEYS | _STAGE_FALSE_PROOF_KEYS[work_log]:
        if proof.get(key) is not False:
            raise ValueError(f"no-claim proof field changed for {work_log}: {key}")
    for key in _NO_CLAIM_TOP_LEVEL:
        if payload.get(key) is not False:
            raise ValueError(f"no-claim field changed for {work_log}: {key}")
    if payload.get("stop_after_current_task") is not True:
        raise ValueError(f"task boundary changed for {work_log}")


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a stage onto its exact semantic allowlist."""
    if work_log not in C3_STAGES:
        raise KeyError(f"unknown C3 work log: {work_log}")
    if not isinstance(payload, Mapping):
        raise ValueError(f"invalid stage payload for {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = C3_ALLOWLISTS[work_log]
    unknown = set(payload) - allowed - {"ready", "violations"}
    if unknown:
        raise ValueError(f"unallowlisted fields for {work_log}: {sorted(unknown)}")
    missing = allowed - set(payload)
    if missing:
        raise ValueError(f"missing allowlisted fields for {work_log}: {sorted(missing)}")
    if "ready" in payload and not isinstance(payload["ready"], bool):
        raise ValueError(f"invalid ready field for {work_log}")
    if "violations" in payload and not isinstance(payload["violations"], list):
        raise ValueError(f"invalid violations field for {work_log}")
    checkpoint = payload["input_checkpoint"]
    if (
        not isinstance(checkpoint, Mapping)
        or set(checkpoint) != {"work_log", "ready"}
        or checkpoint.get("work_log") != _EXPECTED_PREDECESSOR[work_log]
        or not isinstance(checkpoint.get("ready"), bool)
    ):
        raise ValueError(f"invalid input checkpoint for {work_log}")
    proof = payload["proof_status"]
    if not isinstance(proof, Mapping):
        raise ValueError(f"invalid proof_status for {work_log}")
    proof_allowed = C3_PROOF_ALLOWLISTS[work_log]
    unknown_proof = set(proof) - proof_allowed
    if unknown_proof:
        raise ValueError(f"unallowlisted proof fields for {work_log}: {sorted(unknown_proof)}")
    status = payload.get("status")
    if status not in {"ok", "issues"}:
        raise ValueError(f"invalid status for {work_log}")
    if status == "ok":
        _validate_ready_semantics(payload, work_log, proof)
    elif proof and set(proof) != proof_allowed:
        raise ValueError(f"incomplete proof_status for {work_log}")
    projected = {key: payload[key] for key in allowed}
    projected["proof_status"] = dict(proof)
    return json.loads(json.dumps(projected, sort_keys=True))


def _strict_ready(evidence: C3Evidence | Mapping[str, Mapping[str, Any]]) -> bool:
    try:
        stages = _stages_for(evidence)
        if tuple(stages) != C3_STAGES:
            return False
        for work_log in C3_STAGES:
            stage = project_stage(evidence, work_log)
            semantic_projection(stage, work_log)
            if (
                stage.get("status") != "ok"
                or stage.get("ready") is not True
                or stage.get("violations") != []
                or stage.get("work_log") != work_log
                or stage["input_checkpoint"].get("ready") is not True
            ):
                return False
            _validate_ready_semantics(stage, work_log, stage["proof_status"])
        return True
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    evidence = build_c3()
    payload = {"schema_version": 1, "stages": evidence.stages}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ok = _strict_ready(evidence)
    print(f"stage_count={len(evidence.stages)}")
    print(f"status={'ok' if ok else 'issues'}")
    return 1 if args.strict and not ok else 0


if __name__ == "__main__":
    raise SystemExit(main())
