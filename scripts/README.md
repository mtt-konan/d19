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
- `rank_mixed_closure_curves.py` — 闭合条件混合商曲线 rank 实验 (wl290)

Rank-zero Selmer / AA+BB audit helpers:
- `audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder.py` — wl481 M_tail 显式矩阵与有限样本 kernel 诊断
- `audit_closure_quotient_rank_zero_aa_bb_wl482_m_tail_kernel_classification_gate.py` — wl482 AA A=3,B=1 的 `u_3` kernel 分类门
- `audit_closure_quotient_rank_zero_aa_bb_wl483_local_hilbert_row_decision_gate.py` — wl483 判断当前 local/Hilbert row ledger 是否能杀掉 `u_3`
- `audit_closure_quotient_rank_zero_aa_bb_wl484_u3_obstruction_route_entry_audit.py` — wl484 记录 `u_3` 完整 d-坐标候选并选择 obstruction workflow gate
- `audit_closure_quotient_rank_zero_aa_bb_wl485_explicit_cd_cover_equation_instantiation.py` — wl485 写出 `d=(3,3,1)` 的显式 `C_d` cover 方程
- `audit_closure_quotient_rank_zero_aa_bb_wl486_local_solubility_gate.py` — wl486 在 `infinity,2,3,13` 记录显式 local solubility 证书
- `audit_closure_quotient_rank_zero_aa_bb_wl487_route_impact_of_global_point.py` — wl487 记录 `u_3` cover 全局点对 M_tail / obstruction route 的影响
- `audit_closure_quotient_rank_zero_aa_bb_wl488_select_next_complete_d_coordinate_route_after_u3_global_point.py` — wl488 在 `u_3` 全局点后选择 AA+BB closure/pullback/common-source 下一路由门
- `audit_closure_quotient_rank_zero_aa_bb_wl489_closure_pullback_common_source_constraints_for_global_c_d_point.py` — wl489 检查 `u_3` 全局点的 AA pullback 与 AA+BB common-source 约束
- `audit_closure_quotient_rank_zero_aa_bb_wl490_route_impact_after_wl489_admissibility_failure.py` — wl490 在 `u_3` 点级 admissibility 失败后更新 route ledgers 并选择 reusable filter 下一门
- `audit_closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter.py` — wl491 定义 ambient `C_d` 点进入 AA+BB admissible ledger 前的 reusable filter，并回归 `u_3` 为 not_admissible
- `audit_closure_quotient_rank_zero_aa_bb_wl492_route_selection_after_admissibility_filter.py` — wl492 在 filter 存在且已知 ambient ledger 已过滤后，选择从现有 `M_tail` diagnostics 建候选队列
- `audit_closure_quotient_rank_zero_aa_bb_wl493_candidate_queue_from_existing_m_tail_diagnostics.py` — wl493 从现有 wl481 `M_tail` kernel diagnostics 建队列，并将已处理的 `u_3` 降级/排除出 active queue
- `audit_closure_quotient_rank_zero_aa_bb_wl494_extend_or_refresh_m_tail_diagnostics.py` — wl494 用有界 primitive AA/BB 样本网格刷新 `M_tail` diagnostics，记录新 active supports 与已处理 `u_3`
- `audit_closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.py` — wl495 将 wl494 的 refreshed `v_5` supports 先过 ambient `C_d` solubility，再只对已证全局点应用 wl491 filter
- `audit_closure_quotient_rank_zero_aa_bb_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers.py` — wl496 解决 wl495 两个 deferred `v_5` ambient `C_d` ledgers，记录其共同 `L=4,T=5,d=(5,1,5)` cover 为 globally not soluble
- `audit_closure_quotient_rank_zero_aa_bb_wl497_post_wl496_route_choice_audit.py` — wl497 在 `u_3` 和有界 refreshed `v_5` supports 均已处置后选择下一窄门为 structured `M_tail` diagnostic extension，但不执行该门
- `audit_closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan.py` — wl498 定义下一批 `M_tail` diagnostic extension 的 finite-shell axes、exclusion ledger、duplicate-support guard、未来输出 schema 和 routing contract，但不刷新新网格
- `audit_closure_quotient_rank_zero_aa_bb_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan.py` — wl499 按 wl498 plan 执行 `max(A,B)=5` finite primitive shell，记录 active `u_5` M_tail diagnostic supports，并停止在 ambient `C_d` / wl491 之前
- `audit_closure_quotient_rank_zero_aa_bb_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py` — wl500 将 wl499 两个 active `u_5` supports 路由过 ambient `C_d` solubility；共同 `L=5,T=8,d=(5,5,1)` cover 被记录为 globally not soluble，因此不应用 wl491
- `audit_closure_quotient_rank_zero_aa_bb_wl501_post_wl500_route_choice_audit.py` — wl501 在 shell-5 `u_5` ledgers 均已 refuted 后选择下一窄门为按 wl498 plan 执行下一个 finite `M_tail` shell，但不执行该门
- `audit_closure_quotient_rank_zero_aa_bb_wl502_execute_next_finite_m_tail_shell_from_wl498_plan.py` — wl502 按 wl501 gate 执行 `max(A,B)=6` finite primitive shell，应用 wl498 duplicate guard 和 wl501 closed-ledger exclusions，记录空的 M_tail diagnostic support queues，并停止在 ambient `C_d` / wl491 之前
- `audit_closure_quotient_rank_zero_aa_bb_wl503_post_wl502_empty_shell_route_choice_audit.py` — wl503 在 shell-6 空队列后选择下一窄门为按 wl498 plan 稍后执行 `max(A,B)=7` finite `M_tail` shell，但不执行 shell 7
- `audit_closure_quotient_rank_zero_aa_bb_wl504_execute_next_finite_m_tail_shell_from_wl498_plan.py` — wl504 按 wl503 gate 执行 `max(A,B)=7` finite primitive shell，应用 wl498 duplicate guard 和 wl503 closed-ledger exclusions，记录 shell-7 active/excluded M_tail diagnostic support queues，并停止在 ambient `C_d` / wl491 之前
- `audit_closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py` — wl505 将 12 个 active shell-7 supports 先过 ambient `C_d` solubility，再只对已证全局点应用 wl491 filter
- `audit_closure_quotient_rank_zero_aa_bb_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers.py` — wl506 解决 wl505 四个 deferred shell-7 ambient `C_d` ledgers：两个 refuted，两个 global but not AA+BB-admissible
- `audit_closure_quotient_rank_zero_aa_bb_wl507_post_wl506_route_choice_audit.py` — wl507 在 shell-7 active/deferred ledgers 全部处置后选择下一窄门为按 wl498 plan 执行 shell `max(A,B)=8`，但不执行 shell 8
- `audit_closure_quotient_rank_zero_aa_bb_wl508_execute_next_finite_m_tail_shell_from_wl498_plan.py` — wl508 按 wl507 gate 执行 `max(A,B)=8` finite primitive shell，记录空 active queue 和两个 pure `u_3` processed exclusions，并停止在 ambient `C_d` / wl491 之前
- `audit_closure_quotient_rank_zero_aa_bb_wl509_post_wl508_empty_shell_route_choice_audit.py` — wl509 在 shell-8 active queue 为空且 pure `u_3` outputs 已 processed 后选择下一窄门为按 wl498 plan 执行 shell `max(A,B)=9`，但不执行 shell 9
- `audit_closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan.py` — wl510 按 wl509 gate 执行 `max(A,B)=9` finite primitive shell，记录 8 个 active shell-9 M_tail diagnostic supports，并停止在 ambient `C_d` / wl491 之前
- `audit_closure_quotient_rank_zero_aa_bb_wl511_route_active_shell9_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py` — wl511 将 8 个 active shell-9 supports 先过 ambient `C_d` solubility，再只对已证全局点应用 wl491 filter
- `audit_closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers.py` — wl512 分类 wl511 四个 deferred shell-9 ambient `C_d` ledgers：两个 `v_13` refuted，两个 `u_7` 继续 deferred
- `audit_closure_quotient_rank_zero_aa_bb_wl513_post_wl512_route_choice_audit.py` — wl513 在两个 shell-9 `u_7` ledgers 仍 deferred 后选择下一窄门为 targeted resolution of the shared `L=7,T=16,d=(7,7,1)` cover，但不进入该门
- `audit_closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger.py` — wl514 进入 wl513 选定窄门，用 mod-17 Mordell-Weil sieve no-lift certificate 解决 shared shell-9 `u_7` cover 为 globally not soluble，并停止在 post-wl514 route choice 前
- `audit_closure_quotient_rank_zero_aa_bb_wl515_post_wl514_route_choice_audit.py` — wl515 在 shell-9 deferred ambient `C_d` ledgers 全部分类后选择下一窄门为按 wl498 plan 执行 shell `max(A,B)=10`，但不执行 shell 10
- `audit_closure_quotient_rank_zero_aa_bb_wl516_execute_next_finite_m_tail_shell_from_wl498_plan.py` — wl516 按 wl515 gate 执行 `max(A,B)=10` finite primitive shell，记录 10 个 active shell-10 M_tail diagnostic supports，并停止在 ambient `C_d` / wl491 之前
- `audit_closure_quotient_rank_zero_aa_bb_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py` — wl517 将 10 个 active shell-10 supports 先过 ambient `C_d` solubility，再只对已证全局点应用 wl491 filter
- `audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517.py` — wl518 将 wl491-wl517 ledger outputs 按 support family / cover family 聚合，选择 shared shell-10 `u_5` deferred cover resolution 为下一窄门但不进入
- `audit_closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover.py` — wl519 进入 wl518 选定窄门，用 exact rational ambient `C_d` point 解决 shared shell-10 `u_5` cover 为 globally soluble，并对两个 mirror entries 应用 wl491 后归入 not AA+BB-admissible ledgers
- `audit_closure_quotient_rank_zero_aa_bb_wl520_post_wl519_route_choice_audit.py` — wl520 在 shared shell-10 `u_5` cover 已分类后选择 post-classification support/cover-family synthesis 为下一窄门，但不进入该 synthesis 或执行 shell 11
- `audit_closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis_after_wl519.py` — wl521 进入 wl520 选定 synthesis，按 support/cover family 重聚合 wl491-wl519 ledgers，记录无 deferred/admissible cover family，并只选择后续 finite shell `max(A,B)=11` 而不执行 shell 11
- `audit_closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.py` — wl522 用 wl521 作为 latest state，把 wl491-wl521 ledgers 压成 support/cover taxonomy，区分 ambient refutation 与 AA+BB common-source admissibility failure，并只选择 unproved common-source square obstruction lemma candidate 而不进入证明或执行 shell 11

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
