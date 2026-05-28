from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from math import gcd
from time import perf_counter

from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair

Pair = tuple[int, int]
JsonScalar = str | int | float | bool | None


@dataclass(frozen=True)
class CandidateGeneratorResult:
    name: str
    max_hyp: int
    pair_count: int
    elapsed_s: float
    carries_concordant_n: bool
    min_n_count: int | None
    max_n_count: int | None

    def to_json_dict(self) -> dict[str, JsonScalar]:
        return {
            "name": self.name,
            "max_hyp": self.max_hyp,
            "pair_count": self.pair_count,
            "elapsed_s": self.elapsed_s,
            "carries_concordant_n": self.carries_concordant_n,
            "min_n_count": self.min_n_count,
            "max_n_count": self.max_n_count,
        }


def _validate_max_hyp(max_hyp: int) -> None:
    if max_hyp <= 0:
        raise ValueError("max_hyp must be positive")


def iter_coprime_pairs(max_hyp: int) -> Iterator[Pair]:
    _validate_max_hyp(max_hyp)
    for a in range(1, max_hyp + 1):
        for b in range(a + 1, max_hyp + 1):
            if gcd(a, b) == 1:
                yield (a, b)


def iter_safe_coprime_pairs(max_hyp: int) -> Iterator[Pair]:
    _validate_max_hyp(max_hyp)
    for a in range(1, max_hyp + 1, 2):
        for b in range(a + 2, max_hyp + 1, 4):
            if gcd(a, b) == 1 and allow_reduced_pair(a, b):
                yield (a, b)


def _count_iterator(name: str, max_hyp: int, pairs: Iterator[Pair]) -> CandidateGeneratorResult:
    started = perf_counter()
    count = sum(1 for _ in pairs)
    elapsed = perf_counter() - started
    return CandidateGeneratorResult(
        name=name,
        max_hyp=max_hyp,
        pair_count=count,
        elapsed_s=elapsed,
        carries_concordant_n=False,
        min_n_count=None,
        max_n_count=None,
    )


def _summarize_multi_n(max_hyp: int) -> CandidateGeneratorResult:
    started = perf_counter()
    pairs = fast_multi_concordant_pairs(max_hyp)
    elapsed = perf_counter() - started
    n_counts = [len(ns) for ns in pairs.values()]
    return CandidateGeneratorResult(
        name="multi_n",
        max_hyp=max_hyp,
        pair_count=len(pairs),
        elapsed_s=elapsed,
        carries_concordant_n=True,
        min_n_count=min(n_counts) if n_counts else None,
        max_n_count=max(n_counts) if n_counts else None,
    )


def run_generator_benchmark(max_hyp: int) -> tuple[CandidateGeneratorResult, ...]:
    _validate_max_hyp(max_hyp)
    return (
        _count_iterator("all_coprime", max_hyp, iter_coprime_pairs(max_hyp)),
        _count_iterator("safe_coprime", max_hyp, iter_safe_coprime_pairs(max_hyp)),
        _summarize_multi_n(max_hyp),
    )


def run_named_generator_benchmark(name: str, max_hyp: int) -> CandidateGeneratorResult:
    _validate_max_hyp(max_hyp)
    if name == "all_coprime":
        return _count_iterator("all_coprime", max_hyp, iter_coprime_pairs(max_hyp))
    if name == "safe_coprime":
        return _count_iterator("safe_coprime", max_hyp, iter_safe_coprime_pairs(max_hyp))
    if name == "multi_n":
        return _summarize_multi_n(max_hyp)
    raise ValueError(f"unknown generator: {name}")


__all__ = [
    "CandidateGeneratorResult",
    "iter_coprime_pairs",
    "iter_safe_coprime_pairs",
    "run_generator_benchmark",
    "run_named_generator_benchmark",
]
