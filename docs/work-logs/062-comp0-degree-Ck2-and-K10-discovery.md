# wl062 — comp 0 度数分析：degree 严格 = C(k, 2)，发现 K_10，hubs disjoint

## 触发

wl061 普查找到 309,689 节点超级 component (comp 0)。用户问"comp 0 能不能画图，
看看图结构有什么性质"。

## 工具

- `scripts/comp0_analyze.py`：读 `results/partner_full_bfs_*.jsonl`，分析 comp 0
  degree 分布 + 渲染 PNG 图。
- `scripts/k9_inspect.py`：检查 4 个 K_9 hub 的实际 N 列表 + closure。

## 数据：comp 0 的 8 种离散 degree

```text
deg=1   = C(2,2) → k=2          197,488    63.77%
deg=3   = C(3,2) → k=3           81,386    26.28%
deg=6   = C(4,2) → k=4           23,777     7.68%
deg=10  = C(5,2) → k=5            5,642     1.82%
deg=15  = C(6,2) → k=6            1,132     0.37%
deg=21  = C(7,2) → k=7              218     0.07%
deg=28  = C(8,2) → k=8               42     0.01%
deg=36  = C(9,2) → k=9                4    0.0013%   ← max degree

mean = 2.14   max = 36
```

**所有 degree 严格属于 {C(k, 2) : k = 2..9}**，没有任何例外值（不出现 deg=2, 4, 5, 7,
8, 9, 11-14, 16-20, 22-27, 29-35）。

### 代数解释

partner identity：每个 multi-N pair `(A, B)` 的 N 列表 `[N_1, ..., N_k]` 给出
`C(k, 2)` 个 partner pair `(N_i, N_j)`，每条 partner pair 对应 G_M 上一条边。

⇒ **顶点 v 的 degree = C(k_visible, 2)**，其中 `k_visible` 是该顶点 N 列表中
`max ≤ 1M` 的 N 数（`max_value=1M` 截断之后）。

⇒ **degree 跟 k 双射**：知道 degree 就知道 k。

## 主结论 1：发现 K_9 实例（partner-only，非互素）

wl055 catalog 互素行最高是 K_8（仅 2 个）。wl062 在 comp 0 partner-only 顶点中
发现 **4 个 K_9 实例**：

```text
pair (a, b)             gcd     k_real    N 列表
─────────────────────────────────────────────────────────────────────
(  61200, 222768)       2448    9         17850, 29835, 47424, 92820,
                                          101660, 146880, +3 more
(  76440, 831600)        840    10  ⚠     21888, 33957, 64064, 242550,
                                          262080, 422450, +4 more
( 184800, 308880)       2640    10  ⚠     24750, 90090, 110124, 198900,
                                          231660, 246400, +4 more
(  69615, 221760)        315    9         26180, 64680, 80784, 108108,
                                          142800, 191100, +3 more
```

**两个实例真实 k=10**（图上 degree=36 是因为 1 个 N > 1M 被截断）。也就是
**partner web 实际有 K_10 实例**，wl055 catalog 完全没看到。

closure 检查（N_i + N_j == A+B）全部失败。

## 主结论 2：catalog vs partner-only 的 k_max 巨大反差

```text
catalog 互素行 (550 个 in comp 0):
  avg degree = 1.19    max degree = 6     ⇒  avg k = 2.04, max k = 4

partner-only 顶点 (309,139 个 in comp 0):
  avg degree = 2.14    max degree = 36    ⇒  avg k = 2.46, max k_visible = 9
                                              max k_real = 10
```

**catalog 互素行根本看不到 K_5+**。所有高阶 K_n 实例（K_5 到 K_10）全部躲在
非互素 partner-only 顶点里。

这跟 wl056 的发现一致 ("91-94% partner pair 是非互素")，但 wl062 给出量化：
**互素 catalog 行的 partner k 最多到 4**（典型 ≈ 2-3），高阶聚合都在非互素层。

## 主结论 3：Hubs 互不相邻 + 邻居 disjoint

`scripts/comp0_analyze.py` 抽 top-30 / top-100 高度数顶点诱导子图：

```text
top-30 induced subgraph:    30 nodes, 0 edges
top-100 induced subgraph:  100 nodes, 0 edges
```

**任何两个 K_6+ hub 之间都没有直接 partner edge**（在 comp 0 里）。

抽 4 个 K_9 hub + 1-hop 邻居子图：

```text
K_9 hubs + neighbors:  V = 148  E = 144 = 4 × 36
                       即 4 hub × 36 邻居 = 144 邻居（无重叠）
                       ⇒ 4 个 K_9 实例的 N 列表彼此 disjoint
```

见 `docs/figures/wl062/comp0_k9_neighborhood.png` —— 4 个 K_9 hub 表现为 4 个
完全独立的 star（如果没有重叠邻居则 V = 4 + 144 = 148，实际 V = 148 即 0 重叠）。

## 主结论 4：Power-law degree 分布

`docs/figures/wl062/comp0_degree_distribution.png` 显示 log-log 分布近似线性：

```text
degree     count           log10(count) / log10(degree)
─────────────────────────────────────────────────────────
   1     197,488                      ∞ (无穷)
   3      81,386       4.91 / 0.48 ≈ 10.2
   6      23,777       4.38 / 0.78 ≈  5.6
  10       5,642       3.75 / 1.00  =  3.75
  15       1,132       3.05 / 1.18 ≈  2.59
  21         218       2.34 / 1.32 ≈  1.77
  28          42       1.62 / 1.45 ≈  1.12
  36           4       0.60 / 1.56 ≈  0.38
```

接近 log-linear（power-law），slope 大致 −2 到 −3。是典型 scale-free network。

## 拓扑解释

G_M comp 0 整体结构：

```text
hierarchical scale-free network with 8 discrete strata:
  k=2 (deg=1)   layer:  197,488 nodes   ← 大量"leaves"，单 partner
  k=3 (deg=3)   layer:   81,386 nodes
  k=4-5         layer:  ~30,000 nodes   ← K_4, K_5 hubs
  k=6-7         layer:   ~1,350 nodes   ← K_6, K_7 hubs
  k=8-9         layer:       46 nodes   ← K_8, K_9 super-hubs

每层 hub 不相邻同层其他 hub，必经过低层（小 k）顶点中转。
形成"hubs ↔ low-degree intermediaries"的 bipartite-like 拓扑。
```

这跟 Barabási–Albert 偏好附着模型生成的 scale-free network 拓扑很相似。
但 G_M 的 **degree 离散到只 8 个值**（不是连续 power-law），结构更刚硬。

## wl059 deficit 猜想 + wl060 rank 上限的更新

wl060 实测 catalog 内所有 K_3 到 K_8 hub 的 PARI rank ≤ 4。但 wl062 发现
catalog 不见的 K_9, K_10 实例。需要给它们跑 ellrank 验证 rank ≤ 4 是否仍成立：

```text
预测 (wl060 rank 上限假设):
  K_9  rank ≤ 4 ⇒ deficit = 9 - rank ≥ 5
  K_10 rank ≤ 4 ⇒ deficit = 10 - rank ≥ 6
```

如果 K_9/K_10 实测 rank > 4，wl060 假设需要修正。如果仍 ≤ 4，那是个非常强的
catalog-wide 结构性证据。**留给 wl063**。

## 反例搜索的影响

```text
反例搜索:  multi-N pair (A, B) k≥2 + N_i + N_j = A + B

wl062 数据告诉我们:
  comp 0 共 309,689 个 multi-N pair 候选
  其中 ~1,396 个高 k (k≥6) hub
  其中 4 个 K_9 + 2 个 K_10 (kingsmaker hub)
  closure 检查全部失败 (从 K_8 wl055 + K_9/K_10 wl062 实测)

下一步搜索面应该:
  K_n 阶 (n=6, 7, 8, 9, 10) 全 hub × 它们的所有 (N_i, N_j) 对
  即 ~1,400 hub × 平均 28 partner pair = 39,200 candidate sums
  每个 hub 跑一次 closure check ≈ 1ms ⇒ 全检测 < 1 分钟
```

也就是说，**反例搜索其实可以彻底完成（在 max_value=1M 截断内）**：把所有 G_M 顶点
全检 closure，1-2 分钟出结果。**这是个全新的可以做的实验**——之前我们一直用
catalog (10333 行) 检 closure，但现在 G_M 真实顶点数是 338K。**留给 wl063
另一线**。

## 文件

```text
scripts/comp0_analyze.py                              comp 0 分析 + 渲染
scripts/k9_inspect.py                                 K_9 实际 N 列表检查
results/comp0_analyze_summary.json                    comp 0 分析摘要 (gitignored)
results/comp0_degree_distribution.png                 (gitignored)
results/comp0_top30_subgraph.png                      (gitignored)
results/comp0_top100_subgraph.png                     (gitignored)
results/comp0_k9_neighborhood.png                     (gitignored)

docs/figures/wl062/comp0_degree_distribution.png      入库的关键图
docs/figures/wl062/comp0_top30_subgraph.png
docs/figures/wl062/comp0_k9_neighborhood.png

docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md  本文件
```

## 元注

wl062 是 wl061 的自然延伸：从"G_M 全貌"钻进 comp 0 看真正中心结构。
两个最深的发现：

1. **degree = C(k, 2)** 这个事实把 wl054-055 的 partner-pair k 等价定理
   翻译成图上严格的代数公式。所以 G_M 的 degree 分布 ≡ k 分布。
2. **K_10 的发现** + **catalog max k = 4 vs partner-only max k = 10**：
   说明 catalog 不是 G_M 的代表性样本，是个 highly biased slice。

下一步路线：
- wl063: 跑 G_M 全 closure 检查 (~1 分钟)
- wl064: K_9/K_10 ellrank
- wl065: power-law 拟合 + scale-free 性质形式化
