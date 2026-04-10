"""Tests for square.py and search.py (smoke tests)."""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.square import VERTICES, compute_distances, make_point
from rational_distance.search import parametric_search, brute_force_search


def test_vertex_self_distance():
    """Distance from a vertex to itself is 0 (rational)."""
    for vx, vy in VERTICES:
        pt = make_point(vx, vy)
        zero = [d for d in pt.distances if d == Fraction(0)]
        assert len(zero) == 1


def test_known_3vertex_point():
    """Point (3/4, 0): d(A)=3/4, d(B)=1/4, d(D)=5/4 — all rational; d(C)=irrational."""
    x, y = Fraction(3, 4), Fraction(0)
    pt = make_point(x, y)
    assert pt.distances[0] == Fraction(3, 4)   # d(A) = 3/4
    assert pt.distances[1] == Fraction(1, 4)   # d(B) = 1/4
    assert pt.distances[3] == Fraction(5, 4)   # d(D) = sqrt(9/16+1) = 5/4
    # d(C) = sqrt((3/4-1)²+1) = sqrt(1/16+1) = sqrt(17/16) — irrational
    assert pt.distances[2] is None
    assert pt.rational_count == 3


def test_parametric_yields_3vertex():
    """Parametric search must yield at least some 3-vertex points quickly."""
    results = list(parametric_search(max_m=10, max_k_num=50, max_k_den=25, min_rational=3))
    assert len(results) > 0
    for pt in results:
        assert pt.rational_count >= 3


def test_brute_force_yields_known():
    """Brute-force with small denominator finds trivial vertex solutions."""
    results = list(brute_force_search(max_den=5, min_rational=2))
    xs = {(pt.x, pt.y) for pt in results}
    # Vertices themselves should appear (distance 0 is rational)
    assert (Fraction(0), Fraction(0)) in xs
    assert (Fraction(1), Fraction(0)) in xs
