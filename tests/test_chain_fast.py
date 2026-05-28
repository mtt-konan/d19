"""Tests for chain-fast search behavior and profiling."""

from __future__ import annotations

import sys
from math import gcd
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def _bucket_row_map(rows) -> dict[tuple[str, str], dict]:
    return {
        (row.bucket_type, row.bucket_key_json): row.as_dict()
        for row in rows
    }


def _bucket_totals_by_type(rows) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = {}
    for row in rows:
        current = totals.setdefault(
            row.bucket_type,
            {
                "n_total": 0,
                "n_after_basic": 0,
                "n_c3_pass": 0,
                "n_c4_pass": 0,
                "n_near_miss": 0,
            },
        )
        current["n_total"] += row.n_total
        current["n_after_basic"] += row.n_after_basic
        current["n_c3_pass"] += row.n_c3_pass
        current["n_c4_pass"] += row.n_c4_pass
        current["n_near_miss"] += row.n_near_miss
    return totals


class TestChainFast:
    """Tests for the O(n²) primitive-triple-pair chain search."""

    def test_returns_list(self):
        """find_chains_fast should return an empty list (no Harborth solution known)."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        results = find_chains_fast(max_hyp=200, progress=False)
        assert isinstance(results, list)

    def test_all_results_square_ok(self):
        """All results must satisfy a+c == b+d by construction."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert r.square_ok, f"square_ok should be True: {r}"
            assert r.a + r.c == r.b + r.d, f"a+c != b+d: {r}"

    def test_pythagorean_conditions(self):
        """All four hypotenuses must be correct integer square roots."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

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
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert r.a * r.c != r.b * r.d, f"Cross-product family found: {r}"

    def test_all_distinct(self):
        """All four values a,b,c,d must be distinct."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        for r in find_chains_fast(max_hyp=500, progress=False):
            assert len({r.a, r.b, r.c, r.d}) == 4, f"Non-distinct: {r}"

    def test_no_duplicates(self):
        """No two results should be equivalent under the dihedral symmetry group."""
        from rational_distance._legacy.search_chain import _symmetry_group
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        results = find_chains_fast(max_hyp=500, progress=False)
        keys: set[tuple[int, int, int, int]] = set()
        for r in results:
            syms = _symmetry_group(r.a, r.b, r.c, r.d)
            key = min(syms)
            assert key not in keys, f"Duplicate via symmetry: {(r.a,r.b,r.c,r.d)}"
            keys.add(key)

    def test_consistent_with_chain_no_solution(self):
        """Both search methods should agree: no unit-square solution in small range."""
        from rational_distance._legacy.search_chain import find_chains
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        fast = find_chains_fast(max_hyp=200, progress=False)
        slow = find_chains(max_val=200, require_square=True, progress=False)
        assert fast == [] and slow == [], (
            f"Unexpected results: fast={fast}, slow={slow}"
        )


class TestSafePairSieveHelpers:
    """Tests for the mathematically safe pair-sieve helpers."""

    def test_classify_orientation_for_both_orderings(self):
        """Each primitive triple orientation should map to OE or EO correctly."""
        from rational_distance.chain_fast.safe_pair_sieve import classify_orientation

        assert classify_orientation(3, 4) == "OE"
        assert classify_orientation(4, 3) == "EO"
        assert classify_orientation(5, 12) == "OE"
        assert classify_orientation(12, 5) == "EO"

    def test_v2_small_examples(self):
        """v2 should count the exact power of two dividing each input."""
        from rational_distance.chain_fast.safe_pair_sieve import v2

        assert v2(1) == 0
        assert v2(2) == 1
        assert v2(4) == 2
        assert v2(12) == 2
        assert v2(40) == 3

    def test_same_orientation_pairs_are_rejected(self):
        """(OE, OE) and (EO, EO) are proved-dead cases."""
        from rational_distance.chain_fast.safe_pair_sieve import decide_safe_pair_sieve

        assert decide_safe_pair_sieve(3, 4, 5, 12).allow_pair is False
        assert decide_safe_pair_sieve(4, 3, 12, 5).allow_pair is False

    def test_oe_eo_requires_matching_v2(self):
        """For T1=OE and T2=EO, mismatched v2 values must be rejected."""
        from rational_distance.chain_fast.safe_pair_sieve import decide_safe_pair_sieve

        decision = decide_safe_pair_sieve(3, 4, 8, 15)
        assert decision.allow_pair is False
        assert decision.require_n_multiple_of_4 is False

    def test_oe_eo_n_mod4_requirement_uses_actual_n(self):
        """The surviving OE/EO case must still satisfy N ≡ 0 (mod 4)."""
        from rational_distance.chain_fast.safe_pair_sieve import (
            decide_safe_pair_sieve,
            passes_n_mod4_requirement,
        )

        blocked = decide_safe_pair_sieve(3, 4, 12, 5)
        assert blocked.allow_pair is True
        assert blocked.require_n_multiple_of_4 is True
        g_blocked = gcd(4, 12)
        n_blocked = (4 // g_blocked) * 5 + (12 // g_blocked) * (3 - 4)
        assert n_blocked == 2
        assert passes_n_mod4_requirement(blocked, n_blocked) is False

        allowed = decide_safe_pair_sieve(3, 4, 20, 21)
        assert allowed.allow_pair is True
        assert allowed.require_n_multiple_of_4 is True
        g_allowed = gcd(4, 20)
        n_allowed = (4 // g_allowed) * 21 + (20 // g_allowed) * (3 - 4)
        assert n_allowed == 16
        assert passes_n_mod4_requirement(allowed, n_allowed) is True


# ── chain-fast numpy backend ──────────────────────────────────────────────────


class TestChainFastNumpy:
    """Tests for the numpy-vectorised backend of find_chains_fast."""

    def test_numpy_matches_python(self):
        """numpy and python backends must return identical results."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        py = find_chains_fast(max_hyp=300, progress=False, backend="python")
        np_ = find_chains_fast(max_hyp=300, progress=False, backend="numpy")
        assert py == np_

    def test_auto_selects_numpy(self):
        """backend='auto' should choose numpy when it is available."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        # Should not raise; confirms numpy path runs without error.
        find_chains_fast(max_hyp=200, progress=False, backend="auto")

    def test_numpy_backend_forced(self):
        """backend='numpy' should not raise for safe max_hyp values."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        find_chains_fast(max_hyp=500, progress=False, backend="numpy")

    def test_numpy_overflow_guard(self):
        """backend='numpy' with max_hyp > _NUMPY_MAX_HYP must raise ValueError."""
        from rational_distance._legacy.search_chain_fast import (
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
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, find_chains_fast

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

    def test_mod_sieve_numpy_matches_python(self):
        """The experimental mod sieve must preserve results across both backends."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        py = find_chains_fast(max_hyp=300, progress=False, backend="python", mod_sieve=True)
        np_ = find_chains_fast(max_hyp=300, progress=False, backend="numpy", mod_sieve=True)
        assert py == np_

    def test_safe_pair_sieve_rejects_numpy_backend(self):
        """The safe pair sieve is an experimental python-only path."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, run_chain_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        with pytest.raises(ValueError, match="backend='python'"):
            run_chain_fast(
                max_hyp=200,
                progress=False,
                backend="numpy",
                safe_pair_sieve=True,
            )

    def test_safe_pair_sieve_rejects_auto_when_numpy_would_be_used(self):
        """backend=auto should also fail if it resolves to numpy."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, run_chain_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        with pytest.raises(ValueError, match="backend='python'"):
            run_chain_fast(
                max_hyp=200,
                progress=False,
                backend="auto",
                safe_pair_sieve=True,
            )

    def test_start_t1_resumes_subset(self):
        """start_t1=k should return a subset of the full run's results."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        full = find_chains_fast(max_hyp=300, progress=False, backend="python")
        partial = find_chains_fast(max_hyp=300, progress=False, backend="python", start_t1=5)
        # partial is a strict subset (same or fewer results)
        for r in partial:
            assert r in full, f"partial result not in full: {r}"

    def test_python_workers_match_single_process(self):
        """workers>1 must preserve the exact python-backend result set."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        single = find_chains_fast(max_hyp=300, progress=False, backend="python", workers=1)
        parallel = find_chains_fast(max_hyp=300, progress=False, backend="python", workers=2)
        assert parallel == single

    def test_numpy_workers_match_single_process(self):
        """workers>1 must preserve the exact numpy-backend result set."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, find_chains_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        single = find_chains_fast(max_hyp=300, progress=False, backend="numpy", workers=1)
        parallel = find_chains_fast(max_hyp=300, progress=False, backend="numpy", workers=2)
        assert parallel == single

    def test_parallel_start_t1_resumes_subset(self):
        """workers>1 with start_t1 should still return a subset of the full run."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

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
        from rational_distance._legacy.search_chain_fast import run_chain_fast

        execution = run_chain_fast(max_hyp=200, progress=False, backend="python", profile=True)
        profile = execution.profile.as_dict()
        assert set(profile) >= {
            "n_triples",
            "n_pairs_total",
            "n_pairs_after_safe_pair_sieve",
            "n_pairs_after_basic_filters",
            "n_pairs_after_c3_mod_sieve",
            "n_c3_pass",
            "n_c4_pass",
            "n_solutions_before_dedup",
            "n_solutions_after_dedup",
            "near_miss_seen",
            "near_miss_saved",
            "near_miss_dropped",
            "time_generate_triples_s",
            "time_safe_pair_sieve_s",
            "time_filter_s",
            "time_mod_sieve_c3_s",
            "time_c3_s",
            "time_c4_s",
            "time_dedup_s",
            "time_db_write_s",
            "db_bytes_after_run",
        }
        assert (
            profile["n_pairs_total"]
            >= profile["n_pairs_after_safe_pair_sieve"]
            >= profile["n_pairs_after_basic_filters"]
            >= profile["n_pairs_after_c3_mod_sieve"]
            >= profile["n_c3_pass"]
            >= profile["n_c4_pass"]
        )
        assert profile["n_solutions_before_dedup"] >= profile["n_solutions_after_dedup"]
        assert profile["n_pairs_after_safe_pair_sieve"] == profile["n_pairs_total"]
        assert profile["n_pairs_after_c3_mod_sieve"] == profile["n_pairs_after_basic_filters"]
        assert profile["time_safe_pair_sieve_s"] == pytest.approx(0.0)
        assert profile["time_mod_sieve_c3_s"] == pytest.approx(0.0)

    def test_run_chain_fast_profile_keys_match_numpy(self):
        """python and numpy profiled runs should expose the same profile keys."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, run_chain_fast

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

    def test_run_chain_fast_profile_mod_sieve_fields(self):
        """Enabling mod sieve should populate its counters and preserve monotonic counts."""
        from rational_distance._legacy.search_chain_fast import run_chain_fast

        profile = run_chain_fast(
            max_hyp=200,
            progress=False,
            backend="python",
            profile=True,
            mod_sieve=True,
        ).profile.as_dict()
        assert profile["mod_sieve_enabled"] is True
        assert profile["mod_sieve_moduli"] == [16, 3, 5, 7]
        assert (
            profile["n_pairs_total"]
            >= profile["n_pairs_after_safe_pair_sieve"]
            >= profile["n_pairs_after_basic_filters"]
            >= profile["n_pairs_after_c3_mod_sieve"]
            >= profile["n_c3_pass"]
            >= profile["n_c4_pass"]
        )
        assert profile["time_mod_sieve_c3_s"] >= 0.0

    def test_run_chain_fast_profile_safe_pair_sieve_fields(self):
        """Enabling the safe pair sieve should expose stable counters and timings."""
        from rational_distance._legacy.search_chain_fast import run_chain_fast

        profile = run_chain_fast(
            max_hyp=200,
            progress=False,
            backend="python",
            profile=True,
            safe_pair_sieve=True,
        ).profile.as_dict()
        assert profile["safe_pair_sieve_enabled"] is True
        assert (
            profile["n_pairs_total"]
            >= profile["n_pairs_after_safe_pair_sieve"]
            >= profile["n_pairs_after_basic_filters"]
            >= profile["n_c3_pass"]
            >= profile["n_c4_pass"]
        )
        assert profile["time_safe_pair_sieve_s"] >= 0.0

    def test_run_chain_fast_with_cached_triples_keeps_results(self):
        """Passing prebuilt triples should not change the result set."""
        from rational_distance._legacy.search_chain_fast import (
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

    def test_run_chain_fast_bucket_stats_rows_are_monotone(self):
        """bucket_stats=True should emit stable per-bucket monotone counters."""
        from rational_distance._legacy.search_chain_fast import run_chain_fast

        execution = run_chain_fast(
            max_hyp=120,
            progress=False,
            backend="python",
            bucket_stats=True,
        )
        rows = execution.bucket_stats
        assert {row.bucket_type for row in rows} == {
            "g_bucket",
            "delta_bucket",
            "residue_bucket",
        }
        for row in rows:
            assert row.n_total >= row.n_after_basic >= row.n_c3_pass >= row.n_c4_pass
            assert row.n_c3_pass >= row.n_near_miss
            assert row.n_c3_pass == row.n_c4_pass + row.n_near_miss
            if row.n_near_miss > 0:
                assert row.best_sq4_deficit is not None
                assert row.best_sq3_deficit is not None
                assert row.sample_a is not None
                assert row.sample_b is not None
                assert row.sample_c is not None
                assert row.sample_d is not None
            else:
                assert row.best_sq4_deficit is None
                assert row.sample_a is None

    def test_run_chain_fast_bucket_stats_match_parallel_python(self):
        """bucket stats should be identical across python worker counts."""
        from rational_distance._legacy.search_chain_fast import run_chain_fast

        single = run_chain_fast(
            max_hyp=120,
            progress=False,
            backend="python",
            workers=1,
            bucket_stats=True,
        )
        parallel = run_chain_fast(
            max_hyp=120,
            progress=False,
            backend="python",
            workers=2,
            bucket_stats=True,
        )
        assert _bucket_row_map(single.bucket_stats) == _bucket_row_map(parallel.bucket_stats)

    def test_run_chain_fast_bucket_stats_match_numpy_totals(self):
        """When numpy is available, bucket totals should match the python backend."""
        from rational_distance._legacy.search_chain_fast import _HAS_NUMPY, run_chain_fast

        if not _HAS_NUMPY:
            pytest.skip("numpy not installed")
        py = run_chain_fast(
            max_hyp=120,
            progress=False,
            backend="python",
            bucket_stats=True,
        )
        np_run = run_chain_fast(
            max_hyp=120,
            progress=False,
            backend="numpy",
            bucket_stats=True,
        )
        assert _bucket_totals_by_type(py.bucket_stats) == _bucket_totals_by_type(
            np_run.bucket_stats
        )

    def test_bucket_stats_do_not_change_results_or_near_misses(self):
        """bucket stats collection must not change the solution or near-miss sets."""
        from rational_distance._legacy.search_chain_fast import run_chain_fast

        baseline_near_misses: list[tuple] = []
        bucket_near_misses: list[tuple] = []
        baseline = run_chain_fast(
            max_hyp=300,
            progress=False,
            backend="python",
            near_miss_callback=lambda *row: baseline_near_misses.append(row),
        )
        bucketed = run_chain_fast(
            max_hyp=300,
            progress=False,
            backend="python",
            near_miss_callback=lambda *row: bucket_near_misses.append(row),
            bucket_stats=True,
        )
        assert bucketed.results == baseline.results
        assert bucket_near_misses == baseline_near_misses


class TestChainFastModSieve:
    """Tests for the experimental C3 modulus sieve."""

    def test_square_sum_lookup_matches_bruteforce(self):
        """Each per-modulus lookup must agree with direct residue checks."""
        from rational_distance.chain_fast.mod_sieve import (
            DEFAULT_C3_MOD_SIEVE,
            build_square_sum_lookup,
            square_residues,
        )

        for modulus in DEFAULT_C3_MOD_SIEVE.moduli:
            residues = square_residues(modulus)
            lookup = build_square_sum_lookup(modulus)
            for a_residue in range(modulus):
                for n_residue in range(modulus):
                    expected = (
                        ((a_residue * a_residue) + (n_residue * n_residue)) % modulus
                    ) in residues
                    assert lookup[a_residue][n_residue] is expected

    def test_mod_sieve_keeps_python_results_and_near_misses(self):
        """The sieve must not change solutions or near-miss callbacks on python."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        baseline_near_misses: list[tuple] = []
        sieve_near_misses: list[tuple] = []
        baseline = find_chains_fast(
            max_hyp=500,
            progress=False,
            backend="python",
            near_miss_callback=lambda *row: baseline_near_misses.append(row),
        )
        filtered = find_chains_fast(
            max_hyp=500,
            progress=False,
            backend="python",
            mod_sieve=True,
            near_miss_callback=lambda *row: sieve_near_misses.append(row),
        )
        assert filtered == baseline
        assert sieve_near_misses == baseline_near_misses


class TestChainFastSafePairSieve:
    """Tests for the experimental mathematically safe pair sieve."""

    def test_safe_pair_sieve_keeps_python_results_and_near_misses(self):
        """The safe sieve must only remove doomed pairs, not change outputs."""
        from rational_distance._legacy.search_chain_fast import find_chains_fast

        baseline_near_misses: list[tuple] = []
        sieve_near_misses: list[tuple] = []
        baseline = find_chains_fast(
            max_hyp=500,
            progress=False,
            backend="python",
            near_miss_callback=lambda *row: baseline_near_misses.append(row),
        )
        filtered = find_chains_fast(
            max_hyp=500,
            progress=False,
            backend="python",
            safe_pair_sieve=True,
            near_miss_callback=lambda *row: sieve_near_misses.append(row),
        )
        assert filtered == baseline
        assert sieve_near_misses == baseline_near_misses
