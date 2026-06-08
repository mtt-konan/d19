# results/ — 输出索引与可信度说明

按主题分目录. 顶层只放主索引 (catalog) + 数据库 + 子目录入口.

## 先读这个：哪些结果能当证据？

这里的文件大多是“实验记录”或“本机快照”，不是数学证明。最容易误读的规则是：

- `authoritative=true` 只表示“这个文件是某个有限范围实验的原始/基准数据”，不表示已经证明全空间无解。
- `proof_status.db` 是本机旧 workflow 快照；当前审计认为它相对 wl094 full-plane closure 和后续 gcd-aware 语义已经 stale。除非重新生成并写明版本，否则不要引用它的 `hard_case/no_solution` 计数当当前结论。
- `chain.db` 是 legacy chain-fast SQLite 库，和当前 chain-fast schema 不匹配；保留作历史线索，不是当前代码可直接复用的权威结果库。
- `catalog.json` 是机器可读目录；如果它和这里冲突，以带有 stale/legacy 说明的新文字为准，并优先重新运行 `scripts/multi_n/build_results_catalog.py`。

## 顶层

| 文件 | 用途 |
|------|------|
| `catalog.json` | 主结果目录 (机器可读索引) |
| `chain.db` | legacy chain-fast SQLite 结果库；历史线索，不是当前 schema 证据 |
| `proof_status.db` (+ shm/wal) | stale proof-status workflow 快照；历史线索，不是当前结论 |
| `proof_status_multi_1m.db` | non-coprime/full-space 相关旧快照；引用前必须核对生成脚本和语义 |
| `proof_status_10k.sqlite3` | 10k 范围 proof status snapshot；若本机存在，按 snapshot/historical 处理 |

## 子目录

### `multi_n/` — multi-N 枚举与目录

| 文件类 | 来源 |
|--------|------|
| `multi_concordant_N_max{N}.jsonl` | wl046 ground truth (max_hyp=10000 是有限范围 authoritative) |
| `multi_concordant_N_max{N}_fast.jsonl` | fast pivot-on-N 扫描 (wl048+) |
| `multi_concordant_N_max{N}_classified.jsonl` | F₂-rank 分类 (wl049) |
| `multi_concordant_N_max{N}_pari_rank.jsonl` | PARI ellrank audit (wl050) |
| `non_coprime_scan_max{N}*.{jsonl,json}` | 非互素扫描 (wl056) |

复现命令见 `scripts/multi_n/`.

### `path_a/` — Path A 实证 (closure fiber + F₂-rank)

| 文件类 | 来源 |
|--------|------|
| `k2_closure_fiber_max{N}.jsonl` | k=2 closure fiber 实证 (wl074, PARI ellrank) |
| `k2_f2_rank_max{N}.jsonl` | k=2 F₂-rank 实证 (wl076) |
| `kn_f2_rank_max{N}.jsonl` | 通用 k=n F₂-rank 实证 (wl084) |
| `kn_f2_rank_max1m_k4plus.jsonl` | k=4 反例数据 (wl084) |

### `path_b/` — Path B mod p² 实证

| 文件类 | 来源 |
|--------|------|
| `dual_closure_max{N}.json` | dual closure sieve (wl073) |
| `uniform_mod_p2_max{N}.jsonl` | uniform mod p² audit (wl078) |
| `wl078_phase3c_crt_*moduli.json` | CRT 合并 mod p² (wl078) |

### `partner/` — Partner graph (G_M) 数据

包含全 G_M BFS, K_n hub, comp 0 拓扑, cycle, full closure scan, 等.

| 文件前缀 | 来源 |
|---------|------|
| `partner_bfs_root*` | 单源 BFS (wl058) |
| `partner_full_*` | 全 G_M BFS (wl061) |
| `partner_pair_*` | pair-level partner 图 |
| `partner_kn_subgraphs.*` | K_n 子图抽取 |
| `comp0_*.{json,png}` | comp 0 拓扑分析 (wl062) |
| `full_gm_*` | G_M 反例彻底搜索 (wl063), delta 统计 (wl066) |
| `k8_ellrank_*`, `k9_*`, `k10_*` | K_n 实例 ellrank (wl060, wl062, wl065) |
| `cycle_ellrank_*` | cycle / deficit 分析 (wl059) |
| `gephi_comp0/` | Gephi 导出 |

### `benchmark/` — 性能基准

| 文件类 | 来源 |
|--------|------|
| `ab_*.json`, `ab_sieve_benchmark_*.json` | proof_status A/B sieve order 基准 (wl067-068) |
| `candidate_generators_max{N}*.json` | 三种候选生成方式对比 (wl072) |

### `archive/` — 历史/废弃方向数据

下面这些都是被 wl 链关闭/废弃的方向, 数据保留作历史:

- `ell2cover_*` — ell2cover / 2-descent (wl036, wl039)
- `sha2_*` — Sha[2] pattern hunt (wl038)
- `finite_descent_*` — finite descent (wl037)
- `hyp_identity_*` — hypotenuse identity (wl034, 假设错废弃)
- `dual_ec_*` — dual EC probe (wl033)
- `ellrank_effort_compare.json` — PARI effort compare (wl036)
- `generator_lattice_*` — generator lattice search (wl044)
- `pattern_hunt_*` — pattern hunt with chi² (wl038)

---

## 主要 jsonl/json 字段约定

每个 multi-N pair 文件每行至少包含:

```json
{
  "A": int, "B": int,
  "concordant_n": [N_1, N_2, ...],
  "k": int                       // = len(concordant_n)
}
```

PARI rank 数据再加:
```json
{
  "rank_lower": int, "rank_upper": int,
  "torsion": "...",
  "sha2_lower": int
}
```

F₂-rank 数据再加:
```json
{
  "f2_rank_pure": int,
  "f2_rank_with_T_A": int,
  "qs_x": [...],
  "qs_sig": [[..., ..., ...], ...]
}
```

---

## .gitignore

大体原则是：大型运行产物和本机 DB 不进 git；README、catalog、少量归档/基准小文件可能已经被跟踪，用于说明 provenance。判断一个文件是否跟踪，用：

```bash
git ls-files results
```

所有可复现实验数据应能通过 `scripts/` 中对应入口重新生成。

需要分享 / 跨机器复现时, 用 rsync / Zenodo / S3, 不要进 git.
