from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def test_mixed_closure_polynomials_for_known_pair() -> None:
    from rational_distance.concordant.mixed_closure_curves import closure_quotient_polynomials

    curves = closure_quotient_polynomials(3, 5)

    assert [curve.name for curve in curves] == ["AA", "BB", "AB", "BA"]
    assert {curve.name: curve.coeffs for curve in curves} == {
        "AA": (657, -144, 82, -16, 1),
        "BB": (2225, -400, 114, -16, 1),
        "AB": (801, -144, 98, -16, 1),
        "BA": (1825, -400, 98, -16, 1),
    }


def test_pari_polynomial_uses_constant_first_coefficients() -> None:
    from rational_distance.concordant.mixed_closure_curves import ClosureQuotientCurve

    curve = ClosureQuotientCurve(name="AB", A=3, B=5, coeffs=(1226, -320, 114, -16, 1))

    assert curve.pari_polynomial() == "x^4-16*x^3+114*x^2-320*x+1226"


def test_mixed_quotients_have_universal_affine_points() -> None:
    from fractions import Fraction

    from rational_distance.concordant.mixed_closure_curves import (
        closure_quotient_polynomials,
        evaluate_quartic,
    )

    A = 7
    B = 45
    curves = {curve.name: curve for curve in closure_quotient_polynomials(A, B)}

    universal_points = {
        "AB": {
            Fraction(A): Fraction(2 * A * B),
            Fraction(B): Fraction(A * A + B * B),
        },
        "BA": {
            Fraction(A): Fraction(A * A + B * B),
            Fraction(B): Fraction(2 * A * B),
        },
    }

    for curve_name, points in universal_points.items():
        curve = curves[curve_name]
        for n_value, y_value in points.items():
            assert evaluate_quartic(curve, n_value) == y_value * y_value


def test_batch_rank_records_pari_unavailable_without_crashing() -> None:
    from rational_distance.concordant.mixed_closure_curves import rank_mixed_closure_curves

    rows = rank_mixed_closure_curves([(3, 5)], pari=None, pari_available=False)

    assert len(rows) == 4
    assert {row["curve"] for row in rows} == {"AA", "BB", "AB", "BA"}
    assert all(row["status"] == "pari-unavailable" for row in rows)
    assert all(row["A"] == 3 and row["B"] == 5 for row in rows)


def test_rank_record_includes_root_number_when_pari_is_available() -> None:
    from rational_distance.concordant.analysis import _ensure_pari
    from rational_distance.concordant.mixed_closure_curves import (
        closure_quotient_polynomials,
        rank_closure_quotient,
    )

    pari = _ensure_pari()
    curve = next(c for c in closure_quotient_polynomials(9, 35) if c.name == "AA")

    row = rank_closure_quotient(curve, pari=pari)

    assert row["status"] == "ok"
    assert row["root_number"] in {-1, 1}


def test_hyperelliptic_points_are_classified_on_rank_zero_curve() -> None:
    from rational_distance.concordant.analysis import _ensure_pari
    from rational_distance.concordant.mixed_closure_curves import (
        classify_quartic_point,
        closure_quotient_polynomials,
        enumerate_quartic_points,
        evaluate_quartic,
    )

    pari = _ensure_pari()
    curve = next(c for c in closure_quotient_polynomials(9, 35) if c.name == "AA")

    points = enumerate_quartic_points(curve, height=100, pari=pari)

    assert {(point.x, point.y) for point in points} == {("22", "565"), ("22", "-565")}
    for point in points:
        assert evaluate_quartic(curve, point.x_fraction) == point.y_fraction**2
        classification = classify_quartic_point(curve, point)
        assert classification["is_midpoint"]
        assert not classification["is_full_closed_square"]


def test_rank_zero_even_quotient_torsion_certificate_pulls_back_all_affine_points() -> None:
    from rational_distance.concordant.analysis import _ensure_pari
    from rational_distance.concordant.mixed_closure_curves import (
        certify_rank_zero_even_quotient,
        closure_quotient_polynomials,
    )

    pari = _ensure_pari()
    curve = next(c for c in closure_quotient_polynomials(9, 35) if c.name == "AA")

    certificate = certify_rank_zero_even_quotient(curve, pari=pari)

    assert certificate["status"] == "certified"
    assert certificate["rank_lower"] == 0
    assert certificate["rank_upper"] == 0
    assert certificate["torsion_order"] == 4
    assert certificate["torsion_point_count"] == 4
    assert {
        point["reason"]
        for point in certificate["torsion_pullbacks"]
        if not point["has_affine_preimage"]
    } == {"point-at-infinity", "quartic-infinity"}
    assert certificate["affine_preimage_count"] == 2
    assert {point["N"] for point in certificate["affine_preimage_classifications"]} == {"22"}
    assert all(point["is_midpoint"] for point in certificate["affine_preimage_classifications"])
    assert not any(
        point["is_full_closed_square"]
        for point in certificate["affine_preimage_classifications"]
    )


def test_rank_zero_even_quotient_certificate_refuses_mixed_or_positive_rank_curve() -> None:
    from rational_distance.concordant.analysis import _ensure_pari
    from rational_distance.concordant.mixed_closure_curves import (
        certify_rank_zero_even_quotient,
        closure_quotient_polynomials,
    )

    pari = _ensure_pari()
    curves = closure_quotient_polynomials(7, 45)

    mixed = next(c for c in curves if c.name == "AB")
    positive_rank = next(c for c in curves if c.name == "AA")

    assert certify_rank_zero_even_quotient(mixed, pari=pari)["status"] == "unsupported-curve"
    assert certify_rank_zero_even_quotient(positive_rank, pari=pari)["status"] == "not-rank-zero"
