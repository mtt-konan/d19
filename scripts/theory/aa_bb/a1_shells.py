"""Deterministic finite ``M_tail`` shell arithmetic for wl502-wl516."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from scripts.theory import (
    audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder as wl481,
)

SHELL_BOUNDS = (6, 7, 8, 9, 10)


@dataclass(frozen=True)
class ShellResult:
    shell_bound: int
    matrices: tuple[dict[str, Any], ...]
    active_supports: tuple[dict[str, Any], ...]
    excluded_supports: tuple[dict[str, Any], ...]

    @property
    def summary(self) -> dict[str, int]:
        full = sum(
            row["computed_rank_status"] == "full_for_this_finite_sample" for row in self.matrices
        )
        basis = sum(len(row["kernel_diagnostics"]["basis_supports"]) for row in self.matrices)
        return {
            "sample_count": len(self.matrices),
            "full_rank_sample_count": full,
            "kernel_sample_count": len(self.matrices) - full,
            "kernel_support_entry_count": basis,
            "active_new_support_entry_count": len(self.active_supports),
            "excluded_duplicate_or_processed_support_entry_count": len(self.excluded_supports),
        }

    def projection(self) -> dict[str, Any]:
        unique_supports = sorted(
            {support for row in self.active_supports for support in row["candidate_support"]}
        )
        return {
            "shell_bound": self.shell_bound,
            "sample_summary": {**self.summary, "unique_active_supports": unique_supports},
            "rank_kernel_summary_by_sample": [
                {
                    "sample": row["sample"],
                    "rank_needed": row["rank_needed"],
                    "computed_rank": row["computed_rank"],
                    "computed_rank_status": row["computed_rank_status"],
                    "kernel_dimension": row["kernel_diagnostics"]["kernel_dimension"],
                    "basis_supports": row["kernel_diagnostics"]["basis_supports"],
                }
                for row in self.matrices
            ],
            "active_new_kernel_supports": list(self.active_supports),
            "excluded_duplicate_or_processed_supports": list(self.excluded_supports),
        }


def _samples(shell_bound: int) -> list[tuple[str, int, int]]:
    if shell_bound not in SHELL_BOUNDS:
        raise ValueError(f"unsupported shell bound: {shell_bound}")
    return [
        (side, a, b)
        for side in ("AA", "BB")
        for a in range(1, shell_bound + 1)
        for b in range(1, shell_bound + 1)
        if max(a, b) == shell_bound and math.gcd(a, b) == 1
    ]


def _candidate_id(sample: dict[str, Any], support: list[str], shell_bound: int) -> str:
    return (
        f"{sample['side']}_A{sample['A']}_B{sample['B']}_"
        f"{'_plus_'.join(support)}_m_tail_shell{shell_bound}_candidate"
    )


def evaluate_shell(a0: Any, shell_bound: int) -> ShellResult:
    """Recompute one primitive shell and route every kernel basis support.

    The A0 ledger is the tracked routing authority.  Arithmetic comes only
    from the explicit wl481 matrix kernel; no ignored result is read.
    """

    matrices = tuple(
        wl481.build_sample_m_tail_matrix(side=side, A=a, B=b)
        for side, a, b in _samples(shell_bound)
    )
    ledger = {row["candidate_id"]: row for row in a0.ledger}
    active: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for matrix in matrices:
        sample = matrix["sample"]
        for support in matrix["kernel_diagnostics"]["basis_supports"]:
            candidate_id = _candidate_id(sample, support, shell_bound)
            row = ledger.get(candidate_id)
            if row is None:
                raise ValueError(f"A0 ledger lacks shell certificate {candidate_id}")
            item = {
                "candidate_id": candidate_id,
                "candidate_support": support,
                "sample": sample,
                "classification": row["classification"],
                "source_work_log": row["source_work_log"],
            }
            if row["classification"] == "already_closed":
                excluded.append(item)
            else:
                active.append(item)
    return ShellResult(shell_bound, matrices, tuple(active), tuple(excluded))
