# Rank-Zero Selmer Odd-Prime Lemma Queue

## Question

Can the 27 odd-prime valuation cases be collapsed into uniform lemma
obligations rather than treated as 27 separate proof tasks?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.py \
  --odd-prime-valuations results/closure_quotient_rank_zero_selmer_odd_prime_valuations.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.json \
  --strict
```

## Output

```text
status=ok
input_valuation_case_count=27
lemma_obligation_count=9
local_lemma_proved_count=0
```

## Interpretation

普通话说：这一步把 27 个奇素数小分支压成 9 个统一证明任务。原因是
不同 `AA/BB/AA-BB` package 里，只要 `kernel` 和 `ell` 整除的位置相同，
valuation 形状就是同一类。以后证明时应优先写 9 条统一 lemma，而不是给 27
个分支各写一遍。

## Boundary

This is a lemma queue, not a proof. No local lemma, local condition, Selmer rank
bound, or lambda-family exclusion is proved here.
