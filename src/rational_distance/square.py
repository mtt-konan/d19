"""Unit square geometry and rational-distance point type."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from rational_distance.math_utils import rational_sqrt

# The four vertices of the unit square, labelled A-D going counter-clockwise.
VERTICES: list[tuple[Fraction, Fraction]] = [
    (Fraction(0), Fraction(0)),  # A
    (Fraction(1), Fraction(0)),  # B
    (Fraction(1), Fraction(1)),  # C
    (Fraction(0), Fraction(1)),  # D
]
VERTEX_NAMES = ["A(0,0)", "B(1,0)", "C(1,1)", "D(0,1)"]


@dataclass(frozen=True)
class RationalPoint:
    """A point P=(x,y) with known rational distances to some square vertices.

    distances[i] is the distance to VERTICES[i], or None if irrational/unknown.
    """

    x: Fraction
    y: Fraction
    distances: tuple[Optional[Fraction], ...]  # length 4

    @property
    def rational_count(self) -> int:
        return sum(1 for d in self.distances if d is not None)

    def __str__(self) -> str:
        dstr = ", ".join(
            str(d) if d is not None else "?" for d in self.distances
        )
        return f"P=({self.x}, {self.y})  d=[{dstr}]  ({self.rational_count}/4 rational)"

    def as_dict(self) -> dict:
        return {
            "x": str(self.x),
            "y": str(self.y),
            "dA": str(self.distances[0]) if self.distances[0] else None,
            "dB": str(self.distances[1]) if self.distances[1] else None,
            "dC": str(self.distances[2]) if self.distances[2] else None,
            "dD": str(self.distances[3]) if self.distances[3] else None,
            "rational_count": self.rational_count,
        }


def compute_distances(
    x: Fraction, y: Fraction
) -> tuple[Optional[Fraction], ...]:
    """Compute rational distances from P=(x,y) to all four square vertices.

    Returns a 4-tuple; entry is None where the distance is irrational.
    """
    result: list[Optional[Fraction]] = []
    for vx, vy in VERTICES:
        d2 = (x - vx) ** 2 + (y - vy) ** 2
        result.append(rational_sqrt(d2))
    return tuple(result)


def make_point(x: Fraction, y: Fraction) -> RationalPoint:
    return RationalPoint(x=x, y=y, distances=compute_distances(x, y))
