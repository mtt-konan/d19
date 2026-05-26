"""Unit square geometry and rational-distance point type."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm

from rational_distance.math_utils import rational_sqrt

# The four vertices of the unit square, labelled A-D going counter-clockwise.
VERTICES: list[tuple[Fraction, Fraction]] = [
    (Fraction(0), Fraction(0)),  # A
    (Fraction(1), Fraction(0)),  # B
    (Fraction(1), Fraction(1)),  # C
    (Fraction(0), Fraction(1)),  # D
]
VERTEX_NAMES = ["A(0,0)", "B(1,0)", "C(1,1)", "D(0,1)"]

_ONE = Fraction(1)


def d4_images(x: Fraction, y: Fraction) -> list[tuple[Fraction, Fraction]]:
    """Return the (up to) 8 images of (x,y) under the D4 symmetry group of
    the unit square.  Some images coincide when the point lies on a symmetry
    axis, so the returned list may have fewer than 8 distinct elements.

    The 8 transformations (center = (1/2, 1/2)):
        identity, flip-x, flip-y, 180°,
        flip-diagonal, flip-antidiagonal, 90°-CW, 90°-CCW
    """
    return list(
        {
            (x, y),
            (_ONE - x, y),
            (x, _ONE - y),
            (_ONE - x, _ONE - y),
            (y, x),
            (_ONE - y, _ONE - x),
            (y, _ONE - x),
            (_ONE - y, x),
        }
    )


def canonical_xy(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    """Return the lexicographically smallest D4 image — the canonical
    representative of the orbit.  Used to deduplicate symmetric solutions."""
    return min(d4_images(x, y))


@dataclass(frozen=True)
class RationalPoint:
    """A point P=(x,y) with known rational distances to some square vertices.

    distances[i] is the distance to VERTICES[i], or None if irrational/unknown.
    """

    x: Fraction
    y: Fraction
    distances: tuple[Fraction | None, ...]  # length 4

    @property
    def rational_count(self) -> int:
        return sum(1 for d in self.distances if d is not None)

    @property
    def denominator(self) -> int:
        """LCM of x and y denominators — a measure of solution complexity."""
        return lcm(self.x.denominator, self.y.denominator)

    def __str__(self) -> str:
        dstr = ", ".join(str(d) if d is not None else "?" for d in self.distances)
        return f"P=({self.x}, {self.y})  d=[{dstr}]  ({self.rational_count}/4 rational)"

    def as_dict(self) -> dict:
        return {
            "x": str(self.x),
            "y": str(self.y),
            "dA": str(self.distances[0]) if self.distances[0] is not None else None,
            "dB": str(self.distances[1]) if self.distances[1] is not None else None,
            "dC": str(self.distances[2]) if self.distances[2] is not None else None,
            "dD": str(self.distances[3]) if self.distances[3] is not None else None,
            "rational_count": self.rational_count,
            "denominator": self.denominator,
        }


def compute_distances(x: Fraction, y: Fraction) -> tuple[Fraction | None, ...]:
    """Compute rational distances from P=(x,y) to all four square vertices.

    Returns a 4-tuple; entry is None where the distance is irrational.
    """
    result: list[Fraction | None] = []
    for vx, vy in VERTICES:
        d2 = (x - vx) ** 2 + (y - vy) ** 2
        result.append(rational_sqrt(d2))
    return tuple(result)


def make_point(x: Fraction, y: Fraction) -> RationalPoint:
    return RationalPoint(x=x, y=y, distances=compute_distances(x, y))
