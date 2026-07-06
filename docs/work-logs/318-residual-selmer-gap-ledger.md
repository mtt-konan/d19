# wl318 - residual Selmer gap ledger

日期：2026-07-07

## 一句话结论

剩余 residual cover 的 Selmer/Sha[2] 缺口现在有了独立 ledger。

普通话说：我们现在不只是知道“还有 27 个候选 cover 没严格关掉”，还知道它们主要卡在哪里。
真实结果是：27 个候选 cover 都有 Sage diagnostic，其中 20 个是 `rank0-sha2-gap2`。
后续 wl320 又把剩下 7 个细分成 3 个 `rank1-sha2-gap2-open` 和 4 个
`even-rank-sha2-gap4-open`。

## 更新脚本

```text
scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py
tests/test_mixed_closure_residual_selmer_gap_ledger.py
scripts/theory/summarize_closure_quotient_partial_result.py
tests/test_summarize_closure_quotient_partial_result.py
scripts/theory/audit_closure_quotient_partial_artifacts.py
tests/test_closure_quotient_partial_artifacts.py
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

## 当前 ledger 数字

```text
candidate_cover_total = 27
diagnostic_status_counts.ok = 27
missing_diagnostic_rows = 0
rank0_sha2_gap2_cover_total = 20
gap_type_counts.rank0-sha2-gap2 = 20
gap_type_counts.rank1-sha2-gap2-open = 3
gap_type_counts.even-rank-sha2-gap4-open = 4
all_rows_candidate_not_proof = true
```

这表示大多数剩余 cover 的主要缺口不是局部可解性，而是 Selmer rank 与已知 rank/torsion
之间留下的 2 维 Sha[2] 型缺口。

## 接入 partial summary

`summarize_closure_quotient_partial_result.py` 新增输入：

```text
--selmer-gap-ledger results/mixed_closure_residual_selmer_gap_ledger.json
```

summary 现在输出：

```text
residual_selmer_gap_status.candidate_cover_total = 27
residual_selmer_gap_status.rows_with_ok_diagnostics = 27
residual_selmer_gap_status.missing_diagnostic_rows = 0
residual_selmer_gap_status.rank0_sha2_gap2_cover_total = 20
```

## 边界

这个 ledger 是路线图，不是证明。它把剩余问题分类，方便下一步集中攻
Cassels-Tate pairing、Mordell-Weil sieve、或可引用的严格 rank/L-value 证书。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_residual_selmer_gap_ledger.py \
  tests/test_summarize_closure_quotient_partial_result.py \
  tests/test_closure_quotient_partial_artifacts.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/summarize_mixed_closure_residual_selmer_gaps.py \
  tests/test_mixed_closure_residual_selmer_gap_ledger.py \
  scripts/theory/summarize_closure_quotient_partial_result.py \
  tests/test_summarize_closure_quotient_partial_result.py \
  scripts/theory/audit_closure_quotient_partial_artifacts.py \
  tests/test_closure_quotient_partial_artifacts.py
```

结果：

```text
7 passed
All checks passed!
```
