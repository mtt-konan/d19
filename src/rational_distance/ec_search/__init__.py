"""Elliptic-curve search split into models, seeds, curve, and workflow."""

from .curve import QuarticEC
from .models import (
    ECCandidateRecord,
    ECCurveEdgeRecord,
    ECCurveNodeRecord,
    ECOrbitTrace,
    ECSeedBranch,
    ECSeedRecord,
    ECTripleTrace,
)
from .seeds import (
    _INT64_SAFE_HALF,
    _build_coprime_arrays,
    _find_seeds_gpu,
    _find_seeds_numpy,
    _isqrt_arr,
    _seeds_raw_to_fractions,
    find_seeds_for_triple,
)
from .workflow import (
    _build_triple_trace,
    _evaluate_candidate,
    _make_ec_point,
    _point_xy_from_k,
    ec_search,
)

__all__ = [
    "_INT64_SAFE_HALF",
    "ECCandidateRecord",
    "ECCurveEdgeRecord",
    "ECCurveNodeRecord",
    "ECOrbitTrace",
    "ECSeedBranch",
    "ECSeedRecord",
    "ECTripleTrace",
    "QuarticEC",
    "_build_coprime_arrays",
    "_build_triple_trace",
    "_evaluate_candidate",
    "_find_seeds_gpu",
    "_find_seeds_numpy",
    "_isqrt_arr",
    "_make_ec_point",
    "_point_xy_from_k",
    "_seeds_raw_to_fractions",
    "ec_search",
    "find_seeds_for_triple",
]
