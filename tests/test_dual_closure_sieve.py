"""Tests for the dual chain-closure mod p² sieve."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.chain_closure_sieve import STANDARD_MODULI
from rational_distance.concordant.dual_closure_sieve import (
    all_n_pairs_killed,
    dual_pair_killed,
    find_surviving_n_pair,
)
from rational_distance.concordant.factor_search import find_concordant_by_factorization


class TestDualPairKilled:
    def test_self_pair_is_killed_with_sentinel(self) -> None:
        # Degenerate self-pair: returns 0 sentinel meaning "killed".
        assert dual_pair_killed(100, 100) == 0

    def test_known_killed_pair_for_26611_680561(self) -> None:
        # The unique k=2 hard_case at max_hyp=10000 is (26611, 680561) with
        # concordant N = [48048, 89148]. Reduced (4004, 7429) is killed at
        # mod 53² = 2809.
        ns = find_concordant_by_factorization(26611, 680561)
        assert ns == [48048, 89148]
        killer = dual_pair_killed(ns[0], ns[1], STANDARD_MODULI)
        assert killer == 2809


class TestAllNPairsKilled:
    def test_empty_returns_true(self) -> None:
        assert all_n_pairs_killed([]) is True

    def test_single_n_returns_true(self) -> None:
        assert all_n_pairs_killed([42]) is True

    def test_known_multi_n_pair_all_killed(self) -> None:
        ns = find_concordant_by_factorization(26611, 680561)
        assert len(ns) == 2
        assert all_n_pairs_killed(ns, STANDARD_MODULI) is True


class TestFindSurvivingNPair:
    def test_returns_none_when_all_killed(self) -> None:
        ns = find_concordant_by_factorization(26611, 680561)
        assert find_surviving_n_pair(ns, STANDARD_MODULI) is None

    def test_returns_none_for_too_few_ns(self) -> None:
        assert find_surviving_n_pair([], STANDARD_MODULI) is None
        assert find_surviving_n_pair([7], STANDARD_MODULI) is None
