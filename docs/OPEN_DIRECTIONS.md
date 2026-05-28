# Open Directions — 可做但未实施的方向汇总

本文件系统收录从 wl001 到 wl084 中提到的"下一步 / 后续 / 待做 / 候选"
方向，按可行性 + ROI 分类。每条标注 **出处 wl**, **可行性**, **预估工作量**。

更新时间: wl084 之后. 维护原则: 落地一项就从本文件移除, 添加新发现的
方向时直接 append 到对应分类下.

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

### A.1 K_n hub partner identity 推广 ⭐⭐ ★ HIGH-ROI

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

### A.2 cycle linear relation 追踪 ⭐⭐⭐

**出处**: wl058 §未做的事, wl059 §五

**思路**: wl058 在 (153, 560) BFS 中发现 1 个 6-cycle. wl059 找到
"cycle 与 rank deficit 高度相关". 但具体 linear relation
`c₁ Q_{N_1} + c₂ Q_{N_2} + c₃ Q_{N_3} = 0 ∈ E(ℚ)` 没追.

**为何没做**: 当时方向转向 wl060+ 的 K_8 audit, cycle 算法被搁置.

**怎么做**: 对 (420, 1344) (deficit=2 的 sample), 用 PARI ellgens 算
Mordell-Weil generators, 把 3 个 Q_{N_i} 作为 generators 的整数线性组合
表达, 找 c_i 系数. 如果有 universal pattern, 可能给 closure obstruction.

**工作量**: 几天 (PARI 直接做)

---

### A.3 Heegner sieve on closure-failure outliers ⭐⭐

**出处**: wl039 §下一步 (高优先), wl040 §下一步 3

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

### A.5 扩 safe_sieve 到 Peschmann §7(2) 规模 ⭐⭐

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

### A.6 K_n 与 4-chain 反例的关系厘清 ⭐⭐

**出处**: wl055 §下一步 3

**思路**: K_n 是"n 个 a 两两 multi-N", 反例是 4-chain (K_4 closure).
两者关系尚未严格梳理.

**为何没做**: wl055 之后转去其他方向.

**怎么做**: 形式化 K_n 与 4-chain closure 的精确数学等价 / 包含关系.

**工作量**: 几天纸面工作

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

### B.4 A1 严格证明 🛑 (vacuous truth)

**出处**: wl084

**状态**: wl081-083 chain 在 k=2 sample 上 vacuously hold, algebraic
论证 invalid.

### B.5 path B uniform mod p² 严格证明 🛑

**出处**: wl078, wl079, wl080

**状态**: max_hyp ≤ 2M 实证全杀, 但严格证明在 mod p² (p ≥ 5) 上无简单
algebraic. path B 关闭.

### B.6 height-bound argument 🛑

**出处**: wl077

**状态**: 实证 1879/1879 fail, `min ĥ > 2 log(A+B)` 路径不通.

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

### C.2 `multi_n_sieve` 接入 DEFAULT_METHOD_PIPELINE ⭐⭐⭐

**出处**: wl073 §后续

**思路**: multi_n_sieve 是 k≥2 必要条件, 现在还没接入主 pipeline.

**工作量**: 1-2 天

---

### C.3 `rank_zero` 加 F₂-rank short-circuit ⭐⭐⭐

**出处**: wl051 §后续

**思路**: F₂-rank ≥ 3 时直接返回 inconclusive 并 skip PARI, 节省 PARI
调用. 需要给方法间传递状态.

**工作量**: 1 天

---

### C.4 `proof_status` schema 加 `f2_rank` 列 ⭐⭐⭐

**出处**: wl051 §后续

**思路**: 给 hard_case 按 F₂-rank 分层查询.

**工作量**: 半天

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

### D.1 110 个 F₂-rank ≥ 3 pair 跑 PARI ellrank ⭐⭐⭐

**出处**: wl049 §后续, wl050

**当前**: wl050 跑了一部分但没完整 110 pair audit.

**工作量**: 1-2 天

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

### E.3 cycle 的代数解释 ⭐⭐⭐ ★ 与 A.2 联动

**出处**: wl058 §下一步 3, wl059 §下一步

**思路**: (153, 560) 的 6-cycle 经过 K_5 hub. 是否所有 G_M cycle 都
经过某个 K_n hub? cycle 与 rank deficit 的相关性是否严格?

**工作量**: 1-2 周 (与 A.2 一起做)

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

### F.1 LaTeX 形式化 paper ⭐ (依赖 A1 严格)

**出处**: wl083 §状态

**状态**: A1 现在不严格 (wl084), 暂不可写. 只能写 conditional paper
("假设 A1, ...").

---

### F.2 Stoll-Bruin Chabauty 工具调研 ⭐

**出处**: wl080 §六, wl079 §五

**思路**: Stoll/Bruin 的 Chabauty 工具是否能用 (替代 Magma).

**工作量**: 1 周调研

---

### F.3 Mazur uniform bound 文献 ⭐

**出处**: wl080 §六

**思路**: 是否能用 Mazur 风格的 uniform bound 论证 closure-fiber 闭包.

**工作量**: 几周深度文献

---

### F.4 Peschmann §7(2) 文献深读 + modular search 实施 ⭐⭐

**出处**: wl036 §五

**思路**: Peschmann arXiv 2604.09328 §7(2) 的 modular search (45 primes < 200)
是否能直接迁移.

**工作量**: 1-2 周

---

## 优先级汇总

按"真正可推动证明 + 可行性高"排序:

1. **A.2 cycle linear relation 追踪** ⭐⭐⭐ (与 E.3 联动)
2. **A.1 K_n hub partner identity 推广** ⭐⭐ (有突破性)
3. **A.3 Heegner sieve on outliers** ⭐⭐
4. **D.1 110 个 F₂-rank ≥ 3 pair PARI ellrank** ⭐⭐⭐ (低成本数据)
5. **A.5 扩 safe_sieve 到 Peschmann 规模** ⭐⭐
6. **C.2-C.4 工程小项** ⭐⭐⭐ (低成本工程)
7. **E.1-E.2 G_M BFS 扩展 + K_9/K_10 ellrank** ⭐⭐
8. **A.6 K_n vs 4-chain 严格关系** ⭐⭐ (纸面工作)

按"工作量低 + 立即可做"排序:

1. **C.4** proof_status schema (半天)
2. **C.3** rank_zero F₂-rank short-circuit (1 天)
3. **C.2** multi_n_sieve 接入 pipeline (1-2 天)
4. **D.1** 110 pair PARI ellrank (1-2 天)
5. **E.1** max_value 推到 10M (几小时, BFS 并行已 ready)
6. **E.2** K_9/K_10 ellrank (1 天)

---

## 维护规则

- 启动一项任务时, 在该 section 加 "🚧 in progress (wlXXX)"
- 完成时移除条目 + 在对应 wl 中标注 "回填到 OPEN_DIRECTIONS.md 移除"
- 否定时改为 🛑 + 简述结论
- 新发现的方向直接 append 到对应 section
