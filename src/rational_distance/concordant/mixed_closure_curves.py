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
from itertools import product
from typing import Any

from rational_distance.math_utils import is_rational_sqrt


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
        "NA": is_rational_sqrt(q_na),
        "NB": is_rational_sqrt(q_nb),
        "MA": is_rational_sqrt(q_ma),
        "MB": is_rational_sqrt(q_mb),
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


def _centered_even_quartic_parameters(curve: ClosureQuotientCurve) -> dict[str, int] | None:
    """Return the centered even-quartic model for ``AA``/``BB`` quotients.

    For ``AA`` and ``BB``, setting ``t = 2N - (A+B)`` and ``z = 4y`` gives
    ``z^2 = t^4 + p*t^2 + q``. The mixed ``AB``/``BA`` quotients do not become
    even under this centering.
    """
    if curve.name == "AA":
        leg = curve.A
    elif curve.name == "BB":
        leg = curve.B
    else:
        return None

    total = curve.A + curve.B
    sqrt_q = total * total + 4 * leg * leg
    p = 8 * leg * leg - 2 * total * total
    q = sqrt_q * sqrt_q
    return {
        "total": total,
        "leg": leg,
        "p": p,
        "q": q,
        "sqrt_q": sqrt_q,
    }


def _enumerate_torsion_points(elliptic_curve, torsion, pari) -> list[Any | None]:
    """Enumerate all torsion points from PARI ``elltors`` output.

    ``None`` represents the identity point at infinity. PARI represents it as
    ``[0]``, but keeping it explicit avoids accidental coordinate indexing.
    """
    structures = [int(torsion[1][idx]) for idx in range(len(torsion[1]))]
    generators = [torsion[2][idx] for idx in range(len(torsion[2]))]
    if not structures:
        return [None]

    points: list[Any | None] = []
    seen: set[str] = set()
    for coefficients in product(*(range(order) for order in structures)):
        point = None
        for coefficient, generator in zip(coefficients, generators, strict=True):
            if coefficient == 0:
                continue
            term = pari.ellmul(elliptic_curve, generator, coefficient)
            point = term if point is None else pari.elladd(elliptic_curve, point, term)

        key = "[0]" if point is None else str(point)
        if key not in seen:
            seen.add(key)
            points.append(point)
    return points


def _pull_back_even_torsion_point(
    curve: ClosureQuotientCurve,
    params: dict[str, int],
    point,
) -> dict[str, Any]:
    """Pull one torsion point on the centered even model back to the quartic."""
    if point is None:
        return {
            "kind": "identity",
            "has_affine_preimage": False,
            "reason": "point-at-infinity",
        }

    x_coord = Fraction(str(point[0]))
    v_coord = Fraction(str(point[1]))
    p = Fraction(params["p"])
    q = Fraction(params["q"])
    denominator = 2 * (x_coord + p)
    base = {
        "kind": "torsion",
        "X": str(x_coord),
        "V": str(v_coord),
    }

    if denominator == 0:
        return {
            **base,
            "has_affine_preimage": False,
            "reason": "quartic-infinity",
        }

    t = v_coord / denominator
    z = x_coord / 2 - t * t
    rhs = t**4 + p * t * t + q
    if z * z != rhs:
        return {
            **base,
            "has_affine_preimage": False,
            "reason": "inverse-map-check-failed",
            "t": str(t),
            "z": str(z),
            "rhs": str(rhs),
        }

    n = (Fraction(params["total"]) + t) / 2
    y = z / 4
    classification = classify_quartic_point(curve, QuarticPoint(x=str(n), y=str(y)))
    return {
        **base,
        "has_affine_preimage": True,
        "t": str(t),
        "z": str(z),
        "N": str(n),
        "quartic_y": str(y),
        "classification": classification,
    }


def certify_rank_zero_even_quotient(
    curve: ClosureQuotientCurve,
    pari=None,
    *,
    effort: int = 1,
) -> dict[str, Any]:
    """Certify all affine quartic points for rank-zero ``AA``/``BB`` quotients.

    The certificate is strict for the centered even model: when PARI certifies
    rank ``0/0``, all rational points on the elliptic curve are torsion, and the
    explicit inverse map lists every affine quartic preimage.
    """
    params = _centered_even_quartic_parameters(curve)
    if params is None:
        return {
            "A": curve.A,
            "B": curve.B,
            "curve": curve.name,
            "status": "unsupported-curve",
            "reason": "only AA/BB quotients become centered even quartics",
        }
    if params["p"] * params["p"] == 4 * params["q"]:
        return {
            "A": curve.A,
            "B": curve.B,
            "curve": curve.name,
            "status": "singular-even-model",
        }

    if pari is None:
        pari = _ensure_pari()

    p = params["p"]
    q = params["q"]
    model = [0, p, 0, -4 * q, -4 * p * q]
    elliptic_curve = pari.ellinit(model)
    rank_result = pari.ellrank(elliptic_curve, effort)
    torsion = pari.elltors(elliptic_curve)

    certificate: dict[str, Any] = {
        "A": curve.A,
        "B": curve.B,
        "curve": curve.name,
        "centered_variable": "t=2*N-(A+B)",
        "even_quartic": f"z^2=t^4+({p})*t^2+({q})",
        "weierstrass_model": model,
        "rank_lower": int(rank_result[0]),
        "rank_upper": int(rank_result[1]),
        "sha2_lower": int(rank_result[2]) if len(rank_result) > 2 else 0,
        "torsion_order": int(torsion[0]),
    }
    if certificate["rank_lower"] != 0 or certificate["rank_upper"] != 0:
        certificate["status"] = "not-rank-zero"
        return certificate

    torsion_points = _enumerate_torsion_points(elliptic_curve, torsion, pari)
    pullbacks = [
        _pull_back_even_torsion_point(curve, params, point)
        for point in torsion_points
    ]
    affine_classifications = [
        pullback["classification"]
        for pullback in pullbacks
        if pullback.get("has_affine_preimage")
    ]
    map_errors = [
        pullback
        for pullback in pullbacks
        if pullback.get("reason") == "inverse-map-check-failed"
    ]
    certificate.update(
        {
            "status": "map-error" if map_errors else "certified",
            "torsion_point_count": len(torsion_points),
            "torsion_pullbacks": pullbacks,
            "affine_preimage_count": len(affine_classifications),
            "affine_preimage_classifications": affine_classifications,
            "certifies_no_full_closed_square": not any(
                point["is_full_closed_square"] for point in affine_classifications
            ),
            "all_affine_preimages_are_midpoints": all(
                point["is_midpoint"] for point in affine_classifications
            ),
        }
    )
    return certificate


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
        try:
            root_number = int(pari.ellrootno(elliptic_curve))
            root_number_error = None
        except Exception as exc:
            root_number = None
            root_number_error = str(exc)
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
    if root_number is not None:
        row["root_number"] = root_number
    else:
        row["root_number_error"] = root_number_error
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
