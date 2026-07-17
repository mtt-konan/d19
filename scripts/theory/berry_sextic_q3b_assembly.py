"""Assemble the supported Berry Q3b fake-Selmer candidate.

The verifier consumes the accepted Q2c matrices and Q3a2 dyadic payload.  It
keeps the final dyadic local-image membership question explicit because Q3a3
certifies only the dimension of ``I_varpi`` and one image class, not a basis.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DYADIC_TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
Q3A2_PAYLOAD = DYADIC_TASK / "q3a2-dyadic-matrices-payload.json"

Vector = list[int]
Matrix = list[list[int]]


def _rank(rows: Matrix) -> int:
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


def _rref(rows: Matrix, width: int) -> tuple[Matrix, list[int]]:
    matrix = [[int(value) & 1 for value in row] for row in rows]
    pivot_row = 0
    pivots: list[int] = []
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix[:pivot_row], pivots


def _nullspace(rows: Matrix, width: int) -> Matrix:
    reduced, pivots = _rref(rows, width)
    free_columns = [column for column in range(width) if column not in pivots]
    basis: Matrix = []
    for free_column in free_columns:
        vector = [0] * width
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = reduced[row][free_column]
        basis.append(vector)
    return basis


def _transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix, strict=True)] if matrix else []


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right:
        return []
    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(len(right))) % 2
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum(left * right for left, right in zip(row, vector, strict=True)) % 2 for row in matrix
    ]


def _inverse(matrix: Matrix) -> Matrix:
    size = len(matrix)
    augmented = [
        row[:] + [int(row_index == column) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise ValueError("singular F2 matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        for row in range(size):
            if row != column and augmented[row][column]:
                augmented[row] = [
                    left ^ right
                    for left, right in zip(augmented[row], augmented[column], strict=True)
                ]
    return [row[size:] for row in augmented]


def _extend_basis(seed: Matrix, candidates: Matrix) -> Matrix:
    basis = [row[:] for row in seed]
    added: Matrix = []
    current_rank = _rank(basis)
    for candidate in candidates:
        if _rank([*basis, candidate]) > current_rank:
            basis.append(candidate[:])
            added.append(candidate[:])
            current_rank += 1
    return added


def _coordinate_extractor(basis_rows: Matrix) -> Matrix:
    """Return the inverse coordinate map on the span of the basis rows."""

    basis_columns = _transpose(basis_rows)
    selected: list[int] = []
    for row_index, row in enumerate(basis_columns):
        if _rank([basis_columns[index] for index in selected] + [row]) > len(selected):
            selected.append(row_index)
    if len(selected) != len(basis_rows):
        raise AssertionError("the H_varpi basis is not independent")
    square = [basis_columns[index] for index in selected]
    inverse = _inverse(square)
    extractor = [[0] * len(basis_columns) for _ in basis_rows]
    for output, inverse_row in enumerate(inverse):
        for position, row_index in enumerate(selected):
            extractor[output][row_index] = inverse_row[position]
    if _matmul(extractor, basis_columns) != [
        [int(row == column) for column in range(len(basis_rows))] for row in range(len(basis_rows))
    ]:
        raise AssertionError("failed to build H_varpi coordinate extractor")
    return extractor


def _extend_constants(constants: Matrix, candidate_basis: Matrix) -> Matrix:
    if _rank(constants) != len(constants):
        raise AssertionError("supported constants are not independent")
    return _extend_basis(constants, candidate_basis)


def _in_span(vector: Vector, basis: Matrix) -> bool:
    return _rank([*basis, vector]) == _rank(basis)


def _bits(vector: Vector) -> str:
    return "".join(str(value) for value in vector)


def _zero_matrix(rows: int, columns: int) -> Matrix:
    return [[0] * columns for _ in range(rows)]


def verify_assembly() -> dict[str, Any]:
    from scripts.theory import berry_sextic_q2c_maps as q2c
    from scripts.theory import berry_sextic_q3a3_exact_class as q3a3_class
    from scripts.theory import berry_sextic_q3a3_fake_kernel as q3a3_kernel
    from scripts.theory import berry_sextic_q3a_dyadic_matrices as q3a2

    q2c_certificate = q2c.build_certificate()
    assert q2c_certificate["status"] == "ok"
    q3a2_certificate = q3a2.verify_payload()
    assert q3a2_certificate["status"] == "ok"
    q3a3_class_certificate = q3a3_class.verify_payload()
    q3a3_kernel_certificate = q3a3_kernel.verify_exact_sequence()

    q3a2_payload = json.loads(Q3A2_PAYLOAD.read_text(encoding="utf-8"))
    labels = list(q2c.LABELS)
    ambient_dimension = len(labels)
    assert ambient_dimension == 16

    constants = [list(column) for column in q2c.M_CONST]
    norm_rows = [list(row) for row in q2c.M_NORM]
    local_h_rows = [list(row) for row in q2c_certificate["local_h_matrix_rows"]]
    odd_condition_rows = [*norm_rows, local_h_rows[0], local_h_rows[3]]

    # On the global norm kernel, I_pi is exactly h_varpi=h_u=0.
    candidate_basis = _nullspace(odd_condition_rows, ambient_dimension)
    assert _rank(odd_condition_rows) == 6
    assert len(candidate_basis) == 10
    assert all(_matvec(odd_condition_rows, vector) == [0] * 6 for vector in candidate_basis)
    assert all(_matvec(odd_condition_rows, vector) == [0] * 6 for vector in constants)
    assert all(_in_span(vector, candidate_basis) for vector in constants)
    odd_image_basis = [[0, 1, 1, 0], [0, 0, 1, 0]]
    assert all(
        _in_span(_matvec(local_h_rows, vector), odd_image_basis) for vector in candidate_basis
    )
    assert all(_matvec(local_h_rows, vector)[0] == 0 for vector in candidate_basis)
    assert all(_matvec(local_h_rows, vector)[3] == 0 for vector in candidate_basis)

    quotient_basis = _extend_constants(constants, candidate_basis)
    assert len(quotient_basis) == 6
    assert _rank(constants + quotient_basis) == 10

    dyadic_localization = q3a2_payload["ambient_localization_matrix_rows"]
    quotient_matrix = q3a2_payload["quotient_coordinate_matrix_rows"]
    norm_fake = q3a2_payload["norm_matrix_on_fake_quotient_rows"]
    h_basis_rows = q3a2_payload["norm_kernel_basis_quotient_rows"]
    assert _rank(q3a2_payload["global_norm_restriction_matrix"]) == 4
    assert _rank(norm_rows + q3a2_payload["global_norm_restriction_matrix"]) == 4

    quotient_localization = _matmul(quotient_matrix, dyadic_localization)
    quotient_basis_columns = _transpose(quotient_basis)
    localized_quotient_basis = _matmul(quotient_localization, quotient_basis_columns)
    assert _matmul(norm_fake, localized_quotient_basis) == _zero_matrix(4, 6)

    constant_columns = _transpose(constants)
    localized_constants = _matmul(quotient_localization, constant_columns)
    assert localized_constants == _zero_matrix(12, 4)

    h_coordinate_extractor = _coordinate_extractor(h_basis_rows)
    h_map = _matmul(h_coordinate_extractor, localized_quotient_basis)
    assert _matmul(_transpose(h_basis_rows), h_map) == localized_quotient_basis
    image_columns: Matrix = []
    for column in _transpose(h_map):
        if _rank([*image_columns, column]) > len(image_columns):
            image_columns.append(column)
    assert len(image_columns) == 6
    assert _rank(h_map) == 6
    kernel_basis = _nullspace(h_map, len(quotient_basis))
    assert kernel_basis == []

    h_d_i = list(q3a3_class_certificate["h_varpi_squareclass"])
    image_annihilator = _nullspace(image_columns, 8)
    assert len(image_annihilator) == 2
    known_projection = _matvec(image_annihilator, h_d_i)
    assert known_projection != [0, 0]
    assert not _in_span(h_d_i, image_columns)

    image_dimension = len(image_columns)
    local_image_dimension = q3a3_kernel_certificate["local_fake_image_dimension"]
    assert local_image_dimension == 4
    intersection_lower_bound = image_dimension + local_image_dimension - 8
    intersection_upper_bound = local_image_dimension - 1
    assert intersection_lower_bound == 2
    assert intersection_upper_bound == 3

    return {
        "status": "coordinate_blocker",
        "schema_version": "berry-c1-q3b-supported-fake-selmer-v1",
        "ambient_labels": labels,
        "odd_local_image_basis": ["0110", "0010"],
        "odd_condition_rows": odd_condition_rows,
        "odd_condition_rank": _rank(odd_condition_rows),
        "candidate_space_basis": candidate_basis,
        "candidate_space_dimension": len(candidate_basis),
        "constant_matrix_columns": constants,
        "constant_matrix_rank": _rank(constants),
        "supported_quotient_basis": quotient_basis,
        "supported_quotient_dimension": len(quotient_basis),
        "supported_quotient_labels": [
            "epsilon_1",
            "epsilon_2",
            "epsilon_3",
            "epsilon_4",
            "S_prime_5+S_prime_6",
            "S_prime_5+S_prime_8",
        ],
        "odd_h_coordinates_on_quotient_basis": [
            _matvec(local_h_rows, vector) for vector in quotient_basis
        ],
        "dyadic_h_map_rows": h_map,
        "dyadic_image_basis": image_columns,
        "dyadic_image_dimension": image_dimension,
        "dyadic_kernel_basis_in_quotient_coordinates": kernel_basis,
        "dyadic_kernel_dimension": len(kernel_basis),
        "dyadic_norm_rows_vanish": True,
        "constants_vanish_dyadically": True,
        "h_varpi_image_annihilator_rows": image_annihilator,
        "q3a3_local_image_dimension": local_image_dimension,
        "q3a3_known_class": h_d_i,
        "q3a3_known_class_in_supported_dyadic_image": False,
        "q3a3_known_class_projection_to_H_over_image": known_projection,
        "supported_intersection_dimension_bounds": [
            intersection_lower_bound,
            intersection_upper_bound,
        ],
        "remaining_membership_object": "I_varpi intersect W_supported",
        "i_varpi_coordinate_basis": None,
        "exact_intersection_computed": False,
    }


def main() -> int:
    result = verify_assembly()
    print(
        "q3b status={status} candidate_dim={candidate_space_dimension} "
        "quotient_dim={supported_quotient_dimension} dyadic_image_dim={dyadic_image_dimension} "
        "dyadic_kernel_dim={dyadic_kernel_dimension} I_dim={q3a3_local_image_dimension}".format(
            **result
        )
    )
    print(
        "q3b supported_image_basis="
        + ",".join(_bits(vector) for vector in result["dyadic_image_basis"])
    )
    print(
        "q3b remaining_intersection_dimension_bounds="
        + str(result["supported_intersection_dimension_bounds"])
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
