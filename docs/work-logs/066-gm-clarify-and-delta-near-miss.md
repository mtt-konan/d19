# wl066 — `G_M` 术语澄清与 `Δ` 近失统计：338K 顶点里最近只差 1

## 触发

wl065 之后，问题开始从“还能不能继续扫更大范围”转向两件更基础的事：

- `G_M` 到底指什么：是整个 multi-`N` 图，还是只是 `comp 0` 那个 30w 超大分量？
- 既然 338,225 个 multi-`N` 顶点已经能给出很多 `C(k,2)` 个“长方形候选”，它们离真正的 `closure`（即正方形闭合）到底还差多远？

本轮把这两件事一起整理：

1. 统一 `G_M / k_real / k_visible / 秩 / primitive（约去公因子的底型） / 放大倍数` 的语义
2. 直接统计

```text
Δ = (A + B) - (N_i + N_j)
```

看 338,225 个 `G_M` 顶点上，所有长方形候选离 `closure = 0` 有多近。

## 术语澄清

### 1. `G_M` 不是 `comp 0`

`G_M` 的定义是：

- 顶点：所有 multi-`N` pair `(A, B)`（即至少有两个 concordant `N`）
- 边：若 `(N_i, N_j)` 是 `(A, B)` 的一个 partner pair，则在 `(A, B)` 与 `(N_i, N_j)` 之间连边

因此：

```text
G_M @ max_value=1M = 当前截断下的整张 partner 图
comp 0             = 这张图中的最大连通分量
```

当前数据里：

```text
G_M @ max_value=1M: 338,225 顶点, 9,580 个分量
comp 0            : 309,689 顶点
```

所以“30w 巨型分量”只是 `G_M` 的一部分，不是 `G_M` 本身。

### 2. `k_real` 与 `k_visible`

对任意 `(A, B)`：

```text
k_real    = 真正完整的 concordant N 个数
k_visible = 在 max_value=1M 截断图里真正看得见的那个 k
```

图上的 degree（度数）满足：

```text
degree = C(k_visible, 2)
```

但若某些 partner `N > 1M` 被截掉，则图上只看见较小的 `k_visible`，而真实的 `k_real` 更大。

### 3. 这里的秩（rank）是什么

这里的秩指椭圆曲线

```text
E_{A,B}: Y² = X(X + A²)(X + B²)
```

在有理数域上的 Mordell-Weil 秩（独立解个数），不是图论里的 degree，也不是 `k`。

可粗略理解为：

- `k`：当前看见了多少个整数平方 `X = N²` 的特殊点
- 秩：这条曲线本身有多少条独立的有理解方向

二者有关，但不是同一个量。

### 4. wl065 的“高 k 常常只是少数低秩底型的放大版本”是什么意思

若

```text
(A, B) = (d a, d b)
```

则两条曲线

```text
E_{A,B}, E_{a,b}
```

在有理数域上同构，所以**秩不变**。

但整数 `N` 的个数并不是这个同构下的不变量：primitive（约去公因子的底型）上的一些有理 `n`，在放大后可能因为分母被 `d` 清掉而变成新的整数 `N = d n`。

因此可能发生：

```text
primitive 底型自身 k 只有 1 或 2
→ 某些放大版本却已经变成 K_9 / K_10
→ 但 rank 仍然只有 3 或 4
```

wl065 的 16 个高 `k` 样本最后只归并到 4 个底型，就是这个现象的直接证据。

### 5. 现在能安全推出的必要条件

若 Harborth / Steiner-Beukers 反例存在，则必有：

```text
反例
=> 存在同一 pair (A, B) 的两个 concordant N
=> k_real >= 2
=> 反例一定落在完整 G_M 里
=> 对应曲线至少正秩（秩 >= 1）
=> 存在某对 (N_i, N_j) 满足 N_i + N_j = A + B
```

但现在**不能**推出：

```text
反例 => k > 2
反例 => 秩 >= 2 或 >= 3
```

因为反例本身只需要两个 `N`；两个 `N` 也未必意味着有两个独立方向。

## 工具

本轮新增：

```text
src/rational_distance/results/gm_closure_delta.py   pair 级 Δ 汇总 helper
scripts/full_gm_delta_stats.py                      全 G_M 的 Δ 近失统计脚本
tests/test_gm_closure_delta.py                      helper 单测（3 passed）
```

运行：

```text
uv run python scripts/full_gm_delta_stats.py --workers 10
```

耗时：`717.9s`。

## 结果

### 1. 总体规模

```text
Total vertices scanned: 338,225
Total candidate pairs:  829,444
Total closure hits:     0
Global min |Δ|:         1
```

这里的 `829,444` 正是

```text
Σ_v C(k_real(v), 2)
```

也就是把 338,225 个 multi-`N` 顶点的全部长方形候选都检查一遍之后的总对子数。

### 2. `Δ` 符号分布：负值更多，0 仍然完全缺席

```text
negative: 477,327   (57.55%)
positive: 352,117   (42.45%)
zero    :       0
```

因为

```text
Δ = (A + B) - (N_i + N_j)
```

所以这意味着：

```text
更多的候选对子其实落在 N_i + N_j > A + B 一侧
```

也就是“过线”（overshoot）比“没到线”更常见，但两边都很多，唯独 `0` 仍完全缺席。

### 3. 最近能靠到多近

按顶点统计“该顶点最接近 `closure` 的那一对”后，阈值分布为：

```text
min |Δ| <=     1 :      10  顶点   (0.0030%)
min |Δ| <=     2 :      12  顶点   (0.0035%)
min |Δ| <=     5 :      22  顶点   (0.0065%)
min |Δ| <=    10 :      62  顶点   (0.018%)
min |Δ| <=    20 :     116  顶点   (0.034%)
min |Δ| <=    50 :     392  顶点   (0.116%)
min |Δ| <=   100 :     770  顶点   (0.228%)
min |Δ| <=   500 :   4,064  顶点   (1.20%)
min |Δ| <= 1,000 :   7,907  顶点   (2.34%)
min |Δ| <= 5,000 :  31,069  顶点   (9.19%)
min |Δ| <= 10,000:  50,629  顶点   (14.97%)
```

这说明：

- `closure = 0` 仍是 0 命中
- 但“非常贴线”的 near-miss 确实存在
- 只是比例极低

特别是：

```text
338,225 个顶点里，只有 10 个顶点能靠到 |Δ| = 1
```

### 4. `|Δ| = 1` 的样本长什么样

`results/full_gm_delta_top.jsonl` 里最靠近 `closure` 的 10 个顶点，按 partner 对偶去重后其实只有 5 个 near-miss：

```text
(1260, 5440)   <->   (3024, 3675)    in comp 0
(12177, 16240) <->   (12180, 16236)  in comp 1758
(82824, 83640) <->   (82943, 83520)  in comp 5534
(70980, 94644) <->   (70983, 94640)  in comp 6369
(60, 84)       <->   (63, 80)        in comp 6602
```

最小样例如：

```text
(A, B) = (60, 84),   A + B = 144
closest (N_i, N_j) = (63, 80),   N_i + N_j = 143
Δ = 1
```

这些 `|Δ| = 1` 样本有两个重要现象：

1. **它们成 partner 对偶出现**。
   - 这不是孤立 accident，而是 partner 关系本身带来的成对近失。
2. **它们并没有集中在高 k hub 上**。
   - 前 10 个 `|Δ| = 1` 顶点里，只有 1 个是 `k = 3`，其余都只是 `k = 2`。
   - 所以“最贴近 closure”这件事，至少在当前数据里，并不专属于高 `k` 顶点。

## 主结论

### 主结论 1：现在不是“长方形太少”，而是“长方形很多，但 exact closure 仍完全缺席”

wl063 已经告诉我们：

```text
338,225 顶点上 closure = 0
```

本轮把这个结论换成“距离版”之后，可以更具体地说：

```text
829,444 个长方形候选里
最近已经能靠到 |Δ| = 1
但仍然没有任何 Δ = 0
```

所以问题不是样本太稀，而是 exact closure 这个条件比“有很多长方形”要苛刻得多。

### 主结论 2：near-miss 很少，而且很薄

虽然 `|Δ| = 1` 确实出现了，但数量极少：

```text
|Δ| = 1 只出现于 10 / 338,225 个顶点
```

连 `|Δ| <= 10` 也只有 62 个顶点，占比还不到 `0.02%`。

这说明 `closure` 不是在一条“厚边界”附近随机漏掉，而更像是在一条**非常薄的整点条件**上系统性缺席。

### 主结论 3：最近的 near-miss 并不提示“只盯高 k 就够了”

wl065 告诉我们：高 `k` 很多时候只是少数低秩底型被放大后的整模型效应。

本轮又看到：最贴近 `closure` 的样本并没有集中在高 `k` 顶点，反而大量是 `k = 2` 的 pair。

所以当前 picture 更像：

```text
高 k 让某个顶点内部可检查的长方形更多
但“最靠近 closure”这件事并不只由高 k 决定
```

后续若要缩小反例搜索面，更合理的关键字是：

- `k`
- 秩
- primitive 底型
- `min |Δ|`

而不是只看哪个点的 `k` 最大。

### 主结论 4：反例若存在，更像是非常罕见的 arithmetic exact hit，而不是普通 near-miss 的自然延伸

从 `|Δ|` 统计看，数据更支持下面这个 picture：

```text
很多 pair 能给出长方形
少数 pair 能非常接近 closure
但 exact closure 仍然像一条非常窄的算术共振线
```

这也解释了为什么：

- cycle 多 ≠ closure 多
- 高 `k` 多 ≠ 反例快出现
- 有 near-miss ≠ 很快会有 exact hit

## 对后续方向的影响

如果只做两步，那么这两步已经足够把优先级重新排清楚：

1. **术语层面**：以后讨论要明确区分
   - `G_M` vs `comp 0`
   - `k_real` vs `k_visible`
   - 图论层的 `k` 与代数层的秩
   - raw 顶点与 primitive 底型

2. **数据层面**：以后讨论“离反例多远”，应默认说 `min |Δ|`，而不是只说 `closure = 0`

3. **筛选层面**：下一批最值得看的，不是“所有高 `k` 点”，而是：
   - `min |Δ| <= 100` 或 `<= 1000` 的 near-miss 子集
   - 再按 primitive 底型去重
   - 再和秩、放大倍数一起看

## 文件

```text
scripts/full_gm_delta_stats.py                       本轮 Δ 统计脚本
src/rational_distance/results/gm_closure_delta.py    pair 级 Δ helper
tests/test_gm_closure_delta.py                       helper 单测
results/full_gm_delta_summary.json                   Δ 汇总结果
results/full_gm_delta_top.jsonl                      最接近 closure 的 top near-miss

docs/work-logs/066-gm-clarify-and-delta-near-miss.md 本文件
```

## 没做的事

1. **按 partner 对偶去重所有 near-miss**
   - 本轮只在 top 文件里肉眼看到 `|Δ|=1` 会成对出现。
   - 还没把全体 `Δ` 结果系统去重成“无向长方形”。

2. **按 primitive 底型去重 near-miss**
   - 这会更直接地回答：近失到底来自很多不同曲线类，还是主要来自少数底型的放大。

3. **把 `min |Δ|` 与秩联动**
   - 现在只知道最近的样本不集中在高 `k`。
   - 还没把这些 near-miss 的秩全部补齐。

## 元注

wl061-066 现在已经把 partner 方向的主线切成了三层：

```text
wl061-063 : G_M 的整体拓扑 + 全图 closure=0
wl065     : 高 k 主要来自少数低秩底型的放大
wl066     : 即使改看“距离版 closure”，最近也只到 |Δ|=1，且近失极少
```

也就是说，到目前为止最稳的结论已经不是“暂时没找到反例”，而是：

> 在当前 `G_M @ max_value=1M` 数据里，长方形早就很多了；真正缺席的是那条极薄的 exact closure 线。
