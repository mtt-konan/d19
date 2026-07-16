"""Verify the exact Q3a dyadic completion and matrix certificate.

The Sage producer uses exact maximal-order ideals.  This verifier deliberately
uses only the serialized integer lattices, multiplication table, squareclass
witnesses, and F_2 matrices, so the certificate can be checked without a
local-factor or p-adic-factorization backend.
"""

from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
PAYLOAD = TASK / "q3a2-dyadic-matrices-payload.json"
Q2B_PAYLOAD = (
    ROOT
    / "docs/codex/tasks/berry-sextic-genus2-classification-20260715/q2b-fixed-basis-payload.json"
)

EXPECTED_LABELS = (
    "zeta4",
    *(f"epsilon_{index}" for index in range(1, 6)),
    *(f"S_prime_{index}" for index in range(1, 11)),
)


def _rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    matrix = [[int(value) & 1 for value in row] for row in rows]
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                matrix[row] = [
                    left ^ right for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def _matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    if not left or not right:
        return []
    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(len(right))) % 2
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def _transpose(columns: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*columns, strict=True)] if columns else []


def _reduce(vector: list[int] | tuple[int, ...], hnf: list[list[int]]) -> tuple[int, ...]:
    dimension = len(hnf)
    current = [int(value) for value in vector]
    diagonal = [int(hnf[index][index]) for index in range(dimension)]
    for index, modulus in enumerate(diagonal):
        quotient, remainder = divmod(current[index], modulus)
        current[index] = remainder
        for column in range(index + 1, dimension):
            current[column] -= quotient * int(hnf[index][column])
    if any(value < 0 or value >= diagonal[index] for index, value in enumerate(current)):
        raise AssertionError("HNF reduction did not produce a canonical residue")
    return tuple(current)


def _multiply(left: tuple[int, ...], right: tuple[int, ...], table: list[Any]) -> tuple[int, ...]:
    result = [0] * len(left)
    for left_index, left_value in enumerate(left):
        if left_value == 0:
            continue
        for right_index, right_value in enumerate(right):
            if right_value == 0:
                continue
            for coordinate, value in enumerate(table[left_index][right_index]):
                result[coordinate] += left_value * right_value * int(value)
    return tuple(result)


def _quotient_squareclass_check(
    record: dict[str, Any], table: list[Any], one: tuple[int, ...]
) -> None:
    quotient = record["quotient"]
    hnf = quotient["ideal_hnf"]
    prime_hnf = quotient["ideal_hnf_p"]
    diagonal = [int(value) for value in quotient["diagonal"]]
    expected_count = 1
    for value in diagonal:
        expected_count *= value
    assert expected_count == int(quotient["residue_count"])
    assert expected_count == 2 ** int(quotient["precision_exponent"])
    residues = list(product(*(range(value) for value in diagonal)))
    assert len(residues) == expected_count
    zero = (0,) * 12
    one_residue = _reduce(one, hnf)
    units = [residue for residue in residues if _reduce(residue, prime_hnf) != zero]
    square_set = {_reduce(_multiply(residue, residue, table), hnf) for residue in units}
    assert len(square_set) == int(record["unit_square_count"])
    assert one_residue in square_set

    basis = [tuple(int(value) for value in row) for row in record["unit_basis_order_coordinates"]]
    assert len(basis) == int(record["absolute_degree"]) + 1
    for generator in basis:
        assert generator in residues
        assert _reduce(generator, prime_hnf) != zero

    coordinate_map: dict[tuple[int, ...], tuple[int, ...]] = {}
    for bits in product((0, 1), repeat=len(basis)):
        representative = one_residue
        for bit, generator in zip(bits, basis, strict=True):
            if bit:
                representative = _reduce(_multiply(representative, generator, table), hnf)
        for square in square_set:
            value = _reduce(_multiply(representative, square, table), hnf)
            previous = coordinate_map.setdefault(value, bits)
            assert previous == bits
    assert len(coordinate_map) == len(units)
    record["_coordinate_map"] = coordinate_map
    record["_square_set"] = square_set


def _squareclass_from_witness(
    witness: dict[str, Any], record: dict[str, Any], table: list[Any]
) -> list[int]:
    hnf = record["quotient"]["ideal_hnf"]
    residue = tuple(int(value) for value in witness["unit_residue"])
    residue = _reduce(residue, hnf)
    assert residue in record["_coordinate_map"]
    return [int(witness["valuation"]) & 1, *record["_coordinate_map"][residue]]


def _gaussian_reduce(vector: tuple[int, int], hnf: list[list[int]]) -> tuple[int, int]:
    return _reduce(vector, hnf)  # the generic HNF reducer also handles dimension two


def _gaussian_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0])


def _check_base_squareclass_certificate(payload: dict[str, Any]) -> None:
    certificate = payload["base_squareclass_local_certificate"]
    hnf = certificate["ideal_hnf"]
    prime_hnf = certificate["prime_hnf"]
    diagonal = [int(hnf[index][index]) for index in range(2)]
    residues = list(product(*(range(value) for value in diagonal)))
    units = [residue for residue in residues if _gaussian_reduce(residue, prime_hnf) != (0, 0)]
    square_set = {_gaussian_reduce(_gaussian_multiply(residue, residue), hnf) for residue in units}
    assert len(residues) == certificate["residue_count"] == 32
    assert len(units) == 16
    assert len(square_set) == certificate["unit_square_count"] == 2
    unit_basis = [tuple(row) for row in certificate["representatives"][1:]]
    unit_cosets: dict[tuple[int, int], tuple[int, ...]] = {}
    for bits in product((0, 1), repeat=3):
        representative = (1, 0)
        for bit, generator in zip(bits, unit_basis, strict=True):
            if bit:
                representative = _gaussian_multiply(representative, generator)
        for square in square_set:
            value = _gaussian_reduce(_gaussian_multiply(representative, square), hnf)
            previous = unit_cosets.setdefault(value, bits)
            assert previous == bits
    assert len(unit_cosets) == len(units)
    assert tuple(certificate["representatives"][0]) == (1, 1)


def _check_matrix_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    labels = payload["ambient_labels"]
    assert labels == list(EXPECTED_LABELS)
    B = payload["product_basis_restriction_matrix"]
    N = payload["norm_matrix_rows"]
    Lambda = payload["ambient_localization_matrix_rows"]
    global_norm = payload["global_norm_restriction_matrix"]
    assert len(B) == len(N[0]) == len(Lambda) == 16
    assert len(B[0]) == len(global_norm) == 4
    assert _rank(B) == 4
    assert _rank(N) == 4
    assert _matmul(N, B) == [[0] * 4 for _ in range(4)]
    assert _matmul(N, Lambda) == global_norm
    assert _rank(Lambda) == 16

    quotient = payload["quotient_coordinate_matrix_rows"]
    complement_indices = payload["quotient_complement_standard_indices"]
    assert len(quotient) == 12 and len(quotient[0]) == 16
    assert len(complement_indices) == 12
    # The complement is standard-coordinate columns, so its row matrix is
    # obtained directly by placing those columns in their selected positions.
    complement_matrix = [[0] * 12 for _ in range(16)]
    for column, row in enumerate(complement_indices):
        complement_matrix[row][column] = 1
    assert _matmul(quotient, B) == [[0] * 4 for _ in range(12)]
    assert _matmul(quotient, complement_matrix) == [
        [int(row == column) for column in range(12)] for row in range(12)
    ]
    norm_fake = payload["norm_matrix_on_fake_quotient_rows"]
    assert norm_fake == _matmul(N, complement_matrix)
    assert _rank(norm_fake) == 4
    kernel_rows = payload["norm_kernel_basis_quotient_rows"]
    assert len(kernel_rows) == 8 and len(kernel_rows[0]) == 12
    assert _matmul(norm_fake, _transpose(kernel_rows)) == [[0] * 8 for _ in range(4)]
    assert _rank(kernel_rows) == 8
    lifts = payload["norm_kernel_basis_product_lifts_columns"]
    assert len(lifts) == 16 and len(lifts[0]) == 8
    assert _matmul(N, lifts) == [[0] * 8 for _ in range(4)]
    assert _matmul(quotient, lifts) == _transpose(kernel_rows)

    ranks = payload["ranks"]
    assert ranks == {
        "ambient_localization_rank": 16,
        "diagonal_image_rank": 4,
        "fake_localization_rank": 12,
        "fake_norm_kernel_dimension": 8,
        "fake_quotient_dimension": 12,
        "norm_on_fake_quotient_rank": 4,
        "product_norm_rank": 4,
        "product_squareclass_dimension": 16,
    }
    return ranks


def verify_payload(path: Path = PAYLOAD) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    labels = payload["ambient_labels"]
    assert payload["schema_version"] == "berry-c1-q3a2-dyadic-matrices-v1"
    field = payload["field"]
    assert field["absolute_degree"] == 12
    assert field["maximal_order_discriminant"] == 5019340374016
    assert len(field["order_basis_power_coordinates"]) == 12
    assert all(len(row) == 12 for row in field["order_basis_power_coordinates"])
    assert len(field["order_one_coordinates"]) == 12
    assert payload["dyadic_factorization"]["ramification_exponents"] == [4, 8]
    assert payload["dyadic_factorization"]["residue_degrees"] == [1, 1]
    assert field["embedding_checks"]["i_squared"] == field["embedding_checks"]["minus_one"]
    assert all(value == [0, 1] for value in field["embedding_checks"]["relative_polynomial_at_a"])
    assert payload["product_squareclass_basis"] == [
        "factor_1_uniformizer",
        *(f"factor_1_unit_{index}" for index in range(1, 6)),
        "factor_2_uniformizer",
        *(f"factor_2_unit_{index}" for index in range(1, 10)),
    ]
    assert payload["relative_basis"]["change_of_basis_determinant"] == [-1, 2**34]
    assert payload["q2b_payload_sha256"] == hashlib.sha256(Q2B_PAYLOAD.read_bytes()).hexdigest()

    table = payload["order_multiplication_table"]
    assert len(table) == 12 and all(len(row) == 12 for row in table)
    one = tuple(int(value) for value in field["order_one_coordinates"])
    for record in payload["local_records"]:
        assert record["absolute_degree"] == record["ramification_index"] * record["residue_degree"]
        assert record["residue_degree"] == 1
        _quotient_squareclass_check(record, table, one)
        for label in EXPECTED_LABELS:
            witness = record["ambient_local_unit_residue_witnesses"][label]
            assert record["ambient_local_squareclass_columns"][label] == _squareclass_from_witness(
                witness, record, table
            )
        for label in payload["base_squareclass_basis"]:
            witness = record["base_local_unit_residue_witnesses"][label]
            assert record["base_squareclass_columns"][label] == _squareclass_from_witness(
                witness, record, table
            )

    for label in EXPECTED_LABELS:
        columns = [
            record["ambient_local_squareclass_columns"][label]
            for record in payload["local_records"]
        ]
        assert payload["product_localization_columns"][label] == [
            value for column in columns for value in column
        ]
    for label in payload["base_squareclass_basis"]:
        columns = [record["base_squareclass_columns"][label] for record in payload["local_records"]]
        assert payload["base_restriction_columns"][label] == [
            value for column in columns for value in column
        ]
    assert payload["product_basis_restriction_matrix"] == _transpose(
        [payload["base_restriction_columns"][label] for label in payload["base_squareclass_basis"]]
    )
    assert payload["norm_basis_squareclass_columns"] == [
        column["squareclass"]
        for record in payload["local_records"]
        for column in record["basis_norm_squareclass_columns"]
    ]
    assert payload["norm_matrix_rows"] == _transpose(payload["norm_basis_squareclass_columns"])
    _check_base_squareclass_certificate(payload)
    ranks = _check_matrix_certificate(payload)
    return {
        "status": "ok",
        "ranks": ranks,
        "local_factor_degrees": [record["absolute_degree"] for record in payload["local_records"]],
        "ambient_labels": labels,
    }


def main() -> int:
    certificate = verify_payload()
    print(
        "q3a2 dyadic status={status} factors={local_factor_degrees} "
        "B_rank={diagonal_image_rank} N_rank={product_norm_rank} "
        "F_dim={fake_quotient_dimension} H_dim={fake_norm_kernel_dimension}".format(
            **certificate,
            **certificate["ranks"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
