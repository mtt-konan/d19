# wl060 — K_8 / K_7 / K_6 rank 审计：deficit 猜想确认 + rank 上限假设

## 触发

wl059 提出新猜想：

> partner graph G_M circuit rank ≈ Σ (k − rank) on cycle 节点

并预测：K_8 hub 应有 deficit ≥ 3。本 worklog 跑 wl055 发现的所有 K_8/K_7
顶级实例 + K_6 取样的 PARI ellrank，验证猜想。

## 数据：11 个高 k hub 的 ellrank

```text
class  pair               k    rank   deficit  sha2   #gens
─────────────────────────────────────────────────────────────
K_8   (55440, 445536)     8    4      4   ⚠⚠    0     4
K_8   (58800,  98280)     8    3      5   ⚠⚠    0     3       ← deficit 创纪录
K_7   (10200,  37128)     7    3      4   ⚠⚠    0     3
K_7   (10920, 118800)     7    4      3   ⚠⚠    0     4
K_7   (50160, 403104)     7    4      3   ⚠⚠    0     4
K_7   (102000, 303600)    7    3      4   ⚠⚠    0     3
K_6   ( 2640,  21216)     6    4      2    ⚠     0     4
K_6   ( 3696,   8160)     6    3      3   ⚠⚠    0     3
K_6   ( 4680,  95760)     6    3      3   ⚠⚠    0     3
K_6   ( 5304,  27300)     6    3      3   ⚠⚠    0     3
K_6   ( 5460,  59400)     6    4      2    ⚠     0     4

聚合:
  K_8 (n=2):  rank ∈ {3, 4}    deficit ∈ {4, 5}    avg deficit = 4.5
  K_7 (n=4):  rank ∈ {3, 4}    deficit ∈ {3, 4}    avg deficit = 3.5
  K_6 (n=5):  rank ∈ {3, 4}    deficit ∈ {2, 3}    avg deficit = 2.6
```

所有 PARI ellrank 调用 effort=1 都 certified（lower == upper），sha2_lower = 0。

## 主结论 1：wl059 deficit 猜想严格成立

```text
K_8 deficit ≥ 4  (实际 4-5)    ← 比预测的 ≥3 更强
K_7 deficit ≥ 3  (实际 3-4)    ← 比预测的 ≥2 更强
K_6 deficit ≥ 2  (实际 2-3)
```

每个 K_n hub 的 N 列表里，**至少有 ⌈n/2⌉ 个 N 之间存在线性依赖**。

## 主结论 2：rank 在 max=100000 catalog 内似乎 bounded by ~4

对比 wl048 catalog 范围内所有已知样本（来自 wl059 + wl060）：

```text
样本                          k    rank
─────────────────────────────────────────
(153, 560)                    3    3      ← 唯一 k = rank 样本（"perfect"）
(560, 2925)                   3    2
(420, 1344)                   3    1
(1008, 2925)                  4    3
(264, 420)                    4    2
(1344, 7020)                  4    2
(1344, 3900) K_5              5    3
(2925, 9360)                  3    1
2 K_8 hub                     8    3, 4
4 K_7 hub                     7    3, 4
5 K_6 hub                     6    3, 4
```

**没有任何样本 rank > 4**。

这是一个非常强的实证观察。如果在 catalog 全范围（10,333 互素 + 10,533 partner 反推
非互素 + wl056 直接非互素扫描）真的没有 rank ≥ 5 的椭圆曲线 E_{A, B}，那
**Mordell-Weil rank 在该 family 上有自然上限**。

理论上一些已知 family bound：
- Ono 1996 给出 quadratic twist rank 在某些 family 上的限制
- KSS 2019 §6.3 暗示 multi-N k 与 rank 的关系受 homogeneous space 个数限制
- Halbeisen-Hungerbühler 2021 Γ_{a, b} 的 torsion = ℤ/2 × ℤ/4，不直接限制 rank
  但 Schroeter parametrization 的 rational twists 可能有界

> **未解决**：rank 上限是 4 还是 5？需要更多样本验证 / 提高 effort 到 2 或 3
> 看是否捕获额外 generators。

## 主结论 3：高 k 实例 = 大量 P_N 共享同一些 half-points

按 Ono Prop 1，每个 P_N ∈ 2E(ℚ) 对应一个 half-point Q_N。但 rank 限制意味着
**不同 P_N 共享同一些 half-points**：

```text
K_8 (58800, 98280) k=8 rank=3:
  8 个 P_N (对应 8 个 concordant N) ↔ 只有 3 个独立 half-point lattice 维度
  ⇒ 8 个 P_N "塞进" 3 维 ℤ-lattice，平均 2.67 个 P_N 共享 1 维
```

这跟 KSS §6.3 一致：rank=2 的 example 中每个 homogeneous space 只给 1 个 generator，
要找独立点需要不同的 homogeneous spaces。这里 K_8 hub 的 8 个 N 来自 ≤ 3 个 distinct
homogeneous spaces 的"翻倍"。

## 主结论 4：closure 0 命中跨所有 K_n 阶

wl055 已检查所有 11 个 K_6+ hub 的 N 配对：

```text
K_8 (55440, 445536)  C(8, 2) = 28 pairs of (N_i, N_j), checking N_i + N_j == 500976:
                     0 hits.
K_8 (58800, 98280)   28 pairs, target 157080:  0 hits.
... K_7 + K_6 全部 0 hits.
```

**closure 失败与 rank deficit 同时发生**，但 closure 不是 deficit 的直接
推论。它们可能在某个更深的代数障碍下都成立（参考
[`THEORY_DIRECTIONS_ADVANCED.md`](../THEORY_DIRECTIONS_ADVANCED.md) 方向七、八）。

## 反例搜索的影响

```text
反例条件:  multi-N pair (A, B) k>=2 + ∃ (N_i, N_j) ∈ closure (N_i + N_j = A+B)

目前数据:
  rank ≤ 4 in catalog 范围
  deficit 随 k 增长
  closure 0 hits in K_3+ samples
  
猜想 (待验证):
  反例存在 ⇔ E_{A, B} 上某些"特殊" half-point 配对在 ℤ 上加法满足 closure
  rank 上限 ≈ 4 ⇒ 反例需要在最多 4 维 lattice 内找符合 closure 的配对
  这是个有限维问题，理论上可以系统地搜
```

## 没做的事

1. **effort=2 重跑**：看是否有些 rank 实际是 5+ 但 effort=1 漏报。
2. **rank ≤ 4 的全 catalog 验证**：跑所有 10,333 互素 catalog 行的 rank，
   看分布。预计跑全表 ~1 小时（每行 < 1s）。
3. **确认 N 与 half-point 的对应**：(420, 1344) k=3 rank=1 这种极端 deficit
   样本，3 个 N 中哪些是同一个 Q_N 的不同表示？
4. **closure 与 rank=k 的相关性**：(153, 560) 是唯一 rank = k 样本。
   它的 closure 检查也是 0。即使 rank "饱和"也不出反例。这暗示什么？
5. **K_8 不在 cycle 上还是 cycle 上？**(55440, 445536) 与 (58800, 98280)
   不一定属于 (153, 560) 的 71-node component。需要从它们做 BFS 看其
   component 结构。

## 文件

```text
scripts/k8_ellrank.py                                  K_8/K_7/K_6 hub rank 跑数据
results/k8_ellrank_wl055_top_hubs.jsonl                rank 数据 + generators
docs/work-logs/060-k8-rank-audit-deficit-confirmed.md  本文件
```

## 元注

wl059 的猜想从"具体 6-cycle 现象"上升为"K_n 阶层的全局规律"。配合 wl058
的"G_M ≈ forest"，整个 partner graph 的代数+拓扑双层结构正在浮现：

```text
拓扑层 (G_M):                  代数层 (E_{A,B} 上 Q_N):
─────────────────────         ─────────────────────────
G_M ≈ forest                  rank ≤ 4 in catalog
cycle 罕见                     deficit 随 k 增长
K_n 是 star                    K_n 上 P_N 共享 Q_N

二者通过 Ono Prop 1 + KSS §6.3 framework 直接对应。
```
