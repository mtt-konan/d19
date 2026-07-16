"""Tests for the exact Q3a3 D_inf local obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def test_q3a3_dinf_local_divisibility_obstruction() -> None:
    from scripts.theory.berry_sextic_q3a3_dinf import verify_certificate

    assert verify_certificate() == {
        "status": "ok",
        "outcome": "D_inf_not_in_2J_Q2_i",
        "terminal_residual": "z^2+z+1",
        "fake_kernel_contribution_dimension": 1,
    }
