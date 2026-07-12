# 历史 worklog 归档

这里收集已经由 consolidated worklog 取代的明细记录。当前主线保留在
`docs/work-logs/` 根目录；阅读时先用 consolidated worklog，只有在追溯具体证据
或失败路径时才进入本目录。

下面这批是历史档案，**不再作为当前研究入口**，但保留是为：

- 复现旧实验（GPU 后端、d4 对称性、parametric 比较）
- 追溯算法选型理由（chain 数据库、bucket stats、mod sieve 实验）
- 归档已结束的尝试

## 分组

### 三顶点 / parametric / GPU 起步（wl001-009）

```text
001-initial-parametric-search.md      最初参数化搜索
002-numpy-vectorization.md             numpy 向量化
003-d4-symmetry-dedup.md               D4 对称去重
004-side-exclusion-filter.md           边长排除筛
005-gpu-search.md                      GPU 后端
006-int64-overflow-fix.md              int64 溢出
007-pytorch-astype-fix.md              pytorch astype 兼容
008-visualization.md                   results→html 可视化
009-backend-split-test-consolidation.md
```

### EC / chain foundation（wl010-019）

```text
010-ec-search-foundation.md
011-unified-cli-entry.md
012-ec-vectorization-gpu.md
013-parametric-shared-core.md
014-ec-db-analysis.md                  注意编号重复（与下条同号）
014-pythagorean-chain-search.md
015-cross-product-family-exclusion.md
016-primitive-decomposition-display.md
017-chain-reduction-math.md
018-chain-fast-implementation.md
019-parity-filter-and-ec-analysis.md
```

### chain-fast 数据库 / safe-pair 时代（wl020-027）

```text
020-ec-concordant-analysis-pipeline.md
021-chain-numpy-db.md
022-chain-fast-profile-cache.md
023-chain-fast-mod-sieve-experiment.md
024-chain-fast-100k-structure-findings.md
025-chain-fast-safe-pair-sieve.md
026-concordant-local-sieve-mod1680.md
027-concordant-safe-pair-sieve.md
```

## 当前主线 worklog（不在本目录）

```text
028-proof-status-ec-foundation-consolidated.md
053-partner-graph-fast-core-consolidated.md
073-gen-closure-modular-fullspace-consolidated.md
105-sum-ab-fixed-ratio-consolidated.md
162-r-lambda-centerline-consolidated.md
203-wl218-full-plane-reciprocal-consolidated.md
294-closure-quotient-foundation-consolidated.md
```

## AA+BB admissibility taxonomy（wl491-522）

`wl491-wl522` 的 32 份明细记录保留在本目录。默认入口是：

```text
../491-522-aa-bb-admissibility-taxonomy-consolidated.md
```

这些明细用于追溯 admissibility filter、finite `M_tail` shell routing、ambient
`C_d` classification 和 support/cover taxonomy，不再作为当前研究入口。
