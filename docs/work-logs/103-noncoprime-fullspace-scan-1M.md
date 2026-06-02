# wl103 — 非互素全空间扫描推到 hyp≤1M（优化 + 阶段3）

接 wl102。把扫描优化到可上 1M，并跑出阶段3。

## 优化（脚本 `scripts/multi_n/noncoprime_full_scan_fast.py`）

- **生成**：Cython 核 `_concordant_gen.generate` 出 (A,N) 关系流；新增 `emit_pairs(..., coprime_only=False)`
  参数（默认 True 向后兼容）覆盖非互素半空间。numpy 排序/去重提取 multi-N 对，结果存成
  **int64 pkey 数组**（pkey=A·factor+B，~8 B/对），不再用会 OOM 的 Python 关系字典。
- **判定**：sound 三段管线 `gcd_aware_kills → chain_closure 模 p² → GEN-CLOSURE`
  铺到 `--workers` 个进程，每进程只解码自己那段 pkey、返回聚合计数（IPC 极小）。
- **验证**：在 100k 上与单线程 `noncoprime_full_scan.py` 结果**逐位一致**
  （324,925 对 / 非互素 314,592 / ①200,707 ②104,999 ③19,219 / 0 闭合），用时 122 s → 57 s（2 进程，生成 12 s→0.5 s）。

## 阶段3 结果（max_hyp=1,000,000，2 进程，1037 s）

| 项 | 数 |
|---|---|
| multi-N 对总数 | **4,951,985** |
| 互素 | 111,090 |
| **非互素** | **4,840,895** |
| ① D_g 筛杀 | 3,001,807 |
| ② chain_closure 模 p² 杀 | 1,617,805 |
| ③ GEN-CLOSURE 残余 | 332,373 |
| **闭合命中（反例）** | **0** |

- **互素对数 111,090 与历史 1M 互素 multi-N 计数完全吻合**（`proof_status_multi_1m.db`）→ 去过滤后生成器对互素半空间无回归，强一致性检验。
- **0 闭合**：首次给出**同时覆盖互素 ∪ 非互素**到 hyp≤1M 的"无反例"声明。非互素多-N 对从 wl102 的
  314,592（hyp≤100k）推到 **4,840,895（hyp≤1M）**；相对最早只有 1,802（hyp≤2000）已扩大 ~2,685×。
- 残余 gcd 仍 `12∣g` 主导（g=12: 20,275、60: 16,888、24: 12,962、120: 10,629…），与 wl100 的 local-global 残余同构；全部经完备 GEN-CLOSURE 判定 0 闭合。

## 性能 / 后续

1M 用时 ~17 min（生成 10.7 s，判定 ~1026 s 在 2 核上；瓶颈是 ② chain_closure 对每个对算残基）。
推 5M 单机约需数小时（线性外推），届时可加更多核 / 分片落盘断点续跑。

## 产出

- `scripts/multi_n/_concordant_gen.pyx`（`emit_pairs` 加 `coprime_only` 旗标）
- `scripts/multi_n/noncoprime_full_scan_fast.py`（优化并行扫描）
- `results/multi_n/full_scan_max1000000.json`
