"""Exact parser and reusable-basis checks for the Berry Q2b payload."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

ROOT = Path(__file__).parents[1]
TASK = ROOT / "docs/codex/tasks/berry-sextic-genus2-classification-20260715"
TRANSCRIPT = TASK / "q2b-fixed-basis-magma-result.json"
PAYLOAD = TASK / "q2b-fixed-basis-payload.json"


def _module():
    from scripts.theory import berry_sextic_q2b_fixed_basis as q2b

    return q2b


def _zero() -> list[Fraction]:
    q2b = _module()
    return [Fraction(0)] * q2b.BASIS_SIZE


def _one() -> list[Fraction]:
    q2b = _module()
    return [Fraction(1)] + [Fraction(0)] * (q2b.BASIS_SIZE - 1)


def test_parser_reads_all_sixteen_emitted_elements() -> None:
    q2b = _module()
    result, coordinates = q2b.parse_calculator_json(TRANSCRIPT)

    assert result["status"] == "ok"
    assert result["version"] == "2.29-8"
    assert result["elapsed_seconds"] == 0.78
    assert len(coordinates) == 16
    assert all(len(vector) == q2b.BASIS_SIZE for vector in coordinates.values())
    assert coordinates[1][0] == Fraction(-1817, 2048)
    assert coordinates[16][-1] == Fraction(2145, 2048)


def test_payload_preserves_transcript_coordinates_and_labels() -> None:
    q2b = _module()
    _result, coordinates = q2b.parse_calculator_json(TRANSCRIPT)
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))

    assert q2b.validate_payload(payload) == []
    assert payload["source"]["script"]["input_bytes"] == 1557
    assert payload["source"]["script"]["sha256"] == (
        "771d9f203975a5aad72eadf9b086360f5cae036c57a687f156395c373ac7e67e"
    )
    assert [item["label"] for item in payload["s_unit_group"]["elements"]] == list(
        q2b.S_UNIT_LABELS
    )
    for index, vector in coordinates.items():
        expected = [[value.numerator, value.denominator] for value in vector]
        assert payload["s_unit_group"]["elements"][index - 1]["coordinates"] == expected


def test_reduction_table_and_k_embedding_are_exactly_reusable() -> None:
    q2b = _module()
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    reduction = payload["field"]["reduction"]
    table = reduction["basis_product_table"]

    assert table == q2b.basis_product_table()
    assert reduction["basis_product_table_orientation"].startswith("basis_product_table[j][k][r]")
    assert reduction["multiplication_by_a_matrix"] == q2b.multiplication_by_generator_matrix()
    assert reduction["multiplication_by_a_matrix_orientation"].startswith("matrix[r][k]")

    zeta4 = q2b.decode_vector(payload["s_unit_group"]["elements"][0]["coordinates"])
    embedded_i = q2b.decode_vector(payload["field"]["k_embedding"]["coordinates"])
    assert q2b.multiply_vectors(zeta4, zeta4) == _scale(_one(), -1)
    assert q2b.multiply_vectors(embedded_i, embedded_i) == _scale(_one(), -1)
    assert q2b._relative_polynomial_value(embedded_i) == _zero()

    theta_times_a11 = table[1][11]
    assert theta_times_a11 == reduction["reduction_coefficients"]


def _scale(vector: list[Fraction], scalar: int) -> list[Fraction]:
    return [scalar * value for value in vector]
