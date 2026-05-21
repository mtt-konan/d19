"""Judgement methods for the proof_status workflow.

Each method takes a reduced ``(A, B)`` pair and returns a ``MethodResult``
describing what it could conclude. Methods are pure-ish: they may call PARI
or any other library, but they must NOT touch the SQLite database — the
workflow layer is responsible for persistence.

Methods are listed in increasing order of cost and mathematical depth:

1. ``safe_sieve``       — instantaneous 2-adic necessary conditions
2. ``factor_concordant``— enumerate concordant N via h4^2 - h3^2 = B^2 - A^2
                          and check chain closure
3. ``rank_zero``        — call PARI ellrank; if proven rank == 0 ⇒ no_solution
4. ``heegner``          — rank-one generator + canonical-height diagnostics
5. ``chabauty_stub``    — placeholder for Quadratic Chabauty
6. ``brauer_manin_stub``— placeholder for Brauer–Manin obstruction

The Heegner/height method is deliberately conservative: it can record rank-one
generator/height evidence and can prove a positive witness if a chain-compatible
point is found, but it does not mark ``no_solution`` until a future global height
bound is implemented.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from math import isqrt

from rational_distance.concordant.factor_search import find_concordant_by_factorization
from rational_distance.concordant.safe_pair_sieve import classify_reduced_pair
from rational_distance.proof_status.types import MethodResult

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def _check_chain_compatibility(A: int, B: int, N: int) -> bool:
    """Return True iff (A, B, N) extends to a full chain (a+c=b+d)."""
    b = A + B - N
    if b <= 0:
        return False
    return _is_perfect_square(B * B + b * b) and _is_perfect_square(b * b + A * A)


# ---------------------------------------------------------------------------
# Method 1: safe_sieve  (2-adic necessary conditions on reduced pairs)
# ---------------------------------------------------------------------------


def run_safe_sieve(A: int, B: int) -> MethodResult:
    """Apply the proven 2-adic necessary conditions on reduced ``(A, B)``."""
    started = time.perf_counter()
    classification = classify_reduced_pair(A, B)
    elapsed = time.perf_counter() - started

    details: dict[str, object] = {"classification": classification}

    if classification == "pass":
        return MethodResult(
            method="safe_sieve",
            outcome="pass",
            details=details,
            elapsed_s=elapsed,
            notes="2-adic necessary conditions satisfied; deeper methods required.",
        )

    # mixed_parity and odd_odd_wrong_mod4 are both rigorous obstructions
    # for the full chain (not just for concordant existence).
    return MethodResult(
        method="safe_sieve",
        outcome="no_solution",
        details=details,
        elapsed_s=elapsed,
        notes=f"Rejected by safe_sieve: {classification}",
    )


# ---------------------------------------------------------------------------
# Method 2: factor_concordant  (exhaustive concordant N + chain closure)
# ---------------------------------------------------------------------------


def run_factor_concordant(A: int, B: int) -> MethodResult:
    """Enumerate every concordant N via factor decomposition and test chain closure.

    The factor enumeration is provably exhaustive (see
    ``concordant.factor_search``): every concordant integer N is recovered
    from some divisor pair of ``B^2 - A^2``. Therefore:

    - If the enumeration returns an empty list, no concordant integer N exists
      at all ⇒ no full chain solution can exist ⇒ ``no_solution``.
    - If at least one N satisfies the full chain closure, that pair has a
      full solution ⇒ ``solution_found`` (would refute Harborth).
    - Otherwise, all N fail closure ⇒ ``inconclusive`` (concordant exists
      but never closes into a 4-cycle; a deeper method must decide whether
      that gap is necessary).
    """
    started = time.perf_counter()
    Ns = find_concordant_by_factorization(A, B)
    chain_ok = [N for N in Ns if _check_chain_compatibility(A, B, N)]
    elapsed = time.perf_counter() - started

    details: dict[str, object] = {
        "concordant_n_count": len(Ns),
        "chain_compatible_count": len(chain_ok),
        "chain_compatible_n": chain_ok[:16],  # cap to keep JSON small
        "sample_concordant_n": Ns[:16],
    }

    if not Ns:
        return MethodResult(
            method="factor_concordant",
            outcome="no_solution",
            details=details,
            elapsed_s=elapsed,
            notes="No concordant N exists (exhaustive factor enumeration).",
        )

    if chain_ok:
        return MethodResult(
            method="factor_concordant",
            outcome="solution_found",
            details=details,
            elapsed_s=elapsed,
            notes=f"Chain-compatible N found: {chain_ok[:4]} (would refute Harborth).",
        )

    return MethodResult(
        method="factor_concordant",
        outcome="inconclusive",
        details=details,
        elapsed_s=elapsed,
        notes=(
            f"Concordant N exist ({len(Ns)} total) but none close the 4-cycle. "
            "Need deeper EC / Heegner / Chabauty analysis."
        ),
    )


# ---------------------------------------------------------------------------
# Method 3: rank_zero  (PARI ellrank; proven rank == 0 ⇒ no_solution)
# ---------------------------------------------------------------------------


# PARI is expensive to initialise (64 MB allocation). We cache one instance per
# process so that batch calls into ``run_rank_zero`` only pay the cost once.
# Tests can reset via ``_reset_pari_cache``.
_pari_cache: object | None = None


def _get_cached_pari() -> object | None:
    """Return a process-wide PARI instance, or None if cypari2 is unavailable."""
    global _pari_cache
    if _pari_cache is not None:
        return _pari_cache
    try:
        from rational_distance.concordant.analysis import _ensure_pari
    except ImportError:
        return None
    try:
        _pari_cache = _ensure_pari()
    except Exception:
        _pari_cache = None
    return _pari_cache


def _reset_pari_cache() -> None:
    """Drop the cached PARI instance. Intended for tests only."""
    global _pari_cache
    _pari_cache = None


def run_rank_zero(A: int, B: int) -> MethodResult:
    """Call PARI ellrank on E: Y^2 = X(X+A^2)(X+B^2).

    If the *upper* bound on rank is 0, the curve has only torsion points.
    Since the torsion subgroup is Z/2Z × Z/4Z with X-coordinates in
    {0, -A^2, -B^2, AB, -AB}, and none of these is a positive perfect
    square X = N^2 with N > 0, the pair has no concordant integer N and
    therefore no full chain solution.

    PARI may also return a strict lower bound > 0, which we use only as a
    sanity check (does NOT imply solution existence — only that concordant
    rational points exist, which the chain closure layer still has to
    reject).
    """
    started = time.perf_counter()
    pari = _get_cached_pari()
    if pari is None:
        return MethodResult(
            method="rank_zero",
            outcome="skipped",
            details={"reason": "cypari2 unavailable"},
            elapsed_s=time.perf_counter() - started,
            notes="Skipped: cypari2 / PARI not available.",
        )

    try:
        from rational_distance.concordant.analysis import compute_rank

        rank, (lower, upper), gens = compute_rank(A, B, pari)
    except Exception as exc:
        return MethodResult(
            method="rank_zero",
            outcome="error",
            details={"exception": str(exc)},
            elapsed_s=time.perf_counter() - started,
            notes=f"PARI error: {exc}",
        )

    elapsed = time.perf_counter() - started
    details: dict[str, object] = {
        "rank": rank,
        "rank_lower": lower,
        "rank_upper": upper,
        "generators": gens[:4],
    }

    if upper == 0:
        return MethodResult(
            method="rank_zero",
            outcome="no_solution",
            details=details,
            elapsed_s=elapsed,
            notes="Proven rank = 0; only torsion points exist (none give N^2 > 0).",
        )

    if lower >= 1:
        return MethodResult(
            method="rank_zero",
            outcome="inconclusive",
            details=details,
            elapsed_s=elapsed,
            notes=(
                f"rank in [{lower}, {upper}]; non-torsion points exist. "
                "Need Heegner / Chabauty / Brauer–Manin to decide whether "
                "any of them give an integer N closing the chain."
            ),
        )

    return MethodResult(
        method="rank_zero",
        outcome="inconclusive",
        details=details,
        elapsed_s=elapsed,
        notes=f"rank in [{lower}, {upper}]; bounds inconclusive.",
    )


# ---------------------------------------------------------------------------
# Method 4: heegner  (rank-one generator + canonical-height scan)
# ---------------------------------------------------------------------------


def _heegner_details(scan) -> dict[str, object]:
    """Convert a HeegnerHeightScan dataclass into JSON-friendly details."""
    return {
        "backend": scan.backend,
        "reason": scan.skipped_reason,
        "rank_lower": scan.rank_lower,
        "rank_upper": scan.rank_upper,
        "generator": list(scan.generator) if scan.generator is not None else None,
        "generator_height": scan.generator_height,
        "multiple_bound": scan.multiple_bound,
        "height_bound": scan.height_bound,
        "effective_height_bound": scan.effective_height_bound,
        "points_checked": scan.points_checked,
        "square_x_count": len(scan.square_x_points),
        "square_x_points": [
            {
                "multiple": point.multiple,
                "torsion_label": point.torsion_label,
                "x": point.x,
                "n": point.n,
                "concordant": point.concordant,
                "chain_compatible": point.chain_compatible,
                "canonical_height": point.canonical_height,
            }
            for point in scan.square_x_points[:16]
        ],
        "concordant_n_count": len(scan.concordant_n),
        "sample_concordant_n": scan.concordant_n[:16],
        "chain_compatible_count": len(scan.chain_compatible_n),
        "chain_compatible_n": scan.chain_compatible_n[:16],
    }


def run_heegner_height(A: int, B: int) -> MethodResult:
    """Run direction-five rank-one generator / canonical-height diagnostics.

    See docs/THEORY_DIRECTIONS_ADVANCED.md (方向五).

    This is a safe partial implementation: it scans the rank-one
    Mordell-Weil generator (from PARI ``ellrank``; Heegner construction can
    replace this source later) together with the known torsion subgroup, and
    records canonical-height evidence.  It returns ``solution_found`` if a real
    chain witness is found.  It otherwise returns ``inconclusive`` for rank-one
    scans and ``skipped`` when the method is not applicable (for example
    rank != 1).  It never returns ``no_solution`` yet.
    """
    started = time.perf_counter()
    try:
        from rational_distance.concordant.heegner_height import scan_rank_one_height

        scan = scan_rank_one_height(A, B, pari=_get_cached_pari())
    except Exception as exc:
        return MethodResult(
            method="heegner",
            outcome="error",
            details={"exception": str(exc)},
            elapsed_s=time.perf_counter() - started,
            notes=f"Heegner/height method failed: {exc}",
        )

    details = _heegner_details(scan)
    elapsed = scan.elapsed_s or (time.perf_counter() - started)

    if scan.skipped_reason is not None:
        outcome = (
            "error"
            if scan.skipped_reason == "pari_error"
            else "inconclusive"
            if scan.skipped_reason == "missing_generator"
            else "skipped"
        )
        return MethodResult(
            method="heegner",
            outcome=outcome,
            details=details,
            elapsed_s=elapsed,
            notes=scan.notes or f"Heegner/height skipped: {scan.skipped_reason}",
        )

    if scan.chain_compatible_n:
        return MethodResult(
            method="heegner",
            outcome="solution_found",
            details=details,
            elapsed_s=elapsed,
            notes=(
                "Rank-one height scan found chain-compatible N: "
                f"{scan.chain_compatible_n[:4]} (would refute Harborth)."
            ),
        )

    return MethodResult(
        method="heegner",
        outcome="inconclusive",
        details=details,
        elapsed_s=elapsed,
        notes=(
            "Rank-one generator/height scan found no chain-compatible point "
            f"within |n| <= {scan.multiple_bound}. This is diagnostic only, "
            "not a global no-solution proof."
        ),
    )


def run_heegner_stub(A: int, B: int) -> MethodResult:
    """Backward-compatible name for the direction-five method.

    Older docs/tests imported ``run_heegner_stub``.  Keep the symbol, but route
    it to the implemented conservative method.
    """
    return run_heegner_height(A, B)


# ---------------------------------------------------------------------------
# Methods 5-6: stubs for the remaining advanced theoretical directions
# ---------------------------------------------------------------------------


def run_chabauty_stub(_A: int, _B: int) -> MethodResult:
    """Placeholder for Chabauty / Quadratic Chabauty.

    See docs/THEORY_DIRECTIONS_ADVANCED.md (方向七).
    """
    return MethodResult(
        method="chabauty",
        outcome="skipped",
        details={"reason": "not_implemented"},
        elapsed_s=0.0,
        notes="Chabauty / QC not yet implemented (planned via SageMath qc_mod).",
    )


def run_brauer_manin_stub(_A: int, _B: int) -> MethodResult:
    """Placeholder for Brauer–Manin obstruction.

    See docs/THEORY_DIRECTIONS_ADVANCED.md (方向八).
    """
    return MethodResult(
        method="brauer_manin",
        outcome="skipped",
        details={"reason": "not_implemented"},
        elapsed_s=0.0,
        notes="Brauer–Manin obstruction not yet implemented (planned via Magma).",
    )


# ---------------------------------------------------------------------------
# Method registry
# ---------------------------------------------------------------------------


MethodFn = Callable[[int, int], MethodResult]

# Methods that the workflow will call in this order by default.
# Each entry is (name, MethodFn). Stubs at the end so they are always recorded.
DEFAULT_METHOD_PIPELINE: tuple[tuple[str, MethodFn], ...] = (
    ("safe_sieve", run_safe_sieve),
    ("factor_concordant", run_factor_concordant),
    ("rank_zero", run_rank_zero),
    ("heegner", run_heegner_stub),
    ("chabauty", run_chabauty_stub),
    ("brauer_manin", run_brauer_manin_stub),
)


__all__ = [
    "DEFAULT_METHOD_PIPELINE",
    "MethodFn",
    "run_brauer_manin_stub",
    "run_chabauty_stub",
    "run_factor_concordant",
    "run_heegner_height",
    "run_heegner_stub",
    "run_rank_zero",
    "run_safe_sieve",
]
