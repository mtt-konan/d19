"""Tests for chain search, pair generation, and concordant analysis."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

class TestChainSearch:
    """Tests for the Pythagorean 4-cycle search module."""

    def test_known_general_family_cycle(self):
        """(25,60,91,312) is the smallest general-family (ac≠bd) 4-cycle."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=313, progress=False)
        tuples = {(r.a, r.b, r.c, r.d) for r in results}
        assert (25, 60, 91, 312) in tuples, f"(25,60,91,312) not found; got {sorted(tuples)}"

    def test_cross_product_family_excluded(self):
        """Cross-product family (ac=bd) must be excluded from all results."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=500, progress=False)
        for r in results:
            assert r.a * r.c != r.b * r.d, f"Cross-product solution returned: {r}"

    def test_symmetric_cycles_excluded(self):
        """Cycles like (3,4,3,4) with repeated values must be excluded."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=500, progress=False)
        for r in results:
            assert len({r.a, r.b, r.c, r.d}) == 4, f"Non-distinct cycle returned: {r}"

    def test_hypotenuses_correct(self):
        """Hypotenuses must equal isqrt of the respective sum of squares."""
        from rational_distance.search_chain import find_chains

        for r in find_chains(max_val=500, progress=False):
            assert r.x1**2 == r.a**2 + r.b**2, f"x1 wrong for {r}"
            assert r.x2**2 == r.b**2 + r.c**2, f"x2 wrong for {r}"
            assert r.x3**2 == r.c**2 + r.d**2, f"x3 wrong for {r}"
            assert r.x4**2 == r.d**2 + r.a**2, f"x4 wrong for {r}"

    def test_canonical_no_duplicates(self):
        """Canonical mode must return no two tuples related by dihedral symmetry."""
        from rational_distance.search_chain import _symmetry_group, find_chains

        results = find_chains(max_val=500, canonical=True, progress=False)
        keys: set[tuple[int, int, int, int]] = set()
        for r in results:
            syms = _symmetry_group(r.a, r.b, r.c, r.d)
            for sym in syms:
                assert sym not in keys or sym == min(syms), (
                    f"Duplicate via symmetry: {(r.a, r.b, r.c, r.d)} and {sym}"
                )
            keys.add(min(syms))

    def test_no_square_solutions_small(self):
        """No general-family 4-cycle with a+c == b+d exists up to max_val=500.
        This is consistent with the Harborth conjecture."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=500, require_square=True, progress=False)
        assert results == [], f"Unexpected square solution found: {results[0]}"

    def test_square_ok_flag(self):
        """square_ok must correctly reflect a+c == b+d."""
        from rational_distance.search_chain import find_chains

        for r in find_chains(max_val=500, progress=False):
            assert r.square_ok == (r.a + r.c == r.b + r.d)

    def test_chain_result_str(self):
        """ChainResult.__str__ must include edge decomposition lines."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=313, progress=False)
        assert results, "No results to test"
        s = str(results[0])
        # Must have four edge lines with x1..x4 labels and →
        assert "x1:" in s
        assert "x2:" in s
        assert "x3:" in s
        assert "x4:" in s
        assert "→" in s


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


# ── concordant_ec ─────────────────────────────────────────────────────────────


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


# ── chain_fast (additional) ───────────────────────────────────────────────────
