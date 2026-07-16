from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def test_q3a3_exact_local_class_certificate() -> None:
    from scripts.theory.berry_sextic_q3a3_exact_class import verify_payload

    assert verify_payload() == {
        "status": "ok",
        "image_lower_bound": 1,
        "h_varpi_squareclass": [0, 1, 1, 1, 0, 1, 1, 0],
    }
