# Open Directions — 可做但未实施的方向汇总

本文件系统收录从 wl001 到 wl092 中提到的"下一步 / 后续 / 待做 / 候选"
方向，按可行性 + ROI 分类。每条标注 **出处 wl**, **可行性**, **预估工作量**。

更新时间: wl092 之后. 维护原则: 落地一项就把状态标 ✅/🛑（保留作记录），
添加新发现的方向时直接 append 到对应分类下.

> 📍 想看「所有方向如何彼此衍生、各自为何关闭」的叙事/脉络视图，见
> [`EXPLORATION_MAP.md`](./EXPLORATION_MAP.md)（探索脉络图）。本文件是逐条可执行清单。

---

## 现实情景判断 (2026-05, wl084 之后)

**严格证明卡点**: A1 不严格 (wl084), path B 关闭, 三大重剩余路径都需要重大投入:
Brauer-Manin (协作者), Magma quadratic Chabauty (拒装), Stoll-Bruin Chabauty (调研).

**不引入新工具时, 真正"能继续做"的有意义工作分三类**:

1. **工程加速 max_hyp**: 推到 10M-30M 给 empirical 信心, 但**不构成证明**
2. **低成本非工程方向**: A.2 / A.3 / A.5 / D.1 — 真有可能突破的代数 / 数据工作
3. **写 conditional paper**: "假设 A1 成立, 则 ..." 形式的论文

**关于"找高 k pair 出反例"这个直觉 — 没据**:

数据显示高 k 既不增加也不减少反例概率, 详见 A.7 §警告. 不要把
"高 k 更易出反例" 或 "反例倾向出在小 k" 当 established fact. wl066 |Δ|=1
sample (10 个) k 分布跟总体 k 分布几乎一致, 没有任何 k 维度的偏好.

A.7 (D-scaling 快速生成器) 仍值得做, 但理由是:
- per-point closure-check 信号密度 (K_10 ≈ 45 × k=2)
- 给 A.1 (K_n hub partner identity) 提供 sample
- **不是** "更高反例概率"

---

## 分类

- **A. 理论方向 — 真正没尝试过 (新角度)**
- **B. 理论方向 — 已尝试但未完成 / 已被否定**
- **C. 工程优化 — 未实施**
- **D. 数据 / 实证 — 未实施**
- **E. 图论 / partner network — 未实施**
- **F. 文献 / 形式化 — 未实施**

可行性图例:
- ⭐⭐⭐ 立即可做，工具齐全
- ⭐⭐  需要中等开发或学习
- ⭐    需要外部工具 / 协作 / 重大投入
- 🛑   已被验证否定 / 关闭

---

## A. 理论方向 — 真正没尝试过 (新角度)

### A.1 K_n hub partner identity 推广 ✅ 已实现 (wl089) — informative negative

**结论 (wl089)**: 28 个 hub / 49 条边的 shared concordant 点 Q_N 在各自曲线上
**49/49 全 2-可除**（同 A.2 的墙）——hub「共享」不带来跨边代数障碍，无法区分反例。
配套 A.6：shared_partner K_n ⟺ partner pair 本身是 k≥n multi-N（17/17 对偶成立），
general K_n 上限仅到 K_3。顺手修了 wl086 `compute_rank` 把 PARI 有理坐标 generator
`int()` 截断的真 bug（约 40% 曲线误报 "point not on E"），新增 `compute_rank_exact_points`
+ 回归测试。脚本 `scripts/partner/kn_partner_identity.py`。**作为「找新必要条件」关闭。**

下面保留原始设计记录作 reference。

**出处**: wl080 §六, wl062, wl059

**思路**: K_n hub 是 G_M (partner graph) 中 n 个 vertex 共享一组
multi-N. wl080 提到"看 K4/K5 的 partner identity 能否 push 类似 path A
的论证到更高 k". 核心想法: K_n hub 中 n vertex 的 (A_i, B_i) 共享 N
们, 它们的 half-points 在 Mordell-Weil lattice 上有特殊代数关系
(类似 wl059 的 cycle deficit).

**为何没做**: wl080 关闭 path B 后直接进入 path A k=2 严格化, 没回头
做这个. wl062 找到 K_9, K_10 hubs 但没做代数分析.

**怎么做**:
1. 取一个 K_4 hub (如 catalog 中找), 列出 4 个 vertex 的 (A_i, B_i, N_i set)
2. 对每对 vertex 算 partner identity 关系
3. 找 4 vertex 共同满足的代数 invariant
4. 看是否给 closure 失败的代数 obstruction

**风险**: K_n hub 在 reduced coprime safe-pass 中**没有 K≥5** (max_hyp=2M),
推广可能仅适用 partner-only (非互素) vertex.

**工作量**: 1-2 周

---

### A.2 cycle linear relation 追踪 ✅ 已实现 (wl086) — 不构成障碍

**状态**: wl086 落地。模块 `src/rational_distance/concordant/cycle_relations.py`,
CLI `scripts/multi_n/cycle_relations.py`, 测试 `tests/test_cycle_relations.py`,
结果 `results/multi_n/cycle_relations_wl058.jsonl`。见
`docs/work-logs/086-cycle-linear-relations-A2.md`。

**结论 (negative but informative)**: 把 8 个 wl058 6-cycle pair 的 Q_N 全部
表成 generator 整数组合并逐条精确验证。发现:
1. **每个 Q_N ∈ 2·E(ℚ)** (ellisdivisible 确认, 8/8 普遍) —— 因为
   `(x, x+A², x+B²)=(N²,□,□)` 是 concordant 定义, descent class 恒为 (1,1)。
2. 所有 cycle 关系被 2-可除性 + 坐标秩亏**完全解释** (#relations == k − coord_rank, 8/8)。
3. 真正的 deficit 是 k − coord_rank (非 k − MW_rank); (153,560) 的 deficit=0
   仍有关系。

因为 2-可除性对**任何** concordant 点都成立 (无关 closure), cycle 关系**不能
区分反例**, 故 A.2 作为"找新必要条件"的路线关闭。它在 MW 格层面重新确认了
wl035 / CURRENT_FINDINGS §5.2 的 2-descent 平凡性。

---

### A.3 Heegner sieve on closure-failure outliers ⭐⭐

**出处**: wl039 §下一步 (高优先), wl040 §下一步 3

> ⚠️ wl092 注：步骤 3（“generator + height bound 枚举所有 N candidate”）**不必做**。
> `factor_concordant`（`factor_search.find_concordant_by_factorization`）已穷尽枚举
> 全部 concordant 整数 N（全 rank、无 height bound），rank=1 有界扫描是其严格子集；
> height 上界本身又已被 B.6/wl077 判不通。若要处理 9 个 outlier，直接用 `factor_concordant`
> 判定即可，无需 Heegner/height。

**思路**: wl039 发现 9 个 outlier "PARI 找到 gen 但 hyperellratpoints
找不到 cover-lift". 这些是 closure 失败的最弱 case. Heegner point 在
rank=1 上 effective (PARI ellheegner 直接可调).

**为何没做**: wl040 转去做 chain_closure_mod_sieve, 把 9 个 outlier
挂起.

**怎么做**:
1. 取 9 个 outlier (results/ell2cover_sha2_*.jsonl 找)
2. 对每个 pair 运行 `ellheegner` 试找 generator
3. 用 generator + height bound 枚举所有 N candidate

**工作量**: 1 周内 (PARI 直接做)

---

### A.4 Brauer-Manin obstruction 探索 ⭐ (但定向)

**出处**: wl040 §下一步 4, wl043, wl075 方向 4

**思路**: 学术合作级别. closure-fiber 的 Brauer-Manin 障碍.

**为何没做**: 工作量极大, 需要专业代数几何背景或合作者.

**估算**: 数月 + 合作者. 不优先.

---

### A.5 扩 safe_sieve 到 Peschmann §7(2) 规模 🛑 关闭 (wl091)

**结论 (wl091)**: 不值得做，三条实测支撑：(1) Peschmann §7(2) 是 per-point 平方检测
（类比方向五 Heegner-height），真正对应 safe_sieve 的是 §7(3) blocker prime，而 §7(3)
明说无 universal prime（同 wl078-079 的 mod p² 结论）；(2) d19 早已超 45-prime 规模
（mod-p² 筛到 p=97，finite-descent N-only 已检 p<200）；(3) 实测 d19 筛力 100% 来自
closure reflection，90% killer 是 p≡3 mod4（p=3 占 88%），与 Peschmann「blocker 从不
p≡3 mod4」正相反——照其思路扩会丢掉主力素数。脚本 `scripts/modular/sieve_killer_prime_class.py`。

下面保留原始设计记录作 reference。

**出处**: wl036 §五, wl037

**思路**: 现 safe_sieve 用 mod 1680 (~5 primes). Peschmann §7(2) 用
45 primes < 200. 扩到这个规模可能让 sieve 提前 kill 更多 pair.

**为何没做**: wl037 提到是 wl037 目标, 但实际 wl037 转向 finite descent.

**怎么做**:
1. 给每个 prime p < 200 算 quadratic residue table
2. 对 (A, B) 在 mod p² 看 closure 局部 obstruction
3. CRT 合并到一个 combined sieve

**风险**: wl078-079 path B 已经验证 (a, b) mod p² CRT 不能 universal kill.
但 Peschmann 的 sieve 不一定是 mod p²-style.

**工作量**: 1-2 周

---

### A.7 D-scaling K_n 快速生成器 ✅ 已实现 (wl085)

**状态**: wl085 落地. 见 `docs/work-logs/085-dscale-kn-fast-generator.md`.
模块 `src/rational_distance/concordant/dscale_kn.py`, CLI
`scripts/multi_n/dscale_kn_generator.py`, 测试 `tests/test_dscale_kn.py`.

验证: 6/6 wl063 K_10 hub 完美 reproduce (2.7s for 4 primitives vs wl063
partner BFS 几十分钟). 新发现 K_11/K_12/K_13 hub (wl063 max_value=100k 限制范围外).

下面保留原始设计文档作 reference.

---

**出处**: wl065 §3 ("再研究每个底型沿着不同放大倍数 d 的 k(d) 如何增长"), wl066

**问题**: 现有 `fast_multi_concordant_pairs` 是全 (a, b) ≤ max_hyp 暴力扫. 找到
K_9/K_10 需要 max_hyp ≥ 100k, 实际**4 个 primitive 底型** ((25,91), (70,117),
(91,990), (221,704)) 就解释 wl065 全部 16 个 K_9/K_10 样本.

**思路 (wl065 已分析机制, 未实现)**:

```
1. 在 small max_hyp 内扫 primitive (a₀, b₀) (rank ≥ 1)
2. 对每个 primitive, PARI 算 E_{a₀,b₀}(ℚ) 的有限 rational concordant n 全集
3. 枚举放大倍数 d ∈ ℤ⁺, 对每个 n 检查 d·n ∈ ℤ (即 d 清掉 n 分母)
4. 输出 (d·a₀, d·b₀) 与对应 N = d·n 的整数集
5. filter k(d, primitive) ≥ target, target=4/5/9/10/...
```

**关键事实**: 同构 X = d² x, Y = d³ y 让 rank 不变, 但整数 N 是 d 决定的.

**预期收益 (校准后, 2026-05 修正)**:
- 给定 target k=10, 不必扫到 max_hyp 极大, 只用几十个 primitive × 几千个 d
- 对 path A K_n hub partner identity 推广 (A.1) 提供 sample (主要价值)
- **per-point efficiency**: K_n 顶点提供 C(n,2) 个 (N₁, N₂) closure 候选,
  K_10 单顶点 ≈ 45 × k=2 顶点的 closure check 量, 信号密度更大
- ⚠️ **不是**"找反例的更高概率路径": 见下文 §A.7 警告

**A.7 警告 — "高 k 更易出反例" 这个直觉无据**:

我之前在文档里有过 "高 k 是反例最优路径" 类型的措辞, 实际数据**不支持**这点:

1. **wl063 全 G_M scan**: 338,225 顶点 (含全部 K_5 到 K_10) → 0 closure
2. **wl065 K_9/K_10 全检**: 16 个 hub → 0 closure (但 sample 仅 4 个 primitive 底型)
3. **wl066 |Δ|=1 顶点 k 分布** (10 个 near-miss):
   ```
   k=2: 9   (90%)     vs 总体 unsafe k=2: 98.04%
   k=3: 1   (10%)     vs 总体 unsafe k=3:  1.87%
   ```
   |Δ|=1 sample 的 k 分布跟总体几乎一致, **没有显示高 k 更近 closure**, 也
   **没有显示小 k 更近 closure**.

4. **wl065 §3 机制论证**: 高 k 是 primitive 底型 (a₀, b₀) 通过 d 放大产生
   (X = d²x, Y = d³y 同构), rank 不变, **不在代数层产生新 independent
   closure 机会**.

**严格能 conclude 的**:
- (a) 已扫范围内 K_9/K_10 全 closure=0 (sample 小, 不是 statistical proof)
- (b) 高 k 机制不在 rank 层产生新 independent closure 机会
- (c) 已扫范围内 closure-near-miss 没有 k 偏好

**严格不能 conclude 的**:
- ✗ "高 k 不增加反例概率" — sample 太小, 仅 algebraic 论证不够
- ✗ "反例倾向出在小 k" — |Δ|=1 sample 仅 10 个, k 分布 ≈ 总体

⟹ A.7 仍值得做, 但理由是 **per-point efficiency + path A sample 源**,
不是"更可能出反例". 不要把"高 k bias"当 established fact 使用.

**工作量**: 1 周 (PARI ellgens 找 generators + 枚举 d 较直接)

---

### A.6 K_n 与 4-chain 反例的关系厘清 ✅ 已实现 (wl089) — 与 A.1 合并解决

**结论 (wl089)**: shared_partner K_n ⟺ partner pair 本身是 k≥n multi-N（17/17 对偶成立）；
general K_n 上限 K_3。K_n hub 与 4-chain closure 的关系已厘清为 partner/multi-N 等价，
不提供 closure 的额外代数 obstruction。详见 A.1 / wl089。

下面保留原始设计记录作 reference。

**出处**: wl055 §下一步 3

**思路**: K_n 是"n 个 a 两两 multi-N", 反例是 4-chain (K_4 closure).
两者关系尚未严格梳理.

**为何没做**: wl055 之后转去其他方向.

**怎么做**: 形式化 K_n 与 4-chain closure 的精确数学等价 / 包含关系.

**工作量**: 几天纸面工作

---

### A.8 Cassels-Tate pairing 把 sha2_lower 升级为严格 Sha[2] 证书 ⭐⭐ ★ 新整理 (2026-05-31)

**出处**: wl036 §五C, wl044 §十 (C1), PROJECT_STATUS §9.9, CURRENT_FINDINGS §（4-tuple bug 段）

**思路**: 现在 PARI `ellrank` 给的 `sha2_lower > 0` 只是下界估计；要把
「sha2≥2 hard_case 的非平凡 Sha[2] 元素」变成**严格证书**，需要对 quartic cover
做 Cassels-Tate pairing（PARI `elltatepairing`）+ 逐处局部可解性验证。156 个 sha2≥2
hard_case 的 `Sha[E][2] dim` 实测稳定 = 2（PROJECT_STATUS §9.9），是个干净的小样本。
具体可先做 (169,235) 的 cover quartic `-5279x⁴-17626x³+25673x²+27418x-2831`
的 everywhere-local-solubility（= D.5 重叠）。

**为何没做**: 多个 wl（036/044）都列为「后续不在本 wl 内做」，一直没启动。
需要先从 quartic cover 拿到 Sha[2] 代表。

**风险/收益**: 即便严格化，也只对 sha2≥2 子类（约 320 hard_case 中的少数）有效；
rank≥2 主流仍要 Chabauty。属于「清理最弱 case + 增强证据库」而非主线突破。

**工作量**: 半天–几天（PARI 直接做）

---

### A.9 closure-necessity 引理：闭合 4-chain 是否反例必要 🟡 部分解决 (wl093)

**出处**: wl092 §二, MULTI_CONCORDANT_N_STRATEGY §（结尾 402 行）, wl048 §后续 5

**结论 (wl093)**: 几何内容已厘清。现判据（`check_chain_compatibility` 的 `b=A+B−N`、
`chain_closure_sieve` 按 `A+B` 反射）只检验**和关系** `N₁+N₂=A+B`，几何上恰对应反例点
**落在单位正方形内部**——项目归约（MATH §7 要求 `a,b,c,d>0`）一直**默认反例在正方形内**，
此前从未论证（`D4` 对称把外部映到外部，WLOG-inside 不是免费的）。全平面的**充要必要
条件**是四个线性关系合写：

```
{N₁+N₂, |N₁−N₂|} ∩ {A+B, |A−B|} ≠ ∅      (GEN-CLOSURE)
```

（内部=和关系，左右/上下/四角外各对应一个差关系。）它仍只用 factor_search 穷尽出的
有限 concordant 集、全 rank、毫秒级、无 Magma。实测把判据升级到全平面后，
`max_hyp≤2000`（8220 pair，67 multi-N）**0 个**满足任一关系——把无反例证据从正方形内
扩到全平面。脚本 `scripts/theory/closure_necessity_relations.py`。

**sum 关系大尺度实证 (wl093 §四之二)**: 用 pivot-on-N 生成式扫描器把**和关系** `N₁+N₂=A+B`
（正方形内）推到 `max_hyp=5,000,000`（580,828 约化互素多-N pair，k≤5）——`closure=0` 依旧。
原 dict 实现 2M OOM（8 GiB），新增 numpy 排序-分组变体
`scripts/multi_n/fast_multi_concordant_scan_numpy.py`（1M/2M 精确复现 111,090/226,120，
5M 峰值 5.92 GiB；≥8M 需外部排序）。全平面四关系 GEN-CLOSURE 的扩尺度仍只到 max_hyp=2000。
该扫描器随后做了三轴优化（wl093 §四之三，每步对拍精确）：`--shards` ai 分片把 5M 峰值降到
3.83 GiB；Cython 内核 `_concordant_gen`（生成+桶内出对下沉 C，`_build_gen.py` 现场编译、
`.so` 不入库、缺则自动回退 Python）把 5M 总时 270→76s；`--workers` 并行（共享内存 + ai 分片）
2 核再到 56s。综合 5M 270→56s（4.8×）、计数精确不变。

**可立即落地的升级（建议，未在本 PR 改生产判据）**: 把闭合判据扩成查 GEN-CLOSURE 四关系，
即可把残余 inconclusive hard_case 在**全平面（互素腿）**下判 `no_solution`。因改 `no_solution`
语义、牵动既有结果/测试，留单独 PR + 用户确认。

**仍开放**: (a) §8.6 **gcd-scaling 覆盖**——`generate_ab_pairs` 只产互素对，非互素腿的反例在
约化对上不可见（对原 sum-only 与升级后判据同样存在）；(b) rank≥2 的结论性工具
Chabauty（B.1，需 Magma）/ Brauer–Manin（A.4）。GEN-CLOSURE 不依赖这些，但彻底证明仍需 (a)(b)。

**工作量**: 几何引理已完成（wl093）；落地升级半天；(a)(b) 仍是独立大方向。

---

## B. 理论方向 — 已尝试但未完成 / 已被否定

### B.1 closure-fiber Chabauty 🛑 (要 Magma)

**出处**: wl074 §状态, wl076 §状态, wl083 §状态

**状态**: rank ≥ 2 fiber finiteness 严格证明需要 quadratic Chabauty,
工具栈不够 (Magma 必需).

### B.2 A_k 推广 k≥3 严格证明 🛑

**出处**: wl084

**状态**: k=4 case 实证就有 counterexample (`(A=426496, B=482625, N=352800)`,
δ(Q)=0). 严格通用证明不可能.

### B.3 wl082 论证修补 (c composite) 🛑

**出处**: wl084 §九

**状态**: 工作量大, 修需要 c² 的所有表示如何与 Pythagorean 参数关联,
不打算做.

### B.4 A1 严格证明 🛑 (vacuous truth) — 但**猜想本身仍开放**

**出处**: wl084

**状态**: wl081-083 的 algebraic chain 在 k=2 sample 上 vacuously hold，证明
invalid（wl082 在 c composite 时失效）。⚠️ 注意区分：**被否定的是那条具体证明路径**，
而命题「k=2 ⟹ rank(E_{A,B}) ≥ 2」**实证 1879/1879 universal (max_hyp=1M)、仍是
开放猜想**，并且是 path A 最有希望的代数突破点（只是现有 Gaussian-integer 工具不够）。
若要重启，需要「c² 的所有两平方和表示如何与 Pythagorean 参数关联」的更细分析
（wl084 §九判为工作量大、暂不做）。

### B.5 path B uniform mod p² 严格证明 🛑

**出处**: wl078, wl079, wl080

**状态**: max_hyp ≤ 2M 实证全杀, 但严格证明在 mod p² (p ≥ 5) 上无简单
algebraic. path B 关闭.

### B.6 height-bound argument 🛑

**出处**: wl077

**状态**: 实证 1879/1879 fail, `min ĥ > 2 log(A+B)` 路径不通.

### B.8 “Heegner 升级成判定器（补 height bound）” 🛑

**出处**: wl092

**状态**: 判为**冗余**。`factor_concordant`（在 pipeline 里排在 `heegner` 之前）
已穷尽枚举全部 concordant 整数 N（由 `B²−A²` 的 divisor pair，自证完整、无上界、
全 rank），rank=1 有界 MW 扫描只是其严格子集。实测（max_hyp=500，24.8 ms 全判完）：
7 个残余 inconclusive hard_case **全 rank≥2**（heegner 仅 rank=1，全 skipped），且因子法找到
的 N（如 260820）远超任何有界扫描窗口。需要的 height 上界又被 B.6 判不成立。
残余 `inconclusive` 的真正 gap 是 **closure-necessity（闭合 4-chain 是否必要）**，
与 Heegner/height 无关；script: `scripts/theory/heegner_vs_factor_decider.py`.

### B.7 hypotenuse identity / blocker prime 🛑

**出处**: wl034

**状态**: "h_i 都不含 ≡ 3 mod 4 素因子 → 矛盾" 基础假设错, 路径废弃.

---

## C. 工程优化 — 未实施

### C.1 chain_db 升级 (增量缓存 + cross-run sharing) ⭐⭐

**出处**: wl080 §六

**思路**: 当前 chain_db 每次 rerun 重算; 可以加增量缓存共享多个
benchmark run.

**工作量**: 1 周

---

### ~~C.2 / C.3 / C.4 工程小项~~ ✅ 已完成 (wl088)

- **C.2** `multi_n_sieve` 接入 `DEFAULT_METHOD_PIPELINE` (factor_concordant 之后),
  k<2 ⇒ 严格 no_solution。
- **C.3** `rank_zero` 加 `rank_lower_hint`: F₂-rank ≥ 3 时短路, 跳过 PARI ellrank
  (主路 + ab_sieve ctx 路均接入)。
- **C.4** `pair_proof_status` 加 `f2_rank` 列 (schema v2), thread 过 workflow 两条路。

全套 319 测试通过。详见 wl088。

---

### C.5 `fast_multi_concordant_pairs` 进一步加速 ⭐⭐

**出处**: wl073, wl048

**当前**: max_hyp=2M ~170s. 已 1.68× 加速 (wl073). 剩余瓶颈 Python loop.

**思路**:
- ParallelExecutor 划 a 块并行 (4-6× 加速)
- Cython/C 重写 Phase 2 (3-5× 加速)
- m, n parameterization 替换 SPF (1.5-2× 加速)

**工作量**: 累乘理论 30-50× , 实际 10-15×, 1-2 周

---

### C.6 推 max_hyp ≤ 10^7 unconditional 实证 ⭐⭐

**出处**: wl073

**思路**: 配合 C.5 加速, max_hyp 推到 10M / 30M, 给 confidence boost.
**不是证明**, 仅信心增强.

**工作量**: 配合 C.5 后 1 天

---

### C.7 GPU int64 overflow 保护 ⭐⭐

**出处**: wl005, wl006, wl007 (archive)

**当前**: GPU 路径 scale > 400 时静默错误. 现在用 numpy/Python 路径.

**思路**: GPU 路径 + CPU 回退混合.

**工作量**: 几天 (但当前 GPU 路径未启用, 优先级低)

---

### C.8 ParallelExecutor 在循环 map 调用点替换 ⭐⭐

**出处**: wl064 §后续

**思路**: 找"循环里反复 cfg.map(...)"的调用点, 改成 executor 复用进程池.
基准 6-9× 加速.

**工作量**: 1 周

---

## D. 数据 / 实证 — 未实施

### D.1 F₂-rank ≥ 3 pair 跑 PARI ellrank ✅ 已完成 (wl050 / wl052 / wl087)

**状态**: 已完整。审计在两个尺度都跑完且全 certified:
- max_hyp=50000: 110 候选 (wl050), `results/multi_n/multi_concordant_N_max50000_pari_rank.jsonl`
- max_hyp=100000: 190 候选 (wl052), `results/multi_n/multi_concordant_N_max100000_pari_rank.jsonl`

wl087 对 190 个 max100000 候选**从头独立复现** (0 disagreements, 0 uncertified)。
结构允许 (rank≥4) 候选: 13 @ 50k / 34 @ 100k；Sha[2]≥2: `(36225,40592)`,
`(34307,74000)`；全部 closure_pairs 为空。脚本 `scripts/theory/pari_rank_high_f2.py`。

---

### D.2 (1845, 2912) 深度审计 ⭐⭐

**出处**: wl050, wl052

**思路**: 113 这个差能不能被某个更小或更大的 N 补上 (closure 局部障碍最弱).

**工作量**: 几天

---

### D.3 (27328, 44055) 结构分析 ⭐⭐

**出处**: wl050

**思路**: rank=5 但 k=3, 很多 Mordell-Weil 方向 *不* 落在 square-x 截面.

**工作量**: 几天

---

### D.4 (153, 560) 的三个 N 的 Mordell-Weil 结构 ⭐⭐

**出处**: wl046 §后续

**思路**: 经典样本 (Bremner-Ulas 等用过), N=[204, 420, 3900], rank=3.
三个 Q_{N_i} 在 MW lattice 上的具体位置.

**工作量**: 几天 (PARI ellgens)

---

### D.5 9 个 outlier explicit cover quartic ⭐⭐

**出处**: wl039 §下一步 (Manual deep-dive on (169, 235))

**思路**: PARI 找到 gen 但 hyperellratpoints 找不到 cover-lift 的 9 个
case 的手动 deep-dive.

**工作量**: 几周

---

### D.6 max_hyp=5000 → 750 sha2 ≥ 2 case ⭐⭐

**出处**: wl039 §下一步 (Scale up)

**思路**: 把 156 sha2 ≥ 2 case 扩到 ~750.

**工作量**: 1 周 + 大量 PARI 时间

---

## E. 图论 / partner network — 未实施

### E.1 max_value = 10M / 100M G_M BFS ⭐⭐

**出处**: wl063 §下一步, wl056

**思路**: 当前 G_M comp 0 在 max_value=1M 找到 K_10. 推到 10M 看
K_11+ 是否出现.

**工作量**: 几小时 (BFS 已并行化)

---

### E.2 K_9 / K_10 实例 ellrank ⭐⭐

**出处**: wl063 §下一步 2, wl062

**思路**: 测 wl060 "rank ≤ 4 在 catalog" 假设是否在 K_9/K_10 hub 上仍 hold.

**工作量**: 1 天 (PARI ellrank)

---

### E.3 cycle 的代数解释 — 代数半部分已解决 (wl086)

**出处**: wl058 §下一步 3, wl059 §下一步

**状态**: 代数半部分由 wl086 (A.2) 解决: cycle 的 rank deficit = Q_N 坐标矩阵
的秩亏, 而每个 Q_N ∈ 2·E(ℚ) (descent-trivial)。"cycle ↔ rank deficit"
相关性的精确机制由此给出, 但**不构成 closure 障碍** (见 A.2)。

**剩余 (纯图论, 与代数独立)**: "是否所有 G_M cycle 都经过某个 K_n hub?"
这部分未做, 可在 E.1/E.2 跑 BFS 时顺带统计。

---

### E.4 power-law 拟合 / scale-free 形式化 ⭐

**出处**: wl062 §下一步 (wl065 候选), wl063

**思路**: comp 0 度数分布 log-log slope ~-2 到 -3. 形式化为 BA 模型?

**工作量**: 几天 (但偏理论, ROI 低)

---

### E.5 Δ-near-miss 与秩联动 ⭐⭐

**出处**: wl066 §下一步 3

**思路**: 把每个 multi-N pair 的 min |Δ| (closure 距离) 和 rank 联动看分布.

**工作量**: 几天

---

### E.6 K_n 跨级 partner 链接 ⭐

**出处**: wl056 §下一步 4

**思路**: (300, 1092) 的 N 列表含 3744 这种跨级关系.

**工作量**: 几天

---

### E.7 partner-only 顶点 sha2 / rank 测试 ⭐⭐

**出处**: wl054 §未做的事

**思路**: (3192, 97308) 这种非互素 partner-only 顶点的 sha2/rank 没测过.

**工作量**: 几天

---

## F. 文献 / 形式化 — 未实施

### F.1 conditional paper 骨架 ✅ 已实现 (wl090) — 正文待写

**出处**: wl083 §状态

**状态 (wl090)**: 已写 conditional paper 骨架 `docs/paper/CONDITIONAL_PAPER_OUTLINE.md`，
只用已证结果（恒等式 A/C 100% 验证 + 无解 census）+ 可复现数据，**不依赖 A1 严格**。
下一步是把骨架扩成正文（仍属开放，工作量 = 写作，非数学突破）。原「依赖 A1 严格」的前提
已纠正：conditional paper 恰恰不需要 A1 严格。

---

### F.2 Stoll-Bruin Chabauty 工具调研 ✅ 已完成 (wl090)

**出处**: wl080 §六, wl079 §五

**结论 (wl090)**: Stoll/Bruin 工具**部分**可替代 Magma——Sage 有 Coleman 积分 /
经典 Chabauty–Coleman / two-cover descent，但结论性的 **MW-sieve + 高亏格 rank 计算
仍主要靠 Magma**。B.1 因此从「全程要 Magma」降级为「两步要 Magma」。详见 wl090。

---

### F.3 Mazur uniform bound 文献 ⭐

**出处**: wl080 §六

**思路**: 是否能用 Mazur 风格的 uniform bound 论证 closure-fiber 闭包.

**工作量**: 几周深度文献

---

### F.4 Peschmann §7(2) 文献深读 ✅ 已完成 (wl091) — 导致 A.5 关闭

**出处**: wl036 §五

**结论 (wl091)**: §7(2) 是 per-point 平方检测，不是参数 sieve；对应 safe_sieve 的是
§7(3) blocker prime，且 §7(3) 明说无 universal prime。modular search 迁移（= A.5）
据此**关闭**（见 A.5 / wl091）。

下面保留原始调研记录作 reference。

**出处**: wl036 §五

**工作量**: 1-2 周

---

## 优先级汇总

> 📌 2026-05-31 回填（wl086–092）：A.1/A.2/A.6/A.7/D.1/C.2–C.4/E.3/F.1/F.2/F.4
> 已完成；A.5 与方向五 Heegner 判定器（B.8）已 🛑 关闭；E.1 暂缓。详见各 section
> 与「探索脉络图」`docs/EXPLORATION_MAP.md`。

**A–F 类已完成 / 关闭一览**

| 条目 | 状态 | wl | 一句话结论 |
|------|------|----|-----------|
| A.1 K_n hub identity | ✅ negative | wl089 | shared Q_N 全 2-可除，无跨边障碍 |
| A.2 cycle linear relation | ✅ negative | wl086 | cycle = 2-可除性，不区分反例 |
| A.6 K_n vs 4-chain | ✅ | wl089 | K_n ⟺ multi-N，上限 K_3 |
| A.7 D-scaling K_n 生成器 | ✅ | wl085 | K_11/12/13 新发现 |
| D.1 F₂-rank≥3 ellrank | ✅ | wl050/052/087 | 110@50k+190@100k 全 certified |
| C.2–C.4 pipeline 工程 | ✅ | wl088 | multi_n_sieve 入主线 |
| E.3 cycle 代数解释 | ✅ | wl086 | 与 A.2 同 |
| F.1 conditional paper 骨架 | ✅ 骨架 | wl090 | 不依赖 A1，正文待写 |
| F.2 Stoll-Bruin 调研 | ✅ | wl090 | 部分替代 Magma，MW-sieve 仍要 |
| F.4 Peschmann §7(2) 深读 | ✅ | wl091 | §7(2) per-point，非 sieve |
| A.5 扩 safe_sieve | 🛑 | wl091 | 与 mod p² 同坑，丢主力素数 |
| B.8 Heegner 升级判定器 | 🛑 | wl092 | factor_search 已穷尽，冗余 |

**剩余真正开放（按"可推动证明 + 可行性"排序）**

1. **A.3 Heegner sieve on outliers** ⭐⭐（⚠️ wl092：步骤3不必做，直接用 factor_concordant 判 9 个 outlier）
2. **A.4 Brauer-Manin** ⭐（数月 + 合作者）
3. **A.9 closure-necessity 引理** 🟡 部分解决（wl093：和关系=正方形内；全平面充要条件是
   GEN-CLOSURE 四关系，实测全平面 0 反例至 max_hyp=2000；落地升级 + §8.6 gcd 覆盖待做）
4. **B.1 Chabauty**（wl090 后降级为「两步要 Magma」，配 F.2）
5. **F.1 正文**（把骨架写成 conditional paper，现在就能变现）

按"工作量低 + 立即可做"排序:

1. **E.2** K_9/K_10 ellrank (1 天)
2. **D.2–D.6** 个案审计 / sha2 扩样本
3. **C.1 / C.5–C.8** 工程优化（与证明无关，想做随时）
4. **E.1** max_value 推到 10M（⚠️ 已暂缓：1M BFS 已 738s，10M 小时级，且 K_11+ 已被 wl085 构造性回答）

---

## 维护规则

- 启动一项任务时, 在该 section 加 "🚧 in progress (wlXXX)"
- 完成时移除条目 + 在对应 wl 中标注 "回填到 OPEN_DIRECTIONS.md 移除"
- 否定时改为 🛑 + 简述结论
- 新发现的方向直接 append 到对应 section
