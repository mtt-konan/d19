"""Helpers for the max_hyp=10000 multi-concordant ground-truth dataset."""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MULTI_CONCORDANT_PATH = ROOT / "results" / "multi_concordant_N_max10000.jsonl"


@dataclass(frozen=True)
class MultiConcordantPair:
    A: int
    B: int
    n_concordant: int
    concordant_N: list[int]
    A_plus_B: int
    closure_pairs: list[list[int]]


def _require_int(value: object, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    return value


def _require_int_list(value: object, field_name: str) -> list[int]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list[int]")

    items: list[int] = []
    for item in value:
        if not isinstance(item, int):
            raise ValueError(f"{field_name} must be a list[int]")
        items.append(item)
    return items


def _require_int_pair_list(value: object, field_name: str) -> list[list[int]]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list[list[int]]")

    pairs: list[list[int]] = []
    for pair in value:
        if not isinstance(pair, list):
            raise ValueError(f"{field_name} must be a list[list[int]]")

        typed_pair: list[int] = []
        for item in pair:
            if not isinstance(item, int):
                raise ValueError(f"{field_name} must be a list[list[int]]")
            typed_pair.append(item)
        pairs.append(typed_pair)
    return pairs


class MultiConcordantRow(TypedDict):
    A: int
    B: int
    n_concordant: int
    concordant_N: list[int]
    A_plus_B: int
    closure_pairs: list[list[int]]


def iter_multi_concordant_pairs(
    dataset_path: Path = DEFAULT_MULTI_CONCORDANT_PATH,
) -> Iterator[MultiConcordantPair]:
    with dataset_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            row = cast(dict[str, object], json.loads(line))
            typed_row: MultiConcordantRow = {
                "A": _require_int(row["A"], "A"),
                "B": _require_int(row["B"], "B"),
                "n_concordant": _require_int(row["n_concordant"], "n_concordant"),
                "concordant_N": _require_int_list(row["concordant_N"], "concordant_N"),
                "A_plus_B": _require_int(row["A_plus_B"], "A_plus_B"),
                "closure_pairs": _require_int_pair_list(row["closure_pairs"], "closure_pairs"),
            }
            yield MultiConcordantPair(
                A=typed_row["A"],
                B=typed_row["B"],
                n_concordant=typed_row["n_concordant"],
                concordant_N=typed_row["concordant_N"],
                A_plus_B=typed_row["A_plus_B"],
                closure_pairs=typed_row["closure_pairs"],
            )


def load_multi_concordant_index(
    dataset_path: Path = DEFAULT_MULTI_CONCORDANT_PATH,
) -> dict[tuple[int, int], MultiConcordantPair]:
    index: dict[tuple[int, int], MultiConcordantPair] = {}
    for row in iter_multi_concordant_pairs(dataset_path):
        index[(row.A, row.B)] = row
    return index


def lookup_multi_concordant_pair(
    A: int,
    B: int,
    dataset_path: Path = DEFAULT_MULTI_CONCORDANT_PATH,
) -> MultiConcordantPair | None:
    a, b = sorted((A, B))
    return load_multi_concordant_index(dataset_path).get((a, b))
