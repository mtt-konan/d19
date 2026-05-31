from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import cast

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.parallel import ParallelConfig
from rational_distance.proof_status.ab_sieve_benchmark import (
    OrderSpec,
    benchmark_specs,
    build_core_order_specs,
    build_head_validation_specs,
    build_incremental_specs,
    build_legacy_baseline_spec,
    build_safe_top2_specs,
    build_tail_order_specs,
    evaluate_pair_in_order,
)
from rational_distance.proof_status.ab_sieve_methods import (
    PairEvalContext,
    run_concordant_search_ctx,
    run_f2_rank_ctx,
    run_factor_concordant_ctx,
    run_multi_n_sieve_ctx,
)
from scripts.benchmark.benchmark_ab_sieve_orders import main


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


def test_factor_concordant_and_f2_rank_reuse_cached_concordant_n() -> None:
    ctx = PairEvalContext()

    _ = run_factor_concordant_ctx(153, 560, ctx)
    _ = run_f2_rank_ctx(153, 560, ctx)

    assert ctx.factor_search_calls == 1
    assert ctx.concordant_n == [204, 420, 3900]


def test_core_order_builder_has_6_orders() -> None:
    specs = build_core_order_specs()
    assert len(specs) == 6
    assert {len(spec.method_names) for spec in specs} == {3}


def test_safe_first_core_subset_has_2_orders() -> None:
    specs = build_core_order_specs(prefix=("safe_sieve",))
    assert len(specs) == 2
    assert all(spec.method_names[0] == "safe_sieve" for spec in specs)
    assert {len(spec.method_names) for spec in specs} == {3}


def test_head_validation_specs_cover_each_first_method_once() -> None:
    specs = build_head_validation_specs()
    assert len(specs) == 4
    assert {spec.method_names[0] for spec in specs} == {
        "safe_sieve",
        "chain_closure_mod_sieve",
        "concordant_search",
        "multi_n_sieve",
    }
    assert {len(spec.method_names) for spec in specs} == {4}


def test_safe_top2_specs_cover_two_finalists() -> None:
    specs = build_safe_top2_specs()
    assert len(specs) == 2
    assert [spec.method_names for spec in specs] == [
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
    ]


def test_legacy_baseline_matches_default_pipeline() -> None:
    spec = build_legacy_baseline_spec()
    assert spec.name == "legacy_default_pipeline"
    assert spec.method_names == (
        "safe_sieve",
        "chain_closure_mod_sieve",
        "factor_concordant",
        "multi_n_sieve",
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
        "factor_concordant",
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


def test_benchmark_specs_accepts_pair_factory() -> None:
    specs = [
        OrderSpec(name="safe_only", method_names=("safe_sieve",), category="test"),
        OrderSpec(name="safe_only_again", method_names=("safe_sieve",), category="test"),
    ]
    observed = {"calls": 0}

    def make_pairs() -> list[tuple[int, int]]:
        observed["calls"] += 1
        return [(1, 5), (1, 3)]

    summaries = benchmark_specs(
        specs=specs,
        pairs=make_pairs,
        parallel=ParallelConfig(workers=1, chunksize=2),
        batch_size=1,
    )

    assert len(summaries) == 2
    assert observed["calls"] == 2


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
    assert payload["core_order_count"] == 6
    assert payload["extra_order_count"] == 10
    assert payload["best_core_order"]


def test_cli_safe_first_only_skips_extra(tmp_path: Path) -> None:
    out = tmp_path / "ab-sieve-bench-safe-first.json"
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
            "--safe-first-only",
            "--skip-extra",
            "--json-out",
            str(out),
        ]
    )
    assert rc == 0
    payload = cast(dict[str, object], json.loads(out.read_text()))
    assert payload["core_order_count"] == 2
    assert payload["extra_order_count"] == 0
    assert payload["safe_first_only"] is True
    assert payload["skip_extra"] is True
    best_core = cast(list[str], payload["best_core_order"])
    assert best_core[0] == "safe_sieve"


def test_cli_limit_uses_iter_ab_pairs_instead_of_full_generator(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import rational_distance.concordant.pairs as pair_module

    def fail_generate(_max_hyp: int = 500) -> list[tuple[int, int]]:
        raise AssertionError("full pair materialization should not run when --limit is set")

    def fake_iter(_max_hyp: int = 500):
        yield from [(1, 5), (1, 3), (7, 45), (9, 16)]

    monkeypatch.setattr(pair_module, "generate_ab_pairs", fail_generate)
    monkeypatch.setattr(pair_module, "iter_ab_pairs", fake_iter)

    out = tmp_path / "ab-sieve-bench-limit.json"
    rc = main(
        [
            "--max-hyp",
            "100",
            "--limit",
            "3",
            "--workers",
            "1",
            "--chunksize",
            "8",
            "--batch-size",
            "2",
            "--json-out",
            str(out),
        ]
    )

    assert rc == 0
    payload = cast(dict[str, object], json.loads(out.read_text()))
    assert payload["pair_count"] == 3


def test_cli_head_only_runs_four_representatives(tmp_path: Path) -> None:
    out = tmp_path / "ab-sieve-bench-head-only.json"
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
            "--head-only",
            "--json-out",
            str(out),
        ]
    )
    assert rc == 0
    payload = cast(dict[str, object], json.loads(out.read_text()))
    assert payload["core_order_count"] == 4
    assert payload["extra_order_count"] == 0
    assert payload["head_only"] is True
    core_rows = cast(list[dict[str, object]], payload["core"])
    heads = {cast(list[str], row["method_names"])[0] for row in core_rows}
    assert heads == {
        "safe_sieve",
        "chain_closure_mod_sieve",
        "concordant_search",
        "multi_n_sieve",
    }


def test_cli_safe_top2_only_runs_two_orders(tmp_path: Path) -> None:
    out = tmp_path / "ab-sieve-bench-safe-top2.json"
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
            "--safe-top2-only",
            "--json-out",
            str(out),
        ]
    )
    assert rc == 0
    payload = cast(dict[str, object], json.loads(out.read_text()))
    assert payload["core_order_count"] == 2
    assert payload["extra_order_count"] == 0
    assert payload["safe_top2_only"] is True
    core_rows = cast(list[dict[str, object]], payload["core"])
    assert len(core_rows) == 2
    assert all(cast(list[str], row["method_names"])[0] == "safe_sieve" for row in core_rows)
    assert all(
        cast(list[str], row["method_names"])[1] == "chain_closure_mod_sieve"
        for row in core_rows
    )
