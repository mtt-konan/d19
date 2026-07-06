# wl296 - mixed closure residual 2-cover summary

日期：2026-07-06

## 一句话结论

`AA/BB` 的 `12` 条 residual 现在有了一个单独的 cover 汇总器。真实数据确认：

```text
12 条都能把 Selmer gap 和 ell2cover 的 no-point cover 数对上。
```

普通话说：剩余问题已经不是“rank 算不准”这么粗，而是落到了几条显式四次 cover
上。下一步要证明这些 cover 真没点，不能只继续调 rank 参数。

## 新增脚本

```text
scripts/theory/summarize_mixed_closure_residual_covers.py
tests/test_mixed_closure_residual_cover_summary.py
```

脚本输入两类文件：

```text
results/pari_ell2cover_mixed_aabb_h100000.jsonl
results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl
```

输出：

```text
results/mixed_closure_aabb_residual_cover_summary.json
```

它会统计：

- 每条 residual 有多少个 2-cover；
- 有多少个 cover 在给定高度内没找到点；
- no-point cover 的编号；
- `covers_without_points` 是否等于 `selmer_rank_pari - torsion_two_dimension`；
- 当前证据等级。

证据等级被明确写成：

```text
bounded-search-no-point-candidate
```

这避免把 `hyperellratpoints` 的有界搜索误写成严格无点证明。

## 真实运行

命令：

```bash
uv run python scripts/theory/summarize_mixed_closure_residual_covers.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_aabb_residual_cover_summary.json
```

输出：

```text
wrote residual cover summary for 12 rows to results/mixed_closure_aabb_residual_cover_summary.json
status_counts={'ok': 12}
covers_without_points_counts={'2': 10, '3': 1, '4': 1}
selmer_gap_alignment_counts={'match': 12}
evidence_level_counts={'bounded-search-no-point-candidate': 12}
```

逐条结构里，典型行是：

```text
(115,297) AA:
  cover_count = 4
  covers_without_points = 2
  no_point_cover_indices = [3, 4]
  selmer_gap = 2
  selmer_gap_alignment = match
```

## 对当前数学方向的影响

这一步没有新增严格排除证书。

它新增的是更精确的剩余问题描述：

```text
原问题: 12 条 AA/BB rank bounds 不闭合
现在:  12 条 AA/BB 显式 2-cover no-point candidates
```

这比继续盲目跑 `two_descent(second_limit=20+)` 更好，因为它告诉我们应该攻哪些对象：

```text
先攻 (115,297) AA 的 cover 3 和 cover 4。
```

如果能严格证明这两个 cover 无有理点，那么第一条典型 residual 就能从“很可能 rank 0 + Sha[2]”
升级为真正可引用的 rank/Sha 证据。之后再看这类 cover 是否有统一结构。

## 边界

当前不能写：

```text
这些 cover 没有有理点。
```

只能写：

```text
这些 cover 是显式 Sha[2] 候选；在高度 100000 内没找到点，并且 no-point cover 数与 Selmer gap 完全对齐。
```

要进入论文主证明，还缺严格无点证书，例如：

- 局部 obstruction；
- Cassels-Tate / Brauer-Manin 解释；
- 可认证的 rank 或 L 值非零证书；
- Magma/Sage 能导出的可检查 genus-one cover 证书。

## 验证

```bash
uv run pytest tests/test_mixed_closure_residual_cover_summary.py -q
uv run ruff check \
  scripts/theory/summarize_mixed_closure_residual_covers.py \
  tests/test_mixed_closure_residual_cover_summary.py
```

结果：

```text
2 passed
All checks passed!
```
