"""Tests for the F₂-rank classifier on concordant-N half-point images."""

from __future__ import annotations

import pytest

from rational_distance.concordant.two_descent_rank import (
    F2RankResult,
    f2_rank_of_concordant_pair,
)


class TestThreeNPair:
    """`(153, 560)` has three concordant N: 204, 420, 3900."""

    def test_returns_dataclass(self) -> None:
        result = f2_rank_of_concordant_pair(153, 560, [204, 420, 3900])
        assert isinstance(result, F2RankResult)
        assert result.A == 153
        assert result.B == 560
        assert result.ns == (204, 420, 3900)

    def test_three_concordant_n_are_independent(self) -> None:
        """All three half-point images independent in (Q*/Q*²)²."""
        result = f2_rank_of_concordant_pair(153, 560, [204, 420, 3900])
        assert result.f2_rank == 3
        assert result.minimal_relation is None

    def test_image_first_coords_match_known_signatures(self) -> None:
        """Sanity check: positive-sig first coords from previous analysis."""
        result = f2_rank_of_concordant_pair(153, 560, [204, 420, 3900])
        assert result.images[0][0] == 102   # N=204
        assert result.images[1][0] == 210   # N=420
        assert result.images[2][0] == 30    # N=3900


class TestK4Pairs:
    """The three k=4 pairs from `max_hyp=50000`."""

    def test_pair_11776_17199_has_rank_3_with_relation(self) -> None:
        result = f2_rank_of_concordant_pair(
            11776, 17199, [3960, 4368, 46368, 541632]
        )
        assert result.f2_rank == 3
        assert result.minimal_relation == (3960, 4368, 541632)

    def test_pair_6669_26656_has_rank_3_with_relation(self) -> None:
        result = f2_rank_of_concordant_pair(
            6669, 26656, [8892, 13860, 19992, 91392]
        )
        assert result.f2_rank == 3
        assert result.minimal_relation == (13860, 19992, 91392)

    def test_pair_7337_28288_has_rank_4_no_relation(self) -> None:
        result = f2_rank_of_concordant_pair(
            7337, 28288, [1716, 5916, 31584, 84216]
        )
        assert result.f2_rank == 4
        assert result.minimal_relation is None


class TestEdgeCases:
    def test_empty_n_list_is_rank_zero(self) -> None:
        result = f2_rank_of_concordant_pair(153, 560, [])
        assert result.f2_rank == 0
        assert result.minimal_relation is None
        assert result.images == ()

    def test_single_n_is_rank_one(self) -> None:
        result = f2_rank_of_concordant_pair(153, 560, [204])
        assert result.f2_rank == 1
        assert result.minimal_relation is None

    def test_invalid_n_raises(self) -> None:
        """N must be concordant for (A, B); otherwise no half-point exists."""
        with pytest.raises(ValueError):
            f2_rank_of_concordant_pair(153, 560, [7])
