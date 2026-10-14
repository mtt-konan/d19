# 历史文档与实验记录

本目录包含已经完成或暂停的工程实验记录，保留作为参考和背景理解，但不是当前主线。

[研究路线归档](RESEARCH_ROUTES.md) 另外索引数学路线的已证成果、未解缺口、停止原因和恢复条件。这里只归档默认入口，不搬动证明文件，也不把暂停改写成路线已被否定。历史记录中的“下一步”不自动生效。

## 文档列表

| 文档 | 内容 | 状态 |
|------|------|------|
| [RESEARCH_ROUTES.md](RESEARCH_ROUTES.md) | 数学路线与旧交接入口的状态索引 | 按需查阅 |
| `CHAIN_PERFORMANCE.md` | `chain` 命令的实测耗时记录 | 参考用 |
| `CHAIN_FAST_PERFORMANCE.md` | `chain-fast` 加 `--profile` 后的首轮性能记录 | 参考用 |
| `CHAIN_FAST_OPTIMIZATION.md` | `chain-fast` 性能分析与优化方向 | 参考用 |
| `CHAIN_FAST_MOD_SIEVE.md` | `mod` 预筛实验：筛掉了多少、为什么没更快 | 已结束 |
| `CHAIN_FAST_BUCKET_STATS.md` | 结构桶统计的 SQLite 设计 | 参考用 |
| `CHAIN_FAST_STRUCTURE_FINDINGS.md` | `chain-fast --bucket-stats` 在 `max_hyp=100000` 上的首轮结论 | 参考用 |
| `CHAIN_STRUCTURE_IDEAS.md` | 2026-05 头脑风暴的 4 个想法（已被 wl 033/034/035 实证 follow-up） | 参考用 |
| `CONCORDANT_SAFE_FILTERS.md` | concordant 的早期前筛实验 | 已结束 |
| `CHAIN_FAST_SAFE_FILTERS.md` | chain-fast 当前 safe_sieve 的可证明性说明 | 参考用 |
| `SEARCH_METHODS.md` | 5 个 CLI 子命令的词典（parametric / ec / chain / chain-fast / concordant） | 参考用 |
| `METHOD_COMPARISON.md` | 5 个方法的实测时间与适用场景对比 | 参考用 |
| `DIRECTIONS.md` / `EXPLORATION_MAP.md` | 旧路线入口与探索地图 | 已归档 |
| `THEORY_DIRECTIONS*.md` / `OPEN_DIRECTIONS` 旧长清单 | 旧理论路线清单 | 已归档 |
| `CURRENT_FINDINGS.md` / `MULTI_CONCORDANT_N_STRATEGY.md` / `PARTNER_GRAPH_THEORY.md` / `PROOF_STATUS_FAST_MODE.md` | 旧主线说明与工程说明 | 已归档 |
| `MULTI_N_FILTER_LADDER.md` | multi-N 阶梯与 pivot-on-N 快速算法记录 | 已归档 |

## 何时查看

- **需要了解 chain-fast 性能历史**：看 `CHAIN_FAST_PERFORMANCE.md` / `CHAIN_FAST_OPTIMIZATION.md`
- **需要 SQLite 数据库设计细节**：看 `CHAIN_FAST_BUCKET_STATS.md`
- **需要看 max_hyp=100000 下 chain-fast 结构桶分布**：看 `CHAIN_FAST_STRUCTURE_FINDINGS.md`
- **需要理解 4 个 chain 数学想法的最初提法**：看 `CHAIN_STRUCTURE_IDEAS.md`（实证结论看 wl 033–037）
- **需要理解已尝试过但未成功的方向**：看 `CHAIN_FAST_MOD_SIEVE.md` 或 `CONCORDANT_SAFE_FILTERS.md`

## 当前入口

数学成果和本次活动分别从以下入口读取：

- [项目状态](../PROJECT_STATUS.md)：已证明什么、尚未证明什么。
- [当前上下文](../codex/current-context.md)：本次活动与独立任务锚点。
- [任务选择](../NEXT_RESEARCH_GATE.md)：新研究任务的选择边界。
- [数学参考](../MATH.md)：按需查阅原始方程与已有推导。
