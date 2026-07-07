# Rank-Zero Selmer Odd-Prime Valuations

## Question

Can the 27 open odd-prime local cases be organized by symbolic valuation
shape before attempting local Selmer proofs?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_valuations.py \
  --odd-prime-cases results/closure_quotient_rank_zero_selmer_odd_prime_cases.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_valuations.json \
  --strict
```

## Output

```text
status=ok
package_count=9
odd_prime_valuation_case_count=27
local_condition_proved_count=0
```

## Interpretation

普通话说：这一步不是继续多找 `(A,B)` 例子，而是把每个奇素数分支里
`a2`、`a4`、二次判别式的整除情况写清楚。以后要证明某个局部条件时，
可以直接对着这些小分支做，不用再从原始曲线公式重新拆。

For example, when `ell` is odd and divides `L`, coprime support says `ell`
does not divide `T` or `T^2+4L^2`. The valuation audit records which curve
coefficient remains a unit and which discriminant factor carries the valuation.

## Boundary

This is a valuation-shape audit only. It does not compute local Selmer images,
prove local conditions, prove a Selmer rank bound, or exclude any lambda family.
