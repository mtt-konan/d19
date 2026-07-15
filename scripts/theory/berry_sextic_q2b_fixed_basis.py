"""Parse and validate the public Magma Q2b fixed-basis S-unit payload.

The Magma transcript supplies the sixteen field elements.  The absolute
power-basis reduction data below are derived exactly from the emitted
defining polynomial, so no Magma object handle or maximal-order basis is
persisted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "berry-c1-q2b-fixed-basis-v1"
DEFAULT_PROXY = "http://127.0.0.1:7897"
DEFAULT_SOURCE = Path("scripts/theory/berry_sextic_magma_sunits.m")

# Coefficients are in ascending order for f12(a) = 0.
ABSOLUTE_POLYNOMIAL = (
    1,
    -12,
    194,
    -788,
    623,
    -376,
    2716,
    4184,
    1647,
    68,
    -62,
    -4,
    1,
)
REDUCTION_COEFFICIENTS = tuple(-coefficient for coefficient in ABSOLUTE_POLYNOMIAL[:12])
BASIS_SIZE = 12

S_UNIT_LABELS = (
    "zeta4",
    *(f"epsilon_{index}" for index in range(1, 6)),
    *(f"S_prime_{index}" for index in range(1, 11)),
)

# The selected relative polynomial is stored as pairs (constant, i) in K.
G6_COEFFICIENTS = (
    (-1, 0),
    (6, 14),
    (19, -40),
    (-52, -28),
    (-35, -8),
    (-2, -2),
    (1, 0),
)


def _fraction_token(token: str) -> Fraction:
    token = token.strip()
    if not token:
        raise ValueError("empty Magma coordinate")
    if "/" in token:
        numerator, denominator = token.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    return Fraction(int(token), 1)


def _encode_fraction(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def _decode_fraction(value: Any) -> Fraction:
    if isinstance(value, int):
        return Fraction(value, 1)
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"invalid rational coordinate: {value!r}")
    return Fraction(int(value[0]), int(value[1]))


def _encode_vector(vector: Iterable[Fraction]) -> list[list[int]]:
    return [_encode_fraction(value) for value in vector]


def decode_vector(vector: Iterable[Any]) -> list[Fraction]:
    values = [_decode_fraction(value) for value in vector]
    if len(values) != BASIS_SIZE:
        raise ValueError(f"expected {BASIS_SIZE} coordinates, got {len(values)}")
    return values


def _zero_vector() -> list[Fraction]:
    return [Fraction(0) for _ in range(BASIS_SIZE)]


def _add_vectors(left: Iterable[Fraction], right: Iterable[Fraction]) -> list[Fraction]:
    return [a + b for a, b in zip(left, right, strict=True)]


def _scale_vector(vector: Iterable[Fraction], scalar: Fraction) -> list[Fraction]:
    return [scalar * value for value in vector]


def _basis_power_vectors(maximum: int = 22) -> list[list[int]]:
    powers: list[list[int]] = []
    for exponent in range(maximum + 1):
        if exponent < BASIS_SIZE:
            vector = [0] * BASIS_SIZE
            vector[exponent] = 1
        else:
            vector = [0] * BASIS_SIZE
            for index, coefficient in enumerate(REDUCTION_COEFFICIENTS):
                previous = powers[exponent - BASIS_SIZE + index]
                for coordinate, value in enumerate(previous):
                    vector[coordinate] += coefficient * value
        powers.append(vector)
    return powers


def basis_product_table() -> list[list[list[int]]]:
    powers = _basis_power_vectors(2 * (BASIS_SIZE - 1))
    return [[powers[left + right] for right in range(BASIS_SIZE)] for left in range(BASIS_SIZE)]


def multiplication_by_generator_matrix() -> list[list[int]]:
    table = basis_product_table()
    column_vectors = [table[1][column] for column in range(BASIS_SIZE)]
    return [
        [column_vectors[column][row] for column in range(BASIS_SIZE)] for row in range(BASIS_SIZE)
    ]


def multiply_vectors(left: Iterable[Fraction], right: Iterable[Fraction]) -> list[Fraction]:
    left_values = list(left)
    right_values = list(right)
    if len(left_values) != BASIS_SIZE or len(right_values) != BASIS_SIZE:
        raise ValueError("absolute-field vectors must have length 12")
    table = basis_product_table()
    result = _zero_vector()
    for left_index, left_value in enumerate(left_values):
        for right_index, right_value in enumerate(right_values):
            result = _add_vectors(
                result,
                _scale_vector(
                    table[left_index][right_index],
                    left_value * right_value,
                ),
            )
    return result


def _power_vector(exponent: int) -> list[Fraction]:
    return [Fraction(value) for value in _basis_power_vectors(exponent)[exponent]]


def _relative_polynomial_value(i_vector: list[Fraction]) -> list[Fraction]:
    result = _zero_vector()
    for exponent, (constant, i_coefficient) in enumerate(G6_COEFFICIENTS):
        coefficient = _add_vectors(
            [Fraction(constant)] + [Fraction(0)] * (BASIS_SIZE - 1),
            _scale_vector(i_vector, Fraction(i_coefficient)),
        )
        result = _add_vectors(result, multiply_vectors(coefficient, _power_vector(exponent)))
    return result


def parse_sunit_lines(lines: Iterable[str]) -> dict[int, list[Fraction]]:
    transcript = "\n".join(lines)
    matches = list(
        re.finditer(
            r"BERRY_C1_SUNIT_BASIS\s+(\d+)\s+\[(.*?)\]",
            transcript,
            flags=re.DOTALL,
        )
    )
    if len(matches) != len(S_UNIT_LABELS):
        raise ValueError(f"expected 16 S-unit basis lines, got {len(matches)}")

    parsed: dict[int, list[Fraction]] = {}
    for match in matches:
        index = int(match.group(1))
        if index in parsed:
            raise ValueError(f"duplicate S-unit basis index {index}")
        tokens = [token for token in match.group(2).replace("\n", " ").split(",") if token.strip()]
        vector = [_fraction_token(token) for token in tokens]
        if len(vector) != BASIS_SIZE:
            raise ValueError(f"basis index {index} has {len(vector)} coordinates")
        parsed[index] = vector

    if sorted(parsed) != list(range(1, len(S_UNIT_LABELS) + 1)):
        raise ValueError("S-unit basis indices are not 1 through 16")
    return parsed


def parse_calculator_json(path: Path) -> tuple[dict[str, Any], dict[int, list[Fraction]]]:
    result = json.loads(path.read_text(encoding="utf-8"))
    if result.get("status") != "ok":
        raise ValueError(f"Magma calculator status is {result.get('status')!r}")
    lines = result.get("lines")
    if not isinstance(lines, list) or not all(isinstance(line, str) for line in lines):
        raise ValueError("calculator result has no line transcript")
    return result, parse_sunit_lines(lines)


def _source_metadata(source: Path) -> dict[str, Any]:
    contents = source.read_bytes()
    return {
        "path": source.as_posix(),
        "input_bytes": len(contents),
        "sha256": hashlib.sha256(contents).hexdigest(),
    }


def build_payload(
    result: dict[str, Any],
    coordinates: dict[int, list[Fraction]],
    *,
    source: Path = DEFAULT_SOURCE,
    proxy: str = DEFAULT_PROXY,
) -> dict[str, Any]:
    if len(coordinates) != len(S_UNIT_LABELS):
        raise ValueError("the fixed-basis payload must contain sixteen elements")

    zeta4 = coordinates[1]
    k_embedding_i = _scale_vector(zeta4, Fraction(-1))
    one = [Fraction(1)] + [Fraction(0)] * (BASIS_SIZE - 1)
    theta = [Fraction(0), Fraction(1)] + [Fraction(0)] * (BASIS_SIZE - 2)
    if multiply_vectors(k_embedding_i, k_embedding_i) != _scale_vector(one, Fraction(-1)):
        raise ValueError("the selected K embedding does not square to -1")
    if _relative_polynomial_value(k_embedding_i) != _zero_vector():
        raise ValueError("the selected K embedding does not make g6(theta) vanish")

    table = basis_product_table()
    matrix = multiplication_by_generator_matrix()
    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "calculator": "University of Sydney Magma Calculator",
            "proxy": proxy,
            "status": result["status"],
            "version": result.get("version"),
            "elapsed_seconds": result.get("elapsed_seconds"),
            "max_time": result.get("max_time"),
            "max_input": result.get("max_input"),
            "seed": result.get("seed"),
            "script": _source_metadata(source),
            "emission_marker": "BERRY_C1_SUNIT_BASIS",
            "emission_expression": "Eltseq(La!sunit_map(sunit_generators[j]))",
        },
        "field": {
            "base": "Q(i)",
            "absolute_degree": BASIS_SIZE,
            "absolute_defining_polynomial_ascending": list(ABSOLUTE_POLYNOMIAL),
            "basis": ["1", *(f"a^{index}" for index in range(1, BASIS_SIZE))],
            "basis_policy": "absolute power basis [1,a,...,a^11]",
            "relative_generator": {
                "symbol": "theta",
                "absolute_symbol": "a",
                "coordinates": _encode_vector(theta),
            },
            "k_embedding": {
                "symbol": "i",
                "coordinates": _encode_vector(k_embedding_i),
                "construction": "i = -zeta4; g6(a)=0 and i^2=-1",
            },
            "reduction": {
                "relation": "a^12 = sum_j reduction_coefficients[j]*a^j",
                "reduction_coefficients": list(REDUCTION_COEFFICIENTS),
                "basis_product_table": table,
                "basis_product_table_orientation": (
                    "basis_product_table[j][k][r] is the coefficient of a^r in a^j*a^k"
                ),
                "multiplication_by_a_matrix": matrix,
                "multiplication_by_a_matrix_orientation": (
                    "matrix[r][k] is the coefficient of a^r in a*a^k"
                ),
            },
        },
        "s_unit_group": {
            "invariants": [4, *(0 for _ in range(15))],
            "squareclass_basis": list(S_UNIT_LABELS),
            "relation_sequence": [4],
            "elements": [
                {
                    "index": index,
                    "label": S_UNIT_LABELS[index - 1],
                    "coordinates": _encode_vector(coordinates[index]),
                }
                for index in range(1, len(S_UNIT_LABELS) + 1)
            ],
        },
        "checks": {
            "basis_element_count": len(coordinates),
            "coordinate_length": BASIS_SIZE,
            "k_embedding_square": "-1",
            "relative_polynomial_at_theta": "0",
            "metadata_is_handle_free": True,
        },
    }


def validate_payload(payload: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        violations.append("schema_version")
    field = payload.get("field", {})
    if field.get("absolute_degree") != BASIS_SIZE:
        violations.append("absolute_degree")
    if field.get("basis_policy") != "absolute power basis [1,a,...,a^11]":
        violations.append("basis_policy")
    if len(field.get("reduction", {}).get("basis_product_table", [])) != BASIS_SIZE:
        violations.append("basis_product_table")
    elements = payload.get("s_unit_group", {}).get("elements", [])
    if len(elements) != len(S_UNIT_LABELS):
        violations.append("s_unit_element_count")
    if [element.get("label") for element in elements] != list(S_UNIT_LABELS):
        violations.append("s_unit_labels")
    for element in elements:
        try:
            decode_vector(element["coordinates"])
        except (KeyError, TypeError, ValueError):
            violations.append(f"coordinates_{element.get('index')}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--magma-json", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--proxy", default=DEFAULT_PROXY)
    args = parser.parse_args()

    result, coordinates = parse_calculator_json(args.magma_json)
    payload = build_payload(result, coordinates, source=args.source, proxy=args.proxy)
    violations = validate_payload(payload)
    if violations:
        raise SystemExit(f"invalid payload: {', '.join(violations)}")
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(coordinates)} fixed-basis S-unit elements to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
