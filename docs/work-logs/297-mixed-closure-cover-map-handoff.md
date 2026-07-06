# wl297 - mixed closure no-point cover map handoff

日期：2026-07-06

## 一句话结论

`AA/BB` residual 的 no-point cover 现在不只保留点数，还保留了具体四次方程；重跑
`ell2cover` 后也会保留 PARI 给出的 covering map。

普通话说：后面要严格化时，不需要再从“第几个 cover”猜对象。对象已经能完整导出来。

## 1. 工具边界

查 PARI `ell2cover` 帮助后，关键句是：

```text
ell2cover(E) returns a basis of the set of everywhere locally soluble 2-covers.
```

所以这些 cover 不应该被说成“等待普通局部 obstruction 排除”。它们按 `ell2cover` 的定义已经是局部处处可解。

当前正确口径是：

```text
explicit Sha[2] candidate / everywhere-locally-soluble 2-cover with no point found
by bounded search.
```

这仍然不是严格无点证明。

## 2. 代码更新

更新：

```text
scripts/theory/pari_ell2cover_mixed_residuals.py
scripts/theory/summarize_mixed_closure_residual_covers.py
tests/test_pari_ell2cover_mixed_residuals.py
tests/test_mixed_closure_residual_cover_summary.py
```

变化：

- `pari_ell2cover_mixed_residuals.py` 对每个 cover 增加
  `covering_map_to_elliptic`；
- `summarize_mixed_closure_residual_covers.py` 的 `no_point_cover_rows` 现在保留
  no-point cover 的 `quartic`；
- 如果输入 cover 行带 `covering_map_to_elliptic`，summary 也会把它带入 no-point cover
  目标清单；
- summary 的 boundary 明确写出：PARI `ell2cover` 返回局部处处可解 cover。

## 3. 真实重跑

全量 `AA/BB` residual 重跑：

```bash
uv run python scripts/theory/pari_ell2cover_mixed_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --curve AA \
  --curve BB \
  --height 100000 \
  --effort 1
```

结果仍是：

```text
status_counts={'ok': 12}
covers_without_points_counts={'2': 10, '3': 1, '4': 1}
```

再生成 summary：

```bash
uv run python scripts/theory/summarize_mixed_closure_residual_covers.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_aabb_residual_cover_summary.json
```

结果：

```text
status_counts={'ok': 12}
covers_without_points_counts={'2': 10, '3': 1, '4': 1}
selmer_gap_alignment_counts={'match': 12}
evidence_level_counts={'bounded-search-no-point-candidate': 12}
```

## 4. 最小目标对象

当前建议先攻：

```text
(A,B,curve) = (115,297,AA)
no_point_cover_indices = [3,4]
selmer_gap = 2
```

两个 no-point cover 的方程是：

```text
cover 3:
y^2 = 41*x^4 + 10812*x^3 + 27981*x^2 - 54060*x + 1025

cover 4:
y^2 = -19*x^4 + 1848*x^3 + 182394*x^2 - 1062600*x - 6281875
```

单条带 map 的复现命令：

```bash
uv run python scripts/theory/pari_ell2cover_mixed_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_ell2cover_mixed_115_297_AA_h100000_with_maps.jsonl \
  --target 115,297,AA \
  --height 100000 \
  --effort 1
```

再生成目标 summary：

```bash
uv run python scripts/theory/summarize_mixed_closure_residual_covers.py \
  --covers results/pari_ell2cover_mixed_115_297_AA_h100000_with_maps.jsonl \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --out results/mixed_closure_115_297_AA_cover_targets_with_maps.json
```

## 5. 下一步判断

因为 cover 已经是局部处处可解，下一步不应继续押“找一个坏素数排除”。

更合理的严格化路线：

- 用 Magma 或更专门的 genus-one tooling 做 Mordell-Weil sieve；
- 研究这两个 cover 在 Cassels-Tate pairing 里的角色；
- 找可引用的严格 rank / L 值非零证书，把 `(115,297) AA` 从 probable rank `0`
  升级成可写入证明的 rank `0`；
- 若一个样本跑通，再看 10 条典型 `[4,2,0,0]` pattern 是否共用结构。

## 6. 验证

```bash
uv run pytest \
  tests/test_pari_ell2cover_mixed_residuals.py \
  tests/test_mixed_closure_residual_cover_summary.py \
  -q

uv run ruff check \
  scripts/theory/pari_ell2cover_mixed_residuals.py \
  scripts/theory/summarize_mixed_closure_residual_covers.py \
  tests/test_pari_ell2cover_mixed_residuals.py \
  tests/test_mixed_closure_residual_cover_summary.py
```

结果：

```text
4 passed
All checks passed!
```
