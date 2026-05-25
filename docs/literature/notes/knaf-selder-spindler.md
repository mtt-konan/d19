# Knaf, Selder, Spindler 三部曲（2019-2020）

**配置**：三篇相关论文，研究协调形式椭圆曲线 $E_{M,N}: y^2 = x(x+M)(x+N)$ 上的有理点问题——**和 d19 的 $E_{A,B}$ 是同一族曲线**（取 $M=A^2,N=B^2$）。

---

## 论文 1：Quadrics → Weierstrass 显式变换

**arXiv**: 1906.10230 (2019)
**标题**: Explicit transformation of an intersection of two quadrics to an elliptic curve in Weierstrass form
**主要贡献**: 给出一个 explicit 算法把"两个二次型的交（rational smooth）"变成 Weierstrass form 椭圆曲线。

为什么是 KSS 三部曲的起点？因为 Diophantine 问题（包括协调形式问题）经常自然写成"两个二次型联立"，KSS 的 explicit 构造让后续算法变得 explicit。

### 与 d19 的关系

Harborth 4-chain 的核心条件 "$N^2 + A^2 = h_3^2$ 且 $N^2 + B^2 = h_4^2$" 本质上就是两个二次型联立——所以 KSS 的 quadrics-to-Weierstrass 变换可以**直接应用到我们的问题**。

我们当前用的 EC 方程 $E_{A,B}: Y^2 = X(X+A^2)(X+B^2)$ 实际上就是这个变换的结果（用代换 $X = N^2$, $Y = N \cdot h_3 \cdot h_4 / \text{某常数}$）。

---

## 论文 2：⭐ 找有理点算法（核心）

**arXiv**: 1907.02148 (2019)
**标题**: An Algorithm to Find Rational Points on Elliptic Curves Related to the Concordant Form Problem
**优先级**：⭐⭐⭐

**本地 PDF**：`../pdfs/knaf-selder-spindler-2019-algorithm.pdf`
**抽取文本**：`../pdfs/knaf-selder-spindler-2019-algorithm.txt`

### 摘要要点（已从全文抽取确认）

> "We derive an efficient algorithm to find solutions to Euler's concordant form problem and rational points on elliptic curves associated with this problem."
>
> "Points at infinity on $E_{M,N}$ correspond to the trivial solutions $(1, 0, \pm 1, \pm 1)$ of the concordant form equations and to the trivial solution (the degenerated triangle)."
>
> "An even more exciting example was discovered by Bremner and Cassels in [1] who considered the family of curves with equations $y^2 = x(x^2 + p)$ with prime numbers $p \equiv 5 \pmod 8$."

### 与 d19 的关系

**这是和 d19 最直接相关的现代算法论文。区别**：

| 维度 | KSS 1907.02148 | d19 |
|---|---|---|
| 方向 | 正向（找有理点）| 反向（证明无 chain 解）|
| 框架 | algorithm（高效）| pipeline（incremental）|
| 工具 | 数学算法描述 | Python + cypari2 实现 |
| 输出 | 找到的 (M,N,...) 解 | 已证 (A,B) 的 outcome |

### 对 d19 的价值

1. **学术对接**：引用这篇论文我们就有 family 的合法历史背景
2. **工具验证**：他们的算法可以验证我们 PARI Heegner 输出
3. **反向利用**：他们的算法在 hard_case 上"找不到点"，本身就是 d19 想要的证据

### 已确认算法结构

KSS 的定位不是“判定 rank”，而是在曲线已知/预期 positive rank 时找显式有理点。
全文 introduction 明确说：

```text
we are not interested in general discussions on the determination of the rank ...
but focus on finding explicit solutions.
```

核心步骤：

1. **2-descent / homogeneous space**：把原曲线 `E` 替换成某个 homogeneous space `Q`。
2. **两个二次型联立**：`Q` 写成 projective 3-space 中两个 quadrics 的交。
3. **Newton projection 参数化一个 quadric**：先从已知点参数化 `Q1=0`。
4. **剩下一个 quartic square test**：把参数代入 `Q2`，循环检查某个值是否平方。
5. **strong algorithm**：若某个 technical condition 成立，把 quartic 变成 biquadratic，再降成二次型与两个平方条件，搜索复杂度改善。

对 d19 的具体意义：

```text
KSS = 给正秩 concordant curve 找 rational points / generators 的工具
d19 multi-N = 在这些 rational points 里筛 x=N^2 且 Y=1 截面
```

因此 KSS 更适合服务：

- `(153,560)` rank=3 的 Mordell-Weil 结构解释；
- 26 个 `k=3` multi-N pair 的独立点分析；
- rank-audit 后对高 rank 样本找 generators；
- 比较不同 homogeneous spaces 是否对应不同独立点。

### 结构问题：独立点来自不同 homogeneous spaces

KSS §6.3 的结论对我们很关键：

```text
rk(E)=2 的例子中，每个用于找点的 homogeneous space 往往只给 rk(E_Q)=1；
要找 independent solutions，需要看两个不同且非 2-torsion 等价的 homogeneous spaces。
```

这为 d19 的 rank=3 / multi-N 样本提供了分析模板：

```text
不同 concordant N 是否来自不同 2-descent homogeneous spaces？
如果是，multi-N count 可能与 Selmer image / independent spaces 有直接关系。
```

这里还要加上一个来自 Ono 1996 Proposition 1 的修正：

```text
对 concordant N 点 P_N=(N^2, N*sqrt(N^2+A^2)*sqrt(N^2+B^2))，
x, x+A^2, x+B^2 三项本身全是平方，故 P_N 自动属于 2E(Q)。
```

因此真正该比较的不是 `P_N` 在 `E(Q)/2E(Q)` 中的类，而是它的 **half-points** `Q_N`。
换句话说：

```text
multi-N 不是“多个 2-descent 类”本身，
而更可能是“多个不同 half-points / homogeneous spaces 经 doubling 后命中 square-x 截面”。
```

对 `(153,560)` 已显式验证：

```text
2*(19992,  -17013192) = P_204
2*( 7560,   -8671320) = P_420
2*(  120,    -941160) = P_3900
```

所以后续若要解释 `(153,560)` 的三个 concordant `N`，应优先分析这些 half-points 的
2-descent image / homogeneous-space class，而不是直接分析 `P_N`。

下一步可对 `(153,560)` 的三个 `N=[204,420,3900]` 计算它们在 2-descent map 下的 image。

### 关键引用链

KSS 引用了 Bremner-Cassels 1984 关于 $y^2 = x(x^2+p)$ 的工作（**rank 非平凡的家族**），这进一步联系到 Ono 1996 的协调形式工作。

---

## 论文 3：四个有理平方在 AP

**期刊**: Math. Sem. Hamburg 91 (2020)
**arXiv 对应**: 通过 1906.10230 + 1907.02148 工具研究"四个有理数平方成等差数列"
**优先级**：⭐⭐

### 与 d19 的关系

弱相关。本论文研究的是 "4 squares in AP"，跟 d19 的 4-chain 是不同问题（一个是 AP 结构，一个是 chain 结构），但用同样的 EC family 工具，可以借鉴他们的 MW rank 计算技巧。

---

## 跨论文总结：KSS 程序对 d19 的指导

1. **不要重新发明轮子**：$E_{A,B}$ 的 quadrics 表述、Weierstrass 化、有理点找寻，KSS 已经做完了。我们要做的是**反向应用**。

2. **学习他们的 reduction 写法**：KSS 1907.02148 § 2-3 极可能有标准的 "concordant form → EC point" 的 Lemma 写法，可以照搬到 "4-chain → EC point"。

3. **关键 reference 追踪**：他们引用的 Bremner-Cassels 1984、Ono 1996 都是协调形式核心文献，d19 也应该引用。

---

## Action items

| 优先 | 任务 |
|---|---|
| ✅ | 下载并抽取 KSS 1907.02148 PDF/text |
| ✅ | 精读 KSS 1907.02148 § 2-4 的 reduction/algorithm setup |
| ⭐⭐ | 把 KSS 算法和我们 `scan_rank_one_height` 对比，确认 PARI 输出一致 |
| ⭐⭐ | 对 `(153,560)` 的三个 `N` 计算 2-descent image / homogeneous-space class |
| ⭐ | 如果时间允许，扫一遍 1906.10230 § 1-2 的 quadrics→Weierstrass 公式 |
