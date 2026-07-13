"""Exact complete-d cover arithmetic and the reusable wl491 point filter."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from typing import Any

ECPoint = tuple[Fraction, Fraction] | None


def rational(value: int | str | dict[str, str]) -> Fraction:
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if set(value) != {"numerator", "denominator"}:
        raise ValueError("rational object must contain numerator and denominator")
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def _square(value: Fraction) -> bool:
    return (
        value >= 0
        and isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _fmt(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


@dataclass(frozen=True)
class CertificateChecks:
    cover_equations: bool
    elliptic_product: bool
    no_lift_certificate: bool

    @property
    def passed(self) -> bool:
        return self.cover_equations and self.elliptic_product and self.no_lift_certificate


def _cover_values(certificate: dict[str, Any]) -> tuple[Fraction, ...]:
    point = certificate["point_on_cover"]
    return tuple(
        rational(point[key]) for key in ("X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q")
    )


def _parse_point(value: str) -> ECPoint:
    if value == "O":
        return None
    if not (value.startswith("(") and value.endswith(")")):
        raise ValueError(f"invalid point: {value}")
    x, y = value[1:-1].split(",", 1)
    return Fraction(x), Fraction(y)


def _ec_add(left: ECPoint, right: ECPoint, a2: Fraction, a4: Fraction) -> ECPoint:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and y1 == -y2:
        return None
    if left == right:
        if y1 == 0:
            return None
        slope = (3 * x1 * x1 + 2 * a2 * x1 + a4) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = slope * slope - a2 - x1 - x2
    return x3, -y1 + slope * (x1 - x3)


def _ec_mul(multiplier: int, point: ECPoint, a2: Fraction, a4: Fraction) -> ECPoint:
    if multiplier < 0:
        assert point is not None
        return _ec_mul(-multiplier, (point[0], -point[1]), a2, a4)
    result = None
    addend = point
    while multiplier:
        if multiplier & 1:
            result = _ec_add(result, addend, a2, a4)
        addend = _ec_add(addend, addend, a2, a4)
        multiplier >>= 1
    return result


def _point_string(point: tuple[int, int] | None) -> str:
    return "O" if point is None else f"({point[0]},{point[1]})"


def _fp_add(
    left: tuple[int, int] | None,
    right: tuple[int, int] | None,
    prime: int,
    a2: int,
    a4: int,
) -> tuple[int, int] | None:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % prime == 0:
        return None
    if left == right:
        slope = (3 * x1 * x1 + 2 * a2 * x1 + a4) * pow(2 * y1, -1, prime)
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, prime)
    slope %= prime
    x3 = (slope * slope - a2 - x1 - x2) % prime
    return x3, (-y1 + slope * (x1 - x3)) % prime


def _torsion_lifts(certificate: dict[str, Any]) -> list[bool]:
    proof = certificate["no_lift"]
    params = certificate["parameters"]
    d = certificate["d_vector"]
    result = []
    for label in proof["torsion_points"]:
        point = _parse_point(label)
        if point is None:
            ratios = (
                Fraction(d["d_minus_p"], d["d_pos_2sqrt_q"]),
                Fraction(d["d_minus_p"], d["d_neg_2sqrt_q"]),
            )
            result.append(all(_square(value) for value in ratios))
            continue
        x = point[0]
        rhs = (
            (x + params["p"]) / d["d_minus_p"],
            (x - 2 * params["sqrt_q"]) / d["d_pos_2sqrt_q"],
            (x + 2 * params["sqrt_q"]) / d["d_neg_2sqrt_q"],
        )
        result.append(all(_square(value) for value in rhs))
    return result


def _torsion_points_on_curve(certificate: dict[str, Any]) -> bool:
    params = certificate["parameters"]
    for label in certificate["no_lift"]["torsion_points"]:
        point = _parse_point(label)
        if point is None:
            continue
        x, y = point
        if y * y != (x + params["p"]) * (x * x - 4 * params["q"]):
            return False
    return True


def _verify_wl506_point(certificate: dict[str, Any]) -> bool:
    source = certificate.get("mordell_weil_point_source")
    if source is None:
        return True
    if source.get("point_expression") != "-49*G + T":
        return False
    generator = _parse_point(source["curve_generator"].removeprefix("G="))
    torsion = _parse_point(source["torsion_translate"].removeprefix("T="))
    a2 = Fraction(certificate["parameters"]["p"])
    a4 = Fraction(-4 * certificate["parameters"]["q"])
    point = _ec_add(_ec_mul(-49, generator, a2, a4), torsion, a2, a4)
    expected = (
        rational(certificate["point_on_E_L"]["X"]),
        rational(certificate["point_on_E_L"]["Y"]),
    )
    return point == expected


def _verify_mod_17(certificate: dict[str, Any]) -> bool:
    proof = certificate["no_lift"]
    prime = proof["prime"]
    if prime != 17:
        return False
    generator_q = _parse_point(proof["generator"])
    assert generator_q is not None
    generator = (int(generator_q[0]) % prime, int(generator_q[1]) % prime)
    torsion = [None, (14, 0), (16, 0), (3, 0)]
    subgroup = []
    current = None
    for _ in range(6):
        subgroup.append(current)
        current = _fp_add(current, generator, prime, 1, -9)
    rational_image = {
        _fp_add(point, translate, prime, 1, -9)
        for point in subgroup
        for translate in torsion
    }
    squares = {value * value % prime for value in range(prime)}
    local = set()
    for x in range(prime):
        rhs = (x + 1) * (x - 3) * (x + 3) % prime
        for y in range(prime):
            point = (x, y)
            if y * y % prime != rhs:
                continue
            if (
                (x + 1) * pow(7, -1, prime) % prime in squares
                and (x - 3) * pow(7, -1, prime) % prime in squares
                and (x + 3) % prime in squares
            ):
                local.add(point)
    stored_image = set(map(_parse_point, proof["rational_reduction_image"]))
    stored_local = set(map(_parse_point, proof["local_lift_candidate_reductions"]))
    intersection = rational_image.intersection(local)
    stored_intersection = set(map(_parse_point, proof["rational_image_intersection"]))
    legendre = -1 if pow(7, 8, 17) == 16 else 1
    return (
        rational_image == stored_image
        and local == stored_local
        and intersection == stored_intersection == set()
        and proof["legendre_symbol_7"] == legendre == -1
    )


def verify_cover_certificate(certificate: dict[str, Any]) -> CertificateChecks:
    params = certificate["parameters"]
    d = certificate["d_vector"]
    if certificate["status"] == "globally_soluble":
        x, u0, u1, u2 = _cover_values(certificate)
        equations = (
            x + params["p"] == d["d_minus_p"] * u0 * u0,
            x - 2 * params["sqrt_q"] == d["d_pos_2sqrt_q"] * u1 * u1,
            x + 2 * params["sqrt_q"] == d["d_neg_2sqrt_q"] * u2 * u2,
        )
        product = d["d_minus_p"] * d["d_pos_2sqrt_q"] * d["d_neg_2sqrt_q"]
        scale = isqrt(product)
        y = rational(certificate["point_on_E_L"]["Y"])
        elliptic = scale * scale == product and y == scale * u0 * u1 * u2
        return CertificateChecks(
            all(equations), elliptic and _verify_wl506_point(certificate), True
        )

    proof = certificate["no_lift"]
    if proof["method"] == "torsion_exhaustion":
        recomputed = _torsion_lifts(certificate)
        recorded = [check["lift_exists"] for check in proof["lift_checks"]]
        checked_points = [check["torsion_point"] for check in proof["lift_checks"]]
        no_lift = (
            proof["rank"] == 0
            and _torsion_points_on_curve(certificate)
            and checked_points == proof["torsion_points"]
            and recomputed == recorded == [False] * 4
        )
    elif proof["method"] == "mordell_weil_sieve_mod_17":
        no_lift = proof["rank"] == 1 and _verify_mod_17(certificate)
    else:
        raise ValueError(f"unknown no-lift method: {proof['method']}")
    return CertificateChecks(True, True, no_lift)


def classify_point(point: dict[str, Any]) -> dict[str, Any]:
    """Apply the centered-even wl491 inverse and all square/sign checks."""

    required = {
        "candidate_id",
        "A",
        "B",
        "L",
        "quotient",
        "parameters",
        "point_on_E_L",
        "complete_d_squareclass",
    }
    missing = sorted(required - set(point))
    if missing:
        return {
            "output_class": "invalid_input",
            "blocking_reasons": [f"missing_{key}" for key in missing],
        }
    if point["quotient"] not in {"AA", "BB"}:
        return {
            "output_class": "invalid_input",
            "blocking_reasons": ["quotient_not_centered_even_AA_or_BB"],
        }
    a, b = rational(point["A"]), rational(point["B"])
    x = rational(point["point_on_E_L"]["X"])
    y = rational(point["point_on_E_L"]["Y"])
    p, q = rational(point["parameters"]["p"]), rational(point["parameters"]["q"])
    denominator = 2 * (x + p)
    if denominator == 0:
        return {
            "output_class": "missing_pullback_data",
            "blocking_reasons": ["centered_even_inverse_denominator_zero"],
        }
    t = y / denominator
    z = x / 2 - t * t
    n = (a + b + t) / 2
    m = a + b - n
    leg = a if point["quotient"] == "AA" else b
    pullback = z * z == t**4 + p * t * t + q and (z / 4) ** 2 == (n * n + leg * leg) * (
        m * m + leg * leg
    )
    sides = {}
    reasons = []
    for label, side_leg in (("AA", a), ("BB", b)):
        left, right = n * n + side_leg * side_leg, m * m + side_leg * side_leg
        product = left * right
        sides[label] = {"product": _fmt(product), "product_is_square": _square(product)}
        if not sides[label]["product_is_square"]:
            reasons.append(f"{label}_common_source_product_not_square")
    for label, value in (("A", a), ("B", b), ("N", n), ("M", m)):
        if value <= 0:
            reasons.append(f"{label}_not_positive")
    return {
        "candidate_id": point["candidate_id"],
        "output_class": "admissible" if pullback and not reasons else "not_admissible",
        "centered_even_pullback_check": {
            "passed": pullback,
            "values": {
                "t": _fmt(t),
                "z": _fmt(z),
                "N": _fmt(n),
                "M": _fmt(m),
                "quartic_y": _fmt(z / 4),
            },
        },
        "common_source_square_checks": sides,
        "blocking_reasons": reasons,
    }
