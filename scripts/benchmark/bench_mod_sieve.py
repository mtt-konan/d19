#!/usr/bin/env python3
"""Benchmark mod sieve per-modulus cost vs kills."""
import sys
import time
sys.path.insert(0, "src")

from rational_distance.concordant.chain_closure_sieve import (
    killed_at_modulus, DEFAULT_PRIME_SQUARE_MODULI
)
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair
from rational_distance.pair_generator import generate_ab_pairs

MAX_HYP = 20000
pairs = [(A,B) for A,B in generate_ab_pairs(MAX_HYP) if allow_reduced_pair(A,B)]
print(f"测试 {len(pairs)} 对\n")
print(f"{'模数':>6} {'素数':>4} {'耗时ms':>8} {'kills':>6} {'μs/kill':>8}")
print("-" * 40)

survivors = set(pairs)
for M in DEFAULT_PRIME_SQUARE_MODULI:
    t0 = time.perf_counter()
    new_survivors = {(A,B) for A,B in survivors if not killed_at_modulus(A,B,M)}
    elapsed_ms = (time.perf_counter() - t0) * 1000
    kills = len(survivors) - len(new_survivors)
    us_per_kill = (elapsed_ms * 1000 / kills) if kills else float('inf')
    p = int(M**0.5)
    print(f"{M:>6} {p:>4}² {elapsed_ms:>8.2f} {kills:>6} {us_per_kill:>8.1f}")
    survivors = new_survivors

print(f"\n剩余 {len(survivors)} 对")
