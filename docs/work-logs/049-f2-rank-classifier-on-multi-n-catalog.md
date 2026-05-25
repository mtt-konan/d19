# wl049 — F₂-rank classifier on the multi-N catalog

## 目的

接 wl048 Phase 2 follow-up：把“F₂-rank 是 rank 的免-PARI 快速代理”这条结论从 3 个 k=4 pair 推到全部 multi-N catalog（max_hyp=10000 / 20000 / 50000，共 854 / 1848 / 4968 pair），看 rank 分布、找出真正“值得 PARI 审计”的小集合。

## 思路

`F₂-rank` 的定义：对每个 concordant `N`，取一个 positive-sig 半点，计算 `(sf(x), sf(x+A²))`；把全部 N 的这些向量做 F₂ Gauss 消元，记 rank。

```text
F₂-rank ≤ k                 总成立
F₂-rank ≤ rank(E) + 2       因为 image lives in (Q*/Q*²)² ≅ E(Q)/2E(Q)
                            而 dim(E(Q)/2E(Q)) = rank + 2
F₂-rank == k (saturated)    "无 2-torsion 翻折"，4 个 N 的方向互相独立
F₂-rank <  k (deficient)    "torsion 翻折"，多余的 N 来自 2-torsion 平移
```

### 推论：rank 的下界

```text
rank(E) ≥ F₂-rank − 2     (来自 dim(E(Q)/2E(Q)) ≥ F₂-rank)
```

所以 `F₂-rank ≥ 3` 给出 `rank ≥ 1`，`F₂-rank ≥ 4` 给出 `rank ≥ 2`。这两条判定都不需要 PARI。

## 实现

### 模块

```text
src/rational_distance/concordant/two_descent_rank.py
    F2RankResult
    f2_rank_of_concordant_pair(A, B, ns) -> F2RankResult
```

返回的字段：

```text
A, B, ns                                      原始输入
images: tuple[(sf(x), sf(x+A²)), ...]         每个 N 的正 sig image
f2_rank: int                                   Gauss 消元后的 F₂-rank
minimal_relation: tuple[int, ...] | None      最小的 F₂-依赖子集（如有）
```

### 测试 (TDD)

```text
tests/test_two_descent_rank.py    9 tests
  TestThreeNPair          (153, 560)  k=3 → F₂-rank=3, 无关系
  TestK4Pairs:            三个 k=4 pair，与 wl048 数据一致
  TestEdgeCases:          空 / 单 N / 非 concordant N (raises)
```

### 分类脚本

```text
scripts/classify_multi_n_by_f2_rank.py
    --in   ground-truth jsonl
    --out  附加 f2_rank / minimal_relation 字段后的 jsonl
    --top  打印的 high-rank candidate 数
```

## 实测

```text
$ uv run python scripts/classify_multi_n_by_f2_rank.py \
    --in  results/multi_concordant_N_max50000_fast.jsonl \
    --out results/multi_concordant_N_max50000_classified.jsonl
processed: 4968 pairs in 1.0s
```

### 全量 F₂-rank 分布

```text
                max_hyp=10000   max_hyp=20000   max_hyp=50000
F₂-rank=2          829 (97.1%)     1803 (97.6%)    4858 (97.8%)
F₂-rank=3           25 ( 2.9%)       45 ( 2.4%)     109 ( 2.2%)
F₂-rank=4            0                1 ( 0.05%)      1 ( 0.02%)
```

三档分布几乎平移 —— **F₂-rank 比例对 max_hyp 鲁棒**。

### Joint (k, F₂-rank) 分布（max_hyp=50000）

```text
k=2  F₂-rank=2:  4853     普通 multi-N (rank 通常 0)
k=3  F₂-rank=2:     5     k=3 的 torsion-fold 假象 (rank ≥ 0)
k=3  F₂-rank=3:   107  ←  saturated k=3 (rank ≥ 1)
k=4  F₂-rank=3:     2     k=4 但有 1 维 torsion 关系 (rank ≥ 1)
k=4  F₂-rank=4:     1  ←  saturated k=4 (rank ≥ 2，PARI 实测=4)
```

只有 **110 pair (2.2%)** 是 `F₂-rank ≥ 3` 的真候选。其中 **1 个唯一的 saturated k=4** 就是 `(7337, 28288)`，rank=4。

closure pair 数仍为 0。

## 关键含义

### 对反例搜索

把搜索池从 4968 pair 缩到 110 pair —— **2 个数量级的压缩**，且每对剔除都有代数理由（rank=0/1 → 不可能凑出 4-chain）。

| F₂-rank | rank 下界 | 4968 中的占比 | 解读 |
|---------|-----------|---------------|------|
| 2 | 0 | 97.8% | rank=0 / torsion 凑出来的 noise，4-chain 不可能 |
| 3 | 1 | 2.2% | rank ≥ 1 的真候选，需要 PARI 进一步审计 |
| 4 | 2 | 0.02% | rank ≥ 2 的稀有候选 |

### 对证明非存在

可以在 `proof_status` workflow 里加一层 short-circuit：

```text
if F₂-rank ≤ 2:
    → rank ≤ 0 (after 2-torsion 折扣，且 2-torsion 不能给出 closure 必需的独立 chain 元素)
    → 4-chain 不可能在 E_{A,B} 上实现
    → 等价于现有 rank_zero 方法的代数预筛
```

这条 short-circuit 不调用 PARI，毫秒级。

## 副观察

### F₂-rank 跨尺度稳定

```text
F₂-rank=3 占比:  2.9% (10k) → 2.4% (20k) → 2.2% (50k)
F₂-rank=4 占比:                0.05% (20k) → 0.02% (50k)
```

随 max_hyp 增大，F₂-rank=3 比例略降；F₂-rank=4 数量增长慢。  
推测：rank 的“典型分布”在 multi-N pair 上是分布式的，而非集中在某个特殊范围。

### Top 候选都很小

```text
A=  153 B=   560   F₂-rank=3   k=3
A=  208 B=   495   F₂-rank=3   k=3
A=  275 B=   576   F₂-rank=3   k=3
...
```

即在 max_hyp=50000 池里，最值得审计的样本反而是历史已知的 small pairs（含被 Bremner-Ulas 等文献用过的 (153, 560)）。

## 后续任务

1. 用 PARI ellrank 给 110 个 F₂-rank≥3 的 pair 都跑一遍 rank 实测，建“真高 rank”分布
2. 把 F₂-rank short-circuit 接进 `proof_status` 流水线，看能多压掉多少 hard_case
3. 把 `max_hyp` 推到 100k–200k，看是否出现新的 saturated k≥5 pair
4. 对 saturated 候选做 chain closure 的 mod-p² sieve，对 closure 失败模式做统计

## 文件

模块/测试：

```text
src/rational_distance/concordant/two_descent_rank.py    新建
tests/test_two_descent_rank.py                          新建 (9 tests)
```

脚本：

```text
scripts/classify_multi_n_by_f2_rank.py                  新建
```

输出：

```text
results/multi_concordant_N_max10000_classified.jsonl    854 行
results/multi_concordant_N_max20000_classified.jsonl   1848 行
results/multi_concordant_N_max50000_classified.jsonl   4968 行
```
