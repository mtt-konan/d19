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

### A.1 K_n hub partner identity 推广 ✅ 已实现 (wl089) — 不构成障碍

**状态**: wl089 落地。脚本 `scripts/partner/kn_partner_identity.py`,
结果 `results/partner/kn_partner_identity.jsonl`,
回归测试 `tests/test_cycle_relations.py::test_rational_generator_coords_do_not_raise`。
见 `docs/work-logs/089-kn-hub-partner-identity-A1-A6.md`。

**结论 (negative but informative)**: 对 28 个 K_n hub 的全部 49 条边复用 wl086
machinery，检查 shared concordant 点 Q_N 是否落在 2·E(ℚ)：**49/49 全部 2-可除**。
每个点在它**自己那条曲线**上就 2-可除 (同 A.2/wl086)，与 hub 是否 "共享" 无关。
K_n hub 的 sharing 只是不同曲线 (j-invariant 一般不同) 之间 N 值的巧合，**不是
代数 linkage**，不提供跨边 closure 障碍。A.1 撞上和 A.2 同一堵墙：推到更高 k 需要
**新的**代数恒等式，而非 hub 巧合。

**副产物 (bug fix)**: 发现并修复 `analysis.compute_rank` 把 PARI ellrank 返回的
**有理坐标** generator 用 `int()` 截断 (例如 (425,1001) 的 gen
`[-5504345/9, ...]`)，导致 ~40% 曲线报 "point not on E"。新增
`compute_rank_exact_points` 保留精确点，`cycle_relations` 改用之；`compute_rank`
对外行为不变 (向后兼容)。

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

**出处**: wl036 §五, wl037

**结论 (wl091)**: **不值得做**，三条理由（全实测支撑，见
`docs/work-logs/091-f4-peschmann-sieve-vs-mod-p2-closure.md`）：
1. "45-prime 参数 sieve" 在 d19 **早已实现**——`chain_closure_mod_sieve`(wl040) 用
   mod-p² 到 p=97，`finite_descent_hard_cases`(wl037) N-only 已检 p<200；单 mod-p²
   筛在 max_hyp=2000 就砍 99.6% hard_case。A.5 的"现仅 ~5 primes mod 1680"前提已过时。
2. A.5 把 Peschmann §7(2) 当"45-prime 参数 sieve"是 **category error**：§7(2) 是
   per-point 平方检测（类比方向五 Heegner-height），真正对应 safe_sieve 的是 §7(3)
   blocker prime，而 §7(3) 明说**无 universal prime**（同 wl078-079）。
3. **实测**：d19 的筛力 100% 来自 closure reflection `T∩((A+B)−T)=∅`（pure `T=∅` 砍 0
   个），且 90% killer 是 **p≡3 (mod 4)**（p=3 占 88%）。若照 Peschmann 的纯平方 /
   Gaussian blocker 思路扩 sieve，会**恰好丢掉**这些承担 90% 筛力的素数 ⟹ 严格更弱。

⟹ 不重走 path B；维持现 mod-p² closure sieve。**注意**: 别因 Gaussian-范数论证去删
p≡3 (mod 4) 模数（如 p=3）——它们在 closure reflection 里恰恰最关键。

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

### A.6 K_n 与 4-chain 反例的关系厘清 ✅ 已厘清 (wl089)

**状态**: wl089 与 A.1 一起做掉。见
`docs/work-logs/089-kn-hub-partner-identity-A1-A6.md`。

**结论**:
1. **shared_partner 对偶**: shared_partner K_n（n 节点共享 partner pair
   (P_a,P_b)）⟺ (P_a,P_b) 自身是 k≥n 的 multi-N pair 且其 N 集含这 n 个节点
   ——(A,B)↔N 对偶。17/17 shared_partner hub 验证成立。
2. **general K_n 上限**: general K_n 要求 C(n,2) 条边全 multi-N；max100000 互素
   catalog 中只有 11 个 K_3、**0 个 K_4+**。
3. 这两点说明 "K_n 给比单 multi-N pair 更强的 closure 障碍" 不成立（A.1 已验证
   每条边的 Q_N 仍只是 2-可除）；K_n 与 4-chain closure 没有提供新的代数包含关系。

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

### A.9 closure-necessity 引理：闭合 4-chain 是否反例必要 ✅ 已落地 (wl093 引理 + wl094 落地)

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
2 核再到 56s。综合 5M 270→56s（4.8×）、计数精确不变。用省内存档实测**纯内存封顶 ≈ 7M**
（822,108 多-N pair、closure 仍 0、k≤5 仍无 k=6，5.56 GiB）；10M OOM——瓶颈是关系 `argsort`
索引+重排翻倍（分片只压下游 emit），故先前估的 10–12M 高估，≥8M 需外部排序或大内存机。

**落地完成 (wl094)**: 已把生产判据扩成查 GEN-CLOSURE 四关系。`chain_closure_sieve.killed_at_modulus`
加 `full_plane=` 参数（`run_chain_closure_mod_sieve` 传 `True`）；新增 `analysis.gen_closure_hit`
在穷尽 concordant 集上做四关系测试；`run_factor_concordant` 改用它，穷尽枚举无命中 ⇒ `no_solution`
（旧 `inconclusive`），成为**穷尽、全 rank、无 Magma** 的互素腿判定器。实测默认 pipeline：
max_hyp=2000 的 **99,311 个互素约化对全部 `no_solution`、0 hard_case**（safe_sieve 91,091 +
全平面 chain_closure 7,975 + GEN-CLOSURE factor 245），全程不调 PARI、1.6s。322 测试全过
（8 个语义相关测试按新语义更新）。

**互素腿 mod-12 定理 (wl097，MATH §8.5.1)**: 已证 `gcd(A,B)=1 ⟹ 12|N`（每个 concordant N），
初等 mod 3 + mod 8。推论：互素腿闭合需 `12|(A+B)` 或 `12||A−B|`（mod 12 一步排除约 99.7% 互素对）。
经验面 >1.16M 个 N 跨 hyp≤5M + 7M BFS 零例外（wl096）。这把"互素腿 GEN-CLOSURE 跑到 2000 无命中"
往**闭式**推了一步，也精确解释了 (a) 为何只在非互素腿失效（互素性是定理两步的必要前提）。

**⚠️ 框架级澄清（coprime-`(A,B)` 并非 WLOG，wl097 后补记）**: 整条 `(A,B)`-first 筛线
（`safe_sieve → chain_closure 模 p² → factor_concordant → multi_n`）**只筛过互素 `(A,B)`**，且其
soundness **全部挂在互素前提上**——`safe_sieve` 的两条规则就是 mod-12 定理的 mod-2/4 推论（MATH §8.5.1），
非互素腿上 mod-12 塌、规则失依据。而把搜索限制在 `gcd(A,B)=1` **不是 WLOG**：反例整体放缩只保证
`gcd(A,B,N₁,N₂)=1`，完全可能 `gcd(A,B)>1` 而四数整体互素（§7 中 `A=q₁q₂,B=p₁p₂` 是本原三元组腿积，
跨三元组公因子天然出现）。故非互素 `(A,B)` 半空间是**结构性盲区**，不是罕见 edge case。**覆盖全的是
multi-N 生成线**（partner 图 / 扫描，wl058–wl096）：它天然含非互素顶点（7M comp0 即 99.5% 非互素），
closure 经验扫描已覆盖非互素到 7M、仍 0 命中——所以缺口是**证明**、不是搜索。§8.6 应视为与互素腿
**同级的主目标**。

**仍开放**: (a) §8.6 **gcd-scaling 覆盖（升级为主目标）**——给非互素腿一个独立的解析障碍（刻画
`gcd=g` 时 concordant `N` 的剩余类，看能否凑出类 mod-12 的闭式障碍），或证明任何非互素反例可约化到
互素反例（即真的把 coprime-`(A,B)` 做成 WLOG）。二选一即补齐彻底证明的最后结构缺口。
(b) rank≥2 的结论性工具 Chabauty（B.1，需 Magma）/ Brauer–Manin（A.4）。GEN-CLOSURE 不依赖这些，但彻底证明仍需 (a)(b)。

**工作量**: 几何引理已完成（wl093）；落地升级半天；互素腿 mod-12 定理已证（wl097）；(a)(b) 仍是独立大方向。

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

### E.1 max_value = 7M / 10M G_M BFS ⭐ (7M 已跑, wl096; 更大窗口仍暂缓)

**出处**: wl063 §下一步, wl056

**思路**: 当前 G_M comp 0 在 max_value=1M 找到 K_10. 推到更大窗口看 comp0 如何生长.

**状态 (wl096 更新)**: **7M 已跑完** (2 worker, 1348.6s, 2,530,620 顶点 / 2,719,386 边,
`results/partner/partner_full_bfs_7M_summary.json`)，用来验证 comp0 的结构（见下方
「G_M 三层分解」）。10M/100M 仍暂缓：要回答的科学问题 ("K_11+ 是否存在") **已被 wl085 的
D-scaling 生成器构造性回答**，更大经验扫描边际价值低。

**G_M 三层分解 (wl096)**: 用 wl095 精确因子核（对 N 不设上界）给每个非 comp0 分量贴标签——
*branch*(被窗口截断，伙伴坐标>W) vs *island*(partner 封闭，永久独立)。1M 数据：comp0
(309689, 92%) + 620 断枝 (5647 v, max_k 3→8) + **8959 永久孤岛** (22889 v, max_k≤5,
含 1029 个 K_3/K_4/K_5 自闭合孤岛, 非仅 K_2)。7M 验证：comp0→2,503,583 (98.9%);
所有 k≥6 非 comp0 分量都是断枝, 最大 11 个里 10 个在 7M 并入 comp0 (K_7/K_8 全并);
**8959 孤岛 0 顶点泄漏进 7M giant** (untruncated ⟺ 永久独立, 100% 验证)。closure 在
孤岛+comp0 上恒 0。结论：高 k 被 comp0 垄断；"剔除 comp0"作工程筛选可行、作证明分解才有
真价值，但不改 closure 恒 0。脚本 `comp0_island_analysis.py` / `verify_window_merge.py`。

---

### E.2 K_9 / K_10 实例 ellrank — ✅ 已完成 (wl094)

**出处**: wl063 §下一步 2, wl062

**思路**: 测 wl060 "rank ≤ 4 在 catalog" 假设是否在 K_9/K_10 hub 上仍 hold.

**结论 (wl094)**: 全部 48 个 K_9/K_10 hub + 11 个 K_11–K_13 hub (wl085 D-scaling)
ellrank, **0 个 rank > 4** (rank ∈ {3,4}, 全 certified, sha2[2]=0)。rank ≤ 4 假设
从 k=6–8 (wl060) 延伸到 k=9–13 无一例外 (合计 70 hub); K_11–13 放大 hub 的 rank
精确等于 primitive rank (11/11, 算术验证 D-scaling rank 不变性); deficit 随 k 单调
升 (K_13 deficit=9)。

**K_14+ 延伸 (wl095) ✅**: 把"D-scaling 瞄准 + 快速因子核精确数 k"两个工具合并
(`scripts/multi_n/k14_search.py` + `fast_multi_n.exact_concordant_pair`)，跑全 854 个
primitive (d_max=50000)。可达 hub 阶数随 primitive rank 走: rank1→K_5, rank2→K_8,
rank3→K_11, rank4→**K_16**。**K_14+ 确实出现** (primitive (2975,7904) rank-4 →
K_16 hub (82467000, 219098880))。9 个 k≥11 hub (含 K_16) 全部 ellrank 认证:
rank ≤ 4、certified、放大 rank == primitive rank (D-scaling 不变性守到 k=16)。
结果存 `results/multi_n/k14_search.jsonl` / `k14_ellrank.jsonl`。

**剩余钩子**: 对 rank=4 hub 找共同 2-descent 像 (跨 hub closure 障碍, 已被 A.1 negative)。

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

### F.1 conditional / empirical paper 骨架 ✅ 骨架已写 (wl090)

**出处**: wl083 §状态

**状态**: A1 不严格 (wl084), 但 conditional/empirical paper **不依赖** A1 严格,
现在就能写。骨架落地于 `docs/paper/CONDITIONAL_PAPER_OUTLINE.md`：proven 部分
(恒等式 A/C、2-adic + mod-p² 必要条件、N≤10⁸ finite descent、2-可除性定理 wl086)
+ 可复现 no-solution census + 仅 §7 conditional on A1。后续把骨架填成 LaTeX 即可
(census 表用既有 certified range, 不长跑)。

---

### F.2 Stoll-Bruin Chabauty 工具调研 ✅ 已调研 (wl090)

**出处**: wl080 §六, wl079 §五

**结论**: 见 `docs/work-logs/090-f2-chabauty-tooling-survey.md`。Stoll–Bruin 一系
**部分可替代、整体尚不可替代** Magma：经典 Chabauty–Coleman 的 Coleman 积分在 Sage
成熟 (BBK)，奇数次超椭圆 + rank 0/1 有成体系 Sage 实现 (arXiv:1909.04808)，
Bruin–Stoll two-cover descent 有开源版 (`twocover-descent`)；但让结论性的
**Mordell–Weil sieve** 与高亏格 `Jac` 的 rank 计算至今主要是 Stoll 的 Magma 代码
(QCMod 等)。**B.1 降级措辞**: 不是全程要 Magma, 而是 MW-sieve + 高亏格 rank 两步要。
最低成本 PoC: 挑一个 rank<g 的 hard_case fiber 写成超椭圆模型用 Sage 跑经典 CC。

---

### F.3 Mazur uniform bound 文献 ⭐

**出处**: wl080 §六

**思路**: 是否能用 Mazur 风格的 uniform bound 论证 closure-fiber 闭包.

**工作量**: 几周深度文献

---

### F.4 Peschmann §7(2) 文献深读 + modular search 实施 ✅ 已读懂 (wl091)

**出处**: wl036 §五

**结论 (wl091)**: 见 `docs/work-logs/091-f4-peschmann-sieve-vs-mod-p2-closure.md`。
Peschmann §7(2) 是 **per-point 平方检测**（对 5 个 hard 曲线在 height box 内枚举
有理点 P，用 45 primes<200 判 `f(P)∈ℚ*²`），类比 d19 的**方向五 Heegner-height
有界枚举 + 多素数平方过滤**，**不是** safe_sieve 类的参数 sieve。真正对应 safe_sieve
的是 §7(3) blocker prime（无 universal prime，同 wl078-079）。Peschmann Remark 6.5
(Gaussian 范数 ⟹ p≡3 mod4 不能当 blocker) 不直接迁移，因为 d19 的筛力在 closure
reflection（实测 90% killer 是 p≡3 mod4）。→ 连带关闭 A.5。

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
| E.2 K_9–K_16 ellrank | ✅ | wl094/095 | k=6→16 全 rank ≤ 4，0 反例；K_16 hub rank=4 |
| E.1 7M BFS + G_M 三层分解 | ✅ | wl096 | comp0 92%→98.9%；断枝并入、8959 孤岛永久独立(0泄漏)；closure 恒0 |
| F.1 conditional paper 骨架 | ✅ 骨架 | wl090 | 不依赖 A1，正文待写 |
| F.2 Stoll-Bruin 调研 | ✅ | wl090 | 部分替代 Magma，MW-sieve 仍要 |
| F.4 Peschmann §7(2) 深读 | ✅ | wl091 | §7(2) per-point，非 sieve |
| A.5 扩 safe_sieve | 🛑 | wl091 | 与 mod p² 同坑，丢主力素数 |
| B.8 Heegner 升级判定器 | 🛑 | wl092 | factor_search 已穷尽，冗余 |
| A.9 GEN-CLOSURE 落地 | ✅ | wl093/wl094 | 全平面四关系判据；max_hyp=2000 全 no_solution，0 hard_case |

**剩余真正开放（按"可推动证明 + 可行性"排序）**

1. **A.3 Heegner sieve on outliers** ⭐⭐（⚠️ wl092：步骤3不必做，直接用 factor_concordant 判 9 个 outlier）
2. **A.4 Brauer-Manin** ⭐（数月 + 合作者）
3. **A.9 §8.6 gcd-scaling 覆盖** ⭐⭐（wl094 后，GEN-CLOSURE 已把**互素腿**做成判定器；
   唯一剩的 gap 是非互素腿 `(gA',gB')` 的反例在约化对上不可见——彻底证明 Harborth 的最后一块）
4. **B.1 Chabauty**（wl090 后降级为「两步要 Magma」，配 F.2）
5. **F.1 正文**（把骨架写成 conditional paper，现在就能变现）

按"工作量低 + 立即可做"排序:

1. ~~**E.2** K_9/K_10 ellrank~~ ✅ 已完成 (wl094: 70 hub k=6→13 全 rank ≤ 4)
2. **D.2–D.6** 个案审计 / sha2 扩样本
3. **C.1 / C.5–C.8** 工程优化（与证明无关，想做随时）
4. ~~**E.1** max_value 推到 7M~~ ✅ 7M 已跑 (wl096: comp0 92%→98.9%, 三层分解验证); 10M+ 仍暂缓

---

## 维护规则

- 启动一项任务时, 在该 section 加 "🚧 in progress (wlXXX)"
- 完成时移除条目 + 在对应 wl 中标注 "回填到 OPEN_DIRECTIONS.md 移除"
- 否定时改为 🛑 + 简述结论
- 新发现的方向直接 append 到对应 section
