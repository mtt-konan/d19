"""Tests for curated results catalog helpers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.results.catalog import build_results_catalog


def test_build_results_catalog_records_curated_artifacts(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    multi_n_dir = results_dir / "multi_n"
    multi_n_dir.mkdir()
    dataset = multi_n_dir / "multi_concordant_N_max10000.jsonl"
    _ = dataset.write_text('{"A": 27, "B": 160}\n', encoding="utf-8")

    catalog = build_results_catalog(results_dir)

    assert catalog["artifacts"][0]["path"] == "multi_n/multi_concordant_N_max10000.jsonl"
    assert catalog["artifacts"][0]["exists"] is True
    assert catalog["artifacts"][0]["category"] == "multi-concordant"
    assert catalog["artifacts"][0]["authoritative"] is True


def test_build_results_catalog_marks_stale_proof_status_snapshot(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    db_path = results_dir / "proof_status.db"
    _ = db_path.write_bytes(b"sqlite placeholder")

    catalog = build_results_catalog(results_dir)

    proof_status = next(
        item for item in catalog["artifacts"] if item["path"] == "proof_status.db"
    )
    assert proof_status["exists"] is True
    assert proof_status["authoritative"] is False
    assert "stale" in proof_status["description"].lower()
