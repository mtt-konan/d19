from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_cli_max_hyp_uses_iter_ab_pairs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import rational_distance.concordant.pairs as pair_module
    from rational_distance.proof_status import schema
    from scripts import prove_no_solution as cli

    def fail_generate(_max_hyp: int = 500):
        raise AssertionError("full pair materialization should not run")

    def fake_iter(_max_hyp: int = 500):
        yield (1, 5)
        yield (1, 3)

    monkeypatch.setattr(pair_module, "generate_ab_pairs", fail_generate)
    monkeypatch.setattr(pair_module, "iter_ab_pairs", fake_iter)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(tmp_path / "proof.sqlite3"),
            "--max-hyp",
            "100",
            "--workers",
            "1",
            "--no-progress",
        ],
    )

    cli.main()

    conn = schema.connect_db(tmp_path / "proof.sqlite3")
    schema.init_schema(conn)
    counts = schema.status_counts(conn)
    assert counts["no_solution"] == 2


def test_cli_progress_every_emits_plain_heartbeat(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import rational_distance.concordant.pairs as pair_module
    from scripts import prove_no_solution as cli

    def fake_iter(_max_hyp: int = 500):
        yield (1, 5)
        yield (1, 3)

    monkeypatch.setattr(pair_module, "iter_ab_pairs", fake_iter)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(tmp_path / "heartbeat.sqlite3"),
            "--max-hyp",
            "100",
            "--workers",
            "1",
            "--progress-every",
            "1",
        ],
    )

    cli.main()

    out = capsys.readouterr().out
    assert "[progress]" in out
