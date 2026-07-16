"""Tests for the Q3a3 fake-kernel exact-sequence certificate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def test_q3a3_fake_kernel_exact_sequence() -> None:
    from scripts.theory.berry_sextic_q3a3_fake_kernel import verify_exact_sequence

    assert verify_exact_sequence() == {
        "status": "ok",
        "relative_factor_degrees": [2, 4],
        "constant_restriction_kernel_dimension": 0,
        "cohomological_fake_kernel_dimension": 1,
        "kernel_generator": "D_inf",
        "local_fake_image_dimension": 4,
    }
