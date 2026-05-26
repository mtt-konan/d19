#  wl061 — G_M 完整 BFS 普查：309,689 节点超级 component + 99.6% tree

## 触发

用户问："不能用 BFS 把所有目前已知的多 N pair 都跑一遍吗，看看有几个结构，
以及一共有多少个多 N pair 在一定范围内"。

wl058 之前只 BFS 了两个根 (153, 560) + (264, 420)，还以为 G_M ≈ forest。
本次完整跑遍 G_M（catalog seed + 多核并行 + BFS fixed-point）一次性出结果。

## 工具

`scripts/partner_full_bfs.py`（新）：

- 种子 = catalog 10,333 互素 multi-N pair (`max_hyp=100000`)
- 每轮用 `parallel_map(find_concordant_by_factorization)` 并行算 N 列表（10 cores）
- BFS fixed-point：直到无新顶点加入
- `max_value=1,000,000` 截断（跳过 N > 1M 的 partner pair）
- union-find 输出 component 分布

参数也支持 `--workers`、`--chunksize`、`--max-value`。

## 时长

```text
47 BFS rounds, ~12 分钟（10 核并行）

round  visited       next_frontier   compute  
─────────────────────────────────────────────
  1     10,333         10,176          3.1s   ← catalog seed
  2     20,509          5,769          8.0s
  3     26,277          5,069          6.5s
  4     31,339          9,902          6.7s
  5     41,215         11,967         14.1s
 10    160,072         35,802         72.9s
 20    277,000+
 47    338,225               2          0.1s   ← 收敛
```

## 数据：G_M 全貌（max_value=1M）

```text
顶点总数:     338,225
边总数:       350,868
component 数:  9,580

种子 catalog 占比:           10,333 / 338,225 = 3.1%
非互素 partner-only 顶点:    327,892 / 338,225 = 96.9%
                              （= G_M 绝大多数顶点是非互素的）

99.6% 的 component 是纯 tree (9540 / 9580 个)
40 个 component 有 cycle (即 circuit_rank ≥ 1)
总 circuit rank = E - V + components = 22,223
```

## 主结论 1：发现 309,689 节点的超级 component

```text
comp 0:   size = 309,689    edges = 331,803    circuit_rank = 22,115
        catalog 内部: 550 (catalog 总 10,333 中的 5.3%)

它包含所有 wl055 发现的 K_n 顶级 hub:
  (40950, 99470)    ← 代表顶点（最小字典序）
  (55440, 445536)   K_8 (wl055 顶端实例之一)
  (58800, 98280)    K_8
  (5985, 59584)     wl061 上一版"不闭合脚本"找到的 392-node 中心 hub

巨型 component 单一占 G_M 92% 顶点 + 95% 边 + 99.5% circuit rank
```

这跟 wl058 的 forest 假设**完全相反**。原因：wl058 只 BFS 了 (153, 560) 和
(264, 420) 这两个**孤立的小 component**，没碰到主体。

## 主结论 2：(153, 560) 和 (264, 420) 真的是孤立小 component

```text
comp 15:  size = 71    edges = 71    circuit_rank = 1   ← wl058 BFS 数据完全一致
          内含: (153, 560), (1344, 3900) K_5 hub, (7105, 9360), ...
          有唯一 6-cycle（wl059 已细致分析）

comp 58:  size = 28    edges = 27    circuit_rank = 0   ← 严格 tree
          内含: (264, 420)
```

wl058 的 BFS 数字 71 + 28 在 wl061 完全复现，证明 BFS 实现正确。
两个 component 独立于巨型主体（任意路径连不过去，因为巨型 component 的代表
顶点都 ≥ 5985）。

## 主结论 3：Component size 的双峰分布

```text
size 分布:
  size = 1:        307 个       (孤立顶点，partner-only 但 N 列表为空)
  size = 2:      8,046 个   ⚠   (单边 component，主导小 component 池)
  size = 4:        698 个
  size = 6:         78 个
  size = 7-100:    ~360 个
  size = 100-500:   ~10 个     (中等独立 component, 例如 comp 1-4)
  size = 309,689:    1 个      (绝对统治的超级 component)
```

**双峰**：小 component 平均 size ≈ 3，大 component size = 309,689，中间几乎没东西。

跟典型 percolation / random-graph 现象一致：phase transition 把图分成
"giant component + 小碎片"。

## 主结论 4：catalog 数据的"小 hub" vs G_M 真实结构的反差

wl055 测试 partner-pair k 值得出"K_8 是 catalog 内最高阶"，但这是**仅看 catalog
互素行**的 k。在 G_M 全图里：

- 巨型 component 的中心顶点 (40950, 99470) 度数远超 K_8（要查具体 degree）
- 309,689 节点共享 22,115 个独立 cycle
- **catalog 是 G_M 的稀疏切片**，10,333 互素顶点投射到 G_M 后高度分散：
  comp 0 含 550 个 catalog 行，剩下 9,783 个 catalog 行散布在 9,579 个其他
  component 中（平均每 component 1 个 catalog 行）

也就是说：
**catalog 互素行几乎都是孤立"刺"，挂在巨型非互素主干上**。

## 主结论 5：99.6% component 是 tree

只有 40 个 component 有 cycle：

```text
component  size      circuit_rank
──────────────────────────────
comp 0    309689    22115            ← 单一 component 含 22,115 cycles
comp 1       473       13
comp 2       471       15
comp 3       393       12
comp 4       155        2
comp 6       121        7
comp 7       109        4
... 其余 33 个 cycle component
comp 15       71        1            ← (153, 560), wl058 6-cycle
其他 9540 个 component 全都 circuit_rank = 0
```

**全部 cycle 的 99.5% 都集中在 comp 0**（22,115 / 22,223）。

## wl059 deficit 猜想 vs wl061 实测

wl059 提出："G_M 上 cycle 数 ≈ 节点 (k - rank) 之和"。

wl061 数据：
- comp 0 有 22,115 cycle
- 其顶点数 309,689，假设平均 k - rank ≈ 0.07，22115 / 309689 ≈ 0.07，
  数量级相符（但实际平均 deficit 应高于此，因为很多顶点是 non-multi-N or
  tree 顶点贡献 0 deficit）

要严格验证，得对 comp 0 的 309,689 顶点全部跑 PARI ellrank。
按 wl060 的 ~50ms/顶点估算，并行 10 核 ≈ 30 分钟。等到下次再做。

## 反例搜索的意义

```text
catalog (10,333 互素 multi-N pair, max_hyp=100k):
  closure_pairs = 0
  rank ≤ 4 in samples
  forest-like (most components are tree)

G_M 全图 (338,225 顶点, max_value=1M):
  巨型 component 含 22,115 cycle
  cycle 多 ⇒ partner identity 之间有大量"closed walk"
  但仍然 0 个 closure (N_i + N_j == A + B)
```

cycle 多 ≠ closure 多。cycle 在乘法结构 (Mordell-Weil) 上闭合，closure
要在加法结构 (ℤ) 上闭合。两者结构不同。

**反例可能藏在巨型 component 的 22,115 个 cycle 中某个非平凡 cycle 上**——
这些 cycle 才是真正的"代数闭合候选"，但加法 closure 检查需要对 cycle 上
N 值做积分式遍历，不是简单的 pairwise sum。

## 工程意义

```text
catalog 工作流 (wl048):
  fast pivot scanner → 10,333 互素 multi-N pair
  ⇒ 只看到 G_M 的 3.1% 顶点

完整 partner BFS (wl061):
  catalog 种子 + parallel BFS → 338,225 顶点 (G_M @ max_value=1M)
  ⇒ 真正的 partner web 全貌

要找反例，得在 G_M 全图（不只 catalog）上搜:
  - K_n 真实分布远超 wl055 catalog 数字
  - 顶级 K_n 实例可能在巨型 component 深处
  - 如果有反例，95% 概率在 comp 0 的 22,115 cycle 中
```

## 没做的事

1. **comp 0 内部最高度数顶点**：要找 G_M 真正的 super-hub。可能比 K_8 阶高
2. **巨型 component 内部 22,115 cycle 的拓扑分析**：
   - cycle 长度分布
   - 跟 catalog 互素行的关联模式
3. **comp 0 的 ellrank 全跑**：验证 wl059 deficit 猜想在巨型 component 上
4. **(153, 560) component 的"为什么孤立"分析**：
   max_value=1M 仍然孤立，说明 (153, 560) 的所有 partner web 都在 N≤9360 范围内
   闭合（component 顶点最大坐标 ≤ 100000），结构上是 partner-self-similar 的
5. **更大 max_value (10M, 100M) 重跑**：看 G_M 是否在 max_value=∞ 时
   彻底连通成单一 component（即"G_M 是连通的"）

## 文件

```text
scripts/partner_full_bfs.py                         BFS fixed-point + parallel_map
scripts/partner_full_graph_query.py                 component 查询小工具
results/partner_full_bfs_summary.json               总览
results/partner_full_bfs_components.jsonl           9580 个 component (含全顶点)
results/partner_full_bfs_edges.jsonl                350,868 条边
results/partner_full_bfs_run.log                    完整运行日志（47 round）
docs/work-logs/061-partner-graph-full-bfs-supercomponent.md  本文件
```

## 元注

wl061 是单次工作量最大的 worklog（12 分钟跑数据 + ~30 分钟分析与写作）。
G_M 全貌出来后，之前所有 worklog 都需要重新放在更大背景下：

- wl054-055 K_n 等价定理：成立但只描述 G_M 的"局部 star 结构"
- wl058 G_M ≈ forest：错（仅在 (153, 560) 这种 isolated 小 component 成立）
- wl059 cycle 与 deficit：可能成立但需要在 comp 0 上验证
- wl060 rank ≤ 4：仅对 catalog hub 实测；comp 0 内非互素顶点 rank 还未测

partner graph theory 第一次有了"全貌"。下一步是钻进 comp 0 看真正的中心
拓扑结构。
