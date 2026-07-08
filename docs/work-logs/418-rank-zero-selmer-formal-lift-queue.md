# Rank-Zero Selmer Formal-Lift Queue

## Question

Which formal-lift compatibility theorems are needed to turn the reduction-level
squareclass partitions into usable odd-prime local-image inputs for the 9
rank-zero Selmer bound arguments?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_formal_lift_queue.py \
  --bound-argument-sections results/closure_quotient_rank_zero_selmer_bound_argument_sections.json \
  --tangent-one-reduction-partition results/closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.json \
  --tangent-minus-one-reduction-partition results/closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.json \
  --out results/closure_quotient_rank_zero_selmer_formal_lift_queue.json \
  --strict
```

## Output

```text
status=ok
covered_bound_argument_outline_count=9
formal_lift_task_count=4
open_formal_lift_task_count=4
reduction_partition_exhausted_count=4
formal_lift_compatibility_proved_count=0
local_image_schema_proved_count=0
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：odd-prime 部分现在的下一道硬门槛是 4 个 formal-lift 定理。前面已经把
reduction-level，也就是“模掉奇素数以后”的点分成了有限块；但要用于 Selmer bound，还要证明这些
有限块真的能控制局部域里的点。这就是 formal lift compatibility。

这一步没有证明 formal lift，只是把 4 个必须写的 theorem task 固定下来。它们服务于 9 个
`selmer_bound_argument` outline。

## Boundary

This is a theorem-task queue. It does not prove formal lift compatibility,
local-image schemas, local conditions, Selmer bounds, rank zero, or lambda
family exclusions.
