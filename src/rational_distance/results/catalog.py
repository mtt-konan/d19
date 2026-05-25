"""Curated metadata for important result artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


class CatalogArtifact(TypedDict):
    path: str
    category: str
    description: str
    authoritative: bool
    exists: bool
    size_bytes: int | None


class ResultsCatalog(TypedDict):
    results_dir: str
    artifacts: list[CatalogArtifact]


@dataclass(frozen=True)
class CuratedArtifact:
    path: str
    category: str
    description: str
    authoritative: bool = False


CURATED_ARTIFACTS: tuple[CuratedArtifact, ...] = (
    CuratedArtifact(
        path="multi_concordant_N_max10000.jsonl",
        category="multi-concordant",
        description="Ground-truth reduced pairs with >= 2 concordant N for max_hyp=10000.",
        authoritative=True,
    ),
    CuratedArtifact(
        path="multi_concordant_N_max20000_fast.jsonl",
        category="multi-concordant",
        description=(
            "Pivot-on-N fast scanner output for max_hyp=20000 "
            "(extends beyond ground-truth scale)."
        ),
        authoritative=False,
    ),
    CuratedArtifact(
        path="multi_concordant_N_max50000_fast.jsonl",
        category="multi-concordant",
        description=(
            "Pivot-on-N fast scanner output for max_hyp=50000 "
            "(extends beyond ground-truth scale)."
        ),
        authoritative=False,
    ),
    CuratedArtifact(
        path="multi_concordant_N_max10000_classified.jsonl",
        category="multi-concordant",
        description=(
            "max_hyp=10000 multi-N pairs annotated with F₂-rank "
            "(see scripts/classify_multi_n_by_f2_rank.py, wl049)."
        ),
        authoritative=False,
    ),
    CuratedArtifact(
        path="multi_concordant_N_max20000_classified.jsonl",
        category="multi-concordant",
        description=(
            "max_hyp=20000 multi-N pairs annotated with F₂-rank "
            "(wl049)."
        ),
        authoritative=False,
    ),
    CuratedArtifact(
        path="multi_concordant_N_max50000_classified.jsonl",
        category="multi-concordant",
        description=(
            "max_hyp=50000 multi-N pairs annotated with F₂-rank "
            "(wl049)."
        ),
        authoritative=False,
    ),
    CuratedArtifact(
        path="proof_status.db",
        category="proof-status",
        description="SQLite database for proof workflow state.",
        authoritative=True,
    ),
)


def build_results_catalog(results_dir: Path) -> ResultsCatalog:
    artifacts: list[CatalogArtifact] = []
    for item in CURATED_ARTIFACTS:
        file_path = results_dir / item.path
        exists = file_path.exists()
        artifacts.append(
            {
                "path": item.path,
                "category": item.category,
                "description": item.description,
                "authoritative": item.authoritative,
                "exists": exists,
                "size_bytes": file_path.stat().st_size if exists else None,
            }
        )
    return {"results_dir": str(results_dir), "artifacts": artifacts}


def write_results_catalog(results_dir: Path, output_path: Path | None = None) -> Path:
    target = output_path if output_path is not None else results_dir / "catalog.json"
    payload = build_results_catalog(results_dir)
    _ = target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
