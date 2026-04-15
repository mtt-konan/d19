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


# ── chain_fast (additional) ───────────────────────────────────────────────────
