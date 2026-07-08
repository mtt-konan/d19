# Rank-Zero Selmer Kernel-Local Schemas

## Question

Do the 9 rank-zero Selmer local-support candidates really represent 9 different
 local shapes, or do they collapse to a smaller kernel-level ledger?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_kernel_local_schemas.py \
  --local-supports results/closure_quotient_rank_zero_selmer_local_supports.json \
  --out results/closure_quotient_rank_zero_selmer_kernel_local_schemas.json \
  --strict
```

## Output

```text
status=ok
package_count=9
support_entry_count=9
family_pattern_count=3
kernel_schema_count=3
shared_kernel_schema_count=3
local_condition_proved_count=0
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：9 个 package 在这一步没有保留成 9 套局部候选形状，而是按 `kernel`
压成了 3 套统一模板：

```text
kernel_minus_p
kernel_neg_2sqrt_q
kernel_pos_2sqrt_q
```

每一套模板都同时覆盖 `AA`、`AA+BB`、`BB` 三个 family pattern，说明当前这层
局部候选依赖的是 `kernel`，不是 `family pattern`。这能把后续 transcript 的局部部分
从“9 份各写一遍”收缩成“3 套模板复用”。

但边界没变：这里仍然只是 symbolic local-support schema，不是 local condition，
更不是 Selmer bound、rank-zero 定理或 `lambda` 整族排除。

## Boundary

This is a kernel-level schema ledger for symbolic local-support candidates. It
does not prove any local condition, Selmer rank bound, rank-zero theorem, or
lambda-family exclusion.
