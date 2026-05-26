# AB Sieve Pipeline and Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a context-aware `(A, B)` sieve benchmark harness that componentizes layers 1-4, keeps the legacy proof-status workflow unchanged, and benchmarks the default `24 + 6 + 3 + 1` order set using the shared parallel executor.

**Architecture:** Add a new context-aware sieve layer beside the existing `proof_status.methods` / `workflow` stack instead of rewriting it. The new layer reuses `MethodResult` and the existing rigorous methods for `safe_sieve`, `chain_closure_mod_sieve`, `rank_zero`, and `heegner`, but splits the current `factor_concordant` behavior into `concordant_search` and `multi_n_sieve` with a shared per-pair cache so order benchmarks are fair. A separate benchmark runner uses `ParallelConfig.executor()` with `collect_results=False` to reuse spawned workers across many order runs while aggregating timing and kill-rate stats in the main process.

**Tech Stack:** Python 3.12, `pytest`, existing `MethodResult` / `PairProofStatus` types, `multiprocessing` spawn via `rational_distance.parallel.ParallelConfig`, existing `(A, B)` generator in `rational_distance.concordant.pairs`.

---

## File structure

- Create: `src/rational_distance/proof_status/ab_sieve_methods.py`
  - Context-aware versions of layers 1-4.
  - Optional wrappers for `f2_rank`, `rank_zero`, `heegner`, plus legacy wrappers for `factor_concordant`, `chabauty`, `brauer_manin` so the benchmark can run the current default pipeline unchanged.
  - Shared `PairEvalContext` cache for concordant `N`.
- Create: `src/rational_distance/proof_status/ab_sieve_benchmark.py`
  - Order specs, pair evaluator, per-order aggregation, default benchmark-plan builders, and the parallel batch runner.
- Create: `scripts/benchmark_ab_sieve_orders.py`
  - CLI driver that generates `(A, B)` pairs, runs the core 24 orders, picks the fastest core order, then runs the extra `6 + 3 + 1` orders and writes JSON output.
- Create: `tests/test_ab_sieve_benchmark.py`
  - Unit tests for split layer 3/4 behavior, cache reuse, order-plan sizes, serial benchmark aggregation, and CLI smoke behavior.
- Modify: `tests/test_proof_status.py`
  - Regression tests that the legacy `DEFAULT_METHOD_PIPELINE` order and `run_factor_concordant` behavior remain intact.

---

### Task 1: Add context-aware split sieve methods

**Files:**
- Create: `src/rational_distance/proof_status/ab_sieve_methods.py`
- Test: `tests/test_ab_sieve_benchmark.py`

- [ ] **Step 1: Write the failing tests**

```python
from rational_distance.proof_status.ab_sieve_methods import (
    PairEvalContext,
    run_concordant_search_ctx,
    run_multi_n_sieve_ctx,
)


def test_concordant_search_and_multi_n_are_split() -> None:
    ctx = PairEvalContext()

    search = run_concordant_search_ctx(7, 45, ctx)
    multi = run_multi_n_sieve_ctx(7, 45, ctx)

    assert search.outcome == "pass"
    assert search.details["concordant_n_count"] == 1
    assert multi.outcome == "no_solution"
    assert multi.details["k"] == 1


def test_multi_n_reuses_cached_concordant_n() -> None:
    ctx = PairEvalContext()

    _ = run_concordant_search_ctx(153, 560, ctx)
    _ = run_multi_n_sieve_ctx(153, 560, ctx)

    assert ctx.factor_search_calls == 1
    assert ctx.concordant_n == [204, 420, 3900]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_concordant_search_and_multi_n_are_split tests/test_ab_sieve_benchmark.py::test_multi_n_reuses_cached_concordant_n -v`
Expected: FAIL with `ModuleNotFoundError` for `rational_distance.proof_status.ab_sieve_methods`.

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from rational_distance.concordant.factor_search import find_concordant_by_factorization
from rational_distance.concordant.two_descent_rank import f2_rank_of_concordant_pair
from rational_distance.proof_status.methods import (
    run_brauer_manin_stub,
    run_chain_closure_mod_sieve,
    run_chabauty_stub,
    run_factor_concordant,
    run_heegner_height,
    run_rank_zero,
    run_safe_sieve,
)
from rational_distance.proof_status.types import MethodResult


@dataclass
class PairEvalContext:
    concordant_n: list[int] | None = None
    factor_search_calls: int = 0


ContextMethod = Callable[[int, int, PairEvalContext], MethodResult]


def _get_concordant_n(A: int, B: int, ctx: PairEvalContext) -> list[int]:
    if ctx.concordant_n is None:
        ctx.concordant_n = find_concordant_by_factorization(A, B)
        ctx.factor_search_calls += 1
    return ctx.concordant_n


def run_safe_sieve_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_safe_sieve(A, B)


def run_chain_closure_mod_sieve_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_chain_closure_mod_sieve(A, B)


def run_concordant_search_ctx(A: int, B: int, ctx: PairEvalContext) -> MethodResult:
    started = time.perf_counter()
    ns = _get_concordant_n(A, B, ctx)
    elapsed = time.perf_counter() - started
    details = {
        "concordant_n_count": len(ns),
        "sample_concordant_n": ns[:16],
    }
    if not ns:
        return MethodResult(
            method="concordant_search",
            outcome="no_solution",
            details=details,
            elapsed_s=elapsed,
            notes="No concordant N exists (exhaustive factor enumeration).",
        )
    return MethodResult(
        method="concordant_search",
        outcome="pass",
        details=details,
        elapsed_s=elapsed,
        notes=f"Concordant search found {len(ns)} N values.",
    )


def run_multi_n_sieve_ctx(A: int, B: int, ctx: PairEvalContext) -> MethodResult:
    started = time.perf_counter()
    ns = _get_concordant_n(A, B, ctx)
    elapsed = time.perf_counter() - started
    details = {
        "k": len(ns),
        "concordant_n_count": len(ns),
        "sample_concordant_n": ns[:16],
    }
    if len(ns) < 2:
        return MethodResult(
            method="multi_n_sieve",
            outcome="no_solution",
            details=details,
            elapsed_s=elapsed,
            notes=f"Need at least 2 concordant N for multi-N; got {len(ns)}.",
        )
    return MethodResult(
        method="multi_n_sieve",
        outcome="pass",
        details=details,
        elapsed_s=elapsed,
        notes=f"Pair is multi-N with k={len(ns)}.",
    )


def run_f2_rank_ctx(A: int, B: int, ctx: PairEvalContext) -> MethodResult:
    started = time.perf_counter()
    ns = _get_concordant_n(A, B, ctx)
    if len(ns) < 2:
        return MethodResult(
            method="f2_rank",
            outcome="skipped",
            details={"reason": "need_at_least_two_concordant_n", "concordant_n_count": len(ns)},
            elapsed_s=time.perf_counter() - started,
            notes=f"Skipped: only {len(ns)} concordant N (need >=2 for F2-rank).",
        )
    f2_result = f2_rank_of_concordant_pair(A, B, ns)
    elapsed = time.perf_counter() - started
    rank_floor = max(0, f2_result.f2_rank - 2)
    details: dict[str, object] = {
        "f2_rank": f2_result.f2_rank,
        "k": len(ns),
        "saturated": f2_result.f2_rank == len(ns),
        "rank_lower": rank_floor if rank_floor > 0 else None,
    }
    if f2_result.minimal_relation is not None:
        details["minimal_relation"] = list(f2_result.minimal_relation)
    return MethodResult(
        method="f2_rank",
        outcome="pass",
        details=details,
        elapsed_s=elapsed,
        notes=f"F2-rank={f2_result.f2_rank} with k={len(ns)}.",
    )


def run_rank_zero_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_rank_zero(A, B)


def run_heegner_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_heegner_height(A, B)


def run_factor_concordant_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_factor_concordant(A, B)


def run_chabauty_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_chabauty_stub(A, B)


def run_brauer_manin_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_brauer_manin_stub(A, B)


METHOD_REGISTRY: dict[str, ContextMethod] = {
    "safe_sieve": run_safe_sieve_ctx,
    "chain_closure_mod_sieve": run_chain_closure_mod_sieve_ctx,
    "concordant_search": run_concordant_search_ctx,
    "multi_n_sieve": run_multi_n_sieve_ctx,
    "factor_concordant": run_factor_concordant_ctx,
    "f2_rank": run_f2_rank_ctx,
    "rank_zero": run_rank_zero_ctx,
    "heegner": run_heegner_ctx,
    "chabauty": run_chabauty_ctx,
    "brauer_manin": run_brauer_manin_ctx,
}


def resolve_method_names(names: tuple[str, ...]) -> tuple[tuple[str, ContextMethod], ...]:
    return tuple((name, METHOD_REGISTRY[name]) for name in names)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_concordant_search_and_multi_n_are_split tests/test_ab_sieve_benchmark.py::test_multi_n_reuses_cached_concordant_n -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_ab_sieve_benchmark.py src/rational_distance/proof_status/ab_sieve_methods.py
git commit -m "feat: add split ab-sieve methods with shared context"
```

---

### Task 2: Add order specs and pair evaluator

**Files:**
- Create: `src/rational_distance/proof_status/ab_sieve_benchmark.py`
- Test: `tests/test_ab_sieve_benchmark.py`

- [ ] **Step 1: Write the failing tests**

```python
from rational_distance.proof_status.ab_sieve_benchmark import (
    OrderSpec,
    build_core_order_specs,
    build_legacy_baseline_spec,
    evaluate_pair_in_order,
)


def test_core_order_builder_has_24_orders() -> None:
    specs = build_core_order_specs()
    assert len(specs) == 24
    assert {len(spec.method_names) for spec in specs} == {4}


def test_legacy_baseline_matches_default_pipeline() -> None:
    spec = build_legacy_baseline_spec()
    assert spec.name == "legacy_default_pipeline"
    assert spec.method_names == (
        "safe_sieve",
        "chain_closure_mod_sieve",
        "factor_concordant",
        "f2_rank",
        "rank_zero",
        "heegner",
        "chabauty",
        "brauer_manin",
    )


def test_evaluate_pair_short_circuits_on_multi_n() -> None:
    result = evaluate_pair_in_order(
        7,
        45,
        OrderSpec(
            name="split_only",
            method_names=("concordant_search", "multi_n_sieve"),
            category="test",
        ),
    )
    assert result.final_status == "no_solution"
    assert result.terminal_method == "multi_n_sieve"
    assert [r.method for r in result.method_results] == [
        "concordant_search",
        "multi_n_sieve",
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_core_order_builder_has_24_orders tests/test_ab_sieve_benchmark.py::test_legacy_baseline_matches_default_pipeline tests/test_ab_sieve_benchmark.py::test_evaluate_pair_short_circuits_on_multi_n -v`
Expected: FAIL with `ModuleNotFoundError` for `rational_distance.proof_status.ab_sieve_benchmark`.

- [ ] **Step 3: Write minimal implementation**

```python
from __future__ import annotations

import itertools
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from rational_distance.proof_status.ab_sieve_methods import PairEvalContext, resolve_method_names
from rational_distance.proof_status.methods import DEFAULT_METHOD_PIPELINE
from rational_distance.proof_status.types import MethodResult

CORE_METHOD_NAMES: tuple[str, ...] = (
    "safe_sieve",
    "chain_closure_mod_sieve",
    "concordant_search",
    "multi_n_sieve",
)
TAIL_METHOD_NAMES: tuple[str, ...] = ("f2_rank", "rank_zero", "heegner")


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
    total_elapsed_s: float = 0.0
    final_status_counts: Counter[str] = field(default_factory=Counter)
    terminal_method_counts: Counter[str] = field(default_factory=Counter)
    method_attempt_counts: Counter[str] = field(default_factory=Counter)
    method_outcome_counts: Counter[tuple[str, str]] = field(default_factory=Counter)
    method_elapsed_s: defaultdict[str, float] = field(default_factory=lambda: defaultdict(float))

    def add_result(self, result: PairBenchmarkResult) -> None:
        self.n_pairs += 1
        self.total_elapsed_s += result.elapsed_s
        self.final_status_counts[result.final_status] += 1
        self.terminal_method_counts[result.terminal_method] += 1
        for method_result in result.method_results:
            self.method_attempt_counts[method_result.method] += 1
            self.method_outcome_counts[(method_result.method, method_result.outcome)] += 1
            self.method_elapsed_s[method_result.method] += method_result.elapsed_s

    def method_report(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for method in self.spec.method_names:
            attempts = self.method_attempt_counts.get(method, 0)
            kills = self.method_outcome_counts.get((method, "no_solution"), 0)
            solved = self.method_outcome_counts.get((method, "solution_found"), 0)
            rows.append(
                {
                    "method": method,
                    "attempts": attempts,
                    "kills": kills,
                    "solutions": solved,
                    "kill_rate": (kills / attempts) if attempts else 0.0,
                    "is_empty": kills == 0 and solved == 0,
                    "elapsed_s": self.method_elapsed_s.get(method, 0.0),
                }
            )
        return rows


def build_core_order_specs() -> list[OrderSpec]:
    return [
        OrderSpec(
            name="core__" + "__".join(perm),
            method_names=perm,
            category="core",
        )
        for perm in itertools.permutations(CORE_METHOD_NAMES)
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_core_order_builder_has_24_orders tests/test_ab_sieve_benchmark.py::test_legacy_baseline_matches_default_pipeline tests/test_ab_sieve_benchmark.py::test_evaluate_pair_short_circuits_on_multi_n -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_ab_sieve_benchmark.py src/rational_distance/proof_status/ab_sieve_benchmark.py
git commit -m "feat: add ab-sieve order specs and evaluator"
```

---

### Task 3: Add the default `24 + 6 + 3 + 1` benchmark plan and parallel runner

**Files:**
- Modify: `src/rational_distance/proof_status/ab_sieve_benchmark.py`
- Test: `tests/test_ab_sieve_benchmark.py`

- [ ] **Step 1: Write the failing tests**

```python
from rational_distance.parallel import ParallelConfig
from rational_distance.proof_status.ab_sieve_benchmark import (
    OrderSpec,
    benchmark_specs,
    build_tail_order_specs,
    build_incremental_specs,
)


def test_tail_and_incremental_plan_sizes() -> None:
    best_core = (
        "safe_sieve",
        "chain_closure_mod_sieve",
        "concordant_search",
        "multi_n_sieve",
    )
    assert len(build_tail_order_specs(best_core)) == 6
    assert len(build_incremental_specs(best_core)) == 3


def test_benchmark_specs_aggregates_results_serially() -> None:
    spec = OrderSpec(name="safe_only", method_names=("safe_sieve",), category="test")
    summaries = benchmark_specs(
        specs=[spec],
        pairs=[(1, 5), (1, 3)],
        parallel=ParallelConfig(workers=1, chunksize=2),
        batch_size=2,
    )
    summary = summaries[0]
    assert summary.n_pairs == 2
    assert summary.final_status_counts["no_solution"] == 1
    assert summary.final_status_counts["hard_case"] == 1
    assert summary.method_attempt_counts["safe_sieve"] == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_tail_and_incremental_plan_sizes tests/test_ab_sieve_benchmark.py::test_benchmark_specs_aggregates_results_serially -v`
Expected: FAIL because `build_tail_order_specs`, `build_incremental_specs`, and `benchmark_specs` do not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
from collections.abc import Iterable
from rational_distance.parallel import ParallelConfig


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
            method_names=best_core + (tail_name,),
            category="incremental",
        )
        for tail_name in TAIL_METHOD_NAMES
    ]


def _make_batches(pairs: list[tuple[int, int]], batch_size: int) -> list[list[tuple[int, int]]]:
    return [pairs[i:i + batch_size] for i in range(0, len(pairs), batch_size)]


def _worker_run_batch(
    packed: tuple[OrderSpec, list[tuple[int, int]]]
) -> list[PairBenchmarkResult]:
    spec, batch = packed
    return [evaluate_pair_in_order(A, B, spec) for A, B in batch]


def benchmark_specs(
    *,
    specs: Iterable[OrderSpec],
    pairs: list[tuple[int, int]],
    parallel: ParallelConfig,
    batch_size: int,
) -> list[OrderBenchmarkSummary]:
    batches = _make_batches(pairs, batch_size)
    summaries: list[OrderBenchmarkSummary] = []
    with parallel.executor() as executor:
        for spec in specs:
            summary = OrderBenchmarkSummary(spec=spec)

            def _handle(batch_results: list[PairBenchmarkResult]) -> None:
                for result in batch_results:
                    summary.add_result(result)

            executor.map(
                _worker_run_batch,
                ((spec, batch) for batch in batches),
                on_result=_handle,
                collect_results=False,
            )
            summaries.append(summary)
    return summaries
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_tail_and_incremental_plan_sizes tests/test_ab_sieve_benchmark.py::test_benchmark_specs_aggregates_results_serially -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_ab_sieve_benchmark.py src/rational_distance/proof_status/ab_sieve_benchmark.py
git commit -m "feat: add ab-sieve parallel benchmark runner"
```

---

### Task 4: Add the benchmark CLI

**Files:**
- Create: `scripts/benchmark_ab_sieve_orders.py`
- Test: `tests/test_ab_sieve_benchmark.py`

- [ ] **Step 1: Write the failing test**

```python
import json
from pathlib import Path

from scripts.benchmark_ab_sieve_orders import main


def test_cli_writes_json_report(tmp_path: Path) -> None:
    out = tmp_path / "ab-sieve-bench.json"
    rc = main(
        [
            "--max-hyp",
            "100",
            "--limit",
            "50",
            "--workers",
            "1",
            "--chunksize",
            "8",
            "--batch-size",
            "10",
            "--json-out",
            str(out),
        ]
    )
    assert rc == 0
    payload = json.loads(out.read_text())
    assert payload["core_order_count"] == 24
    assert payload["extra_order_count"] == 10
    assert payload["best_core_order"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_cli_writes_json_report -v`
Expected: FAIL with `ModuleNotFoundError` for `scripts.benchmark_ab_sieve_orders`.

- [ ] **Step 3: Write minimal implementation**

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.pairs import generate_ab_pairs
from rational_distance.parallel import add_parallel_args, get_parallel_config_from_args
from rational_distance.proof_status.ab_sieve_benchmark import (
    benchmark_specs,
    build_core_order_specs,
    build_incremental_specs,
    build_legacy_baseline_spec,
    build_tail_order_specs,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-hyp", type=int, default=500)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--json-out", type=Path, default=ROOT / "results" / "ab_sieve_benchmark.json")
    parser.add_argument("--full-permutations", action="store_true")
    add_parallel_args(parser)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    pairs = generate_ab_pairs(args.max_hyp)
    if args.limit > 0:
        pairs = pairs[: args.limit]
    cfg = get_parallel_config_from_args(args)

    core_specs = build_core_order_specs()
    core_summaries = benchmark_specs(
        specs=core_specs,
        pairs=pairs,
        parallel=cfg,
        batch_size=args.batch_size,
    )
    best_core = min(core_summaries, key=lambda summary: summary.total_elapsed_s)

    extra_specs = build_tail_order_specs(best_core.spec.method_names)
    extra_specs.extend(build_incremental_specs(best_core.spec.method_names))
    extra_specs.append(build_legacy_baseline_spec())

    extra_summaries = benchmark_specs(
        specs=extra_specs,
        pairs=pairs,
        parallel=cfg,
        batch_size=args.batch_size,
    )

    payload = {
        "max_hyp": args.max_hyp,
        "pair_count": len(pairs),
        "core_order_count": len(core_specs),
        "extra_order_count": len(extra_specs),
        "best_core_order": list(best_core.spec.method_names),
        "core": [
            {
                "name": summary.spec.name,
                "method_names": list(summary.spec.method_names),
                "category": summary.spec.category,
                "n_pairs": summary.n_pairs,
                "total_elapsed_s": summary.total_elapsed_s,
                "final_status_counts": dict(summary.final_status_counts),
                "terminal_method_counts": dict(summary.terminal_method_counts),
                "method_report": summary.method_report(),
            }
            for summary in core_summaries
        ],
        "extra": [
            {
                "name": summary.spec.name,
                "method_names": list(summary.spec.method_names),
                "category": summary.spec.category,
                "n_pairs": summary.n_pairs,
                "total_elapsed_s": summary.total_elapsed_s,
                "final_status_counts": dict(summary.final_status_counts),
                "terminal_method_counts": dict(summary.terminal_method_counts),
                "method_report": summary.method_report(),
            }
            for summary in extra_summaries
        ],
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(f"pairs={len(pairs)} core_orders={len(core_specs)} extra_orders={len(extra_specs)}")
    print(f"best_core={' -> '.join(best_core.spec.method_names)}")
    print(f"json={args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py::test_cli_writes_json_report -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_ab_sieve_benchmark.py scripts/benchmark_ab_sieve_orders.py
git commit -m "feat: add ab-sieve benchmark cli"
```

---

### Task 5: Protect the legacy workflow and default pipeline

**Files:**
- Modify: `tests/test_proof_status.py`
- Test: `tests/test_proof_status.py`

- [ ] **Step 1: Write the failing regression tests**

```python
from rational_distance.proof_status.methods import DEFAULT_METHOD_PIPELINE, run_factor_concordant


def test_default_method_pipeline_names_are_stable() -> None:
    assert tuple(name for name, _ in DEFAULT_METHOD_PIPELINE) == (
        "safe_sieve",
        "chain_closure_mod_sieve",
        "factor_concordant",
        "f2_rank",
        "rank_zero",
        "heegner",
        "chabauty",
        "brauer_manin",
    )


def test_legacy_factor_concordant_still_checks_chain_closure() -> None:
    result = run_factor_concordant(264, 420)
    assert result.method == "factor_concordant"
    assert result.details["concordant_n_count"] == 3
    assert result.details["chain_compatible_count"] == 0
    assert result.outcome == "inconclusive"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_proof_status.py::test_default_method_pipeline_names_are_stable tests/test_proof_status.py::test_legacy_factor_concordant_still_checks_chain_closure -v`
Expected: the first test FAILS if the pipeline order drifted during implementation; the second test FAILS if the old wrapper was accidentally changed.

- [ ] **Step 3: Write minimal implementation**

```python
# No production-code change is desired in this task.
# If either regression test fails, fix the new benchmark code instead of
# changing DEFAULT_METHOD_PIPELINE or run_factor_concordant semantics.
# The target state is:
# 1. methods.py stays the source of truth for the legacy default pipeline.
# 2. The new benchmark code lives beside it and imports from it.
# 3. The legacy factor_concordant wrapper keeps doing exhaustive N search
#    plus chain-closure checking exactly as before.
```

- [ ] **Step 4: Run the full targeted test set**

Run: `uv run pytest tests/test_ab_sieve_benchmark.py tests/test_proof_status.py -q`
Expected: PASS.

Also run: `uv run ruff check src/rational_distance/proof_status/ab_sieve_methods.py src/rational_distance/proof_status/ab_sieve_benchmark.py scripts/benchmark_ab_sieve_orders.py tests/test_ab_sieve_benchmark.py tests/test_proof_status.py`
Expected: PASS.

And run a smoke benchmark:

```bash
uv run python scripts/benchmark_ab_sieve_orders.py \
  --max-hyp 500 \
  --limit 200 \
  --workers 1 \
  --chunksize 16 \
  --batch-size 20 \
  --json-out results/ab_sieve_benchmark_smoke.json
```

Expected: exit code `0`, JSON written, `core_order_count=24`, `extra_order_count=10`.

- [ ] **Step 5: Commit**

```bash
git add tests/test_proof_status.py tests/test_ab_sieve_benchmark.py src/rational_distance/proof_status/ab_sieve_methods.py src/rational_distance/proof_status/ab_sieve_benchmark.py scripts/benchmark_ab_sieve_orders.py
git commit -m "test: protect legacy workflow while adding ab-sieve benchmark"
```

---

## Self-review checklist

- Coverage check:
  - `(A, B)` 路线：Task 1-4
  - 只把 1-4 当主筛子：Task 1-3
  - 拆开第 3/4 层：Task 1
  - 保留后 3 个方法作顺序基准：Task 1, Task 3, Task 4
  - 默认不跑 `7!`：Task 3, Task 4
  - 用公共并行层：Task 3, Task 4
  - 不改坏原默认流水线：Task 5
- Placeholder scan: no `TODO` / `TBD` / “similar to previous task” placeholders remain.
- Type consistency:
  - `PairEvalContext`, `OrderSpec`, `PairBenchmarkResult`, `OrderBenchmarkSummary` are introduced before later tasks use them.
  - Method names are stable across all tasks: `safe_sieve`, `chain_closure_mod_sieve`, `concordant_search`, `multi_n_sieve`, `factor_concordant`, `f2_rank`, `rank_zero`, `heegner`, `chabauty`, `brauer_manin`.

---

Plan complete and saved to `docs/superpowers/plans/2026-05-26-ab-sieve-pipeline-benchmark.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
