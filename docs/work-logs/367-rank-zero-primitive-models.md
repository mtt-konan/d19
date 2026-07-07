# Rank-Zero Primitive Models

## Question

For the 200 rank-zero family candidates, what are the primitive AA/BB models
that should be studied for family-level rank-zero proofs?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_rank_zero_primitive_models.py \
  --candidates results/closure_quotient_rank_zero_family_candidates.json \
  --out results/closure_quotient_rank_zero_primitive_models.json \
  --strict
```

## Output

```text
status=ok
candidate_class_count=200
model_count=243
model_counts_by_curve={'AA': 125, 'BB': 118}
family_exclusion_proved_count=0
```

## Interpretation

普通话说：现在 200 个 rank-zero family candidate 不只是一个名单了。每个候选比例类都带上
本原 AA/BB 模型参数：

```text
z^2 = t^4 + p t^2 + q
E: V^2 = X^3 + pX^2 - 4qX - 4pq
```

其中 `p,q,sqrt_q,weierstrass_model` 都写进
`results/closure_quotient_rank_zero_primitive_models.json`。后续如果要证明某个比例类或子族
整族 rank-zero，就应该从这些本原模型出发，而不是继续增加同一 ray 的 scale 样本。

这一步没有证明任何比例类已经整族排除。它只是把 rank-zero 结构证明的输入固定下来。

## Boundary

This is a primitive model index for future family-level proof work. It does not
prove rank zero or no-pointness for a lambda family.
