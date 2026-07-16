#!/usr/bin/env sage
"""Generate the exact Q3a3 certificate for the local point above t=i."""

import json
import runpy
from pathlib import Path

from sage.all import QQ

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
Q3A2_SOURCE = ROOT / "scripts/theory/berry_sextic_q3a_dyadic_matrices.sage"
Q3A2_PAYLOAD = TASK / "q3a2-dyadic-matrices-payload.json"
OUT = TASK / "q3a3-exact-class-payload.json"


def solve_kernel_coordinates(library, kernel_rows, target):
    equations = [
        [kernel_rows[column][row] for column in range(len(kernel_rows))] + [target[row]]
        for row in range(len(target))
    ]
    reduced, pivots = library["f2_rref"](equations)
    result = [0] * len(kernel_rows)
    for row, pivot in enumerate(pivots):
        if pivot < len(result):
            result[pivot] = reduced[row][-1]
    if any(
        sum(kernel_rows[column][row] * result[column] for column in range(len(result))) % 2
        != target[row]
        for row in range(len(target))
    ):
        raise AssertionError("the fake class is not in the accepted H_varpi basis")
    return result


def main():
    library = runpy.run_path(str(Q3A2_SOURCE), run_name="q3a2_library")
    accepted = json.loads(Q3A2_PAYLOAD.read_text(encoding="utf-8"))
    La, O, prime_data = library["build_field"]()
    table = library["multiplication_table_from_order_data"](La, O)
    ambient = library["load_ambient_elements"](La)
    i_absolute = -ambient["zeta4"]
    theta = La.gen()
    alpha = i_absolute - theta

    records = []
    product_vector = []
    for index, P, e, f in prime_data:
        quotient = library["quotient_data"](La, O, P, e)
        quotient["local_degree"] = int(e * f)
        _, _, coordinate_map = library["unit_squareclasses"](quotient, table)
        valuation, residue = library["local_unit_residue"](
            La, O, P, e, alpha, La.uniformizer(P), quotient, table
        )
        local_vector = [
            int(valuation % 2),
            *map(int, library["unit_coordinates"](residue, coordinate_map)),
        ]
        product_vector.extend(local_vector)
        records.append(
            {
                "index": int(index),
                "valuation": int(valuation),
                "unit_residue": list(residue),
                "local_squareclass": local_vector,
            }
        )

    quotient_matrix = accepted["quotient_coordinate_matrix_rows"]
    fake_vector = [
        sum(quotient_matrix[row][column] * product_vector[column] for column in range(16)) % 2
        for row in range(12)
    ]
    norm_matrix = accepted["norm_matrix_on_fake_quotient_rows"]
    norm_vector = [
        sum(norm_matrix[row][column] * fake_vector[column] for column in range(12)) % 2
        for row in range(4)
    ]
    h_vector = solve_kernel_coordinates(
        library, accepted["norm_kernel_basis_quotient_rows"], fake_vector
    )

    gaussian = library["gaussian_quotient"]()
    principal_unit = (-11, -12)  # 1-12*(1+i)
    target = gaussian["reduce"](principal_unit)
    square_witness = next(
        residue
        for residue in gaussian["coordinate_map"]
        if gaussian["reduce"](library["pair_mul"](residue, residue)) == target
    )

    g_i = La(11) + La(12) * i_absolute
    identity_rhs = (i_absolute - 1) ** 6 * g_i
    coefficients = (
        -1,
        6 + 14 * i_absolute,
        19 - 40 * i_absolute,
        -52 - 28 * i_absolute,
        -35 - 8 * i_absolute,
        -2 - 2 * i_absolute,
        1,
    )
    identity_lhs = sum(coefficients[index] * i_absolute**index for index in range(7))
    if identity_lhs != identity_rhs:
        raise AssertionError("the exact g6(i) factorization changed")

    payload = {
        "schema_version": "berry-c1-q3a3-exact-class-v1",
        "point_parameter": "i",
        "evaluation_element": "i-theta",
        "g6_i": [11, 12],
        "factorization": "g6(i)=(i-1)^6*(11+12*i)=(i-1)^6*(-1)*(1-12*(1+i))",
        "principal_unit": list(principal_unit),
        "principal_unit_mod_lambda5": list(target),
        "principal_unit_square_witness_mod_lambda5": list(square_witness),
        "local_records": records,
        "product_squareclass": product_vector,
        "fake_quotient_squareclass": fake_vector,
        "norm_squareclass": norm_vector,
        "h_varpi_squareclass": h_vector,
        "ranks": {"certified_image_lower_bound": 1, "source_dimension": 5},
        "q3a2_schema": accepted["schema_version"],
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
