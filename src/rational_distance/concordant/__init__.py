"""Public concordant-analysis interface."""

from rational_distance.concordant.factor_search import find_concordant_by_factorization
from rational_distance.concordant.heegner_height import (
    HeegnerHeightScan,
    HeightScanPoint,
    scan_rank_one_height,
)
from rational_distance.concordant.analysis import (
    ConcordantResult,
    analyze_pair,
    check_chain_compatibility,
    compute_rank,
    enumerate_multiples,
    find_concordant_integers,
)
from rational_distance.concordant.pairs import generate_ab_pairs
from rational_distance.concordant.profile import ConcordantProfile
from rational_distance.concordant.workflow import (
    ChainCandidateDiagnostic,
    ConcordantPairDiagnostics,
    diagnose_pair,
)

__all__ = [
    "ChainCandidateDiagnostic",
    "ConcordantPairDiagnostics",
    "ConcordantProfile",
    "ConcordantResult",
    "HeegnerHeightScan",
    "HeightScanPoint",
    "analyze_pair",
    "check_chain_compatibility",
    "compute_rank",
    "diagnose_pair",
    "enumerate_multiples",
    "find_concordant_by_factorization",
    "find_concordant_integers",
    "generate_ab_pairs",
    "scan_rank_one_height",
]
