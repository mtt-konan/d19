# Next-Step Hard-Layer Follow-Up

Date: 2026-06-07

Scope: follow-up to the theory-framework audit and counterexample-first pass. This run focused on the first concrete next step: the `D_g=1` hard layer, the gap-1 near-miss models, and upgrading old partner-graph evidence from sum-only to full-plane GEN-CLOSURE.

## Executive Summary

本轮把“下一步”推进成了四个可复现结论。

第一，`D_g=1` 不是一个模糊标签。在当前正整数搜索域里，它就是：

```text
12 | gcd(A,B)
```

这层是剩余硬核。到 `max_hyp=1,000,000` 时，exact GEN-CLOSURE 残余里有 `256,774 / 332,373 = 77.25%` 落在这一层。

第二，两个最清楚的 gap-1 样本都说明：平方条件本身已经全过，真正卡住的是最后那条线性闭合条件。普通话说，就是“每条斜边都能是整数，但最后拼回平面时差 1 格”。

第三，旧 partner graph 的最大空缺已经补上：全 `G_M @ max_value=1M` 的 `338,225` 个顶点已经用 full-plane delta 扫过。结果是：

| Item | Value |
|---|---:|
| vertices scanned | `338,225` |
| full-plane relation rows | `5,071,562` |
| full-plane closure hits | `0` |
| global min delta | `1` |
| vertices with delta `1` | `31` |

这不是全局 Harborth 证明，但它把旧的 `G_M` sum-only “0 hit” 升级成了同一个 `max_value=1M` 窗口下的 full-plane “0 hit”。

第四，用户指出的“先闭合、三条边过、第四条失败”方向已经复活成可复跑脚本，并且做了速度优化。`A,B<=2000`、difference tail `<=5000` 从约 `19s` 降到约 `0.035s`；`A,B<=100000`、difference tail `<=250000` 也能在十几秒级跑完。本轮大边界找到 `41,736` 个精确 `3/4` near-miss、`0` 个 `4/4` hit，并出现第四边 nearest-square delta `1` 的样本。Delta `1..10` 里只出现 `1,6,7,8,9,10`，没有 `2..5`；低 delta 主要来自外部 full-plane 关系。

## Produced Artifacts

Documents:

- `hard-layer.md`: why `D_g=1` means `12 | gcd(A,B)` and why it dominates the residual.
- `delta-1-models.md`: factorization and exact square checks for the two gap-1 models.
- `partner-full-plane-scan.md`: new exhaustive `G_M @ 1M` full-plane scan result.
- `closure-first-3of4.md`: closure-first full-plane search for exact `3/4` square near-misses.
- `theorem-targets.md`: the next proof targets that survived this follow-up.
- `center-line-impossibility.md`: local d19 translation of Yang Ji's midline theorem.
- `commands-run.md`: commands and verification.
- `../../work-logs/106-d4-point-plot-and-centerline-branch.md`: D4 point plot and center-line theorem note.
- `../../work-logs/204-d4-invariant-coordinate-summary.md`: D4 invariant table follow-up for the 480 point orbits.
- `../../work-logs/205-closure-first-near-miss-equationization.md`: equation ledger for three low-delta / high-repeat near-miss templates.

Code/results:

- `src/rational_distance/results/gm_closure_delta.py`: adds full-plane delta summary helper while preserving the old sum-only helper.
- `scripts/partner/full_gm_full_plane_delta_stats.py`: exhaustive full-plane partner graph delta scanner.
- `scripts/theory/closure_first_three_square_search.py`: closure-first full-plane `3/4` square near-miss probe.
- `scripts/theory/plot_closure_first_d4_points.py`: plot D4-distinct coordinate representatives from the closure-first run.
- `scripts/theory/summarize_closure_first_d4_invariants.py`: summarize `x(1-x)`, `y(1-y)` and closure-scale invariants for D4 point records.
- `scripts/theory/equationize_closure_first_near_miss.py`: write square-equation ledgers for selected `3/4` near-miss samples.
- `results/partner/full_gm_full_plane_delta_summary.json`
- `results/partner/full_gm_full_plane_delta_top.jsonl`
- `results/partner/full_gm_full_plane_closure_hits.jsonl`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max100_tail300.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max500_tail1500.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max2000_tail5000.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max10000_tail25000_fast.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max50000_tail125000_fast.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json`
- `results/counterexample_first/2026-06-07/closure_first_3of4_d4_points_max100000_tail250000.png`

## Plain-Language Direction

The next mathematical move should not be “scan wider” first. It should be:

```text
Explain why the hard layer can get arbitrarily close, but still misses exact closure.
```

The most promising target is the `12 | gcd(A,B)` layer, especially gap-1 rows and closure-first `3/4` templates. If we can prove the final linear closure or fourth square is forced into a nonzero residue class, this becomes a real obstruction. If we fail, the same structure may become a better counterexample generator.
