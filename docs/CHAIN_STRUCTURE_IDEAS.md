# Chain 结构研究想法（2026-05 头脑风暴整理）

本文档整理 4 个针对 Harborth 4-chain 数学结构的研究想法。这些想法出自 2026-05 文献调研后的头脑风暴，部分已确认在现有文献（Peschmann 2026、KSS 2019、Ono 1996）中**未被系统探索**。

> **配套文档**：
> - 数学定义和现有化简 → [`MATH.md`](MATH.md) §7
> - 文献对接 → [`literature/README.md`](literature/README.md)
> - 长期理论方向 → [`THEORY_DIRECTIONS_ADVANCED.md`](THEORY_DIRECTIONS_ADVANCED.md)

---

## 一、命名规则澄清（重要）

本项目存在三套并行命名，先在这里固化下来。

### 1.1 代码层（`src/.../search_chain.py`）

`ChainResult` 字段：

```
a, b, c, d ∈ ℤ⁺   ← 4-chain 的 4 条边（按顺序）
x1, x2, x3, x4    ← 4 个 hypotenuse
正方形条件:        a + c = b + d
```

4 个 Pythagorean 条件：

```
a² + b² = x₁²    ← 边 (a,b)
b² + c² = x₂²    ← 边 (b,c)
c² + d² = x₃²    ← 边 (c,d)
d² + a² = x₄²    ← 边 (d,a)
```

### 1.2 §7 化简层（`MATH.md` §7）

用本源勾股数三元组 $T_1=(p_1,q_1,h_1)$, $T_2=(p_2,q_2,h_2)$ 参数化，定义辅助量：

```
A := q₁ q₂                    （小腿之积）
B := p₁ p₂                    （大腿之积）
N := p₂(p₁-q₁) + q₁ q₂        （桥接量，自动满足 A < N < B）
```

化简后两个 concordant 条件：

```
A² + N² = □    (C₃)    ↔ 还原 T₃
N² + B² = □    (C₄)    ↔ 还原 T₄
```

### 1.3 头脑风暴中用户视角（本文档）

用户在讨论中习惯用 (B, b, A, N) 命名 4 条 chain 边，对应代码层的 (a, b, c, d)：

| 用户视角 | 代码层 | §7 化简 |
|---|---|---|
| B | a | $k_1 p_1$ |
| b | b | $k_1 q_1 = k_2 p_2$ |
| A | c | $k_2 q_2$ |
| N | d | $k_3 q_3$ |

⚠️ **陷阱**：用户视角的 (A, B, N) **不等于** §7 化简层的 (A, B, N)。前者是直观 chain 边，后者是参数化辅助量。**本文档之后统一使用代码层命名 (a, b, c, d)。**

---

## 二、想法 1 — 4 个 hypotenuse 的联合性质

> **实证更新 (2026-05, worklog [034](work-logs/034-hypotenuse-identity.md))**：
> 在 1005 个长方形 4-chain (`max_val=5000`) 上验证：
> - **恒等式 A 和 C 100% 数值通过** ✅（代数推导无误，是 d19 项目对 chain 结构的真实代数贡献）
> - **§2.4 "h_i 的奇素因子 ≡ 1 (mod 4)" 假设错误** ❌
>   Fermat-Euler 实际只对 primitive Pythagorean triple 的 hypotenuse 成立；
>   non-primitive 的 hypotenuse $kh$ 继承 scale $k$ 的任意素因子。
>   反例：$(66, 88, 105, 360)$，$h_1 = 110 = 2 \cdot 5 \cdot \mathbf{11}$。
> - 因此 §2.4 的 **blocker prime 论证不成立**。208/208 chain 都不能用此方式 obstruct。
> - 后续可探索方向（低优先级）：primitive part vs scale 分解后的更细约束。

**原始结论**：现有文献和 d19 §7 化简都把 $h_1, h_2$ 信息吸收进 $T_1, T_2$ 参数化里，从未显式利用。**反向利用 4 个 hypotenuse 是被忽略的研究方向。**

### 2.1 恒等式 A（无条件成立）

$$h_1^2 + h_3^2 = h_2^2 + h_4^2 = a^2 + b^2 + c^2 + d^2$$

证明：直接代入 4 个 Pythagorean 条件。

**含义**：4 个 hypotenuse 不独立，给定 3 个完全确定第 4 个的平方。

### 2.2 恒等式 B（正方形条件下）

设 $S = a + c = b + d$。则：

$$h_1^2 - h_2^2 = (a-c) \cdot S$$
$$h_3^2 - h_4^2 = (c-a) \cdot S = -(h_1^2 - h_2^2)$$

证明：

- $h_1^2 - h_2^2 = (a^2+b^2) - (b^2+c^2) = a^2 - c^2 = (a-c)(a+c) = (a-c) \cdot S$
- $h_3^2 - h_4^2 = (c^2+d^2) - (d^2+a^2) = c^2 - a^2 = -(h_1^2 - h_2^2)$ ✓

**含义**：正方形条件下，$(h_1^2 - h_2^2) + (h_3^2 - h_4^2) = 0$ 是恒等式 A 的等价改写。

### 2.3 恒等式 C（正方形条件下，最重要的新结果）

$$\boxed{(h_1 \cdot h_3)^2 - (h_2 \cdot h_4)^2 = (d - b)(a - c) \cdot S^2}$$

证明：用 Brahmagupta-Fibonacci 恒等式 $(x^2+y^2)(u^2+v^2) = (xu-yv)^2 + (xv+yu)^2$ 展开：

```
(h₁ h₃)² = (a²+b²)(c²+d²) = (ac-bd)² + (ad+bc)²
(h₂ h₄)² = (b²+c²)(d²+a²) = (bd-ac)² + (ab+cd)²
                          = (ac-bd)² + (ab+cd)²
```

减得：

```
(h₁ h₃)² - (h₂ h₄)² = (ad+bc)² - (ab+cd)²
                    = (ad+bc - ab - cd)(ad+bc + ab + cd)
                    = [a(d-b) + c(b-d)] · [a(d+b) + c(b+d)]
                    = (d-b)(a-c) · (a+c)(b+d)
                    = (d-b)(a-c) · S²    （正方形条件 a+c = b+d = S）
```

✓

### 2.4 恒等式 C 的应用：blocker prime 现象

**核心观察**：左边 $(h_1 h_3)^2 - (h_2 h_4)^2$ 受限于 4 个 hypotenuse 的素因子结构，右边 $(d-b)(a-c) S^2$ 是 chain 边的代数差。

每个 $h_i$ 是 hypotenuse → 它的奇素因子 $\equiv 1 \pmod 4$（Fermat 二平方定理）。

把恒等式 C 写成因子形式：

$$(h_1 h_3 - h_2 h_4)(h_1 h_3 + h_2 h_4) = (d-b)(a-c) \cdot S^2$$

如果存在素数 $p \equiv 3 \pmod 4$ 整除右边但不能整除左边的某个因子（因为 $p$ 不出现在 $h_i$ 的因子分解里），则**这个 $p$ 就是一个 blocker prime**。

**与 Peschmann §7(3) 的对应**：Peschmann 在 perfect cuboid 上观察到 88.4% case 的 blocker 都是 $p \equiv 1 \pmod 4$，没有 $p \equiv 3 \pmod 4$ 出现。我们在 4-chain 上能否找到同类现象？

### 2.5 行动建议

| 优先 | 任务 |
|---|---|
| ⭐⭐ | 写脚本验证恒等式 C 在 chain_fast.db 现有 4-cycle 上数值成立 |
| ⭐⭐ | 扫所有已知 4-cycle 提取 $(d-b)(a-c) S^2$ 的素因子分解，统计 mod-4 分布 |
| ⭐ | 推 hypothenuse 之间的更高阶恒等式（如 $h_1 h_2$、$h_1 + h_2$ 是否有意义）|

---

## 三、想法 2 — 正方形 vs 长方形条件强度

**结论**：这是一个**观察**，不是单独的研究方向。背后的数学就是整个 d19 项目的核心难题。

### 3.1 实证数据

worklog 014 记录：

| max_val | 找到 4-cycle（长方形）| 满足 $a+c=b+d$（正方形）|
|---|---|---|
| 100 | 206 | **0** |
| 500 | 2525+ | **0** |

强度比 = 0 / 2525 = 无穷强。

### 3.2 数学解释

**长方形条件**（4 个独立 Pythagorean）：
- 自由度高，几何上是任意"4 个直角三角形围成 cyclic quadrilateral"
- 解大量存在（如 (3,4,3,4) 在 6×8 矩形中心）

**加上正方形条件 $a+c=b+d$**：
- 通过 §7 化简强制把 4 个 Pythagorean **耦合到同一条椭圆曲线** $E_{A,B}: Y^2 = X(X+A^2)(X+B^2)$ 上找一个 $X = N^2$ 形式的有理点
- "在 EC 上找有理点"容易（一般 rank ≥ 1，KSS 算法可以找）
- "在 EC 上找 X 是平方数的有理点"极难 — **这就是 Euler 协调形式问题**

### 3.3 与 Peschmann 的对应

Peschmann 2026 §7 在 perfect cuboid 上看到完全同类现象：他的 quartic pair $f_1, f_2$ 单独都有解，但同时是平方的从来没出现过。Peschmann 把这定位为"reduction-then-no-square"，d19 的"正方形 vs 长方形"是同一个数学难度。

### 3.4 行动建议

不需要单独动手。把这个观察写进未来 paper 的 introduction：

> "While general 4-chains (without the square-closure constraint) admit thousands of solutions in our search range, **no instance has ever been found that simultaneously satisfies the closure $a+c=b+d$**. This phenomenon — solvable in isolation but not jointly — is the same obstruction that drives the perfect-cuboid problem ([Peschmann 2026, §7])."

---

## 四、想法 3 — 2-descent on $E_{A,B}$

> **工具更新 (2026-05, worklog [035](work-logs/035-pari-selmer-api.md))**：
> 经过 PARI API 探查，**无需装 SageMath** 即可拿到 2-descent 全部输出：
> - `pari.ellrank(E, effort)` 已经返回 4 元组 `[rank_lo, rank_hi, sha2_lo, gens]`
> - `pari.ell2cover(E)` 直接给出 Selmer 群的 quartic covers（= Sage `E.two_descent()` 的核心输出）
> - `pari.elltors(E)` 给出完整 torsion 结构
>
> 项目 bug：现行 `concordant.analysis.compute_rank` 只用了 4 元组里的前 3 项，
> 丢了 sha2。修这个 bug 是 worklog 036 的第一步。
>
> 余下工作量从"装 Sage 1-2 天"降为"在现有 PARI 上跑 batch + 写 Peschmann §6
> 的 obstruction logic"。

**结论**：直接对应 Peschmann §6 的方法。**所有底层计算工具已经免费在 cypari2 里**。

### 4.1 思路

对 hard_case 的椭圆曲线 $E_{A,B}: Y^2 = X(X+A^2)(X+B^2)$ 调用 Sage 内置的 `E.two_descent()`：

```python
from sage.all import EllipticCurve
E = EllipticCurve([0, A**2 + B**2, 0, A**2 * B**2, 0])
descent_data = E.two_descent()    # 计算 2-Selmer group
```

输出包含：
- 2-Selmer rank（理论上是 rank 的上界）
- 各 descent class 的代表
- "trivial" / "non-trivial" 标记

### 4.2 与 Peschmann §6 的对应

Peschmann **Theorem 6.2**（2-descent obstruction）：若某个 2-descent 标量 $\delta_3 = 1$，则 $f(P) \notin \mathbb{Q}^{*2}$，即排除整个 descent class。

我们的 hard_case 都是 rank=1（确认有 generator 但没找到 chain-兼容 N）。如果它们的 2-Selmer 结构特殊（比如 $\delta_3 = 1$），直接给出 obstruction。

### 4.3 行动建议

| 优先 | 任务 |
|---|---|
| ⭐⭐ | 装 SageMath（推荐 conda 或 Docker） |
| ⭐⭐ | 在 hard_case 的前 10 个 (A,B) 上跑 `E.two_descent()` |
| ⭐ | 如果 2-Selmer 结构有规律，写 Lemma 把规律变成 obstruction 定理 |

工程注意：Sage 装起来不便宜（>2GB），可以先用 Docker `sagemath/sagemath` 镜像试。

---

## 五、想法 4 — 对偶 EC 视角

> **实证更新 (2026-05, worklog [033](work-logs/033-dual-ec-probe.md))**：
> 在 150 个 D4-distinct chain near-miss 候选上跑双 EC rank 联合分布，
> **0 个 dual EC 是 certified rank=0**。所有看似 rank=0 的样本在
> PARI `ellrank(E, effort=2)` 下都升级到 rank=2。
> chain near-miss 上对偶 EC **不提供 free obstruction**。下面的设想保留
> 作为历史参考。
>
> **副产品**：发现 cypari2 的 `ellrank` 默认 effort 太浅，会系统性给出
> 虚假的 rank=0；以及 `ellanalyticrank` 在中等 conductor 上能跑数小时。
> 详见 worklog 033。

**原始结论**（已被实证否定）：这是 4 个想法里**潜力最大**的一个。**没有任何文献系统做过对偶 EC 视角**。直接对应 d19 现有 116 个 hard_case 的瓶颈。

### 5.1 4-chain 的两条对角线

4-chain 几何上：

```
   a ——— b
   |     |
   d ——— c
```

两条"对角线"（按节点配对）：

- **对角线 1**: $(a, c)$ — d19 现有方向，对应 $E_{a,c}: Y^2 = X(X+a^2)(X+c^2)$
- **对角线 2**: $(b, d)$ — **对偶方向**，对应 $E_{b,d}: Y^2 = X(X+b^2)(X+d^2)$

### 5.2 同一个 4-chain 给出两条 EC 上各 2 个有理点

| 对角 | EC | 有理点 1 | 有理点 2 |
|---|---|---|---|
| $(a, c)$ | $E_{a,c}$ | $X = b^2$（来自 $a^2+b^2=\square$ 和 $b^2+c^2=\square$）| $X = d^2$（来自 $c^2+d^2=\square$ 和 $d^2+a^2=\square$）|
| $(b, d)$ | $E_{b,d}$ | $X = a^2$（来自 $b^2+a^2=\square$ 和 $a^2+d^2=\square$）| $X = c^2$（来自 $b^2+c^2=\square$ 和 $c^2+d^2=\square$）|

**正方形条件 $a+c=b+d=S$** 翻译成对偶语言：

- 在 $E_{a,c}$ 上：$\sqrt{X_{P_1}} + \sqrt{X_{P_2}} = b + d = S$
- 在 $E_{b,d}$ 上：$\sqrt{X_{Q_1}} + \sqrt{X_{Q_2}} = a + c = S$

每条 EC 上**两个有理点的"sqrt(X) 之和"等于 chain 周长 $S$**。

### 5.3 双 EC 接力 obstruction（核心新方法）

设我们有一个 hard_case：(A=c, B=a)，$E_{A,B}$ rank=1，传统方法（rank 不可达 0、Heegner 太大、safe_sieve 不通过）无法 close。

**对偶视角**：每个 chain 候选 $(a, b, c, d)$ 同时给出对偶 EC $E_{b, d}$。

- 如果 $E_{b,d}$ rank = 0 → 它上面只有 torsion 点 → **可以直接枚举所有有理点验证**，从而排除整个 chain 候选

这是一种"两边接力"：原方向攻不动，绕到对偶边攻。

**预期统计行为**：116 个 hard_case 里，可能有显著比例的对偶 $E_{b,d}$ 是 rank=0 的，每一个都是免费 obstruction。

### 5.4 与 Peschmann 的关系

Peschmann 2026 在 perfect cuboid 上**没有**用到对偶视角 — 他的 quartic pair $f_1, f_2$ 是同质的。原因是 cuboid 的对称性结构跟 chain 不同：cuboid 是 3D，chain 是 2D 4-cycle。

**这意味着**：对偶 EC 视角是 4-chain 问题**特有的工具**，cuboid 没有对应物。如果可以做出来，是 d19 项目可以发表的真正新结果。

### 5.5 行动建议

| 优先 | 任务 |
|---|---|
| ⭐⭐⭐ | 写脚本：从 chain_fast.db 抽 50 个 (A,B) hard_case，每个算 $E_{a,c}$ 和 $E_{b,d}$ 的 rank，统计联合分布 |
| ⭐⭐⭐ | 如果统计漂亮：写 Lemma "对偶 $E_{b,d}$ rank=0 时排除整个 chain 候选" |
| ⭐⭐ | 进一步：研究 $E_{a,c}$ 和 $E_{b,d}$ 之间的代数关系（可能存在显式同源关系）|

---

## 六、想法之间的关系

```
想法 4（对偶 EC）─┐
                  ├─→ 联合形成 "利用 chain 4 边对称性 + 4 hypotenuse" 的研究 program
想法 1（hypotenuse 恒等式）─┘

想法 2（正方形强度）  → 写进 paper introduction，作为 motivation
想法 3（2-descent）   → 已知工具（Peschmann §6 用过），快速套用
```

**最优组合**：想法 1 + 想法 4。两者都从"chain 的 4 边/4 hypotenuse 对称性"出发，互相支撑：

- 想法 1 给出 $h_1, h_2, h_3, h_4$ 之间的代数恒等式
- 想法 4 给出 $E_{a,c}$ 和 $E_{b,d}$ 之间的对偶关系
- 两者一起可能给出"双 EC + 双 hypotenuse 联合 obstruction"

---

## 七、行动优先级总表

| 想法 | 是否可马上动手 | 工作量 | 文献是否做过 | 优先级 |
|---|---|---|---|---|
| ~~**1** hypotenuse 恒等式 + blocker prime~~ | ✅ | 已做 | 没做过 | △ 恒等式 ✅ / blocker 论证 ✗ ([wl 034](work-logs/034-hypotenuse-identity.md)) |
| **2** 正方形条件强度 | 不需动手（写 intro）| — | 同 Peschmann §7 | — |
| **3** 2-descent on $E_{A,B}$ | ✅（**PARI 已自带**，见 [wl 035](work-logs/035-pari-selmer-api.md)）| 半天-1 天 | Peschmann §6 已用 | ⭐⭐⭐（最高） |
| ~~**4** 对偶 EC 视角~~ | ✅ | 已做 | **没做过** | ✗ 已实证否定 ([wl 033](work-logs/033-dual-ec-probe.md)) |

**推荐起手顺序（2026-05 更新）**：

1. ~~**想法 4 的 probe 脚本**~~ — 已做，实证为负面，见 worklog 033
2. ~~**想法 1 的恒等式 C 验证**~~ — 已做，恒等式正确但 blocker prime 论证错误，见 worklog 034
3. ~~**想法 3 工具调研**~~ — 已做，PARI 自带 `ell2cover` / `ellrank` 4-tuple，
   无需装 Sage，见 worklog 035
4. **想法 3 实证（worklog 036+）**：先读 Peschmann §6 的 Theorem 6.2 实现细节，
   再在 116 个 hard_case 上跑 `pari.ell2cover` 批量分析，复刻"δ₃=1 obstruction"

---

## 八、相关 worklog

- `work-logs/032-literature-review.md` — 本 ideas 的上下文（文献调研）
- `work-logs/033-dual-ec-probe.md` — 想法 4 实证：dual EC rank 联合分布，**0 个 free obstruction**
- `work-logs/034-hypotenuse-identity.md` — 想法 1 实证：恒等式 A/C 100% 验证 ✅，但 §2.4 blocker prime 论证基础假设错误 ❌
- `work-logs/035-pari-selmer-api.md` — 想法 3 工具发现：PARI 已自带 ell2cover/Sha2，**无需装 Sage**
- `work-logs/036-compute-rank-fix-and-ell2cover-batch.md` — compute_rank 4-tuple 修复 + 320 hard_case ell2cover 批量，发现 2 个 sha2=2 case
- `work-logs/037-finite-descent-on-hard-cases.md` — Peschmann §7(2) 风格两层 modular search，320 hard_case × N ≤ 10^8 零 chain solution
- 后续动手时新建 `work-logs/038-...`（Heegner 完整版 / Cassels-Tate / Brauer-Manin / 更大 N_max）
