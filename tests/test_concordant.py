"""Tests for pair generation and concordant analysis."""

from __future__ import annotations

import json
import subprocess
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


class TestConcordantDiagnostics:
    """Tests for fixed-pair concordant diagnostics."""

    def test_diagnose_pair_264_420(self):
        from rational_distance.concordant import diagnose_pair

        diagnostics = diagnose_pair(264, 420, ec_bound=400000)
        assert diagnostics.all_concordant_n == [77, 315, 352]
        assert diagnostics.deep_extra_n == []
        assert diagnostics.mirror_hit_n == []
        assert diagnostics.chain_compatible == []

        expected_b = {77: 607, 315: 369, 352: 332}
        assert {candidate.n: candidate.b for candidate in diagnostics.candidates} == expected_b

        for candidate in diagnostics.candidates:
            assert candidate.source == "ellratpoints"
            assert candidate.chain_ok is False
            assert candidate.b_positive is True
            assert candidate.b_in_concordant_set is False
            assert candidate.b_source is None
            assert candidate.side_hit == "none"
            assert candidate.c1_nearest_square_delta >= 0
            assert candidate.c2_nearest_square_delta >= 0

        assert diagnostics.best_candidate is not None
        assert diagnostics.best_candidate.combined_delta == min(
            candidate.combined_delta for candidate in diagnostics.candidates
        )
        assert all(candidate.source != "deep" for candidate in diagnostics.candidates)
        assert diagnostics.c1_hit_n == []
        assert diagnostics.c2_hit_n == []
        assert diagnostics.side_hit_n == []


class TestConcordantSafePairSieve:
    """Tests for the reduced-pair concordant safe sieve."""

    def test_allow_reduced_pair_examples(self):
        from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair

        assert allow_reduced_pair(22, 35) is False
        assert allow_reduced_pair(5, 9) is False
        assert allow_reduced_pair(7, 45) is True

    def test_classify_matches_allow_and_is_symmetric(self):
        from rational_distance.concordant.safe_pair_sieve import (
            allow_reduced_pair,
            classify_reduced_pair,
        )

        examples = [(22, 35), (5, 9), (7, 45), (45, 7), (11, 21), (13, 19)]
        for A, B in examples:
            classification = classify_reduced_pair(A, B)
            assert allow_reduced_pair(A, B) is (classification == "pass")
            assert allow_reduced_pair(A, B) is allow_reduced_pair(B, A)
            assert classify_reduced_pair(A, B) == classify_reduced_pair(B, A)


class TestConcordantCompatibility:
    """Smoke tests for old and new concordant import paths."""

    def test_legacy_and_new_import_paths_are_available(self):
        from rational_distance.concordant import (
            ChainCandidateDiagnostic as new_candidate_diagnostic,
        )
        from rational_distance.concordant import (
            ConcordantPairDiagnostics as new_pair_diagnostics,
        )
        from rational_distance.concordant import (
            ConcordantProfile as new_profile,
        )
        from rational_distance.concordant import (
            analyze_pair as new_analyze_pair,
        )
        from rational_distance.concordant import (
            diagnose_pair as new_diagnose_pair,
        )
        from rational_distance.concordant import (
            generate_ab_pairs as new_generate_ab_pairs,
        )
        from rational_distance.concordant_ec import (
            ChainCandidateDiagnostic as legacy_candidate_diagnostic,
        )
        from rational_distance.concordant_ec import (
            ConcordantPairDiagnostics as legacy_pair_diagnostics,
        )
        from rational_distance.concordant_ec import (
            ConcordantProfile as legacy_profile,
        )
        from rational_distance.concordant_ec import (
            analyze_pair as legacy_analyze_pair,
        )
        from rational_distance.concordant_ec import (
            diagnose_pair as legacy_diagnose_pair,
        )
        from rational_distance.pair_generator import generate_ab_pairs as legacy_generate_ab_pairs

        assert callable(new_analyze_pair)
        assert callable(new_diagnose_pair)
        assert callable(new_generate_ab_pairs)
        assert callable(legacy_analyze_pair)
        assert callable(legacy_diagnose_pair)
        assert callable(legacy_generate_ab_pairs)
        assert new_candidate_diagnostic.__name__ == "ChainCandidateDiagnostic"
        assert legacy_candidate_diagnostic.__name__ == "ChainCandidateDiagnostic"
        assert new_profile.__name__ == "ConcordantProfile"
        assert legacy_profile.__name__ == "ConcordantProfile"
        assert new_pair_diagnostics.__name__ == "ConcordantPairDiagnostics"
        assert legacy_pair_diagnostics.__name__ == "ConcordantPairDiagnostics"

        new_result = new_diagnose_pair(264, 420, ec_bound=400000)
        legacy_result = legacy_diagnose_pair(264, 420, ec_bound=400000)
        assert new_result.all_concordant_n == legacy_result.all_concordant_n
        assert new_result.chain_compatible == legacy_result.chain_compatible
        assert new_result.candidates[0].side_hit == legacy_result.candidates[0].side_hit


class TestConcordantCli:
    """CLI tests for fixed-pair concordant diagnostics."""

    @staticmethod
    def _run_pair(*extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "concordant",
                "--pair",
                "264,420",
                "--ec-bound",
                "400000",
                *extra_args,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    @staticmethod
    def _run_batch(*extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "search.py"),
                "concordant",
                "--max-hyp",
                "200",
                "--ec-bound",
                "100000",
                "--no-progress",
                *extra_args,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_pair_cli_prints_diagnostics(self):
        proc = self._run_pair()
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert "Chain compatibility diagnostics" in proc.stdout
        assert "mirror_hit_n: none" in proc.stdout
        assert "side_hit_n: none" in proc.stdout
        assert "side_hit=none" in proc.stdout

    def test_pair_cli_out_writes_json(self, tmp_path):
        out_path = tmp_path / "pair.json"
        proc = self._run_pair("--out", str(out_path))
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert out_path.exists()
        payload = json.loads(out_path.read_text(encoding="utf-8"))
        assert payload["mode"] == "pair"
        assert payload["A"] == 264
        assert payload["B"] == 420
        assert payload["all_concordant_n"] == [77, 315, 352]
        assert payload["mirror_hit_n"] == []
        assert payload["c1_hit_n"] == []
        assert payload["c2_hit_n"] == []
        assert payload["side_hit_n"] == []
        assert len(payload["candidates"]) == 3
        assert payload["best_candidate"]["side_hit"] == "none"
        assert payload["best_candidate"]["b_positive"] is True

    def test_pair_cli_deep_zero_matches_default(self, tmp_path):
        default_out = tmp_path / "default.json"
        deep_out = tmp_path / "deep0.json"

        default_proc = self._run_pair("--out", str(default_out))
        deep_proc = self._run_pair("--deep", "0", "--out", str(deep_out))
        assert default_proc.returncode == 0, default_proc.stderr or default_proc.stdout
        assert deep_proc.returncode == 0, deep_proc.stderr or deep_proc.stdout

        default_payload = json.loads(default_out.read_text(encoding="utf-8"))
        deep_payload = json.loads(deep_out.read_text(encoding="utf-8"))
        assert default_payload == deep_payload

    def test_pair_cli_profile_writes_profile_json(self, tmp_path):
        out_path = tmp_path / "pair_profile.json"
        proc = self._run_pair("--profile", "--out", str(out_path))
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert "Concordant profile" in proc.stdout
        payload = json.loads(out_path.read_text(encoding="utf-8"))
        assert "profile" in payload
        profile = payload["profile"]
        assert profile["n_pairs_total"] == 1
        assert profile["n_pairs_after_safe_pair_sieve"] == 1
        assert profile["n_pairs_rejected_by_safe_pair_sieve"] == 0
        assert profile["n_pairs_rejected_mixed_parity"] == 0
        assert profile["n_pairs_rejected_mod4"] == 0
        assert profile["n_pairs_completed"] == 1
        assert profile["rank_enabled"] is False
        assert profile["safe_pair_sieve_enabled"] is False
        assert profile["time_rank_s"] == 0
        assert profile["time_safe_pair_sieve_s"] == 0
        assert "time_rank_s" in profile
        assert "time_find_concordant_s" in profile
        assert "time_candidate_diagnostics_s" in profile

    def test_pair_cli_rejects_safe_pair_sieve(self):
        proc = self._run_pair("--safe-pair-sieve")
        assert proc.returncode != 0
        assert "--safe-pair-sieve currently supports only batch concordant runs" in (
            proc.stderr or proc.stdout
        )

    def test_batch_cli_out_includes_diagnostic_summary(self, tmp_path):
        out_path = tmp_path / "batch.json"
        proc = self._run_batch("--profile", "--top", "3", "--out", str(out_path))
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert "Pairs with concordant N" in proc.stdout
        assert "Pairs with mirror hits" in proc.stdout
        assert "Pairs with C1 hits" in proc.stdout
        assert "Pairs with side hits" in proc.stdout
        assert "Concordant profile" in proc.stdout
        payload = json.loads(out_path.read_text(encoding="utf-8"))
        assert payload["n_pairs"] > 0
        assert "n_with_mirror_hit" in payload
        assert "n_with_c1_hit" in payload
        assert "n_with_c2_hit" in payload
        assert "n_with_side_hit" in payload
        assert "n_pairs_analyzed" in payload
        assert "profile" in payload
        assert payload["profile"]["n_pairs_total"] == payload["n_pairs"]
        assert payload["profile"]["n_pairs_after_safe_pair_sieve"] == payload["n_pairs"]
        assert payload["profile"]["n_pairs_rejected_by_safe_pair_sieve"] == 0
        assert payload["profile"]["n_pairs_rejected_mixed_parity"] == 0
        assert payload["profile"]["n_pairs_rejected_mod4"] == 0
        assert payload["n_pairs_analyzed"] == payload["n_pairs"]
        assert payload["safe_pair_sieve_enabled"] is False
        assert payload["profile"]["rank_enabled"] is False
        assert payload["profile"]["safe_pair_sieve_enabled"] is False
        assert payload["profile"]["time_rank_s"] == 0
        assert "time_pari_init_s" in payload["profile"]
        assert "time_safe_pair_sieve_s" in payload["profile"]
        assert "time_pair_generation_s" in payload["profile"]
        assert payload["pairs"]
        first = payload["pairs"][0]
        assert "c1_hit_n" in first
        assert "c2_hit_n" in first
        assert "side_hit_n" in first
        assert "best_side_hit" in first
        assert "best_b_positive" in first
        assert "mirror_hit_count" in first
        assert "min_combined_delta" in first
        assert "best_candidate" in first

    def test_batch_cli_safe_pair_sieve_reduces_analyzed_pairs(self, tmp_path):
        baseline_path = tmp_path / "baseline.json"
        sieve_path = tmp_path / "sieve.json"

        baseline_proc = self._run_batch("--profile", "--out", str(baseline_path))
        sieve_proc = self._run_batch("--profile", "--safe-pair-sieve", "--out", str(sieve_path))
        assert baseline_proc.returncode == 0, baseline_proc.stderr or baseline_proc.stdout
        assert sieve_proc.returncode == 0, sieve_proc.stderr or sieve_proc.stdout
        assert "Safe pair sieve:" in sieve_proc.stdout

        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        filtered = json.loads(sieve_path.read_text(encoding="utf-8"))

        assert filtered["n_pairs"] == baseline["n_pairs"]
        assert filtered["safe_pair_sieve_enabled"] is True
        assert filtered["n_pairs_analyzed"] == filtered["profile"]["n_pairs_after_safe_pair_sieve"]
        assert (
            filtered["profile"]["n_pairs_after_safe_pair_sieve"]
            == filtered["profile"]["n_pairs_completed"]
        )
        assert filtered["n_pairs_analyzed"] == len(filtered["pairs"])
        assert filtered["n_pairs_analyzed"] < filtered["n_pairs"]
        assert filtered["profile"]["safe_pair_sieve_enabled"] is True
        assert (
            filtered["profile"]["n_pairs_rejected_by_safe_pair_sieve"]
            == filtered["n_pairs"] - filtered["n_pairs_analyzed"]
        )
        assert (
            filtered["profile"]["n_pairs_rejected_mixed_parity"]
            + filtered["profile"]["n_pairs_rejected_mod4"]
            == filtered["profile"]["n_pairs_rejected_by_safe_pair_sieve"]
        )
        assert filtered["profile"]["time_safe_pair_sieve_s"] >= 0

        from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair

        assert all(allow_reduced_pair(row["A"], row["B"]) for row in filtered["pairs"])
        baseline_keys = {(row["A"], row["B"]) for row in baseline["pairs"]}
        filtered_keys = {(row["A"], row["B"]) for row in filtered["pairs"]}
        assert filtered_keys < baseline_keys
