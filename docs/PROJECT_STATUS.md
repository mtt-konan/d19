# 项目现状

这份文档只回答三件事：

- 项目现在主要推进哪条线
- 其它路线现在处于什么状态
- 当前真正的瓶颈是什么

如果想看完整方向地图，请先看 [docs/DIRECTIONS.md](./DIRECTIONS.md)。
读 §9.x（PARI / 沙群 / Selmer 相关）时英文术语查 [docs/GLOSSARY.md](./GLOSSARY.md)。

## 一、当前主线已经定下来了

目前统一口径是：

- `concordant` = `active`
- `chain-fast` = `baseline`
- `parametric` / `ec` / `chain` = `paused`

大白话就是：

- 现在真正值得继续深挖的，是 `concordant` 这条数学线
- `chain-fast` 继续保留，负责做主问题基线搜索和实验对照
- `parametric`、`ec`、`chain` 不删，但暂时不作为当前推进重点

## 二、为什么把 `concordant` 设成主线

原因不是它代码最多，而是它更接近现在真正卡住的问题：

- `chain-fast` 已经证明了“直接穷举 pair + 工程优化”这条路可以稳定跑
- 但它的主复杂度还是 `O(n^2)`，继续堆工程只能慢慢推上限
- 想明显减少 pair，更有希望的是先从数学上找必要条件

`concordant` 这条线研究的是：

- 固定 `(A,B)`
- 看是否存在共同腿 `N`
- 使得 `N^2 + A^2` 和 `N^2 + B^2` 同时是平方

这条路更像是在问：

- 哪些 `(A,B)` 从一开始就不值得配
- 哪些结构即使能过后两条，也根本回不去完整四边闭环

这正是后面想减少搜索空间时最需要的东西。

## 三、`tmp.txt` 和现在的 `concordant` 其实是一条线

这里之前最容易让人混乱，所以单独写清楚：

- `tmp.txt` 里讨论的，是“从 chain 结构出发，推到固定 `(A,B)` 与共同腿 `N`”
- 现在代码里的 `concordant`，是“先把 `(A,B)` 当输入，再做 concordant / 椭圆曲线分析，并检查和 chain 条件是否兼容”

所以它们不是两条彼此无关的新方向，而是**同一条数学路线的两个切面**：

- `tmp.txt` 更偏从四边结构往里推
- `concordant` 更偏固定 `(A,B)` 后做数论分析

项目现在把这两部分统一归到 `concordant` 主线下。

## 四、其它路线现在分别扮演什么角色

### 1. `chain-fast`：主问题基线

它现在仍然非常重要，因为：

- 它直接对准四顶点正方形主问题
- 它是现在最可信的完整搜索器
- profile、near-miss、结构桶统计这些工程底座都已经在这里

但它现在更适合承担这两个角色：

- 做基线搜索
- 给 `concordant` 和后续数学剪枝提供对照数据

它不再是“唯一主线”，而是 `baseline`。

### 2. `chain`：保留作结构参考

`chain` 更像“长方形问题”或“四条勾股边闭环”这条线。

它帮助过项目完成：

- 交叉乘积族排除
- chain 化简
- 从四边结构走到 `(A,B), N` 视角

但在当前阶段，它更像背景路线，不再单独推进。

### 3. `parametric` 和 `ec`：三顶点研究区

这两条线主要还是三顶点研究：

- `parametric` 是最直观的三顶点基线
- `ec` 是从 seed 出发沿椭圆曲线扩展

它们对验证、种子、结构理解仍然有价值，但目前没有证据说明继续深推它们会直接突破四顶点主问题。

## 五、当前已经明确的瓶颈

### 1. 工程瓶颈

`chain-fast` 的主复杂度仍然是 `O(n^2)`。

这意味着：

- 搜索范围扩大一点，pair 数会很快暴涨
- `numpy`、多进程、数据库只能改善常数，不能改变增长趋势

### 2. 数学瓶颈

现在最缺的不是“还能不能再多跑一点”，而是：

- 能不能证明某些 pair 根本不可能
- 能不能把 `(A,B)` 的可行性提前说清楚
- 能不能从共同腿 `N` 的结构里推出更硬的必要条件

这也是为什么当前主线转向 `concordant`。

### 3. 数据与工程边界

项目最近已经补上了一些很有用的工程信息：

- `chain-fast` profile 让耗时分布更清楚
- SQLite 让长跑、resume、结构聚合更容易管理
- 结构桶统计已经开始出现稳定信号

但这些东西目前更像“采证据”，还不等于已经得到可证明的新剪枝。

## 六、当前最合理的推进方式

下一阶段更合理的顺序是：

1. 把已经落地的 `concordant --safe-pair-sieve` 当作“完整链导向”的快路径，继续跑更大范围的批量诊断。
2. 在这条更快的批量路径上，继续整理哪些 pair 仍然能活到后面，给下一轮更深的数学筛提供样本。
3. 继续把 `chain-fast` 当作 baseline，用来验证任何新必要条件有没有误杀真候选。
4. 暂时不把主要精力放在 `parametric`、`ec`、`chain` 的继续扩展上。

如果只是想知道“现在先看哪条线”，结论很简单：

- 先看 `concordant`
- 再把 `chain-fast` 当对照基线
- 其它路线先放着，不删除，也不当主战场

## 七、`concordant` 主线的眼下最近一步

这一步已经不是“计划中”，而是已经做完并验证过了：

- 旧的 pair 级 `mod1680` 前筛已经确认是空筛，只保留实验记录
- 新的一阶工程前筛改走 2-adic 必要条件
- 对当前 reduced `(A,B)` 批量入口，已经用下面三个条件做成实验开关 `--safe-pair-sieve`：
  - `A` 为奇数
  - `B` 为奇数
  - `(A + B) % 4 == 0`

这样做的原因很实际：

- 默认 `concordant` 语义仍然保留“全量 concordant 视图”
- 但一旦要做“完整链导向”的批量加速，就终于有了一条数学上站得住、而且实测有效的前筛，而不是继续押空筛

当前已经拿到的直接结果是：

- `max_hyp=2000` 时，原始 `99311` 个 pair 会先被砍到 `8220`
- `time_find_concordant_s` 从 `96.4s` 降到 `7.7s`
- 默认模式和实验模式的语义差别也已经收清楚：
  - 默认模式看全量 concordant 现象
  - 实验模式专门看“完整链导向”的候选

### 7.1 `proof_status` 的 AB sieve 排序基准：这是工程子方向，不是项目只剩这一件事

在 `(A,B)` / `proof_status` 这条线上，最近又做了一轮 AB sieve 顺序 benchmark。
它的目标不是改变当前默认 pipeline 的语义，而是回答：如果后续继续做更大规模的
`(A,B)` 诊断，前面的安全筛和低成本判定应该怎样排，wall time 最省。

当前这条实验线已经比较稳的结论是：

- 第 1 位基本锁定：`safe_sieve`
- 第 2 位基本锁定：`chain_closure_mod_sieve`
- 原来拆开的第 3 / 第 4 层现在已经合并回默认 `factor_concordant`
- 因此默认 core 排序问题已经收口成 3 层，也就是 `3! = 6` 种顺序

这部分一定要和项目总线区分开：

- 它只是 `proof_status` / `(A,B)` 分支里的一个工程调度问题
- 它服务于更快地枚举、诊断、落库
- 它不等于项目已经收敛成“只剩 benchmark 调顺序”
- `chain-fast` baseline，以及 Heegner / Chabauty / Brauer-Manin / K3 等更硬的数学方向，仍然是项目整体后续的一部分

如果后续有人接手这条分支，最合理的继续方式是：

1. 默认 benchmark 直接按 3 层 / 6 排序来理解
2. 如果只想复查旧的 split 问题，再用 `head_only` / `safe_top2_only`
3. 把这条线当作 `(A,B)` 批量诊断的加速手段，而不是把它误当成主问题已经解决的信号

## 八、长期方向：跳出“加速搜索”的范式

上面几节说的都还是工程范式内：把现有搜索器跑得更快、加更多筛、积累更多数据。

但要看清现在真正卡在哪——项目跑了这么久，已经基本确认：

- 单纯的工程优化在 `O(n^2)` 复杂度面前只是常数改善
- 现有的局部筛（`mod 8`、近期实验中的 `mod p^2`）能砍空间，但**不能证明无解**
- `concordant` 椭圆曲线的 rank 过滤器实测过滤率为 0%，说明仅靠 rank 看是看不出 pair 不行的

更接近“撬动 Harborth 猜想本身”的几条线（详见 [THEORY_DIRECTIONS_ADVANCED.md](./THEORY_DIRECTIONS_ADVANCED.md)）：

- **Heegner 点直接构造**（方向五）：把 rank=1 的 generator 用解析公式直接算出来，
  看其 X 坐标是不是平方数。这是把**过滤器变判定器**。
- **Chabauty / Quadratic Chabauty**（方向七）：把 chain 系统翻译为高亏格曲线，
  在 `rank < genus` 时**枚举所有有理点**。
- **Brauer–Manin 障碍**（方向八）：从 Hasse 局部-整体原理失效切入，
  可能直接证明某类 pair 全局无解。
- **K3 曲面 / Mordell–Weil lattice**（方向十）：把 4-cycle 系统看作高维代数簇，
  用 lattice 高度下界**直接证明搜索范围内不存在解**。

诚实评估：这些方向**短期内不会让搜索更快**，需要 SageMath / Magma 重型工具栈。
但它们是当前已知的、最有可能跳出 “O(n²) 暴力 + 局部筛” 范式的方向。

工程上最容易上手的是**方向五（Heegner 点）**，理由是 SageMath 已有现成 API，
对单个 `(A,B)` pair 的判定可能是 O(1) 解析公式。

## 九、2026-05 实证进展（worklog 033–035）

本月对 `docs/archive/CHAIN_STRUCTURE_IDEAS.md`（已归档）列出的 4 个数学想法做了系统性实证。
**主线不变**（仍是 concordant），但若干新结论确认或排除了具体路径，并暴露
出一个项目级 bug。

### 9.1 想法 4（对偶 EC）：实证否定（[wl 033](./work-logs/033-dual-ec-probe.md)）

在 150 个 D4-distinct chain near-miss 上跑 dual EC `E_{b,d}` 的 rank：

- **0 个 certified rank=0** dual EC（即想法 4 期望的 "free obstruction" 不存在）
- 11 个 `default ellrank` 报 rank=0 的候选，用 `effort=2` 复核后**全部升级到 rank=2**
- 项目级教训：cypari2 `ellrank` 默认 effort 太浅，会系统性给出虚假 `lower=0`

### 9.2 想法 1（hypotenuse 恒等式 + blocker prime）：部分确认 / 部分否定（[wl 034](./work-logs/034-hypotenuse-identity.md)）

在 1005 个长方形 4-chain (`max_val=5000`) 上：

- **代数恒等式 A 和 C 数值 100% 通过验证** ✅（chain 结构的真实代数贡献）
- **IDEAS §2.4 的"$h_i$ 奇素因子 ≡ 1 mod 4"假设错误** ❌
  - Fermat-Euler 只对 *primitive* Pythagorean triple 的 hypotenuse 成立
  - non-primitive 的 hypotenuse $kh$ 继承 scale $k$ 的任意素因子
  - 反例：$(66, 88, 105, 360)$ 的 $h_1 = 110 = 2 \cdot 5 \cdot \mathbf{11}$
- 因此 §2.4 的 blocker prime 论证不成立

### 9.3 想法 3（2-descent）：工具就绪（[wl 035](./work-logs/035-pari-selmer-api.md)）

原计划装 SageMath（1–2 天工作量）。实测发现 PARI 自带工具已足够：

- `pari.ellrank(E, effort)` 返回 **4 元组** `[rank_lo, rank_hi, sha2_lo, gens]`，
  现行 `concordant.analysis.compute_rank` 只用前 3 项 ← **项目级 bug**
- `pari.ell2cover(E)` 直接给出 Selmer 群的 quartic covers（= Sage `E.two_descent()`
  的核心输出）
- 读完 Peschmann 2026 §6 + §7 后澄清的关键事实：**chain candidate 在 dual EC
  上自动落入 trivial 2-descent class**——这从理论上解释了 wl033 的 dual EC
  失败为何是必然而非巧合

工作量从"装 Sage 1–2 天"降为"在 PARI 上跑 batch + 实现 finite-descent"，
是 worklog 036 的目标。

### 9.4 长期方向列表更新（§8 补充第 5 条）

在原列表（Heegner / Chabauty / Brauer-Manin / K3）外加：

- **方向 N：PARI 内置 2-descent + finite-descent on hard_case**（无需 Sage）
  Peschmann §7(2) 的 "modular search on lattice + 45 primes < 200" 思路
  在 d19 上的对应物。是 d19 现有 safe_sieve（mod 1680, ~5 primes）的自然
  扩展版本。

### 9.5 chain ≠ cuboid 的算术结构差异

| | Peschmann (cuboid) | d19 (chain, wl 034) |
|---|---|---|
| 主导素因子 mod 4 | 88.4% $\equiv 1$, 0% $\equiv 3$ | 大多数因子里 $\equiv 3$ 占多数 |
| Selmer trivial class | 主要 obstruction 来源 | chain candidate 自动落入，无 obstruction |

这定量验证了"chain 不是 cuboid"——Peschmann 风格的经典 Selmer obstruction
**不直接适用**于 chain candidate，d19 需要找自己问题特有的 obstruction。

### 9.6 compute_rank bug 修复 + 320 hard_case Selmer 实证（[wl 036](./work-logs/036-compute-rank-fix-and-ell2cover-batch.md)）

修了 wl035 标记的项目级 bug：`compute_rank` 现在返回 4 元组
`(rank, (lower, upper), sha2_lower, gens)`，默认 `effort=1`（实测在 hard
case 上 +33% time 换 7/7 certified vs effort=0 的 1/7）。`ConcordantResult`
也加了 `sha2_lower` 字段。194/194 测试通过。

在 320 hard_case (max_hyp=500) 上跑了 ell2cover + ellrank 批量（3.6s 总）：

- 公式确认：`n_quartic_covers = rank + 2 + sha2_lower`（318/318 sha2=0 + 2/2
  sha2=2 全满足）
- **新发现**：2 个 hard_case 有非平凡 Sha[2]（sha2_lower=2）：
  - $(A, B) = (243, 1085)$
  - $(A, B) = (3969, 15895)$
  - 两个都是 rank=1，给出 5 个 quartic covers（不是 rank=1 普遍的 3 个）

这是项目第一次显式追踪到 Sha[2] 信息——是 wl036 4-tuple bug 修复的直接收益。

### 9.7 Finite-descent 在 320 hard_case × N ≤ 10^8 上零候选（[wl 037](./work-logs/037-finite-descent-on-hard-cases.md)）

实现 Peschmann §7(2) 风格的两层 modular search：

- **Layer 1** (per-prime universal blocker probe，46 primes < 200，0.1s):
  0/320 hard_case 被某 prime 简单阻挡; log_density ∈ [-61, -54]，median ≈
  $e^{-58} \approx 10^{-25}$，heuristic 上 N ≤ $10^{25}$ 才期待出现单个候选
- **Layer 2** (CRT-merged mod 30030 sieve + 精确 N 枚举，N ≤ $10^8$，58s):
  全 320 hard_case 上 0 chain-compatible N，$4.82 \times 10^8$ N 通过 sieve
  后用精确平方判定 + 4-chain closure 检查全部排除

**实证 lemma (effective)**: 对 max_hyp=500 的全部 320 个 hard_case $(A, B)$，
不存在整数 $N \in [1, 10^8]$ 使 $N^2 + A^2$ 和 $N^2 + B^2$ 都是平方且
$b = A+B-N \geq 1$ 给出有效 4-chain closure。这把 d19 的 ec_bound 从 $10^5$
推到 $10^8$（×1000），完全可复现，58s 一次。

观察：concordant N 大量出现（每 hard_case 在 $N \leq 10^8$ 内至少 1 个），
但几乎全部 degenerate（$A+B-N \leq 0$ 或剩余两个平方条件不满足），定量印证
chain 问题 vs cuboid 问题在 closure constraint 上的本质区别。

### 9.8 4653 hard_case Sha[2] 大规模扫描 + 模式狩猎（[wl 038](./work-logs/038-large-scale-sha2-pattern-hunt.md)）

把 hard_case 从 320 → **4653**（max_hyp=2000），用 timeout-safe subprocess
scanner（`scripts/batch_sha2_scan_v2.py` + `sha2_worker.py`）跑全集 PARI
ellrank effort=1，6 分钟完成：

- **rank=1: 1410, rank=2: 2175, rank=3: 939, rank=4: 122, rank=5: 3** （0 个真 rank=0）
- **sha2_lower=2: 156 个 (3.35% of hard_case)**，sha2≥4: 0
- TIMEOUT: 4 (0.09%)，ERROR: 0

之前 wl036 在 320 sample 上找到的 2 个 sha2≥2 是统计正常波动 (0.6% vs 3.4%)，
**sha2≥2 不是孤立特例，是稳定的 hard_case 子类**。

**chi² 找到 sha2≥2 的明确子标记**:

| Feature | sha2≥2% | sha2=0% | χ² | p |
|---|---|---|---|---|
| max_exp(B) ≥ 4 | **21.2%** | 10.9% | 14.94 | **1.1e-4** |
| neither_squarefree | **43.0%** | 31.2% | 9.12 | **2.5e-3** |
| B_squarefree | 28.9% | 37.5% | 4.47 | 0.03 |
| A 的 features | — | — | — | NS |
| mod 4 / mod 8 | — | — | — | NS |

**sha2≥2 的明确形状：rank=1 (80.8%) + B 含 ≥ 4 次素数幂 + A 任意**。这条公式
能在 ~1ms 不调 PARI 的情况下圈出"高概率 sha2≥2 候选"——给后续 Cassels-Tate /
Heegner work 列出 priority queue。

**意外修正**：之前以为"hard_case 倾向于 (A, B) 含高 prime power"。**实际相反**：

- A squarefree: hard 44% vs easy 33%
- B squarefree: hard 37% vs easy 25%
- max_exp(B) ≥ 5: hard 3% vs easy **22%**

(A, B) 含高 prime power → 丰富 bad reduction → cheap sieve 易杀 → 进 no_solution；
hard_case 反而是"clean" pair 的子集。

### 9.9 ell2cover 实证 BM-obstruction + 2-Selmer 结构公式（[wl 039](./work-logs/039-ell2cover-sha2-explicit.md)）

在 156 sha2≥2 case 上跑 PARI `ell2cover(E)` + `hyperellratpoints` (h=10⁴ 然后
h=10⁵)，11 秒跑完：

- **156/156 都至少有 ≥1 个 cover 没有有理点** → 100% explicit Sha[E][2] candidate
- 两条 deterministic 规律：
  - **`n_covers = rank + 4`** 完美匹配 `dim Sel(E,2) = rank + dim E[2](Q) + dim Sha[2] = rank + 2 + 2`
  - **PARI ell2cover 输出顺序严格分层**：先 E(Q)/2E(Q) image cover，后 Sha + 高度大的 generator pullback

**outliers (n_without_pt ≥ 4) 是 9 个 case，全部 robust**：

- h=10⁴ 跟 h=10⁵ 完全一致（9/9 STAY） → 不是 height search 假象
- effort=1/2/3 的 sha2_lower 全部 = 2 → 不是 effort 太低看不到更高 sha2
- 解释：generator 在 cover-pullback 后 height ≫ 10⁵，需要 Heegner-level 工具

**修正**：之前以为 n_without_pt 直接量度 Sha 维度。实际 `n_without_pt = sha2 + k(h)`，
其中 k(h) 跟 generator 在 cover 上 lift-height 相关。

**156 case 的 Sha[E][2] dim 全部 = 2**——是 sha2≥2 hard_case 子集的稳定 invariant。

下一步候选：
- Heegner / Stoll 高度 sieve 在 9 outliers 上 cert no_solution
- max_hyp=5000 scale up（156 → ~750 sha2≥2 case）验证公式在更大 sample
- (169, 235) deep-dive：手算 quartic `-5279x⁴ - 17626x³ + 25673x² + 27418x - 2831`
  的 local solubility everywhere → 直接 cert "explicit Sha[2] generator"

### 9.10 Chain-closure mod p² 联立筛：hard_case 砍 99.6%（[wl 040](./work-logs/040-chain-closure-mod-sieve.md)）

之前所有 sieve（wl037 含 46 个 prime $< 200$）**只筛 N 不筛 b = A+B-N**。
本 worklog 把对称约束改成 mod p² 联立筛：

> $N \bmod M \in T(A,B,M) \cap \bigl((A+B) - T(A,B,M)\bigr) \pmod M$

其中 $T = \{n : n^2+A^2, n^2+B^2 \text{ 都是 mod } M \text{ 的平方}\}$。
对某 $M$ 这个交集为空 → 不存在 chain 解。**Unconditional obstruction**，0 误杀。

实测（14 个 prime square, $p \in [3, 53]$，~50 µs per pair）：

| max_hyp | 之前 hard_case | 现在 hard_case | 砍 % |
|---|---|---|---|
| 500   | 320   | **2**   | **99.4%** |
| 2,000 | 4,653 | **18**  | **99.6%** |

剩下 18 个就是真正"硬"的 case，不再被噪声淹没。可以集中力量上 Heegner /
Chabauty / Brauer-Manin。

**重要更新**：方向五 Heegner 之前估计能砍 ~37% hard_case（rank=1 子集），
现在 hard_case 砍到 18 个，方向五能升级的绝对数量从 ~118 降到 ~6。但
**剩下的就是 deep theory 真正应该攻的目标**。

### 9.11 Parallel pipeline + max_hyp=10000 scaling（[wl 041](./work-logs/041-parallel-pipeline-and-max-hyp-10k.md)）

接 wl040 后立刻把 pipeline 并行化（multiprocessing + batched commit），
把 max_hyp=10000 的全 pipeline 时间从估计的 30-60 分钟压到 **1m25s**
（8 workers, 599% CPU）。

| max_hyp | pair 总数 | hard_case | wall time | 加速 |
|---:|---:|---:|---:|---:|
| 500   | 6.2k    | 2   | 0.4s   | — |
| 2,000 | 99.3k   | 18  | ~3s    | — |
| 5,000 | 617.4k  | 77  | 19s    | ~20× |
| **10,000** | **2.5M** | **326** | **1m25s** | **~25×** |

**hard_case 比例稳定 ~0.01%**，2.5M pair 上 0 chain 反例。

326 hard_case 的 ell2cover/rank 分布（max_hyp=10000，6.6 秒）：

- rank=1: 88 (Heegner 目标)；rank=2: 146；rank=3+: 92；**0 个 rank=0**
- **sha2_lower=2: 13 (4.0%)** — chain_closure_sieve 砍掉了大量 sha2=0 的
  "简单 local 障碍" case，留下来的 hard_case 中 sha2≥2 比例从 wl036 的
  0.6% 升到 4.0%
- 公式 `n_quartic_covers = rank + 2 + sha2_lower` 326/326 完全成立

326 case 的 chain refutation 检查：0 反例。326 全部都是 "唯一/极少 concordant
N + chain closure 失败" 的 local-global gap 样本。
