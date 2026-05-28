"""Tests for chain search."""

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
        from rational_distance._legacy.search_chain import find_chains

        results = find_chains(max_val=313, progress=False)
        tuples = {(r.a, r.b, r.c, r.d) for r in results}
        assert (25, 60, 91, 312) in tuples, f"(25,60,91,312) not found; got {sorted(tuples)}"

    def test_cross_product_family_excluded(self):
        """Cross-product family (ac=bd) must be excluded from all results."""
        from rational_distance._legacy.search_chain import find_chains

        results = find_chains(max_val=500, progress=False)
        for r in results:
            assert r.a * r.c != r.b * r.d, f"Cross-product solution returned: {r}"

    def test_symmetric_cycles_excluded(self):
        """Cycles like (3,4,3,4) with repeated values must be excluded."""
        from rational_distance._legacy.search_chain import find_chains

        results = find_chains(max_val=500, progress=False)
        for r in results:
            assert len({r.a, r.b, r.c, r.d}) == 4, f"Non-distinct cycle returned: {r}"

    def test_hypotenuses_correct(self):
        """Hypotenuses must equal isqrt of the respective sum of squares."""
        from rational_distance._legacy.search_chain import find_chains

        for r in find_chains(max_val=500, progress=False):
            assert r.x1**2 == r.a**2 + r.b**2, f"x1 wrong for {r}"
            assert r.x2**2 == r.b**2 + r.c**2, f"x2 wrong for {r}"
            assert r.x3**2 == r.c**2 + r.d**2, f"x3 wrong for {r}"
            assert r.x4**2 == r.d**2 + r.a**2, f"x4 wrong for {r}"

    def test_canonical_no_duplicates(self):
        """Canonical mode must return no two tuples related by dihedral symmetry."""
        from rational_distance._legacy.search_chain import _symmetry_group, find_chains

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
        from rational_distance._legacy.search_chain import find_chains

        results = find_chains(max_val=500, require_square=True, progress=False)
        assert results == [], f"Unexpected square solution found: {results[0]}"

    def test_square_ok_flag(self):
        """square_ok must correctly reflect a+c == b+d."""
        from rational_distance._legacy.search_chain import find_chains

        for r in find_chains(max_val=500, progress=False):
            assert r.square_ok == (r.a + r.c == r.b + r.d)

    def test_chain_result_str(self):
        """ChainResult.__str__ must include edge decomposition lines."""
        from rational_distance._legacy.search_chain import find_chains

        results = find_chains(max_val=313, progress=False)
        assert results, "No results to test"
        s = str(results[0])
        # Must have four edge lines with x1..x4 labels and →
        assert "x1:" in s
        assert "x2:" in s
        assert "x3:" in s
        assert "x4:" in s
        assert "→" in s

    def test_diagonal_sign_sieve_rejects_smallest_general_family_cycle(self):
        """The experimental diagonal sign sieve should reject (25,60,91,312)."""
        from rational_distance._legacy.search_chain import find_chains, passes_diagonal_sign_sieve

        results = find_chains(max_val=313, progress=False)
        target = next(
            result
            for result in results
            if (result.a, result.b, result.c, result.d) == (25, 60, 91, 312)
        )
        assert passes_diagonal_sign_sieve(target) is False

    def test_diagonal_sign_sieve_keeps_known_small_example(self):
        """The experimental diagonal sign sieve should keep at least one small 4-cycle."""
        from rational_distance._legacy.search_chain import find_chains, passes_diagonal_sign_sieve

        results = find_chains(max_val=400, progress=False)
        target = next(
            result
            for result in results
            if (result.a, result.b, result.c, result.d) == (65, 72, 320, 156)
        )
        assert passes_diagonal_sign_sieve(target) is True

    def test_diagonal_sign_sieve_matches_manual_filter(self):
        """Direct diagonal-sign mode must match manual post-filtering on canonical results."""
        from rational_distance._legacy.search_chain import find_chains, passes_diagonal_sign_sieve

        default_results = find_chains(max_val=500, progress=False)
        direct_results = find_chains(max_val=500, diagonal_sign_sieve=True, progress=False)
        manual_results = [
            result for result in default_results if passes_diagonal_sign_sieve(result)
        ]

        assert [(r.a, r.b, r.c, r.d) for r in direct_results] == [
            (r.a, r.b, r.c, r.d) for r in manual_results
        ]

    def test_diagonal_sign_sieve_square_mode_matches_manual_filter(self):
        """Square-only diagonal-sign mode must match filtering the square-only result set."""
        from rational_distance._legacy.search_chain import find_chains, passes_diagonal_sign_sieve

        default_square = find_chains(max_val=500, require_square=True, progress=False)
        direct_square = find_chains(
            max_val=500,
            require_square=True,
            diagonal_sign_sieve=True,
            progress=False,
        )
        manual_square = [result for result in default_square if passes_diagonal_sign_sieve(result)]

        assert [(r.a, r.b, r.c, r.d) for r in direct_square] == [
            (r.a, r.b, r.c, r.d) for r in manual_square
        ]

    def test_diagonal_sign_stats_report_search_stage_counts(self):
        """Search stats must reflect canonical counts before and after the sieve."""
        from rational_distance._legacy.search_chain import ChainSearchStats, find_chains

        stats = ChainSearchStats()
        results = find_chains(max_val=500, diagonal_sign_sieve=True, progress=False, stats=stats)

        assert len(results) == 2
        assert stats.pre_diagonal_results == 10
        assert stats.diagonal_sign_filtered == 8
        assert stats.emitted_results == 2


# ── chain_fast (additional) ───────────────────────────────────────────────────
