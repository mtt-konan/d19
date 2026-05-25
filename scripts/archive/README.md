# 历史脚本归档

这些脚本对应已经结束或转入 baseline 的实验阶段，不在当前 multi-N / proof_status 主线上。
保留是为了能复现历史结果、回看实验选型理由。

当前主线脚本仍在 `scripts/` 根目录：

```text
prove_no_solution.py            主 proof 入口
search.py                       顶层 search dispatcher
multi_concordant_n_scan.py      慢路 ground truth (wl046)
fast_multi_concordant_scan.py   快路 pivot-on-N (wl048)
validate_fast_multi_n.py        快慢一致校验
classify_multi_n_by_f2_rank.py  F₂-rank 分类器 (wl049)
lookup_multi_n.py               (A,B) 反查
analyze_multi_n_half_points.py  half-point 分析
build_results_catalog.py        catalog 生成
extract_pdf_text.py             文献 PDF→txt
analyze_k4_signatures.py        Phase 2 audit
k4_two_descent_rank.py          Phase 2 audit
k4_rank.py                      Phase 2 audit (PARI ellrank)
```

---

## 分组

### chain / EC db 时代（baseline / paused）

```text
analyze_chain_db.py        chain 数据库的 SQLite 分析（wl021）
analyze_ec_db.py           EC 数据库的 SQLite 分析（wl014）
compare_parametric.py      CPU / GPU parametric 后端对照
visualize.py               results.json → HTML（plotly）
```

### sha2 / dual_ec / ell2cover 时代（wl033-039）

```text
probe_dual_ec.py                双 EC rank 探测主入口
analyze_dual_ec_probe.py        certified vs unproven 区分
deep_rank_recheck.py            effort=2 复核
probe_pari_selmer_api.py        PARI Selmer API 探查
sha2_worker.py                  单 (A,B) sha2 worker（subprocess 隔离）
batch_sha2_scan_v2.py           timeout-safe sha2 扫描器
ell2cover_worker.py             单 (A,B) ell2cover worker
batch_ell2cover_v2.py           timeout-safe ell2cover 驱动
batch_ell2cover_hard_cases.py   ell2cover 在 hard_case 上的批量
ell2cover_height_followup.py    h=10⁵ 复算 outlier
analyze_ell2cover.py            n_covers vs n_without_pt 联合分布
analyze_sha2_cases.py           sha2 hard_case 分析
analyze_hypotenuse_identity.py  hypotenuse 恒等式分析（wl034）
compare_ellrank_effort.py       ellrank effort=0/1/2 对照
probe_chain_closure_mod_sieve.py
                                chain closure 在 mod p² 上的筛子探针
pattern_hunt_hard_cases.py      hard_case 特征猎取（卡方）
```

### finite-descent / generator-lattice 实验（wl037, wl044）

```text
finite_descent_hard_cases.py    finite descent 在 hard_case 上
finite_descent_layer2.py        layer-2 嵌套
generator_lattice_search.py     X1 generator lattice 搜索（wl044）
find_h_3mod4_counterexamples.py 假设性反例搜索
```

---

## 当前 docs/work-logs/archive/ 索引

需要查这些脚本对应的实验记录：

- chain / EC db：wl014, wl021
- sha2 / dual_ec / ell2cover：wl033-039
- finite descent：wl037
- generator lattice：wl044

worklog wl001-027 也已归档，详见 `docs/work-logs/archive/README.md`。
