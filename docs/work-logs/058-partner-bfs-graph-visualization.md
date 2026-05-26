# wl058 — Partner Graph BFS 可视化：发现 G_M 近似森林

## 触发

用户在 wl057 理论 grounding 完成后建议：

> "要不先走用 BFS 方式在一定范围内画图？之前画的图走成了 K_n，但是用 BFS 会展开
> 的更全面，说不定 BFS 是更大的一个结构，也有可能根节点只有一个"

也就是说：之前 wl054-055 的 K_n 枚举是局部缩影，BFS 才是 G_M（partner graph）
的原生探索方式。需要看看 G_M 的全局结构。

## 工具

```text
scripts/partner_bfs.py            从给定根节点 (A, B) 出发做 BFS，
                                  限定 max_value 上界 + max_visited 截断
scripts/partner_bfs_analyze.py    分析多个 BFS 输出：
                                  1) 比较节点集合（是否相交）
                                  2) closure 检查 (N_i + N_j == A + B)
                                  3) 输出 graphviz .dot
scripts/partner_bfs_plot.py       matplotlib + networkx 画图
                                  (kamada_kawai / spring layout)
```

新增项目依赖（[dependency-groups.viz]）：

```toml
[dependency-groups]
viz = ["networkx", "matplotlib", "scipy"]
```

调用：`uv run --group viz python scripts/partner_bfs_plot.py ...`

## 数据：两个根节点的 BFS

### `(264, 420)` 出发：max_value=10000 与 100000 完全一致

```text
max_value=10000      28 节点  54 条 directed edges (= 27 undirected)
max_value=100000     28 节点  54 条 directed edges (= 27 undirected)
```

**这个连通分量在 max=10000 时已完全闭合**。把上界推到 100000 没有任何新节点出现。
BFS 探索到 depth=8，全部 partner 邻居都在该 28 节点集合内部循环。

### `(153, 560)` 出发：max_value=10000 与 100000 显著不同

```text
max_value=10000      46 节点  深度达到 10
max_value=100000     71 节点  深度达到 ≈ 10
```

后者比前者多 25 节点，说明 max=10000 还没闭合。但 71 节点已经覆盖了几个高 k hub，
完全闭合需要更大的 max_value。

### 节点集合的关键观察：两个连通分量**完全不相交**

```text
(264, 420) ∩ (153, 560)：0 共同节点
```

这**否定**了用户的"也有可能根节点只有一个"猜想。partner graph G_M 至少有两个
独立的 connected component。

## 拓扑发现：G_M 近似森林

```text
(264, 420)  28 节点 27 边  →  严格 tree（n−1 边，无圈）
(153, 560)  71 节点 71 边  →  tree + 1 个 cycle (circuit rank = 1)
```

**关键 insight**：K_n shared-partner 在 G_M 上**不是 clique**，而是 **star**：

```text
设 (A, B) 是 k=n multi-N pair, N=[N_1,...,N_n]。
G_M 上 (A, B) 的邻居是 C(n, 2) 个 partner pair (N_i, N_j)。
但 (N_i, N_j) 与 (N_p, N_q) 之间在 G_M 上 NO direct edge（除非它们再通过别的 multi-N pair 共享）。
```

也即 partner identity 给出的边是 (A, B) ↔ (N_i, N_j)，不是 (N_i, N_j) ↔ (N_p, N_q)。
所以一个 K_n hub 在 G_M 上长成 star（中心 + C(n,2) 个 leaves）而不是完全图。

**G_M 因此倾向于树状结构**。圈只在多个 K_n hub 通过链相连且形成回路时出现。

## (153, 560) 唯一 6-cycle 的具体形状

```text
(560, 2925) — (420, 1344) — (1008, 2925) — (1344, 7020) — (2925, 9360) — (1344, 3900) — 回 (560, 2925)
   k=3          k=3            k=4             k=4             k=3            k=5
```

经过 1 个 K_5 hub `(1344, 3900)` 和 2 个 K_4 hub。元素涉及 8 个不同整数：
{420, 560, 1008, 1344, 2925, 3900, 7020, 9360}。

cycle 节点的 N 列表展示密集 N-sharing：

```text
(560, 2925)  N = [420, 1344, 3900]
(420, 1344)  N = [560, 1008, 2925]
(1008, 2925) N = [420, 1100, 1344, 7020]
(1344, 7020) N = [1008, 2925, 6992, 9360]
(2925, 9360) N = [1344, 3900, 7020]
(1344, 3900) N = [560, 1792, 2925, 7105, 9360]
```

每对相邻 cycle 节点共享至少 1 个 N，对应 partner identity 边。

## closure 检查：两个分量都没有反例

```text
(264, 420)  28 nodes:  closure pair (N_i + N_j == A + B) 数 = 0
(153, 560)  71 nodes:  closure pair                       数 = 0
```

99 个 multi-N pair 内部全部不出反例，与 wl055-056 整体观察一致。

## 实证回答用户的猜想

| 用户猜想 | 实证结果 |
|---|---|
| "BFS 是更大的结构" | ✅ 确认 — K_n 只是局部 star，BFS 暴露真正 connected component |
| "根节点只有一个" | ❌ 否定 — 至少 (264, 420) 与 (153, 560) 不相连 |
| (隐含) connected component 是 dense | ❌ 否定 — 实际近似森林，circuit rank 极低 |

## 可视化输出（不入 git，本地 artifact）

```text
results/partner_bfs_root264_420_M100000.png         kamada_kawai layout
results/partner_bfs_root264_420_M100000_spring.png  spring layout
results/partner_bfs_root153_560_M100000.png         kamada_kawai layout
results/partner_bfs_root153_560_M100000_spring.png  spring layout
results/partner_bfs_root*.dot                       graphviz dot 文件（备用）
```

颜色编码（节点）：

```text
white       k=2  (叶子型 partner pair, 仅 1 个 partner 即 hub)
lightyellow k=3  (中等 hub)
lightcoral  k=4  (重要 hub)
tomato      k=5
red/dark    k>=6
```

节点大小按 k 递增。

## 没做的事 / 钩子

1. **更广的 BFS**：从 catalog 中其他高 k hub（K_8 实例 (55440, 445536) 等）出发 BFS，
   看 G_M 全局有多少 connected component。
2. **G_M 是否真的森林？**当前 (153, 560) 出现 1 个 cycle。需要更大数据集（多个 BFS 起点）
   验证"G_M 几乎是森林"是否是普遍性质。
3. **cycle 的代数解释**：(153, 560) 的 6-cycle 经过 K_5 hub。是否所有 G_M cycle
   都经过某个 K_n hub (n>=3)？是否对应 Mordell-Weil 群上的某种关系？
4. **(15, 48) ↔ (20, 36) 单边孤立 component** 是 G_M 的最小可能 component（2 顶点 1 边）。
   这类 component 数量？
5. **partner graph 的连通分量谱**：从所有已知 multi-N pair 出发并查集合并，
   得到全局 connected component 数与大小分布。这是 wl057 PARTNER_GRAPH_THEORY.md
   §6 Q2 的核心问题。

## 文件

```text
scripts/partner_bfs.py                                BFS 主脚本
scripts/partner_bfs_analyze.py                        交集 + closure + dot 输出
scripts/partner_bfs_plot.py                           matplotlib 画图
pyproject.toml                                        加 [dependency-groups.viz]
uv.lock                                               (随之更新)
results/partner_bfs_*                                 BFS 数据 + PNG（本地，不入 git）
docs/work-logs/058-partner-bfs-graph-visualization.md 本文件
```
