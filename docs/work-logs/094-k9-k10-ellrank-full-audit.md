# wl094 — K_9 / K_10 全量 ellrank 审计：rank ≤ 4 假设在 k=9,10 仍严格成立

## 触发

用户在 review G_M (partner graph) BFS 方向后选定先做 OPEN_DIRECTIONS **E.2**：

> 测 wl060 "rank ≤ 4 在 catalog" 假设是否在 K_9/K_10 hub 上仍 hold。

wl060 只在 catalog 内的 K_6–K_8 hub（共 11 个）上实测 rank ≤ 4。wl062/wl063
随后在 comp 0 的非互素 partner-only 顶点里发现了 catalog 完全看不到的 **42 个
K_9 + 6 个 K_10** 实例。这批高阶 hub 此前从未跑过 ellrank（wl063 只做了
closure 检查）。本次把它们全部跑完。

> 一次性早期 sample（10 个 K_9 + 6 个 K_10，见 `k10_ellrank_wl063.jsonl`）已确认
> rank ≤ 4，但 K_9 只覆盖 42 个里的 10 个。本 worklog 补齐剩余 32 个，做**全量**审计。

## 工具

`scripts/partner/k10_extract_and_ellrank.py`（沿用，做两处改动）：

1. 修正 wl061 数据路径：`results/partner_full_bfs_components.jsonl` →
   `results/partner/partner_full_bfs_components.jsonl`（数据已归入 `results/partner/`）。
2. 加 `--k9-limit` 参数，默认 `0 = 全部 42 个`（之前硬编码 `sorted(k9)[:10]`）。
   输出改写到 `results/partner/k9k10_ellrank_full.jsonl`。

流程：

```text
1. 读 wl061 components（338,225 个 G_M 顶点）
2. parallel_map(find_concordant_by_factorization) 算每个顶点 k_real，筛 k >= 9
3. 对全部 48 个高阶 hub 跑 compute_rank（PARI ellrank, effort=1）
```

运行：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/k10_extract_and_ellrank.py
```

扫描 338K 顶点 ~98s（2 核），ellrank 部分每个 hub < 0.1s。

## 数据：48 个高阶 hub 全部 ellrank（k_real = 9, 10）

```text
class  pair                k    rank   deficit  sha2[2]_lo  #gens
──────────────────────────────────────────────────────────────────
K_10  ( 76440, 831600)     10   4      6         0          4
K_10  (184800, 308880)     10   3      7         0          3
K_10  (224400, 816816)     10   3      7         0          3
K_10  (301665, 960960)     10   3      7         0          3
K_10  (369600, 617760)     10   3      7         0          3
K_10  (554400, 926640)     10   3      7         0          3
K_9   (39 个 rank=3) + (5 个 rank=4)   deficit 5–6  sha2[2]=0
        rank=4 的 5 个: (50960,554400) (65520,712800) (91728,997920)
                        (263120,687960) (294525,782496)
```

完整 48 行见 `results/partner/k9k10_ellrank_full.jsonl`。

聚合：

```text
class   n    rank 分布          rank max   deficit (min/max/avg)   rank>4
────────────────────────────────────────────────────────────────────────
K_10    6    {3: 5, 4: 1}       4          6 / 7 / 6.83            0 / 6
K_9    42    {3: 37, 4: 5}      4          5 / 6 / 5.88            0 / 42

全部 48: certified (lower == upper) = 48/48,  sha2[2]_lower = 0 (48/48),
         #gens == rank (48/48),  rank > 4 = 0/48
```

## 主结论 1：rank ≤ 4 假设在 k=9,10 严格成立（0 反例）

**48 个 hub 没有一个 rank > 4。** rank 只取 {3, 4} 两个值，且 K_10 里 5/6 是
rank 3。所有 ellrank 在 effort=1 即 certified（`lower == upper`），不依赖更高
effort。

把 wl060 的实测面从 K_6–K_8（11 个，全在 catalog 互素行）扩到 K_9–K_10
（48 个，全是 catalog 看不到的非互素 partner-only 顶点）：

```text
              k     hub 数   rank 范围   来源
─────────────────────────────────────────────────
wl060        6–8      11      3–4        catalog 互素行
wl094        9–10     48      3–4        comp 0 非互素 partner-only
─────────────────────────────────────────────────
合计         6–10     59      3–4        rank ≤ 4 无一例外
```

这是迄今对 "concordant multi-N hub 的 E_{A,B} rank ≤ 4" 最强的经验证据：跨越
k=6 到 k=10、跨越互素与非互素两层，rank 上限纹丝不动。

## 主结论 2：deficit 随 k 单调上升，sha2[2] 恒为 0

```text
        k     avg deficit (= k - rank)
        6      2.6   (wl060)
        7      3.5   (wl060)
        8      4.5   (wl060)
        9      5.88  (wl094)
       10      6.83  (wl094)
```

deficit = k − rank 几乎随 k 线性增长（斜率 ≈ 1，因为 rank 被钉在 3–4）。
这跟 wl059 deficit 猜想、wl086 "Q_N 坐标矩阵秩亏" 的图像一致：k 越大，N 列表
给出的 concordant 点越多，但它们都落在一个 rank ≤ 4 的 Mordell-Weil 自由部分
里，多出来的全是线性关系（deficit）。

`sha2[2]_lower = 0` 在 48/48 上成立，与 wl060 一致——这些 hub 的 2-Selmer 下界
没有给出额外 Sha 障碍。

## 对 closure / 反例搜索的意义

rank ≤ 4 是个**正面结构事实**，本身不直接给 closure 障碍（wl086 已说明
concordant 点的 2-可除性对闭合/不闭合无差别）。但它有两个用处：

1. **height-bound / Heegner 判定器（A.3/F.x）的前提收紧**：rank 被严格压在 ≤ 4，
   意味着这些 hub 上的有理点结构受控，后续把 Heegner 过滤器升级成判定器时
   搜索空间有明确上界。
2. 排除了 "高 k hub 会涌现高 rank（从而可能藏 closure）" 这一猜测：k 升到 10
   时 rank 不升反而 deficit 暴涨，说明 partner web 的高阶结构是**线性冗余**而非
   独立秩的堆叠。

## 没做的事 / 钩子

1. **K_11 / K_12 / K_13 ellrank**：wl085 的 D-scaling 生成器已造出这些更高阶
   hub（max_value=1M BFS 之外）。它们的 rank 是否仍 ≤ 4？是 E.2 的自然延伸。
2. **E.1（max_value=10M/100M BFS）**：用户已说明 BFS 算法需先优化才能跑更大
   范围，留待后续。
3. rank=4 的 6 个 hub（1 个 K_10 + 5 个 K_9）是否有共同的代数特征（如某个固定
   的 2-descent 像）？可对照 wl086 的坐标矩阵分析。

## 文件

```text
scripts/partner/k10_extract_and_ellrank.py            改: 路径修正 + --k9-limit (默认全跑)
results/partner/k9k10_ellrank_full.jsonl              48 个 hub 全量结果
results/partner/k9k10_ellrank_full_run.log            运行日志
docs/work-logs/094-k9-k10-ellrank-full-audit.md       本文件
docs/OPEN_DIRECTIONS.md                               E.2 标记完成
```
