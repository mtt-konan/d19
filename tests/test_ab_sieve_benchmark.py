from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.parallel import ParallelConfig
from rational_distance.proof_status.ab_sieve_benchmark import (
    OrderSpec,
    benchmark_specs,
    build_core_order_specs,
    build_incremental_specs,
    build_legacy_baseline_spec,
    build_tail_order_specs,
    evaluate_pair_in_order,
)
from rational_distance.proof_status.ab_sieve_methods import (
    PairEvalContext,
    run_concordant_search_ctx,
    run_multi_n_sieve_ctx,
)
from scripts.benchmark_ab_sieve_orders import main


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
    payload = cast(dict[str, object], json.loads(out.read_text()))
    assert payload["core_order_count"] == 24
    assert payload["extra_order_count"] == 10
    assert payload["best_core_order"]
