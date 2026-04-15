"""Compatibility re-export for concordant elliptic-curve helpers."""

from rational_distance.concordant.analysis import (
    ConcordantResult,
    _is_perfect_square,
    analyze_pair,
    check_chain_compatibility,
    compute_rank,
    enumerate_multiples,
    find_concordant_integers,
)
from rational_distance.concordant.workflow import (
    ChainCandidateDiagnostic,
    ConcordantPairDiagnostics,
    diagnose_pair,
)

__all__ = [
    "ChainCandidateDiagnostic",
    "ConcordantPairDiagnostics",
    "ConcordantResult",
    "_is_perfect_square",
    "analyze_pair",
    "check_chain_compatibility",
    "compute_rank",
    "diagnose_pair",
    "enumerate_multiples",
    "find_concordant_integers",
]
