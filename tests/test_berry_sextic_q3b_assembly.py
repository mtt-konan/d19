"""Focused exact checks for the Berry Q3b supported assembly."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def _result():
    from scripts.theory.berry_sextic_q3b_assembly import verify_assembly

    return verify_assembly()


def _bits(v: list[int]) -> str:
    return "".join(map(str, v))


def test_q3b_global_candidate_and_constant_quotient_are_exact() -> None:
    result = _result()

    assert result["status"] == "coordinate_blocker"
    assert result["odd_condition_rank"] == 6
    assert result["candidate_space_dimension"] == 10
    assert result["constant_matrix_rank"] == 4
    assert result["supported_quotient_dimension"] == 6
    assert all(
        not any(
            sum(row[column] * vector[column] for column in range(16)) % 2
            for row in result["odd_condition_rows"]
        )
        for vector in result["constant_matrix_columns"]
    )
    assert [_bits(vector) for vector in result["supported_quotient_basis"]] == [
        "0100000000000000",
        "0010000000000000",
        "0001000000000000",
        "0000100000000000",
        "0000000000110000",
        "0000000000100100",
    ]
    assert result["odd_h_coordinates_on_quotient_basis"] == [
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
    ]


def test_q3b_dyadic_image_is_explicit_but_I_varpi_membership_is_not() -> None:
    result = _result()

    assert result["dyadic_image_dimension"] == 6
    assert [_bits(vector) for vector in result["dyadic_image_basis"]] == [
        "00011010",
        "11000001",
        "01101001",
        "10100011",
        "11000000",
        "00101000",
    ]
    assert result["dyadic_kernel_dimension"] == 0
    assert result["dyadic_kernel_basis_in_quotient_coordinates"] == []
    assert result["dyadic_norm_rows_vanish"] is True
    assert result["constants_vanish_dyadically"] is True
    assert result["h_varpi_image_annihilator_rows"] == [
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
    ]
    assert result["q3a3_local_image_dimension"] == 4
    assert result["q3a3_known_class"] == [0, 1, 1, 1, 0, 1, 1, 0]
    assert result["q3a3_known_class_in_supported_dyadic_image"] is False
    assert result["q3a3_known_class_projection_to_H_over_image"] == [1, 0]
    assert result["supported_intersection_dimension_bounds"] == [2, 3]
    assert result["i_varpi_coordinate_basis"] is None
    assert result["exact_intersection_computed"] is False
