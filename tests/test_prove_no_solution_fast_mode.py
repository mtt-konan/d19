from __future__ import annotations

import sqlite3
import sys
from collections.abc import Iterable
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_cli_fast_core_audits_only_survivors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import rational_distance.concordant.pairs as pair_module
    import rational_distance.proof_status.fast_core as fast_core_module
    import rational_distance.proof_status.workflow as workflow_module
    from rational_distance.proof_status import schema
    from rational_distance.proof_status.fast_core import CoreChunkResult
    from rational_distance.proof_status.workflow import PairComputeResult
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"

    def fake_iter(max_hyp: int) -> Iterable[tuple[int, int]]:
        assert max_hyp == 100
        yield (1, 5)
        yield (2, 7)
        yield (7, 45)

    def fake_run_fast_core(pairs, *, workers, pair_chunk_size, pool_chunksize, on_chunk):
        assert list(pairs) == [(1, 5), (2, 7), (7, 45)]
        assert workers == 2
        assert pair_chunk_size == 50_000
        assert pool_chunksize == 1
        result = CoreChunkResult(checked=3, no_solution=2, survivors=((7, 45),))
        if on_chunk is not None:
            on_chunk(result)
        return result

    def fake_process_pairs_parallel(
        conn,
        pairs,
        *,
        workers,
        commit_every,
        skip_terminal,
        on_result,
    ):
        assert tuple(pairs) == ((7, 45),)
        assert workers == 2
        assert commit_every == 1000
        assert skip_terminal is False
        schema.upsert_pair_status(
            conn,
            A=7,
            B=45,
            status="hard_case",
            method="exhausted",
            notes="fake survivor audit",
            commit=True,
        )
        on_result(
            PairComputeResult(
                A=7,
                B=45,
                final_status="hard_case",
                final_method="exhausted",
                final_notes="fake survivor audit",
                rank_lower=None,
                rank_upper=None,
                concordant_n_count=None,
                chain_compatible_count=None,
                f2_rank=None,
                method_results=(),
            )
        )
        return {"hard_case": 1}

    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)
    monkeypatch.setattr(pair_module, "iter_ab_pairs", fake_iter)
    monkeypatch.setattr(fast_core_module, "run_fast_core", fake_run_fast_core)
    monkeypatch.setattr(workflow_module, "process_pairs_parallel", fake_process_pairs_parallel)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--fast-core",
            "--force",
            "--no-progress",
        ],
    )

    cli.main()

    out = capsys.readouterr().out
    assert "mode:             fast-core" in out
    assert "fast-core done checked=3 no_solution=2 survivors=1" in out
    assert "no_solution               2" in out
    assert "hard_case                 1" in out

    conn = sqlite3.connect(db)
    total = conn.execute("SELECT COUNT(*) FROM pair_proof_status").fetchone()[0]
    assert total == 1


def test_cli_fast_core_writes_summary_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import json

    import rational_distance.concordant.pairs as pair_module
    import rational_distance.proof_status.fast_core as fast_core_module
    import rational_distance.proof_status.workflow as workflow_module
    from rational_distance.proof_status.fast_core import CoreChunkResult
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"
    summary = tmp_path / "summary.json"

    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)
    monkeypatch.setattr(pair_module, "iter_ab_pairs", lambda _max_hyp: iter([(1, 5), (7, 45)]))
    monkeypatch.setattr(
        fast_core_module,
        "run_fast_core",
        lambda pairs, **kwargs: CoreChunkResult(
            checked=2,
            no_solution=1,
            survivors=((7, 45),),
        ),
    )
    monkeypatch.setattr(
        workflow_module,
        "process_pairs_parallel",
        lambda *args, **kwargs: {"hard_case": 1},
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--fast-core",
            "--fast-summary-json",
            str(summary),
            "--force",
            "--no-progress",
        ],
    )

    cli.main()

    payload = json.loads(summary.read_text())
    assert payload["checked"] == 2
    assert payload["no_solution"] == 1
    assert payload["survivor_count"] == 1
    assert payload["survivors"] == [[7, 45]]


def test_cli_fast_core_streams_pairs_without_materializing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import rational_distance.concordant.pairs as pair_module
    import rational_distance.proof_status.fast_core as fast_core_module
    import rational_distance.proof_status.workflow as workflow_module
    from rational_distance.proof_status.fast_core import CoreChunkResult
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"
    summary = tmp_path / "summary.json"

    def fail_generate(_max_hyp: int) -> list[tuple[int, int]]:
        raise AssertionError("fast-core should stream pairs instead of materializing")

    def fake_iter(max_hyp: int) -> Iterable[tuple[int, int]]:
        assert max_hyp == 100
        yield (1, 5)
        yield (7, 45)

    def fake_run_fast_core(pairs, **kwargs):
        assert list(pairs) == [(1, 5), (7, 45)]
        return CoreChunkResult(
            checked=2,
            no_solution=1,
            survivors=((7, 45),),
        )

    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)
    monkeypatch.setattr(pair_module, "generate_ab_pairs", fail_generate)
    monkeypatch.setattr(pair_module, "iter_ab_pairs", fake_iter)
    monkeypatch.setattr(fast_core_module, "run_fast_core", fake_run_fast_core)
    monkeypatch.setattr(
        workflow_module,
        "process_pairs_parallel",
        lambda *args, **kwargs: {"hard_case": 1},
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--fast-core",
            "--fast-core-only",
            "--fast-summary-json",
            str(summary),
            "--force",
            "--no-progress",
        ],
    )

    cli.main()


def test_cli_fast_core_only_skips_survivor_audit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import rational_distance.concordant.pairs as pair_module
    import rational_distance.proof_status.fast_core as fast_core_module
    import rational_distance.proof_status.workflow as workflow_module
    from rational_distance.proof_status.fast_core import CoreChunkResult
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"
    summary = tmp_path / "summary.json"
    audit_called = False

    def fail_if_called(*args, **kwargs):
        nonlocal audit_called
        audit_called = True
        raise AssertionError("survivor audit should not run in --fast-core-only mode")

    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)
    monkeypatch.setattr(pair_module, "iter_ab_pairs", lambda _max_hyp: iter([(1, 5), (7, 45)]))
    monkeypatch.setattr(
        fast_core_module,
        "run_fast_core",
        lambda pairs, **kwargs: CoreChunkResult(
            checked=2,
            no_solution=1,
            survivors=((7, 45),),
        ),
    )
    monkeypatch.setattr(workflow_module, "process_pairs_parallel", fail_if_called)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--fast-core",
            "--fast-core-only",
            "--fast-summary-json",
            str(summary),
            "--force",
            "--no-progress",
        ],
    )

    cli.main()

    assert audit_called is False
    conn = sqlite3.connect(db)
    total = conn.execute("SELECT COUNT(*) FROM pair_proof_status").fetchone()[0]
    assert total == 0


def test_cli_sets_pari_single_thread_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    from scripts import prove_no_solution as cli

    monkeypatch.delenv("PARI_MT_ENGINE", raising=False)
    monkeypatch.setattr(cli, "_print_status_report", lambda _db_path: None)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            "/tmp/unused-proof-report.sqlite3",
            "--report",
        ],
    )

    cli.main()

    import os

    assert os.environ["PARI_MT_ENGINE"] == "single"


def test_cli_fast_core_only_requires_fast_core(monkeypatch: pytest.MonkeyPatch) -> None:
    from scripts import prove_no_solution as cli

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            "/tmp/unused-proof-fast-core-only.sqlite3",
            "--max-hyp",
            "100",
            "--fast-core-only",
        ],
    )

    with pytest.raises(SystemExit, match="--fast-core-only requires --fast-core"):
        cli.main()
