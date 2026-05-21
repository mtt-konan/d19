# 进阶理论方向（长期突破层）

这份文档承接 [THEORY_DIRECTIONS.md](./THEORY_DIRECTIONS.md)，但定位完全不同：

- `THEORY_DIRECTIONS.md` 写的是“能在几周内落到 `chain-fast` / `concordant` 里的安全前筛”。
- 本文写的是“可能直接撬动 Harborth 猜想本身”的方向，**工程上不一定更快，但理论深度更高**。

如果你只想加速搜索，先看 `THEORY_DIRECTIONS.md`。  
如果你已经接受“现有范式可能就是天花板”，继续看本文。

---

## 实现状态速查（2026-05 更新）

本文描述的方向已经有一部分被工程化，集中在 `proof_status` 模块和 `scripts/prove_no_solution.py`：

| 方向 | 实现状态 | 入口 |
|------|---------|------|
| 方向五（Heegner 点构造） | 🟡 stub（保留 method 名 `heegner`，调用即 `skipped`） | `proof_status/methods.py::run_heegner_stub` |
| 方向六（L-函数高阶导数 / BSD 精细化） | 🔴 未开始 | — |
| 方向七（Chabauty / QC） | 🟡 stub | `proof_status/methods.py::run_chabauty_stub` |
| 方向八（Brauer–Manin） | 🟡 stub | `proof_status/methods.py::run_brauer_manin_stub` |
| 方向九（Second descent） | 🔴 未开始 | — |
| 方向十（K3 曲面） | 🔴 未开始 | — |

同时已有的、属于"短中期"层但被集成进同一 pipeline 的方法：

| 方法 | 实现状态 | 入口 |
|------|---------|------|
| `safe_sieve` 2-adic 必要条件 | ✅ 完成 | `proof_status/methods.py::run_safe_sieve` |
| `factor_concordant` 因子分解攻击 | ✅ 完成 | `proof_status/methods.py::run_factor_concordant` |
| `rank_zero`（PARI ellrank） | ✅ 完成 | `proof_status/methods.py::run_rank_zero` |

**实测数据（max_hyp=500，6172 个 reduced pair；max_hyp=100 数据括号附后）**：

- `no_solution` 严格证明：5852（94.82%；max_hyp=100 时 238/93.7%）
  - 由 safe_sieve 砍掉：5632
  - 由 factor_concordant 砍掉：220
- `hard_case`（pipeline 用尽，需更深方法）：320（5.18%）
- 全部 `rank ≥ 1`，rank 过滤器实测过滤率 0%（与既有结论一致）

**hard_case 的 rank 分布（max_hyp=500，320 个）**：

| rank | 数量 | 占比 |
|---:|---:|---:|
| 1 | 118 | 36.9% |
| 2 | 155 | **48.4%（主流）** |
| 3 | 43 | 13.4% |
| 4 | 4 | 1.2% |
| imprecise（lower < upper） | **0** | **0%** |

**两个关键发现**：

1. **PARI rank 精确率 100%**——320/320 都是 lower==upper。这进一步确认方向六（L-函数判 rank）和方向九（second descent 压 Selmer 上界）作为"判 rank"工具**完全冗余**。
2. **rank=1 不再是大多数**——仅 36.9%，主流是 rank=2（48.4%）。意味着方向五 Heegner（仅对 rank=1 有效）能砍 hard_case 的上限是 **~37%**，剩下 63% 必须靠方向七 Chabauty 或方向八 Brauer–Manin。

**hard_case 比例稳定在 5–6%**：

| max_hyp | 总 pair | hard_case | 比例 |
|---:|---:|---:|---:|
| 100 | 254 | 16 | 6.3% |
| 500 | 6172 | 320 | 5.2% |

意味着不增加新 method 的话，hard_case 数量随 max_hyp 大致线性增长。

意义：**项目首次有了一个"可累积的、严格的不存在性证据库"**——每加一个新方向（方向五/七/八），就把更多 hard_case 标记为 `proven_no_solution`。

CLI 入口：

```bash
uv run python scripts/prove_no_solution.py --max-hyp 100 --db .cache/proofs.sqlite3
uv run python scripts/prove_no_solution.py --pair 7,45  --db .cache/proofs.sqlite3
uv run python scripts/prove_no_solution.py --db .cache/proofs.sqlite3 --report
```

---

## 写在最前面：会更快吗？

诚实回答：

| 维度 | 是否更快 | 备注 |
|------|---------|------|
| 找解的工程速度 | ❌ 不会 | 需要 SageMath / Magma / PARI 高级模块 |
| 单对 `(A,B)` 的判定速度 | ✅ 可能更快 | Heegner 点是 O(1) 解析公式 |
| 学习与开发周期 | ❌ 慢 | 本科代数几何 / 椭圆曲线高级课程级 |
| 接近“证明或反证”的速度 | ✅ 更快 | 把过滤器变判定器，把搜索变证明 |

一句话：**这些方向不是为了"找解找得更快"，而是为了"判得更死"**。

---

## 方向五：Heegner 点直接构造法

### 核心想法

当前 `concordant` 已经发现：所有 chain-fast 产出的 `(A, B)` pair 对应的椭圆曲线
$$E: Y^2 = X(X + A^2)(X + B^2)$$
都满足 `rank ≥ 1`。换句话说，rank 这个过滤器**完全失效**。

但 `rank ≥ 1` 只告诉我们"曲线上有有理点"，没告诉我们"那个有理点的 X 坐标是不是 N²"。

**Heegner 点公式**给出了一种可能性：当 `rank = 1`（绝大多数情况）时，曲线的 generator 可以由 CM（复乘）理论显式构造：

$$P_K = \mathrm{tr}_{H/K}\left(\sum_{[\mathfrak{a}] \in \mathrm{Cl}(O_K)} \varphi([\mathfrak{a}])\right)$$

这给出 generator 的 X 坐标的**解析表达式**。

### 为什么"快"

- 对每个 `(A, B)`，不再"在某个 bound 内枚举 N"。
- 而是**直接算出 generator**，看它的 X 坐标是不是某个整数的平方。
- 如果不是，且整个 Mordell-Weil 群由 generator + 挠点生成，就**严格证明了不存在 concordant 整数 N**。

### 工程化路径

1. 用 `sage` 的 `EllipticCurve.heegner_point(D)` API（D 是合适的判别式）
2. 或者直接查 [LMFDB](https://www.lmfdb.org/) 的椭圆曲线数据库，很多 concordant 曲线的 generator 已经预算好
3. 集成到 `concordant` workflow 作为 `--method heegner`

### 风险与已知障碍

- Heegner 点只有在 `rank = 1` 时给出 generator；`rank ≥ 2` 的少数情况要另想办法
- `Heegner hypothesis`（判别式条件）不一定对所有 `(A, B)` 成立，需要换 `D`
- Sage 的实现对大判别式可能很慢

### 难度评估

- **数学难度**：中（需要懂 CM 理论和 Gross–Zagier 公式的陈述，但**不需要懂证明**）
- **工程难度**：低（Sage 现成 API）
- **预期收益**：**高**（绝大多数 chain pair 一次性判完）

---

## 方向六：L-函数高阶导数与 BSD 精细化

### 重要更新（2026-05）

**当前 `proof_status` pipeline 里的 `rank_zero` 方法已经通过 PARI `ellrank` 拿到精确 rank**：
对 `max_hyp=500` 的全部 320 个 hard_case，**100% 实测 `lower == upper`**
（118 rank=1, 155 rank=2, 43 rank=3, 4 rank=4，imprecise 数为 0）。

所以方向六**作为"判 rank 的前置体检"已经被 PARI 顶替**。它仍可能有用的场景：

- 极少数情况下 PARI 给不出精确 rank（`lower < upper`，Selmer 群存在 2-Sha 不确定性）
- 配合 Gross–Zagier 公式估计 generator 的 **canonical height**——这是 PARI 不直接提供的
- 作为后续 BSD-conditional 分析的工具入口

下面是原始描述，保留作为理论背景。

### 核心想法

BSD 猜想的精细形式：
$$\mathrm{ord}_{s=1} L(E, s) = \mathrm{rank}(E)$$

我们已经知道 rank ≥ 1（即 $L(E, 1) = 0$），但不知道 rank 到底是 1、2 还是更高。

**思路**：用 modular symbols 数值算 $L'(E, 1), L''(E, 1), L'''(E, 1)$，区分：

- $L'(E, 1) \neq 0$ → rank = 1，可用 Heegner 点
- $L'(E, 1) = 0, L''(E, 1) \neq 0$ → rank = 2，需用方向七
- 更高阶 → 极少见，需要更深工具

### 工程化路径

- `sage`：`E.lseries().deriv_at1()` 系列 API
- 数值精度需要小心，但有现成的 Pari/GP 算法

### 难度评估

- **数学难度**：中（懂 L-函数和 BSD 陈述即可）
- **工程难度**：低
- **预期收益**：**低**（PARI 已经精确给 rank；只在 height 估计场景有用）

---

## 方向七：Chabauty–Coleman 与 Quadratic Chabauty

### 核心想法

椭圆曲线只是 4-cycle 问题的一个切面。如果把变量提升：

$$(A, B, N, h_3, h_4) \in \mathbb{Z}^5$$

加上联立条件 $h_3^2 = A^2 + N^2$、$h_4^2 = N^2 + B^2$、`a + c = b + d` 等，这定义了一条**亏格 $g \geq 2$ 的高亏格曲线** $C$。

**Chabauty 定理**：当 $\mathrm{rank}(\mathrm{Jac}(C)) < g$ 时，$C(\mathbb{Q})$ 是**有限集**，且可以用 $p$-adic 积分**枚举完全部**。

**Quadratic Chabauty**（Balakrishnan–Müller, 2017–2023）：把可处理范围扩展到 `rank = g` 的情形。已经成功解决了多个之前认为不可解的 Diophantine 问题，包括著名的 "cursed curve"（Bilu–Parent 模曲线 $X_s(13)$）。

### 为什么"是真正的判定器"

不像过滤器只能"砍候选"，Chabauty 给出曲线上**全部有理点的有限列表**：

> "我证明了这条曲线上有理点只有这几个：$P_1, P_2, \ldots, P_n$，列完了。"

如果列出来的点都不对应整数 N（例如 X 坐标不是平方数），就**严格证明** Harborth 在这条切面上无解。

### 工程化路径

1. 把 chain 系统翻译为单变量曲线方程（对 `(A, B)` 固定后，关于 `(N, h_3, h_4)` 的曲线）
2. 用 Magma 或 SageMath 计算 `Jac(C)` 的 Mordell–Weil rank
3. 调用 `Chabauty` / `QCMod` 包做 $p$-adic 计算
4. 验证有理点列表是否覆盖整数解

### 风险与已知障碍

- 需要 **Magma** 商业许可（有学术免费版），或 SageMath 的 `qc_mod` 实验包
- 高亏格曲线的 Mordell–Weil rank 计算可能本身就是难题
- Quadratic Chabauty 对每条曲线都要单独调参

### 难度评估

- **数学难度**：高（需要懂 $p$-adic 几何、Coleman 积分、Iyer–Müller 算法）
- **工程难度**：高（Magma 集成 + Sage QC 包）
- **预期收益**：**极高**（一次性证明某类 pair 不存在解）

---

## 方向八：Brauer–Manin 障碍

### 核心想法

当前所有局部筛（mod 8、mod $p^2$、Gaussian integer）都假设：

> 局部都过 ⟹ 全局可能有解（Hasse 局部-整体原理）

但 **Hasse 原理在 concordant 问题上已知会失效**。也就是说，存在 `(A, B)` 满足：

- 在所有 $\mathbb{Q}_p$（包括 $\mathbb{R}$）上都有解
- 但在 $\mathbb{Q}$ 上**没有**解

这种失效的标准刻画就是 **Brauer–Manin 配对**：

$$X(\mathbb{Q}) \subseteq X(\mathbb{A}_\mathbb{Q})^{\mathrm{Br}} \subseteq X(\mathbb{A}_\mathbb{Q})$$

如果某个 `(A, B)` 对应的代数簇 $X$ 在 Brauer–Manin 配对下被排除，就**不必搜索就证明无解**。

### 为什么是范式转换

现有所有方向都在"找解"或"砍候选"。Brauer–Manin 是直接证明：

> "这一大类 `(A, B)` 即使穷举所有局部条件都看不出问题，但 Brauer 群非平凡元素直接告诉我们全局无解。"

这是费马大定理之后整数论的**主流武器之一**，但国内做这个方向的人极少。

### 工程化路径

1. 写出 chain 系统对应的代数簇 $X$（很可能是某种 conic bundle 或 K3 曲面）
2. 用 Magma 的 `BrauerGroup` 包计算 $\mathrm{Br}(X) / \mathrm{Br}(\mathbb{Q})$
3. 对每个非平凡元素 $\alpha \in \mathrm{Br}(X)$，计算局部 invariants $\sum_v \mathrm{inv}_v(\alpha(P_v))$
4. 如果任何非零，则 $X(\mathbb{Q}) = \emptyset$

### 风险与已知障碍

- 计算 Brauer 群本身就是研究级难题
- 即使 Brauer–Manin 障碍非空，也不保证它捕获**所有**全局障碍（"Brauer–Manin 充分性"是另一个未解猜想）
- 国内可参考的工程实现极少

### 难度评估

- **数学难度**：极高（需要懂 étale cohomology、类域论、Tate 对偶）
- **工程难度**：极高
- **预期收益**：**极高**（如果成功，可能**直接证明 Harborth 猜想成立**）

---

## 方向九：Iterated 2-descent / Second descent

### 核心想法

标准 2-descent 给出 Selmer 群 $\mathrm{Sel}^{(2)}(E)$，关系：
$$\mathrm{rank}(E) \leq \dim_{\mathbb{F}_2} \mathrm{Sel}^{(2)}(E) - \dim_{\mathbb{F}_2} E(\mathbb{Q})[2]$$

差额由 Tate–Shafarevich 群的 2-挠 $\mathrm{Sha}(E)[2]$ 决定。

**Second descent**（Cassels–Cremona–Stoll）通过分析 2-Selmer 群的同源映射结构，进一步限制 $\mathrm{Sha}[2]$，把 rank 上界压紧。在某些情况下能直接证明 `rank = 0`。

### 为什么有用

我们之前以为 "rank ≥ 1 是事实"，但其实**只有 Selmer 群上界 ≥ 1**。如果 second descent 能把上界打到 0，就**反证**了 `rank ≥ 1` 这个假设。

### 工程化路径

- Sage 的 `E.descend_via_isogeny()` API
- Magma 的 `TwoDescent` + `SecondDescent` 包
- John Cremona 的 `mwrank` 工具

### 难度评估

- **数学难度**：高（需要懂 Galois cohomology 和 Tate–Shafarevich）
- **工程难度**：中（有现成工具）
- **预期收益**：中（可能让一部分 pair 反证 rank=0）

---

## 方向十：把 4-cycle 看作 K3 曲面

### 核心想法

固定 `(A, B)` 后是椭圆曲线，但**不固定**时呢？

把 $(A, B, N)$ 一起看作变量，加上 `(h_3, h_4)`，再加上 chain 闭合条件 `a + c = b + d`，得到的是 $\mathbb{P}^N$ 中的代数簇。

经过仔细计数（变量数 - 方程数 + 对称性），这个簇极有可能是一个 **K3 曲面**（2 维 Calabi–Yau）或更高维的 elliptic surface。

### 为什么 K3 是关键

K3 曲面有非常成熟的工具栈：

- **Picard rank** $\rho(X)$：刻画 $X$ 上的代数曲线类
- **Mordell–Weil lattice**（Shioda–Tate 公式）：刻画有理截面群
- **Néron–Severi group** 上的 Galois 表示

van Luijk、Elkies 等人在类似 Diophantine 问题（包括 Erdős–Ulam 问题、有理距离问题）上**已经用 K3 曲面工具取得进展**。

### 关键 payoff

Mordell–Weil lattice 给出**有理点高度的下界**。如果 chain-fast 的搜索范围对应的高度低于这个下界，就**严格证明在该范围内无解**——把"没找到"升级为"证明不存在"。

### 工程化路径

1. 仔细推导 chain 系统的代数簇方程（这本身是个数学工作）
2. 计算 Picard rank（用 reduction mod p + Tate 猜想，或者 Lefschetz 类）
3. 计算 Mordell–Weil lattice 的 Gram 矩阵
4. 推出高度下界

### 难度评估

- **数学难度**：极高（需要 K3 曲面专家级知识）
- **工程难度**：高（Magma 的 K3 工具栈，但需要手动推导曲面方程）
- **预期收益**：**革命性**（如果成功，得到的不仅是一个判定器，而是关于整个搜索空间的结构定理）

---

## 优先级建议（合并 THEORY_DIRECTIONS.md 的视角）

| 编号 | 方向 | 数学难度 | 工程难度 | 预期收益 | 推荐时机 |
|------|------|---------|---------|---------|---------|
| 一 | 因子分解攻击 ✅已实现 | 低 | 中 | 高 | — |
| 二 | Gaussian 整数 mod $p^2$ 筛 | 中 | 低 | 中（initial 阶段砍 pair） | 短期可做 |
| 三 | 标准 2-descent / Selmer | 高 | 高 | 高 | PARI ellrank 已隐含 |
| 四 | 对角符号筛加强 | 低 | 低 | 中 | 可选 |
| 五 | **Heegner 点 + canonical height** | 高 | 中 | 中（仅 rank=1，~37% hard_case） | 需 2-4 周 height theory |
| 六 | L-函数高阶导数 | 中 | 低 | **0** | PARI 已精确算 rank，此方向冗余 |
| 七 | Chabauty / Quadratic Chabauty | 高 | 高 | **高（rank≥2，~63% hard_case）** | 长期攻关 |
| 八 | Brauer–Manin 障碍 | 极高 | 极高 | **极高（理论上 100%）** | 学术合作 |
| 九 | Second descent | 高 | 中 | **0** | PARI 已给精确 rank，此方向冗余 |
| 十 | K3 曲面 / Mordell–Weil lattice | 极高 | 高 | **革命性** | 学术合作 |

**预期收益依据 max_hyp=500 实测**：rank 分布 36.9% rank=1 / 48.4% rank=2 / 13.4% rank=3 / 1.2% rank=4。

---

## 给学艺不精者的最实在建议（2026-05 更新）

**重要更新**：原本以为方向五能砍 hard_case 80%+，实测 max_hyp=500 后发现只有
**~37%** 的 hard_case 是 rank=1。原本以为只调通 PARI ellheegner 是 1-2 天，但
**严格判定还需要 canonical height bound（2-4 周 height theory 工作）**，不是
纯工程整合。

更新后的可行路径：

1. **短期能做的（1 周内）**
   - **方向二（Gaussian mod $p^2$ 筛）**：1 天，纯 Python，作用是在 initial 阶段
     多砍一些 safe_sieve 没砍掉的 pair。**不能升级 hard_case**，但能让 initial
     filter 更强。
   - **跑更大的 max_hyp**：把 hard_case 数据集做大，为后续理论工作积累样本。

2. **中期目标（2-4 周）**
   - **方向五完整版**（Heegner + canonical height）
   - 学习成本：读完 Silverman《Advanced Topics》第 III、VI 章
     （canonical height + Néron–Tate pairing）+ Sage / PARI 的 ellheegner API
   - 工程量：写真正的 `run_heegner` method，给 rank=1 的 pair 严格判定
   - 预期：能将 hard_case 中 ~37%（118/320 max_hyp=500）升级为
     `proven_no_solution`

3. **方向七、八、十作为长期目标**
   - 不要自己硬啃，找数学系合作者
   - 整理出所有 chain pair 数据 + 已经做出的 concordant 曲线分析，
     这本身就是合作的资产

---

## 参考文献

数论专著：
- **Silverman**, *The Arithmetic of Elliptic Curves*（基础）
- **Silverman**, *Advanced Topics in the Arithmetic of Elliptic Curves*（Heegner 点）
- **Skorobogatov**, *Torsors and Rational Points*（Brauer–Manin）
- **Schütt–Shioda**, *Mordell–Weil Lattices*（K3 曲面）

近期突破性论文：
- Balakrishnan–Müller, *Quadratic Chabauty: p-adic heights and integral points on hyperelliptic curves*
- Bremner, *On square values of quadratics and quartic polynomials*（与 Harborth 类问题相关）

工具栈：
- [SageMath](https://www.sagemath.org/) — 开源，覆盖 80% 的方向五、六、九
- [Magma](http://magma.maths.usyd.edu.au/) — 商业，但学术 license 免费，覆盖方向七、八、十
- [LMFDB](https://www.lmfdb.org/) — 椭圆曲线和模形式数据库，可直接查现成结果
- [PARI/GP](https://pari.math.u-bordeaux.fr/) — 项目已经在用，方向五、六、九都支持
