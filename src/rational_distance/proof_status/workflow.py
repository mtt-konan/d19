"""Workflow orchestration for the proof_status pipeline.

The workflow is responsible for:

- deciding when to call PARI (expensive) vs cheap arithmetic methods,
- recording every method attempt into ``pair_method_attempts``,
- updating the materialised ``pair_proof_status`` row with the strongest
  conclusion reached so far,
- being safe to re-run incrementally: pairs already classified as
  ``no_solution`` or ``solution_found`` are not re-processed.

It does NOT decide what is mathematically rigorous — that lives in
``methods.py``. The workflow just trusts the outcome that each method
returns.
"""

from __future__ import annotations

import multiprocessing as mp
import sqlite3
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

from rational_distance.proof_status import schema as schema
from rational_distance.proof_status.methods import DEFAULT_METHOD_PIPELINE, MethodFn
from rational_distance.proof_status.types import MethodResult, PairProofStatus

# Re-export the canonical type from methods, plus the pipeline shape.
MethodPipeline = Iterable[tuple[str, MethodFn]]


@dataclass(frozen=True)
class WorkflowConfig:
    """Knobs for ``process_pair`` and ``process_pairs``."""

    methods: MethodPipeline = DEFAULT_METHOD_PIPELINE
    # If True, methods marked "skipped" still run (and are recorded). We never
    # actually skip in code — "skipped" is only an outcome the method returns
    # when its optional dependency is missing.
    record_skipped: bool = True
    # If True, re-run methods even for pairs already terminal. Useful when a
    # method is implemented for the first time and you want to re-classify the
    # current ``hard_case`` set.
    rerun_terminal: bool = False


_TERMINAL_STATUSES = frozenset({"no_solution", "solution_found"})


def _is_terminal(status: PairProofStatus | None) -> bool:
    return status is not None and status.status in _TERMINAL_STATUSES


def _coerce_int(value: object, default: int | None) -> int | None:
    """Best-effort coercion of a method-supplied detail value to ``int | None``.

    ``value is None`` is treated as "absent" — we keep the running ``default``
    rather than overwriting it with None. This matters because methods that
    do not produce a particular column (e.g. the Heegner stub does not produce
    ``rank_lower``) leave ``details.get(...)`` as None, and we don't want them
    to clobber what a previous method already stored.
    """
    if value is None:
        return default
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return default


def _aggregate_details(
    method: str,
    result: MethodResult,
    *,
    rank_lower: int | None,
    rank_upper: int | None,
    concordant_n_count: int | None,
    chain_compatible_count: int | None,
) -> dict[str, int | None]:
    """Fold one method's details into the running pair-level summary.

    The four named arguments carry the values that previous methods in the
    pipeline have already accumulated. Each method only updates the columns
    it owns; missing fields fall through unchanged.
    """
    details = result.details

    if method in {"rank_zero", "heegner"}:
        rank_lower = _coerce_int(details.get("rank_lower"), rank_lower)
        rank_upper = _coerce_int(details.get("rank_upper"), rank_upper)
    if method == "factor_concordant":
        concordant_n_count = _coerce_int(
            details.get("concordant_n_count"), concordant_n_count
        )
        chain_compatible_count = _coerce_int(
            details.get("chain_compatible_count"), chain_compatible_count
        )

    return {
        "rank_lower": rank_lower,
        "rank_upper": rank_upper,
        "concordant_n_count": concordant_n_count,
        "chain_compatible_count": chain_compatible_count,
    }


def process_pair(
    conn: sqlite3.Connection,
    A: int,
    B: int,
    config: WorkflowConfig | None = None,
) -> PairProofStatus:
    """Run the configured method pipeline on one ``(A, B)`` pair.

    The pipeline stops as soon as a method returns ``no_solution`` or
    ``solution_found`` (a terminal outcome). All non-terminal outcomes
    (``pass``, ``inconclusive``, ``skipped``, ``error``) are still recorded
    in ``pair_method_attempts``.

    Returns the final materialised status row.
    """
    config = config or WorkflowConfig()

    existing = schema.get_pair_status(conn, A, B)
    if not config.rerun_terminal and existing is not None and _is_terminal(existing):
        return existing

    # Aggregated columns evolve as methods run.
    rank_lower = existing.rank_lower if existing else None
    rank_upper = existing.rank_upper if existing else None
    concordant_n_count = existing.concordant_n_count if existing else None
    chain_compatible_count = existing.chain_compatible_count if existing else None

    terminal_status: str | None = None
    terminal_method: str | None = None
    terminal_notes: str = ""

    for method_name, method_fn in config.methods:
        result = method_fn(A, B)
        # Defensive: methods may forget to set the name; trust the registry.
        if result.method != method_name:
            result = MethodResult(
                method=method_name,
                outcome=result.outcome,
                details=result.details,
                elapsed_s=result.elapsed_s,
                notes=result.notes,
            )

        if result.outcome == "skipped" and not config.record_skipped:
            continue

        schema.record_method_attempt(conn, A=A, B=B, result=result)

        agg = _aggregate_details(
            method_name,
            result,
            rank_lower=rank_lower,
            rank_upper=rank_upper,
            concordant_n_count=concordant_n_count,
            chain_compatible_count=chain_compatible_count,
        )
        rank_lower = agg["rank_lower"]
        rank_upper = agg["rank_upper"]
        concordant_n_count = agg["concordant_n_count"]
        chain_compatible_count = agg["chain_compatible_count"]

        if result.outcome == "no_solution":
            terminal_status = "no_solution"
            terminal_method = method_name
            terminal_notes = result.notes
            break
        if result.outcome == "solution_found":
            terminal_status = "solution_found"
            terminal_method = method_name
            terminal_notes = result.notes
            break

    final_status = terminal_status or "hard_case"
    final_method = terminal_method or "exhausted"
    final_notes = terminal_notes or (
        "All methods returned non-terminal outcomes; classified as hard_case."
    )

    schema.upsert_pair_status(
        conn,
        A=A,
        B=B,
        status=final_status,
        method=final_method,
        rank_lower=rank_lower,
        rank_upper=rank_upper,
        concordant_n_count=concordant_n_count,
        chain_compatible_count=chain_compatible_count,
        notes=final_notes,
    )

    updated = schema.get_pair_status(conn, A, B)
    if updated is None:
        # Should be unreachable: upsert_pair_status just wrote this row.
        raise RuntimeError(
            f"proof_status: failed to read back row for pair ({A}, {B}) after upsert"
        )
    return updated


def process_pairs(
    conn: sqlite3.Connection,
    pairs: Iterable[tuple[int, int]],
    config: WorkflowConfig | None = None,
    on_pair: Callable[[PairProofStatus], None] | None = None,
) -> dict[str, int]:
    """Run ``process_pair`` over many pairs and return a status histogram."""
    config = config or WorkflowConfig()
    counts: dict[str, int] = {}
    for A, B in pairs:
        status = process_pair(conn, A, B, config)
        counts[status.status] = counts.get(status.status, 0) + 1
        if on_pair is not None:
            on_pair(status)
    return counts


# ---------------------------------------------------------------------------
# Parallel / batched path
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PairComputeResult:
    """Result of running the method pipeline on one pair WITHOUT touching
    the SQLite database.

    Used by the parallel path: workers compute these in subprocesses,
    the main process serialises the database writes.
    """

    A: int
    B: int
    final_status: str  # "no_solution" / "solution_found" / "hard_case"
    final_method: str  # method that produced the terminal outcome, or "exhausted"
    final_notes: str
    rank_lower: int | None
    rank_upper: int | None
    concordant_n_count: int | None
    chain_compatible_count: int | None
    method_results: tuple[MethodResult, ...]


def compute_pair_status(
    A: int, B: int, methods: tuple[tuple[str, MethodFn], ...] = DEFAULT_METHOD_PIPELINE,
) -> PairComputeResult:
    """Pure compute path: run the configured method pipeline on one pair
    and return all results. Does NOT touch any database.

    Mirrors the logic of ``process_pair`` but isolates it from persistence
    so that workers in a multiprocessing pool can call it directly.
    """
    rank_lower: int | None = None
    rank_upper: int | None = None
    concordant_n_count: int | None = None
    chain_compatible_count: int | None = None

    method_results: list[MethodResult] = []

    terminal_status: str | None = None
    terminal_method: str | None = None
    terminal_notes: str = ""

    for method_name, method_fn in methods:
        result = method_fn(A, B)
        # Defensive: methods may forget to set the name; trust the registry.
        if result.method != method_name:
            result = MethodResult(
                method=method_name,
                outcome=result.outcome,
                details=result.details,
                elapsed_s=result.elapsed_s,
                notes=result.notes,
            )

        method_results.append(result)

        agg = _aggregate_details(
            method_name,
            result,
            rank_lower=rank_lower,
            rank_upper=rank_upper,
            concordant_n_count=concordant_n_count,
            chain_compatible_count=chain_compatible_count,
        )
        rank_lower = agg["rank_lower"]
        rank_upper = agg["rank_upper"]
        concordant_n_count = agg["concordant_n_count"]
        chain_compatible_count = agg["chain_compatible_count"]

        if result.outcome == "no_solution":
            terminal_status = "no_solution"
            terminal_method = method_name
            terminal_notes = result.notes
            break
        if result.outcome == "solution_found":
            terminal_status = "solution_found"
            terminal_method = method_name
            terminal_notes = result.notes
            break

    final_status = terminal_status or "hard_case"
    final_method = terminal_method or "exhausted"
    final_notes = terminal_notes or (
        "All methods returned non-terminal outcomes; classified as hard_case."
    )

    return PairComputeResult(
        A=A,
        B=B,
        final_status=final_status,
        final_method=final_method,
        final_notes=final_notes,
        rank_lower=rank_lower,
        rank_upper=rank_upper,
        concordant_n_count=concordant_n_count,
        chain_compatible_count=chain_compatible_count,
        method_results=tuple(method_results),
    )


def _persist_compute_result(
    conn: sqlite3.Connection, result: PairComputeResult
) -> None:
    """Write a worker's PairComputeResult into the database WITHOUT
    committing. The caller is expected to commit periodically."""
    for r in result.method_results:
        schema.record_method_attempt(
            conn, A=result.A, B=result.B, result=r, commit=False
        )

    schema.upsert_pair_status(
        conn,
        A=result.A,
        B=result.B,
        status=result.final_status,
        method=result.final_method,
        rank_lower=result.rank_lower,
        rank_upper=result.rank_upper,
        concordant_n_count=result.concordant_n_count,
        chain_compatible_count=result.chain_compatible_count,
        notes=result.final_notes,
        commit=False,
    )


def _worker_compute(packed: tuple[int, int]) -> PairComputeResult:
    """Top-level helper so it is picklable for multiprocessing.

    Methods are taken from ``DEFAULT_METHOD_PIPELINE`` directly inside the
    worker — passing the tuple via Pool args adds pickling cost without
    helping (every worker would receive the same value).
    """
    A, B = packed
    return compute_pair_status(A, B, DEFAULT_METHOD_PIPELINE)


def process_pairs_parallel(
    conn: sqlite3.Connection,
    pairs: Iterable[tuple[int, int]],
    *,
    workers: int = 1,
    commit_every: int = 1000,
    chunksize: int = 50,
    skip_terminal: bool = True,
    on_result: Callable[[PairComputeResult], None] | None = None,
) -> dict[str, int]:
    """Parallel sibling of ``process_pairs`` with batched commits.

    - ``workers``: number of worker processes (1 = sequential, no Pool).
    - ``commit_every``: commit the SQLite transaction every N pairs.
    - ``chunksize``: ``Pool.imap_unordered`` chunksize knob.
    - ``skip_terminal``: skip pairs already classified ``no_solution`` /
      ``solution_found``. Mirrors ``WorkflowConfig.rerun_terminal=False``.

    Method pipeline is the project default (``DEFAULT_METHOD_PIPELINE``).
    Use ``process_pair`` / ``process_pairs`` for custom pipelines or
    when ``rerun_terminal=True``.

    Returns the status histogram (same shape as ``process_pairs``).
    """
    pairs_list = list(pairs)
    if skip_terminal:
        kept: list[tuple[int, int]] = []
        for A, B in pairs_list:
            existing = schema.get_pair_status(conn, A, B)
            if not _is_terminal(existing):
                kept.append((A, B))
        pairs_list = kept

    counts: dict[str, int] = {}
    pending = 0

    def _handle(result: PairComputeResult) -> None:
        nonlocal pending
        _persist_compute_result(conn, result)
        counts[result.final_status] = counts.get(result.final_status, 0) + 1
        pending += 1
        if pending >= commit_every:
            conn.commit()
            pending = 0
        if on_result is not None:
            on_result(result)

    if workers <= 1:
        for A, B in pairs_list:
            _handle(_worker_compute((A, B)))
    else:
        # spawn context: macOS / Linux; avoids fork+PARI library quirks.
        ctx = mp.get_context("spawn")
        with ctx.Pool(processes=workers) as pool:
            for result in pool.imap_unordered(
                _worker_compute, pairs_list, chunksize=chunksize
            ):
                _handle(result)

    if pending > 0:
        conn.commit()

    return counts


__all__ = [
    "MethodFn",
    "MethodPipeline",
    "PairComputeResult",
    "WorkflowConfig",
    "compute_pair_status",
    "process_pair",
    "process_pairs",
    "process_pairs_parallel",
]
