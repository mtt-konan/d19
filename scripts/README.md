# scripts/ — 脚本入口索引

按主题分组. 顶层只放主入口与常用 lookup 工具. 每个子目录有自己的功能集合.

## 顶层 (主入口)

| 脚本 | 用途 |
|------|------|
| `search.py` | 主搜索 CLI (chain-fast / EC / parametric, 见 `--help`) |
| `prove_no_solution.py` | 增量证明 hard_case 不可解 (proof_status pipeline) |
| `prove_no_solution_multi_first.py` | multi-N first variant of `prove_no_solution` |
| `lookup_multi_n.py` | 给 (A, B) 查 concordant N 列表 (常用查询工具) |

## 子目录

### `benchmark/` — 性能基准

| 脚本 | 用途 |
|------|------|
| `benchmark_candidate_generators.py` | 比较 safe / non_coprime / multi_n 三种候选生成方式 (wl072) |
| `benchmark_ab_sieve_orders.py` | proof_status A/B sieve 顺序基准 (wl067-068) |
| `benchmark_parallel_executor.py` | parallel executor 复用 vs 重建池基准 (wl064) |
| `bench_mod_sieve.py` | mod sieve 微基准 |

### `multi_n/` — multi-N 枚举与目录

| 脚本 | 用途 |
|------|------|
| `fast_multi_concordant_scan.py` | pivot-on-N 快速枚举 (wl048) |
| `multi_concordant_n_scan.py` | 老版 (A,B)-pivot 枚举 (wl046, 慢但可对照) |
| `non_coprime_multi_n_scan.py` | 非互素 (a,b) multi-N 扫描 (wl056) |
| `build_results_catalog.py` | 结果目录构建 |
| `k_distribution_audit.py` | k 分布 (safe-pass vs unsafe) 统计 (wl084) |
| `validate_fast_multi_n.py` | fast scanner 与朴素扫描的一致性校验 |
| `dscale_kn_generator.py` | D-scaling K_n 快速生成器 (wl085, A.7 落地) |

### `partner/` — Partner graph (G_M) / K_n hub 分析

BFS / 全图构建:
- `partner_bfs.py` — 单源 BFS
- `partner_full_bfs.py` — 全 G_M BFS (并行)
- `partner_full_graph.py` — 全图持久化
- `partner_full_graph_query.py` — 查询接口
- `partner_pair_graph.py` — pair-level 图
- `partner_pair_k_distribution.py` — pair k 分布

分析 / 可视化:
- `partner_bfs_analyze.py` — BFS 结果分析
- `partner_bfs_plot.py` — 子图绘制
- `partner_kn_subgraphs.py` — K_n 子图抽取
- `comp0_analyze.py` — 超大 component 0 拓扑分析 (wl062)
- `export_gephi_component.py` — Gephi 导出
- `find_partner_origin.py` — partner 来源回溯
- `verify_missing_partner.py` / `verify_kn_equivalence.py` — 一致性校验

K_n 实例 + 全 G_M closure:
- `full_gm_closure_scan.py` — G_M 反例彻底搜索 (wl063)
- `full_gm_delta_stats.py` — delta near-miss 统计 (wl066)
- `k8_ellrank.py` — K_8 实例 ellrank (wl060)
- `k9_inspect.py` — K_9 hub 检查 (wl062)
- `k10_extract_and_ellrank.py` — K_10 实例分析 (wl065)
- `cycle_ellrank.py` — cycle / deficit 分析 (wl059)

### `theory/` — Path A / closure / F₂-rank 实证

Path A 主线 (k=2 → k=n):
- `analyze_k2_closure_fiber.py` — k=2 closure fiber 实证 (wl074)
- `analyze_k2_f2_rank.py` — k=2 F₂-rank 实证 (wl076)
- `analyze_k2_height_bound.py` — k=2 height bound 实证 (wl077)
- `analyze_kn_f2_rank.py` — 通用 k=n F₂-rank 实证 (wl084)
- `analyze_k4_signatures.py` — k=4 signatures 探索

Pythagorean / half-points:
- `analyze_a2_pythagorean.py` — A2 conjecture (wl081)
- `analyze_multi_n_half_points.py` — multi-N half-points 列表
- `audit_halfpoint_factorization.py` — half-point 因式分解 audit (wl083)
- `verify_a1_proof_chain.py` — A1 证明链端到端验证 (wl083, ⚠️ 见 wl084 修正)
- `d_valuation_analysis.py` — d_2/d_3 估值分析

F₂-rank 工具:
- `classify_multi_n_by_f2_rank.py` — F₂-rank 分类器 (wl049)
- `pari_rank_high_f2.py` — high F₂-rank pair PARI ellrank (wl050)
- `k4_rank.py` / `k4_two_descent_rank.py` — k=4 rank 实测

### `modular/` — Path B / mod p² 实证

| 脚本 | 用途 |
|------|------|
| `enumerate_mod_p2_classes.py` | (a, b) mod p² 类枚举 (wl078) |
| `enumerate_mod_p2_crt.py` | CRT 合并 mod p² (wl079) |
| `mod_p2_unused_analysis.py` | unused mod p² class 分析 (wl078) |
| `uniform_mod_p2_audit.py` | uniform mod p² audit (wl077-079) |
| `analyze_multi_n_mod_pattern.py` | multi-N mod pattern (wl079) |

### `utility/` — 工具

| 脚本 | 用途 |
|------|------|
| `extract_pdf_text.py` | PDF 文本抽取 (文献调研) |

### `archive/` — 历史归档

wl053 round-2 archive 之前的脚本. 不要新增. 见 `archive/README.md`.

---

## 路径约定

所有子目录脚本顶端用:
```python
ROOT = Path(__file__).parent.parent.parent  # → 项目 root
```
（顶层主入口仍用 `Path(__file__).parent.parent`.）

新增脚本时:
1. 选合适分类放进对应子目录
2. 顶部加一行 docstring 说明用途
3. 在本 README 对应 section 加一行索引
