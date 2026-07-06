"""Mixed closure quotient curves for the closed-chain problem.

For fixed legs ``(A, B)`` and the inside closure relation ``M = A + B - N``,
the full closed curve asks for all four quantities below to be squares:

    N^2 + A^2,  N^2 + B^2,  M^2 + A^2,  M^2 + B^2.

Pairwise products give six genus-one quotients. The two non-mixed quotients
``(N^2+A^2)(N^2+B^2)`` and its mirror are the old concordant curve. This
module focuses on the four quotients that see both ``N`` and ``M``.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from typing import Any


@dataclass(frozen=True)
class ClosureQuotientCurve:
    """A quartic quotient ``y^2 = q_left(N) * q_right(N)``."""

    name: str
    A: int
    B: int
    coeffs: tuple[int, int, int, int, int]
    left: str = ""
    right: str = ""

    def pari_polynomial(self, variable: str = "x") -> str:
        """Return a PARI polynomial string from constant-first coefficients."""
        terms: list[str] = []
        for power, coeff in reversed(list(enumerate(self.coeffs))):
            if coeff == 0:
                continue
            abs_coeff = abs(coeff)
            if power == 0:
                body = str(abs_coeff)
            elif power == 1:
                body = variable if abs_coeff == 1 else f"{abs_coeff}*{variable}"
            else:
                body = (
                    f"{variable}^{power}"
                    if abs_coeff == 1
                    else f"{abs_coeff}*{variable}^{power}"
                )
            if not terms:
                terms.append(f"-{body}" if coeff < 0 else body)
            else:
                terms.append(f"-{body}" if coeff < 0 else f"+{body}")
        return "".join(terms) if terms else "0"


@dataclass(frozen=True)
class QuarticPoint:
    """One affine rational point returned by PARI on ``y^2 = Q(x)``."""

    x: str
    y: str

    @property
    def x_fraction(self) -> Fraction:
        return Fraction(self.x)

    @property
    def y_fraction(self) -> Fraction:
        return Fraction(self.y)


def _quadratic_coeffs(A: int, B: int, kind: str) -> tuple[int, int, int]:
    """Return constant-first coefficients for a closure quadratic."""
    if kind == "NA":
        return (A * A, 0, 1)
    if kind == "NB":
        return (B * B, 0, 1)

    s = A + B
    if kind == "MA":
        return (s * s + A * A, -2 * s, 1)
    if kind == "MB":
        return (s * s + B * B, -2 * s, 1)
    raise ValueError(f"unknown closure quadratic kind: {kind!r}")


def _mul_quadratics(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> tuple[int, int, int, int, int]:
    out = [0, 0, 0, 0, 0]
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] += left_coeff * right_coeff
    return tuple(out)  # type: ignore[return-value]


def closure_quotient_polynomials(A: int, B: int) -> list[ClosureQuotientCurve]:
    """Build the four closure quotients that involve both ``N`` and ``M``."""
    factors = {
        "NA": _quadratic_coeffs(A, B, "NA"),
        "NB": _quadratic_coeffs(A, B, "NB"),
        "MA": _quadratic_coeffs(A, B, "MA"),
        "MB": _quadratic_coeffs(A, B, "MB"),
    }
    specs = (
        ("AA", "NA", "MA"),
        ("BB", "NB", "MB"),
        ("AB", "NA", "MB"),
        ("BA", "NB", "MA"),
    )
    return [
        ClosureQuotientCurve(
            name=name,
            A=A,
            B=B,
            coeffs=_mul_quadratics(factors[left], factors[right]),
            left=left,
            right=right,
        )
        for name, left, right in specs
    ]


def evaluate_quartic(curve: ClosureQuotientCurve, x: Fraction) -> Fraction:
    """Evaluate the quartic at a rational ``x``."""
    total = Fraction(0)
    power = Fraction(1)
    for coeff in curve.coeffs:
        total += coeff * power
        power *= x
    return total


def enumerate_quartic_points(
    curve: ClosureQuotientCurve,
    *,
    height: int,
    pari=None,
) -> list[QuarticPoint]:
    """Enumerate affine rational points on ``curve`` up to PARI naive height."""
    if pari is None:
        pari = _ensure_pari()
    polynomial = curve.pari_polynomial()
    raw_points = pari(f"hyperellratpoints({polynomial}, {height})")
    return [QuarticPoint(x=str(point[0]), y=str(point[1])) for point in raw_points]


def _is_square_fraction(value: Fraction) -> bool:
    if value < 0:
        return False
    numerator_root = isqrt(value.numerator)
    denominator_root = isqrt(value.denominator)
    return (
        numerator_root * numerator_root == value.numerator
        and denominator_root * denominator_root == value.denominator
    )


def classify_quartic_point(
    curve: ClosureQuotientCurve,
    point: QuarticPoint,
) -> dict[str, Any]:
    """Classify whether a quartic point is midpoint/trivial/full-closed."""
    n = point.x_fraction
    total = Fraction(curve.A + curve.B)
    m = total - n
    q_na = n * n + curve.A * curve.A
    q_nb = n * n + curve.B * curve.B
    q_ma = m * m + curve.A * curve.A
    q_mb = m * m + curve.B * curve.B
    square_flags = {
        "NA": _is_square_fraction(q_na),
        "NB": _is_square_fraction(q_nb),
        "MA": _is_square_fraction(q_ma),
        "MB": _is_square_fraction(q_mb),
    }
    return {
        "x": point.x,
        "y": point.y,
        "N": str(n),
        "M": str(m),
        "is_midpoint": n == m,
        "is_positive_closure": n > 0 and m > 0,
        "square_flags": square_flags,
        "is_full_closed_square": all(square_flags.values()),
    }


def _ensure_pari():
    from rational_distance.concordant.analysis import _ensure_pari as ensure

    return ensure()


def rank_closure_quotient(
    curve: ClosureQuotientCurve,
    pari=None,
    *,
    effort: int = 1,
) -> dict[str, Any]:
    """Convert one quartic quotient with PARI and compute its rank bounds."""
    if pari is None:
        pari = _ensure_pari()

    started = time.perf_counter()
    polynomial = curve.pari_polynomial()
    row: dict[str, Any] = {
        "A": curve.A,
        "B": curve.B,
        "curve": curve.name,
        "left": curve.left,
        "right": curve.right,
        "polynomial": polynomial,
        "status": "ok",
    }
    try:
        model = pari(f"ellfromeqn(y^2-({polynomial}))")
        elliptic_curve = pari.ellinit(model)
        rank_result = pari.ellrank(elliptic_curve, effort)
        torsion = pari.elltors(elliptic_curve)
    except Exception as exc:
        row.update(
            {
                "status": "pari-error",
                "error": str(exc),
                "elapsed_s": round(time.perf_counter() - started, 4),
            }
        )
        return row

    row.update(
        {
            "model": [int(model[i]) for i in range(5)],
            "rank_lower": int(rank_result[0]),
            "rank_upper": int(rank_result[1]),
            "sha2_lower": int(rank_result[2]) if len(rank_result) > 2 else 0,
            "n_generators": len(rank_result[3]) if len(rank_result) > 3 else 0,
            "torsion_order": int(torsion[0]),
            "elapsed_s": round(time.perf_counter() - started, 4),
        }
    )
    return row


def rank_mixed_closure_curves(
    pairs: list[tuple[int, int]],
    pari=None,
    *,
    effort: int = 1,
    pari_available: bool = True,
) -> list[dict[str, Any]]:
    """Rank all four mixed closure quotients for each pair."""
    rows: list[dict[str, Any]] = []
    if not pari_available:
        for A, B in pairs:
            for curve in closure_quotient_polynomials(A, B):
                rows.append(
                    {
                        "A": A,
                        "B": B,
                        "curve": curve.name,
                        "left": curve.left,
                        "right": curve.right,
                        "polynomial": curve.pari_polynomial(),
                        "status": "pari-unavailable",
                    }
                )
        return rows

    if pari is None:
        pari = _ensure_pari()
    for A, B in pairs:
        for curve in closure_quotient_polynomials(A, B):
            rows.append(rank_closure_quotient(curve, pari=pari, effort=effort))
    return rows
