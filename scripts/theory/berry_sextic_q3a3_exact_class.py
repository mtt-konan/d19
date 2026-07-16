"""Verify the serialized exact Q3a3 local class in frozen Q3a2 coordinates."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

TASK = ROOT / "docs/codex/tasks/berry-q3a-dyadic-kernel-20260715"
PAYLOAD = TASK / "q3a3-exact-class-payload.json"


def _q3a2_module():
    from scripts.theory import berry_sextic_q3a_dyadic_matrices

    return berry_sextic_q3a_dyadic_matrices


def verify_payload(path: Path = PAYLOAD) -> dict[str, object]:
    q3a2_module = _q3a2_module()
    payload = json.loads(path.read_text(encoding="utf-8"))
    q3a2 = json.loads(q3a2_module.PAYLOAD.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "berry-c1-q3a3-exact-class-v1"
    assert payload["q3a2_schema"] == q3a2["schema_version"]
    assert payload["g6_i"] == [11, 12]
    assert payload["product_squareclass"] == [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    assert payload["fake_quotient_squareclass"] == [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0]
    assert payload["norm_squareclass"] == [0, 0, 0, 0]
    assert payload["h_varpi_squareclass"] == [0, 1, 1, 1, 0, 1, 1, 0]

    table = q3a2["order_multiplication_table"]
    one = tuple(q3a2["field"]["order_one_coordinates"])
    reconstructed = []
    for witness, record in zip(payload["local_records"], q3a2["local_records"], strict=True):
        q3a2_module._quotient_squareclass_check(record, table, one)
        residue = tuple(witness["unit_residue"])
        residue = q3a2_module._reduce(residue, record["quotient"]["ideal_hnf"])
        bits = record["_coordinate_map"][residue]
        local_vector = [witness["valuation"] % 2, *bits]
        assert local_vector == witness["local_squareclass"]
        reconstructed.extend(local_vector)
    assert reconstructed == payload["product_squareclass"]

    quotient_matrix = q3a2["quotient_coordinate_matrix_rows"]
    assert q3a2_module._matmul(quotient_matrix, [[bit] for bit in reconstructed]) == [
        [bit] for bit in payload["fake_quotient_squareclass"]
    ]
    norm_matrix = q3a2["norm_matrix_on_fake_quotient_rows"]
    assert q3a2_module._matmul(
        norm_matrix, [[bit] for bit in payload["fake_quotient_squareclass"]]
    ) == [
        [0],
        [0],
        [0],
        [0],
    ]
    kernel_rows = q3a2["norm_kernel_basis_quotient_rows"]
    assert [
        sum(
            payload["h_varpi_squareclass"][column] * kernel_rows[column][row] for column in range(8)
        )
        % 2
        for row in range(12)
    ] == payload["fake_quotient_squareclass"]

    gaussian = q3a2["base_squareclass_local_certificate"]
    witness = tuple(payload["principal_unit_square_witness_mod_lambda5"])
    square = (
        witness[0] * witness[0] - witness[1] * witness[1],
        2 * witness[0] * witness[1],
    )
    assert q3a2_module._reduce(square, gaussian["ideal_hnf"]) == tuple(
        payload["principal_unit_mod_lambda5"]
    )
    assert any(payload["h_varpi_squareclass"])
    return {
        "status": "ok",
        "image_lower_bound": 1,
        "h_varpi_squareclass": payload["h_varpi_squareclass"],
    }


def main() -> int:
    result = verify_payload()
    print(
        "q3a3 exact-class status={status} image_lower_bound={image_lower_bound} H={h}".format(
            **result, h="".join(map(str, result["h_varpi_squareclass"]))
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
