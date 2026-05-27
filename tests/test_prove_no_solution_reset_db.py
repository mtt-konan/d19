from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_force_removes_db_and_sqlite_sidecars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from scripts import prove_no_solution as cli

    db = tmp_path / "proof.sqlite3"
    db.write_text("old db")
    db.with_name(db.name + "-wal").write_text("old wal")
    db.with_name(db.name + "-shm").write_text("old shm")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prove_no_solution.py",
            "--db",
            str(db),
            "--pair",
            "1,5",
            "--serial",
            "--force",
            "--no-progress",
        ],
    )

    cli.main()

    assert db.exists()

    conn = sqlite3.connect(db)
    total = conn.execute("SELECT COUNT(*) FROM pair_proof_status").fetchone()[0]
    assert total == 1


def test_reset_sqlite_db_removes_main_db_and_sidecars(tmp_path: Path) -> None:
    from scripts.prove_no_solution import _reset_sqlite_db

    db = tmp_path / "proof.sqlite3"
    paths = [
        db,
        db.with_name(db.name + "-wal"),
        db.with_name(db.name + "-shm"),
    ]
    for path in paths:
        path.write_text("old")

    _reset_sqlite_db(db)

    assert all(not path.exists() for path in paths)
