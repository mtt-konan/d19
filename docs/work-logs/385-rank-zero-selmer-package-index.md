# Rank-Zero Selmer Package Index

## Question

Can the 9 open rank-zero Selmer obligations be exported as reviewable proof
tasks, so the next step is a theorem transcript rather than more search?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/export_closure_quotient_rank_zero_selmer_package_index.py \
  --selmer-obligations results/closure_quotient_rank_zero_selmer_obligations.json \
  --isogeny-templates results/closure_quotient_rank_zero_isogeny_templates.json \
  --out results/closure_quotient_rank_zero_selmer_package_index.json \
  --strict
```

## Output

```text
status=ok
package_count=9
open_package_count=9
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：rank-zero 主线现在有 9 个可交给外部 CAS 或人工审阅的 proof packages。
每个 package 固定一个 family pattern 和一个 2-isogeny kernel，并要求输出：

```text
reviewable transcript proving the uniform isogeny-Selmer rank upper bound
```

这一步的重点是把后续工作变成“证明包输入”，不再是跑更多单点样本。

## Boundary

All 9 packages are `open`. No Selmer rank upper bound is proved here, and no
lambda family is promoted to a proved exclusion.
