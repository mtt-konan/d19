# Rank-Zero Selmer Isogeny-Setup Templates

## Question

Among the 9 open rank-zero Selmer transcript packages, does the `isogeny_setup`
part still need to be written 9 times, or does it collapse to shared kernel
templates?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_isogeny_setup_templates.py \
  --materialization results/closure_quotient_rank_zero_selmer_package_materialization.json \
  --kernel-local-schemas results/closure_quotient_rank_zero_selmer_kernel_local_schemas.json \
  --out results/closure_quotient_rank_zero_selmer_isogeny_setup_templates.json \
  --strict
```

## Output

```text
status=ok
package_count=9
kernel_schema_count=3
setup_template_count=3
shared_isogeny_setup_template_count=3
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：这一步说明 `isogeny_setup` 也不该理解成 9 份互相独立的任务。同一个
`kernel` 下，9 个 package 的 `symbolic_model` 完全一致，所以它也能压成 3 套共享模板：

```text
kernel_minus_p
kernel_neg_2sqrt_q
kernel_pos_2sqrt_q
```

这样一来，当前 transcript 工作里至少有两块已经结构化收缩了：

```text
local_squareclass_conditions -> 3 个共享 kernel 模板
isogeny_setup               -> 3 个共享 kernel 模板
```

这仍然不是 Selmer bound，更不是 rank-zero 定理。它只是把后续 transcript 撰写从“9 份平铺”
继续收缩成“kernel 模板复用 + 剩余字段补齐”。

## Boundary

This is a template-sharing audit for transcript isogeny setup. It does not
prove local conditions, Selmer rank bounds, rank zero, or lambda-family
exclusions.
