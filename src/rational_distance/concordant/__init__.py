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
from rational_distance.concordant.workflow import (
    ChainCandidateDiagnostic,
    ConcordantPairDiagnostics,
    diagnose_pair,
)

__all__ = [
    "ChainCandidateDiagnostic",
    "ConcordantPairDiagnostics",
    "ConcordantResult",
    "analyze_pair",
    "check_chain_compatibility",
    "compute_rank",
    "diagnose_pair",
    "enumerate_multiples",
    "find_concordant_integers",
    "generate_ab_pairs",
]
