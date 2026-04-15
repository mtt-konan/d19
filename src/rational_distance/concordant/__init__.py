"""Public concordant-analysis interface."""

from rational_distance.concordant.analysis import (
    ConcordantResult,
    analyze_pair,
    check_chain_compatibility,
    compute_rank,
    enumerate_multiples,
    find_concordant_integers,
)
from rational_distance.concordant.pairs import generate_ab_pairs

__all__ = [
    "ConcordantResult",
    "analyze_pair",
    "check_chain_compatibility",
    "compute_rank",
    "enumerate_multiples",
    "find_concordant_integers",
    "generate_ab_pairs",
]
