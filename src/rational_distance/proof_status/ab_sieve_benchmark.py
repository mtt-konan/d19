from __future__ import annotations

import itertools
import time
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import TypeAlias

from rational_distance.parallel import ParallelConfig
from rational_distance.proof_status.ab_sieve_methods import (
    PairEvalContext,
    resolve_method_names,
)
from rational_distance.proof_status.methods import DEFAULT_METHOD_PIPELINE
from rational_distance.proof_status.types import MethodResult

CORE_METHOD_NAMES: tuple[str, ...] = (
    "safe_sieve",
    "chain_closure_mod_sieve",
    "factor_concordant",
)
TAIL_METHOD_NAMES: tuple[str, ...] = ("f2_rank", "rank_zero", "heegner")
FULL_METHOD_NAMES: tuple[str, ...] = CORE_METHOD_NAMES + TAIL_METHOD_NAMES
HEAD_VALIDATION_ORDERS: tuple[tuple[str, ...], ...] = (
    (
        "safe_sieve",
        "multi_n_sieve",
        "concordant_search",
        "chain_closure_mod_sieve",
    ),
    (
        "chain_closure_mod_sieve",
        "multi_n_sieve",
        "concordant_search",
        "safe_sieve",
    ),
    (
        "concordant_search",
        "safe_sieve",
        "multi_n_sieve",
        "chain_closure_mod_sieve",
    ),
    (
        "multi_n_sieve",
        "safe_sieve",
        "concordant_search",
        "chain_closure_mod_sieve",
    ),
)
SAFE_TOP2_ORDERS: tuple[tuple[str, ...], ...] = (
    (
        "safe_sieve",
        "chain_closure_mod_sieve",
        "multi_n_sieve",
        "concordant_search",
    ),
    (
        "safe_sieve",
        "chain_closure_mod_sieve",
        "concordant_search",
        "multi_n_sieve",
    ),
)


@dataclass(frozen=True)
class OrderSpec:
    name: str
    method_names: tuple[str, ...]
    category: str


@dataclass(frozen=True)
class PairBenchmarkResult:
    A: int
    B: int
    final_status: str
    terminal_method: str
    elapsed_s: float
    method_results: tuple[MethodResult, ...]


@dataclass
class OrderBenchmarkSummary:
    spec: OrderSpec
    n_pairs: int = 0
    sum_pair_elapsed_s: float = 0.0
    wall_elapsed_s: float = 0.0
    final_status_counts: Counter[str] = field(default_factory=Counter)
    terminal_method_counts: Counter[str] = field(default_factory=Counter)
    method_attempt_counts: Counter[str] = field(default_factory=Counter)
    method_outcome_counts: Counter[tuple[str, str]] = field(default_factory=Counter)
    method_elapsed_s: defaultdict[str, float] = field(default_factory=lambda: defaultdict(float))

    def add_result(self, result: PairBenchmarkResult) -> None:
        self.n_pairs += 1
        self.sum_pair_elapsed_s += result.elapsed_s
        self.final_status_counts[result.final_status] += 1
        self.terminal_method_counts[result.terminal_method] += 1
        for method_result in result.method_results:
            self.method_attempt_counts[method_result.method] += 1
            self.method_outcome_counts[(method_result.method, method_result.outcome)] += 1
            self.method_elapsed_s[method_result.method] += method_result.elapsed_s

    @property
    def total_elapsed_s(self) -> float:
        return self.wall_elapsed_s

    def method_report(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for method in self.spec.method_names:
            attempts = self.method_attempt_counts.get(method, 0)
            kills = self.method_outcome_counts.get((method, "no_solution"), 0)
            solutions = self.method_outcome_counts.get((method, "solution_found"), 0)
            passes = self.method_outcome_counts.get((method, "pass"), 0)
            inconclusive = self.method_outcome_counts.get((method, "inconclusive"), 0)
            skipped = self.method_outcome_counts.get((method, "skipped"), 0)
            errors = self.method_outcome_counts.get((method, "error"), 0)
            elapsed_s = self.method_elapsed_s.get(method, 0.0)
            rows.append(
                {
                    "method": method,
                    "attempts": attempts,
                    "kills": kills,
                    "solutions": solutions,
                    "passes": passes,
                    "inconclusive": inconclusive,
                    "skipped": skipped,
                    "errors": errors,
                    "kill_rate": (kills / attempts) if attempts else 0.0,
                    "terminal_rate": ((kills + solutions) / attempts) if attempts else 0.0,
                    "is_empty": kills == 0 and solutions == 0,
                    "elapsed_s": elapsed_s,
                    "mean_elapsed_ms": (elapsed_s * 1000 / attempts) if attempts else 0.0,
                }
            )
        return rows

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.spec.name,
            "method_names": list(self.spec.method_names),
            "category": self.spec.category,
            "n_pairs": self.n_pairs,
            "wall_elapsed_s": self.wall_elapsed_s,
            "sum_pair_elapsed_s": self.sum_pair_elapsed_s,
            "final_status_counts": dict(self.final_status_counts),
            "terminal_method_counts": dict(self.terminal_method_counts),
            "method_report": self.method_report(),
        }


PairSource: TypeAlias = Iterable[tuple[int, int]] | Callable[[], Iterable[tuple[int, int]]]


def build_core_order_specs(prefix: tuple[str, ...] = ()) -> list[OrderSpec]:
    remaining = tuple(name for name in CORE_METHOD_NAMES if name not in prefix)
    return [
        OrderSpec(
            name="core__" + "__".join((*prefix, *perm)),
            method_names=(*prefix, *perm),
            category="core",
        )
        for perm in itertools.permutations(remaining)
    ]


def build_tail_order_specs(best_core: tuple[str, ...]) -> list[OrderSpec]:
    return [
        OrderSpec(
            name="tail__" + "__".join(best_core + perm),
            method_names=best_core + perm,
            category="tail",
        )
        for perm in itertools.permutations(TAIL_METHOD_NAMES)
    ]


def build_incremental_specs(best_core: tuple[str, ...]) -> list[OrderSpec]:
    return [
        OrderSpec(
            name=f"incremental__{'__'.join(best_core)}__{tail_name}",
            method_names=(*best_core, tail_name),
            category="incremental",
        )
        for tail_name in TAIL_METHOD_NAMES
    ]


def build_full_order_specs() -> list[OrderSpec]:
    return [
        OrderSpec(
            name="full__" + "__".join(perm),
            method_names=perm,
            category="full",
        )
        for perm in itertools.permutations(FULL_METHOD_NAMES)
    ]


def build_head_validation_specs() -> list[OrderSpec]:
    return [
        OrderSpec(
            name="head__" + "__".join(method_names),
            method_names=method_names,
            category="head",
        )
        for method_names in HEAD_VALIDATION_ORDERS
    ]


def build_safe_top2_specs() -> list[OrderSpec]:
    return [
        OrderSpec(
            name="safe_top2__" + "__".join(method_names),
            method_names=method_names,
            category="safe_top2",
        )
        for method_names in SAFE_TOP2_ORDERS
    ]


def build_legacy_baseline_spec() -> OrderSpec:
    return OrderSpec(
        name="legacy_default_pipeline",
        method_names=tuple(name for name, _ in DEFAULT_METHOD_PIPELINE),
        category="legacy",
    )


def evaluate_pair_in_order(A: int, B: int, spec: OrderSpec) -> PairBenchmarkResult:
    started = time.perf_counter()
    ctx = PairEvalContext()
    method_results: list[MethodResult] = []
    final_status = "hard_case"
    terminal_method = "exhausted"

    for method_name, method_fn in resolve_method_names(spec.method_names):
        result = method_fn(A, B, ctx)
        if result.method != method_name:
            result = MethodResult(
                method=method_name,
                outcome=result.outcome,
                details=result.details,
                elapsed_s=result.elapsed_s,
                notes=result.notes,
            )
        method_results.append(result)
        if result.outcome in {"no_solution", "solution_found"}:
            final_status = result.outcome
            terminal_method = method_name
            break

    return PairBenchmarkResult(
        A=A,
        B=B,
        final_status=final_status,
        terminal_method=terminal_method,
        elapsed_s=time.perf_counter() - started,
        method_results=tuple(method_results),
    )


def _iter_pairs(pairs: PairSource) -> Iterable[tuple[int, int]]:
    if callable(pairs):
        return pairs()
    return pairs


def _make_batches(pairs: Iterable[tuple[int, int]], batch_size: int) -> Iterable[list[tuple[int, int]]]:
    batch: list[tuple[int, int]] = []
    for pair in pairs:
        batch.append(pair)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def _worker_run_batch(
    packed: tuple[OrderSpec, list[tuple[int, int]]],
) -> list[PairBenchmarkResult]:
    spec, batch = packed
    return [evaluate_pair_in_order(A, B, spec) for A, B in batch]


def benchmark_specs(
    *,
    specs: Iterable[OrderSpec],
    pairs: PairSource,
    parallel: ParallelConfig,
    batch_size: int,
) -> list[OrderBenchmarkSummary]:
    summaries: list[OrderBenchmarkSummary] = []
    with parallel.executor() as executor:
        for spec in specs:
            summary = OrderBenchmarkSummary(spec=spec)

            def _handle(
                batch_results: list[PairBenchmarkResult],
                *,
                current_summary: OrderBenchmarkSummary = summary,
            ) -> None:
                for result in batch_results:
                    current_summary.add_result(result)

            started = time.perf_counter()
            _ = executor.map(
                _worker_run_batch,
                ((spec, batch) for batch in _make_batches(_iter_pairs(pairs), batch_size)),
                on_result=_handle,
                collect_results=False,
            )
            summary.wall_elapsed_s = time.perf_counter() - started
            summaries.append(summary)
    return summaries


__all__ = [
    "CORE_METHOD_NAMES",
    "FULL_METHOD_NAMES",
    "HEAD_VALIDATION_ORDERS",
    "SAFE_TOP2_ORDERS",
    "TAIL_METHOD_NAMES",
    "OrderBenchmarkSummary",
    "OrderSpec",
    "PairBenchmarkResult",
    "benchmark_specs",
    "build_core_order_specs",
    "build_full_order_specs",
    "build_head_validation_specs",
    "build_incremental_specs",
    "build_legacy_baseline_spec",
    "build_safe_top2_specs",
    "build_tail_order_specs",
    "evaluate_pair_in_order",
]
