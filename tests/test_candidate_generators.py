from __future__ import annotations

import json
import subprocess
import sys
from math import gcd
from pathlib import Path
from typing import cast

from pytest import MonkeyPatch

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant import candidate_generators as candidate_module
from rational_distance.concordant.candidate_generators import (
    iter_coprime_pairs,
    iter_safe_coprime_pairs,
    run_generator_benchmark,
)
from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


def test_iter_coprime_pairs_matches_direct_gcd_definition() -> None:
    max_hyp = 8

    expected = [
        (a, b) for a in range(1, max_hyp + 1) for b in range(a + 1, max_hyp + 1) if gcd(a, b) == 1
    ]

    assert list(iter_coprime_pairs(max_hyp)) == expected


def test_iter_safe_coprime_pairs_applies_safe_sieve_definition() -> None:
    max_hyp = 10

    expected = [
        (a, b)
        for a in range(1, max_hyp + 1)
        for b in range(a + 1, max_hyp + 1)
        if gcd(a, b) == 1 and allow_reduced_pair(a, b)
    ]

    assert list(iter_safe_coprime_pairs(max_hyp)) == expected
    assert list(iter_safe_coprime_pairs(max_hyp)) == [
        (1, 3),
        (1, 7),
        (3, 5),
        (5, 7),
        (7, 9),
    ]


def test_iter_safe_coprime_pairs_does_not_depend_on_all_coprime_stream(
    monkeypatch: MonkeyPatch,
) -> None:
    def fail_iter_coprime_pairs(max_hyp: int):
        raise AssertionError(f"iter_coprime_pairs should not be called for {max_hyp}")

    monkeypatch.setattr(candidate_module, "iter_coprime_pairs", fail_iter_coprime_pairs)

    assert list(candidate_module.iter_safe_coprime_pairs(10)) == [
        (1, 3),
        (1, 7),
        (3, 5),
        (5, 7),
        (7, 9),
    ]


def test_generators_reject_non_positive_max_hyp() -> None:
    for generator in (iter_coprime_pairs, iter_safe_coprime_pairs):
        try:
            _ = list(generator(0))
        except ValueError as exc:
            assert str(exc) == "max_hyp must be positive"
        else:
            raise AssertionError("generator must reject non-positive max_hyp")


def test_run_generator_benchmark_reports_expected_rows() -> None:
    max_hyp = 200

    rows = run_generator_benchmark(max_hyp)
    by_name = {row.name: row for row in rows}

    assert tuple(by_name) == ("all_coprime", "safe_coprime", "multi_n")
    assert by_name["all_coprime"].pair_count == len(list(iter_coprime_pairs(max_hyp)))
    assert by_name["safe_coprime"].pair_count == len(list(iter_safe_coprime_pairs(max_hyp)))
    assert by_name["multi_n"].pair_count == len(fast_multi_concordant_pairs(max_hyp))
    assert by_name["multi_n"].carries_concordant_n is True
    assert by_name["multi_n"].min_n_count is None or by_name["multi_n"].min_n_count >= 2


def test_cli_writes_json_summary(tmp_path: Path) -> None:
    output_path = tmp_path / "candidate_generators_200.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/benchmark/benchmark_candidate_generators.py",
            "--max-hyp",
            "200",
            "--json-out",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "all_coprime" in completed.stdout
    assert "safe_coprime" in completed.stdout
    assert "multi_n" in completed.stdout

    rows = cast(list[dict[str, object]], json.loads(output_path.read_text(encoding="utf-8")))
    assert [row["name"] for row in rows] == ["all_coprime", "safe_coprime", "multi_n"]
    assert rows[2]["carries_concordant_n"] is True


def test_cli_can_run_only_multi_n_generator(tmp_path: Path) -> None:
    output_path = tmp_path / "candidate_generators_200_multi_n.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/benchmark/benchmark_candidate_generators.py",
            "--max-hyp",
            "200",
            "--only",
            "multi_n",
            "--json-out",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "multi_n" in completed.stdout
    assert "all_coprime" not in completed.stdout
    assert "safe_coprime" not in completed.stdout

    rows = cast(list[dict[str, object]], json.loads(output_path.read_text(encoding="utf-8")))
    assert [row["name"] for row in rows] == ["multi_n"]
    assert rows[0]["pair_count"] == len(fast_multi_concordant_pairs(200))
