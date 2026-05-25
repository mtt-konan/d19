# 历史 worklog 归档（wl001-027）

这里收集 d19 早期到 chain-fast 时代结束之间的全部 worklog。当前主线已经迁移到
`proof_status` / `concordant` / `multi-N` / `F₂-rank`，对应 worklog 是
**wl028-049**，仍在 `docs/work-logs/` 根目录。

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
028-proof-status-pipeline.md           proof_status 框架奠基
029-legacy-stub-cleanup.md
030-large-range-proof-stats.md
031-heegner-height-diagnostic.md
032-literature-review.md
033-dual-ec-probe.md
034-hypotenuse-identity.md
035-pari-selmer-api.md
036-compute-rank-fix-and-ell2cover-batch.md
037-finite-descent-on-hard-cases.md
038-large-scale-sha2-pattern-hunt.md
039-ell2cover-sha2-explicit.md
040-chain-closure-mod-sieve.md
041-parallel-pipeline-and-max-hyp-10k.md
042-sha2-clean-13-deep-dive.md
043-post-wl042-direction-map.md
044-generator-lattice-search-x1.md
045-parallel-infrastructure.md
046-multi-concordant-n-scan-10k.md
047-literature-and-multi-n-tooling.md
048-fast-pivot-on-n-scanner.md
049-f2-rank-classifier-on-multi-n-catalog.md
```
