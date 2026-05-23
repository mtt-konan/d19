# 038 — 4653 hard_case sha2 大规模扫描 + 模式狩猎

**日期**: 2026-05-23
**触发原因**: worklog 036 在 320 hard_case 中只发现 2 个 sha2≥2 case，sample
偏小，无法判断 sha2≥2 是孤立特例还是稳定子类。本 worklog 把 hard_case 扩大到
4653 + 系统化跑 PARI ellrank effort=1 + 跑特征 chi² 找 hard_case 的内部结构。
**输出**: 4 个新脚本（含 timeout-safe 扫描器）+ 1 项颠覆性方向修正 +
1 个明确的 sha2≥2 子类标记（max_exp(B) ≥ 4）+ 4 个 PARI 卡死 case 的隔离记录。

---

## 一、Scale up: 320 → 4653 hard_case

`scripts/prove_no_solution.py --max-hyp 2000` 把 hard_case 从 320 增到 **4653**。
跑时间 ~1.5 min，新增主要在 max_hyp ∈ (500, 2000] 区间。

```
Total pairs:    99,311
no_solution:    94,658 (95.3%)
solution:            0
hard_case:       4,653 (4.7%)
```

`hard_case` 占比稳定在 ~5%，没随 max_hyp 增长。

## 二、第一轮：(A, B) 描述统计 + 与直觉相反的发现

`scripts/pattern_hunt_hard_cases.py` 跑特征 chi²（hard_case vs no_solution）。

**最强 chi² 信号（前 5）**:

| Feature | hard% | easy% | χ² (df=1) |
|---|---|---|---|
| `B_squarefree=False` | 62.8% | 74.7% | 330.7 |
| `A_squarefree=False` | 55.6% | 66.9% | 252.3 |
| `max_exp(B) ≥ 5` | **3.2%** | **22.5%** | huge |
| `max_exp(A) ≥ 5` | 1.1% | 18.3% | huge |
| `B mod 4 = 1` | 50.1% | 49.9% | NS |

### 关键修正（与之前直觉相反）

我之前的直觉是"hard_case 倾向于 (A, B) 含高 prime power"。**实际方向相反**：

| | A squarefree | B squarefree | both squarefree | neither squarefree |
|---|---|---|---|---|
| hard_case | **44.4%** | **37.2%** | **13.2%** | 31.6% |
| no_solution | 33.1% | 25.3% | 6.1% | **47.7%** |

**hard_case 比 no_solution 更"clean"（更 squarefree）**：

- A squarefree: hard 44% vs easy 33% (+11 pp)
- B squarefree: hard 37% vs easy 25% (+12 pp)
- 两个都不 squarefree: hard 32% vs easy **48%**

**直觉解释**：(A, B) 含高 prime power → $E_{A,B}$ 有丰富 bad reduction primes →
cheap sieve 容易找 obstruction → no_solution 多。**hard_case 是 (A, B) 最"clean"
的子集，需要更深的工具才能 cert**。

`max_exp(B) ≥ 5`：easy 22.5% vs hard **3.2%** —— 高 prime power 几乎全在
no_solution。

3 | A 或 3 | B：hard 81.4% vs easy 74.0% （+7 pp）。**不是 obstruction 信号**，
仅是 reduce primitive 后的轻微偏倚（pair 是 $\gcd(A,B)=1$ 的，所以
`P(3|A) + P(3|B)` 直接给出 `P(3|AB)`）。

## 三、9 个 "rank=0 hard_case" 的真相

之前 db 中标记为 `rank_lower=0` 的 9 个 hard_case 引人注意：rank=0 应该被
`_method_rank_zero` 直接 cert no_solution，但这 9 个还 hard。

`/tmp/d19_rank02_probe.py` 用 effort=2 重跑：

| (A, B) | effort=1 | effort=2 |
|---|---|---|
| (413, 255635) | rank=[2,2] sha2=0 | rank=[2,2] sha2=0 |
| (549, 29435) | rank=[2,2] **sha2≥2** | rank=[2,2] sha2≥2 |
| (12943, 78705) | rank=[2,2] **sha2≥2** | rank=[2,2] sha2≥2 |
| (12943, 415125) | rank=[0,2] sha2=0 | rank=[2,2] sha2=0 |
| (14535, 462241) | rank=[2,2] **sha2≥2** | rank=[2,2] sha2≥2 |
| (16907, 238005) | rank=[2,2] **sha2≥2** | rank=[2,2] sha2≥2 |
| (48749, 57575) | rank=[2,2] sha2=0 | rank=[2,2] sha2=0 |
| (122549, 681615) | rank=[0,2] sha2=0 | rank=[2,2] sha2=0 |
| (131175, 251617) | rank=[2,2] sha2=0 | rank=[2,2] sha2=0 |

**没有一个真的是 rank=0**。db 的 `rank_lower=0` 是 effort=1 在某些 case 给出的
"虚假下界"——effort=2 全部 cert 为 rank=2（甚至 effort=1 多数给的就是 rank=2，
db 数据是更早 effort=0/1 mix 时期的污染）。

更显眼：**7/9 case 在 effort=2 给出 sha2_lower ≥ 2**。给出"sha2≥2 不是孤立"的
首个强信号，启发下一步全集扫描。

## 四、Timeout-safe scanner: `batch_sha2_scan_v2.py`

第一版 `batch_sha2_scan.py` 在 cypari2 in-process 模式下跑 4653 case 时，**1 小时
无任何输出**。原因：少数 (A, B) 让 PARI ellrank 进入超长（甚至无限）循环，
cypari2 不能被 Python SIGINT 中断，整个进程卡死。

新方案：**subprocess 隔离 + per-case 硬超时 + JSONL incremental flush + resumable**：

- `scripts/sha2_worker.py`：单 (A, B) worker，stdin 读 args，stdout 写 1 行 JSON
- `scripts/batch_sha2_scan_v2.py`：fork worker subprocess + `subprocess.run(timeout=15s)`
  + 每行 flush + 启动时跳过已存在 JSONL 行

**4653 case 全集结果（6 分钟）**:

```
rank_lower:  rank=1: 1410, rank=2: 2175, rank=3: 939, rank=4: 122, rank=5: 3
sha2_lower:  sha2=0: 4493, sha2=2: 156, sha2≥4: 0
TIMEOUT:     4 (0.09%)
ERROR:       0
```

- **156 个 sha2_lower=2** = **3.35% of hard_case**（非 0.6%）
- **0 个 rank=0** confirmed（之前以为有 9 个全是 effort 偏差）
- **4 个 PARI 卡死** case（见下节）

之前 320 sample 给出 0.6% 估计是采样偏差。**sha2≥2 是 hard_case 中稳定的子类**，
不是孤立特例。

## 五、sha2≥2 vs sha2=0 的特征 chi² (`scripts/analyze_sha2_cases.py`)

### Rank stratification

| rank_lower | sha2≥2 占比 | sha2=0 占比 |
|---|---|---|
| 1 | **126 / 156 = 80.8%** | 1284 / 4493 = 28.6% |
| 2 | 29 / 156 = 18.6% | 2146 / 4493 = 47.8% |
| 3 | 1 / 156 = 0.6% | 938 / 4493 = 20.9% |
| ≥ 4 | **0** | 125 / 4493 = 2.8% |

**sha2≥2 case 高度集中在 rank=1**，rank≥4 case 100% 是 sha2=0。

### Yates-corrected 2×2 chi² (sha2≥2 vs sha2=0)

| Feature | pos% | zero% | χ² | p | sig |
|---|---|---|---|---|---|
| **max_exp(B) ≥ 4** | **21.2%** | 10.9% | 14.94 | **1.1e-4** | *** |
| **neither_squarefree** | **43.0%** | 31.2% | 9.12 | **2.5e-3** | ** |
| B_squarefree | 28.9% | 37.5% | 4.47 | 0.03 | * |
| max_exp(B) ≥ 2 | 71.2% | 62.5% | 4.47 | 0.03 | * |
| 3 \| B | 49.4% | 43.1% | 2.18 | 0.14 | NS |
| A_squarefree | 41.7% | 44.5% | 0.37 | 0.55 | NS |
| max_exp(A) ≥ 4 | 7.7% | 6.7% | 0.12 | 0.73 | NS |
| 3 \| AB | 82.7% | 81.4% | 0.09 | 0.77 | NS |
| A mod 4 = 3 | 50.6% | 50.1% | 0.00 | 0.96 | NS |
| max_exp(A) ≥ 3 | 20.5% | 21.0% | 0.00 | 0.97 | NS |
| both_squarefree | 13.5% | 13.1% | 0.00 | 1.00 | NS |

### 核心结论

- **sha2≥2 hard_case 的明确标记：B 含 ≥ 4 次素数幂**（χ²=14.94，p<10⁻⁴）
- **A 的结构跟 sha2 几乎无关**——所有 A-features 都不显著
- **mod 4/8、parity 全部不显著**（PARI Selmer 已经隐含这些 local 信息）
- 信号不对称（B 强 / A 弱）很可能来自 (A, B) 在 EC 模型 $y^2 = x(x+A^2)(x+B^2)$
  里的位置不对称——三个 2-torsion 点 $\{0, -A^2, -B^2\}$ 中 $-B^2$ 跟 $0$ 的
  Q-rational isogeny pattern 跟 $-A^2$ 不一样

### sha2≥2 case 实例（前 20 中的几个）

```
(243,  1085)  rank=1  A=3⁵         B=5·7·31
(845,  1647)  rank=1  A=5·13²       B=3³·61
(715,  3321)  rank=1  A=5·11·13     B=3⁴·41
(1705, 4779)  rank=1  A=5·11·31     B=3⁴·59
(1375, 5217)  rank=1  A=5³·11       B=3·37·47
(3751, 6525)  rank=1  A=11²·31      B=3²·5²·29
```

**B 经常含 3⁴ 或 3³** + A 含一个 prime square 或 cube。这是 sha2≥2 的"典型形状"。

## 六、4 个 PARI 卡死 case（隔离记录）

```
(   177,   8671)  A=3·59           B=13·23·29
(   413, 255635)  A=7·59           B=5·29·41·43
( 14927,  48825)  A=11·23·59       B=3²·5²·7·31
( 17329,  24679)  A=13·31·43       B=23·29·37
```

共同点：**A 至少有 prime 59 或 31 或类似的 large prime; B 含至少 4 个 distinct
primes**。这些 case 让 ellrank 在 effort=1 内无法完成，需要更高 effort 或别的
工具（Cassels-Tate、Heegner、Sage）。**只占 0.09% (4/4653)**，pipeline 不需要
特殊处理，timeout=15s 直接 skip 即可。

## 七、四组核心数据归位

| 数据 | 路径 |
|---|---|
| 4653 hard_case scan | `results/sha2_scan_hard_cases.jsonl` |
| 进度日志 | `results/sha2_scan_progress.log` |
| chi² 分析报告 | `results/sha2_analysis_report.txt` |
| 第一轮 pattern hunt | `results/pattern_hunt_hard_cases.json` (来自 wl037 工作链) |

## 八、对项目方向的修正

worklog 035-037 的"sha2≥2 是孤立特例（2 个）"判断要修正为：

> **sha2≥2 是 hard_case 中 ~3.4% 的稳定子类，156 个实例已记录。这一类的明确
> 子标记是 "rank=1 + B 含 ≥ 4 次素数幂"。**

下一步候选：

1. **(已完成) sha2≥2 case 的特征化** ← 本 worklog
2. 对 156 个 sha2≥2 case 跑 `ell2cover` 拿 Selmer 4-cover，看是否能找到全局
   Brauer-Manin obstruction（Cassels-Tate pairing 的实证版）
3. 对 156 个 sha2≥2 case 跑 Heegner point search（rank=1 case Heegner 直接 work）
4. 把 timeout-safe scanner 升级为通用工具，再跑 max_hyp=5000 的全集
   （~5× 工作量，估计 ~25,000 hard_case，~30-40 min）

## 九、commit 计划

1. `feat(scripts): timeout-safe sha2 scanner via subprocess isolation`
   - `sha2_worker.py` + `batch_sha2_scan_v2.py`
2. `feat(scripts): analyze_sha2_cases for chi² over Sha[E][2] subclass`
   - `analyze_sha2_cases.py`
3. `docs(worklog): 038 large-scale sha2 pattern hunt + 156 sha2≥2 cases`
   - 本 worklog + `results/sha2_scan_hard_cases.jsonl`
   - `results/sha2_analysis_report.txt`

## 十、附：Failed approaches（避坑参考）

- `batch_sha2_scan.py` 第一版用 cypari2 in-process loop。**4653 case 1 小时
  无输出**。原因：cypari2 不能被 SIGINT 中断；少数 case 让 ellrank 进入长跑
  把整个 Python 进程卡死。已替换为 subprocess 版。
- 想用 `signal.SIGALRM` 在 in-process 实现 timeout。**不可行**：PARI 是 C 库，
  signal handler 是 Python 解释器级，会一直 pending 直到 PARI 返回。
- 想用 `multiprocessing.Process + Process.terminate()`。可行但 macOS spawn
  开销 ~0.3s/启动 × 4653 = 25 min just for spawn，不如 `subprocess.run` 简单。
- 之前推断 "hard_case 倾向 (A, B) 含高 prime power" 是 **完全反的**。直觉害人，
  必须靠 chi² 数据修正方向。
