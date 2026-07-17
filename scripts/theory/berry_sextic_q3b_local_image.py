"""Verify exact local divisor classes closing Berry Q3b.

The verifier keeps the Q3a2 primary-quotient basis fixed.  It checks the
quadratic local-point certificates by exact integer polynomial arithmetic and
checks each localization residue by an exact maximal-order numerator /
denominator identity before converting it to the frozen H_varpi coordinates.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TASK = ROOT / "docs/codex/tasks/berry-sextic-genus2-classification-20260715"
DYADIC_TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
PAYLOAD = TASK / "q3b-local-image-payload.json"
Q3A2_PAYLOAD = DYADIC_TASK / "q3a2-dyadic-matrices-payload.json"

Polynomial = list[int]
RationalPolynomial = list[Fraction]


def _add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return _trim(result)


def _neg(value: Polynomial) -> Polynomial:
    return [-entry for entry in value]


def _sub(left: Polynomial, right: Polynomial) -> Polynomial:
    return _add(left, _neg(right))


def _mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return _trim(result)


def _pow(value: Polynomial, exponent: int) -> Polynomial:
    result = [1]
    while exponent:
        if exponent & 1:
            result = _mul(result, value)
        value = _mul(value, value)
        exponent >>= 1
    return result


def _trim(value: Polynomial) -> Polynomial:
    result = value[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _rational_poly_add(left: RationalPolynomial, right: RationalPolynomial) -> RationalPolynomial:
    result = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _rational_poly_mul(left: RationalPolynomial, right: RationalPolynomial) -> RationalPolynomial:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _rational_poly_reduce(
    value: RationalPolynomial, modulus: RationalPolynomial
) -> RationalPolynomial:
    remainder = value[:]
    while len(remainder) >= len(modulus):
        shift = len(remainder) - len(modulus)
        coefficient = remainder[-1] / modulus[-1]
        for index, entry in enumerate(modulus):
            remainder[index + shift] -= coefficient * entry
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return remainder


def _power_multiply(
    left: RationalPolynomial, right: RationalPolynomial, modulus: RationalPolynomial
) -> RationalPolynomial:
    return _rational_poly_reduce(_rational_poly_mul(left, right), modulus)


def _solve_rational_system(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction]:
    size = len(matrix)
    augmented = [[*row[:], target[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise AssertionError("the frozen order basis is not invertible")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[column], strict=True)
                ]
    return [augmented[index][-1] for index in range(size)]


def _divmod_monic(value: Polynomial, modulus: Polynomial) -> tuple[Polynomial, Polynomial]:
    remainder = value[:]
    quotient = [0] * max(1, len(value) - len(modulus) + 1)
    while len(remainder) >= len(modulus):
        shift = len(remainder) - len(modulus)
        coefficient = remainder[-1]
        quotient[shift] += coefficient
        for index, entry in enumerate(modulus):
            remainder[index + shift] -= coefficient * entry
        remainder = _trim(remainder)
    return _trim(quotient), remainder


def _reduce(value: Polynomial, modulus: Polynomial) -> Polynomial:
    return _divmod_monic(value, modulus)[1]


def _v2(value: Fraction | int) -> int:
    value = Fraction(value)
    if value == 0:
        return 10**9
    numerator = abs(value.numerator)
    denominator = value.denominator
    result = 0
    while numerator % 2 == 0:
        numerator //= 2
        result += 1
    while denominator % 2 == 0:
        denominator //= 2
        result -= 1
    return result


def _z_valuation(coefficients: Polynomial | RationalPolynomial, a: int, norm_d: int) -> int:
    """Compute the exact valuation for z^4-2*a*z^2+norm_d."""

    current = [Fraction(value) for value in coefficients] + [Fraction(0)] * 4
    current = current[:4]
    valuation = 0
    while True:
        if all(value == 0 for value in current):
            return 10**9
        if any(_v2(value) < 0 for value in current):
            return valuation
        if _v2(current[0]) < 1:
            return valuation
        y3 = -current[0] / norm_d
        current = [current[1], current[2] - 2 * a * y3, current[3], y3]
        valuation += 1


def _gaussian_mul(left: list[int], right: list[int]) -> list[int]:
    return [
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    ]


def _gaussian_sub(left: list[int], right: list[int]) -> list[int]:
    return [left[0] - right[0], left[1] - right[1]]


def _gaussian_scale(value: list[int], scalar: int) -> list[int]:
    return [scalar * value[0], scalar * value[1]]


def _poly_scale(value: Polynomial, scalar: int) -> Polynomial:
    return [scalar * entry for entry in value]


def _pair_to_poly(pair: list[int], i_poly: Polynomial) -> Polynomial:
    return _add([pair[0]], _poly_scale(i_poly, pair[1]))


def _exact_square_certificate(entry: dict[str, Any]) -> None:
    da, db = map(int, entry["d"])
    assert db == 1
    norm_d = da * da + db * db
    assert _v2(norm_d) == 1
    assert da % 2 == 1

    i_poly = [-da, 0, 1]
    t0 = list(map(int, entry["point_t0"]))
    t1 = list(map(int, entry["point_t1"]))
    assert t1 != [0, 0]
    t_poly = _add(_pair_to_poly(t0, i_poly), _mul(_pair_to_poly(t1, i_poly), [0, 1]))
    modulus = [norm_d, 0, -2 * da, 0, 1]
    assert _reduce(modulus, modulus) == [0]
    assert entry["t_polynomial_ascending"] == t_poly

    g_coefficients = [
        (-1, 0),
        (6, 14),
        (19, -40),
        (-52, -28),
        (-35, -8),
        (-2, -2),
        (1, 0),
    ]
    g_poly = [0]
    for exponent, coefficient in enumerate(g_coefficients):
        g_poly = _add(
            g_poly,
            _mul(
                _pair_to_poly(list(coefficient), i_poly),
                _pow(t_poly, exponent),
            ),
        )
    g_value = _reduce(g_poly, modulus)
    assert g_value != [0]
    witness = list(map(int, entry["witness_coefficients"]))
    error = _reduce(_sub(_mul(witness, witness), g_poly), modulus)
    assert error == list(map(int, entry["expected_error_remainder"]))
    assert entry["g_value_remainder"] == g_value

    witness_value = _z_valuation(witness, da, norm_d)
    g_value_valuation = _z_valuation(g_value, da, norm_d)
    error_value = _z_valuation(error, da, norm_d)
    assert witness_value == int(entry["expected_witness_valuation"])
    assert g_value_valuation == int(entry["expected_g_value_valuation"])
    assert error_value == int(entry["expected_error_valuation"])
    assert g_value_valuation == 2 * witness_value
    if error_value < 10**9:
        assert error_value - 2 * witness_value >= 2 * 4 + 1

    # The quartic is 2-Eisenstein: its nonleading coefficients are even and
    # its constant coefficient has valuation one. Hence e=4, and U_{2e+1}
    # is a square in the resulting local field.
    # Thus g(t)=w^2*(1-error/w^2) is an exact square, not a finite-precision
    # assertion.
    assert 2 * 4 + 1 == 9


def _encoded_fraction_vector(encoded: list[list[int]]) -> list[Fraction]:
    return [Fraction(int(numerator), int(denominator)) for numerator, denominator in encoded]


def _verify_element_coordinate_certificate(
    entry: dict[str, Any], q3a2_payload: dict[str, Any]
) -> None:
    d = list(map(int, entry["d"]))
    t0 = list(map(int, entry["point_t0"]))
    t1 = list(map(int, entry["point_t1"]))
    expected_u = [
        _gaussian_sub(_gaussian_mul(t0, t0), _gaussian_mul(d, _gaussian_mul(t1, t1))),
        _gaussian_scale(t0, -2),
        [1, 0],
    ]
    assert entry["u_coefficients_ascending"] == expected_u

    field = q3a2_payload["field"]
    modulus = [Fraction(int(value)) for value in field["absolute_polynomial_ascending"]]
    one = [Fraction(int(index == 0)) for index in range(12)]
    theta = [Fraction(int(index == 1)) for index in range(12)]
    i_absolute = _encoded_fraction_vector(field["k_embedding_power_coordinates"])
    i_theta = _power_multiply(i_absolute, theta, modulus)
    theta_squared = _power_multiply(theta, theta, modulus)
    constant, linear, _ = expected_u
    element_power = _rational_poly_add(
        _rational_poly_add(
            _rational_poly_add(
                [Fraction(constant[0]) * value for value in one],
                [Fraction(constant[1]) * value for value in i_absolute],
            ),
            [Fraction(linear[0]) * value for value in theta],
        ),
        _rational_poly_add(
            [Fraction(linear[1]) * value for value in i_theta],
            theta_squared,
        ),
    )
    order_basis = [_encoded_fraction_vector(row) for row in field["order_basis_power_coordinates"]]
    order_matrix = [[order_basis[column][row] for column in range(12)] for row in range(12)]
    order_coordinates = _solve_rational_system(order_matrix, element_power)
    assert all(value.denominator == 1 for value in order_coordinates)
    assert [int(value) for value in order_coordinates] == list(
        map(int, entry["element_order_coordinates"])
    )


def _fraction_vector(encoded: list[list[int]]) -> list[Fraction]:
    return [Fraction(int(numerator), int(denominator)) for numerator, denominator in encoded]


def _fraction_multiply(
    left: list[Fraction], right: list[Fraction], table: list[Any]
) -> list[Fraction]:
    result = [Fraction(0)] * len(left)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            if left_value == 0 or right_value == 0:
                continue
            for coordinate, value in enumerate(table[left_index][right_index]):
                result[coordinate] += left_value * right_value * int(value)
    return result


def _fraction_power(
    value: list[Fraction], exponent: int, table: list[Any], one: list[Fraction]
) -> list[Fraction]:
    if exponent < 0:
        raise ValueError("fraction-power verifier only accepts nonnegative exponents")
    result = one[:]
    while exponent:
        if exponent & 1:
            result = _fraction_multiply(result, value, table)
        value = _fraction_multiply(value, value, table)
        exponent >>= 1
    return result


def _assert_fraction_equal(left: list[Fraction], right: list[Fraction]) -> None:
    assert left == right


def _quotient_inverse(
    value: tuple[int, ...],
    record: dict[str, Any],
    table: list[Any],
    order_one: tuple[int, ...],
) -> tuple[int, ...]:
    from scripts.theory import berry_sextic_q3a_dyadic_matrices as q3a2

    quotient = record["quotient"]
    result = q3a2._reduce(order_one, quotient["ideal_hnf"])
    base = value
    exponent = 2 ** int(quotient["precision_exponent"]) - 1
    while exponent:
        if exponent & 1:
            result = q3a2._reduce(q3a2._multiply(result, base, table), quotient["ideal_hnf"])
        base = q3a2._reduce(q3a2._multiply(base, base, table), quotient["ideal_hnf"])
        exponent >>= 1
    assert q3a2._reduce(
        q3a2._multiply(value, result, table), quotient["ideal_hnf"]
    ) == q3a2._reduce(order_one, quotient["ideal_hnf"])
    return result


def _prepare_local_records(q3a2_payload: dict[str, Any]) -> list[dict[str, Any]]:
    from scripts.theory import berry_sextic_q3a_dyadic_matrices as q3a2

    table = q3a2_payload["order_multiplication_table"]
    one = tuple(int(value) for value in q3a2_payload["field"]["order_one_coordinates"])
    records: list[dict[str, Any]] = []
    for original in q3a2_payload["local_records"]:
        record = json.loads(json.dumps(original))
        q3a2._quotient_squareclass_check(record, table, one)
        records.append(record)
    return records


def _verify_localization(
    entry: dict[str, Any],
    q3a2_payload: dict[str, Any],
    local_records: list[dict[str, Any]],
) -> list[int]:
    from scripts.theory import berry_sextic_q3a_dyadic_matrices as q3a2

    table = q3a2_payload["order_multiplication_table"]
    order_one = tuple(int(value) for value in q3a2_payload["field"]["order_one_coordinates"])
    field = q3a2_payload["field"]
    order_basis = [_encoded_fraction_vector(row) for row in field["order_basis_power_coordinates"]]
    order_matrix = [[order_basis[column][row] for column in range(12)] for row in range(12)]
    element = [Fraction(int(value), 1) for value in entry["element_order_coordinates"]]
    flat: list[int] = []
    for local_record, witness in zip(local_records, entry["local_records"], strict=True):
        assert int(witness["prime_index"]) == int(local_record["index"])
        quotient = local_record["quotient"]
        hnf = quotient["ideal_hnf"]
        prime_hnf = quotient["ideal_hnf_p"]
        valuation = int(witness["valuation"])
        uniformizer = _fraction_vector(witness["uniformizer_order_coordinates"])
        frozen_uniformizer_power = _encoded_fraction_vector(
            local_record["uniformizer_power_coordinates"]
        )
        frozen_uniformizer_order = _solve_rational_system(
            order_matrix,
            frozen_uniformizer_power,
        )
        assert uniformizer == frozen_uniformizer_order
        denominator = [
            Fraction(int(value), 1) for value in witness["denominator_order_coordinates"]
        ]
        numerator = [Fraction(int(value), 1) for value in witness["numerator_order_coordinates"]]
        denominator_times_element = _fraction_multiply(denominator, element, table)
        if valuation >= 0:
            uniformizer_power = _fraction_power(
                uniformizer,
                valuation,
                table,
                [Fraction(value, 1) for value in order_one],
            )
            _assert_fraction_equal(
                _fraction_multiply(numerator, uniformizer_power, table),
                denominator_times_element,
            )
        else:
            uniformizer_power = _fraction_power(
                uniformizer,
                -valuation,
                table,
                [Fraction(value, 1) for value in order_one],
            )
            _assert_fraction_equal(
                numerator,
                _fraction_multiply(denominator_times_element, uniformizer_power, table),
            )
        assert all(value.denominator == 1 for value in numerator + denominator)
        denominator_int = tuple(int(value) for value in denominator)
        numerator_int = tuple(int(value) for value in numerator)
        assert q3a2._reduce(denominator_int, prime_hnf) != (0,) * 12
        assert q3a2._reduce(numerator_int, prime_hnf) != (0,) * 12

        denominator_residue = q3a2._reduce(denominator_int, hnf)
        numerator_residue = q3a2._reduce(numerator_int, hnf)
        inverse = _quotient_inverse(denominator_residue, local_record, table, order_one)
        residue = q3a2._reduce(q3a2._multiply(numerator_residue, inverse, table), hnf)
        assert list(residue) == list(map(int, witness["unit_residue"]))
        coordinate_map = local_record["_coordinate_map"]
        assert residue in coordinate_map
        expected_local = [valuation & 1, *map(int, coordinate_map[residue])]
        assert expected_local == list(map(int, witness["local_squareclass"]))
        flat.extend(expected_local)

    assert len(flat) == 16
    return flat


def _verify_entry(
    entry: dict[str, Any], q3a2_payload: dict[str, Any], local_records: list[dict[str, Any]]
) -> list[int]:
    from scripts.theory import berry_sextic_q3b_assembly as q3b

    _exact_square_certificate(entry)
    _verify_element_coordinate_certificate(entry, q3a2_payload)
    flat = _verify_localization(entry, q3a2_payload, local_records)
    quotient_matrix = q3a2_payload["quotient_coordinate_matrix_rows"]
    fake = [
        sum(quotient_matrix[row][column] * flat[column] for column in range(16)) % 2
        for row in range(12)
    ]
    assert q3a2_payload["norm_matrix_on_fake_quotient_rows"]
    assert all(
        sum(row[column] * fake[column] for column in range(12)) % 2 == 0
        for row in q3a2_payload["norm_matrix_on_fake_quotient_rows"]
    )
    h_coordinates = q3b._matvec(
        q3b._coordinate_extractor(q3a2_payload["norm_kernel_basis_quotient_rows"]),
        fake,
    )
    assert "".join(map(str, h_coordinates)) == entry["expected_h"]
    return h_coordinates


def verify_local_image() -> dict[str, Any]:
    from scripts.theory import berry_sextic_q3a3_exact_class as q3a3_class
    from scripts.theory import berry_sextic_q3a3_fake_kernel as q3a3_kernel
    from scripts.theory import berry_sextic_q3a_dyadic_matrices as q3a2
    from scripts.theory import berry_sextic_q3b_assembly as q3b

    q3a2_payload = json.loads(Q3A2_PAYLOAD.read_text(encoding="utf-8"))
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "berry-c1-q3b-local-image-v1"
    assert payload["q3a2_schema"] == q3a2_payload["schema_version"]
    assert q3a2.verify_payload()["status"] == "ok"
    assert q3a3_class.verify_payload()["status"] == "ok"
    kernel = q3a3_kernel.verify_exact_sequence()
    assert kernel["local_fake_image_dimension"] == 4
    assembly = q3b.verify_assembly()
    assert assembly["status"] == "coordinate_blocker"

    local_records = _prepare_local_records(q3a2_payload)
    classes = [
        q3a3_class.verify_payload()["h_varpi_squareclass"],
        *[_verify_entry(entry, q3a2_payload, local_records) for entry in payload["entries"]],
    ]
    assert q3b._rank(classes) == 4
    image_basis = [list(vector) for vector in classes]
    annihilator = [list(row) for row in assembly["h_varpi_image_annihilator_rows"]]
    coefficient_kernel = q3b._nullspace(
        q3b._matmul(annihilator, q3b._transpose(image_basis)),
        len(image_basis),
    )
    intersection_basis = [
        q3b._matvec(q3b._transpose(image_basis), coefficients)
        for coefficients in coefficient_kernel
    ]
    assert len(intersection_basis) == 2
    assert q3b._rank(intersection_basis) == 2
    assert all(q3b._matvec(annihilator, vector) == [0, 0] for vector in intersection_basis)
    expected_intersection = [
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 0],
    ]
    assert all(q3b._in_span(vector, intersection_basis) for vector in expected_intersection)
    assert all(q3b._in_span(vector, expected_intersection) for vector in intersection_basis)
    return {
        "status": "ok",
        "local_image_dimension": 4,
        "image_basis": ["".join(map(str, value)) for value in image_basis],
        "image_basis_rank": q3b._rank(classes),
        "intersection_dimension": len(intersection_basis),
        "intersection_basis": ["".join(map(str, value)) for value in expected_intersection],
        "kernel_generator": "D_inf",
        "membership_evidence": "three quadratic local divisors plus frozen D_i",
    }


def main() -> int:
    result = verify_local_image()
    print(
        "q3b-local-image status={status} dimension={local_image_dimension} "
        "rank={image_basis_rank} basis={basis} intersection={intersection_basis}".format(
            basis=",".join(result["image_basis"]), **result
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
