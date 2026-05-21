"""Tests for the proof_status pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


# ---------------------------------------------------------------------------
# Method-level tests (no SQLite required)
# ---------------------------------------------------------------------------


class TestSafeSieveMethod:
    """The 2-adic safe_sieve method is rigorous and PARI-free."""

    def test_rejects_mixed_parity(self):
        from rational_distance.proof_status.methods import run_safe_sieve

        # (1, 2): A odd, B even → mixed parity → no_solution.
        result = run_safe_sieve(1, 2)
        assert result.method == "safe_sieve"
        assert result.outcome == "no_solution"
        assert result.details["classification"] == "mixed_parity"

    def test_rejects_odd_odd_wrong_mod4(self):
        from rational_distance.proof_status.methods import run_safe_sieve

        # (1, 3): both odd, A+B = 4, that PASSES; pick (1, 5): 1+5=6, 6%4 != 0
        result = run_safe_sieve(1, 5)
        assert result.outcome == "no_solution"
        assert result.details["classification"] == "odd_odd_wrong_mod4"

    def test_passes_valid_pair(self):
        from rational_distance.proof_status.methods import run_safe_sieve

        # (1, 3): both odd, (1+3) % 4 == 0 → pass
        result = run_safe_sieve(1, 3)
        assert result.outcome == "pass"
        assert result.details["classification"] == "pass"


class TestFactorConcordantMethod:
    """The factor_concordant method is rigorous and PARI-free."""

    def test_finds_concordant_for_264_420(self):
        from rational_distance.proof_status.methods import run_factor_concordant

        result = run_factor_concordant(264, 420)
        # Known: N=77, 315, 352 are all concordant for (264, 420)
        sample = result.details["sample_concordant_n"]
        assert isinstance(sample, list)
        assert {77, 315, 352}.issubset(set(sample))
        # None of them close the chain (well-known empirical fact).
        assert result.details["chain_compatible_count"] == 0
        assert result.outcome == "inconclusive"

    def test_no_concordant_returns_no_solution(self):
        """When B^2 - A^2 has no compatible factorisation, prove no_solution."""
        from rational_distance.proof_status.methods import run_factor_concordant

        # (1, 3): B^2 - A^2 = 8. Divisor pairs (1,8) parity mismatch;
        # (2,4) gives h3 = 1, h4 = 3, N^2 = 1 - 1 = 0 → N=0 not positive.
        # So no positive concordant N exists.
        result = run_factor_concordant(1, 3)
        assert result.outcome == "no_solution"
        assert result.details["concordant_n_count"] == 0


class TestRankZeroMethod:
    """The rank_zero method requires PARI; tests are skipped if unavailable."""

    def test_returns_method_result(self):
        """Smoke test: must return a MethodResult, not raise."""
        from rational_distance.proof_status.methods import (
            _reset_pari_cache,
            run_rank_zero,
        )

        _reset_pari_cache()
        try:
            result = run_rank_zero(264, 420)
        finally:
            _reset_pari_cache()

        assert result.method == "rank_zero"
        # If PARI is available, expect inconclusive (264,420 has rank 2 ≥ 1).
        # If not available, expect skipped.
        assert result.outcome in {"skipped", "inconclusive", "no_solution", "error"}


class TestAdvancedMethods:
    """Advanced methods must be safe to call with optional dependencies."""

    def test_scan_rank_one_height_rejects_non_rank_one(self):
        from rational_distance.concordant.heegner_height import scan_rank_one_height

        scan = scan_rank_one_height(264, 420, multiple_bound=1)
        if scan.skipped_reason == "cypari2_unavailable":
            pytest.skip("cypari2 / PARI not available")
        assert scan.skipped_reason == "rank_not_one"
        assert scan.rank_lower == 2
        assert scan.rank_upper == 2

    def test_scan_rank_one_height_7_45_regression(self, monkeypatch):
        from rational_distance.concordant.heegner_height import scan_rank_one_height

        monkeypatch.delenv("RD_HEEGNER_MULTIPLE_BOUND", raising=False)
        monkeypatch.delenv("RD_HEEGNER_HEIGHT_BOUND", raising=False)

        scan = scan_rank_one_height(7, 45)
        if scan.skipped_reason == "cypari2_unavailable":
            pytest.skip("cypari2 / PARI not available")
        assert scan.skipped_reason is None
        assert scan.rank_lower == 1
        assert scan.rank_upper == 1
        assert scan.generator is not None
        assert scan.points_checked > 0
        assert scan.multiple_bound == 12
        assert scan.concordant_n == [24]
        assert scan.chain_compatible_n == []

    def test_heegner_height_is_conservative(self):
        from rational_distance.proof_status.methods import run_heegner_height

        result = run_heegner_height(264, 420)
        assert result.method == "heegner"
        # (264,420) is rank 2, so the rank-one method should normally skip.
        # If PARI is unavailable or errors, it must still return a MethodResult
        # rather than raising.  It must never prove no_solution at this stage.
        assert result.outcome in {"skipped", "inconclusive", "solution_found", "error"}
        assert result.outcome != "no_solution"

    def test_heegner_stub_compatibility_name(self):
        from rational_distance.proof_status.methods import run_heegner_stub

        result = run_heegner_stub(264, 420)
        assert result.method == "heegner"
        assert result.outcome != "no_solution"

    def test_chabauty_stub(self):
        from rational_distance.proof_status.methods import run_chabauty_stub

        result = run_chabauty_stub(264, 420)
        assert result.method == "chabauty"
        assert result.outcome == "skipped"

    def test_brauer_manin_stub(self):
        from rational_distance.proof_status.methods import run_brauer_manin_stub

        result = run_brauer_manin_stub(264, 420)
        assert result.method == "brauer_manin"
        assert result.outcome == "skipped"


# ---------------------------------------------------------------------------
# Schema / DAO tests
# ---------------------------------------------------------------------------


class TestSchema:
    def test_init_creates_tables(self, tmp_path: Path):
        from rational_distance.proof_status import schema

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        }
        assert {"proof_meta", "pair_proof_status", "pair_method_attempts"}.issubset(tables)

    def test_upsert_idempotent(self, tmp_path: Path):
        from rational_distance.proof_status import schema

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        schema.upsert_pair_status(conn, A=3, B=5, status="hard_case", method="exhausted")
        schema.upsert_pair_status(
            conn,
            A=3,
            B=5,
            status="no_solution",
            method="safe_sieve",
            notes="upgraded",
        )

        row = schema.get_pair_status(conn, 3, 5)
        assert row is not None
        assert row.status == "no_solution"
        assert row.method == "safe_sieve"
        assert row.notes == "upgraded"

    def test_record_attempt_appends(self, tmp_path: Path):
        from rational_distance.proof_status import schema
        from rational_distance.proof_status.types import MethodResult

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        for outcome in ("pass", "no_solution"):
            schema.record_method_attempt(
                conn,
                A=3,
                B=5,
                result=MethodResult(method="safe_sieve", outcome=outcome),
            )

        rows = conn.execute(
            "SELECT method, outcome FROM pair_method_attempts ORDER BY id"
        ).fetchall()
        assert [(r[0], r[1]) for r in rows] == [
            ("safe_sieve", "pass"),
            ("safe_sieve", "no_solution"),
        ]


# ---------------------------------------------------------------------------
# Workflow tests (use only PARI-free methods so they are deterministic)
# ---------------------------------------------------------------------------


@pytest.fixture
def pari_free_pipeline():
    """A pipeline that uses only the deterministic, PARI-free methods."""
    from rational_distance.proof_status.methods import (
        run_factor_concordant,
        run_safe_sieve,
    )

    return (
        ("safe_sieve", run_safe_sieve),
        ("factor_concordant", run_factor_concordant),
    )


class TestWorkflow:
    def test_safe_sieve_terminates_pipeline(self, tmp_path: Path, pari_free_pipeline):
        from rational_distance.proof_status import schema, workflow

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        cfg = workflow.WorkflowConfig(methods=pari_free_pipeline)
        # (1, 5): both odd, (1+5) % 4 != 0 ⇒ safe_sieve rejects.
        status = workflow.process_pair(conn, 1, 5, cfg)

        assert status.status == "no_solution"
        assert status.method == "safe_sieve"

        # Only safe_sieve should have been recorded (factor_concordant skipped
        # because the pipeline broke after the terminal outcome).
        attempt_methods = [
            row[0]
            for row in conn.execute(
                "SELECT method FROM pair_method_attempts WHERE A=? AND B=?",
                (1, 5),
            ).fetchall()
        ]
        assert attempt_methods == ["safe_sieve"]

    def test_factor_concordant_terminates_when_no_n(self, tmp_path: Path, pari_free_pipeline):
        from rational_distance.proof_status import schema, workflow

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        cfg = workflow.WorkflowConfig(methods=pari_free_pipeline)
        # (1, 3): passes safe_sieve, fails factor_concordant (no N).
        status = workflow.process_pair(conn, 1, 3, cfg)

        assert status.status == "no_solution"
        assert status.method == "factor_concordant"

    def test_inconclusive_pair_becomes_hard_case(self, tmp_path: Path, pari_free_pipeline):
        from rational_distance.proof_status import schema, workflow

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        cfg = workflow.WorkflowConfig(methods=pari_free_pipeline)
        # (7, 45): both odd, (7+45) % 4 == 0, so safe_sieve passes.
        # factor_concordant finds at least one concordant N but none closes the
        # chain ⇒ inconclusive. With this PARI-free pipeline that means hard_case.
        status = workflow.process_pair(conn, 7, 45, cfg)
        assert status.status == "hard_case"
        # factor_concordant should still have recorded its inconclusive attempt.
        outcomes = conn.execute(
            "SELECT method, outcome FROM pair_method_attempts WHERE A=7 AND B=45"
        ).fetchall()
        method_outcomes = {(r[0], r[1]) for r in outcomes}
        assert ("safe_sieve", "pass") in method_outcomes
        assert ("factor_concordant", "inconclusive") in method_outcomes

    def test_terminal_pair_not_reprocessed(self, tmp_path: Path, pari_free_pipeline):
        from rational_distance.proof_status import schema, workflow

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        cfg = workflow.WorkflowConfig(methods=pari_free_pipeline)
        workflow.process_pair(conn, 1, 5, cfg)
        before = conn.execute(
            "SELECT COUNT(*) FROM pair_method_attempts WHERE A=1 AND B=5"
        ).fetchone()[0]

        # Re-run: should be a no-op.
        workflow.process_pair(conn, 1, 5, cfg)
        after = conn.execute(
            "SELECT COUNT(*) FROM pair_method_attempts WHERE A=1 AND B=5"
        ).fetchone()[0]
        assert before == after

    def test_rerun_terminal_does_reprocess(self, tmp_path: Path, pari_free_pipeline):
        from rational_distance.proof_status import schema, workflow

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        cfg = workflow.WorkflowConfig(methods=pari_free_pipeline)
        workflow.process_pair(conn, 1, 5, cfg)
        before = conn.execute(
            "SELECT COUNT(*) FROM pair_method_attempts WHERE A=1 AND B=5"
        ).fetchone()[0]

        cfg_rerun = workflow.WorkflowConfig(methods=pari_free_pipeline, rerun_terminal=True)
        workflow.process_pair(conn, 1, 5, cfg_rerun)
        after = conn.execute(
            "SELECT COUNT(*) FROM pair_method_attempts WHERE A=1 AND B=5"
        ).fetchone()[0]
        assert after == before + 1  # safe_sieve attempted once more

    def test_status_counts_aggregate(self, tmp_path: Path, pari_free_pipeline):
        from rational_distance.proof_status import schema, workflow

        db = tmp_path / "p.sqlite3"
        conn = schema.connect_db(db)
        schema.init_schema(conn)

        cfg = workflow.WorkflowConfig(methods=pari_free_pipeline)
        workflow.process_pair(conn, 1, 5, cfg)  # no_solution via safe_sieve
        workflow.process_pair(conn, 1, 3, cfg)  # no_solution via factor_concordant
        workflow.process_pair(conn, 7, 45, cfg)  # hard_case

        counts = schema.status_counts(conn)
        assert counts["no_solution"] == 2
        assert counts["hard_case"] == 1
