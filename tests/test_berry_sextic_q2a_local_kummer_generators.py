"""Pure-Python exact residue check for the Berry C_1 Q2a classes.

The test checks the tangent-normalized evaluations attached to the two
degree-two branch divisors D_12 and D_r.  It uses only the certified residue
factorization at pi; no p-adic, Sage, Magma, or point search is involved.
"""

from __future__ import annotations

PRIME = 37397
RESIDUE_I = 1991
RESIDUE_QUADRATIC = (25179, 6501, 1)

Pair = tuple[int, int]


def _fp2_add(left: Pair, right: Pair) -> Pair:
    return ((left[0] + right[0]) % PRIME, (left[1] + right[1]) % PRIME)


def _fp2_mul(left: Pair, right: Pair) -> Pair:
    left_0, left_1 = left
    right_0, right_1 = right
    constant, alpha = RESIDUE_QUADRATIC[0], RESIDUE_QUADRATIC[1]
    return (
        (left_0 * right_0 - constant * left_1 * right_1) % PRIME,
        (left_0 * right_1 + left_1 * right_0 - alpha * left_1 * right_1) % PRIME,
    )


def _fp2_pow(value: Pair, exponent: int) -> Pair:
    result = (1, 0)
    base = value
    while exponent:
        if exponent & 1:
            result = _fp2_mul(result, base)
        base = _fp2_mul(base, base)
        exponent //= 2
    return result


def _fp2_inv(value: Pair) -> Pair:
    assert value != (0, 0)
    return _fp2_pow(value, PRIME * PRIME - 2)


def _poly_mul(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % PRIME
    return result


def _poly_eval(coefficients: list[int], value: Pair) -> Pair:
    result = (0, 0)
    for coefficient in reversed(coefficients):
        result = _fp2_add(
            _fp2_mul(result, value),
            (coefficient % PRIME, 0),
        )
    return result


def _linear_factor(root: int) -> list[int]:
    return [(-root) % PRIME, 1]


def _fp_square_bit(value: int) -> int:
    value %= PRIME
    assert value != 0
    return 0 if pow(value, (PRIME - 1) // 2, PRIME) == 1 else 1


def _fp2_square_bit(value: Pair) -> int:
    assert value != (0, 0)
    return 0 if _fp2_pow(value, (PRIME * PRIME - 1) // 2) == (1, 0) else 1


def _fp2_norm(value: Pair) -> Pair:
    return _fp2_pow(value, PRIME + 1)


def _rank_mod_two(rows: list[tuple[int, ...]]) -> int:
    mutable = [sum(bit << index for index, bit in enumerate(row)) for row in rows]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (index for index in range(rank, len(mutable)) if mutable[index] >> column & 1),
            None,
        )
        if pivot is None:
            continue
        mutable[rank], mutable[pivot] = mutable[pivot], mutable[rank]
        for index in range(len(mutable)):
            if index != rank and (mutable[index] >> column & 1):
                mutable[index] ^= mutable[rank]
        rank += 1
    return rank


def _residue_factors() -> dict[str, list[int]]:
    roots = {
        "a": (-3615) % PRIME,
        "b": (-9390) % PRIME,
        "r": (-25652) % PRIME,
    }
    f1 = _linear_factor(roots["a"])
    f2 = _linear_factor(roots["b"])
    fr = _poly_mul(_linear_factor(roots["r"]), _linear_factor(roots["r"]))
    fu = list(RESIDUE_QUADRATIC)
    return {"F1": f1, "F2": f2, "Fr": fr, "Fu": fu}


def _component_values() -> dict[str, tuple[Pair, Pair, Pair, Pair]]:
    factors = _residue_factors()
    f1, f2, fr, fu = (factors[name] for name in ("F1", "F2", "Fr", "Fu"))
    h12 = _poly_mul(f1, f2)
    k12 = _poly_mul(fr, fu)
    kr = _poly_mul(h12, fu)
    alpha = (0, 1)
    a = (-3615) % PRIME
    b = (-9390) % PRIME
    r = (-25652) % PRIME
    return {
        "beta_12": (
            _fp2_inv(_poly_eval(k12, (a, 0))),
            _fp2_inv(_poly_eval(k12, (b, 0))),
            _poly_eval(h12, (r, 0)),
            _poly_eval(h12, alpha),
        ),
        "beta_r": (
            _poly_eval(fr, (a, 0)),
            _poly_eval(fr, (b, 0)),
            _fp2_inv(_poly_eval(kr, (r, 0))),
            _poly_eval(fr, alpha),
        ),
    }


def _component_bits(values: tuple[Pair, Pair, Pair, Pair]) -> tuple[int, int, int, int]:
    return (
        _fp_square_bit(values[0][0]),
        _fp_square_bit(values[1][0]),
        _fp_square_bit(values[2][0]),
        _fp2_square_bit(values[3]),
    )


def _norm_residue(values: tuple[Pair, Pair, Pair, Pair]) -> Pair:
    result = _fp2_mul(values[0], values[1])
    result = _fp2_mul(result, (values[2][0] ** 2 % PRIME, 0))
    return _fp2_mul(result, _fp2_norm(values[3]))


def _h_coordinates(bits: tuple[int, int, int, int, int, int, int, int]) -> tuple[int, ...]:
    a_1, b_1, a_2, b_2, c, d, e, f = bits
    assert (a_1 + a_2 + c) % 2 == 0
    assert (b_1 + b_2 + f) % 2 == 0
    return (
        (a_2 + a_1) % 2,
        (b_2 + b_1) % 2,
        (d + b_1) % 2,
        (e + a_1) % 2,
    )


def test_q2a_tangent_classes_are_exact_and_independent() -> None:
    factors = _residue_factors()
    reconstructed = factors["F1"]
    for factor_name in ("F2", "Fr", "Fu"):
        reconstructed = _poly_mul(reconstructed, factors[factor_name])
    reduced_g6 = [
        -1,
        6 + 14 * RESIDUE_I,
        19 - 40 * RESIDUE_I,
        -52 - 28 * RESIDUE_I,
        -35 - 8 * RESIDUE_I,
        -2 - 2 * RESIDUE_I,
        1,
    ]
    assert reconstructed == [value % PRIME for value in reduced_g6]
    discriminant = (6501 * 6501 - 4 * 25179) % PRIME
    assert discriminant == 15866
    assert _fp_square_bit(discriminant) == 1

    eta = (2, 1)
    assert _fp2_square_bit(eta) == 1
    assert _fp2_norm(eta) == (12181, 0)
    assert _fp_square_bit(12181) == 1
    assert _fp_square_bit(2) == 1

    values = _component_values()
    assert values["beta_12"] == (
        (20701, 0),
        (11446, 0),
        (27640, 0),
        (592, 6504),
    )
    assert values["beta_r"] == (
        (29324, 0),
        (18457, 0),
        (8588, 0),
        (37107, 7406),
    )
    assert _norm_residue(values["beta_12"]) == (1, 0)
    assert _norm_residue(values["beta_r"]) == (1, 0)
    assert _component_bits(values["beta_12"]) == (0, 1, 1, 1)
    assert _component_bits(values["beta_r"]) == (0, 0, 1, 0)

    # H coordinates are ordered (h_varpi, h_nu, h_r, h_u).
    beta_12_bits = (0, 0, 0, 1, 0, 1, 0, 1)
    beta_r_bits = (0, 0, 0, 0, 0, 1, 0, 0)
    beta_coordinates = [_h_coordinates(beta_12_bits), _h_coordinates(beta_r_bits)]
    assert beta_coordinates == [(0, 1, 1, 0), (0, 0, 1, 0)]
    assert _rank_mod_two(beta_coordinates) == 2
