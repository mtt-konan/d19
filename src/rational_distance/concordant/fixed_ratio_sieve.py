"""Fixed-ratio ``A = kB`` modular certificates.

This module deliberately has a negative conclusion: the existing pure
congruence sieve cannot prove the whole fixed-ratio branch impossible.

For any fixed integer ``k`` and any modulus ``M >= 2``, the residue class

    B ≡ 0,  N1 ≡ 1,  N2 ≡ -1  (mod M)

passes both Pythagorean-leg congruences and the full-plane sum relation
``N1 + N2 ≡ A + B``. It is also primitive modulo ``M``. Therefore a finite
modulus certificate of the form "no primitive residue classes survive" can
never exist for this branch without adding non-congruence information.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from rational_distance.concordant.chain_closure_sieve import squares_mod

REL_SUM_AB = "sum=A+B"
REL_SUM_DIFF = "sum=|A-B|"
REL_DIFF_AB = "diff=A+B"
REL_DIFF_DIFF = "diff=|A-B|"
FULL_PLANE_RELATIONS: tuple[str, ...] = (
    REL_SUM_AB,
    REL_SUM_DIFF,
    REL_DIFF_AB,
    REL_DIFF_DIFF,
)


@dataclass(frozen=True)
class FixedRatioWitness:
    """A residue-level witness for the fixed-ratio full-plane conditions."""

    b: int
    n1: int
    n2: int
    relation: str
    primitive_gcd_mod: int


@dataclass(frozen=True)
class FixedRatioModCertificate:
    """Result of testing one ``A = kB`` branch modulo one modulus."""

    k: int
    modulus: int
    status: str
    total_witness_count: int
    primitive_witness_count: int
    universal_witness: FixedRatioWitness | None
    sample_primitive_witnesses: tuple[FixedRatioWitness, ...]


def _validate_inputs(k: int, modulus: int) -> None:
    if k < 1:
        raise ValueError("k must be a positive integer")
    if modulus < 2:
        raise ValueError("modulus must be at least 2")


def _primitive_gcd_mod(b: int, n1: int, n2: int, modulus: int) -> int:
    return gcd(gcd(gcd(b, n1), n2), modulus)


def fixed_ratio_allowed_n_mod(k: int, b: int, modulus: int) -> frozenset[int]:
    """Return residues ``n`` satisfying the two fixed-ratio leg conditions.

    For ``A = kB`` and ``B ≡ b (mod M)``, a vertical leg ``n`` must satisfy

        n² + B²   ≡ square (mod M)
        n² + A²   ≡ square (mod M).
    """
    _validate_inputs(k, modulus)
    sq = squares_mod(modulus)
    b_mod = b % modulus
    b2 = (b_mod * b_mod) % modulus
    kb = (k * b_mod) % modulus
    kb2 = (kb * kb) % modulus
    out: set[int] = set()
    for n in range(modulus):
        n2 = (n * n) % modulus
        if (n2 + b2) % modulus in sq and (n2 + kb2) % modulus in sq:
            out.add(n)
    return frozenset(out)


def _relation_target(k: int, b: int, modulus: int, relation: str) -> int:
    if relation in {REL_SUM_AB, REL_DIFF_AB}:
        coefficient = k + 1
    elif relation in {REL_SUM_DIFF, REL_DIFF_DIFF}:
        coefficient = abs(k - 1)
    else:
        raise ValueError(f"unknown fixed-ratio relation: {relation}")
    return (coefficient * (b % modulus)) % modulus


def is_fixed_ratio_witness(k: int, modulus: int, witness: FixedRatioWitness) -> bool:
    """Return whether ``witness`` passes the fixed-ratio congruence system."""
    _validate_inputs(k, modulus)
    b = witness.b % modulus
    n1 = witness.n1 % modulus
    n2 = witness.n2 % modulus
    allowed = fixed_ratio_allowed_n_mod(k, b, modulus)
    if n1 not in allowed or n2 not in allowed:
        return False

    target = _relation_target(k, b, modulus, witness.relation)
    if witness.relation.startswith("sum="):
        relation_ok = (n1 + n2 - target) % modulus == 0
    else:
        relation_ok = (n1 - n2 - target) % modulus == 0
    if not relation_ok:
        return False

    return witness.primitive_gcd_mod == _primitive_gcd_mod(b, n1, n2, modulus)


def universal_zero_b_witness(k: int, modulus: int) -> FixedRatioWitness:
    """Return the universal primitive local survivor for ``A = kB``.

    Since ``B ≡ 0`` also gives ``A ≡ 0``, both Pythagorean conditions reduce
    to ``n² ≡ square``. Taking ``N1 ≡ 1`` and ``N2 ≡ -1`` gives
    ``N1 + N2 ≡ 0 ≡ A+B`` and keeps the residue primitive.
    """
    _validate_inputs(k, modulus)
    b = 0
    n1 = 1 % modulus
    n2 = (-1) % modulus
    return FixedRatioWitness(
        b=b,
        n1=n1,
        n2=n2,
        relation=REL_SUM_AB,
        primitive_gcd_mod=_primitive_gcd_mod(b, n1, n2, modulus),
    )


def _relations_for_pair(k: int, b: int, n1: int, n2: int, modulus: int) -> tuple[str, ...]:
    out: list[str] = []
    for relation in FULL_PLANE_RELATIONS:
        target = _relation_target(k, b, modulus, relation)
        if relation.startswith("sum="):
            if (n1 + n2 - target) % modulus == 0:
                out.append(relation)
        elif (n1 - n2 - target) % modulus == 0:
            out.append(relation)
    return tuple(out)


def certify_fixed_ratio_modulus(
    k: int,
    modulus: int,
    *,
    sample_limit: int = 20,
) -> FixedRatioModCertificate:
    """Test one fixed-ratio branch modulo one modulus.

    ``status == "mod_killed"`` would mean no primitive residue class survives.
    In practice, the universal ``B ≡ 0`` witness forces
    ``status == "local_survives"`` for every valid input.
    """
    _validate_inputs(k, modulus)
    if sample_limit < 0:
        raise ValueError("sample_limit must be non-negative")

    total = 0
    primitive = 0
    samples: list[FixedRatioWitness] = []

    for b in range(modulus):
        allowed = fixed_ratio_allowed_n_mod(k, b, modulus)
        for n1 in allowed:
            for n2 in allowed:
                for relation in _relations_for_pair(k, b, n1, n2, modulus):
                    witness = FixedRatioWitness(
                        b=b,
                        n1=n1,
                        n2=n2,
                        relation=relation,
                        primitive_gcd_mod=_primitive_gcd_mod(b, n1, n2, modulus),
                    )
                    total += 1
                    if witness.primitive_gcd_mod == 1:
                        primitive += 1
                        if len(samples) < sample_limit:
                            samples.append(witness)

    universal = universal_zero_b_witness(k, modulus)
    status = "local_survives" if primitive else "mod_killed"
    return FixedRatioModCertificate(
        k=k,
        modulus=modulus,
        status=status,
        total_witness_count=total,
        primitive_witness_count=primitive,
        universal_witness=universal if is_fixed_ratio_witness(k, modulus, universal) else None,
        sample_primitive_witnesses=tuple(samples),
    )


def find_fixed_ratio_killer_modulus(
    k: int,
    moduli: tuple[int, ...],
) -> int | None:
    """Return a modulus that kills ``A = kB``, if this pure sieve finds one.

    The universal witness proves no valid finite modulus in this model can
    kill the branch, so the expected return value is always ``None``. The loop
    remains useful as an executable audit of that statement for chosen moduli.
    """
    for modulus in moduli:
        certificate = certify_fixed_ratio_modulus(k, modulus, sample_limit=0)
        if certificate.status == "mod_killed":
            return modulus
    return None


__all__ = [
    "FULL_PLANE_RELATIONS",
    "FixedRatioModCertificate",
    "FixedRatioWitness",
    "certify_fixed_ratio_modulus",
    "find_fixed_ratio_killer_modulus",
    "fixed_ratio_allowed_n_mod",
    "is_fixed_ratio_witness",
    "universal_zero_b_witness",
]
