from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_cli_parallel_max_hyp_uses_generate_ab_pairs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import rational_distance.concordant.pairs as pair_module
    from rational_distance.proof_status import schema
    from scripts import prove_no_solution as cli

    def fail_iter(_max_hyp: int = 500):
        raise AssertionError("parallel max_hyp path should materialize pairs before processing")

    def fake_generate(_max_hyp: int = 500) -> list[tuple[int, int]]:
        return [(1, 5), (1, 3), (7, 45)]

    monkeypatch.setattr(pair_module, "iter_ab_pairs", fail_iter)
    monkeypatch.setattr(pair_module, "generate_ab_pairs", fake_generate)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(tmp_path / "parallel.sqlite3"),
            "--max-hyp",
            "100",
            "--workers",
            "2",
            "--progress-every",
            "1",
        ],
    )

    cli.main()

    out = capsys.readouterr().out
    assert "pairs to process: 3 (materialized from max_hyp=100)" in out
    assert "[progress]" in out

    conn = schema.connect_db(tmp_path / "parallel.sqlite3")
    schema.init_schema(conn)
    counts = schema.status_counts(conn)
    assert counts["no_solution"] == 3
