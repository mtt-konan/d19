#!/usr/bin/env python3
"""Canonical C2 slice for the wl553-wl562 character system."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from typing import Any

import sympy as sp

C2_CHARACTER_STAGES = tuple(f"wl{number}" for number in range(553, 563))

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
    "wl553": {
        "positivity_certificate",
        "full_coordinate_solution_produced_here",
        "rational_wl535_point_produced_here",
    },
    "wl554": {"gcd_certificate", "rational_wl535_point_produced_here"},
    "wl555": {"standard_equation", "rational_wl535_point_produced_here"},
    "wl556": {"orientation_certificate", "rational_wl535_point_produced_here"},
    "wl557": {"valuation_certificate", "rational_wl535_point_produced_here"},
    "wl558": {"character_certificate", "rational_wl535_point_produced_here"},
    "wl559": {"leading_character_certificate", "rational_wl535_point_produced_here"},
    "wl560": {"normalized_character_certificate", "rational_wl535_point_produced_here"},
    "wl561": {
        "matrix_certificate",
        "theorem_level_selmer_matrix_claimed",
        "rational_wl535_point_produced_here",
    },
    "wl562": {"witness_certificate", "rational_wl535_point_produced_here"},
}

_COMMON_PROOF_KEYS = {
    "uniform_full_wl535_obstruction_proved_here",
    "advance_to_m3",
}

_STAGE_PROOF_KEYS: dict[str, set[str]] = {
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
}


def _wl552_ready(payload: Mapping[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl552"
        and proof.get("Gaussian_unit_class_forced_to_i_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("complete_selmer_upper_bound_proved") is False
        and payload.get("rank_zero_claimed") is False
        and payload.get("sha2_trivial_claimed") is False
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
        and payload.get("complete_selmer_upper_bound_proved") is False
        and payload.get("rank_zero_claimed") is False
        and payload.get("sha2_trivial_claimed") is False
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


def _valuation(value: int, prime: int) -> int:
    if value == 0:
        return 100
    result = 0
    while value % prime == 0:
        result += 1
        value //= prime
    return result


def _v2(value: int) -> int:
    return _valuation(value, 2)


def _is_square(value: int, prime: int) -> bool:
    return value % prime == 0 or pow(value % prime, (prime - 1) // 2, prime) == 1


def _is_nonzero_square(value: int, prime: int) -> bool:
    return value % prime != 0 and pow(value % prime, (prime - 1) // 2, prime) == 1


def _legendre(value: int, prime: int) -> int:
    residue = pow(value % prime, (prime - 1) // 2, prime)
    return -1 if residue == prime - 1 else residue


def _positivity_checks() -> bool:
    ell, q, d, r, m, n = sp.symbols("ell q d r m n")
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    e = 4 * (ell - 1) * q**2 * d**2
    f = r_form - e
    h = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    cone = ell * (m**2 - n**2) - 2 * (ell - 1) * m * n
    branch_5 = (ell - 1) * (-2 * r * m * n) + ell * r * (m**2 - n**2)
    branch_1 = (ell - 1) * (8 * r * m * n) - 4 * ell * r * (m**2 - n**2)
    identities = (
        sp.expand(h - ((ell - 1) * e + ell * f)) == 0,
        sp.expand(branch_5 - r * cone) == 0,
        sp.expand(branch_1 + 4 * r * cone) == 0,
    )
    witness_5 = all(
        ell_value * (25 - 64) - 2 * (ell_value - 1) * 5 * (-8) == 41 * ell_value - 80
        and 41 * ell_value - 80 > 0
        for ell_value in range(5, 300, 8)
    )
    witness_1 = all(
        ell_value * (1 - (2**k) ** 2) - 2 * (ell_value - 1) * (2**k) < 0
        for ell_value in range(1, 300, 8)
        if ell_value >= 5
        for k in range(1, 12)
    )
    return all(identities) and witness_5 and witness_1


def _gcd_checks() -> bool:
    for m in range(-30, 31):
        for n in range(-30, 31):
            if m == n == 0:
                continue
            common = math.gcd(m * m - n * n, 2 * m * n)
            if any(_valuation(common, prime) % 2 for prime in (3, 5, 7, 11, 13, 17, 19)):
                return False
    for ell in (5, 13, 17, 29, 37, 41):
        for q in range(1, 15):
            for d in range(1, 15):
                if math.gcd(q, d) != 1:
                    continue
                e = 4 * (ell - 1) * q * q * d * d
                r_value = q**4 + 4 * q * q * d * d - 4 * d**4
                f = r_value - e
                common = math.gcd(e, f)
                for prime in (3, 5, 7, 11, 13, 17, 19):
                    if _valuation(common, prime) != min(
                        _valuation(ell - 1, prime), _valuation(r_value, prime)
                    ):
                        return False
    return True


def _standard_equation_checks() -> bool:
    ell, q, d, r, a, b = sp.symbols("ell q d r a b")
    e = 4 * (ell - 1) * q**2 * d**2
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    f = r_form - e
    h = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    cone = ell * (a**2 - b**2) + 2 * (ell - 1) * a * b
    coordinate_h = (ell - 1) * (2 * r * a * b) + ell * r * (a**2 - b**2)
    algebra = (
        sp.expand(f - (q**4 + (8 - 4 * ell) * q**2 * d**2 - 4 * d**4)) == 0,
        sp.expand(h - ((ell - 1) * e + ell * f)) == 0,
        sp.expand(coordinate_h - r * cone) == 0,
    )
    e_real, f_real, r_real, a_real, b_real = sp.symbols(
        "e_real f_real r_real a_real b_real", real=True
    )
    z = f_real + sp.I * e_real
    delta = e_real + sp.I * f_real
    gamma = a_real - sp.I * b_real
    substituted_delta = sp.I * r_real * gamma**2
    recovered_z = sp.conjugate(substituted_delta / sp.I)
    rotation = sp.simplify(delta - sp.I * sp.conjugate(z)) == 0
    cancellation = sp.expand_complex(recovered_z - r_real * (a_real + sp.I * b_real) ** 2) == 0
    return all(algebra) and rotation and cancellation


def _orientation_checks() -> bool:
    for a_0 in range(1, 16, 2):
        for b_0 in range(2, 16, 2):
            for x in range(-10, 11):
                for y in range(-10, 11):
                    if (x - y) % 2 == 0:
                        continue
                    b_pi = b_0 * (x * x - y * y) + 2 * a_0 * x * y
                    r_pi = a_0 * (x * x - y * y) - 2 * b_0 * x * y
                    if b_pi % 2 != 0 or r_pi % 2 != 1:
                        return False
    for a_0 in range(1, 100, 2):
        for b_0 in range(2, 100, 2):
            ell = a_0 * a_0 + b_0 * b_0
            if ell % 8 == 5 and b_0 % 4 != 2:
                return False
            if ell % 8 == 1 and b_0 % 4 != 0:
                return False
    return True


def _valuation_strata_checks() -> bool:
    for a_0 in range(1, 16, 2):
        for b_0 in range(4, 65, 4):
            c = _v2(b_0)
            for x in range(1, 32):
                for y in range(1, 32):
                    if (x - y) % 2 == 0:
                        continue
                    k = _v2(x * y)
                    b_pi = b_0 * (x * x - y * y) + 2 * a_0 * x * y
                    value = _v2(b_pi)
                    if c < k + 1 and value != c:
                        return False
                    if c > k + 1 and value != k + 1:
                        return False
                    if c == k + 1 and value < c + 1:
                        return False
    for c in range(2, 8):
        for k in range(1, 8):
            can_reach_three = min(c, k + 1) >= 3 or c == k + 1 == 2
            stated = (c == 2 and k == 1) or (c >= 3 and k >= 2)
            if can_reach_three != stated:
                return False
    return True


def _character_checks() -> bool:
    prime = 13
    t = 10
    if not all(_is_square(value, prime) for value in (t, 1 - t, t + 4)):
        return False
    f_t = (t * t + 4 * t - 4) % prime
    if f_t != 6 or _is_square(f_t, prime):
        return False
    for prime in (3, 7, 11, 19, 23, 31):
        if prime % 4 != 3:
            return False
        if any(pow(value, (prime * prime - 1) // 2, prime) != 1 for value in range(1, prime)):
            return False
    return True


def _leading_character_checks() -> bool:
    for prime, j in ((5, 2), (13, 5), (17, 4), (29, 12), (37, 6)):
        if j * j % prime != prime - 1:
            return False
        for f_value in range(prime):
            for e_value in range(prime):
                first = (f_value + j * e_value) % prime
                second = (f_value - j * e_value) % prime
                if first == 0 or second == 0:
                    continue
                norm = first * second % prime
                if _is_nonzero_square(norm, prime) and (
                    _is_nonzero_square(first, prime) != _is_nonzero_square(second, prime)
                ):
                    return False
    prime = 17
    j = 4
    r = 3
    e_d, r_d = 5, 0
    if (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime != (
        e_d * (-1 + j) * pow(r, -1, prime)
    ) % prime:
        return False
    e_d, r_d = 0, 7
    if (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime != (r_d * pow(r, -1, prime)) % prime:
        return False
    e_d, lambda_value = 6, 9
    r_d = lambda_value * e_d % prime
    return (r_d - e_d + j * e_d) * pow(r, -1, prime) % prime == (
        e_d * (lambda_value - 1 + j) * pow(r, -1, prime)
    ) % prime


def _normalization_checks() -> bool:
    for d in range(12):
        epsilon = d % 2
        gamma_exponent = (d - epsilon) // 2
        if d != epsilon + 2 * gamma_exponent or epsilon not in {0, 1}:
            return False
    for prime in (3, 5, 7, 13):
        for d in range(8):
            epsilon = d % 2
            r = prime**epsilon * 11
            gamma = prime ** ((d - epsilon) // 2) * 7
            z_scale = r * gamma * gamma
            if z_scale // prime**d != 11 * 7 * 7:
                return False
    return True


def _reciprocity_checks() -> bool:
    split_primes = [5, 13, 17, 29, 37]
    product = 1
    for index, p in enumerate(split_primes):
        for q in split_primes[index + 1 :]:
            if _legendre(q, p) != _legendre(p, q):
                return False
            product *= _legendre(q, p) * _legendre(p, q)
    if product != 1:
        return False
    split = [5, 13, 17]
    inert = [3, 7, 11]
    left_class_product = 1
    for p in split:
        for q in split + inert:
            if q != p:
                left_class_product *= _legendre(q, p)
    inert_cross_product = 1
    for p in split:
        for q in inert:
            inert_cross_product *= _legendre(q, p)
    return left_class_product == inert_cross_product


def _orientation_value(kind: str, x: int, y: int, prime: int) -> int:
    denominator = (x * x + y * y) % prime
    if denominator == 0:
        raise ValueError("orientation witness has zero norm")
    numerator = 2 * x * y if kind == "B" else x * x - y * y
    return numerator * pow(denominator, -1, prime) % prime


def _local_determinacy_checks() -> bool:
    prime = 13
    for t, expected_f, expected_square in ((0, 9, True), (10, 6, False)):
        if not all(_is_square(value, prime) for value in (t, 1 - t, t + 4)):
            return False
        f_t = (t * t + 4 * t - 4) % prime
        if f_t != expected_f or _is_square(f_t, prime) is not expected_square or f_t == 0:
            return False
    witnesses = {
        ("B", 0): (0, 1),
        ("B", 6): (1, 2),
        ("R", 0): (1, 1),
        ("R", 6): (1, 4),
    }
    return all(
        _orientation_value(kind, x, y, prime) == q for (kind, q), (x, y) in witnesses.items()
    )


def _build_wl553(wl552: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _wl552_ready(wl552)
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl552_input_not_ready")
    if not _positivity_checks():
        violations.append("positivity_certificate_failed")
    proof_status = {
        "positivity_transferred_to_class_coordinates_here": True,
        "rational_squareclass_cancels_from_sign_here": True,
        "positivity_alone_exhausted_on_both_mod8_branches_here": True,
        "simultaneous_orientation_class_cone_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl553",
        object_layer="m2_real_positivity_inside_unique_Gaussian_unit_class",
        predecessor="wl552",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "positivity_certificate": {
                "identity": "H=(ell-1)*E+ell*F",
                "cone": "C_ell(m,n)=ell*(m^2-n^2)-2*(ell-1)*m*n",
                "ell_eq_5_mod_8": {
                    "product_sign": "m*n<0",
                    "condition": "C_ell(m,n)>0",
                    "uniform_witness": "(m,n)=(5,-8)",
                    "witness_value": "41*ell-80",
                },
                "ell_eq_1_mod_8": {
                    "product_sign": "m*n>0",
                    "condition": "C_ell(m,n)<0",
                    "uniform_witness_family": "(m,n)=(1,2^k), k>=1",
                },
            },
            "full_coordinate_solution_produced_here": False,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl554(wl553: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl553, "wl553", "positivity_transferred_to_class_coordinates_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl553_input_not_ready")
    if not _gcd_checks():
        violations.append("gcd_certificate_failed")
    proof_status = {
        "odd_coordinate_gcd_parity_of_Gaussian_square_proved_here": True,
        "rational_class_made_candidate_canonical_here": True,
        "independent_r_divisor_choice_eliminated_here": True,
        "canonical_class_equation_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl554",
        object_layer="m2_canonical_rational_class_inside_unique_unit_class_equation",
        predecessor="wl553",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "gcd_certificate": {
                "Gaussian_square_coordinates": ["m^2-n^2", "2*m*n"],
                "odd_common_valuation_parity": "even",
                "candidate_coordinates": ["E=4*(ell-1)*Q^2*D^2", "F=R-E"],
                "canonical_class": "r=sqf_odd(gcd(E,F))=sqf_odd(gcd(ell-1,R))",
                "primewise_formula": "v_p(r)=min(v_p(ell-1),v_p(R)) mod 2",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl555(wl554: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl554, "wl554", "rational_class_made_candidate_canonical_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl554_input_not_ready")
    if not _standard_equation_checks():
        violations.append("standard_equation_certificate_failed")
    proof_status = {
        "standard_norm_element_identified_here": True,
        "Gaussian_unit_removed_uniformly_here": True,
        "branch_dependent_cone_signs_unified_here": True,
        "standard_orientation_square_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl555",
        object_layer="m2_unit_free_standard_norm_square_inside_trivial_real_unit_branch",
        predecessor="wl554",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "standard_equation": {
                "E": "4*(ell-1)*Q^2*D^2",
                "F": "Q^4+(8-4*ell)*Q^2*D^2-4*D^4",
                "Z": "F+i*E",
                "delta_relation": "delta=i*conjugate(Z)",
                "unit_free_square": "Z=r*(a+i*b)^2",
                "coordinate_equations": ["F=r*(a^2-b^2)", "E=2*r*a*b"],
                "uniform_positivity": "ell*(a^2-b^2)+2*(ell-1)*a*b>0",
                "canonical_r": "sqf_odd(gcd(ell-1,R))",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl556(wl555: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(wl555, "wl555", "Gaussian_unit_removed_uniformly_here")
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl555_input_not_ready")
    if not _orientation_checks():
        violations.append("orientation_certificate_failed")
    proof_status = {
        "wl546_orientations_coupled_to_dyadic_branches_here": True,
        "one_complete_orientation_eliminated_per_branch_here": True,
        "ell_eq_5_mod_8_R_orientation_selected_here": True,
        "ell_eq_1_mod_8_B_orientation_selected_here": True,
        "surviving_orientation_systems_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl556",
        object_layer="m2_dyadic_selection_inside_wl546_Gaussian_orientations",
        predecessor="wl555",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "orientation_certificate": {
                "convention": "a_0 odd and b_0 even",
                "B_pi_parity": "even",
                "R_pi_parity": "odd",
                "ell_eq_5_mod_8": {
                    "Q_parity": "odd",
                    "selected_orientation": "Q=+/-R_pi(x,y)",
                },
                "ell_eq_1_mod_8": {
                    "minimum_v_2_Q": 3,
                    "selected_orientation": "Q=+/-B_pi(x,y)",
                    "remaining_condition": "v_2(B_pi)>=3",
                },
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl557(wl556: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl556, "wl556", "one_complete_orientation_eliminated_per_branch_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl556_input_not_ready")
    if not _valuation_strata_checks():
        violations.append("valuation_certificate_failed")
    proof_status = {
        "surviving_orientations_stratified_2_adically_here": True,
        "real_and_Gaussian_descent_valuations_coupled_here": True,
        "ell_eq_5_mod_8_standalone_dyadic_route_exhausted_here": True,
        "ell_eq_1_mod_8_mixed_valuation_cases_eliminated_here": True,
        "surviving_valuation_strata_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl557",
        object_layer="m2_dyadic_strata_inside_surviving_Gaussian_orientation",
        predecessor="wl556",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "valuation_certificate": {
                "ell_eq_5_mod_8": {
                    "selected_orientation": "R_pi",
                    "valuation": 0,
                    "new_condition": "none",
                },
                "ell_eq_1_mod_8": {
                    "selected_orientation": "B_pi",
                    "c": "v_2(b_0)>=2",
                    "k": "v_2(x*y)>=1",
                    "formula": {
                        "c<k+1": "v_2(B_pi)=c",
                        "c>k+1": "v_2(B_pi)=k+1",
                        "c=k+1": "v_2(B_pi)>=c+1",
                    },
                    "minimum_three_condition": "(c=2 and k=1) or (c>=3 and k>=2)",
                    "real_descent_match": "v_2(B_pi)=2+v_2(mu*nu)",
                },
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl558(wl557: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl557, "wl557", "real_and_Gaussian_descent_valuations_coupled_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl557_input_not_ready")
    if not _character_checks():
        violations.append("character_certificate_failed")
    proof_status = {
        "global_class_equation_applied_at_odd_unit_places_here": True,
        "split_prime_character_condition_proved_here": True,
        "inert_prime_unit_condition_exhausted_here": True,
        "distinct_place_r_coupling_produced_here": True,
        "global_character_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl558",
        object_layer="m2_split_prime_character_inside_global_standard_square",
        predecessor="wl557",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "character_certificate": {
                "unit_place": "odd p|ell-1 with p not dividing R",
                "inert_p_mod_4_eq_3": "automatic in F_(p^2)",
                "split_p_mod_4_eq_1": "Legendre(F/r,p)=1",
                "generic_q_coordinate": "Legendre((t^2+4*t-4)/r,p)=1",
                "Q_or_D_boundary": "Legendre(r,p)=1",
                "nontrivial_example": {
                    "p": 13,
                    "t": 10,
                    "f_t": 6,
                    "source_residues_are_squares": True,
                    "f_t_is_nonsquare": True,
                },
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl559(wl558: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl558, "wl558", "split_prime_character_condition_proved_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl558_input_not_ready")
    if not _leading_character_checks():
        violations.append("leading_character_certificate_failed")
    proof_status = {
        "positive_even_common_valuation_normalized_here": True,
        "split_prime_leading_character_classified_here": True,
        "inert_even_common_valuation_exhausted_here": True,
        "all_odd_places_not_in_r_classified_here": True,
        "global_character_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl559",
        object_layer="m2_even_common_valuation_inside_split_prime_global_character_system",
        predecessor="wl558",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "leading_character_certificate": {
                "setup": "e=v_p(ell-1), k=v_p(R), d=min(e,k)>0 even",
                "normalized_element": "Z_d=(F+i*E)/p^d",
                "inert_case": "automatic from square norm in F_(p^2)",
                "split_master_condition": "Legendre((F_d+j*E_d)/r,p)=1",
                "e<k": "Legendre(L_e*(-1+j)/r,p)=1",
                "k<e": "Legendre((R/p^k)/r,p)=1",
                "e=k": "Legendre(L_e*(lambda-1+j)/r,p)=1",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl560(wl559: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl559, "wl559", "split_prime_leading_character_classified_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl559_input_not_ready")
    if not _normalization_checks():
        violations.append("normalization_certificate_failed")
    proof_status = {
        "odd_common_leading_character_supplied_here": True,
        "all_valuation_parities_unified_here": True,
        "every_odd_ell_minus_one_place_fully_classified_here": True,
        "assembled_global_character_system_solved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl560",
        object_layer="m2_unified_normalized_character_at_all_odd_ell_minus_one_places",
        predecessor="wl559",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "normalized_character_certificate": {
                "d": "min(v_p(ell-1),v_p(R))",
                "epsilon": "d mod 2",
                "canonical_membership": "p|r iff epsilon=1",
                "reduced_class": "r_p=r/p^epsilon",
                "normalized_equation": "(F_d+i*E_d)=r_p*Gamma_p^2",
                "inert_case": "automatic",
                "split_master_condition": "Legendre((F_d+j*E_d)/r_p,p)=1",
                "e<k": "Legendre(L_e*(-1+j)/r_p,p)=1",
                "k<e": "Legendre((R/p^k)/r_p,p)=1",
                "e=k": "Legendre(L_e*(lambda-1+j)/r_p,p)=1",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl561(wl560: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl560, "wl560", "every_odd_ell_minus_one_place_fully_classified_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl560_input_not_ready")
    if not _reciprocity_checks():
        violations.append("reciprocity_certificate_failed")
    proof_status = {
        "split_prime_characters_assembled_as_F2_system_here": True,
        "reciprocity_product_over_odd_common_split_primes_proved_here": True,
        "split_split_pairwise_characters_cancelled_here": True,
        "reciprocity_matrix_uniform_contradiction_proved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl561",
        object_layer="m2_global_F2_character_system_for_standard_Gaussian_square",
        predecessor="wl560",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "matrix_certificate": {
                "rows": "split p|ell-1",
                "columns": "all odd q|ell-1",
                "membership_vector": "epsilon_q=min(v_q(ell-1),v_q(R)) mod 2",
                "entry": "A_pq=(1-Legendre(q,p))/2",
                "row_equation": "n_p=sum_(q!=p) A_pq*epsilon_q mod 2",
                "reciprocity_product": (
                    "prod_(p in S_split) Legendre(C_p,p)="
                    "prod_(p in S_split,q in S_inert) Legendre(q,p)"
                ),
                "split_only_corollary": "if S_inert is empty, the product is +1",
            },
            "theorem_level_selmer_matrix_claimed": False,
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def _build_wl562(wl561: Mapping[str, Any]) -> dict[str, Any]:
    predecessor_ready = _predecessor_ready(
        wl561, "wl561", "split_prime_characters_assembled_as_F2_system_here"
    )
    violations: list[str] = []
    if not predecessor_ready:
        violations.append("wl561_input_not_ready")
    if not _local_determinacy_checks():
        violations.append("local_determinacy_witness_failed")
    proof_status = {
        "opposite_leading_bits_with_same_local_stratum_proved_here": True,
        "both_Gaussian_orientations_locally_compatible_here": True,
        "local_orientation_determinacy_refuted_here": True,
        "global_integer_compatibility_resolved_here": False,
        "uniform_full_wl535_obstruction_proved_here": False,
        "advance_to_m3": False,
    }
    payload = _base_payload(
        work_log="wl562",
        object_layer="m2_local_determinacy_of_global_character_matrix_rows",
        predecessor="wl561",
        predecessor_ready=predecessor_ready,
        proof_status=proof_status,
        violations=violations,
    )
    payload.update(
        {
            "witness_certificate": {
                "prime": 13,
                "local_ell": 1,
                "class_r": 1,
                "square_character_witness": {
                    "t": 0,
                    "f_t": 9,
                    "row_bit": 0,
                    "B_witness": [0, 1],
                    "R_witness": [1, 1],
                },
                "nonsquare_character_witness": {
                    "t": 10,
                    "q": 6,
                    "f_t": 6,
                    "row_bit": 1,
                    "B_witness": [1, 2],
                    "R_witness": [1, 4],
                },
                "same_valuation_stratum": "d=0 and epsilon=0",
            },
            "rational_wl535_point_produced_here": False,
        }
    )
    return payload


def build_c2_character_system(wl552: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Build wl553-wl562 once from the canonical wl552 projection."""
    wl553 = _build_wl553(wl552)
    wl554 = _build_wl554(wl553)
    wl555 = _build_wl555(wl554)
    wl556 = _build_wl556(wl555)
    wl557 = _build_wl557(wl556)
    wl558 = _build_wl558(wl557)
    wl559 = _build_wl559(wl558)
    wl560 = _build_wl560(wl559)
    wl561 = _build_wl561(wl560)
    wl562 = _build_wl562(wl561)
    return {
        "wl553": wl553,
        "wl554": wl554,
        "wl555": wl555,
        "wl556": wl556,
        "wl557": wl557,
        "wl558": wl558,
        "wl559": wl559,
        "wl560": wl560,
        "wl561": wl561,
        "wl562": wl562,
    }


def project_stage(evidence: Mapping[str, Mapping[str, Any]], work_log: str) -> dict[str, Any]:
    """Return one stage after enforcing the explicit slice-2 stage map."""
    if work_log not in C2_CHARACTER_STAGES:
        raise KeyError(f"unknown C2 character-system work log: {work_log}")
    if work_log not in evidence:
        raise KeyError(f"missing C2 character-system work log: {work_log}")
    payload = evidence[work_log]
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return dict(payload)


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Project a ready or failed stage onto its exact semantic allowlist."""
    if work_log not in C2_CHARACTER_STAGES:
        raise KeyError(f"unknown C2 character-system work log: {work_log}")
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
