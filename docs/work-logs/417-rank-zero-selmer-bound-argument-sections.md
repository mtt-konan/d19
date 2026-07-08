# Rank-Zero Selmer Bound Argument Sections

## Question

For the 9 open rank-zero Selmer bound argument tasks, what proof sections must
each package contain before it can be reviewed as a real Selmer bound argument?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_bound_argument_sections.py \
  --bound-argument-queue results/closure_quotient_rank_zero_selmer_bound_argument_queue.json \
  --odd-prime-local-image-schemas results/closure_quotient_rank_zero_selmer_odd_prime_local_image_schemas.json \
  --tangent-one-reduction-partition results/closure_quotient_rank_zero_selmer_tangent_one_reduction_partition.json \
  --tangent-minus-one-reduction-partition results/closure_quotient_rank_zero_selmer_tangent_minus_one_reduction_partition.json \
  --out results/closure_quotient_rank_zero_selmer_bound_argument_sections.json \
  --strict
```

## Output

```text
status=ok
bound_argument_outline_count=9
open_bound_argument_outline_count=9
required_section_per_outline_count=5
required_section_count=45
shared_odd_prime_local_image_schema_count=4
reduction_partition_outline_count=4
formal_lift_compatibility_proved_count=0
local_image_schema_proved_count=0
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：现在每个 package 的 `selmer_bound_argument` 都被拆成 5 段：

```text
shared_isogeny_setup_reference
odd_prime_local_image_theorems
formal_lift_compatibility
dyadic_local_condition
global_selmer_dimension_bound
```

这一步比“9 个任务 open”更具体：后面不是继续等搜索变长，而是逐段补数学论证。odd-prime
部分已经有 4 个 shared local-image schema 和 4 个 reduction partition outline，但它们还只是
证明入口；formal lift、dyadic local condition 和 global Selmer dimension bound 都仍然 open。

当前仍没有 local image theorem、formal lift compatibility、Selmer rank upper bound、rank-zero
定理或 `lambda` family exclusion。

## Boundary

This is a proof-section outline. It does not prove any section.
