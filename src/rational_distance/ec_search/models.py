"""Data models for EC search traces."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from rational_distance.square import RationalPoint


@dataclass(frozen=True)
class ECSeedRecord:
    seed_index: int
    a: int
    b: int
    k: Fraction
    dB: Fraction
    dD: Fraction


@dataclass
class ECCurveNodeRecord:
    node_index: int
    t: Fraction
    E: Fraction
    kind: str
    step: int
    seed_index: int | None = None
    active: bool = False


@dataclass(frozen=True)
class ECCurveEdgeRecord:
    child_index: int
    parent_index: int
    relation: str
    position: int = 0


@dataclass(frozen=True)
class ECCandidateRecord:
    candidate_index: int
    source_kind: str
    source_seed_index: int | None
    source_node_index: int | None
    k: Fraction | None
    status: str
    x: Fraction | None = None
    y: Fraction | None = None
    point: RationalPoint | None = None
    canonical_xy: tuple[Fraction, Fraction] | None = None


@dataclass(frozen=True)
class ECSeedBranch:
    seed_index: int
    t: Fraction
    E: Fraction


@dataclass
class ECOrbitTrace:
    nodes: list[ECCurveNodeRecord]
    edges: list[ECCurveEdgeRecord]
    active_node_indices: list[int]
    seed_primary_nodes: dict[int, int]


@dataclass
class ECTripleTrace:
    p: int
    q: int
    r: int
    seeds: list[ECSeedRecord]
    nodes: list[ECCurveNodeRecord]
    edges: list[ECCurveEdgeRecord]
    candidates: list[ECCandidateRecord]

    def accepted_points(self) -> list[RationalPoint]:
        return [candidate.point for candidate in self.candidates if candidate.status == "accepted"]


__all__ = [
    "ECCandidateRecord",
    "ECCurveEdgeRecord",
    "ECCurveNodeRecord",
    "ECOrbitTrace",
    "ECSeedBranch",
    "ECSeedRecord",
    "ECTripleTrace",
]
