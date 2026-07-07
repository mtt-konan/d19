# Rank-Zero Selmer Package Materialization

## Question

Can the 9 open rank-zero Selmer packages be materialized as per-package JSON and
Markdown review files, so future work can close one package at a time?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/materialize_closure_quotient_rank_zero_selmer_packages.py \
  --package-index results/closure_quotient_rank_zero_selmer_package_index.json \
  --packages-dir results/closure_quotient_rank_zero_selmer_packages \
  --out results/closure_quotient_rank_zero_selmer_package_materialization.json \
  --strict
```

## Output

```text
status=ok
package_count=9
open_package_count=9
materialized_json_count=9
materialized_markdown_count=9
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：这一步把一个总表拆成 9 份具体任务。每份任务都有机器可读的 JSON 和人可读的
Markdown，写明 family pattern、kernel、目标曲线模板，以及后续必须补上的 transcript
字段。

这对主线的意义是：后续进展应该表现为某个 package 的 transcript 被补齐并通过审阅，而不是
继续增加单个 `(A,B)` 搜索命中。

## Boundary

All 9 packages remain `open`. The materialized files do not prove any Selmer
rank upper bound, rank-zero statement, or lambda-family exclusion.
