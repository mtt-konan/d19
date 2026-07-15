"""Pure-Python boundary check for the Berry C_1 Q2 odd-prime retry.

This checks only the already certified residue factorization and dimensions.
It deliberately does not compute a local Kummer image or global coordinates.
"""

from __future__ import annotations

PRIME = 37397
RESIDUE_I = 1991


def _mul_mod(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % PRIME
    return result


def _linear_factor(root: int) -> list[int]:
    return [(-root) % PRIME, 1]


def _legendre(value: int) -> int:
    value %= PRIME
    if value == 0:
        return 0
    result = pow(value, (PRIME - 1) // 2, PRIME)
    return 1 if result == 1 else -1


def build_boundary_certificate() -> dict[str, object]:
    roots = {
        "double": (-25652) % PRIME,
        "linear_3615": (-3615) % PRIME,
        "linear_9390": (-9390) % PRIME,
    }
    reduced_g6 = [
        (-1) % PRIME,
        (6 + 14 * RESIDUE_I) % PRIME,
        (19 - 40 * RESIDUE_I) % PRIME,
        (-52 - 28 * RESIDUE_I) % PRIME,
        (-35 - 8 * RESIDUE_I) % PRIME,
        (-2 - 2 * RESIDUE_I) % PRIME,
        1,
    ]
    reduced_quadratic = [25179, 6501, 1]
    factorization = _mul_mod(
        _mul_mod(
            _mul_mod(
                _mul_mod(
                    _linear_factor(roots["double"]),
                    _linear_factor(roots["double"]),
                ),
                _linear_factor(roots["linear_3615"]),
            ),
            _linear_factor(roots["linear_9390"]),
        ),
        reduced_quadratic,
    )
    discriminant = (6501 * 6501 - 4 * 25179) % PRIME
    global_basis = ("zeta4", *(f"epsilon_{index}" for index in range(1, 6)), *(
        f"S_prime_{index}" for index in range(1, 11)
    ))

    assert RESIDUE_I * 94 % PRIME == 169 % PRIME
    assert factorization == reduced_g6
    assert discriminant == 15866
    assert _legendre(discriminant) == -1
    assert len(global_basis) == 16

    return {
        "status": "precise_q2_missing_coordinate_certificate",
        "place": "pi=(94*i-169)",
        "residue_characteristic": PRIME,
        "reduced_factorization": "(t-11745)^2*(t+3615)*(t+9390)*(t^2+6501*t+25179)",
        "local_factor_degrees": [1, 1, 2, 2],
        "orbit_dimension": 4 - 1 - 1,
        "global_coordinate_dimension": len(global_basis),
        "local_image_coordinates_certified": False,
        "global_selmer_or_rank_claimed": False,
    }


if __name__ == "__main__":
    certificate = build_boundary_certificate()
    print(f"status={certificate['status']}")
    print("mod_pi_factorization=ok")
    print(f"orbit_dimension={certificate['orbit_dimension']}")
    print(f"global_coordinate_dimension={certificate['global_coordinate_dimension']}")
