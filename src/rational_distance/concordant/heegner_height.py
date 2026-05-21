"""Rank-one generator + canonical-height diagnostics for concordant curves.

This module is the engineering foothold for theory direction 5 ("Heegner +
height").  In a full SageMath environment, the rank-one generator may be
constructed from Heegner points.  In this project we keep the runtime dependency
light and use the existing PARI/cypari2 Mordell-Weil generator returned by
``ellrank``; the height and finite multiple scan are the same downstream checks
needed by the Heegner route.

Important safety rule
---------------------
The scan performed here is **not** a global non-existence proof.  It may find a
chain-compatible point, which is a rigorous positive witness, but failure to find
one only returns diagnostics.  The proof-status method built on top of this
module must therefore return ``inconclusive`` rather than ``no_solution`` unless
some future height theorem supplies a certified global bound.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from math import isfinite, isqrt, sqrt
from typing import Any

from rational_distance.concordant.analysis import check_chain_compatibility

DEFAULT_MULTIPLE_BOUND = 12


def _is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(0, value)


def _env_float(name: str) -> float | None:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    if not isfinite(value) or value < 0:
        return None
    return value


@dataclass(frozen=True)
class HeightScanPoint:
    """One scanned Mordell-Weil point whose X-coordinate is an integer square."""

    multiple: int
    torsion_label: str
    x: str
    n: int
    concordant: bool
    chain_compatible: bool
    canonical_height: float | None = None


@dataclass(frozen=True)
class HeegnerHeightScan:
    """Diagnostic result for a rank-one height scan."""

    A: int
    B: int
    backend: str
    rank_lower: int | None
    rank_upper: int | None
    generator: tuple[str, str] | None
    generator_height: float | None
    multiple_bound: int
    height_bound: float | None
    effective_height_bound: float | None
    points_checked: int
    square_x_points: list[HeightScanPoint] = field(default_factory=list)
    concordant_n: list[int] = field(default_factory=list)
    chain_compatible_n: list[int] = field(default_factory=list)
    elapsed_s: float = 0.0
    skipped_reason: str | None = None
    notes: str = ""

    @property
    def ran(self) -> bool:
        return self.skipped_reason is None


def _curve(A: int, B: int, pari: Any):
    a2, b2 = A * A, B * B
    return pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")


def _finite_torsion_points(A: int, B: int) -> list[tuple[str, list[int]]]:
    """Return the known finite torsion points for y²=x(x+A²)(x+B²).

    The identity is handled separately as torsion label ``O``.
    """
    a2, b2, ab = A * A, B * B, A * B
    return [
        ("T2:x=0", [0, 0]),
        ("T2:x=-A^2", [-a2, 0]),
        ("T2:x=-B^2", [-b2, 0]),
        ("T4:x=AB,+", [ab, ab * (A + B)]),
        ("T4:x=AB,-", [ab, -ab * (A + B)]),
        ("T4:x=-AB,+", [-ab, ab * (A - B)]),
        ("T4:x=-AB,-", [-ab, -ab * (A - B)]),
    ]


def _point_xy_strings(point: Any) -> tuple[str, str] | None:
    try:
        if len(point) < 2:
            return None
        return str(point[0]), str(point[1])
    except Exception:
        return None


def _integer_n_from_square_x(pari: Any, x_value: Any) -> int | None:
    """Return N if x_value is a positive integer square X=N², else None."""
    try:
        x_num = int(pari.numerator(x_value))
        x_den = int(pari.denominator(x_value))
    except Exception:
        try:
            x_num = int(x_value)
            x_den = 1
        except Exception:
            return None

    if x_num <= 0 or x_den <= 0:
        return None
    if not _is_perfect_square(x_num) or not _is_perfect_square(x_den):
        return None

    n_num = isqrt(x_num)
    n_den = isqrt(x_den)
    if n_den != 1:
        # Rational square X=(u/v)^2 exists, but the chain model needs integer N.
        return None
    return n_num if n_num > 0 else None


def _canonical_height(pari: Any, E: Any, point: Any) -> float | None:
    try:
        return float(pari.ellheight(E, point))
    except Exception:
        return None


def _effective_multiple_bound(
    *,
    multiple_bound: int | None,
    height_bound: float | None,
    generator_height: float | None,
) -> tuple[int, float | None]:
    """Combine an explicit multiple bound with a canonical-height bound.

    For rank one, h(nG+T)=n²h(G).  A supplied height bound therefore gives a
    multiple bound floor(sqrt(H/h(G))).  We still cap by the explicit multiple
    bound if both are supplied, because CLI users often want a cheap smoke run.
    """
    base = DEFAULT_MULTIPLE_BOUND if multiple_bound is None else max(0, int(multiple_bound))
    if height_bound is None or generator_height is None or generator_height <= 0:
        return base, None

    by_height = int(sqrt(height_bound / generator_height))
    if multiple_bound is None:
        return max(0, by_height), height_bound
    return min(base, max(0, by_height)), height_bound


def scan_rank_one_height(
    A: int,
    B: int,
    *,
    pari: Any | None = None,
    multiple_bound: int | None = None,
    height_bound: float | None = None,
) -> HeegnerHeightScan:
    """Run a conservative rank-one canonical-height scan.

    Parameters
    ----------
    A, B:
        Positive reduced pair for the concordant curve.
    pari:
        Optional cached PARI instance.
    multiple_bound:
        Check all points ``nG + T`` with ``|n| <= multiple_bound`` and torsion
        ``T`` in the known torsion subgroup.  If omitted, the environment
        variable ``RD_HEEGNER_MULTIPLE_BOUND`` is read, falling back to 12.
    height_bound:
        Optional canonical-height cap.  If omitted, ``RD_HEEGNER_HEIGHT_BOUND``
        may provide one.  This controls the multiple scan but is not treated as
        a proof of global non-existence by itself.
    """
    started = time.perf_counter()
    if A == B:
        return HeegnerHeightScan(
            A=A,
            B=B,
            backend="pari_ellrank_height",
            rank_lower=None,
            rank_upper=None,
            generator=None,
            generator_height=None,
            multiple_bound=0,
            height_bound=height_bound,
            effective_height_bound=None,
            points_checked=0,
            elapsed_s=time.perf_counter() - started,
            skipped_reason="singular_curve",
            notes="A == B gives a singular cubic, not an elliptic curve.",
        )

    if multiple_bound is None:
        multiple_bound = _env_int("RD_HEEGNER_MULTIPLE_BOUND", DEFAULT_MULTIPLE_BOUND)
    if height_bound is None:
        height_bound = _env_float("RD_HEEGNER_HEIGHT_BOUND")

    if pari is None:
        try:
            from rational_distance.concordant.analysis import _ensure_pari

            pari = _ensure_pari()
        except Exception as exc:
            return HeegnerHeightScan(
                A=A,
                B=B,
                backend="pari_ellrank_height",
                rank_lower=None,
                rank_upper=None,
                generator=None,
                generator_height=None,
                multiple_bound=max(0, int(multiple_bound)),
                height_bound=height_bound,
                effective_height_bound=None,
                points_checked=0,
                elapsed_s=time.perf_counter() - started,
                skipped_reason="cypari2_unavailable",
                notes=f"PARI unavailable: {exc}",
            )

    try:
        E = _curve(A, B, pari)
        rank_info = pari.ellrank(E)
        lower = int(rank_info[0])
        upper = int(rank_info[1])
    except Exception as exc:
        return HeegnerHeightScan(
            A=A,
            B=B,
            backend="pari_ellrank_height",
            rank_lower=None,
            rank_upper=None,
            generator=None,
            generator_height=None,
            multiple_bound=max(0, int(multiple_bound)),
            height_bound=height_bound,
            effective_height_bound=None,
            points_checked=0,
            elapsed_s=time.perf_counter() - started,
            skipped_reason="pari_error",
            notes=f"PARI ellrank/ellinit failed: {exc}",
        )

    if lower != 1 or upper != 1:
        return HeegnerHeightScan(
            A=A,
            B=B,
            backend="pari_ellrank_height",
            rank_lower=lower,
            rank_upper=upper,
            generator=None,
            generator_height=None,
            multiple_bound=max(0, int(multiple_bound)),
            height_bound=height_bound,
            effective_height_bound=None,
            points_checked=0,
            elapsed_s=time.perf_counter() - started,
            skipped_reason="rank_not_one",
            notes=(
                "Heegner/height scan is only configured for exact rank 1, "
                f"got [{lower},{upper}]."
            ),
        )

    try:
        gen_list = rank_info[3]
        if len(gen_list) < 1:
            raise ValueError("PARI returned rank 1 but no generator list")
        G = gen_list[0]
        generator_xy = _point_xy_strings(G)
        if generator_xy is None:
            raise ValueError(f"invalid generator format: {G!r}")
    except Exception as exc:
        return HeegnerHeightScan(
            A=A,
            B=B,
            backend="pari_ellrank_height",
            rank_lower=lower,
            rank_upper=upper,
            generator=None,
            generator_height=None,
            multiple_bound=max(0, int(multiple_bound)),
            height_bound=height_bound,
            effective_height_bound=None,
            points_checked=0,
            elapsed_s=time.perf_counter() - started,
            skipped_reason="missing_generator",
            notes=str(exc),
        )

    hG = _canonical_height(pari, E, G)
    bound, effective_height_bound = _effective_multiple_bound(
        multiple_bound=multiple_bound,
        height_bound=height_bound,
        generator_height=hG,
    )

    torsion: list[tuple[str, list[int] | None]] = [("O", None)]
    torsion.extend(_finite_torsion_points(A, B))

    checked_points: set[str] = set()
    square_points: list[HeightScanPoint] = []
    concordant: set[int] = set()
    chain_ok: set[int] = set()
    points_checked = 0
    a2, b2 = A * A, B * B

    for n in range(-bound, bound + 1):
        try:
            base_point = None if n == 0 else pari.ellmul(E, G, n)
        except Exception:
            continue

        for torsion_label, torsion_point in torsion:
            try:
                if base_point is None and torsion_point is None:
                    # The point at infinity has no X-coordinate.
                    continue
                if base_point is None:
                    point = torsion_point
                elif torsion_point is None:
                    point = base_point
                else:
                    point = pari.elladd(E, base_point, torsion_point)

                xy = _point_xy_strings(point)
                if xy is None:
                    continue
                point_key = f"{xy[0]},{xy[1]}"
                if point_key in checked_points:
                    continue
                checked_points.add(point_key)
                points_checked += 1

                x_value = point[0]
                N = _integer_n_from_square_x(pari, x_value)
                if N is None:
                    continue

                is_concordant = _is_perfect_square(N * N + a2) and _is_perfect_square(
                    N * N + b2
                )
                is_chain = is_concordant and check_chain_compatibility(A, B, N)
                if is_concordant:
                    concordant.add(N)
                if is_chain:
                    chain_ok.add(N)

                square_points.append(
                    HeightScanPoint(
                        multiple=n,
                        torsion_label=torsion_label,
                        x=str(x_value),
                        n=N,
                        concordant=is_concordant,
                        chain_compatible=is_chain,
                        canonical_height=_canonical_height(pari, E, point),
                    )
                )
            except Exception:
                continue

    notes = (
        "Rank-one MW generator scanned by canonical-height/multiple bound. "
        "No negative conclusion is claimed unless a future theorem certifies the bound."
    )
    return HeegnerHeightScan(
        A=A,
        B=B,
        backend="pari_ellrank_height",
        rank_lower=lower,
        rank_upper=upper,
        generator=generator_xy,
        generator_height=hG,
        multiple_bound=bound,
        height_bound=height_bound,
        effective_height_bound=effective_height_bound,
        points_checked=points_checked,
        square_x_points=square_points,
        concordant_n=sorted(concordant),
        chain_compatible_n=sorted(chain_ok),
        elapsed_s=time.perf_counter() - started,
        skipped_reason=None,
        notes=notes,
    )


__all__ = [
    "DEFAULT_MULTIPLE_BOUND",
    "HeegnerHeightScan",
    "HeightScanPoint",
    "scan_rank_one_height",
]
