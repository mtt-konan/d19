# Knaf, Selder, Spindler 三部曲（2019-2020）

**配置**：三篇相关论文，研究协调形式椭圆曲线 $E_{M,N}: y^2 = x(x+M^2)(x+N^2)$ 上的有理点问题——**和 d19 的 $E_{A,B}$ 是同一族曲线**。

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

### 摘要要点（我从搜索片段拼出的）

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
| ⭐⭐⭐ | 下载并精读 KSS 1907.02148 § 2-3 的 reduction setup |
| ⭐⭐ | 把 KSS 算法和我们 `scan_rank_one_height` 对比，确认 PARI 输出一致 |
| ⭐ | 如果时间允许，扫一遍 1906.10230 § 1-2 的 quadrics→Weierstrass 公式 |
