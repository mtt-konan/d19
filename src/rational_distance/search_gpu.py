"""GPU-accelerated rational-distance search using CuPy or PyTorch.

Search logic only.  Backend detection lives in `backend.py`.

Unlike parametric_search_fast (multiprocessing), this runs in a *single
process*.  The GPU replaces multi-core CPU parallelism: each triple's
entire (a,b) array is dispatched as one GPU kernel that operates on up to
N_pairs elements simultaneously.

Unified memory on APUs (Ryzen AI Max, Apple M-series with PyTorch MPS)
means transfers are logical, not physical — so even "copy to GPU" is cheap.

int64 safety: tB_max ≈ (scale*r_max)^2 ≈ 4e18 for scale ≈ 600.
Unsafe triples now fall back to the shared exact CPU path automatically,
so accelerated runs stay correct even when the int64 vectorized path is
no longer safe.

Architecture guard:
  Parametric formulas and overflow rules belong in `parametric_core.py`.
  This module should only manage backend execution and hand off correctness
  decisions to the shared core.
"""

from __future__ import annotations

from rational_distance import parametric_core as core
from rational_distance.backend import detect_backend
from rational_distance.math_utils import primitive_pythagorean_triples
from rational_distance.square import RationalPoint

# ── Public GPU search ─────────────────────────────────────────────────────────


def _parametric_search_gpu_run(
    max_m: int = 80,
    max_k_num: int = 640,
    max_k_den: int = 320,
    min_rational: int = 3,
    progress: bool = True,
    xp=None,
    inside_only: bool = False,
) -> tuple[list[RationalPoint], str, core.ParametricRunStats]:
    """Run the accelerated parametric search and return results plus stats."""
    if xp is None:
        xp, backend_name, _ = detect_backend()
    else:
        backend_name = getattr(xp, "__name__", type(xp).__name__)

    pairs, a_np, b_np = core.build_coprime_data(max_k_num, max_k_den)
    triples = primitive_pythagorean_triples(max_m)
    stats = core.make_run_stats(triples, max_k_num, max_k_den)

    # Upload to device (no-op for numpy or unified-memory APUs)
    a_dev = xp.array(a_np, dtype=xp.int64)
    b_dev = xp.array(b_np, dtype=xp.int64)

    if progress:
        try:
            from tqdm import tqdm

            it = tqdm(triples, desc="Searching", unit="triple")
        except ImportError:
            it = triples
    else:
        it = triples

    raw: list[dict] = []
    seen_xy: set[tuple] = set()
    if stats.exact_fallback_triples:
        print(
            f"  Note: {stats.exact_fallback_triples}/{stats.total_triples} triples use the "
            f"shared exact CPU fallback (r > {stats.safe_r_max:,}) to stay overflow-safe."
        )
    for p, q, r in it:
        if r <= stats.safe_r_max:
            hits = core.search_triple_vectorized(
                xp, p, q, r, a_dev, b_dev, min_rational, inside_only
            )
        else:
            hits = core.search_triple_exact(p, q, r, pairs, min_rational, inside_only)
        for h in hits:
            key = (h["x"], h["y"])
            if key not in seen_xy:
                seen_xy.add(key)
                raw.append(h)

    return core.best_points_from_raw(raw), backend_name, stats


def parametric_search_gpu(
    max_m: int = 80,
    max_k_num: int = 640,
    max_k_den: int = 320,
    min_rational: int = 3,
    progress: bool = True,
    xp=None,
    inside_only: bool = False,
) -> tuple[list[RationalPoint], str]:
    """GPU/APU-accelerated parametric search (single process)."""
    points, backend_name, _ = _parametric_search_gpu_run(
        max_m=max_m,
        max_k_num=max_k_num,
        max_k_den=max_k_den,
        min_rational=min_rational,
        progress=progress,
        xp=xp,
        inside_only=inside_only,
    )
    return points, backend_name
