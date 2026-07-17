#!/usr/bin/env sage
"""Produce the exact local-divisor payload for Berry Q3b.

The three new classes are traces of quadratic local points.  The square
witnesses are checked by the Python verifier using exact integer polynomial
arithmetic; this producer supplies their frozen-field localization residues
and the corresponding maximal-order witnesses.
"""

import json
import runpy
import sys
from pathlib import Path

from sage.all import QQ, ZZ

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "docs/codex/tasks/berry-sextic-genus2-classification-20260715"
DYADIC_TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
OUT = TASK / "q3b-local-image-payload.json"
Q3A2_SOURCE = ROOT / "scripts/theory/berry_sextic_q3a_dyadic_matrices.sage"
sys.path.insert(0, str(ROOT))


SQUARE_CERTIFICATES = {
    "D_lambda": {
        "d": [1, 1],
        "point_t0": [-1, 2],
        "point_t1": [-2, 0],
        "witness_coefficients": [0, -16, 32, -8],
        "expected_error_remainder": [0],
        "expected_g_value_valuation": 30,
        "expected_witness_valuation": 15,
        "expected_error_valuation": 10**9,
        "expected_h": "01111000",
    },
    "D_3+i": {
        "d": [3, 1],
        "point_t0": [-1, 2],
        "point_t1": [-2, 2],
        "witness_coefficients": [240, 56, 104, 240],
        "expected_error_remainder": [-3588096, -385024, 1712128, 393216],
        "expected_g_value_valuation": 26,
        "expected_witness_valuation": 13,
        "expected_error_valuation": 53,
        "expected_h": "00001100",
    },
    "D_5+i": {
        "d": [5, 1],
        "point_t0": [1, 0],
        "point_t1": [0, 2],
        "witness_coefficients": [16, 832, 80, 1792],
        "expected_error_remainder": [-912670720, -7372800, 268222464, 3047424],
        "expected_g_value_valuation": 32,
        "expected_witness_valuation": 16,
        "expected_error_valuation": 56,
        "expected_h": "00011000",
    },
}


def _add(left, right):
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _neg(value):
    return [-entry for entry in value]


def _sub(left, right):
    return _add(left, _neg(right))


def _mul(left, right):
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _pow(value, exponent):
    result = [1]
    while exponent:
        if exponent & 1:
            result = _mul(result, value)
        value = _mul(value, value)
        exponent >>= 1
    return result


def _divmod_monic(value, modulus):
    remainder = value[:]
    quotient = [0] * max(1, len(value) - len(modulus) + 1)
    while len(remainder) >= len(modulus):
        shift = len(remainder) - len(modulus)
        coefficient = remainder[-1]
        quotient[shift] += coefficient
        for index, entry in enumerate(modulus):
            remainder[index + shift] -= coefficient * entry
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return quotient, remainder


def _reduce(value, modulus):
    return _divmod_monic(value, modulus)[1]


def _gaussian_mul(left, right):
    return [left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]]


def _gaussian_sub(left, right):
    return [left[0] - right[0], left[1] - right[1]]


def _gaussian_scale(value, scalar):
    return [scalar * value[0], scalar * value[1]]


def _poly_scale(value, scalar):
    return [scalar * entry for entry in value]


def _order_coordinates(src, La, O, element):
    return [
        [int(QQ(value).numerator()), int(QQ(value).denominator())]
        for value in src["order_coordinates"](La, O, element)
    ]


def _order_integer_coordinates(src, La, O, element):
    coordinates = _order_coordinates(src, La, O, element)
    if any(value[1] != 1 for value in coordinates):
        raise AssertionError("the local witness is not integral in the maximal order")
    return [value[0] for value in coordinates]


def _local_witness(src, La, O, prime_index, P, e, table, element):
    quotient = src["quotient_data"](La, O, P, e)
    quotient["local_degree"] = int(e)
    _, _, coordinate_map = src["unit_squareclasses"](quotient, table)
    uniformizer = La.uniformizer(P)
    valuation = La.valuation(P)(element)
    integer_valuation = ZZ(e * valuation)
    unit = element / uniformizer**integer_valuation
    denominator_ideal = O.fractional_ideal(1 / unit)
    integral_denominator_ideal = denominator_ideal.intersection(O.fractional_ideal(1))
    denominator = next(
        candidate
        for candidate in integral_denominator_ideal.basis()
        if e * La.valuation(P)(candidate) == 0
    )
    numerator = denominator * unit
    if numerator not in O:
        raise AssertionError("the local numerator is not integral")
    denominator_coordinates = _order_integer_coordinates(src, La, O, denominator)
    numerator_coordinates = _order_integer_coordinates(src, La, O, numerator)
    element_coordinates = _order_integer_coordinates(src, La, O, element)
    denominator_residue = quotient["reduce_vector"](tuple(denominator_coordinates))
    numerator_residue = quotient["reduce_vector"](tuple(numerator_coordinates))
    denominator_inverse = src["quotient_inverse"](denominator_residue, quotient, table)
    residue = src["quotient_multiplication"](
        numerator_residue,
        denominator_inverse,
        quotient,
        table,
    )
    if quotient["reduce_one"](residue) == (0,) * 12:
        raise AssertionError("the exact local unit witness is not a unit")
    return {
        "prime_index": int(prime_index),
        "valuation": int(integer_valuation),
        "uniformizer_order_coordinates": _order_coordinates(src, La, O, uniformizer),
        "element_order_coordinates": element_coordinates,
        "denominator_order_coordinates": denominator_coordinates,
        "numerator_order_coordinates": numerator_coordinates,
        "unit_residue": list(map(int, residue)),
        "local_squareclass": [
            int(integer_valuation % 2),
            *map(int, src["unit_coordinates"](residue, coordinate_map)),
        ],
        "quotient_precision": int(quotient["precision_exponent"]),
    }


def _build_entry(src, La, O, prime_data, table, label, certificate):
    da, db = certificate["d"]
    t0 = certificate["point_t0"]
    t1 = certificate["point_t1"]
    d = [da, db]
    t0_squared = _gaussian_mul(t0, t0)
    t1_squared = _gaussian_mul(t1, t1)
    constant = _gaussian_sub(t0_squared, _gaussian_mul(d, t1_squared))
    linear = _gaussian_scale(t0, -2)
    u_coefficients = [constant, linear, [1, 0]]

    # The absolute local field has i=z^2-da because db=1 in all three rows.
    i_in_z = [-(da), 0, 1]
    t0_poly = _add([t0[0]], _poly_scale(i_in_z, t0[1]))
    t1_poly = _add([t1[0]], _poly_scale(i_in_z, t1[1]))
    t_poly = _add(t0_poly, _mul(t1_poly, [0, 1]))
    modulus = [da * da + db * db, 0, -2 * da, 0, 1]
    witness = certificate["witness_coefficients"]
    g_coefficients = [
        (-1, 0),
        (6, 14),
        (19, -40),
        (-52, -28),
        (-35, -8),
        (-2, -2),
        (1, 0),
    ]
    # Substitute i=z^2-da into g6, then t=t(z).
    g_in_z = [0]
    for exponent, coefficient in enumerate(g_coefficients):
        coefficient_poly = _add(
            [coefficient[0]], _poly_scale(i_in_z, coefficient[1])
        )
        g_in_z = _add(g_in_z, _mul(coefficient_poly, _pow(t_poly, exponent)))
    g_remainder = _reduce(g_in_z, modulus)
    error_remainder = _reduce(_sub(_mul(witness, witness), g_in_z), modulus)
    if error_remainder != certificate["expected_error_remainder"]:
        raise AssertionError(f"square witness changed for {label}")

    theta = La.gen()
    i_absolute = -src["load_ambient_elements"](La)["zeta4"]
    element = (
        La(constant[0])
        + La(constant[1]) * i_absolute
        + (La(linear[0]) + La(linear[1]) * i_absolute) * theta
        + theta**2
    )
    records = [
        _local_witness(src, La, O, index, P, int(e), table, element)
        for index, P, e, _ in prime_data
    ]
    return {
        "label": label,
        **certificate,
        "u_coefficients_ascending": u_coefficients,
        "t_polynomial_ascending": t_poly,
        "g_value_remainder": g_remainder,
        "element_order_coordinates": _order_integer_coordinates(src, La, O, element),
        "local_records": records,
    }


def main():
    src = runpy.run_path(str(Q3A2_SOURCE), run_name="q3a2_producer")
    La, O, prime_data = src["build_field"]()
    table = src["multiplication_table_from_order_data"](La, O)
    entries = [
        _build_entry(src, La, O, prime_data, table, label, certificate)
        for label, certificate in SQUARE_CERTIFICATES.items()
    ]
    payload = {
        "schema_version": "berry-c1-q3b-local-image-v1",
        "q3a2_schema": json.loads((DYADIC_TASK / "q3a2-dyadic-matrices-payload.json").read_text())["schema_version"],
        "entries": entries,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
