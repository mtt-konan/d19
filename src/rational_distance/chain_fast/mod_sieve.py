"""Small-modulus square-residue sieve for chain-fast C3 candidates."""

from __future__ import annotations

from dataclasses import dataclass
from math import lcm

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only when numpy is missing
    np = None  # type: ignore[assignment]

DEFAULT_MODULI: tuple[int, ...] = (16, 3, 5, 7)


def square_residues(modulus: int) -> frozenset[int]:
    """Return all quadratic residues modulo ``modulus``."""
    return frozenset((value * value) % modulus for value in range(modulus))


def build_square_sum_lookup(modulus: int) -> tuple[tuple[bool, ...], ...]:
    """Return a table for whether x²+y² can be a square modulo ``modulus``."""
    residues = square_residues(modulus)
    return tuple(
        tuple((((x * x) + (y * y)) % modulus) in residues for y in range(modulus))
        for x in range(modulus)
    )


@dataclass(frozen=True)
class ModSieve:
    """Precomputed lookups for a fixed collection of small moduli."""

    moduli: tuple[int, ...]
    combined_modulus: int
    combined_lookup: tuple[bool, ...]
    per_modulus_lookup: dict[int, tuple[tuple[bool, ...], ...]]
    combined_lookup_np: object | None = None

    @classmethod
    def build(cls, moduli: tuple[int, ...] = DEFAULT_MODULI) -> ModSieve:
        combined_modulus = 1
        per_modulus_lookup: dict[int, tuple[tuple[bool, ...], ...]] = {}
        for modulus in moduli:
            combined_modulus = lcm(combined_modulus, modulus)
            per_modulus_lookup[modulus] = build_square_sum_lookup(modulus)

        combined_lookup = tuple(
            all(
                per_modulus_lookup[modulus][a_residue % modulus][n_residue % modulus]
                for modulus in moduli
            )
            for a_residue in range(combined_modulus)
            for n_residue in range(combined_modulus)
        )
        return cls(
            moduli=moduli,
            combined_modulus=combined_modulus,
            combined_lookup=combined_lookup,
            per_modulus_lookup=per_modulus_lookup,
            combined_lookup_np=(
                np.fromiter(combined_lookup, dtype=np.bool_) if np is not None else None
            ),
        )

    def allow_pair(self, a_value: int, n_value: int) -> bool:
        """Return whether ``a_value²+n_value²`` could still be a square."""
        modulus = self.combined_modulus
        index = (a_value % modulus) * modulus + (n_value % modulus)
        return self.combined_lookup[index]

    def filter_numpy(self, a_values, n_values):
        """Vectorised version of :meth:`allow_pair` using the combined table."""
        if np is None:  # pragma: no cover - guarded by callers
            raise RuntimeError("numpy filter requested but numpy is not installed")
        modulus = self.combined_modulus
        indices = (a_values % modulus) * modulus + (n_values % modulus)
        return self.combined_lookup_np[indices]


DEFAULT_C3_MOD_SIEVE = ModSieve.build()


__all__ = [
    "DEFAULT_C3_MOD_SIEVE",
    "DEFAULT_MODULI",
    "ModSieve",
    "build_square_sum_lookup",
    "square_residues",
]
