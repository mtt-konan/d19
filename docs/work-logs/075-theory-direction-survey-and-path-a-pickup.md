# wl075 — 从 wl073 到 wl074 之间的讨论：理论方向梳理与路径 A 选择

## 触发

wl073 完成 multi-N-first + 对偶筛流水线后，max_hyp ≤ 2M 实证全杀
（unconditional 模算术）。但用户提出了非常关键的反思：

> 即使极致速度也是要继续跑，全被杀掉也没有一个好结论。

也就是说，**纯实证扩 max_hyp 不构成证明**——它只能保证有限范围里没反例。
要真正"证明 Harborth 反例不存在"必须从理论侧切入，而不是无限刷 max_hyp。

本 wl 记录从 wl073 到 wl074 之间的所有**非实施性**讨论：方向梳理、决策、
路径 A 的选定，以及为后续工作（方向 1：A1 严格证明）铺路。

## 一、用户疑问 1：dual 筛验 C(k, 2) 对吗？

### 1.1 用户原话

> 突然想到个问题是多 n 生成算法，验证对偶时是否是验证 C(2, n) 对的？

### 1.2 答案与实测

**是的**。`find_surviving_n_pair(ns)` 对每个 (A, B) 的 N 列表 ns 做 C(k, 2)
全配对检查。但 max_hyp = 200k 实测分布：

```
k=2:  20,778  (98.3%)
k=3:     337  (1.6%)
k=4:      12  (0.06%)
k=5:       1  (0.005%)

Total multi-N pairs:           21,128
Total C(k, 2) dual checks:     21,871
Average C(k, 2) per pair:      1.035
```

⟹ **99.3% 的 multi-N pair 是 k=2，对偶筛实际几乎"每对验证一对"**。所以
工程开销不存在浪费。**但反过来这也意味着，99% 的 closure 命运由唯一一对
(N_1, N_2) 决定** —— 这成了选路径 A（k=2 fiber analysis）的关键依据。

## 二、理论方向梳理（5 条路径）

用户问"后续看看还有什么方向"。读完
[`THEORY_DIRECTIONS_ADVANCED.md`](../THEORY_DIRECTIONS_ADVANCED.md)、
[`PARTNER_GRAPH_THEORY.md`](../PARTNER_GRAPH_THEORY.md)、
[`CURRENT_FINDINGS.md`](../CURRENT_FINDINGS.md) 后整理出 5 条具体路径：

### 路径 A · 短期（1-2 周）— 证明 "k=2 closure 必失败"

- **设定**: 固定 (A, B)，假设 `concordant_N(A, B) = {N_1, N_2}` 且
  `N_1 + N_2 = A + B`
- **变量消去**: `N_2 = (A+B) − N_1`，得到 4 个对 N_1 的平方条件，关于
  `N_1 ↔ A+B−N_1` 有 D_4 对称
- **目标**: 把 4 个平方拼成单个 elliptic / hyperelliptic / K3 fiber，
  证 fiber 的 Q-rational point 集不含整数对应物
- **杠杆**: 99% multi-N pair 是 k=2，证完直接覆盖 99% 工作量

### 路径 B · 中期（4-8 周）— Uniform mod p² obstruction theorem

把当前实证「STANDARD_MODULI 杀光所有 partner pair」升级为定理：

> **猜测**：∃ 一个有限模数集 M_0 不依赖 (A, B)，使任何 reduced coprime
> safe-pass multi-N pair 必有 M ∈ M_0 让对偶筛杀掉。

- **现有证据**: max_hyp = 2M 上 14 个 prime² (M ≤ 53²) 完全够杀
- **若证成**: 彻底关掉整个 Harborth 反例搜索，纯模算术结论

### 路径 C · 中期（2-4 周）— Halbeisen-Hungerbühler 2024 套用

- 直接套已有定理，**最快出结果**
- H-H 2024 给出形如 `(a^h, b^h)` 的 multi-N pair 上的额外 sieve（Schroeter）
- 当前 catalog 找出 `(A, B) = (a^h, b^h)` 子集，套定理直接砍

### 路径 D · 工程取巧 — 把 dual 条件嵌入生成器

- 修改 `iter_concordant_a_n`：每生成 (A, N)，立即跑 chain_closure_mod_sieve
- 被杀的 N 不进入 a_sets[N]
- **不出新理论**，且当前 sieve 阶段才 0.07s（max_hyp=2M），收益有限

### 路径 E · 长期 / 需要协作 — Brauer-Manin 障碍

- 把 closure 翻译成代数簇 X(A,B) ⊂ P^N，找 Br(X) 非平凡元素证 X(Q) = ∅
- 需要 Magma + 数论合作者
- THEORY_DIRECTIONS_ADVANCED.md §方向七、八、十

### 优先级评估

| 路径 | 数学难度 | 工程难度 | 预期收益 | 时机 |
|---|---|---|---|---|
| **A** k=2 closure 必失败 | 中-高 | 中 | **高（99% 覆盖）** | **立即可做** |
| B uniform mod p² | 高 | 中 | 极高（100%） | 中期 |
| C H-H 2024 套用 | 中 | 低 | 中-高（特定子集） | 短-中期可做 |
| D 生成器嵌入对偶 | 低 | 低 | 低（仅工程） | 跳过 |
| E Brauer-Manin | 极高 | 极高 | 革命性 | 长期合作 |

## 三、用户疑问 2：G_M / comp0 是否研究方向？

### 3.1 用户原话

> 搜索一下，之前得到的 30w 巨大分量 comp0，和 G_m 之类那些东西，算是研究方向吗

### 3.2 调研后的答案

读 wl058 / wl061 / wl062 / wl066 后的判断：

> **是研究方向，且已是项目第二条主线**（仅次于 catalog/concordant）。
> 已经投入大量工程并拿到几个干净的结构性结果。**但目前仍停留在"实验观测
> + 统计"层级，没产出 unconditional 定理**。

具体进展：

| worklog | 关键 deliverable | 性质 |
|---|---|---|
| wl054-055 | partner identity + K_n 等价定理 | **代数事实**（已证） |
| wl058 | 错误假设 G_M 是 forest | 已修正 |
| wl061 | G_M 全 BFS：338,225 顶点 / 9,580 分量 / **comp0 = 309,689 + 22,115 cycle** | 数据 |
| wl062 | comp0 度数 **严格 = C(k, 2)**，K_9 / K_10 实例 | **代数事实**（已证） |
| wl063 | G_M 全图 829,444 长方形候选 closure 检查 | **0 命中** |
| wl066 | 829k 候选最近 \|Δ\|=1，仅 10 顶点；exact closure 是"极薄整点共振线" | 数据 |

### 3.3 G_M 跟反例证明的关系

- ✅ **作为反例搜索的强化版**：在 G_M 全图（不只 catalog）跑 closure，
  比 catalog 严密 30 倍
- ✅ **作为论文素材**：partner identity / K_n / degree=C(k,2) /
  scale-free / |Δ|=1 极薄
- ❌ **作为反例不存在的证明工具**：目前不行。没有从 G_M 结构推出
  "closure 必失败"的代数论证

**结论**：如果目标是 unconditional 证明 Harborth，G_M 不是最优路径——
它给搜索加杠杆，但不给定理。最有希望的还是路径 A + 路径 C。

## 四、路径 A 的选择决策

最终决策：**先做路径 A**。理由：

1. **覆盖面最广**：99% k=2 一次解决
2. **工具齐**：项目已有 PARI ellrank/elladd/ellbil/ellheight 全套
   （`heegner_height._curve` / `analysis._ensure_pari` 直接复用）
3. **可量化里程碑**：
   - 第一里程碑：实证 rank ≥ 2 universal on 1000+ k=2 sample
   - 第二里程碑：Conjecture A1 严格代数证明
   - 第三里程碑：closure-on-rank-2-fiber 的 Chabauty 处理
4. **风险有界**：即使第三里程碑失败，前两个里程碑独立有价值

跳过 D（工程取巧）。C 和 B 排在 A 之后并行。E 留给长期。

## 五、wl074 实施摘要

数学 setup + 实验都在 [wl074](./074-path-a-k2-closure-fiber-analysis.md) 详
述。这里只记关键结果：

```
实验脚本: scripts/analyze_k2_closure_fiber.py
  - 复用 heegner_height._curve / _finite_torsion_points
  - PARI effort=1 + 自动 effort=2 rerank for imprecise rows

实证累计:
  max_hyp 50k:    148/148 rank ≥ 2  (5s)
  max_hyp 200k:   495/495 rank ≥ 2  (9s)
  max_hyp 500k:  1093/1093 rank ≥ 2 (27s)
  max_hyp 1M:    1879/1879 rank ≥ 2 (68s)

rank 分布稳定 (max_hyp=1M):
  rank=2: 28.9%  rank=3: 48.7%  rank=4: 19.2%  rank≥5: 3.2%
  rank<2: 0/1879  (Conjecture A1 universal)
  P_{N_1} + P_{N_2} non-torsion: 1879/1879
```

**Conjecture A1**: 对任意 reduced coprime safe-pass `(A, B)`，
`|concordant_N(A, B)| = 2 ⇒ rank(E_{A, B}) ≥ 2`.

## 六、当前路径优先级（更新）

```
方向 1 (A1 代数证明):       下一步立即做
  - 关键 step: 证 δ(Q_{N_1}) ≠ δ(Q_{N_2}) 在 (Q*/Q*²)² 上独立
  - 工具: Halbeisen-Hungerbühler 2024 / Peschmann 2-descent map
  - 输出: 严格证明 sketch + paper 候选定理

方向 2 (closure-fiber Chabauty):    A1 证完后立即做
  - rank ≥ 2 ⇒ E(Q) free 至少 Z²
  - closure 是 1 维 Diophantine 条件 → fiber
  - 用 Chabauty / quadratic Chabauty 列出 fiber 上全部有理点

方向 3 (路径 C, H-H 2024 套用):     并行可做
  - catalog 中找 (A, B) = (a^h, b^h) 子集
  - 套 H-H Cor 7/8 验证

方向 4 (路径 B, uniform mod p²):    A1 证完后再考虑
方向 5 (路径 E, Brauer-Manin):      留给长期合作
```

## 七、文件 / 引用

```text
docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md  上一 wl
docs/work-logs/074-path-a-k2-closure-fiber-analysis.md       路径 A 实施
docs/THEORY_DIRECTIONS_ADVANCED.md                            5 条路径源头
docs/PARTNER_GRAPH_THEORY.md                                  G_M / partner identity
docs/CURRENT_FINDINGS.md                                      Selmer / Sha[2]
docs/work-logs/061-partner-graph-full-bfs-supercomponent.md   G_M 全 BFS
docs/work-logs/062-comp0-degree-Ck2-and-K10-discovery.md      comp0 度数
docs/work-logs/066-gm-clarify-and-delta-near-miss.md          |Δ|=1 near-miss
```

## 八、状态

- ✅ 用户疑问 1（dual 验 C(k,2) 对）回答 + 99.3% k=2 数据
- ✅ 5 条理论方向梳理与优先级
- ✅ 用户疑问 2（G_M / comp0 是研究方向但不是定理工具）回答
- ✅ 路径 A 选定理由
- ✅ wl074 实施完成（1879/1879 universal）
- ⏭ 下一步：方向 1 — Conjecture A1 严格代数证明
