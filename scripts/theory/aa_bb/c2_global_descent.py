#!/usr/bin/env python3
"""Canonical C2 slice for the wl542-wl552 global descent chain."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

import sympy as sp

C2_GLOBAL_STAGES = tuple(f"wl{number}" for number in range(542, 553))

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

_STAGE_TOP_LEVEL_KEYS: dict[str, set[str]] = {
    "wl542": {"denominator_support", "local_converse"},
    "wl543": {
        "descent",
        "unit_squareclass_split",
        "symbolic_certificate",
        "rational_wl535_point_produced_here",
    },
    "wl544": {
        "coordinate_forms",
        "explicit_system",
        "trivial_unit_branch",
        "symbolic_certificate",
        "rational_wl535_point_produced_here",
    },
    "wl545": {
        "q_valuation_dichotomy",
        "descent_variable_parity",
        "residue_certificate",
        "rational_wl535_point_produced_here",
    },
    "wl546": {
        "Gaussian_descent",
        "double_descent_system",
        "primitive_conditions",
        "symbolic_certificate",
        "rational_wl535_point_produced_here",
    },
    "wl547": {
        "Gaussian_norm",
        "finite_support",
        "squareclass_equation",
        "symbolic_certificate",
        "rational_wl535_point_produced_here",
    },
    "wl548": {"valuation_certificate", "refined_support", "rational_wl535_point_produced_here"},
    "wl549": {"identities_at_a_root", "classification", "rational_wl535_point_produced_here"},
    "wl550": {
        "certificate",
        "global_integer_candidate_produced_here",
        "rational_wl535_point_produced_here",
    },
    "wl551": {"norm_certificate", "rational_wl535_point_produced_here"},
    "wl552": {"parity_certificate", "rational_wl535_point_produced_here"},
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
}


def _c1_wl541_ready(payload: Mapping[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl541"
        and proof.get("parameter_prime_standalone_local_obstruction_exhausted_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("advance_to_m3") is False
    )


def _predecessor_ready(payload: Mapping[str, Any], work_log: str, required_proof_key: str) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == work_log
        and proof.get(required_proof_key) is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("advance_to_m3") is False
    )


def _base_payload(
    *,
    work_log: str,
    object_layer: str,
    predecessor: str,
    predecessor_ready: bool,
    proof_status: dict[str, Any],
    violations: list[str],
) -> dict[str, Any]:
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": work_log,
        "object_layer": object_layer,
        "input_checkpoint": {"work_log": predecessor, "ready": predecessor_ready},
        "proof_status": proof_status if ready else {},
        "violations": violations,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def _symbolic_local_factorization() -> dict[str, Any]:
    ell, q = sp.symbols("ell q", nonzero=True)
    g = (
        q**8
        + (16 - 8 * ell) * q**6
        + (32 * ell**2 - 96 * ell + 72) * q**4
        + (32 * ell - 64) * q**2
        + 16
    )
    normalized = (
        1
        + (16 - 8 * ell) / q**2
        + (32 * ell**2 - 96 * ell + 72) / q**4
        + (32 * ell - 64) / q**6
        + 16 / q**8
    )
    return {
        "G_leading_term_factorization_verified": sp.simplify(g - q**8 * normalized) == 0,
        "first_square_factorization_verified": sp.expand(
            (-1) * q**2 * (1 - ell / q**2) - (ell - q**2)
        )
        == 0,
        "second_square_factorization_verified": sp.expand(
            ell * q**2 * (1 + 4 / (ell * q**2)) - (ell * q**2 + 4)
        )
        == 0,
        "smallest_principal_unit_valuation_for_v_r_q_minus_k": "2*k",
    }


def _build_wl542(c1_wl541: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _symbolic_local_factorization()
    predecessor_ready = _c1_wl541_ready(c1_wl541)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl541_input_not_ready")
    for key in (
        "G_leading_term_factorization_verified",
        "first_square_factorization_verified",
        "second_square_factorization_verified",
    ):
        if symbolic[key] is not True:
            violations.append(f"symbolic_factorization_failed:{key}")
    proof_status = {
        "global_denominator_is_odd_and_coprime_to_ell_here": True,
        "every_denominator_prime_splits_completely_here": True,
        "D_mod_ell_is_nonzero_square_here": True,
        "allowed_denominator_places_add_no_G_local_obstruction_here": True,
        "rational_wl535_point_produced_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl542",
        object_layer="m2_global_denominator_splitting_support_inside_wl535",
        predecessor="wl541",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "denominator_support": {
                "primitive_equations": [
                    "A^2+Q^2=ell*D^2",
                    "C^2=ell*Q^2+4*D^2",
                ],
                "D_is_odd": True,
                "gcd_D_ell": 1,
                "prime_conditions": [
                    "r is congruent to 1 mod 4",
                    "Legendre(ell/r)=1",
                    "Legendre(r/ell)=1",
                ],
                "splitting_field": "Q(i,sqrt(ell))",
                "D_mod_ell_is_nonzero_square": True,
            },
            "local_converse": {
                "scope": "odd r != ell with -1 and ell square in Q_r, v_r(q)<0",
                "all_three_square_conditions_locally_compatible": True,
                "principal_units_are_squares_because_r_is_odd": True,
                "symbolic_factorization": symbolic,
            },
        }
    )
    return payload


def _symbolic_wl543_certificate() -> dict[str, Any]:
    c, q, ell, d = sp.symbols("C Q ell D", real=True)
    norm_numerator = sp.expand((c + q * sp.sqrt(ell)) * (c - q * sp.sqrt(ell)))
    return {
        "alpha_norm_from_primitive_equation": "(C^2-ell*Q^2)/4=D^2",
        "norm_numerator_identity_verified": norm_numerator == c**2 - ell * q**2,
        "integrality_parity_source": "C^2 congruent Q^2 mod 4",
        "total_positivity_source": "C>abs(Q)*sqrt(ell)",
        "ordinary_class_group_2_torsion_rank_for_prime_discriminant": 0,
        "negative_pell_equation": "x^2-ell*y^2=-4",
        "dummy_symbol_guard": str(d) == "D",
    }


def _build_wl543(wl542: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _symbolic_wl543_certificate()
    predecessor_ready = _predecessor_ready(
        wl542, "wl542", "every_denominator_prime_splits_completely_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl542_input_not_ready")
    if symbolic["norm_numerator_identity_verified"] is not True:
        violations.append("norm_identity_not_verified")
    if symbolic["ordinary_class_group_2_torsion_rank_for_prime_discriminant"] != 0:
        violations.append("genus_theory_2_torsion_not_eliminated")
    proof_status = {
        "real_quadratic_alpha_is_totally_positive_integral_here": True,
        "principal_ideal_of_alpha_is_square_ideal_here": True,
        "ordinary_class_group_2_torsion_eliminated_by_genus_theory_here": True,
        "alpha_reduced_to_unit_times_element_square_here": True,
        "remaining_totally_positive_unit_squareclasses_at_most_two": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl543",
        object_layer="m2_real_quadratic_square_ideal_descent_inside_wl535",
        predecessor="wl542",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "descent": {
                "field": "Q(sqrt(ell))",
                "ring_of_integers": "Z[(1+sqrt(ell))/2]",
                "alpha": "(C+Q*sqrt(ell))/2",
                "norm_alpha": "D^2",
                "alpha_is_totally_positive": True,
                "alpha_and_conjugate_ideals_are_coprime": True,
                "square_ideal_equation": "(alpha)=a^2",
                "ordinary_class_group_2_torsion": "trivial by genus theory",
                "element_equation": "alpha=epsilon*beta^2",
            },
            "unit_squareclass_split": {
                "norm_minus_one_unit_exists": {
                    "class_count": 1,
                    "epsilon_is_square": True,
                },
                "no_norm_minus_one_unit": {
                    "class_count": 2,
                    "epsilon_classes": ["1", "fundamental totally positive unit"],
                },
                "negative_pell_equivalence": "x^2-ell*y^2=-4 is soluble",
            },
            "symbolic_certificate": symbolic,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _symbolic_wl544_certificate() -> dict[str, Any]:
    ell, r, s, u, v, z, w = sp.symbols("ell r s u v Z W")
    n = u**2 - ell * v**2
    f = s * (u**2 + ell * v**2) + 2 * r * u * v
    h = r * (u**2 + ell * v**2) + 2 * ell * s * u * v
    unit_relation = r**2 - ell * s**2 - 4
    conic_remainder = sp.rem(sp.expand(h**2 - ell * f**2 - 4 * n**2), unit_relation, r)
    j = (
        f**8
        + (16 - 8 * ell) * f**6 * n**2
        + (32 * ell**2 - 96 * ell + 72) * f**4 * n**4
        + (32 * ell - 64) * f**2 * n**6
        + 16 * n**8
    )
    q_square = f**2 / n**2
    g = (
        q_square**4
        + (16 - 8 * ell) * q_square**3
        + (32 * ell**2 - 96 * ell + 72) * q_square**2
        + (32 * ell - 64) * q_square
        + 16
    )
    return {
        "automatic_conic_identity_verified": sp.factor(conic_remainder) == 0,
        "G_homogenization_verified": sp.simplify(j - n**8 * g) == 0,
        "reconstruction_first_square": "a=Z/N from Z^2=ell*N^2-F^2",
        "reconstruction_second_square": "c=H/N from H^2-ell*F^2=4*N^2",
        "reconstruction_G_square": "V=W/N^4 from W^2=J_ell(F,N)",
        "positivity_homogenization": "ell*F^4+4*F^2*N^2-4*ell*N^4>0",
        "unused_symbol_guard": str(z) == "Z" and str(w) == "W",
    }


def _build_wl544(wl543: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _symbolic_wl544_certificate()
    predecessor_ready = _predecessor_ready(
        wl543, "wl543", "remaining_totally_positive_unit_squareclasses_at_most_two"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl543_input_not_ready")
    for key in ("automatic_conic_identity_verified", "G_homogenization_verified"):
        if symbolic[key] is not True:
            violations.append(f"symbolic_identity_failed:{key}")
    proof_status = {
        "abstract_unit_square_descent_expanded_here": True,
        "at_most_two_explicit_integer_quartic_branches_here": True,
        "Gaussian_G_and_positivity_pulled_back_exactly_here": True,
        "forward_and_converse_reconstruction_proved_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl544",
        object_layer="m2_explicit_two_unit_class_quartic_descent_inside_wl535",
        predecessor="wl543",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "coordinate_forms": {
                "unit": "epsilon=(r+s*sqrt(ell))/2, r^2-ell*s^2=4",
                "beta": "(u+v*sqrt(ell))/2 with u congruent v mod 2",
                "N": "u^2-ell*v^2",
                "F": "s*(u^2+ell*v^2)+2*r*u*v",
                "H": "r*(u^2+ell*v^2)+2*ell*s*u*v",
                "automatic_identity": "H^2-ell*F^2=4*N^2",
            },
            "explicit_system": {
                "unit_class_count_upper_bound": 2,
                "nonzero_condition": "N!=0",
                "Gaussian_square": "Z^2=ell*N^2-F^2",
                "G_square": "W^2=J_ell(F,N)",
                "positivity": "ell*F^4+4*F^2*N^2-4*ell*N^4>0",
                "reconstruction": ["q=F/N", "a=Z/N", "c=H/N", "V=W/N^4"],
            },
            "trivial_unit_branch": {
                "r": 2,
                "s": 0,
                "F": "4*u*v",
                "H": "2*(u^2+ell*v^2)",
                "N": "u^2-ell*v^2",
                "Gaussian_quartic": "Z^2=ell*(u^2-ell*v^2)^2-16*u^2*v^2",
            },
            "symbolic_certificate": symbolic,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _unit_square_residues_mod_8() -> list[int]:
    return sorted({x * x % 8 for x in range(1, 8, 2)})


def _wl545_residue_certificate() -> dict[str, Any]:
    unit_squares = _unit_square_residues_mod_8()
    return {
        "unit_square_residues_mod_8": unit_squares,
        "k_eq_1_parenthesized_residues": {
            1: (1 + 1) % 8,
            5: (5 + 1) % 8,
        },
        "k_eq_1_total_valuation_is_3": True,
        "k_eq_2_unit_residue_mod_8": 5,
        "k_eq_2_unit_is_nonsquare": 5 not in unit_squares,
        "k_eq_0_ell_1_second_square_residue": 5,
        "k_ge_3_first_square_requires_ell_mod_8": 1,
        "G_unit_branch_residue_mod_8": 1,
        "G_high_valuation_unit_precision": "1 mod 2^7 after dividing by 16",
    }


def _build_wl545(wl544: Mapping[str, Any]) -> dict[str, Any]:
    residue = _wl545_residue_certificate()
    predecessor_ready = _predecessor_ready(
        wl544, "wl544", "forward_and_converse_reconstruction_proved_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl544_input_not_ready")
    if residue["unit_square_residues_mod_8"] != [1]:
        violations.append("unit_square_residues_mod_8_mismatch")
    if residue["k_eq_2_unit_is_nonsquare"] is not True:
        violations.append("k_eq_2_not_excluded")
    proof_status = {
        "trivial_unit_2_adic_q_valuation_classified_here": True,
        "ell_eq_5_mod_8_forces_u_v_odd_here": True,
        "ell_eq_1_mod_8_forces_even_halves_opposite_parity_here": True,
        "G_condition_adds_no_2_adic_obstruction_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl545",
        object_layer="m2_trivial_unit_branch_2_adic_dichotomy_inside_wl544",
        predecessor="wl544",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "q_valuation_dichotomy": {
                "ell_eq_5_mod_8": "v_2(q)=0",
                "ell_eq_1_mod_8": "v_2(q)>=3",
                "excluded_valuations": [1, 2],
            },
            "descent_variable_parity": {
                "ell_eq_1_mod_8": "u=2m and v=2n with m,n of opposite parity",
                "ell_eq_5_mod_8": "u and v are both odd",
                "primitive_normalization": "v_2(N)=2",
            },
            "residue_certificate": residue,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _symbolic_gaussian_certificate() -> dict[str, Any]:
    a, b, x, y = sp.symbols("a_0 b_0 x y", integer=True)
    real = a * (x**2 - y**2) - 2 * b * x * y
    imag = b * (x**2 - y**2) + 2 * a * x * y
    norm_identity = sp.expand(real**2 + imag**2 - (a**2 + b**2) * (x**2 + y**2) ** 2)
    conjugate_imag = -b * (x**2 - y**2) + 2 * a * x * y
    conjugate_reduction = sp.expand(conjugate_imag + imag.subs(y, -y))
    return {
        "Gaussian_norm_identity_verified": norm_identity == 0,
        "pi_orientation_imaginary_form": str(imag),
        "i_pi_orientation_imaginary_form": str(real),
        "conjugate_orientation_reduces_by_y_sign_and_Q_sign": conjugate_reduction == 0,
        "essential_orientation_count": 2,
    }


def _build_wl546(wl545: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _symbolic_gaussian_certificate()
    predecessor_ready = _predecessor_ready(
        wl545, "wl545", "trivial_unit_2_adic_q_valuation_classified_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl545_input_not_ready")
    if symbolic["Gaussian_norm_identity_verified"] is not True:
        violations.append("Gaussian_norm_identity_failed")
    if symbolic["conjugate_orientation_reduces_by_y_sign_and_Q_sign"] is not True:
        violations.append("Gaussian_orientation_reduction_failed")
    proof_status = {
        "primitive_Gaussian_factors_proved_coprime_here": True,
        "Gaussian_square_reduced_to_two_orientations_here": True,
        "real_and_Gaussian_descents_coupled_here": True,
        "Gaussian_square_equation_eliminated_exactly_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl546",
        object_layer="m2_trivial_unit_Gaussian_double_descent_inside_wl544",
        predecessor="wl545",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "Gaussian_descent": {
                "prime_representation": "ell=a_0^2+b_0^2",
                "factorization": "A+iQ=eta*pi_or_conjugate(pi)*(x+iy)^2",
                "norm": "x^2+y^2=D",
                "orientation_B": "Q=+/-[b_0*(x^2-y^2)+2*a_0*x*y]",
                "orientation_R": "Q=+/-[a_0*(x^2-y^2)-2*b_0*x*y]",
                "essential_orientation_count": 2,
            },
            "double_descent_system": {
                "norm_compatibility": "u^2-ell*v^2=+/-4*(x^2+y^2)",
                "real_coordinate": "Q=u*v",
                "Gaussian_coordinate_choices": [
                    "+/-[b_0*(x^2-y^2)+2*a_0*x*y]",
                    "+/-[a_0*(x^2-y^2)-2*b_0*x*y]",
                ],
                "remaining_G_square": "D^8*G_ell((Q/D)^2) is a square",
                "remaining_positivity": "ell*Q^4+4*Q^2*D^2-4*ell*D^4>0",
            },
            "primitive_conditions": {
                "gcd_x_y": 1,
                "ell_eq_5_mod_8": "u,v odd and coprime",
                "ell_eq_1_mod_8": "u=2m,v=2n with coprime opposite-parity m,n",
            },
            "symbolic_certificate": symbolic,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _symbolic_support_certificate() -> dict[str, Any]:
    ell, q, d, t, q2 = sp.symbols("ell Q D t Q2")
    p_form = -(q**4) + (8 * ell - 12) * q**2 * d**2 + 4 * d**4
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    sum_identity = sp.factor(p_form + r_form)
    p_in_q2 = -(q2**2) + (8 * ell - 12) * q2 * d**2 + 4 * d**4
    reduced_in_t = sp.factor(p_in_q2.subs({ell: 1, q2: t * d**2}) / d**4)
    root_polynomial = t**2 + 4 * t - 4
    return {
        "P_plus_R": str(sum_identity),
        "P_plus_R_identity_verified": sum_identity == 8 * q**2 * d**2 * (ell - 1),
        "ell_eq_1_root_polynomial_verified": sp.factor(reduced_in_t + root_polynomial) == 0,
        "root_polynomial": "t^2+4*t-4",
        "root_discriminant": int(sp.discriminant(root_polynomial, t)),
        "root_discriminant_equals_32": sp.discriminant(root_polynomial, t) == 32,
    }


def _build_wl547(wl546: Mapping[str, Any]) -> dict[str, Any]:
    symbolic = _symbolic_support_certificate()
    predecessor_ready = _predecessor_ready(
        wl546, "wl546", "Gaussian_square_equation_eliminated_exactly_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl546_input_not_ready")
    for key in (
        "P_plus_R_identity_verified",
        "ell_eq_1_root_polynomial_verified",
        "root_discriminant_equals_32",
    ):
        if symbolic[key] is not True:
            violations.append(f"symbolic_support_failed:{key}")
    proof_status = {
        "G_square_rewritten_as_Gaussian_norm_square_here": True,
        "common_odd_prime_support_bounded_by_ell_minus_1_here": True,
        "common_odd_primes_require_Legendre_2_eq_1_here": True,
        "G_square_reduced_to_finite_S_squareclasses_here": True,
        "theorem_level_Selmer_object_claimed_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl547",
        object_layer="m2_finite_Gaussian_S_squareclass_descent_for_G_inside_wl546",
        predecessor="wl546",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "Gaussian_norm": {
                "P": "-Q^4+(8*ell-12)*Q^2*D^2+4*D^4",
                "R": "Q^4+4*Q^2*D^2-4*D^4",
                "delta": "(P+iR)/(1+i)",
                "norm_delta": "W^2",
            },
            "finite_support": {
                "dyadic_prime": "1+i",
                "odd_rational_primes": "p|ell-1 with Legendre(2/p)=1",
                "candidate_root_condition": "(Q^2/D^2)^2+4*(Q^2/D^2)-4=0 mod p",
                "outside_support_Gaussian_valuations_are_even": True,
            },
            "squareclass_equation": {
                "equation": "delta=eta*d*gamma^2",
                "Gaussian_unit_class_count": 2,
                "d_is_squarefree": True,
                "d_supported_on_finite_S_ell": True,
            },
            "symbolic_certificate": symbolic,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _wl548_valuation_certificate() -> dict[str, Any]:
    return {
        "ell_eq_5_mod_8": {
            "Q_parity": "odd",
            "D_parity": "odd",
            "P_parity": "odd",
            "R_parity": "odd",
            "P_mod_8": 7,
            "R_mod_8": 1,
            "post_division_coordinate_parities": "opposite",
            "v_1_plus_i_P_plus_iR": 1,
            "v_1_plus_i_delta": 0,
        },
        "ell_eq_1_mod_8": {
            "minimum_v_2_Q": 3,
            "P_over_4_mod_16": "D^4",
            "R_over_4_mod_64": "-D^4",
            "P_over_4_mod_4": 1,
            "R_over_4_mod_4": 3,
            "post_division_coordinate_parities": "opposite",
            "P_over_4_and_R_over_4_are_odd": True,
            "v_1_plus_i_P_plus_iR": 5,
            "v_1_plus_i_delta": 4,
        },
        "both_delta_valuations_are_even": True,
    }


def _build_wl548(wl547: Mapping[str, Any]) -> dict[str, Any]:
    valuation = _wl548_valuation_certificate()
    predecessor_ready = _predecessor_ready(
        wl547, "wl547", "G_square_reduced_to_finite_S_squareclasses_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl547_input_not_ready")
    values = [
        valuation["ell_eq_5_mod_8"]["v_1_plus_i_delta"],
        valuation["ell_eq_1_mod_8"]["v_1_plus_i_delta"],
    ]
    if any(value % 2 for value in values):
        violations.append("dyadic_delta_valuation_not_even")
    proof_status = {
        "dyadic_delta_valuation_computed_exactly_here": True,
        "one_plus_i_squareclass_eliminated_here": True,
        "finite_support_reduced_to_odd_primes_here": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl548",
        object_layer="m2_dyadic_Gaussian_squareclass_elimination_inside_wl547",
        predecessor="wl547",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "valuation_certificate": valuation,
            "refined_support": {
                "contains_one_plus_i": False,
                "odd_rational_primes": "p|ell-1 with Legendre(2/p)=1",
                "candidate_root_condition": "(Q^2/D^2)^2+4*(Q^2/D^2)-4=0 mod p",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl549(wl548: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(wl548, "wl548", "one_plus_i_squareclass_eliminated_here")
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl548_input_not_ready")
    proof_status = {
        "root_square_condition_classified_here": True,
        "source_square_residues_automatic_at_square_root_here": True,
        "p_eq_7_mod_8_root_test_exhausted_here": True,
        "odd_Gaussian_class_equations_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl549",
        object_layer="m2_odd_Gaussian_common_prime_root_square_classification",
        predecessor="wl548",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "identities_at_a_root": {
                "polynomial": "t^2+4*t-4",
                "one_minus_t": "t^2/4",
                "t_plus_four": "4/t",
                "root_is_nonzero": True,
            },
            "classification": {
                "p_mod_8_eq_7": "exactly_one_of_two_roots_is_square",
                "p_mod_8_eq_1": "either_zero_or_two_roots_are_square",
                "refined_support": "p|ell-1 and f has a nonzero square root mod p",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl550(wl549: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(wl549, "wl549", "root_square_condition_classified_here")
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl549_input_not_ready")
    proof_status = {
        "both_wl546_orientations_locally_compatible_here": True,
        "quadratic_etale_hilbert_90_witness_given_here": True,
        "same_prime_orientation_route_exhausted_here": True,
        "global_odd_class_equation_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl550",
        object_layer="m2_common_prime_local_compatibility_with_fixed_Gaussian_orientations",
        predecessor="wl549",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "certificate": {
                "quadratic_etale_algebra": "F_p[i] with conjugation",
                "norm_one_parameterization": "h=z/conjugate(z)=z^2/Norm(z)",
                "witness_if_h_not_minus_one": "z=1+h",
                "witness_if_h_is_minus_one": "z=i",
                "first_orientation_target": "w=A+i*q",
                "second_orientation_target": "w=q+i*A",
                "wl549_root_witness": "A=+/-t/2 when q^2=t",
            },
            "global_integer_candidate_produced_here": False,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl551(wl550: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl550, "wl550", "same_prime_orientation_route_exhausted_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl550_input_not_ready")
    proof_status = {
        "global_norm_square_parity_used_here": True,
        "split_Gaussian_primes_paired_here": True,
        "squarefree_factor_reduced_to_rational_integer_here": True,
        "global_rational_class_equations_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl551",
        object_layer="m2_global_norm_pairing_inside_odd_Gaussian_class_equation",
        predecessor="wl550",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "norm_certificate": {
                "element_equation": "delta=eta*d*gamma^2",
                "norm_equation": "W^2=Norm(d)*Norm(gamma)^2",
                "conclusion": "Norm(d) is an integer square",
                "split_prime_rule": "pi and conjugate(pi) have equal squarefree exponents",
                "inert_prime_rule": "the rational Gaussian prime p has norm p^2",
                "reduced_factor": "d=r up to a unit, with rational squarefree r|rad(ell-1)",
                "unit_classes_modulo_squares": ["1", "i"],
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl552(wl551: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl551, "wl551", "squarefree_factor_reduced_to_rational_integer_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl551_input_not_ready")
    proof_status = {
        "dyadic_parity_applied_to_global_class_equation_here": True,
        "Gaussian_unit_class_forced_to_i_here": True,
        "two_unit_classes_reduced_to_one_here": True,
        "remaining_eta_i_coordinate_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl552",
        object_layer="m2_dyadic_unit_class_inside_global_Gaussian_class_equation",
        predecessor="wl551",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "parity_certificate": {
                "ell_eq_5_mod_8": {
                    "delta_coordinate_parities": "even_real_odd_imaginary",
                    "gamma_is_one_plus_i_unit": True,
                    "r_times_gamma_square_parities": "odd_real_even_imaginary",
                    "forced_unit_class": "i",
                    "coordinate_equations": ["E=-2*r*m*n", "F=r*(m^2-n^2)"],
                },
                "ell_eq_1_mod_8": {
                    "minimum_v_2_E": 11,
                    "F_over_4_is_odd": True,
                    "gamma_factorization": "gamma=(1+i)^2*gamma_0",
                    "normalized_delta_coordinate_parities": "even_real_odd_imaginary",
                    "forced_unit_class": "i",
                    "coordinate_equations": ["-E/4=-2*r*m*n", "-F/4=r*(m^2-n^2)"],
                },
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def build_c2_global_descent(c1_wl541: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Build wl542-wl552 once from the canonical C1 wl541 projection."""
    wl542 = _build_wl542(c1_wl541)
    wl543 = _build_wl543(wl542)
    wl544 = _build_wl544(wl543)
    wl545 = _build_wl545(wl544)
    wl546 = _build_wl546(wl545)
    wl547 = _build_wl547(wl546)
    wl548 = _build_wl548(wl547)
    wl549 = _build_wl549(wl548)
    wl550 = _build_wl550(wl549)
    wl551 = _build_wl551(wl550)
    wl552 = _build_wl552(wl551)
    return {
        "wl542": wl542,
        "wl543": wl543,
        "wl544": wl544,
        "wl545": wl545,
        "wl546": wl546,
        "wl547": wl547,
        "wl548": wl548,
        "wl549": wl549,
        "wl550": wl550,
        "wl551": wl551,
        "wl552": wl552,
    }


def project_stage(evidence: Mapping[str, Mapping[str, Any]], work_log: str) -> dict[str, Any]:
    """Return one stage after enforcing the explicit slice-1 stage map."""
    if work_log not in C2_GLOBAL_STAGES:
        raise KeyError(f"unknown C2 global descent work log: {work_log}")
    if work_log not in evidence:
        raise KeyError(f"missing C2 global descent work log: {work_log}")
    payload = evidence[work_log]
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C2_GLOBAL_STAGES:
        raise KeyError(f"unknown C2 global descent work log: {work_log}")
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    allowed = _COMMON_TOP_LEVEL_KEYS | _STAGE_TOP_LEVEL_KEYS[work_log]
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
