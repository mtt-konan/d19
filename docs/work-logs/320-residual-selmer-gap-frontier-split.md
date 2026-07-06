# wl320 - residual Selmer gap frontier split

日期：2026-07-07

## 一句话结论

之前的 7 个 `residual-gap-open` 现在被拆成两个更具体的前沿类型。

普通话说：剩下没收敛的 cover 不再只是“还有 7 个不清楚”。现在知道它们分成：

```text
rank0-sha2-gap2 = 20
rank1-sha2-gap2-open = 3
even-rank-sha2-gap4-open = 4
```

## 更新脚本

```text
scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py
tests/test_mixed_closure_residual_selmer_gap_ledger.py
```

ledger 每行新增：

```text
rank_lower_bound
rank_upper_bound
sha2_gap_over_rank_lower_bound
root_number_parity
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py \
  --priorities results/mixed_closure_aabb_residual_cover_priorities.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_residual_selmer_gap_ledger.json
```

输出：

```text
wrote residual Selmer gap ledger to results/mixed_closure_residual_selmer_gap_ledger.json
candidate_cover_total=27
rank0_sha2_gap2_cover_total=20
```

关键 JSON：

```text
gap_type_counts.even-rank-sha2-gap4-open = 4
gap_type_counts.rank0-sha2-gap2 = 20
gap_type_counts.rank1-sha2-gap2-open = 3
rows_with_ok_diagnostics = 27
missing_diagnostic_rows = 0
```

## 解释

`rank1-sha2-gap2-open` 是 `(209,5355) BB` 上的 3 个 cover：

```text
rank_bounds = [1, 3]
root_number_parity = odd
sha2_gap_over_rank_lower_bound = 2
```

`even-rank-sha2-gap4-open` 是 `(1449,12155) BB` 上的 4 个 cover：

```text
rank_bounds = [0, 4]
root_number_parity = even
sha2_gap_over_rank_lower_bound = 4
```

## 边界

这些名字是诊断分类，不是证明。尤其 `root_number_parity` 只是把 Sage diagnostic
中的 root number 翻译成奇偶标签；它不替代严格 rank 证书。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_residual_selmer_gap_ledger.py \
  tests/test_summarize_closure_quotient_partial_result.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py \
  tests/test_mixed_closure_residual_selmer_gap_ledger.py \
  scripts/theory/summarize_closure_quotient_partial_result.py \
  tests/test_summarize_closure_quotient_partial_result.py
```

结果：

```text
7 passed
All checks passed!
```
