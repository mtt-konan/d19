"""Tests for chain-fast search behavior and profiling."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

class TestChainFast:
    """Tests for the O(n²) primitive-triple-pair chain search."""

    def test_returns_list(self):
        """find_chains_fast should return an empty list (no Harborth solution known)."""
        from rational_distance.search_chain_fast import find_chains_fast

        results = find_chains_fast(max_hyp=200, progress=False)
        assert isinstance(results, list)

    def test_all_results_square_ok(self):
        """All results must satisfy a+c == b+d by construction."""
        from rational_distance.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert r.square_ok, f"square_ok should be True: {r}"
            assert r.a + r.c == r.b + r.d, f"a+c != b+d: {r}"

    def test_pythagorean_conditions(self):
        """All four hypotenuses must be correct integer square roots."""
        from rational_distance.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert r.x1 ** 2 == r.a ** 2 + r.b ** 2, f"x1 wrong: {r}"
            assert r.x2 ** 2 == r.b ** 2 + r.c ** 2, f"x2 wrong: {r}"
            assert r.x3 ** 2 == r.c ** 2 + r.d ** 2, f"x3 wrong: {r}"
            assert r.x4 ** 2 == r.d ** 2 + r.a ** 2, f"x4 wrong: {r}"


# ── pair_generator ────────────────────────────────────────────────────────────


class TestChainFastAdditional:
    """Additional tests for chain-fast (originally in TestChainFast)."""

    def test_no_cross_product_family(self):
        """No result should belong to the cross-product family (ac == bd)."""
        from rational_distance.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert r.a * r.c != r.b * r.d, f"Cross-product family found: {r}"

    def test_all_distinct(self):
        """All four values a,b,c,d must be distinct."""
        from rational_distance.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert len({r.a, r.b, r.c, r.d}) == 4, f"Non-distinct: {r}"

    def test_no_duplicates(self):
        """No two results should be equivalent under the dihedral symmetry group."""
        from rational_distance.search_chain import _symmetry_group
        from rational_distance.search_chain_fast import find_chains_fast

        results = find_chains_fast(max_hyp=500, progress=False)
        keys: set[tuple[int, int, int, int]] = set()
        for r in results:
            syms = _symmetry_group(r.a, r.b, r.c, r.d)
            key = min(syms)
            assert key not in keys, f"Duplicate via symmetry: {(r.a,r.b,r.c,r.d)}"
            keys.add(key)

    def test_consistent_with_chain_no_solution(self):
        """Both search methods should agree: no unit-square solution in small range."""
        from rational_distance.search_chain import find_chains
        from rational_distance.search_chain_fast import find_chains_fast

        fast = find_chains_fast(max_hyp=200, progress=False)
        slow = find_chains(max_val=200, require_square=True, progress=False)
        assert fast == [] and slow == [], (
            f"Unexpected results: fast={fast}, slow={slow}"
        )


# ── chain-fast numpy backend ──────────────────────────────────────────────────


class TestChainFastNumpy:
    """Tests for the numpy-vectorised backend of find_chains_fast."""

    def test_numpy_matches_python(self):
        """numpy and python backends must return identical results."""
        from rational_distance.search_chain_fast import find_chains_fast

        py = find_chains_fast(max_hyp=300, progress=False, backend="python")
        np_ = find_chains_fast(max_hyp=300, progress=False, backend="numpy")
        assert py == np_

    def test_auto_selects_numpy(self):
        """backend='auto' should choose numpy when it is available."""
        from rational_distance.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        # Should not raise; confirms numpy path runs without error.
        find_chains_fast(max_hyp=200, progress=False, backend="auto")

    def test_numpy_backend_forced(self):
        """backend='numpy' should not raise for safe max_hyp values."""
        from rational_distance.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        find_chains_fast(max_hyp=500, progress=False, backend="numpy")

    def test_numpy_overflow_guard(self):
        """backend='numpy' with max_hyp > _NUMPY_MAX_HYP must raise ValueError."""
        from rational_distance.search_chain_fast import (
            _HAS_NUMPY,
            _NUMPY_MAX_HYP,
            find_chains_fast,
        )

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        with pytest.raises(ValueError, match="int64-safe threshold"):
            find_chains_fast(max_hyp=_NUMPY_MAX_HYP + 1, progress=False, backend="numpy")

    def test_near_miss_callback_fires_same_count(self):
        """near_miss_callback should fire the same number of times for both backends."""
        from rational_distance.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        py_hits: list = []
        np_hits: list = []
        find_chains_fast(max_hyp=500, progress=False, backend="python",
                         near_miss_callback=lambda *a: py_hits.append(a))
        find_chains_fast(max_hyp=500, progress=False, backend="numpy",
                         near_miss_callback=lambda *a: np_hits.append(a))
        assert len(py_hits) == len(np_hits), (
            f"near_miss count differs: python={len(py_hits)}, numpy={len(np_hits)}"
        )

    def test_start_t1_resumes_subset(self):
        """start_t1=k should return a subset of the full run's results."""
        from rational_distance.search_chain_fast import find_chains_fast

        full = find_chains_fast(max_hyp=300, progress=False, backend="python")
        partial = find_chains_fast(max_hyp=300, progress=False, backend="python", start_t1=5)
        # partial is a strict subset (same or fewer results)
        for r in partial:
            assert r in full, f"partial result not in full: {r}"

    def test_python_workers_match_single_process(self):
        """workers>1 must preserve the exact python-backend result set."""
        from rational_distance.search_chain_fast import find_chains_fast

        single = find_chains_fast(max_hyp=300, progress=False, backend="python", workers=1)
        parallel = find_chains_fast(max_hyp=300, progress=False, backend="python", workers=2)
        assert parallel == single

    def test_numpy_workers_match_single_process(self):
        """workers>1 must preserve the exact numpy-backend result set."""
        from rational_distance.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        single = find_chains_fast(max_hyp=300, progress=False, backend="numpy", workers=1)
        parallel = find_chains_fast(max_hyp=300, progress=False, backend="numpy", workers=2)
        assert parallel == single

    def test_parallel_start_t1_resumes_subset(self):
        """workers>1 with start_t1 should still return a subset of the full run."""
        from rational_distance.search_chain_fast import find_chains_fast

        full = find_chains_fast(max_hyp=300, progress=False, backend="python", workers=2)
        partial = find_chains_fast(
            max_hyp=300,
            progress=False,
            backend="python",
            workers=2,
            start_t1=5,
        )
        for r in partial:
            assert r in full, f"partial parallel result not in full: {r}"


# ── chain_db persistence ──────────────────────────────────────────────────────


class TestChainFastProfile:
    """Profile-oriented tests for chain-fast."""

    def test_run_chain_fast_profile_fields_python(self):
        """run_chain_fast(profile=True) should populate the expected fields."""
        from rational_distance.search_chain_fast import run_chain_fast

        execution = run_chain_fast(max_hyp=200, progress=False, backend="python", profile=True)
        profile = execution.profile.as_dict()
        assert set(profile) >= {
            "n_triples",
            "n_pairs_total",
            "n_pairs_after_basic_filters",
            "n_c3_pass",
            "n_c4_pass",
            "n_solutions_before_dedup",
            "n_solutions_after_dedup",
            "near_miss_seen",
            "near_miss_saved",
            "near_miss_dropped",
            "time_generate_triples_s",
            "time_filter_s",
            "time_c3_s",
            "time_c4_s",
            "time_dedup_s",
            "time_db_write_s",
            "db_bytes_after_run",
        }
        assert (
            profile["n_pairs_total"]
            >= profile["n_pairs_after_basic_filters"]
            >= profile["n_c3_pass"]
            >= profile["n_c4_pass"]
        )
        assert profile["n_solutions_before_dedup"] >= profile["n_solutions_after_dedup"]

    def test_run_chain_fast_profile_keys_match_numpy(self):
        """python and numpy profiled runs should expose the same profile keys."""
        from rational_distance.search_chain_fast import _HAS_NUMPY, run_chain_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        py_profile = run_chain_fast(
            max_hyp=200,
            progress=False,
            backend="python",
            profile=True,
        ).profile.as_dict()
        np_profile = run_chain_fast(
            max_hyp=200,
            progress=False,
            backend="numpy",
            profile=True,
        ).profile.as_dict()
        assert set(py_profile) == set(np_profile)

    def test_run_chain_fast_with_cached_triples_keeps_results(self):
        """Passing prebuilt triples should not change the result set."""
        from rational_distance.search_chain_fast import (
            build_chain_fast_triples,
            find_chains_fast,
            run_chain_fast,
        )

        triples = build_chain_fast_triples(300)
        base = find_chains_fast(max_hyp=300, progress=False, backend="python")
        cached = run_chain_fast(
            max_hyp=300,
            progress=False,
            backend="python",
            triples=triples,
            triples_source="provided-cache",
            profile=True,
        ).results
        assert cached == base
