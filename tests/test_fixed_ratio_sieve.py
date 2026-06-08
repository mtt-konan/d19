from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def test_fixed_ratio_allowed_n_mod_matches_direct_square_conditions() -> None:
    from rational_distance.concordant.fixed_ratio_sieve import fixed_ratio_allowed_n_mod

    assert fixed_ratio_allowed_n_mod(k=2, b=1, modulus=5) == frozenset({0})


def test_universal_zero_b_witness_is_primitive_and_valid() -> None:
    from rational_distance.concordant.fixed_ratio_sieve import (
        is_fixed_ratio_witness,
        universal_zero_b_witness,
    )

    witness = universal_zero_b_witness(k=7, modulus=25)

    assert witness.b == 0
    assert witness.n1 == 1
    assert witness.n2 == 24
    assert witness.relation == "sum=A+B"
    assert witness.primitive_gcd_mod == 1
    assert is_fixed_ratio_witness(k=7, modulus=25, witness=witness)


def test_fixed_ratio_modulus_certificate_reports_local_survivor_not_kill() -> None:
    from rational_distance.concordant.fixed_ratio_sieve import certify_fixed_ratio_modulus

    certificate = certify_fixed_ratio_modulus(k=2, modulus=9)

    assert certificate.k == 2
    assert certificate.modulus == 9
    assert certificate.status == "local_survives"
    assert certificate.primitive_witness_count > 0
    assert certificate.universal_witness is not None
    assert certificate.universal_witness.primitive_gcd_mod == 1


def test_fixed_ratio_mod_sieve_has_no_killer_modulus_because_universal_witness_survives() -> None:
    from rational_distance.concordant.fixed_ratio_sieve import find_fixed_ratio_killer_modulus

    moduli = (9, 25, 49, 121)

    for k in range(1, 8):
        assert find_fixed_ratio_killer_modulus(k, moduli) is None


def test_universal_witness_survives_any_finite_modulus_package() -> None:
    from math import lcm

    from rational_distance.concordant.fixed_ratio_sieve import (
        is_fixed_ratio_witness,
        universal_zero_b_witness,
    )

    combined_modulus = lcm(9, 25, 49, 121)
    witness = universal_zero_b_witness(k=11, modulus=combined_modulus)

    assert witness.primitive_gcd_mod == 1
    assert is_fixed_ratio_witness(k=11, modulus=combined_modulus, witness=witness)
