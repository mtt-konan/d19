from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from rational_distance.concordant.factor_search import find_concordant_by_factorization
from rational_distance.proof_status.methods import (
    run_brauer_manin_stub,
    run_chabauty_stub,
    run_chain_closure_mod_sieve,
    run_f2_rank,
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
    details: dict[str, object] = {
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
    details: dict[str, object] = {
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
    return run_f2_rank(A, B, concordant_n=_get_concordant_n(A, B, ctx))


def run_rank_zero_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_rank_zero(A, B)


def run_heegner_ctx(A: int, B: int, _ctx: PairEvalContext) -> MethodResult:
    return run_heegner_height(A, B)


def run_factor_concordant_ctx(A: int, B: int, ctx: PairEvalContext) -> MethodResult:
    return run_factor_concordant(A, B, concordant_n=_get_concordant_n(A, B, ctx))


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
