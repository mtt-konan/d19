# wl096 — G_M 三层分解：comp0 巨型分量 vs 截断断枝 vs 永久独立孤岛（7M 验证）

## 触发

用户问了两个相关问题：

1. 要不要跑更大的 BFS，看那个巨型分量（comp0）是**无限还是有限**？
2. 除了 comp0，为什么还有那么多**又小又多**的有限分量？它们是不是都是 comp0 的分支，
   只有 K_2 才可能真的在 comp0 之外？如果能找规律把巨型分量剔除，可筛选的 pair 就少很多，
   反例也许更容易找。

本 worklog 回答这两个问题：先用**现有 1M BFS 数据 + wl095 的精确因子核**把全部非 comp0
分量做结构分类（零额外 BFS），再**重跑 7M BFS**在尺度上验证分类预测。

## 方法：用精确因子核给分量"贴标签"

partner identity 这条边 `(A,B)—(N_i,N_j)`（其中 N_i,N_j ∈ concordant_N(A,B)）在数学上
**与坐标大小无关**，永远存在；但 `partner_full_bfs.py` 只收坐标 ≤ `max_value=W` 的顶点。
于是判定一个分量是否"被窗口截断"很直接：

> 对分量里每个顶点 (A,B)，用 wl095 的 `exact_concordant_pair(A,B)`（枚举 A²/B² 因子对，
> **对 N 不设上界**）拿到全部 concordant N，再看是否存在伙伴对 (N_i,N_j) 坐标 > W。

- 存在 ⟹ **branch（断枝）**：分量在窗口外还在延伸，是 comp0 在更大窗口下的未来分支。
- 不存在 ⟹ **island（孤岛）**：分量在 partner 关系下**封闭**，是无限图 G_M 的一个
  **货真价实、永久独立**的连通分量（放大窗口也不会并入任何东西）。

> 证明 island 永久独立：untruncated 意味着该分量所有顶点的全部伙伴坐标都 ≤ W，且这些伙伴
> 都已在窗口内 BFS 到、属于同一分量（极大连通）。由 partner 对称性，任何 comp0 顶点也不可能
> 以该孤岛顶点为伙伴（否则那条边在窗口内、两者同分量，矛盾）。故孤岛与 comp0 无边，永不合并。

脚本：`scripts/partner/comp0_island_analysis.py`（分类 + closure 检查）。

## 1M 数据的三层分解

输入 `results/partner/partner_full_bfs_components.jsonl`（W=1M，9580 分量，338225 顶点）：

| 层 | 分量数 | 顶点数 | 说明 |
|---|---|---|---|
| **giant (comp0)** | 1 | 309,689 | 92%，独占全部高 k（实测度数到 K_9/K_10） |
| **branch（截断断枝）** | 620 | 5,647 | max_k 3→8，**全部被 1M 截断**，预测放大窗口并入 comp0 |
| **island（永久孤岛）** | 8,959 | 22,889 | 自闭合，partner 封闭，**永不并入 comp0**；max_k 只到 5 |

branch / island 按 max_k 细分：

```
 branch/K_2  307 comps   307 v     island/K_2  7930 comps 15860 v
 branch/K_3  150 comps   420 v     island/K_3   865 comps  4380 v
 branch/K_4   99 comps  1292 v     island/K_4   140 comps  2033 v
 branch/K_5   44 comps  1172 v     island/K_5    24 comps   616 v
 branch/K_6   14 comps  1311 v
 branch/K_7    5 comps  1110 v
 branch/K_8    1 comp     35 v
```

**对用户猜想的修正**：

- ✅ **高 k 被 comp0 垄断**：所有 k≥6 的非 comp0 分量都是 branch（截断），没有一个是永久孤岛。
  大的中/高 k 分量（comp1 size 473 K_6、comp2 471 K_7、comp3 393 K_7 …）确实是 comp0 的断枝。
- ❌ **"只有 K_2 在 comp0 外"偏强**：永久孤岛里除了 7930 个 K_2，还有 **1029 个货真价实的
  K_3/K_4/K_5 自闭合孤岛**（最大 size 83 的 K_4 hub (4536,15300)；多个 size 50–71 的 K_5，
  如 hub (1344,3900)→{560,1792,2925,7105,9360}）。它们整个 partner 轨道坐标都很小、完全自闭合。

**closure 检查**：对全部 8959 个永久孤岛扫 `N_i+N_j == A+B`，**0 命中**（与 wl063 对 comp0
全图的 0 命中一致）。

## 7M BFS 验证

`partner_full_bfs.py --max-value 7000000`（2 worker，120 轮，1348.6s）：

| | 1M | 7M |
|---|---|---|
| vertices | 338,225 | 2,530,620 |
| edges | 350,868 | 2,719,386 |
| components | 9,580 | 9,493 |
| **giant size** | **309,689 (92%)** | **2,503,583 (98.9%)** |
| 最大的非 giant 分量 | 473 | 144 |

把 1M 的每个非 comp0 分量按 branch/island 分类，再看其顶点落进 7M giant 的情况
（`scripts/partner/verify_window_merge.py`）：

```
layer/max_k : components / fully_merged_into_7M_giant / verts_in_giant
 branch/K_2  307 /  11 /   11of307
 branch/K_3  150 /  10 /   38of420
 branch/K_4   99 /  33 /  520of1292
 branch/K_5   44 /  18 /  616of1172
 branch/K_6   14 /   8 / 1056of1311
 branch/K_7    5 /   5 / 1110of1110   <- 全并入
 branch/K_8    1 /   1 /   35of35     <- 全并入
 island/K_2 7930 /   0 /    0of15860  <- 0 泄漏
 island/K_3  865 /   0 /    0of4380   <- 0 泄漏
 island/K_4  140 /   0 /    0of2033   <- 0 泄漏
 island/K_5   24 /   0 /    0of616    <- 0 泄漏
```

最大的 11 个非 comp0 分量（size≥90），10 个在 7M 完全并入 giant：

```
id=1 size=473 K_6 -> ALL      id=7  size=113 K_7 -> ALL
id=2 size=471 K_7 -> ALL      id=8  size=109 K_6 -> ALL
id=3 size=393 K_7 -> ALL      id=9  size=104 K_5 -> ALL
id=4 size=155 K_6 -> ALL      id=10 size=102 K_5 -> ALL
id=5 size=143 K_6 -> ALL      id=11 size= 95 K_7 -> ALL
id=6 size=121 K_6 -> 0/121 (bridge 坐标 > 7M，仍待并)
```

**结论**：

1. **island 永久独立性 100% 验证**：8959 个孤岛的 22889 个顶点，**0 个**泄漏进 7M giant。
   untruncated ⟺ 永久独立，在 7M 尺度上对全部 4 个 k 类完全成立。
2. **branch 单调并入 comp0，且高 k 优先**：K_7（5/5）、K_8（1/1）全并；K_6 8/14；越往低 k
   并入越少（K_2 只 11/307）。原因：高 k hub 伙伴结构更丰富，桥接坐标更靠近窗口；低 k 断枝
   的桥接坐标更远，要更大窗口才并入。这是 percolation giant component 随阈值生长的标准图像。
3. comp0 占比 92% → 98.9%，最大非 giant 分量 473 → 144；"巨型分量随窗口生长、吞并断枝"得到
   直接确认（而**有限 BFS 永远证不了"无限"**——只能看趋势；G_M 顶点集无限性已由 wl085
   D-scaling 解析给出，无需 BFS）。

## 无上限 BFS 直接验证孤岛封闭（回应"即使窗口极大"）

前面的 island 判据是**逐顶点**检查（每个顶点的完整伙伴对坐标都 ≤ W）。为把它升级成**与窗口
无关的直接证明**，`scripts/partner/verify_islands_unbounded.py` 对每个 island **不设任何
max_value 上限**做 BFS：从其顶点集出发，用完备因子核 `exact_concordant_pair`（完全分解
A²/B²，每个顶点的 concordant 集是**整个有限集**，无上界）扩展，确认 BFS **恰好收敛回原顶点集**、
绝不外溢（设 `len(S)*20+200` 的防爆上限，超出即记为泄漏）。

```
islands tested (unbounded BFS, NO window cap): 8959
  closed to EXACTLY original vertex set: 8959
  leaked / grew beyond original:         0
  global max coordinate ever reached:    997101  (< window 1,000,000)
```

**全部 8959 个孤岛在无上限 BFS 下都恰好闭合回自己**，0 外溢；所有孤岛 BFS 触及过的**全局最大
坐标仅 997,101 < 1M**。这给出确定性回答：孤岛不是"≤7M 的观察"，而是无限图 G_M 的真正有限
连通分量——从任何孤岛顶点出发、用**任意上限（含 ∞）**做 BFS 都走不出去，因为每个顶点的伙伴集
固定且有限、早被完备核枚举完，"窗口极大"不会冒出新伙伴。结果存
`results/partner/island_unbounded_bfs.json`。（注：这只断言**已发现的**孤岛封闭；更大窗口仍会
出现**新的、更大的**孤岛，那是另一回事。）

## 对"剔除 comp0 缩小反例搜索"策略的判断

- ✅ **可行的部分**：永久孤岛集**可按 pair 廉价识别**（给定 (A,B) 算精确 concordant 集、
  看伙伴对是否都留在窗口内即可判定 island/branch），**不需要建全图**。剔掉 comp0 + 断枝，
  待筛顶点砍掉 ~99%。
- ⚠️ **要诚实的部分**：(1) closure 在孤岛与 comp0 上**同样是 0**，没有证据反例偏爱孤岛——
  剔 comp0 只砍**数量**、不抬**每个 pair 的命中率**（closure 是加法巧合 N_i+N_j=A+B，与乘法
  的分量结构正交，见 wl086）。(2) 孤岛集随窗口也在增多，不是有限可穷尽集。
- 🎯 **真正的杠杆在"证明"而非"撞运气"**：孤岛（k≤5、小、自闭合、结构有界）是能用**有限/
  有界论证直接 KO** 的那部分；comp0 是无限高 k 的硬骨头。把空间切成"易证的孤岛 + 难的
  comp0"是合理的证明分解，对接 A.9 §8.6（非互素腿反例在约化对上不可见）那块最终缺口。

## 产物

- `scripts/partner/comp0_island_analysis.py` — 单窗口三层分类 + closure 检查
- `scripts/partner/verify_window_merge.py` — 两窗口对比（断枝并入 / 孤岛持存 / 按 k 并入率）
- `scripts/partner/verify_islands_unbounded.py` — 无上限 BFS 验证孤岛恰好闭合（与窗口无关）
- `results/partner/comp0_island_analysis_1M.jsonl` / `_summary.json`
- `results/partner/window_merge_1M_7M.json`
- `results/partner/island_unbounded_bfs.json`
- `results/partner/partner_full_bfs_7M_summary.json` / `_run.log` /
  `_components_trimmed.jsonl`（giant 的 250 万顶点列表已剔除，仅留 metadata + 全部小分量；
  完整 `_components.jsonl`(48MB)/`_edges.jsonl`(132MB) 因体积过大不入库）

## 一句话

G_M = 一个随窗口生长、吞并断枝的巨型分量 comp0（垄断全部高 k）+ 一批永久独立的小孤岛
（自闭合、max_k≤5、closure 恒 0）。用户"大分量是 comp0 分支"的直觉对（高 k 全是断枝，
7M 验证 10/11 大断枝并入），但"只有 K_2 在外"偏强（存在 K_3/K_4/K_5 自闭合孤岛）。
"剔除 comp0"作为**工程筛选**可行、作为**证明分解**才是真价值，但不改变 closure 恒 0 的事实。
