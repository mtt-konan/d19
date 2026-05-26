# wl059 — (153, 560) 6-cycle 的代数解释：partner cycle ≡ Mordell-Weil 线性依赖

## 触发

wl058 BFS 发现 G_M（partner graph）近似森林：(264, 420) 严格 tree，(153, 560)
71 节点仅 1 个 6-cycle。用户问"6-cycle 的代数含义是什么"。

本 worklog 用 PARI ellrank 量化 cycle 上 6 个节点的椭圆曲线 rank，发现一个清晰的
"rank 短缺"模式，给出 cycle 的代数解释。

## 工具

`scripts/cycle_ellrank.py` 用 `compute_rank(A, B, effort=1)`（PARI 的
`ellrank` 包装，见 `src/.../concordant/analysis.py:108`）对 cycle 上 6 个节点 +
2 个对照节点跑 ellrank，输出 `(rank_lower, rank_upper, sha2_lower, generators)`。

## 数据：cycle 节点的 rank 全谱

```text
pair                k    rank    k − rank    sha2    #gens
────────────────────────────────────────────────────────────
(560, 2925)         3    2       1            0       2
(420, 1344)         3    1       2  ⚠         0       1
(1008, 2925)        4    3       1            0       3
(1344, 7020)        4    2       2  ⚠         0       2
(2925, 9360)        3    1       2  ⚠         0       1
(1344, 3900) K_5    5    3       2  ⚠         0       3
────────────────────────────────────────────────────────────
                 Σ k = 22         Σ rank = 12         deficit = 10

参考点（不在 cycle 上）：
(153, 560)          3    3       0            0       3   ← 完美 (k = rank)
(264, 420) tree     4    2       2  ⚠         0       2
```

所有 8 个 rank 都是 PARI certified（lower == upper）。所有 sha2_lower = 0
（在该 effort 下没有 Sha[2] 见证）。

## 关键观察

### 1. cycle 上 6 个节点 rank 总和 = 12，远小于 k 总和 22

deficit = Σ(k − rank) = 10。这意味着 cycle 上**每个节点都有 N 之间的线性依赖**，
平均每个节点损失 10/6 ≈ 1.67 个 rank 维度。

### 2. cycle 上有 4 个节点 deficit ≥ 2

```text
(420, 1344) k=3 rank=1   →  3 个 N 只在 1 维子格上
(1344, 7020) k=4 rank=2  →  4 个 N 只在 2 维子格上
(2925, 9360) k=3 rank=1
(1344, 3900) k=5 rank=3  →  5 个 N 只在 3 维子格上 (K_5 中心 hub)
```

而 cycle 上"过渡型"节点（k=3 deficit=1, k=4 deficit=1）：

```text
(560, 2925)  k=3 rank=2 deficit=1
(1008, 2925) k=4 rank=3 deficit=1
```

deficit 高的节点更靠近 K_5 hub，deficit 低的节点更靠近 cycle 边缘。这暗示
**rank deficit 沿 cycle 累积**。

### 3. 对照点 (153, 560) k=3 rank=3 完美：每个 N 给独立 generator

```text
(153, 560) N = [204, 420, 3900]
           rank = 3, gens = (-242760, ...), (-104040, ...), (3 个独立)
```

这是 BFS 起点，不在 6-cycle 上。**说明 cycle 与 rank-deficit 直接相关**：
cycle 节点都有 deficit ≥ 1，cycle 外节点可能 deficit = 0。

## 代数解释（按 Ono 1996 + KSS 2019 framework）

### Ono Prop 1 重述

对 multi-N pair (A, B) 的每个 concordant N，对应 E_{A, B} 上的 square-x 点

```text
P_N = (N², N · √(N²+A²) · √(N²+B²))
```

由于 N², N²+A², N²+B² 三项全是平方（concordant 条件本身），P_N 自动属于 2E(ℚ)。
故存在 half-points Q_N 使 2 Q_N = P_N。

**Q_N 是椭圆曲线 E 上的"真生成元候选"**，而 P_N 已经被 2 整除。

### rank vs k 的关系（基于 KSS §6.3）

| (A, B) 实例 | k | rank | 解释 |
|---|---|---|---|
| (153, 560) | 3 | 3 | 3 个 Q_N 在 E(ℚ)/torsion 中独立 → rank ≥ 3 ✓ |
| (420, 1344) | 3 | 1 | 3 个 Q_N 在 E(ℚ)/torsion 中**只张成 1 维** → 2 个独立线性关系 |
| (1344, 3900) | 5 | 3 | 5 个 Q_N 在 E(ℚ)/torsion 中张成 3 维 → 2 个独立线性关系 |

**rank deficit = k − rank = 不同 Q_N 之间的独立线性关系个数**。

### partner cycle ≡ Mordell-Weil 线性关系的拓扑表达

```text
猜想 (wl059):
  partner graph G_M 上每条 cycle ↔
  cycle 节点对应的 Q_N 之间的非平凡线性依赖关系（在某个 E_{A,B} 群里）

更精确的对应：
  G_M 上 (A, B) ↔ (X, Y) 边 = X, Y ∈ N(A, B) 的对子选择
  cycle 闭合 = 沿 cycle 的对子选择形成 closed walk in MW 群
  cycle 长度 ≥ 6 (in 71 节点 (153, 560) component)
```

cycle 上每节点 deficit ≥ 1 ⇒ 每节点对 cycle 闭合贡献 1 个独立线性关系，
6 个节点 × 平均 1.67 deficit = 10 个 总线性关系，足以让 6 步走回起点。

### 为什么 (264, 420) tree 上 (264, 420) k=4 rank=2 deficit=2？

(264, 420) 不在 cycle 上 (其 component 是严格 tree)，但仍有 deficit=2。
这说明 **rank deficit 与 cycle 不是完全等价的** —— deficit 反映 Mordell-Weil
内部线性依赖，cycle 反映 G_M 拓扑闭合。两者高度相关但不等同。

可能 (264, 420) 的 28 节点 tree 内部仍然存在"代数依赖"，只是没体现为 G_M 拓扑
cycle —— 比如 (264, 420) 子图内 4 个 N 的 Q_{N_i} 间存在 1 个线性关系，但这关系
没有"绕一圈"回到 (264, 420)（因为它们都通过 (264, 420) 这个唯一的 hub 相连）。

要确认这一点，需要追踪 (264, 420) 上 4 个 N 之间的具体线性关系。等于 KSS §6.3
的"哪个 generator 是哪个 N 的 doubling"分析。

### 对反例搜索的影响

```text
Harborth 反例条件 = (A, B) k≥2 multi-N + N₁ + N₂ = A + B (closure)

观察:
  closure = N₁ + N₂ = A + B 是 ℤ 上的加法关系
  rank deficit = Q_{N_i} 在 E(ℚ) 上的乘法依赖
  两者结构不同

⇒ rank deficit 不直接 imply 或排除 closure
⇒ 反例可能在 deficit = 0 (强独立) 节点上更稀有
   也可能在 deficit ≥ 2 (依赖密集) 节点上更稀有 — 取决于 closure 的代数本质
```

## 实证：generators 坐标透露什么

ellrank 输出的 generators 都有**负 X 坐标**：

```text
(560, 2925) gens:  X = -2839200, 238875
(420, 1344) gens:  X = -1411200
(1008, 2925) gens: X = -3832920, -1289925, ...
(1344, 3900) gens: X = -6814080, -2293200, ...
```

负 X 落在 [-A², 0] ∪ [-B², -A²]（在 2-torsion 之间），不是 X = N²（square-x）。
这跟 Ono Prop 1 一致：**P_N 不是 generator，generator 是 P_N 的 half-point**。
PARI ellrank 返回的就是这些 half-point Q_N（或它们的代表元）。

## 与 wl058 的连接

wl058 末尾留了一个钩子：

> "(153, 560) 6-cycle 经过 K_5 hub。是否所有 G_M cycle 都经过某个 K_n hub (n≥3)？
>  是否对应 Mordell-Weil 群上的某种关系？"

wl059 的回答：

> 6-cycle 上 6 个节点全部 deficit ≥ 1（rank < k），其中 K_5 hub (1344, 3900)
> deficit = 2（最高之一）。**cycle 与 rank deficit 高度相关**，但不严格等价
> （tree 节点也可能 deficit > 0）。

## 没做的事 (留给后续 worklog)

1. **追踪具体线性关系**：对 (420, 1344) 求 3 个 Q_N 之间的具体整数关系
   c₁ Q_{560} + c₂ Q_{1008} + c₃ Q_{2925} = 0 in E(ℚ)/torsion。
   需要把 PARI 返回的 generator 与 Q_{N_i} 对应起来。
2. **对 (264, 420) 28-tree 跑全部节点 rank**：看 deficit 在 tree 上如何分布。
3. **K_8 实例 (55440, 445536) 与 (58800, 98280) 的 rank**：
   wl055 钩子。预期 rank 5-7 之间（k=8 但有 deficit）。
4. **更大 BFS** 找更长 cycle (8-cycle, 10-cycle?)，看 deficit 是否随 cycle 长度增长。
5. **closure 与 rank deficit 的相关性分析**：所有已知 multi-N pair 中
   deficit 分布与 closure failure 是否有规律。

## 文件

```text
scripts/cycle_ellrank.py                        cycle 节点 ellrank 跑数据
results/cycle_ellrank_wl058_6cycle.jsonl        rank 数据（含 generators）
docs/work-logs/059-cycle-algebra-mw-rank-deficit.md  本文件
```

## 元注

这次工作把 wl058 发现的 G_M 拓扑结构（partner cycle）和 wl057 理论文档里
讨论的 Ono / KSS / MW framework 第一次连接起来。新的猜想：

```text
"partner graph G_M 的 circuit rank ≈ Σ 节点 (k − rank)"
                                       cycle 上节点
```

这是个**新的、可证或可证伪的命题**，比 wl058 的"G_M 近似森林"观察更深一层。
但要严格验证，需要更多 BFS component + rank 数据。
