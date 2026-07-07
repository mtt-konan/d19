# Rank-Zero Selmer Odd-Prime Reduction Shapes

## Question

Can the nine odd-prime lemma obligations be advanced by proving their reduced
cubic shapes modulo `ell`?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.py \
  --odd-prime-lemma-queue results/closure_quotient_rank_zero_selmer_odd_prime_lemma_queue.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_reduction_shapes.json \
  --strict
```

## Output

```text
status=ok
input_lemma_obligation_count=9
reduction_shape_count=9
reduction_shape_proved_count=9
local_condition_proved_count=0
```

## Interpretation

普通话说：这一步开始真正做一点数学，而不是继续排队。对每条
`kernel x odd-prime support` 分支，把曲线右边的三次式
`x*(x^2+a2*x+a4)` 在相应的 `ell` 条件下化简。结果都是两种形状之一：

```text
x*(x-r)^2
x^2*(x-s)
```

也就是说，每个奇素数分支都有明确的双根形状。接下来真正要证明的是：
这种 nodal reduction 形状怎样给出所需的 isogeny-Selmer local squareclass image。

## Boundary

This proves only the displayed reduced cubic factorization shapes. It does not
prove any local Selmer condition, Selmer rank upper bound, or lambda-family
exclusion.
