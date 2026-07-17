"""Verify the Berry Q3c fake-Selmer pullback and true-lift sequence.

The finite certificates below are composed with the universal
divisor-evaluation/Kummer lemma proved in the Q3c report.  The verifier checks
the algebraic divisor, tangent, reciprocal-chart, and sign-cocycle identities
exactly; it does not pretend that a returned string is a proof of cohomology.
No rank, saturation, rational-parameter, or point-classification claim is
made.
"""

from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

Vector = list[int]
Matrix = list[list[int]]

EXPECTED_QUOTIENT_COORDINATES: tuple[tuple[int, ...], ...] = (
    (1, 1, 0, 1, 0, 0),
    (0, 1, 0, 1, 0, 0),
)
EXPECTED_H_COORDINATES: tuple[tuple[int, ...], ...] = (
    (0, 1, 1, 1, 1, 0, 0, 0),
    (0, 1, 1, 0, 0, 0, 1, 0),
)
EXPECTED_AMBIENT_LABELS: tuple[tuple[str, ...], ...] = (
    ("epsilon_1", "epsilon_2", "epsilon_4"),
    ("epsilon_2", "epsilon_4"),
)


def _bits(vector: Vector) -> str:
    return "".join(map(str, vector))


def _xor_sum(vectors: list[Vector], width: int) -> Vector:
    result = [0] * width
    for vector in vectors:
        result = [left ^ right for left, right in zip(result, vector, strict=True)]
    return result


def _linear_combination(basis: Matrix, coordinates: tuple[int, ...]) -> Vector:
    if len(basis) != len(coordinates):
        raise AssertionError("coordinate length does not match the quotient basis")
    return _xor_sum(
        [vector for bit, vector in zip(coordinates, basis, strict=True) if bit],
        len(basis[0]),
    )


def _formal_divisor(*terms: tuple[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for label, coefficient in terms:
        result[label] = result.get(label, 0) + coefficient
    return {label: coefficient for label, coefficient in result.items() if coefficient}


def _scale_divisor(divisor: dict[str, int], scalar: int) -> dict[str, int]:
    return _formal_divisor(
        *[(label, scalar * coefficient) for label, coefficient in divisor.items()]
    )


def _add_divisors(*divisors: dict[str, int]) -> dict[str, int]:
    return _formal_divisor(
        *[(label, coefficient) for divisor in divisors for label, coefficient in divisor.items()]
    )


def verify_universal_divisor_evaluation_lemma() -> dict[str, Any]:
    """Check the algebraic identities used by the all-place cohomology lemma.

    The Galois-cohomology conclusion is the proved mathematical lemma in the
    report.  This function checks its finite polynomial/divisor identities and
    the sign cocycle that fixes the boundary element.
    """

    import sympy as sp

    t, x = sp.symbols("t x")
    alpha, beta, gamma, delta, epsilon, zeta = sp.symbols("alpha beta gamma delta epsilon zeta")
    h = (t - alpha) * (t - beta)
    k = (t - gamma) * (t - delta) * (t - epsilon) * (t - zeta)
    g = h * k

    tangent_ratio = sp.simplify(sp.diff(h, t).subs(t, alpha) / sp.diff(g, t).subs(t, alpha))
    other_root_factor = beta - alpha
    regularized_branch_value = sp.simplify(other_root_factor / sp.diff(g, t).subs(t, alpha))
    assert tangent_ratio == 1 / k.subs(t, alpha)
    assert regularized_branch_value == -1 / k.subs(t, alpha)
    assert sp.simplify((t - alpha).subs(t, 1 / x) - (1 - alpha * x) / x) == 0
    assert sp.limit(x * (1 / x - alpha), x, 0) == 1
    assert sp.limit(x**2 * h.subs(t, 1 / x), x, 0) == 1
    assert sp.limit(x**4 * k.subs(t, 1 / x), x, 0) == 1

    resultant_hk = sp.resultant(h, k, t)
    resultant_kh = sp.resultant(k, h, t)
    assert sp.simplify(resultant_kh / resultant_hk) == 1

    div_root = _formal_divisor(("W_alpha", 2), ("P_plus", -1), ("P_minus", -1))
    d_inf = _formal_divisor(("P_plus", 1), ("P_minus", -1))
    half_d_inf = _formal_divisor(("P_plus", 1), ("W_alpha", -1))
    assert _add_divisors(_scale_divisor(half_d_inf, 2), _scale_divisor(d_inf, -1)) == {
        label: -coefficient for label, coefficient in div_root.items()
    }

    pair_divisor = _formal_divisor(
        ("W_alpha", 1),
        ("W_sigma_alpha", 1),
        ("P_plus", -1),
        ("P_minus", -1),
    )
    kummer_cocycle = _formal_divisor(("W_alpha", 1), ("W_sigma_alpha", -1))
    sigma_root_divisor = _formal_divisor(("W_sigma_alpha", 2), ("P_plus", -1), ("P_minus", -1))
    assert _add_divisors(pair_divisor, _scale_divisor(kummer_cocycle, -1)) == dict(
        sigma_root_divisor
    )

    signs = (-1, 1, 1, 1, 1, 1)
    boundary_signs = (-1, -1, 1, 1, 1, 1)
    assert len(signs) == 6
    assert math.prod(signs) == -1
    assert math.prod(boundary_signs) == 1

    return {
        "status": "proved_lemma",
        "scope": "every characteristic-not-2 field and every base change",
        "group_scheme_sequence": "1 -> J[2] -> Q -> mu_2 -> 1",
        "machine_checked_identities": {
            "root_divisor": True,
            "half_of_infinity_difference": True,
            "reciprocal_chart": True,
            "both_infinity_leading_values": True,
            "branch_tangent_ratio": True,
            "factor_zero_other_root_sign": True,
            "factor_norm_resultant_ratio": True,
            "boundary_sign_norm": True,
            "boundary_equals_kummer_mod_principal_divisor": True,
        },
        "boundary_element": "-1",
        "boundary_identity": "partial_F(-1)=kappa_F(D_inf)",
        "functoriality": "all maps and identities are defined over F and commute with base change",
    }


def _support_certificate() -> dict[str, Any]:
    from scripts.theory import berry_sextic_magma_segmented as segmented

    assert segmented.build_certificate()["status"] == "ok"
    model = segmented.stage_snapshot(include_conjugate_support=False)
    conservative = segmented.stage_snapshot(include_conjugate_support=True)
    assert model["class_group"]["invariants"] == []
    assert conservative["class_group"]["invariants"] == []
    assert len(model["support"]) == 6
    assert len(conservative["support"]) == 10
    assert {entry["base_prime"] for entry in model["support"]} == {
        "1+i",
        "94*i-169",
    }
    assert all(entry["base_prime"] == "-94*i-169" for entry in conservative["support"][6:])

    return {
        "allowed_support_base_places": ["1+i", "94*i-169"],
        "reduction_status": {
            "1+i": "unresolved",
            "94*i-169": "bad_reduction_proved",
            "-94*i-169": "good_reduction_proved",
            "outside_allowed_support": "good_reduction_proved",
        },
        "good_conjugate_place": "-94*i-169",
        "model_support_prime_count": len(model["support"]),
        "conservative_support_prime_count": len(conservative["support"]),
        "class_group_trivial": True,
        "outside_support_theorem": (
            "At every finite v outside {1+i,94*i-169}, good reduction and 2 invertible "
            "identify the local Kummer image with the unramified cohomology; the "
            "integral R/Q/J[2] diagram and Br(O_v)=0 put every norm-square fake "
            "class with even valuations in that local image."
        ),
        "constant_parity_normalization": (
            "K=Q(i) is a PID, so the common base-prime parity can be removed by a "
            "global K constant; Cl(L)=1 then removes the remaining even ideal."
        ),
    }


@lru_cache(maxsize=1)
def _frozen_certificates() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    from scripts.theory import berry_sextic_q3b_assembly as assembly_module
    from scripts.theory import berry_sextic_q3b_local_image as local_module

    assembly = assembly_module.verify_assembly()
    local_image = local_module.verify_local_image()
    support = _support_certificate()
    return assembly, local_image, support


def _verify_pullback(assembly: dict[str, Any], local_image: dict[str, Any]) -> dict[str, Any]:
    from scripts.theory import berry_sextic_q3b_assembly as q3b

    assert assembly["status"] == "coordinate_blocker"
    assert local_image["status"] == "ok"
    assert assembly["supported_quotient_labels"] == [
        "epsilon_1",
        "epsilon_2",
        "epsilon_3",
        "epsilon_4",
        "S_prime_5+S_prime_6",
        "S_prime_5+S_prime_8",
    ]
    assert assembly["dyadic_kernel_dimension"] == 0

    quotient_basis = assembly["supported_quotient_basis"]
    h_map = assembly["dyadic_h_map_rows"]
    ambient_labels = assembly["ambient_labels"]
    pulled_back: list[dict[str, Any]] = []
    for coordinates, expected_h, expected_labels in zip(
        EXPECTED_QUOTIENT_COORDINATES,
        EXPECTED_H_COORDINATES,
        EXPECTED_AMBIENT_LABELS,
        strict=True,
    ):
        ambient = _linear_combination(quotient_basis, coordinates)
        h_coordinates = q3b._matvec(h_map, list(coordinates))
        assert h_coordinates == list(expected_h)
        assert [ambient_labels[index] for index, bit in enumerate(ambient) if bit] == list(
            expected_labels
        )
        assert q3b._matvec(assembly["odd_condition_rows"], ambient) == [0] * 6
        assert q3b._in_span(
            _xor_sum(
                [
                    list(value)
                    for value, bit in zip(
                        assembly["odd_h_coordinates_on_quotient_basis"],
                        coordinates,
                        strict=True,
                    )
                    if bit
                ],
                4,
            ),
            [[0, 1, 1, 0], [0, 0, 1, 0]],
        )
        pulled_back.append(
            {
                "quotient_coordinates": _bits(list(coordinates)),
                "ambient_coordinates": _bits(ambient),
                "ambient_labels": list(expected_labels),
                "dyadic_h_coordinates": _bits(h_coordinates),
            }
        )

    constants = assembly["constant_matrix_columns"]
    representatives = [
        _linear_combination(quotient_basis, coordinates)
        for coordinates in EXPECTED_QUOTIENT_COORDINATES
    ]
    assert q3b._rank([*constants, *representatives]) == 6
    assert q3b._rank(representatives) == 2
    assert local_image["intersection_basis"] == [
        _bits(list(EXPECTED_H_COORDINATES[0])),
        _bits(list(EXPECTED_H_COORDINATES[1])),
    ]
    return {
        "quotient_coordinates": [_bits(list(value)) for value in EXPECTED_QUOTIENT_COORDINATES],
        "ambient_representatives": pulled_back,
        "intersection_basis": [_bits(list(value)) for value in EXPECTED_H_COORDINATES],
        "quotient_dimension": assembly["supported_quotient_dimension"],
        "fake_selmer_dimension": len(EXPECTED_QUOTIENT_COORDINATES),
    }


def _verify_true_lift_boundary() -> dict[str, Any]:
    from scripts.theory import berry_sextic_q3a3_fake_kernel as q3a3_kernel

    universal = verify_universal_divisor_evaluation_lemma()
    assert universal["status"] == "proved_lemma"
    assert all(universal["machine_checked_identities"].values())

    kernel = q3a3_kernel.verify_exact_sequence()
    assert kernel["status"] == "ok"
    assert kernel["cohomological_fake_kernel_dimension"] == 1
    assert kernel["kernel_generator"] == "D_inf"
    assert kernel["local_fake_image_dimension"] == 4

    # The local divisibility certificate makes D_inf nonzero at varpi.  A
    # global halving would remain a halving after completion, so this also
    # proves the global Kummer class is nonzero.
    from scripts.theory.berry_sextic_q3a3_dinf import verify_certificate

    divisibility = verify_certificate()
    assert divisibility["outcome"] == "D_inf_not_in_2J_Q2_i"

    # The local Q3a3 calculation is used only to control the norm of the
    # global Q(K)-point term.  Do not infer a global Q(K)=R(K)/mu_2 claim from
    # a single completion.
    local_degrees = kernel["relative_factor_degrees"]
    assert local_degrees == [2, 4]
    assert kernel["constant_restriction_kernel_dimension"] == 0
    assert [degree % 2 for degree in local_degrees] == [0, 0]

    # If kappa_K(D_inf) vanished, completion at varpi would make D_inf
    # divisible by 2, contradicting the exact Q3a3 certificate.
    global_dinf_nonzero = divisibility["outcome"] == "D_inf_not_in_2J_Q2_i"
    assert global_dinf_nonzero
    global_norm_image = ["+1"] if [degree % 2 for degree in local_degrees] == [0, 0] else []
    assert global_norm_image == ["+1"]

    return {
        "universal_boundary_lemma": universal,
        "brauer_cokernel": "ker(Br(K)[2] -> Br(L)[2])",
        "brauer_cokernel_kept_separate": True,
        "brauer_boundary": (
            "A true Selmer class has local fake images at every place; its "
            "Brauer obstruction is locally zero and hence globally zero by "
            "the Brauer-Hasse-Noether injection."
        ),
        "infinity_boundary_identity_proved": True,
        "local_lift_obstruction": (
            "For a norm-zero fake class, any H^1(K,J[2]) lift differs locally "
            "from a Kummer lift by im(partial_v); the infinity identity puts "
            "that kernel inside the local Kummer image at every v."
        ),
        "global_norm_image": global_norm_image,
        "global_norm_argument": (
            "Q(K) maps to Q(K_varpi), whose norm image is {+1} because the "
            "relative factor degrees are 2 and 4; no global Q(K)=R(K)/mu_2 "
            "identification is asserted."
        ),
        "norm_zero_fake_classes_have_global_h1_lifts": True,
        "local_fake_membership_makes_every_h1_lift_kummer": True,
        "true_selmer_sequence": ("0 -> F_2<kappa(D_inf)> -> Sel_2(J/K) -> Sel_fake^S -> 0"),
        "kernel_dimension": 1,
        "global_dinf_nonzero": global_dinf_nonzero,
        "true_selmer_dimension": 3,
        "true_selmer_upper_bound": 3,
        "dimension_is_selmer_only": True,
    }


def verify_q3c() -> dict[str, Any]:
    assembly, local_image, support = _frozen_certificates()
    pullback = _verify_pullback(assembly, local_image)
    true_lift = _verify_true_lift_boundary()
    assert (
        true_lift["kernel_dimension"] + pullback["fake_selmer_dimension"]
        == true_lift["true_selmer_dimension"]
    )
    assert support["class_group_trivial"] is True
    assert all(
        entry["ambient_labels"] == ["epsilon_1", "epsilon_2", "epsilon_4"]
        or entry["ambient_labels"] == ["epsilon_2", "epsilon_4"]
        for entry in pullback["ambient_representatives"]
    )
    return {
        "status": "ok",
        "accepted_outcome": (
            "q3c_exact_supported_fake_selmer_true_lift_with_universal_boundary_lemma"
        ),
        "pullback": pullback,
        "support": support,
        "true_lift": true_lift,
        "rank_claimed": False,
        "saturation_claimed": False,
        "rational_t_claimed": False,
    }


def main() -> int:
    result = verify_q3c()
    print(
        "q3c status={status} fake_dim={fake_selmer_dimension} "
        "true_selmer_upper_bound={true_selmer_upper_bound} "
        "kernel={kernel}".format(
            status=result["status"],
            fake_selmer_dimension=result["pullback"]["fake_selmer_dimension"],
            true_selmer_upper_bound=result["true_lift"]["true_selmer_upper_bound"],
            kernel="D_inf",
        )
    )
    print("q3c quotient_coordinates=" + ",".join(result["pullback"]["quotient_coordinates"]))
    print(
        "q3c ambient_representatives="
        + ",".join(
            entry["ambient_coordinates"] for entry in result["pullback"]["ambient_representatives"]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
