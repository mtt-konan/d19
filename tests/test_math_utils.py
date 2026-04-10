"""Tests for math_utils."""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rational_distance.math_utils import (
    primitive_pythagorean_triples,
    rational_sqrt,
)


def test_rational_sqrt_perfect_squares():
    assert rational_sqrt(Fraction(4)) == Fraction(2)
    assert rational_sqrt(Fraction(9)) == Fraction(3)
    assert rational_sqrt(Fraction(1, 4)) == Fraction(1, 2)
    assert rational_sqrt(Fraction(9, 25)) == Fraction(3, 5)
    assert rational_sqrt(Fraction(0)) == Fraction(0)


def test_rational_sqrt_non_squares():
    assert rational_sqrt(Fraction(2)) is None
    assert rational_sqrt(Fraction(3)) is None
    assert rational_sqrt(Fraction(1, 2)) is None
    assert rational_sqrt(Fraction(-1)) is None


def test_pythagorean_triples_basic():
    triples = primitive_pythagorean_triples(5)
    # (3,4,5) and (4,3,5) must be present
    assert (3, 4, 5) in triples
    assert (4, 3, 5) in triples
    # All must satisfy a²+b²=c²
    for a, b, c in triples:
        assert a * a + b * b == c * c, f"Triple {(a,b,c)} fails"


def test_pythagorean_triples_primitive():
    from math import gcd
    triples = primitive_pythagorean_triples(10)
    for a, b, c in triples:
        # gcd of all three is 1 for primitive triples
        assert gcd(gcd(a, b), c) == 1, f"Non-primitive: {(a,b,c)}"
