# wl306 - mixed residual cover priority queue

日期：2026-07-07

## 一句话结论

`AA/BB` residual 的 `27` 个 no-point cover 现在有可复跑的优先级队列。

普通话说：后续不再随机挑 cover 攻，而是先看有 BSD 条件 rank 0、quartic 系数较小的目标。
这只是工作队列，不是证明。

## 新增脚本

```text
scripts/theory/prioritize_mixed_closure_residual_covers.py
tests/test_prioritize_mixed_closure_residual_covers.py
```

排序输入：

```text
results/mixed_closure_aabb_residual_cover_summary.json
results/mixed_closure_aabb_residual_evidence_audit.json
```

排序字段：

```text
has_bsd_conditional_rank0
coefficient_height
term_count
A+B
curve
cover_index
```

其中 `coefficient_height` 是 quartic 方程所有系数绝对值的最大值。

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/prioritize_mixed_closure_residual_covers.py \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --evidence-audit results/mixed_closure_aabb_residual_evidence_audit.json \
  --out results/mixed_closure_aabb_residual_cover_priorities.json
```

输出：

```text
wrote residual cover priorities to results/mixed_closure_aabb_residual_cover_priorities.json
candidate_cover_total=27
top_target={'A': 115, 'B': 297, 'curve': 'AA', 'cover_index': 3}
```

## 前四个目标

```text
1. (115,297) AA cover 3
   quartic = 41*x^4 + 10812*x^3 + 27981*x^2 - 54060*x + 1025
   coefficient_height = 54060
   BSD conditional rank 0 = yes

2. (115,297) AA cover 4
   quartic = -19*x^4 + 1848*x^3 + 182394*x^2 - 1062600*x - 6281875
   coefficient_height = 6281875
   BSD conditional rank 0 = yes

3. (575,4641) AA cover 4
   quartic = 18439*x^4 + 1469614*x^3 + 4100667*x^2 - 7095212*x + 2366396
   coefficient_height = 7095212
   BSD conditional rank 0 = yes

4. (575,4641) AA cover 3
   quartic = 85481*x^4 - 2779536*x^3 + 14087778*x^2 + 63929328*x + 45219449
   coefficient_height = 63929328
   BSD conditional rank 0 = yes
```

## 边界

这个排序不证明 cover 无点。

它只是把下一步严格化从：

```text
27 个候选 cover 里随便挑
```

收敛成：

```text
先攻有 BSD 条件 rank 0 且系数最小的 cover；
首选仍是 (115,297) AA cover 3/4。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_prioritize_mixed_closure_residual_covers.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/prioritize_mixed_closure_residual_covers.py \
  tests/test_prioritize_mixed_closure_residual_covers.py
```

结果：

```text
4 passed
All checks passed!
```
