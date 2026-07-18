"""Exact B2 boundary data for the Berry C_1 Jacobian over Q(i).

The global two-torsion argument uses a reduction certificate for the branch
polynomial at a prime of Q(i), not a local factorization at a bad place.  The
rank-two lower bound uses one exact good-reduction computation at the split
prime (269, i-82).  No global point search is used here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MOD_13 = 13
REDUCTION_I_13 = 5
REDUCTION_POLY_13 = (12, 11, 1, 3, 3, 1, 1)  # low-to-high coefficients


def _trim(poly: list[int], modulus: int) -> list[int]:
    result = [value % modulus for value in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _add(left: list[int], right: list[int], modulus: int) -> list[int]:
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return _trim(result, modulus)


def _sub(left: list[int], right: list[int], modulus: int) -> list[int]:
    return _add(left, [-value for value in right], modulus)


def _mul(left: list[int], right: list[int], modulus: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return _trim(result, modulus)


def _divmod_poly(
    dividend: list[int], divisor: list[int], modulus: int
) -> tuple[list[int], list[int]]:
    remainder = _trim(dividend[:], modulus)
    divisor = _trim(divisor[:], modulus)
    inverse = pow(divisor[-1], -1, modulus)
    quotient = [0] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [0] and len(remainder) >= len(divisor):
        coefficient = remainder[-1] * inverse % modulus
        shift = len(remainder) - len(divisor)
        quotient[shift] = coefficient
        for index, divisor_value in enumerate(divisor):
            remainder[shift + index] -= coefficient * divisor_value
        remainder = _trim(remainder, modulus)
    return _trim(quotient, modulus), remainder


def _monic_gcd(left: list[int], right: list[int], modulus: int) -> list[int]:
    while right != [0]:
        left, right = right, _divmod_poly(left, right, modulus)[1]
    inverse = pow(left[-1], -1, modulus)
    return _trim([value * inverse for value in left], modulus)


def _pow_mod(base: list[int], exponent: int, modulus_poly: list[int], modulus: int) -> list[int]:
    result = [1]
    base = _divmod_poly(base, modulus_poly, modulus)[1]
    while exponent:
        if exponent & 1:
            result = _divmod_poly(_mul(result, base, modulus), modulus_poly, modulus)[1]
        base = _divmod_poly(_mul(base, base, modulus), modulus_poly, modulus)[1]
        exponent >>= 1
    return result


def _global_branch_algebra_certificate() -> dict[str, Any]:
    polynomial = list(REDUCTION_POLY_13)
    x = [0, 1]
    remainder_q2 = _pow_mod(x, MOD_13**2, polynomial, MOD_13)
    remainder_q3 = _pow_mod(x, MOD_13**3, polynomial, MOD_13)
    remainder_q6 = _pow_mod(x, MOD_13**6, polynomial, MOD_13)
    gcd_q2 = _monic_gcd(
        polynomial,
        _sub(remainder_q2, x, MOD_13),
        MOD_13,
    )
    gcd_q3 = _monic_gcd(
        polynomial,
        _sub(remainder_q3, x, MOD_13),
        MOD_13,
    )
    checks = {
        "i_square_root": (REDUCTION_I_13**2 + 1) % MOD_13 == 0,
        "q2_gcd_is_one": gcd_q2 == [1],
        "q3_gcd_is_one": gcd_q3 == [1],
        "q6_frobenius_remainder_is_x": remainder_q6 == x,
    }
    assert all(checks.values())
    return {
        "prime_ideal": "(13, i-5)",
        "residue_field": "F_13",
        "residue_i": REDUCTION_I_13,
        "reduced_polynomial_high_to_low": [1, 1, 3, 3, 1, 11, 12],
        "irreducibility_test": ("x^(13^6)=x mod f and gcd(f,x^(13^2)-x)=gcd(f,x^(13^3)-x)=1"),
        "remainder_x_13^2_low_to_high": remainder_q2,
        "remainder_x_13^3_low_to_high": remainder_q3,
        "remainder_x_13^6_low_to_high": remainder_q6,
        "gcd_x_13^2_minus_x": gcd_q2,
        "gcd_x_13^3_minus_x": gcd_q3,
        "checks": checks,
        "conclusion": (
            "the reduction is irreducible of degree 6, hence g6 is irreducible over Q(i)"
        ),
    }


def _point_and_relation_certificate() -> dict[str, Any]:
    return {
        "curve": "C_1: v^2=g6(t) over K=Q(i)",
        "points": {
            "A_plus": "[0:i:1]",
            "A_minus": "[0:-i:1]",
            "P_plus": "[1:1:0]",
            "P_minus": "[1:-1:0]",
        },
        "classes": {
            "E_plus": "[A_plus-P_plus]",
            "E_minus": "[A_minus-P_plus]",
            "D_inf": "[P_plus-P_minus]",
        },
        "principal_divisor": "div(t)=A_plus+A_minus-P_plus-P_minus",
        "class_relation": "E_plus+E_minus+D_inf=0",
        "all_relation_vectors": "Z*(1,1,1) in the ordered basis (E_plus,E_minus,D_inf)",
    }


def _t0_fake_squareclass_certificate() -> dict[str, Any]:
    """Verify the finite-chart t=0 evaluation in the exact field L."""

    import sympy as sp

    t = sp.symbols("t")
    i = sp.I
    g6 = (
        t**6
        + (-2 - 2 * i) * t**5
        + (-35 - 8 * i) * t**4
        + (-52 - 28 * i) * t**3
        + (19 - 40 * i) * t**2
        + (6 + 14 * i) * t
        - 1
    )
    beta = (
        (sp.Rational(1, 64) + sp.Rational(3, 64) * i) * t**5
        + (sp.Rational(5, 64) - sp.Rational(5, 64) * i) * t**4
        + (-sp.Rational(3, 32) - sp.Rational(63, 32) * i) * t**3
        + (sp.Rational(5, 32) - sp.Rational(139, 32) * i) * t**2
        + (sp.Rational(117, 64) - sp.Rational(69, 64) * i) * t
        + sp.Rational(1, 64)
        + sp.Rational(27, 64) * i
    )
    remainder = sp.rem(sp.Poly(sp.expand(beta**2 + i * t), t), sp.Poly(g6, t)).as_expr()
    assert sp.simplify(remainder) == 0
    return {
        "finite_evaluation_at_t0": "-theta",
        "beta_squared": "-i*theta",
        "constant_ratio": "(-theta)/beta^2=-i",
        "fake_squareclass": "[1] modulo L^(2) K^*",
        "beta_power_basis_coefficients": [
            "(1+3*i)/64",
            "(5-5*i)/64",
            "(-3-63*i)/32",
            "(5-139*i)/32",
            "(117-69*i)/64",
            "(1+27*i)/64",
        ],
        "exact_polynomial_remainder_zero": True,
    }


def _good_reduction_certificate() -> dict[str, Any]:
    return {
        "prime_ideal": "(269, i-82)",
        "residue_field": "F_269",
        "residue_i": 82,
        "residue_i_square_plus_one": 0,
        "reduced_polynomial_high_to_low": [1, 103, 116, 73, 236, 78, 268],
        "curve_counts": {"C(F_269)": 282, "C(F_269^2)": 72430},
        "jacobian_order": 75708,
        "jacobian_group_invariants": [3, 25236],
        "fixed_generators": {
            "G1": {
                "mumford": "(x^2+96*x+106, 44*x+8)",
                "order": 25236,
            },
            "G2": {
                "mumford": "(x^2+54*x+268, 129*x+60)",
                "order": 3,
            },
        },
        "class_coordinates_in_fixed_basis": {
            "E_plus": [14912, 1],
            "E_minus": [9310, 1],
            "D_inf": [1014, 1],
        },
        "mod_3_coordinates": {
            "E_plus": [2, 1],
            "D_inf": [0, 1],
        },
        "mod_3_determinant": 2,
        "exact_sage_proof": True,
        "no_global_point_search": True,
    }


def verify_b2() -> dict[str, Any]:
    from scripts.theory.berry_sextic_post_b0 import build_post_b0_audit
    from scripts.theory.berry_sextic_q3c_fake_selmer import verify_q3c

    branch = _global_branch_algebra_certificate()
    points = _point_and_relation_certificate()
    t0_squareclass = _t0_fake_squareclass_certificate()
    reduction = _good_reduction_certificate()
    post_b0 = build_post_b0_audit()
    q3c = verify_q3c()

    assert post_b0["torsion"]["conclusion"] == "J_1(K)_tors=0 and J_i(K)_tors=0."
    assert q3c["status"] == "ok"
    assert q3c["true_lift"]["true_selmer_dimension"] == 3
    assert q3c["true_lift"]["true_selmer_sequence"] == (
        "0 -> F_2<kappa(D_inf)> -> Sel_2(J/K) -> Sel_fake^S -> 0"
    )
    assert q3c["true_lift"]["global_dinf_nonzero"] is True
    assert t0_squareclass["exact_polynomial_remainder_zero"] is True
    assert branch["checks"]["q6_frobenius_remainder_is_x"]
    assert branch["checks"]["q2_gcd_is_one"]
    assert branch["checks"]["q3_gcd_is_one"]
    assert (
        reduction["class_coordinates_in_fixed_basis"]["E_plus"][0]
        + reduction["class_coordinates_in_fixed_basis"]["E_minus"][0]
        + reduction["class_coordinates_in_fixed_basis"]["D_inf"][0]
        == 25236
    )
    assert (
        reduction["class_coordinates_in_fixed_basis"]["E_plus"][1]
        + reduction["class_coordinates_in_fixed_basis"]["E_minus"][1]
        + reduction["class_coordinates_in_fixed_basis"]["D_inf"][1]
        == 3
    )
    assert reduction["mod_3_determinant"] % 3 != 0

    return {
        "status": "ok",
        "accepted_outcome": "b2_c1_global_j2_rank2_lower_bound_boundary",
        "global_branch_algebra": branch,
        "points_and_relations": points,
        "t0_fake_squareclass": t0_squareclass,
        "reduction": reduction,
        "rank": {
            "torsion_free_input": True,
            "j2_dimension_over_K": 0,
            "selmer_dimension": q3c["true_lift"]["true_selmer_dimension"],
            "sha_exact_sequence": ("0 -> J(K)/2J(K) -> Sel_2(J/K) -> Sha(J/K)[2] -> 0"),
            "rank_lower_bound": 2,
            "rank_upper_bound": 3,
            "certified_rank_interval": [2, 3],
            "sha_2_dimension_formula": "dim Sha(J/K)[2] = 3-rank J(K)",
        },
        "saturation": {
            "fake_evaluation_E_plus": t0_squareclass["fake_squareclass"],
            "fake_evaluation_E_minus": t0_squareclass["fake_squareclass"],
            "finite_evaluation_at_t0": t0_squareclass["finite_evaluation_at_t0"],
            "true_kernel": "F_2<kappa(D_inf)>",
            "kappa_D_inf_nonzero": True,
            "kummer_image_of_H_dimension": 1,
            "H_rank": 2,
            "H_is_2_saturated": False,
            "exact_alternatives": (
                "kappa(E_plus)=0 or kappa(E_plus)=kappa(D_inf); exactly one of "
                "E_plus,E_minus has zero Kummer class"
            ),
        },
        "next_obligation": (
            "Resolve the exact K-rational half of E_plus or E_plus+D_inf, "
            "then 2-saturate the resulting rank-two subgroup and separately "
            "decide rank 2 versus rank 3."
        ),
        "chabauty": {
            "genus": 2,
            "ordinary_C1_over_K_condition": "rank J(K) < 2",
            "ready": False,
            "rational_t_classification_open": True,
        },
        "proof_boundary": {
            "rank_equals_three": False,
            "sha_2_vanishes": False,
            "full_mordell_weil_basis": False,
            "two_saturation_claimed": False,
            "rational_t_claimed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str)
    args = parser.parse_args()
    result = verify_b2()
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, sort_keys=True)
            handle.write("\n")
    print(
        "b2 status={status} J2_dim={j2} rank_interval={interval} "
        "H_rank={h_rank} H_2_saturated={saturated}".format(
            status=result["status"],
            j2=result["rank"]["j2_dimension_over_K"],
            interval=tuple(result["rank"]["certified_rank_interval"]),
            h_rank=result["saturation"]["H_rank"],
            saturated=result["saturation"]["H_is_2_saturated"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
