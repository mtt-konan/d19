from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def test_exact_dyadic_matrix_certificate() -> None:
    from scripts.theory.berry_sextic_q3a_dyadic_matrices import verify_payload

    certificate = verify_payload()

    assert certificate == {
        "status": "ok",
        "ranks": {
            "ambient_localization_rank": 16,
            "diagonal_image_rank": 4,
            "fake_localization_rank": 12,
            "fake_norm_kernel_dimension": 8,
            "fake_quotient_dimension": 12,
            "norm_on_fake_quotient_rank": 4,
            "product_norm_rank": 4,
            "product_squareclass_dimension": 16,
        },
        "local_factor_degrees": [4, 8],
        "ambient_labels": [
            "zeta4",
            "epsilon_1",
            "epsilon_2",
            "epsilon_3",
            "epsilon_4",
            "epsilon_5",
            "S_prime_1",
            "S_prime_2",
            "S_prime_3",
            "S_prime_4",
            "S_prime_5",
            "S_prime_6",
            "S_prime_7",
            "S_prime_8",
            "S_prime_9",
            "S_prime_10",
        ],
    }
