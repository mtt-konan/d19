from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.pari_ell2cover_mixed_residuals import (
    cover_row,
    write_jsonl,
)


class FakePari:
    def ellinit(self, model: list[int]) -> list[int]:
        return model

    def ellrank(self, curve: list[int], effort: int) -> list[object]:
        assert effort == 1
        return [0, 2, 0, []]

    def ell2cover(self, curve: list[int]) -> list[list[object]]:
        return [["x^4 - 1", []], ["x^4 + 1", []]]

    def hyperellratpoints(self, quartic: object, height: int) -> list[list[int]]:
        assert height == 100
        if quartic == "x^4 - 1":
            return [[1, 0], [-1, 0]]
        return []


def test_cover_row_records_cover_point_counts() -> None:
    row = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "rank": "0/2",
        "model": [0, 196194, 0, -699602500, -137257812885000],
    }

    result = cover_row(row, pari=FakePari(), height=100, effort=1)

    assert result == {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "input_rank": "0/2",
        "model": [0, 196194, 0, -699602500, -137257812885000],
        "status": "ok",
        "ellrank": {"lower": 0, "upper": 2, "sha2_lower": 0},
        "cover_count": 2,
        "covers": [
            {
                "index": 1,
                "quartic": "x^4 - 1",
                "point_count": 2,
                "points": ["[1, 0]", "[-1, 0]"],
            },
            {
                "index": 2,
                "quartic": "x^4 + 1",
                "point_count": 0,
                "points": [],
            },
        ],
        "covers_without_points": 1,
    }


def test_write_jsonl_writes_cover_rows(tmp_path: Path) -> None:
    out_path = tmp_path / "covers.jsonl"

    write_jsonl(out_path, [{"status": "ok"}])

    assert out_path.read_text(encoding="utf-8") == '{"status": "ok"}\n'
