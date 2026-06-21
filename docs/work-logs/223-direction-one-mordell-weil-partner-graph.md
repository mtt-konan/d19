# wl223 — 方向一：`G_M` 是否本质上来自 Mordell-Weil 群

日期：2026-06-21

## 1. 本轮问题

用户提出的方向一：

```text
图是否本质上来自椭圆曲线群？
concordant number 问题本身对应椭圆曲线。
pair 是在找两个整数同时属于多个勾股三元组。
一个节点能生成新节点，新节点又生成新节点，图一直长下去。
这很像 Mordell-Weil 群结构。
如果是真的，图无限不是巧合，而是因为椭圆曲线秩大于 0。
```

普通话先说结论：

```text
这个怀疑是对的，但要改得更精确。

不是“整张 G_M 是同一条椭圆曲线的群”。
更像是：

  每个节点内部由一条椭圆曲线的 Mordell-Weil 群控制；
  整张 partner graph 是很多条椭圆曲线之间，
  由特殊 square-x 点互相跳转织出来的网络。
```

所以方向一不是一句“图等于群”，而是一个更好的研究命题：

```text
G_M 的巨大连通分量很可能来自若干正秩 primitive 椭圆曲线底型；
partner 边不是单条曲线内的群运算，
而是由 Mordell-Weil 群中特殊 square-x 点诱导出的曲线间对应。

当前最强的可检验模型是：
  正秩给出有理点来源
  + 放大倍数 d 清掉分母
  + 某些有理 n 变成整数 N
```

## 2. 基本翻译

对一个节点 `(A, B)`，对应椭圆曲线：

```text
E_{A,B}: y^2 = x(x + A^2)(x + B^2)
```

一个 concordant 整数 `N` 给出曲线上的特殊点：

```text
x = N^2
x + A^2 = square
x + B^2 = square
```

也就是说：

```text
N 是一个整数
<=>
E_{A,B} 上出现了一个 x 坐标为平方数的特殊有理点
```

partner graph 的边再多走一步：

```text
(A, B) 有 N_1, ..., N_k
=> 任取两个 N_i, N_j
=> 生成新节点 (N_i, N_j)
=> 跳到另一条曲线 E_{N_i,N_j}
```

这一步是关键边界：

```text
如果只看一个节点内部，它确实是椭圆曲线群问题。
但 G_M 的边会换曲线，所以全图不是单条 E(Q) 的 Cayley graph。
```

## 3. 已经确认的证据

### 3.1 每个 concordant 点落在 `2E(Q)` 内

wl086 已经把 wl058/wl059 的 cycle 关系算到 Mordell-Weil 坐标层面。

关键事实：

```text
对 concordant 点 Q_N = (N^2, N*sqrt(N^2+A^2)*sqrt(N^2+B^2)):

  x = N^2 是平方
  x + A^2 是平方
  x + B^2 是平方

所以 2-descent 像平凡，Q_N in 2E(Q)。
```

普通话说：

```text
concordant 条件不是随便给曲线上一个点，
而是把点强行压进 Mordell-Weil 格的偶数层。
```

这解释了为什么高 `k` 节点会出现很多线性关系：

```text
N 越多，给出的 Q_N 越多；
但这些 Q_N 全都挤在 2E(Q) 的低维格里；
于是多出来的 N 往往不是新独立方向，而是线性冗余。
```

### 3.2 cycle 的代数半部分已解释，但不是 closure 障碍

wl086 的更精确结论：

```text
cycle 关系 = Q_N 坐标矩阵的秩亏
deficit 应看 k - coord_rank，而不是粗看 k - MW_rank
```

这支持方向一的“图里有 MW 群影子”。

但也给了一个重要刹车：

```text
Q_N in 2E(Q) 对任何 concordant 点都成立，
无论最后有没有 Harborth closure。

所以它解释图结构，
但不能直接区分反例和非反例。
```

换句话说：

```text
MW 群解释了图为什么长成这样；
但 closure=0 还需要额外的加法/高度/模约束。
```

### 3.3 高 `k` 主要来自 D-scaling，不是 rank 一路升高

wl065/wl085/wl094/wl095 给了方向一最强的证据链。

若：

```text
(A, B) = (d a_0, d b_0)
```

则：

```text
E_{A,B} ≅ E_{a_0,b_0} over Q
X = d^2 x
Y = d^3 y
```

所以：

```text
rank 不变
```

但整数 `N` 会变：

```text
primitive 曲线上有 rational n = p/q
放大 d 后，N = d*n
只要 q | d，N 就变成整数
```

这解释了一个之前很怪的现象：

```text
primitive 底型本身整数 N 不多，
但某些放大版本能变成 K_9/K_10/K_16；
rank 却仍然只有 3 或 4。
```

这不是“高 k 带来高 rank”，而是：

```text
低秩正秩曲线
+ 很多有理 square-x 点
+ 放大清分母
=> 高 k 整数 hub
```

### 3.4 rank <= 4 目前守到 K_16

现有高阶 hub 审计：

```text
k = 6..8:   wl060, 11 个 hub, rank 3..4
k = 9..10:  wl094, 48 个 hub, rank 3..4
k = 11..13: wl094, 11 个 hub, rank 3..4
k = 16:     wl095, K_16 hub, rank 4
```

合并读法：

```text
目前看到的高阶 partner hub，
不是因为 Mordell-Weil rank 无限制上升；
而是因为同一批低维 MW 格在不同整数模型里露出了更多整数截面点。
```

这对方向一很重要：

```text
giant 的持续增长可能确实以 rank > 0 为背景；
但“局部高 k”主要来自 scaling 清分母，而不是 rank 无限增大。
```

### 3.5 comp0 / branch / island 三层分解支持这个图像

wl096 把 `G_M @ 1M` 分成：

```text
giant comp0: 309,689 顶点
branch:      620 个截断断枝，窗口变大时会逐步并入 giant
island:      8,959 个永久孤岛，无上限 BFS 仍闭合
```

7M BFS 验证：

```text
giant: 92% -> 98.9%
K_7/K_8 branch 全并入 giant
island 0 泄漏
```

普通话说：

```text
大图不是所有碎片都会连成一团。
它分成：
  一个随窗口增长的巨型主体；
  一些会被主体吞并的断枝；
  还有很多真正自闭合的小孤岛。
```

这也修正了方向一：

```text
正秩/D-scaling 可以解释 giant 的增长和高 k 生成；
但有限孤岛说明 G_M 全局不是单一正秩机制。
```

## 4. 目前不能这么说

### 4.1 不能说 `G_M` 就是一个 Mordell-Weil 群

原因：

```text
每个节点 (A,B) 对应自己的 E_{A,B}。
一条 partner 边会从 E_{A,B} 跳到 E_{N_i,N_j}。
```

所以更准确是：

```text
G_M 是椭圆曲线族之间的 correspondence graph。
每个局部 star/hub 由某条曲线的 MW 格提供点源。
```

### 4.2 不能说 `rank > 0` 自动给无限个整数 `N`

rank > 0 给的是无限有理点。

但我们要的是很特殊的点：

```text
x = N^2
x + A^2 = square
x + B^2 = square
N 是整数
```

这是稀有截面。

所以更安全的表述是：

```text
rank > 0 提供无限有理点背景；
整数 multi-N 的增长还依赖 square-x 截面和 scaling 清分母。
```

### 4.3 不能把 finite `G_M @ 1M/7M` 说成无限图证明

当前 BFS 窗口结果是强实证。

只有 island 的“永久封闭”已经用无上限 BFS + 完备因子核做了确定性验证。

但 giant 是否在无限图里有怎样的完整结构，仍不能靠有限 BFS 直接证明。

## 5. 方向一的下一步最小实验

### 实验 A：primitive 层的 `k(d)` 函数画像

目标：

```text
给定 primitive (a_0,b_0)，把 d -> k(d) 画清楚。
```

已有工具：

```text
scripts/multi_n/k14_search.py
src/rational_distance/concordant/dscale_kn.py
src/rational_distance/concordant/fast_multi_n.py
```

建议输出：

```text
primitive
rank
rational_n_pool_size
d
k_exact(d)
denominator_lcm_pattern
closure_hit
component_layer_if_known
```

要回答：

```text
rank 1/2/3/4 的 k(d) 增长是否有稳定阶梯？
高 k 是否总来自少量分母的 lcm？
closure=0 是否能转写成 denominator/residue 条件？
```

### 实验 B：把 partner 边投影到 primitive 层

对一条边：

```text
(A,B) -- (N_i,N_j)
```

记录：

```text
prim(A,B) = (A/g, B/g)
prim(N_i,N_j) = (N_i/h, N_j/h)
```

看 giant comp0 内：

```text
primitive -> primitive
```

是不是只有少数模板。

如果是，方向一会从“像群”升级成：

```text
finite primitive correspondence templates
+ D-scaling denominators
=> infinite partner graph growth
```

### 实验 C：按 MW 坐标解释 `k(d)` 中新增的 N

对一个代表 primitive，例如：

```text
(91,990), (221,704), (2975,7904)
```

把每个 rational `n=p/q` 对应的点写成 MW generator 坐标：

```text
Q_n = c_1 G_1 + ... + c_r G_r + T
```

然后看：

```text
分母 q 与坐标向量 c 有没有简单关系？
高 k 的 d 是否只是收集了一批低高度坐标点的分母？
```

这个实验能直接回答：

```text
“放大清分母”背后到底是不是 MW 格的低高度壳层在起作用。
```

## 6. 初步实验：primitive 边模板投影

本轮先把实验 B 做了一个最小版本。

新增工具：

```text
scripts/partner/primitive_projection.py
tests/test_partner_primitive_projection.py
results/partner/primitive_projection_1M_summary.json
```

做法很简单：

```text
原始边:        (A,B) -- (N_i,N_j)
压缩成模板:    prim(A,B) -- prim(N_i,N_j)
```

其中：

```text
prim(x,y) = (x/g, y/g), g=gcd(x,y), 再按大小排序
```

跑全 `G_M @ max_value=1M` 的边文件：

```bash
uv run python scripts/partner/primitive_projection.py \
  --top 25 \
  --components results/partner/partner_full_bfs_components.jsonl \
  --layers results/partner/comp0_island_analysis_1M.jsonl
```

结果：

```text
raw edges scanned:     350,868
unique templates:       34,306
unique primitives:      35,670
primitive self-loops:      306

top 25 templates cover:       6.35% of raw edges
top 25 primitive endpoints:  14.07% of endpoint incidences
cross-layer edges:            0
missing-layer edges:          0
```

普通话解释：

```text
把 35 万条边约去缩放后，没有塌成几十条模板；
所以“少数 primitive 模板支配整张图”这个强说法不成立。

但热点也很明显：
前 25 个 primitive 端点吃掉了 14% 的边端点，
说明巨大分量不是均匀散开的，确实有一批 primitive 底型在当骨架节点。
```

top primitive 端点前几名：

```text
(25, 91)     incident_edges = 8290
(70, 117)    incident_edges = 7453
(11, 45)     incident_edges = 5464
(22, 35)     incident_edges = 5243
(13, 64)     incident_edges = 5130
```

这里最有意思的是：

```text
(25,91), (70,117)
```

正是 wl065/wl085 中解释 K_9/K_10 的 D-scaling primitive 底型。

top 模板前几名：

```text
(11,45)  -- (22,35)    count = 1508
(7,32)   -- (22,35)    count = 1408
(6,13)   -- (13,64)    count = 1297
(5,26)   -- (25,91)    count = 1162
(7,18)   -- (7,32)     count = 1101
(25,91)  -- (70,117)   count = 676
```

这给方向一一个更精确的修正：

```text
不是 finite primitive templates + D-scaling 就能解释全图。
更像是：

  一个较大的 primitive correspondence graph
  + 一批高 incident primitive 热点
  + 每个热点周围再由 D-scaling 放大成大量 raw edges。
```

也就是说，方向一仍然成立，但它不是“低模板数”的图像，而是：

```text
primitive 层已有一张不小的图；
raw G_M 是这张 primitive 图被 scaling 展开后的 lift。
```

### 6.1 分层后差异更清楚

把边按 wl096 的三层 `giant / branch / island` 分开看：

```text
layer    raw edges   unique templates   unique primitives   top25 endpoint share
giant    331,803      24,477             19,224              14.56%
branch     5,106       2,704              2,579              19.48%
island    13,959      12,036             19,751               3.27%
```

普通话说：

```text
giant 和 branch 有明显热点骨架：
  很多 raw edges 会反复落到同一批 primitive 底型周围。

island 完全不同：
  13,959 条边已经散成 12,036 个 primitive 模板，
  top 25 primitive 端点只覆盖 3.27% 的 incidence。
```

这很贴合 wl096 的三层图像：

```text
giant / branch = 可由若干热点 primitive + scaling lift 解释的主体结构
island          = 大量小而自闭合、primitive 层也高度分散的碎片
```

top primitive 端点也不同：

```text
giant top:  (25,91), incident_edges = 8121
branch top: (25,91), incident_edges = 151
island top: (2,19),  incident_edges = 80
```

这给方向一一个更好的分层版本：

```text
方向一主要解释 giant/branch 的增长机制；
island 更像是有限自闭合配置池，不该强行并入同一个 MW-scaling 主叙事。
```

所以后续实验要分开问：

```text
giant/branch:
  top primitive 是否 rank 3/4？
  high incident 是否来自 D-scaling denominator lift？

island:
  为什么 primitive 层也这么分散？
  是否可以用低 k、有限封闭轨道、模条件一次性分类？
```

下一步应该把 primitive 层继续分解：

```text
1. 给每个 top primitive 跑 rank / rational_n_pool_size。
2. 看 top primitive 是否主要 rank 3/4。
3. 对 top 模板检查是否来自同一批低分母 rational n。
4. 区分 comp0 / branch / island 后分别统计 primitive 模板。
```

### 6.2 top primitive rank 审计

为了检查“primitive 热点是否真的对应正秩椭圆曲线”，本轮又加了一个小审计：

```text
scripts/partner/primitive_rank_audit.py
tests/test_primitive_rank_audit.py
results/partner/primitive_rank_audit_top.jsonl
results/partner/primitive_rank_audit_top_summary.json
```

命令：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_rank_audit.py --limit 40
```

选择方式：

```text
先取全图 top primitive；
再补 giant / branch / island 各自的 top primitive；
按出现顺序去重，取前 40 个。
```

结果：

```text
total audited: 40
certified:     40 / 40
rank histogram:
  rank 1:  3
  rank 2: 26
  rank 3: 11
  rank>4:  0

by source:
  global:  rank 1:2, rank 2:18, rank 3:5
  branch:  rank 2:3, rank 3:4
  island:  rank 1:1, rank 2:5, rank 3:2
```

top 两个：

```text
(25,91):  incident_edges=8290, rank=3 certified
(70,117): incident_edges=7453, rank=3 certified
```

普通话解释：

```text
primitive 热点确实全是正秩；
这支持“图的热点来自椭圆曲线有理点群”。

但它们不是 rank 4/5/6 这种高维热点。
40 个 top primitive 里，绝大多数只是 rank 2 或 rank 3。
```

所以方向一再收紧一层：

```text
giant/branch 的热点不是靠高 rank 撑起来的；
而是靠低维正秩 MW 格 + 大量 scaling lift + primitive correspondence 重复。
```

这也解释了为什么：

```text
高 k hub 可以到 K_16；
但 primitive / scaled rank 仍然守在 1..4 的低维范围。
```

换句话说：

```text
“群结构”是真的；
“高维群结构”目前不是。
```

### 6.3 rational `n` 池大小：低维但点池很丰富

上面的 rank 审计只说明：

```text
top primitive 是正秩；
但 rank 主要只有 1/2/3。
```

还差中间一步：

```text
这些低维正秩曲线，是否真的给了足够多 rational n，
让 D-scaling 有东西可以清分母？
```

因此把 `primitive_rank_audit.py` 加上：

```text
--include-pool
```

它会调用 `enumerate_rational_n`，记录当前参数下找到的 rational `n` 池：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_rank_audit.py \
  --limit 40 \
  --include-pool
```

结果：

```text
total audited: 40
pool_size_min: 50
pool_size_max: 262
pool_size_avg: 151.28
```

按 rank 分组非常干净：

```text
rank 1: n=3,  pool size = 50
rank 2: n=26, pool size = 116..119, avg 116.12
rank 3: n=11, pool size = 262
```

分层看：

```text
global: n=25, pool 50..262, avg 140.04
branch: n=7,  pool 116..262, avg 199.43
island: n=8,  pool 50..262, avg 144.25
```

top pool 样本：

```text
(25,91)    source=global  rank=3  incident=8290  pool=262
(70,117)   source=global  rank=3  incident=7453  pool=262
(112,325)  source=global  rank=3  incident=3253  pool=262
(13,266)   source=branch  rank=3  incident=88    pool=262
(65,901)   source=island  rank=3  incident=34    pool=262
```

普通话解释：

```text
rank 不高，但每条 primitive 曲线已经有很大的 rational n 池。
rank 1 也能给 50 个，rank 2 约 116 个，rank 3 到 262 个。

所以 D-scaling 不是“凭空制造高 k”，
而是在一个已经很丰富的 rational n 池里，
用 d 把很多分母同时清掉。
```

这把方向一的机制链补完整了一段：

```text
正秩 MW 格
=> 产生大量 rational square-x / concordant n
=> denominator 池很丰富
=> scaling d 清分母
=> raw G_M 里出现大量边和高 k hub
```

但还要保留一个边界：

```text
当前 rational n pool 不是 E(Q) 全集，只是 bounded enumeration。
所以 pool size 是“已找到的下界”，不是数学完整计数。
```

### 6.4 scaling 闭环：真实缩放顶点被分母规则解释

最后还要检查最关键的一步：

```text
真实 G_M 顶点 (A,B)=d(a0,b0) 的整数 k，
是否真的能由 primitive rational n 池的 denominator | d 规则解释？
```

新增：

```text
scripts/partner/primitive_scaling_audit.py
tests/test_primitive_scaling_audit.py
results/partner/primitive_scaling_audit_summary.json
results/partner/primitive_scaling_audit_top40.jsonl
results/partner/primitive_scaling_audit_top40_summary.json
```

审计逻辑：

```text
1. 固定 primitive (a0,b0)。
2. 从 G_M @ 1M components 里找所有缩放顶点 (A,B)=d(a0,b0)。
3. 用 exact_concordant_pair(A,B) 算真实整数 exact_N 集合。
4. 用 primitive rational n pool 算 pool_N(d)={d*n : n=p/q, q | d}。
5. 比较 pool_N(d) 是否等于 exact_N。
```

命令样例：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_scaling_audit.py \
  --primitive 25,91 \
  --out results/partner/primitive_scaling_audit_25_91.jsonl \
  --summary-out results/partner/primitive_scaling_audit_25_91_summary.json
```

审了四个代表：

```text
primitive   layer role        scaled vertices   coverage   max exact k   pool size
(25,91)     global top        1446              100%       10            262
(70,117)    global top        1218              100%       10            262
(2,19)      island top         411              100%        5            116
(13,266)    branch top         192              100%        6            262
```

汇总：

```text
audited primitives:       4
total scaled vertices:    3267
covered vertices:         3267
overall coverage:         100%
exact set matches:        3267
exact set match pct:      100%
max exact k covered:      10
total missing_k:          0
```

普通话解释：

```text
这是真正的闭环证据：

  primitive 曲线上找到的 rational n
  经过 d 清分母
  确实逐项复现了这些真实 G_M 顶点的 exact integer N 集合。
```

尤其是：

```text
(25,91), (70,117)
```

这两个全图 top primitive 的 2664 个真实缩放顶点全部 exact_N 集合匹配，
最高匹配到 K_10。

这让方向一的机制链从“像”变成了可实证复现：

```text
primitive 正秩 MW 格
=> rational n 池
=> denominator | d
=> exact integer N 集
=> raw G_M 高 incident / high-k 结构
```

边界也要写清楚：

```text
这不是全 35,670 个 primitive 的证明；
只是四个代表 primitive 的强实证。

但它已经覆盖了全图 top primitive、branch top primitive、island top primitive，
并且覆盖到 K_10。
```

### 6.5 top40 批量 scaling 审计：闭环扩大到 40/40

为了避免“四个代表点”太像挑样本，又把 top primitive rank audit 的前 40 个
primitive 全部批量跑了一遍 scaling 闭环。

命令：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_scaling_audit.py \
  --rank-audit results/partner/primitive_rank_audit_top.jsonl \
  --limit 40 \
  --out results/partner/primitive_scaling_audit_top40.jsonl \
  --summary-out results/partner/primitive_scaling_audit_top40_summary.json
```

批量审计结果：

```text
audited primitives:             40
total scaled vertices:      30,637
exact set matches:          30,637
exact set match pct:       100.00%
max exact k:                    10
total missing_k:                 0
```

普通话解释：

```text
如果把前 40 个热点 primitive 周围所有真实缩放顶点都拿来问：

  这些真实整数 N 集合，能不能由 primitive rational n 池
  通过 denominator | d 的清分母规则复现？

答案是：top40 里全部可以。

30,637 个缩放顶点里，30,637 个 exact_N 集合逐项相等。
也就是说，这不是只在几个漂亮例子上成立；
它已经覆盖了 top40 热点的全部缩放顶点。
```

更细看：

```text
40 / 40 个 primitive 是 100% exact-set match。

source = island:  8 / 8 primitive, 1555 / 1555 vertices match, 100%
source = global: 25 / 25 primitive 完全匹配
source = branch:  7 / 7 primitive 完全匹配
```

中间曾出现两个没有闭合的点：

```text
primitive     source   rank   scaled vertices   match pct   missing_k
(117,320)    global   2      704               34.80%      549
(800,1463)   branch   3      146                0.00%      359
```

这两个点先给了一个很有用的排错信号。
最小漏点是：

```text
(117,320), d=5:     exact N 包含 2244 = 5 * (2244/5)
(800,1463), d=1:    exact N 包含 840
```

把这些漏点放回椭圆曲线群里看：

```text
(585,1600), N=2244:
  在 E_{585,1600} 上的 MW 坐标是 (-2,-2) + torsion。

(800,1463), N=840:
  在 E_{800,1463} 上可由 effortful generator basis 的 2G 给出。
```

也就是说，问题不在 scaling 规则；
问题在 `enumerate_rational_n` 原来只拿了一次 PARI `ellrank(E)` 返回的基底。

PARI 的 `ellrank` 返回的 rank 可以一样，
但生成元基底不同；
在有限的 `rank_combo_bound` 盒子里，
某个 square-x 点可能在一个基底下系数很小，
在另一个基底下系数很大。

修复：

```text
src/rational_distance/concordant/dscale_kn.py
tests/test_dscale_kn.py
```

`enumerate_rational_n` 现在会合并多个 `ellrank` effort/basis：

```text
effort = requested effort
+ effort 0
+ effort 1
+ effort 2
```

并且每组基底都走同一套：

```text
per-generator multiples
+ rank-combination box
+ torsion expansion
+ ellratpoints fill-in
```

两个回归测试锁住了这两个漏法：

```text
test_enumerate_rational_n_uses_effortful_generators_for_square_x_points
test_enumerate_rational_n_combines_effortful_generators_with_torsion
```

复跑两个异常点：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_scaling_audit.py \
  --primitive 117,320 \
  --rank-combo-bound 7 \
  --ratpoints-bound 500000 \
  --out results/partner/primitive_scaling_audit_117_320_deeper.jsonl \
  --summary-out results/partner/primitive_scaling_audit_117_320_deeper_summary.json

PARI_MT_ENGINE=single uv run python scripts/partner/primitive_scaling_audit.py \
  --primitive 800,1463 \
  --rank-combo-bound 7 \
  --ratpoints-bound 500000 \
  --out results/partner/primitive_scaling_audit_800_1463_deeper.jsonl \
  --summary-out results/partner/primitive_scaling_audit_800_1463_deeper_summary.json
```

结果：

```text
(117,320): 704 / 704 vertices exact-set match, max exact k = 7
(800,1463): 146 / 146 vertices exact-set match, max exact k = 6
```

再复跑 top40：

```text
audited primitives:        40
total scaled vertices:     30,637
exact-set match:           30,637
overall match pct:         100.00%
total missing_k:           0
```

这正好把研究边界画清楚：

```text
不是 “G_M 就是一个 MW 群”。
也不是 “有限枚举器天然完整”。

但可以很有把握地说：
G_M 的 top40 热点缩放主体确实由正秩 primitive 椭圆曲线 +
D-scaling 清分母机制放大出来。
```

### 6.6 MW evidence table：把分母和群坐标放到同一张表里

top40 scaling 闭环回答了：

```text
真实 exact_N 集合能不能由 primitive rational n pool + denominator | d 复现？
```

但还需要再往前一步：

```text
这些 rational n 在 MW 群里到底长什么样？
是不是只是黑箱枚举器碰巧捞到了？
```

新增：

```text
scripts/partner/primitive_mw_evidence.py
tests/test_primitive_mw_evidence.py
results/partner/primitive_mw_evidence_top6.jsonl
results/partner/primitive_mw_evidence_top6_summary.json
```

命令：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_mw_evidence.py \
  --limit-primitives 6 \
  --vertices-per-primitive 1 \
  --out results/partner/primitive_mw_evidence_top6.jsonl \
  --summary-out results/partner/primitive_mw_evidence_top6_summary.json
```

这个表对每个代表缩放顶点逐个记录：

```text
primitive
(A,B)=d(a0,b0)
exact N
rational n = N/d
rational n denominator
pool 是否包含 rational n
MW rank / rank bounds
Q_N 的 MW 坐标
torsion order
two_divisible
point_verified
```

跑前 6 个全图热点 primitive，每个取一个最高 k 的代表缩放顶点：

```text
primitive   d      representative vertex       k    pool hit   MW verified   two-divisible
(25,91)     8976   (224400,816816)             10   yes        yes           yes
(70,117)    2640   (184800,308880)             10   yes        yes           yes
(11,45)    10920   (120120,491400)              7   yes        yes           yes
(22,35)     2340   (51480,81900)                6   yes        yes           yes
(13,64)     5985   (77805,383040)               7   yes        yes           yes
(6,13)      9240   (55440,120120)               6   yes        yes           yes
```

汇总：

```text
primitive count:        6
representative vertices:6
evidence rows:          46
all pool hits:          true
all MW verified:        true
all two-divisible:      true
```

样例行：

```text
primitive (25,91), d=8976, N=65450:
  rational n = 175/24
  24 | 8976
  MW coords = [2,0,0]
  torsion order = 2
  point verified = true

primitive (25,91), d=8976, N=173888:
  rational n = 988/51
  51 | 8976
  MW coords = [0,-2,-2]
  torsion order = 1
  point verified = true
```

更有意思的是坐标大小：

```text
(25,91)   k=10, max |MW coord| = 4
(70,117)  k=10, max |MW coord| = 2
(11,45)   k=7,  max |MW coord| = 2
(22,35)   k=6,  max |MW coord| = 2
(13,64)   k=7,  max |MW coord| = 2
(6,13)    k=6,  max |MW coord| = 2
```

普通话解释：

```text
这些高 k 不是靠 MW 格里很远、很深的点撑出来的。

在这些代表热点上，很多 exact N 对应的是非常低坐标的 MW 点：
±2 级别的生成元组合，再加 torsion。

高 k 的主要来源不是“群坐标很大”，
而是 primitive 曲线上已经有一批低坐标 rational n，
它们的 denominator 同时被某个 d 清掉。
```

这让方向一的结构图更具体：

```text
small MW coordinates
=> rational square-x points n=p/q
=> one d divisible by many q
=> many integer N=d*n
=> high-k raw vertex
=> partner graph hotspot
```

随后把同一张表扩大到 top40 primitive，每个 primitive 取一个最高 k
的代表缩放顶点：

```bash
PARI_MT_ENGINE=single uv run python scripts/partner/primitive_mw_evidence.py \
  --limit-primitives 40 \
  --vertices-per-primitive 1 \
  --out results/partner/primitive_mw_evidence_top40.jsonl \
  --summary-out results/partner/primitive_mw_evidence_top40_summary.json
```

top40 代表表结果：

```text
primitive count:                 40
representative vertices:          40
evidence rows:                   251
pool hit rows:                   251 / 251 = 100.00%
two-divisible rows:              251 / 251 = 100.00%
point verified rows:             251 / 251 = 100.00%
max |MW coord|:                    4
max rational-n denominator:     1995
unverified primitive coords: none
```

普通话解释：

```text
把 top40 每个热点都取一个最高 k 代表点后，
所有 251 个 exact N 都能写成：

  N = d * n

而且 n 全部在 primitive rational pool 里。

这说明 D-scaling 清分母这条链在 top40 代表点上完全成立。
```

同时，所有 251 个 Q_N 都是 two-divisible：

```text
Q_N ∈ 2E(Q)
```

这和 wl086 的 cycle/MW 观察对上：
concordant N 给出的点不是随便散在 E(Q) 里，
而是落在很有结构的 2-divisible 子层里。

再次把这条链收紧：

```text
pool hit / two-divisible / MW coordinate exact verification
现在都是 251 / 251 = 100%。
```

中间曾经有 8 行未 verified，集中在两个 primitive：

```text
(32,143)
(800,1463)
```

排查后确认这不是 scaling 规则失败：

```text
这些行仍然全部 pool hit；
也全部 two-divisible；
MW 坐标也都是小坐标，max |coord| <= 2。
```

一开始怀疑这是 `mw_coordinates` 用 height-pairing round-to-integer
表达坐标时的“小范围取整偏差”。

但对 `(32,143)` 的代表点做了进一步排查：

```text
(109440,489060), Ns = [12705,82080,98800,541728,619008,652080]
```

在当前 effort=1 的 PARI generator basis 下，
对未 verified 的 4 个点搜索坐标半径到 12，
仍然找不到 residual torsion order ∈ {1,2,4} 的表达。

所以更准确的根因不是“rounding 偏一两格”，
而是：

```text
PARI ellrank 返回的 generators 可能只张成一个有限指数子格；
这些 Q_N 在 E(Q) 里 two-divisible，
但不一定落在当前 generator list 的整数张成子格 + torsion 里。
```

换句话说，需要的是 MW generator saturation / 换基底，
不是简单邻域修补。

例如：

```text
(800,1463) 对应的 scaled 代表点
(86400,158004)
在 effort=1 下有 4 个点 residual torsion order = 0；
换 effort=2 的 generator basis 后，该代表点可以 all_verified。

(32,143) 对应的 scaled 代表点
(109440,489060)
在 effort=1..4 下仍有 4 个 residual torsion order = 0；
但对 ellrank generators 做 p=3 saturation 后，
6 个 concordant points 全部 all_verified。
```

实现收口：

```text
src/rational_distance/concordant/cycle_relations.py
新增 _saturate_generators:
  对 ellrank 返回的 generators 依次尝试 p = 2,3,5,7,11,13 saturation。

tests/test_cycle_relations.py
新增 test_mw_coordinates_saturates_ellrank_subgroup，
锁住 (109440,489060) 这个曾经失败的样本。
```

复跑 top40 MW evidence：

```text
evidence rows:              251
pool hit rows:              251 / 251 = 100.00%
two-divisible rows:         251 / 251 = 100.00%
point verified rows:        251 / 251 = 100.00%
MW all verified rows:       251 / 251 = 100.00%
unverified primitives:      []
```

所以 top40 MW evidence 的正确读法现在更强：

```text
方向一的 scaling / denominator / two-divisible / MW-coordinate
四个层面在 top40 代表点上全部闭合。

之前的 8 个 unverified 不是数学反例，
而是 PARI ellrank 给的自由生成元还差 saturation。
```

### 6.7 giant 内是否反复落到同一条椭圆曲线

方向一继续追问：

```text
同一个巨大连通块里的节点，是否反复对应到同一条椭圆曲线？
```

这里要先把“同一条”说清楚。

每个 raw 节点 `(A,B)` 都有自己的整数模型：

```text
E_{A,B}: y^2 = x(x+A^2)(x+B^2)
```

如果只按 raw `(A,B)` 算，那基本就是“一节点一曲线”，问题没有太多信息。
真正和 D-scaling 机制相关的是：

```text
(A,B) = d(a0,b0)
```

这时 `E_{A,B}` 和 `E_{a0,b0}` 在有理数上是缩放同构的：

```text
X = d^2 x
Y = d^3 y
```

所以本轮把“同一条椭圆曲线”定义成：

```text
同一个 primitive 底型 (a0,b0)
```

并额外用 `j` invariant 做了一个更粗的核对。

新增工具：

```text
scripts/partner/giant_curve_repetition.py
tests/test_giant_curve_repetition.py
results/partner/giant_curve_repetition_summary.json
```

命令：

```bash
uv run python scripts/partner/giant_curve_repetition.py \
  --top 25 \
  --out results/partner/giant_curve_repetition_summary.json
```

giant component 结果：

```text
raw vertices:                  309,689
primitive curve classes:        19,224
j-invariant classes:            19,224
repeated primitive classes:      12,943
singleton primitive classes:      6,281
average vertices per primitive:  16.1095
largest primitive class:          1,605 vertices
```

普通话解释：

```text
是的，giant 里的节点会大量反复落到同一批 primitive 椭圆曲线底型上。

309,689 个 raw 节点压缩后只有 19,224 个 primitive curve classes；
平均每个底型出现约 16 个缩放版本。
```

但也不能说：

```text
整个 giant 主要由少数几条曲线支配。
```

因为 top 覆盖率是：

```text
top 10 primitive classes:     13,984 vertices =  4.52%
top 25 primitive classes:     27,274 vertices =  8.81%
top 50 primitive classes:     42,884 vertices = 13.85%
top 100 primitive classes:    64,560 vertices = 20.85%
top 500 primitive classes:   145,082 vertices = 46.85%
top 1000 primitive classes:  187,426 vertices = 60.52%
```

所以更准确是：

```text
giant 不是由一条或几十条曲线吃掉大部分节点；
它是由上万条 primitive 曲线底型组成的。

但这些底型不是一次性出现就消失；
绝大多数 raw 节点都处在某个重复出现的底型缩放族里。
```

复用规模分布：

```text
primitive class size >= 2:     303,408 vertices = 97.97%
primitive class size >= 5:     288,166 vertices = 93.05%
primitive class size >= 10:    269,818 vertices = 87.13%
primitive class size >= 20:    244,432 vertices = 78.93%
primitive class size >= 50:    198,456 vertices = 64.08%
primitive class size >= 100:   158,744 vertices = 51.26%
primitive class size >= 500:    46,991 vertices = 15.17%
primitive class size >= 1000:   16,332 vertices =  5.27%
```

top primitive 底型：

```text
(6,13):    1,605 scaled vertices
(11,45):   1,537
(22,35):   1,512
(7,18):    1,476
(25,91):   1,403
(7,32):    1,393
(5,26):    1,377
(27,50):   1,252
(5,33):    1,237
(13,64):   1,192
```

对比 non-giant 总体：

```text
non-giant vertices:              28,536
primitive curve classes:         21,657
average vertices per primitive:   1.3176
largest primitive class:             70
```

这很有解释力：

```text
giant 的核心特征不是“节点多”这么简单；
而是同一个 primitive 椭圆曲线底型在不同 d 下反复出现。

non-giant 更接近大量零散底型；
每个底型平均只出现 1.3 个 raw 节点。
```

`j` invariant 统计在当前数据中没有进一步合并：

```text
giant primitive classes = 19,224
giant j classes         = 19,224
```

所以当前窗口里，主要重复机制就是：

```text
同一个 primitive 底型的 D-scaling lift
```

不是额外大量不同 primitive 共享同一个 `j`。

这一小节给方向一一个更直接的回答：

```text
是，巨大连通块里确实大量反复对应到同一条椭圆曲线底型。

但不是“一条曲线生成整个 giant”，
也不是“少数几条曲线支配整个 giant”。

更像是：
  上万条正秩 primitive 曲线底型
  每条通过许多 d-scaling 版本反复出现
  再由 partner correspondence 连成一个大网。
```

## 6.8 primitive EC class graph：giant 是否只是 D-scaling 胖影子？

用户提出一个关键分水岭：

```text
不要再看 raw node graph。
把每个 raw 顶点 (A,B) 压到 primitive EC class prim(A,B)。
节点 = primitive 曲线底型。
边 = 只要两个 primitive 家族之间出现过 partner，就连边。

然后看：
  30 万 raw giant 是否压扁后仍然有 primitive giant？
```

普通话先说结果：

```text
是，primitive giant 仍然完整存在。

comp0 的 309,689 个 raw 节点压到 19,224 个 primitive EC class 后，
这 19,224 个 primitive class 仍然全部在同一个连通分量里。

所以 raw giant 不是单纯由 D-scaling 把少数曲线吹胖。
primitive 曲线族之间本身已经形成一张巨型 correspondence graph。
```

新增脚本：

```text
scripts/partner/primitive_ec_class_graph.py
tests/test_primitive_ec_class_graph.py
```

主命令：

```bash
uv run python scripts/partner/primitive_ec_class_graph.py \
  --edges results/partner/partner_full_bfs_edges.jsonl \
  --components results/partner/partner_full_bfs_components.jsonl \
  --component-id 0 \
  --out results/partner/primitive_ec_class_graph_comp0_1M_summary.json \
  --top 30
```

定义：

```text
raw edge:
  (A,B) -- (N_i,N_j)

primitive projection:
  prim(A,B) -- prim(N_i,N_j)

loop:
  prim(A,B) == prim(N_i,N_j)

cross edge:
  prim(A,B) != prim(N_i,N_j)
```

comp0-only primitive graph 结果：

```text
raw edges seen:                 350,868
raw edges used inside comp0:     331,803

primitive nodes:                 19,224
primitive edges:                 24,475
components:                           1
largest component size:          19,224 = 100%

circuit rank:                     5,252
triangles:                        3,357
transitivity:                    0.0591

2-core nodes:                     6,707  (34.89%)
2-core edges:                    11,958
2-core circuit rank:              5,252

3-core nodes:                     1,071   (5.57%)
3-core edges:                     2,360
3-core circuit rank:              1,290

loop raw edges:                     293
loop primitive classes:                2
cross raw edges:                 331,510
cross raw edge share:             99.91%
```

这个结果非常关键：

```text
如果 raw giant 主要是“同一个 primitive 家族内部靠 d 缩放转圈”，
那么 primitive 投影后应该出现大量 loop，或者图会塌成很多小块。

实际相反：
  loop 极少；
  99.91% raw 边跨 primitive family；
  19,224 个 primitive class 全部连在一起；
  2-core 仍有 6,707 个节点和 5,252 个独立环。
```

所以当前模型要改成两层：

```text
第一层：D-scaling 负责把每个 primitive class 变胖，
        解释为什么同一底型有许多 raw 节点、为什么高 k 可由清分母产生。

第二层：primitive correspondence 负责把不同 primitive class 接起来，
        解释为什么 giant 压扁后仍然是 giant。
```

top primitive degree：

```text
(91,990):     degree 106, weighted degree 1669
(693,2080):   degree 98, weighted degree 1519
(25,91):      degree 88, weighted degree 8121
(55,442):     degree 78, weighted degree 1689
(70,117):     degree 68, weighted degree 7293
```

注意 `(25,91)` / `(70,117)` 这类点的普通度不是最高，
但 weighted degree 极高，说明它们不是连接最多不同 primitive 邻居，
而是某些 primitive correspondence 被大量 raw 缩放边重复实现。

top primitive edge weights：

```text
(11,45) -- (22,35):     1470 raw edges
(7,32)  -- (22,35):     1372
(6,13)  -- (13,64):     1258
(5,26)  -- (25,91):     1125
(7,18)  -- (7,32):      1070
```

这给了下一个更细的问题：

```text
同一条 primitive correspondence 为什么会被这么多 d-scaling raw edge 重复实现？
这些 edge weight 是否由两个 primitive 曲线的 rational square-x 分母交集控制？
```

全 1M 图的 primitive 投影作为参照：

```text
primitive nodes:         35,670
primitive edges:         34,304
components:               6,921
largest component:       21,081 nodes = 59.10%
circuit rank:             5,555
2-core nodes:             7,200
3-core nodes:             1,112
```

全图 primitive giant 比 comp0 primitive giant 更大：

```text
comp0 primitive giant: 19,224 nodes
all-1M primitive giant: 21,081 nodes
```

这说明：

```text
raw 层的非 comp0 分量里，有些 primitive class 在 primitive 投影后
会接到同一个 primitive giant 上。

换句话说，raw graph 的窗口截断/缩放坐标限制，
会在 raw 层把一些东西切开；
但 primitive 层已经看到了更底层的连接趋势。
```

当前分水岭结论：

```text
primitive EC class graph 的 giant 存在，而且很强。

因此：
  30 万 raw giant 不是只靠 D-scaling 造成的胖影子；
  D-scaling 是放大器；
  primitive correspondence graph 才是更底层的骨架候选。

但这仍不是“无限性证明”。
下一步应比较 1M / 2M / 7M 的 primitive graph 是否持续增长，
以及 2-core / 3-core 是否随窗口稳定扩大。
```

## 7. 最短研究路线

如果只选一条最有性价比的路线：

```text
1. 选 3 个 primitive：rank 2、rank 3、rank 4 各一个。
2. 用 D-scaling + exact_concordant_pair 生成 d<=50000 的 k(d) 表。
3. 对每个 primitive 取 top 20 rational n，记录 denominator 和 MW 坐标。
4. 把 partner 边投影到 primitive 层，看是否出现少数固定模板。
5. 写成 “local MW lattice + scaling denominators + primitive correspondence” 模型。
```

这条路线的好处：

```text
它不试图一步证明 Harborth。
它先解释 30w giant component 为什么会长出来。
解释清楚后，再问 closure=0 到底是额外模障碍、height 障碍，还是别的结构。
```

## 8. 当前判断

方向一值得继续，而且应该升级为当前 partner graph 的主解释框架之一。

但它的正确形态不是：

```text
G_M = Mordell-Weil group
```

而是：

```text
G_M = elliptic-curve-family correspondence graph
      driven locally by Mordell-Weil lattices
      and globally amplified by D-scaling denominators.
```

普通话说：

```text
每个节点里面确实有椭圆曲线群；
整张图不是一个群，而是一张“曲线和曲线之间互相递交特殊点”的网。

图能持续变大，很可能不是偶然暴扫撞出来的；
当前模型是：正秩曲线给出有理点，放大倍数再把这些有理点变成整数点。
```

这解释了为什么会有巨型分量，也解释了为什么高 k 不等于高 rank。
下一步要做的不是再画更大图，而是把：

```text
primitive 底型
MW 坐标
rational n 分母
D-scaling
partner 边 primitive 投影
```

这五件事放到同一张表里。

## 9. primitive graph growth：1M / 2M / 7M 速度和增长实验

上面第 6.8 节只回答了一个静态问题：

```text
在 1M 窗口里，raw giant 压到 primitive 层后还在不在？
```

后续真正要问的是增长问题：

```text
随着窗口从 1M 到 2M 再到 7M，
primitive 层的 giant 是变弱、停住，还是继续增强？
```

如果 30 万 raw giant 主要只是 D-scaling 造成的胖影子，那么压到 primitive
层后，giant 占比应该不稳定，甚至可能逐渐稀释。

实际结果相反。

### 9.1 命令和本地结果文件

本轮用同一套命令重新跑了 1M、2M、7M：

```bash
uv run python scripts/partner/partner_full_bfs.py \
  --catalog results/multi_n/multi_concordant_N_max100000_fast.jsonl \
  --max-value <W> \
  --workers 10 \
  --chunksize 50 \
  --out-prefix results/partner/speedcheck_full_bfs_<label>_w10
```

然后把 raw edge 投影成 primitive EC class graph：

```bash
uv run python scripts/partner/primitive_ec_class_graph.py \
  --edges results/partner/speedcheck_full_bfs_<label>_w10_edges.jsonl \
  --components results/partner/speedcheck_full_bfs_<label>_w10_components.jsonl \
  --out results/partner/speedcheck_primitive_ec_graph_<label>_w10_summary.json \
  --gephi-out-dir results/partner/gephi_speedcheck_primitive_ec_<label>_w10
```

增长汇总保存在本地：

```text
results/partner/primitive_graph_growth_speedcheck_w10.csv
results/partner/primitive_graph_growth_speedcheck_w10.json
```

这些 `results/` 文件按仓库规则不进 git；worklog 记录关键数字和复现命令。

### 9.2 总表

```text
window  raw vertices  raw edges   raw giant   primitive nodes  primitive edges  primitive giant
1M          338,225    350,868      91.56%            35,670            34,304           59.10%
2M          689,604    729,764      95.98%            48,386            50,983           71.09%
7M        2,530,620  2,719,386      98.93%            96,864           113,599           87.46%
```

core 也一起增长：

```text
window  primitive 2-core nodes  primitive 3-core nodes  circuit rank  triangles
1M                     7,200                  1,112          5,555      3,552
2M                    11,873                  1,810          9,246      5,895
7M                    28,633                  4,390         22,586     14,392
```

速度：

```text
window  raw BFS time  primitive graph time  total time
1M            11.2s                11.5s       22.7s
2M            27.4s                17.7s       45.1s
7M           140.7s                42.4s      183.1s
```

普通话解释：

```text
现在算法已经够快。
7M 全流程大约 3 分钟，不再是半小时级别的实验。
```

### 9.3 这个实验说明什么

最重要的信号是：

```text
primitive giant share:
  1M: 59.10%
  2M: 71.09%
  7M: 87.46%
```

这说明：

```text
raw giant 不是一压缩就消失。
相反，窗口越大，primitive 层自己的 giant 越占主导。
```

这把模型又推进了一步。

之前的模型：

```text
D-scaling 把 primitive 曲线变胖，
所以 raw graph 有 giant。
```

现在更准确：

```text
D-scaling 是放大器；
primitive correspondence graph 本身也在形成 giant；
raw graph 是 primitive skeleton 被 scaling lift 后的结果。
```

还有一个重要细节：

```text
primitive 2-core:
  7,200 -> 11,873 -> 28,633

primitive 3-core:
  1,112 -> 1,810 -> 4,390
```

如果 giant 只是树状地越接越长，core 不会这样同步变厚。
core 变厚说明 primitive 层内部的环和多路径也在增加。

普通话说：

```text
这不像一串偶然接起来的长链。
更像一张越长越密的底层交通网。
```

### 9.4 这还不能说明什么

这个实验仍然不能说：

```text
已经证明 infinite primitive giant 存在。
```

原因很简单：

```text
1M / 2M / 7M 都是有限窗口。
```

更安全的说法是：

```text
有限扫描强烈支持 primitive 层有真实骨架，
并且这个骨架随窗口扩大正在吸收越来越多 primitive class。
```

也不能说：

```text
已经找到一个一行公式，可以生成所有 pair。
```

目前更像是找到了“机器”的轮廓：

```text
primitive 正秩椭圆曲线
=> rational square-x 点池
=> denominator 被 d 清掉
=> 产生 integer N
=> 形成 raw partner edges
=> 投影后得到 primitive correspondence graph
```

所以它不是质数那种“一个闭式公式吐出第 n 个对象”。
更像筛法：

```text
有生成机制；
有过滤条件；
有增长规律；
也可能有只能统计描述的部分。
```

### 9.5 下一步更像研究什么

当前最有价值的后续问题不是继续单纯把窗口推大，而是分层拆机制。

第一条：增长律。

```text
继续补 4M / 10M / 15M。
看 primitive nodes、edges、giant share、2-core、3-core 是否接近幂律或对数修正。
```

可能结果：

```text
giant share 继续趋近 100%：
  primitive 层可能有一个主骨架。

giant share 稳定在 90% 左右：
  主大陆存在，但还有稳定孤岛族。

core 增长明显慢于节点：
  giant 主要靠树枝扩张。

core 与节点同步增长：
  底层 correspondence 越来越像真实算术网络。
```

第二条：rank-degree。

现在 top40 小样本给出：

```text
rank=1: n=3,  average primitive degree = 6.00
rank=2: n=26, average primitive degree = 16.85
rank=3: n=11, average primitive degree = 38.82
```

这只是 top40，不是全体。
下一步要扩大到几百或几千个 primitive。

可能结果：

```text
rank 越高，degree 越高：
  MW rank 可能控制 distinct primitive neighbors。

rank 和 degree 关系弱：
  真正控制边的是 denominator、局部同余或 square-x 截面。

rank 控制度，denominator 控制权重：
  这会是很漂亮的双层模型。
```

第三条：edge weight。

现在知道：

```text
primitive edge 是否存在
```

还要解释：

```text
为什么某些 primitive edge 被上千条 raw edge 重复实现？
```

可能机制：

```text
两端 primitive rational n 池的 denominator 交集
+ 同一个 d 同时清掉多批分母
+ raw window 对 d 的截断
```

第四条：孤岛。

primitive giant 越来越大，但仍然有很多小 component。
这些小 component 可能有两种命运：

```text
窗口继续变大后并入 giant；
或者因为某些同余/局部条件永远自闭合。
```

所以 island 不该被丢掉。
它们可能正是隐藏不变量最容易露出来的地方。

## 10. 当前收束结论

本轮方向一可以收成一句话：

```text
partner graph 的巨大分量，不只是 D-scaling 放大的假象；
压到 primitive EC class 层以后，giant 仍然存在，而且 1M -> 2M -> 7M
越来越强。
```

更具体：

```text
D-scaling:
  解释同一 primitive 底型为什么能产生很多 raw 节点和高 k。

primitive correspondence:
  解释不同 primitive 底型为什么会连成一张越来越大的图。

Mordell-Weil group:
  提供每个 primitive 底型内部的 rational square-x 点来源。
```

所以后续不必执着于“一条公式生成所有 pair”。
更现实、也更可能有数学内容的目标是：

```text
找到一套生成和解释机制：
  哪些 primitive 曲线产生点；
  哪些 denominator 被 d 清掉；
  哪些 primitive family 之间出现 correspondence；
  这些 correspondence 如何长成 giant/core。
```

这条路如果走通，得到的东西可能不像一个闭式公式，
但会像一个“算术筛法 + 图增长律 + 局部椭圆曲线群机制”的组合模型。
