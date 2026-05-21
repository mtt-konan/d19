"""Compatibility layer for the split EC search modules.

The implementation now lives in ``rational_distance.ec_search``:

- ``models.py``   — dataclasses and trace containers
- ``seeds.py``    — seed search helpers
- ``curve.py``    — quartic EC rules and orbit expansion
- ``workflow.py`` — end-to-end EC search orchestration

New code should import from ``rational_distance.ec_search`` directly.
"""

from __future__ import annotations

from rational_distance.ec_search import (
    _INT64_SAFE_HALF,
    ECCandidateRecord,
    ECCurveEdgeRecord,
    ECCurveNodeRecord,
    ECOrbitTrace,
    ECSeedBranch,
    ECSeedRecord,
    ECTripleTrace,
    QuarticEC,
    _build_coprime_arrays,
    _build_triple_trace,
    _evaluate_candidate,
    _find_seeds_gpu,
    _find_seeds_numpy,
    _isqrt_arr,
    _make_ec_point,
    _point_xy_from_k,
    _seeds_raw_to_fractions,
    ec_search,
    find_seeds_for_triple,
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
