"""Tests for cycle linear-relation tracking (wl086, OPEN_DIRECTIONS A.2)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.cycle_relations import (
    analyze_cycle_relations,
    concordant_point,
)


class TestConcordantPoint:
    def test_known_point_on_curve(self):
        # (264,420), N=77: 77^2+264^2=275^2, 77^2+420^2=427^2
        x, y = concordant_point(264, 420, 77)
        assert x == 77 * 77
        assert y == 77 * 275 * 427

    def test_non_concordant_raises(self):
        import pytest

        with pytest.raises(ValueError):
            concordant_point(264, 420, 78)


class TestCycleRelations:
    def test_420_1344_rank1_two_relations(self):
        res = analyze_cycle_relations(420, 1344, [560, 1008, 2925])
        assert res.rank == 1
        assert res.k == 3
        # rank-1 curve: three points collapse to a rank-1 sublattice -> 2 relations
        assert res.coord_matrix_rank == 1
        assert res.relation_count == 2
        assert res.all_two_divisible
        assert res.all_verified

    def test_264_420_rank2(self):
        res = analyze_cycle_relations(264, 420, [77, 315, 352, 1440])
        assert res.rank == 2
        assert res.coord_matrix_rank == 2
        assert res.relation_count == 2
        assert res.all_two_divisible
        assert res.all_verified

    def test_all_points_two_divisible_is_universal_on_sample(self):
        # The structural claim: every concordant point lies in 2*E(Q).
        sample = [
            (560, 2925, [420, 1344, 3900]),
            (1008, 2925, [420, 1100, 1344, 7020]),
            (153, 560, [204, 420, 3900]),
        ]
        for A, B, ns in sample:
            res = analyze_cycle_relations(A, B, ns)
            assert res.all_two_divisible, f"({A},{B}) has a non-2-divisible Q_N"
            assert res.all_verified

    def test_relation_count_matches_coord_deficit(self):
        # #relations must equal k - coord_matrix_rank for every analyzed pair.
        for A, B, ns in [
            (420, 1344, [560, 1008, 2925]),
            (1344, 7020, [1008, 2925, 6992, 9360]),
            (153, 560, [204, 420, 3900]),  # MW rank 3 but coord rank 2 -> 1 relation
        ]:
            res = analyze_cycle_relations(A, B, ns)
            assert res.relation_count == res.k - res.coord_matrix_rank

    def test_153_560_deficit_zero_still_has_relation(self):
        # MW rank == k == 3 (k_minus_rank=0) yet the Q_N span only rank 2.
        res = analyze_cycle_relations(153, 560, [204, 420, 3900])
        assert res.k_minus_rank == 0
        assert res.coord_matrix_rank == 2
        assert res.relation_count == 1

    def test_relations_verified_exactly(self):
        res = analyze_cycle_relations(264, 420, [77, 315, 352, 1440])
        for rel in res.relations:
            assert rel.verified
            assert rel.residual_torsion_order in (1, 2, 4)
