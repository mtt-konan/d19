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
    dataset = results_dir / "multi_concordant_N_max10000.jsonl"
    _ = dataset.write_text('{"A": 27, "B": 160}\n', encoding="utf-8")

    catalog = build_results_catalog(results_dir)

    assert catalog["artifacts"][0]["path"] == "multi_concordant_N_max10000.jsonl"
    assert catalog["artifacts"][0]["exists"] is True
    assert catalog["artifacts"][0]["category"] == "multi-concordant"
    assert catalog["artifacts"][0]["authoritative"] is True
