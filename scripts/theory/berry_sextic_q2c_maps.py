"""Exact Q2c maps for the Berry C_1 fixed-basis S-unit payload.

This module consumes only the serialized absolute power-basis payload and the
accepted Q2a local basis.  It computes the supported constant quotient, the
relative norm columns, and the odd-pi localization columns.  No Sage, Magma,
Selmer, or rank computation is used here.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.theory import berry_sextic_q2b_fixed_basis as q2b  # noqa: E402

TASK = ROOT / "docs/codex/tasks/berry-sextic-genus2-classification-20260715"
PAYLOAD = TASK / "q2b-fixed-basis-payload.json"

PRIME = 37397
RESIDUE_I = 1991
MODULUS = PRIME * PRIME
BASIS_SIZE = q2b.BASIS_SIZE
RELATIVE_DEGREE = 6
LABELS = q2b.S_UNIT_LABELS
AMBIENT_SIZE = len(LABELS)

Vector = list[Fraction]
KPair = tuple[Fraction, Fraction]
BitVector = tuple[int, ...]

PI: KPair = (Fraction(-169), Fraction(94))
VARRPI: KPair = (Fraction(338), Fraction(-188))
FACTOR_ORDER = ("F1", "F2", "Fr", "Fu")
FACTOR_RESIDUE_DEGREES = {"F1": 1, "F2": 1, "Fr": 1, "Fu": 2}

# The local basis is the Q2a basis (h_varpi,h_nu,h_r,h_u).  The local
# computation first uses [pi] at the three unramified components and then
# changes to [varpi], where [varpi]=[2*pi].
LOCAL_FLAT_ORDER = ("a_1", "b_1", "a_2", "b_2", "c", "d", "e", "f")
LOCAL_H_ORDER = ("h_varpi", "h_nu", "h_r", "h_u")

CONSTANT_NAMES = ("i", "lambda", "pi", "bar_pi")

# Columns are in the ambient order
# zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10.
M_CONST: tuple[BitVector, ...] = (
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0),
    (1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1),
)

# Rows are [i], [1+i], [pi], [bar_pi] in K^*/K^*2.
M_NORM: tuple[BitVector, ...] = (
    (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1),
)

# The exact norm values in K=Q(i), in the same ambient order.  These are
# checked against six-by-six relative multiplication determinants below.
NORM_VALUES: tuple[KPair, ...] = (
    (-1, 0),
    (-1, 0),
    (-1, 0),
    (-1, 0),
    (1, 0),
    (1, 0),
    (1, 1),
    (-1, 1),
    (-169, 94),
    (-169, 94),
    (169, 94),
    (-169, -94),
    (169, -94),
    (-169, -94),
    (19725, -31772),
    (-346957, -7223618),
)

# Mod-p^2 Hensel factors for the selected pi-adic embedding i=1991.  Each
# polynomial is listed in ascending coefficient order.  Their product is
# checked against g6 exactly modulo p^2, so these are not an unverified local
# factor label.
LOCAL_FACTOR_MOD_P2 = {
    "F1": ((3615 + 6043 * PRIME) % MODULUS, 1),
    "F2": ((9390 + 29108 * PRIME) % MODULUS, 1),
    "Fr": (
        (24889 + 31240 * PRIME) % MODULUS,
        (13907 + 2002 * PRIME) % MODULUS,
        1,
    ),
    "Fu": (
        (25179 + 30832 * PRIME) % MODULUS,
        (6501 + 13579 * PRIME) % MODULUS,
        1,
    ),
}

# Exact square witnesses for the three nontrivial constant relations.  They
# are stored in the same absolute power basis as the payload and are checked
# by the multiplication table, rather than trusted as coordinates.
CONSTANT_WITNESSES = {
    "lambda": (
        (12881, 4096),
        (-171585, 4096),
        (1048507, 4096),
        (-1315195, 4096),
        (-315351, 2048),
        (-2942425, 2048),
        (-3706097, 2048),
        (-1369743, 2048),
        (-94003, 4096),
        (103683, 4096),
        (6327, 4096),
        (-1655, 4096),
    ),
    "pi": (
        (3005, 4096),
        (5717, 4096),
        (-1417437, 4096),
        (2706843, 4096),
        (1613045, 2048),
        (6448797, 2048),
        (7013703, 2048),
        (2442671, 2048),
        (133225, 4096),
        (-185855, 4096),
        (-10689, 4096),
        (2935, 4096),
    ),
    "bar_pi": (
        (-293, 8192),
        (-235045, 8192),
        (1149253, 8192),
        (-736859, 8192),
        (289123, 4096),
        (-1924749, 4096),
        (-2942399, 4096),
        (-1153295, 4096),
        (-94001, 8192),
        (86831, 8192),
        (5577, 8192),
        (-1399, 8192),
    ),
}


def _zero() -> Vector:
    return [Fraction(0)] * BASIS_SIZE


def _one() -> Vector:
    return [Fraction(1), *([Fraction(0)] * (BASIS_SIZE - 1))]


def _add(left: Iterable[Fraction], right: Iterable[Fraction]) -> Vector:
    return [a + b for a, b in zip(left, right, strict=True)]


def _scale(vector: Iterable[Fraction], scalar: Fraction | int) -> Vector:
    factor = Fraction(scalar)
    return [factor * value for value in vector]


def _mul(left: Iterable[Fraction], right: Iterable[Fraction]) -> Vector:
    return q2b.multiply_vectors(list(left), list(right))


def _k_add(left: KPair, right: KPair) -> KPair:
    return (left[0] + right[0], left[1] + right[1])


def _k_neg(value: KPair) -> KPair:
    return (-value[0], -value[1])


def _k_mul(left: KPair, right: KPair) -> KPair:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _k_inv(value: KPair) -> KPair:
    denominator = value[0] * value[0] + value[1] * value[1]
    if denominator == 0:
        raise ZeroDivisionError("zero K element")
    return (value[0] / denominator, -value[1] / denominator)


def _k_div(left: KPair, right: KPair) -> KPair:
    return _k_mul(left, _k_inv(right))


def _k_pow(value: KPair, exponent: int) -> KPair:
    result: KPair = (Fraction(1), Fraction(0))
    for _ in range(exponent):
        result = _k_mul(result, value)
    return result


def _k_pi_valuation(value: KPair) -> int:
    if value == (0, 0):
        raise ValueError("the zero K element has no pi valuation")
    current = value
    valuation = 0
    while True:
        quotient = _k_div(current, PI)
        if not all(component.denominator == 1 for component in quotient):
            return valuation
        current = quotient
        valuation += 1


def _k_det(matrix: list[list[KPair]]) -> KPair:
    mutable = [[tuple(value) for value in row] for row in matrix]
    size = len(mutable)
    determinant: KPair = (Fraction(1), Fraction(0))
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if mutable[row][column] != (0, 0)),
            None,
        )
        if pivot is None:
            return (Fraction(0), Fraction(0))
        if pivot != column:
            mutable[column], mutable[pivot] = mutable[pivot], mutable[column]
            determinant = _k_neg(determinant)
        pivot_value = mutable[column][column]
        determinant = _k_mul(determinant, pivot_value)
        pivot_inverse = _k_inv(pivot_value)
        for row in range(column + 1, size):
            if mutable[row][column] == (0, 0):
                continue
            factor = _k_mul(mutable[row][column], pivot_inverse)
            for entry in range(column, size):
                mutable[row][entry] = _k_add(
                    mutable[row][entry],
                    _k_neg(_k_mul(factor, mutable[column][entry])),
                )
    return determinant


def _rational_det(matrix: list[list[Fraction]]) -> Fraction:
    mutable = [list(row) for row in matrix]
    determinant = Fraction(1)
    for column in range(len(mutable)):
        pivot = next(
            (row for row in range(column, len(mutable)) if mutable[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            mutable[column], mutable[pivot] = mutable[pivot], mutable[column]
            determinant = -determinant
        pivot_value = mutable[column][column]
        determinant *= pivot_value
        for row in range(column + 1, len(mutable)):
            if mutable[row][column]:
                factor = mutable[row][column] / pivot_value
                for entry in range(column, len(mutable)):
                    mutable[row][entry] -= factor * mutable[column][entry]
    return determinant


def _inverse_rational_matrix(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(matrix)
    mutable = [
        list(row) + [Fraction(int(row_index == column)) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if mutable[row][column]),
            None,
        )
        if pivot is None:
            raise ValueError("singular rational matrix")
        mutable[column], mutable[pivot] = mutable[pivot], mutable[column]
        pivot_value = mutable[column][column]
        mutable[column] = [value / pivot_value for value in mutable[column]]
        for row in range(size):
            if row == column or not mutable[row][column]:
                continue
            factor = mutable[row][column]
            mutable[row] = [
                left - factor * right
                for left, right in zip(mutable[row], mutable[column], strict=True)
            ]
    return [row[size:] for row in mutable]


def _load_payload() -> dict[str, object]:
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    violations = q2b.validate_payload(payload)
    if violations:
        raise ValueError(f"invalid fixed-basis payload: {violations}")
    return payload


def _payload_vectors(payload: dict[str, object]) -> tuple[Vector, ...]:
    group = payload["s_unit_group"]
    assert isinstance(group, dict)
    elements = group["elements"]
    assert isinstance(elements, list)
    vectors = tuple(q2b.decode_vector(element["coordinates"]) for element in elements)
    if len(vectors) != len(LABELS):
        raise ValueError("the payload does not contain sixteen ambient elements")
    return vectors


def _absolute_relative_change_of_basis(
    payload: dict[str, object],
) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    field = payload["field"]
    assert isinstance(field, dict)
    embedding = q2b.decode_vector(field["k_embedding"]["coordinates"])
    powers = []
    for exponent in range(BASIS_SIZE):
        vector = _zero()
        vector[exponent] = Fraction(1)
        powers.append(vector)
    columns = powers[:RELATIVE_DEGREE]
    columns.extend(_mul(embedding, powers[index]) for index in range(RELATIVE_DEGREE))
    matrix = [[columns[column][row] for column in range(BASIS_SIZE)] for row in range(BASIS_SIZE)]
    inverse = _inverse_rational_matrix(matrix)
    if _rational_det(matrix) != Fraction(-1, 2**34):
        raise AssertionError("unexpected K-relative power-basis determinant")
    return powers, inverse


def _relative_coordinates(vector: Vector, inverse_basis: list[list[Fraction]]) -> tuple[KPair, ...]:
    coefficients = [
        sum(row[index] * vector[index] for index in range(BASIS_SIZE)) for row in inverse_basis
    ]
    return tuple(
        (coefficients[index], coefficients[index + RELATIVE_DEGREE])
        for index in range(RELATIVE_DEGREE)
    )


def _relative_norm(
    element: Vector, powers: list[Vector], inverse_basis: list[list[Fraction]]
) -> KPair:
    columns = []
    for power in powers[:RELATIVE_DEGREE]:
        coordinates = _relative_coordinates(_mul(element, power), inverse_basis)
        columns.append(coordinates)
    matrix = [
        [columns[column][row] for column in range(RELATIVE_DEGREE)]
        for row in range(RELATIVE_DEGREE)
    ]
    return _k_det(matrix)


def _k_vector(value: KPair, embedding: Vector) -> Vector:
    return _add(_scale(_one(), value[0]), _scale(embedding, value[1]))


def _product_for_bits(bits: Iterable[int], vectors: tuple[Vector, ...]) -> Vector:
    result = _one()
    for bit, vector in zip(bits, vectors, strict=True):
        if bit:
            result = _mul(result, vector)
    return result


def _encoded_vector(encoded: Iterable[tuple[int, int]]) -> Vector:
    values = [Fraction(numerator, denominator) for numerator, denominator in encoded]
    if len(values) != BASIS_SIZE:
        raise ValueError("invalid exact witness length")
    return values


def _fraction_mod(value: Fraction, modulus: int) -> int:
    return value.numerator * pow(value.denominator, -1, modulus) % modulus


def _k_scalar_mod(value: KPair, modulus: int, embedding: int) -> int:
    return (
        _fraction_mod(value[0], modulus) + embedding * _fraction_mod(value[1], modulus)
    ) % modulus


def _g6_scalar_coefficients(embedding: int, modulus: int) -> list[int]:
    return [
        (constant + coefficient * embedding) % modulus
        for constant, coefficient in q2b.G6_COEFFICIENTS
    ]


def _poly_mul_mod(left: Iterable[int], right: Iterable[int], modulus: int) -> list[int]:
    left_values = list(left)
    right_values = list(right)
    result = [0] * (len(left_values) + len(right_values) - 1)
    for left_index, left_value in enumerate(left_values):
        for right_index, right_value in enumerate(right_values):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % modulus
    return result


def _poly_eval_mod(coefficients: Iterable[int], value: int, modulus: int) -> int:
    result = 0
    for coefficient in reversed(list(coefficients)):
        result = (result * value + coefficient) % modulus
    return result


def _fp2_add(left: tuple[int, int], right: tuple[int, int], modulus: int) -> tuple[int, int]:
    return ((left[0] + right[0]) % modulus, (left[1] + right[1]) % modulus)


def _fp2_mul(
    left: tuple[int, int],
    right: tuple[int, int],
    linear: int,
    constant: int,
    modulus: int,
) -> tuple[int, int]:
    left_0, left_1 = left
    right_0, right_1 = right
    return (
        (left_0 * right_0 - constant * left_1 * right_1) % modulus,
        (left_0 * right_1 + left_1 * right_0 - linear * left_1 * right_1) % modulus,
    )


def _fp2_pow(
    value: tuple[int, int], exponent: int, linear: int, constant: int, modulus: int
) -> tuple[int, int]:
    result = (1, 0)
    base = value
    while exponent:
        if exponent & 1:
            result = _fp2_mul(result, base, linear, constant, modulus)
        base = _fp2_mul(base, base, linear, constant, modulus)
        exponent //= 2
    return result


def _fp_square_bit(value: int) -> int:
    value %= PRIME
    if value == 0:
        raise ValueError("zero is not a unit squareclass")
    return 0 if pow(value, (PRIME - 1) // 2, PRIME) == 1 else 1


def _fp2_square_bit(value: tuple[int, int]) -> int:
    if value == (0, 0):
        raise ValueError("zero is not a quadratic unit squareclass")
    square = _fp2_pow(value, (PRIME * PRIME - 1) // 2, 6501, 25179, PRIME)
    return 0 if square == (1, 0) else 1


def _relative_eval_scalar(
    coordinates: tuple[KPair, ...], value: int, modulus: int, embedding: int
) -> int:
    result = 0
    for coefficient in reversed(coordinates):
        result = (result * value + _k_scalar_mod(coefficient, modulus, embedding)) % modulus
    return result


def _relative_derivative_mod_p(coordinates: tuple[KPair, ...], value: int) -> int:
    result = 0
    for exponent, coefficient in enumerate(coordinates[1:], start=1):
        result = (
            result
            + exponent * _k_scalar_mod(coefficient, PRIME, RESIDUE_I) * value ** (exponent - 1)
        ) % PRIME
    return result


def _relative_eval_fp2(
    coordinates: tuple[KPair, ...], linear: int, constant: int, modulus: int, embedding: int
) -> tuple[int, int]:
    result = (0, 0)
    for coefficient in reversed(coordinates):
        result = _fp2_mul(result, (0, 1), linear, constant, modulus)
        result = _fp2_add(
            result,
            (_k_scalar_mod(coefficient, modulus, embedding), 0),
            modulus,
        )
    return result


def _local_reductions(coordinates: tuple[KPair, ...]) -> dict[str, int | tuple[int, int]]:
    return {
        "F1": _relative_eval_scalar(coordinates, (-3615) % PRIME, PRIME, RESIDUE_I),
        "F2": _relative_eval_scalar(coordinates, (-9390) % PRIME, PRIME, RESIDUE_I),
        "Fr": _relative_eval_scalar(coordinates, (-25652) % PRIME, PRIME, RESIDUE_I),
        "Fu": _relative_eval_fp2(coordinates, 6501, 25179, PRIME, RESIDUE_I),
    }


def _is_zero_reduction(value: int | tuple[int, int]) -> bool:
    return value == 0 or value == (0, 0)


def _factor_norm_residue(factor: str, value: int | tuple[int, int]) -> int:
    if factor == "Fu":
        if not isinstance(value, tuple):
            raise TypeError("the Fu residue must be a quadratic-field pair")
        constant, linear = value
        return (constant * constant - 6501 * constant * linear + 25179 * linear * linear) % PRIME
    if not isinstance(value, int):
        raise TypeError("a linear or ramified residue must be scalar")
    return value % PRIME


def _local_hensel_data() -> dict[str, object]:
    i_lift = (RESIDUE_I - (RESIDUE_I * RESIDUE_I + 1) * pow(2 * RESIDUE_I, -1, MODULUS)) % MODULUS
    if (i_lift * i_lift + 1) % MODULUS:
        raise AssertionError("the selected i residue did not Hensel lift")
    factors = {name: list(values) for name, values in LOCAL_FACTOR_MOD_P2.items()}
    product = _poly_mul_mod(
        _poly_mul_mod(factors["F1"], factors["F2"], MODULUS),
        _poly_mul_mod(factors["Fr"], factors["Fu"], MODULUS),
        MODULUS,
    )
    if product != _g6_scalar_coefficients(i_lift, MODULUS):
        raise AssertionError("the stored pi-adic factor lifts do not multiply to g6")
    discriminant = (factors["Fr"][1] * factors["Fr"][1] - 4 * factors["Fr"][0]) % MODULUS
    if discriminant % PRIME:
        raise AssertionError("the ramified factor discriminant is not pi-adically odd")
    bar_pi_residue = (-169 - 94 * RESIDUE_I) % PRIME
    d_over_2pi = ((discriminant // PRIME) * bar_pi_residue * pow(2, -1, PRIME)) % PRIME
    if _fp_square_bit(d_over_2pi):
        raise AssertionError("the ramified discriminant class is not 2*pi")
    if d_over_2pi != (15446 * 15446) % PRIME:
        raise AssertionError("the ramified discriminant square witness changed")
    pi_to_varpi_linear_bit = _fp_square_bit(2)
    pi_to_varpi_unramified_bit = _fp2_square_bit((2, 0))
    if pi_to_varpi_linear_bit != 1 or pi_to_varpi_unramified_bit != 0:
        raise AssertionError("the pi-to-varpi local basis conversion changed")
    return {
        "i_lift": i_lift,
        "factors": factors,
        "bar_pi_residue": bar_pi_residue,
        "discriminant_mod_p2": discriminant,
        "d_over_2pi_residue": d_over_2pi,
        "pi_to_varpi_linear_bit": pi_to_varpi_linear_bit,
        "pi_to_varpi_unramified_bit": pi_to_varpi_unramified_bit,
    }


def _audit_zero_components(
    coordinates: tuple[tuple[KPair, ...], ...],
    norm_values: tuple[KPair, ...],
) -> list[dict[str, object]]:
    audit: list[dict[str, object]] = []
    for index, (column, norm_value) in enumerate(zip(coordinates, norm_values, strict=True)):
        reductions = _local_reductions(column)
        zero_factors = [factor for factor in FACTOR_ORDER if _is_zero_reduction(reductions[factor])]
        norm_pi_valuation = _k_pi_valuation(norm_value)
        if not zero_factors:
            if norm_pi_valuation:
                raise AssertionError(f"{LABELS[index]} has pi norm valuation without a local zero")
            audit.append(
                {
                    "label": LABELS[index],
                    "zero_factor": None,
                    "norm_pi_valuation": 0,
                    "local_valuation": 0,
                    "unit_square_bit": None,
                    "normalized_local_norm": None,
                }
            )
            continue

        if len(zero_factors) != 1:
            raise AssertionError(
                f"{LABELS[index]} has unexpected local zero components: {zero_factors}"
            )
        factor = zero_factors[0]
        residue_degree = FACTOR_RESIDUE_DEGREES[factor]
        if norm_pi_valuation == 0 or norm_pi_valuation % residue_degree:
            raise AssertionError(
                f"{LABELS[index]} has incompatible {factor} norm valuation {norm_pi_valuation}"
            )
        # Normalize the component norm exactly.  This uses the residue degree,
        # so a Fu norm with pi^2 valuation is not mistaken for a first-order
        # local uniformizer without checking the underlying payload.
        local_valuation = norm_pi_valuation // residue_degree
        if factor in {"F1", "F2"}:
            norm_uniformizer = _k_pow(PI, local_valuation)
        elif factor == "Fr":
            norm_uniformizer = _k_pow(VARRPI, local_valuation)
        else:
            norm_uniformizer = _k_pow(VARRPI, 2 * local_valuation)
        normalized_norm = _k_div(norm_value, norm_uniformizer)

        other_norm_residue = 1
        for other_factor in FACTOR_ORDER:
            if other_factor == factor:
                continue
            other_value = reductions[other_factor]
            if _is_zero_reduction(other_value):
                raise AssertionError(f"{LABELS[index]} has an unaccounted {other_factor} zero")
            other_norm_residue = (
                other_norm_residue * _factor_norm_residue(other_factor, other_value)
            ) % PRIME
        if other_norm_residue == 0:
            raise AssertionError(f"the nonzero local norms for {LABELS[index]} vanished")
        normalized_local_norm = (
            _k_scalar_mod(normalized_norm, PRIME, RESIDUE_I) * pow(other_norm_residue, -1, PRIME)
        ) % PRIME
        unit_square_bit = _fp_square_bit(normalized_local_norm)
        audit.append(
            {
                "label": LABELS[index],
                "zero_factor": factor,
                "norm_pi_valuation": norm_pi_valuation,
                "local_valuation": local_valuation,
                "unit_square_bit": unit_square_bit,
                "normalized_local_norm": normalized_local_norm,
            }
        )

    positive_norm_indices = {
        index for index, norm_value in enumerate(norm_values) if _k_pi_valuation(norm_value)
    }
    zero_indices = {
        index for index, record in enumerate(audit) if record["zero_factor"] is not None
    }
    if positive_norm_indices != zero_indices:
        raise AssertionError("the payload zero support does not match the relative norm pi support")
    return audit


def _raw_local_column(
    index: int,
    coordinates: tuple[KPair, ...],
    local_data: dict[str, object],
) -> BitVector:
    i_lift = local_data["i_lift"]
    factors = local_data["factors"]
    bar_pi_residue = local_data["bar_pi_residue"]
    zero_audit = local_data["zero_audit"]
    assert isinstance(i_lift, int)
    assert isinstance(bar_pi_residue, int)
    assert isinstance(factors, dict)
    assert isinstance(zero_audit, list)
    record = zero_audit[index]
    assert isinstance(record, dict)
    zero_factor = record["zero_factor"]
    norm_pi_valuation = record["norm_pi_valuation"]
    local_valuation = record["local_valuation"]
    unit_square_bit = record["unit_square_bit"]
    assert zero_factor is None or isinstance(zero_factor, str)
    assert isinstance(norm_pi_valuation, int)
    assert isinstance(local_valuation, int)
    assert unit_square_bit is None or isinstance(unit_square_bit, int)

    reductions = _local_reductions(coordinates)
    f1 = reductions["F1"]
    f2 = reductions["F2"]
    fr = reductions["Fr"]
    fu = reductions["Fu"]
    assert isinstance(f1, int)
    assert isinstance(f2, int)
    assert isinstance(fr, int)
    assert isinstance(fu, tuple)

    f1_factor = factors["F1"]
    f2_factor = factors["F2"]
    fu_factor = factors["Fu"]
    assert isinstance(f1_factor, list)
    assert isinstance(f2_factor, list)
    assert isinstance(fu_factor, list)
    f1_root = (-f1_factor[0]) % MODULUS
    f2_root = (-f2_factor[0]) % MODULUS

    if f1:
        a_1, b_1 = 0, _fp_square_bit(f1)
    else:
        if zero_factor != "F1":
            raise AssertionError(f"an unexpected ambient element vanishes at F1: {index}")
        value = _relative_eval_scalar(coordinates, f1_root, MODULUS, i_lift)
        a_1 = local_valuation % 2
        if unit_square_bit is None:
            raise AssertionError("the F1 zero has no normalized unit bit")
        b_1 = unit_square_bit
        if local_valuation == 1 and norm_pi_valuation == 1:
            if value % PRIME or value % MODULUS == 0:
                raise AssertionError("the F1 zero has no exact first-order normalization")
            normalized = (value // PRIME * bar_pi_residue) % PRIME
            if _fp_square_bit(normalized) != b_1:
                raise AssertionError("the F1 normalized unit disagrees with its norm")
        elif value % MODULUS:
            raise AssertionError("the F1 higher valuation was not visible modulo p^2")

    if f2:
        a_2, b_2 = 0, _fp_square_bit(f2)
    else:
        if zero_factor != "F2":
            raise AssertionError(f"an unexpected ambient element vanishes at F2: {index}")
        value = _relative_eval_scalar(coordinates, f2_root, MODULUS, i_lift)
        a_2 = local_valuation % 2
        if unit_square_bit is None:
            raise AssertionError("the F2 zero has no normalized unit bit")
        b_2 = unit_square_bit
        if local_valuation == 1 and norm_pi_valuation == 1:
            if value % PRIME or value % MODULUS == 0:
                raise AssertionError("the F2 zero has no exact first-order normalization")
            normalized = (value // PRIME * bar_pi_residue) % PRIME
            if _fp_square_bit(normalized) != b_2:
                raise AssertionError("the F2 normalized unit disagrees with its norm")
        elif value % MODULUS:
            raise AssertionError("the F2 higher valuation was not visible modulo p^2")

    if fr:
        c, d = 0, _fp_square_bit(fr)
    else:
        if zero_factor != "Fr":
            raise AssertionError(f"an unexpected ambient element vanishes at Fr: {index}")
        c = local_valuation % 2
        if unit_square_bit is None:
            raise AssertionError("the Fr zero has no normalized unit bit")
        d = unit_square_bit
        if local_valuation == 1 and norm_pi_valuation == 1:
            derivative = _relative_derivative_mod_p(coordinates, (-25652) % PRIME)
            normalized = derivative * pow(2, -1, PRIME) % PRIME
            if not normalized or _fp_square_bit(normalized) != d:
                raise AssertionError("the Fr normalized unit disagrees with its norm")

    if fu != (0, 0):
        e, f = 0, _fp2_square_bit(fu)
    else:
        if zero_factor != "Fu":
            raise AssertionError(f"an unexpected ambient element vanishes at Fu: {index}")
        value = _relative_eval_fp2(
            coordinates,
            fu_factor[1],
            fu_factor[0],
            MODULUS,
            i_lift,
        )
        e = local_valuation % 2
        if unit_square_bit is None:
            raise AssertionError("the Fu zero has no normalized unit bit")
        f = unit_square_bit
        if value[0] % PRIME or value[1] % PRIME:
            raise AssertionError("the Fu zero is not p-adically divisible")
        if local_valuation == 1 and norm_pi_valuation == 1:
            if value == (0, 0):
                raise AssertionError("the Fu zero has no exact first-order normalization")
            normalized = (
                value[0] // PRIME * bar_pi_residue % PRIME,
                value[1] // PRIME * bar_pi_residue % PRIME,
            )
            if _fp2_square_bit(normalized) != f:
                raise AssertionError("the Fu normalized unit disagrees with its norm")
        elif local_valuation >= 2 and value != (0, 0):
            raise AssertionError("the Fu higher valuation was not visible modulo p^2")

    # At F1 and F2, [pi]=[varpi]+[nu].  In the unramified quadratic
    # component, [nu] is already a square, so [pi]=[varpi] there.
    linear_conversion = local_data["pi_to_varpi_linear_bit"]
    unramified_conversion = local_data["pi_to_varpi_unramified_bit"]
    assert isinstance(linear_conversion, int)
    assert isinstance(unramified_conversion, int)
    b_1 ^= a_1 * linear_conversion
    b_2 ^= a_2 * linear_conversion
    f ^= e * unramified_conversion
    return (a_1, b_1, a_2, b_2, c, d, e, f)


def _h_coordinates(flat: BitVector) -> BitVector:
    a_1, b_1, a_2, b_2, _c, d, e, _f = flat
    return (a_1 ^ a_2, b_1 ^ b_2, d ^ b_1, e ^ a_1)


def _rank_mod_two(rows: Iterable[BitVector]) -> int:
    mutable = [sum(bit << index for index, bit in enumerate(row)) for row in rows]
    if not mutable:
        return 0
    width = max(value.bit_length() for value in mutable)
    rank = 0
    for column in range(width):
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


def _matrix_vector_mod_two(rows: Iterable[BitVector], vector: BitVector) -> BitVector:
    return tuple(
        sum(row[index] * vector[index] for index in range(len(vector))) % 2 for row in rows
    )


def _solve_affine_mod_two(rows: list[BitVector], target: BitVector) -> tuple[BitVector | None, int]:
    width = len(rows[0])
    mutable = [[*list(row), target[index]] for index, row in enumerate(rows)]
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(mutable)) if mutable[index][column]),
            None,
        )
        if pivot is None:
            continue
        mutable[rank], mutable[pivot] = mutable[pivot], mutable[rank]
        for index in range(len(mutable)):
            if index != rank and mutable[index][column]:
                mutable[index] = [
                    left ^ right for left, right in zip(mutable[index], mutable[rank], strict=True)
                ]
        pivots.append(column)
        rank += 1
    for row in mutable[rank:]:
        if not any(row[:width]) and row[width]:
            return None, rank
    solution = [0] * width
    for row, column in enumerate(pivots):
        solution[column] = mutable[row][width]
    return tuple(solution), rank


def _local_matrix(
    vectors: tuple[Vector, ...],
    inverse_basis: list[list[Fraction]],
    norm_values: tuple[KPair, ...],
) -> tuple[tuple[BitVector, ...], tuple[BitVector, ...], dict[str, object]]:
    local_data = _local_hensel_data()
    coordinates = tuple(_relative_coordinates(vector, inverse_basis) for vector in vectors)
    local_data["zero_audit"] = _audit_zero_components(coordinates, norm_values)
    columns = tuple(
        _raw_local_column(
            index,
            coordinates[index],
            local_data,
        )
        for index in range(len(vectors))
    )
    flat_rows = tuple(tuple(column[row] for column in columns) for row in range(8))
    h_rows = tuple(tuple(_h_coordinates(column)[row] for column in columns) for row in range(4))
    return flat_rows, h_rows, local_data


def _constant_elements(embedding: Vector) -> dict[str, Vector]:
    i = _k_vector((Fraction(0), Fraction(1)), embedding)
    lambda_value = _k_vector((Fraction(1), Fraction(1)), embedding)
    pi = _k_vector((Fraction(-169), Fraction(94)), embedding)
    bar_pi = _k_vector((Fraction(-169), Fraction(-94)), embedding)
    return {"i": i, "lambda": lambda_value, "pi": pi, "bar_pi": bar_pi}


def _verify_constant_matrix(vectors: tuple[Vector, ...], embedding: Vector) -> dict[str, bool]:
    constants = _constant_elements(embedding)
    if _mul(embedding, embedding) != _scale(_one(), -1):
        raise AssertionError("the payload K embedding is not i^2=-1")
    if _mul(embedding, vectors[0]) != _one():
        raise AssertionError("the zeta4 payload element is not -i")
    checks = {"i": True}
    i_witness = embedding
    i_product = _product_for_bits(M_CONST[0], vectors)
    if _mul(_mul(i_witness, i_witness), i_product) != constants["i"]:
        raise AssertionError("the exact i constant relation failed")
    checks["i_square_witness"] = True
    for name, column in zip(CONSTANT_NAMES[1:], M_CONST[1:], strict=True):
        witness = _encoded_vector(CONSTANT_WITNESSES[name])
        product = _product_for_bits(column, vectors)
        if _mul(_mul(witness, witness), product) != constants[name]:
            raise AssertionError(f"the exact {name} constant relation failed")
        checks[f"{name}_square_witness"] = True
    if _rank_mod_two(M_CONST) != 4:
        raise AssertionError("the four supported constant columns are dependent")
    return checks


def _verify_norms(actual: tuple[KPair, ...]) -> dict[str, bool]:
    expected = tuple((Fraction(left), Fraction(right)) for left, right in NORM_VALUES)
    if actual != expected:
        raise AssertionError(f"relative norm mismatch: {actual!r}")
    if _rank_mod_two(M_NORM) != 4:
        raise AssertionError("the norm matrix has unexpected rank")
    return {"relative_determinants": True, "norm_matrix_rank": True}


def _verify_local_matrix(
    flat_rows: tuple[BitVector, ...],
    h_rows: tuple[BitVector, ...],
) -> dict[str, bool]:
    # H coordinates are defined only on the local norm kernel.  The following
    # component norm rows are exact identities in the chosen local basis.
    local_norm_rows = (
        tuple(flat_rows[0][j] ^ flat_rows[2][j] ^ flat_rows[4][j] for j in range(AMBIENT_SIZE)),
        tuple(flat_rows[1][j] ^ flat_rows[3][j] ^ flat_rows[7][j] for j in range(AMBIENT_SIZE)),
    )
    local_constant_rows = ((0, 1), (0, 1), (1, 1), (0, 1))
    for column in range(AMBIENT_SIZE):
        expected = tuple(
            sum(local_constant_rows[basis][row] * M_NORM[basis][column] for basis in range(4)) % 2
            for row in range(2)
        )
        actual = tuple(local_norm_rows[row][column] for row in range(2))
        if actual != expected:
            raise AssertionError(f"local/global norm mismatch in column {column}")

    constant_local_flat = _matrix_vector_mod_two(flat_rows, M_CONST[0])
    if constant_local_flat != (0, 1, 0, 1, 0, 1, 0, 0):
        raise AssertionError("the local i constant is not the certified diagonal class")
    for column in M_CONST[1:]:
        if _matrix_vector_mod_two(h_rows, column) != (0, 0, 0, 0):
            raise AssertionError("a supported constant did not vanish in the fake quotient")

    h_basis = (
        (0, 0, 1, 0, 1, 0, 0, 0),
        (0, 0, 0, 1, 0, 0, 0, 1),
        (0, 0, 0, 0, 0, 1, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 0),
    )
    if any(
        _h_coordinates(vector) != tuple(1 if row == index else 0 for row in range(4))
        for index, vector in enumerate(h_basis)
    ):
        raise AssertionError("the Q2a H_pi basis coordinate convention changed")
    if _rank_mod_two(h_rows) != 4:
        raise AssertionError("the localization projection has unexpected rank")
    return {
        "local_norm_compatibility": True,
        "constant_localization": True,
        "q2a_basis_coordinates": True,
        "local_projection_rank": True,
    }


def build_certificate() -> dict[str, object]:
    payload = _load_payload()
    vectors = _payload_vectors(payload)
    field = payload["field"]
    assert isinstance(field, dict)
    embedding = q2b.decode_vector(field["k_embedding"]["coordinates"])
    powers, inverse_basis = _absolute_relative_change_of_basis(payload)

    checks = {}
    checks.update(_verify_constant_matrix(vectors, embedding))
    norm_values = tuple(_relative_norm(vector, powers, inverse_basis) for vector in vectors)
    checks.update(_verify_norms(norm_values))
    flat_rows, h_rows, local_data = _local_matrix(vectors, inverse_basis, norm_values)
    checks.update(_verify_local_matrix(flat_rows, h_rows))

    combined_rows = list(M_NORM) + list(h_rows)
    beta_12 = (0, 1, 1, 0)
    beta_r = (0, 0, 1, 0)
    beta_solutions = {}
    for name, target in (("beta_12", beta_12), ("beta_r", beta_r)):
        solution, rank = _solve_affine_mod_two(
            combined_rows,
            (0, 0, 0, 0, *target),
        )
        if solution is None:
            raise AssertionError(f"no global ambient lift for {name}")
        if _matrix_vector_mod_two(M_NORM, solution) != (0, 0, 0, 0):
            raise AssertionError(f"norm equation failed for {name}")
        if _matrix_vector_mod_two(h_rows, solution) != target:
            raise AssertionError(f"local equation failed for {name}")
        beta_solutions[name] = {
            "ambient_vector": solution,
            "rank": rank,
            "solution_space_dimension": AMBIENT_SIZE - rank,
        }

    expected_beta_12 = tuple(1 if index == 1 else 0 for index in range(AMBIENT_SIZE))
    expected_beta_r = tuple(1 if index in (1, 4) else 0 for index in range(AMBIENT_SIZE))
    if beta_solutions["beta_12"]["ambient_vector"] != expected_beta_12:
        raise AssertionError("the beta_12 canonical lift changed")
    if beta_solutions["beta_r"]["ambient_vector"] != expected_beta_r:
        raise AssertionError("the beta_r canonical lift changed")

    return {
        "status": "ok",
        "payload": PAYLOAD.as_posix(),
        "ambient_labels": list(LABELS),
        "constant_names": list(CONSTANT_NAMES),
        "constant_matrix_columns": [list(column) for column in M_CONST],
        "norm_basis": list(CONSTANT_NAMES),
        "norm_matrix_rows": [list(row) for row in M_NORM],
        "norm_values": [[left, right] for left, right in NORM_VALUES],
        "local_flat_order": list(LOCAL_FLAT_ORDER),
        "local_flat_matrix_rows": [list(row) for row in flat_rows],
        "local_h_order": list(LOCAL_H_ORDER),
        "local_h_matrix_rows": [list(row) for row in h_rows],
        "beta_solutions": beta_solutions,
        "rational_relative_basis_determinant": [-1, 2**34],
        "local_hensel_data": local_data,
        "checks": checks,
        "constant_matrix_rank": _rank_mod_two(M_CONST),
        "norm_matrix_rank": _rank_mod_two(M_NORM),
        "combined_equation_rank": _rank_mod_two(combined_rows),
    }


def main() -> int:
    certificate = build_certificate()
    print(
        "q2c status={status} M_const_rank={constant_matrix_rank} "
        "M_norm_rank={norm_matrix_rank} combined_rank={combined_equation_rank}".format(
            **certificate
        )
    )
    for name, result in certificate["beta_solutions"].items():
        vector = result["ambient_vector"]
        selected = [LABELS[index] for index, bit in enumerate(vector) if bit]
        print(f"{name} lift=" + "+".join(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
