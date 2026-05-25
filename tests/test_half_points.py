"""Tests for multi-N half-point analysis helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.half_points import enumerate_half_points_for_concordant_N


def test_enumerate_half_points_for_known_multi_n_pair() -> None:
    halves = enumerate_half_points_for_concordant_N(153, 560, 204)

    assert len(halves) == 8
    assert (19992, -17013192) in [(point.x, point.y) for point in halves]
