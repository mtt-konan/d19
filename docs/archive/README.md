# 历史文档与实验记录

本目录包含已经完成或暂停的工程实验记录，保留作为参考和背景理解，但不是当前主线。

## 文档列表

| 文档 | 内容 | 状态 |
|------|------|------|
| `CHAIN_PERFORMANCE.md` | `chain` 命令的实测耗时记录 | 参考用 |
| `CHAIN_FAST_MOD_SIEVE.md` | `mod` 预筛实验：筛掉了多少、为什么没更快 | 已结束 |
| `CHAIN_FAST_BUCKET_STATS.md` | 结构桶统计的 SQLite 设计 | 参考用 |
| `CHAIN_FAST_OPTIMIZATION.md` | `chain-fast` 性能分析与优化方向 | 参考用 |
| `CONCORDANT_SAFE_FILTERS.md` | concordant 的早期前筛实验 | 已结束 |

## 何时查看

- **需要了解历史背景**：看 `CHAIN_PERFORMANCE.md`（当前线性能数据在顶层 `docs/CHAIN_FAST_PERFORMANCE.md`）
- **需要 SQLite 数据库设计细节**：看 `CHAIN_FAST_BUCKET_STATS.md`
- **需要理解已尝试过但未成功的方向**：看 `CHAIN_FAST_MOD_SIEVE.md` 或 `CONCORDANT_SAFE_FILTERS.md`

## 当前主线文档

当前应该优先看的文档在 `docs/` 根目录：

- `THEORY_DIRECTIONS.md` ← **当前重点**
- `PROJECT_STATUS.md`
- `CURRENT_FINDINGS.md`
- `MATH.md`

