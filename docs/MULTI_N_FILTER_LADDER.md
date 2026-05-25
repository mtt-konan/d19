# Multi-N 筛选阶梯与快速算法切入点

本文澄清两件事：

1. 现在所有“筛选”按层级排成一根阶梯
2. “快速算法”应该从这根阶梯的哪一层切入

它是 `docs/MULTI_CONCORDANT_N_STRATEGY.md` 的执行视角补充。

## 1. 主线：从全集到 Harborth 反例

```text
L0  reduced coprime pair (A, B), 1<=A<B<=max_hyp        ~30,000,000 (max_hyp=10000)
        ↓  factor-search 找全部 concordant N
L1  ≥1 个 concordant N                                   稀少
        ↓  统计 |concordant_N(A,B)|
L2  ≥2 个 concordant N (multi-N pair)                    854 (max_hyp=10000)
        ↓  k = |concordant_N|
L3  ≥3 个 concordant N (k=3)                              26
        ↓  closure: 存在 N1+N2 = A+B
L4  multi-N + closure                                      0
        ↓  Harborth 全条件
L5  Harborth 4-chain 反例                                  目标 (是否存在未知)
```

`results/multi_concordant_N_max10000.jsonl` 是 `L0 → L2` 的 authoritative ground truth。

## 2. 辅助筛（与主线正交）

```text
辅助筛 R  rank(E_{A,B}) >= 1, 2, 3
辅助筛 S  half-points 的 squarefree signature 类
辅助筛 H  KSS homogeneous space 类
```

- `L2 ⇏ rank>=2` 严格不成立，但实际数据上几乎一致
- `L3` 与 `rank=3` 在 `(153,560)` 命中
- 这些筛子用来解释 `L4` 难以进入的结构原因，不用来生成

## 3. 主线的两种执行策略

```text
策略 A  慢路 / 暴力 / 完整 (现在)
        外层枚举 (A,B)，内层 factor-search 找 N
        cost ~ |L0| * cost(factor-search per pair)
        max_hyp=10000 已经跑过，得到 854 条 ground truth

策略 B  快路 / 枢轴在 N (待实现)
        外层枚举 Pythagorean 参数 (m, n, k)
        每个参数生成一条 (A, N) 满足 A^2 + N^2 = h^2
        按 N 分组得到 A_set(N)
        对每个 N，把 A_set(N) ∩ [1, max_hyp] 内的两两组合写入 (A,B) 的 N 列表
        最后保留 |N 列表| >= 2 的 (A, B)
        cost ~ sum_(m,n,k) 1 + sum_N |A_set(N) ∩ [1,max_hyp]|^2
        预期 cost << 策略 A
```

策略 B 的关键事实：

```text
(A, N, h) 是 Pythagorean 三元组 ⟺ A^2 + N^2 = h^2
所有 primitive Pythagorean 三元组都形如 (m^2-n^2, 2mn, m^2+n^2)
缩放因子 k 给非 primitive 的全部三元组
```

所以 `(A, N)` 的全集 = `(m, n, k)` 参数空间的像，**没有遗漏**。

## 4. “快速算法”应当从哪里切入

```text
切入点 = L1 之前
作用   = 取代 L0 → L2 这段暴力扫描
对照   = 在 max_hyp=10000 必须重现 854 条 ground truth
```

策略 B 的 v0 目标：

```text
fast_multi_concordant_pairs(max_hyp=10000) == ground_truth_pairs
```

不追求 v0 同时做 closure / signature / rank。这些是 L2 之后的层，已有工具：

- `scripts/lookup_multi_n.py`
- `scripts/analyze_multi_n_half_points.py`

## 5. 验证策略

```text
单元测试  策略 B 在 max_hyp=300 内匹配 brute force
对照脚本  策略 B 在 max_hyp=10000 内匹配 ground truth (854 条)
扩展实验  仅在以上两步通过后，跑 max_hyp=50000 / 100000
```

不允许：

```text
不验证、直接相信策略 B
```

## 6. 实测结果（pivot-on-N v0）

`src/rational_distance/concordant/fast_multi_n.py` 实现并已校验：

```text
max_hyp=10000   1.02s   854 pairs   max k=3   与 ground truth 完全一致
max_hyp=20000   3.96s  1848 pairs   max k=4   首次出现 k=4: (11776, 17199)
max_hyp=50000  25.21s  4968 pairs   max k=4   3 个 k=4 pair
```

参考量级：

```text
slow path (multiprocessing 10 cores)   max_hyp=10000  ~分钟到小时
fast path (single core, pivot-on-N)    max_hyp=10000  ~1 秒
fast path                              max_hyp=50000  ~25 秒
```

所有 scale 上 closure pair 数仍然为 0。三个 k=4 pair 的 4 个 N 任意两两相加都不等于 `A+B`。这表明 closure 失败是结构性原因，不是 k 不够。

新的 k=4 样本：

```text
(11776, 17199)   N = [3960,  4368, 46368, 541632]    A+B = 28975
(6669,  26656)   N = [8892, 13860, 19992,  91392]    A+B = 33325
(7337,  28288)   N = [1716,  5916, 31584,  84216]    A+B = 35625
```

## 7. 之后再考虑的事

- Phase 2  L2 → L3 / L4 / signature 的结构筛
- Phase 3  超大规模时考虑 KSS / Ono twist 之类的有损生成
- Phase 4  Mordell-Weil sieve 把 closure 局部化
- Phase 5  对 k=4 三个新样本做 rank audit 与 half-point 分析
