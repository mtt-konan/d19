"""Verify the exact-sequence hypotheses closing the Q3a3 fake kernel."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
Q3A2_PAYLOAD = TASK / "q3a2-dyadic-matrices-payload.json"
Q3A3_PAYLOAD = TASK / "q3a3-exact-class-payload.json"


def _rank(rows: list[list[int]]) -> int:
    matrix = [[value & 1 for value in row] for row in rows]
    if not matrix:
        return 0
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
    return pivot_row


def verify_exact_sequence() -> dict[str, object]:
    from scripts.theory.berry_sextic_q3a3_dinf import verify_certificate

    q3a2 = json.loads(Q3A2_PAYLOAD.read_text(encoding="utf-8"))
    q3a3 = json.loads(Q3A3_PAYLOAD.read_text(encoding="utf-8"))

    base_dimension = len(q3a2["base_squareclass_basis"])
    restriction = q3a2["product_basis_restriction_matrix"]
    restriction_rank = _rank(restriction)
    assert base_dimension == 4
    assert restriction_rank == q3a2["ranks"]["diagonal_image_rank"] == 4
    assert base_dimension - restriction_rank == 0

    absolute_factor_degrees = sorted(record["absolute_degree"] for record in q3a2["local_records"])
    relative_factor_degrees = [degree // 2 for degree in absolute_factor_degrees]
    assert absolute_factor_degrees == [4, 8]
    assert relative_factor_degrees == [2, 4]

    # R(K)=F_2^2 records the signs on E_2 and E_4.  Modulo the diagonal
    # sign, Q(K) has one generator; both relative degrees are even, so its
    # norm in mu_2(K)=F_2 is zero.
    sign_quotient_dimension = len(relative_factor_degrees) - 1
    sign_norm_row = [degree % 2 for degree in relative_factor_degrees]
    sign_norm_rank = _rank([sign_norm_row])
    assert sign_quotient_dimension == 1
    assert sign_norm_row == [0, 0]
    assert sign_norm_rank == 0
    cohomological_kernel_dimension = 1 - sign_norm_rank

    dinf = verify_certificate()
    assert dinf["outcome"] == "D_inf_not_in_2J_Q2_i"
    assert dinf["fake_kernel_contribution_dimension"] == 1

    source_dimension = q3a3["ranks"]["source_dimension"]
    kernel_dimension = cohomological_kernel_dimension
    image_dimension = source_dimension - kernel_dimension
    assert source_dimension == 5
    assert kernel_dimension == 1
    assert image_dimension == 4

    return {
        "status": "ok",
        "relative_factor_degrees": relative_factor_degrees,
        "constant_restriction_kernel_dimension": 0,
        "cohomological_fake_kernel_dimension": kernel_dimension,
        "kernel_generator": "D_inf",
        "local_fake_image_dimension": image_dimension,
    }


def main() -> int:
    result = verify_exact_sequence()
    print(
        "q3a3-kernel status={status} factors={relative_factor_degrees} "
        "kernel_dim={cohomological_fake_kernel_dimension} "
        "generator={kernel_generator} image_dim={local_fake_image_dimension}".format(**result)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
