from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.a1_shells import evaluate_shell
from scripts.theory.aa_bb.consolidation_inputs import load_a0

DATA = ROOT / "data/theory/aa_bb/wl500"


@pytest.mark.parametrize(
    ("bound", "expected"),
    [
        (6, (8, 8, 0, 0, 0, 0)),
        (7, (24, 12, 12, 14, 12, 2)),
        (8, (16, 14, 2, 2, 0, 2)),
        (9, (24, 16, 8, 8, 8, 0)),
        (10, (16, 6, 10, 10, 10, 0)),
    ],
)
def test_shell_summary(bound: int, expected: tuple[int, ...]) -> None:
    result = evaluate_shell(load_a0(DATA), bound)
    summary = result.summary
    actual = tuple(
        summary[key]
        for key in (
            "sample_count",
            "full_rank_sample_count",
            "kernel_sample_count",
            "kernel_support_entry_count",
            "active_new_support_entry_count",
            "excluded_duplicate_or_processed_support_entry_count",
        )
    )
    assert actual == expected


def test_shell_matrix_contains_exact_rank_kernel_and_basis_data() -> None:
    result = evaluate_shell(load_a0(DATA), 7)
    matrix = next(
        row for row in result.matrices if row["sample"]["side"] == "AA" and row["sample"]["A"] == 3
    )
    assert matrix["sample"] == {
        "side": "AA",
        "A": 3,
        "B": 7,
        "L": 3,
        "T": 10,
        "sqrt_q": 136,
        "primitive": True,
    }
    assert matrix["computed_rank"] == 2
    assert matrix["kernel_diagnostics"] == {
        "kernel_dimension": 1,
        "basis_vectors": [[1, 1, 1]],
        "basis_supports": [["u_3", "v_5", "w_17"]],
    }
    assert (
        result.active_supports[0]["candidate_id"]
        == "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate"
    )
