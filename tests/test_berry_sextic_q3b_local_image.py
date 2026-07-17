from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def test_q3b_exact_local_image() -> None:
    from scripts.theory.berry_sextic_q3b_local_image import verify_local_image

    assert verify_local_image() == {
        "status": "ok",
        "local_image_dimension": 4,
        "image_basis": ["01110110", "01111000", "00001100", "00011000"],
        "image_basis_rank": 4,
        "intersection_dimension": 2,
        "intersection_basis": ["01111000", "01100010"],
        "kernel_generator": "D_inf",
        "membership_evidence": "three quadratic local divisors plus frozen D_i",
    }


def test_q3b_localization_rejects_a_rescaled_uniformizer() -> None:
    from scripts.theory import berry_sextic_q3b_local_image as local_image

    q3a2_payload = json.loads(local_image.Q3A2_PAYLOAD.read_text(encoding="utf-8"))
    payload = json.loads(local_image.PAYLOAD.read_text(encoding="utf-8"))
    entry = copy.deepcopy(payload["entries"][0])
    witness = entry["local_records"][0]
    table = q3a2_payload["order_multiplication_table"]
    uniformizer = [
        Fraction(numerator, denominator)
        for numerator, denominator in witness["uniformizer_order_coordinates"]
    ]
    uniformizer_cubed = local_image._fraction_multiply(
        local_image._fraction_multiply(uniformizer, uniformizer, table),
        uniformizer,
        table,
    )
    assert all(value.denominator == 1 for value in uniformizer_cubed)
    witness["uniformizer_order_coordinates"] = [[int(value), 1] for value in uniformizer_cubed]
    witness["valuation"] //= 3

    records = local_image._prepare_local_records(q3a2_payload)
    with pytest.raises(AssertionError):
        local_image._verify_localization(entry, q3a2_payload, records)
