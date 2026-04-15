"""Tests for pair generation and concordant analysis."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


class TestPairGenerator:
    """Tests for the (A, B) pair generator."""

    def test_returns_sorted_list(self):
        from rational_distance.pair_generator import generate_ab_pairs

        pairs = generate_ab_pairs(50)
        assert isinstance(pairs, list)
        assert pairs == sorted(pairs)

    def test_all_coprime(self):
        """All returned pairs should have gcd(A, B) = 1."""
        from math import gcd

        from rational_distance.pair_generator import generate_ab_pairs

        for a, b in generate_ab_pairs(100):
            assert gcd(a, b) == 1, f"gcd({a},{b}) != 1"

    def test_a_le_b(self):
        """All pairs should satisfy A ≤ B."""
        from rational_distance.pair_generator import generate_ab_pairs

        for a, b in generate_ab_pairs(100):
            assert a <= b, f"A={a} > B={b}"

    def test_count_increases_with_max_hyp(self):
        from rational_distance.pair_generator import generate_ab_pairs

        n50 = len(generate_ab_pairs(50))
        n100 = len(generate_ab_pairs(100))
        assert n100 > n50

    def test_known_pair_present(self):
        """The pair (22, 35) = reduced (264, 420) should appear."""
        from rational_distance.pair_generator import generate_ab_pairs

        pairs = generate_ab_pairs(500)
        assert (22, 35) in pairs


class TestConcordantEC:
    """Tests for the elliptic curve concordant-form analysis."""

    def test_compute_rank_264_420(self):
        """Known pair (264, 420) has rank 2."""
        from rational_distance.concordant_ec import compute_rank

        rank, bounds, gens = compute_rank(264, 420)
        assert rank == 2
        assert bounds == (2, 2)
        assert len(gens) == 2

    def test_compute_rank_singular(self):
        """A == B gives singular curve, rank -1."""
        from rational_distance.concordant_ec import compute_rank

        rank, _bounds, _gens = compute_rank(5, 5)
        assert rank == -1

    def test_concordant_n_264_420(self):
        """Should find N=77, 315, 352 for (264, 420) with sufficient bound."""
        from rational_distance.concordant_ec import find_concordant_integers

        _, concordant = find_concordant_integers(264, 420, ec_bound=400000)
        assert 77 in concordant
        assert 315 in concordant
        assert 352 in concordant

    def test_concordant_n_verifies_squares(self):
        """All returned concordant N must satisfy N²+A²=□ and N²+B²=□."""
        from math import isqrt

        from rational_distance.concordant_ec import find_concordant_integers

        _, concordant = find_concordant_integers(264, 420, ec_bound=400000)
        for N in concordant:
            s1 = isqrt(N * N + 264 * 264)
            s2 = isqrt(N * N + 420 * 420)
            assert s1 * s1 == N * N + 264 * 264, f"N={N}: N²+A² not square"
            assert s2 * s2 == N * N + 420 * 420, f"N={N}: N²+B² not square"

    def test_chain_compatibility_known_failures(self):
        """Known concordant N values for (264, 420) fail chain constraint."""
        from rational_distance.concordant_ec import check_chain_compatibility

        for N in [77, 315, 352]:
            assert not check_chain_compatibility(264, 420, N)

    def test_chain_compatibility_positive_b(self):
        """b = A+B-N must be positive for chain compatibility."""
        from rational_distance.concordant_ec import check_chain_compatibility

        assert not check_chain_compatibility(10, 20, 100)

    def test_analyze_pair_no_normalize(self):
        """analyze_pair without normalization should use original A, B."""
        from rational_distance.concordant_ec import analyze_pair

        result = analyze_pair(264, 420, ec_bound=400000)
        assert result.A == 264
        assert result.B == 420
        assert result.rank == 2
        assert len(result.concordant_n) >= 3

    def test_analyze_pair_normalize(self):
        """analyze_pair with normalization should reduce by gcd."""
        from rational_distance.concordant_ec import analyze_pair

        result = analyze_pair(264, 420, ec_bound=400000, normalize=True)
        assert result.A == 22
        assert result.B == 35
        assert result.rank == 2

    def test_analyze_pair_no_chain_solutions(self):
        """No known chain-compatible concordant N should exist."""
        from rational_distance.concordant_ec import analyze_pair

        result = analyze_pair(264, 420, ec_bound=400000)
        assert not result.has_chain_solution

    def test_rank_0_still_has_concordant(self):
        """Even rank=0 pairs can have concordant N (from torsion points)."""
        from rational_distance.concordant_ec import analyze_pair

        result = analyze_pair(9, 16, ec_bound=100000)
        assert result.rank == 0
        assert 12 in result.concordant_n

    def test_enumerate_multiples_finds_known(self):
        """enumerate_multiples should find concordant N for (22, 35)."""
        from rational_distance.concordant_ec import enumerate_multiples

        conc = enumerate_multiples(22, 35, max_depth=5)
        assert 120 in conc

    def test_is_perfect_square(self):
        from rational_distance.concordant_ec import _is_perfect_square

        assert _is_perfect_square(0)
        assert _is_perfect_square(1)
        assert _is_perfect_square(4)
        assert _is_perfect_square(144)
        assert not _is_perfect_square(2)
        assert not _is_perfect_square(143)
        assert not _is_perfect_square(-1)

    def test_concordant_result_summary(self):
        """ConcordantResult.summary() should produce readable output."""
        from rational_distance.concordant_ec import ConcordantResult

        r = ConcordantResult(
            A=10, B=20, rank=1, rank_bounds=(1, 1),
            generators=[(100, 200)], concordant_n=[15],
            chain_compatible=[], ec_bound=100000,
            raw_square_x=[15],
        )
        s = r.summary()
        assert "rank=1" in s
        assert "concordant N" in s


class TestConcordantCompatibility:
    """Smoke tests for old and new concordant import paths."""

    def test_legacy_and_new_import_paths_are_available(self):
        from rational_distance.concordant import analyze_pair as new_analyze_pair
        from rational_distance.concordant import generate_ab_pairs as new_generate_ab_pairs
        from rational_distance.concordant_ec import analyze_pair as legacy_analyze_pair
        from rational_distance.pair_generator import generate_ab_pairs as legacy_generate_ab_pairs

        assert callable(new_analyze_pair)
        assert callable(new_generate_ab_pairs)
        assert callable(legacy_analyze_pair)
        assert callable(legacy_generate_ab_pairs)

