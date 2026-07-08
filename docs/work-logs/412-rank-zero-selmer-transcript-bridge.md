# Rank-Zero Selmer Transcript Bridge

## Question

After collapsing 9 package-level local supports to 3 kernel-local schemas, can
the transcript workload also be split into a shared local-template part and a
package-specific part?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_transcript_bridge.py \
  --materialization results/closure_quotient_rank_zero_selmer_package_materialization.json \
  --kernel-local-schemas results/closure_quotient_rank_zero_selmer_kernel_local_schemas.json \
  --transcript-intake results/closure_quotient_rank_zero_selmer_transcript_intake.json \
  --out results/closure_quotient_rank_zero_selmer_transcript_bridge.json \
  --strict
```

## Output

```text
status=ok
package_count=9
kernel_schema_count=3
shared_local_squareclass_template_count=3
package_specific_transcript_count=9
transcript_package_ready_count=0
strict_promotion_ready_count=0
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：这一步把 transcript 任务拆成两层：

```text
共享部分：3 个 kernel-local squareclass 模板
逐包部分：9 个 package 的 statement / isogeny_setup / selmer_bound_argument /
         rank_zero_conclusion / review_notes
```

所以现在不该把 9 个 transcript package 理解成 9 份完全独立的局部工作。局部
`local_squareclass_conditions` 这一栏已经能按 kernel 复用，只剩下其余 5 个字段还是
package 级任务。

边界仍然没变：当前 9 个 package 全部还是 `transcript_package_ready_count=0`，没有
任何 Selmer bound、rank-zero 定理或 `lambda` 整族排除被证明。

## Boundary

This is a transcript-task bridge. It does not prove local conditions, Selmer
rank bounds, rank zero, no-point statements, or lambda-family exclusions.
