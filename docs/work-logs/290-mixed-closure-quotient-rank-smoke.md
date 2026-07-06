# wl290 — mixed closure quotient rank smoke

## 结论

按 `tmp.txt` 建议，先测试“看得见闭合关系”的四条 genus-one 商曲线：

- `AA`: `(N^2 + A^2)((A+B-N)^2 + A^2)`
- `BB`: `(N^2 + B^2)((A+B-N)^2 + B^2)`
- `AB`: `(N^2 + A^2)((A+B-N)^2 + B^2)`
- `BA`: `(N^2 + B^2)((A+B-N)^2 + A^2)`

在 archived `320` 个 hard-case pair 上，PARI `ellfromeqn + ellrank(effort=1)` 全部跑通。

最重要的实测结果：

- `AA/BB` 有大量 certified rank `0`。
- `AB/BA` 在这批样本里没有 certified rank `0`。

所以“闭合商曲线确实给出新信号”成立，但 `tmp.txt` 里猜的 `AB` 头号 rank-0 候选暂时没命中。

## 命令

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320.jsonl
```

输出 summary：

```text
wrote 1280 rows for 320 pairs to results/mixed_closure_rank_hard_cases_320.jsonl
status_counts={'ok': 1280}
rank_counts={'0/0': 216, '0/2': 11, '1/1': 560, '1/3': 5, '2/2': 347, '3/3': 127, '4/4': 14}
```

按曲线拆分：

```text
AA {'0/0': 113, '0/2': 5, '1/1': 162, '2/2': 36, '3/3': 4}
AB {'1/1': 117, '1/3': 2, '2/2': 137, '3/3': 57, '4/4': 7}
BA {'1/1': 117, '1/3': 2, '2/2': 137, '3/3': 57, '4/4': 7}
BB {'0/0': 103, '0/2': 6, '1/1': 164, '1/3': 1, '2/2': 37, '3/3': 9}
```

## 实现

- `src/rational_distance/concordant/mixed_closure_curves.py`
- `scripts/theory/rank_mixed_closure_curves.py`
- `tests/test_mixed_closure_curves.py`
- `tests/test_mixed_closure_rank_cli.py`

## 解释边界

这还不是新的 `proof_status` 判定方法。

原因很简单：rank `0` 的商曲线只说明这条 genus-one 商上的有理点是有限/可枚举的候选；要把它升级成 `no_solution`，还必须把 torsion 点回拉到原始 `N`，确认没有非平凡闭合点。当前脚本只负责第一步筛出值得做回拉认证的 pair。

## 后续更新

### 2026-07-06 更新：rank-0 quartic 点回拉烟测

新增 `--pullback-height` 后，对同一批 `320` 个 archived hard-case pair 跑：

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320_pullback_h100000.jsonl \
  --pullback-height 100000
```

结果：

```text
rank0 rows = 216
point_count distribution = {2: 216}
AA {2: 113}
BB {2: 103}
full_closed_points = 0
non_midpoint_points = 0
non_positive_points = 0
```

普通话解释：

- 所有 `AA/BB` certified rank `0` 商曲线，在高度 `100000` 内都只回拉到两个点。
- 这两个点都是同一个中点 `N = M = (A+B)/2`，只是 `y` 正负不同。
- 没有任何点同时让四个平方条件成立。

边界仍然要说清楚：这还不是完整证明。`hyperellratpoints` 是高度枚举；要把它升级成严格
`no_solution`，下一步仍需要把 `ellfromeqn` 的双有理映射/所有 torsion 点逐点回拉，或给出等价的
手算回拉证明。

## 下一步

1. 把 `AA/BB` rank `0` 的中点-only 现象做成严格 torsion 回拉认证。
2. 对 `0/2`、`1/3` 这些 uncertified rank bounds 换成更直接的 2-descent / Selmer / 模型化处理。
3. 把 `C_lambda` 闭合曲线和 4 条商曲线写成正式引理，作为后续论文/规范入口。

### 2026-07-06 更新：uncertified rank bounds 复核

对全量结果里 `16` 条上下界不闭合的曲线，单独跑了 `ellrank(effort=2)` 和
`ellrank(effort=3)`。

结果：全部不变。

```text
0/2 -> 0/2
1/3 -> 1/3
```

所以这批不确定 rank 不能靠简单提高 PARI effort 解决。后续如果要收紧，应该换成更直接的
2-descent / Selmer / 模型化处理，而不是继续加 effort。
