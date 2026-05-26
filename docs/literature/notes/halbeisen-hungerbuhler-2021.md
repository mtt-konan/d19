# Halbeisen & Hungerbühler 2021 — "Pairing Pythagorean Pairs"

**全名**: Halbeisen, L. & Hungerbühler, N. (2021). *Pairing Pythagorean Pairs*. arXiv:2101.08163.
**作者机构**: ETH Zürich, Department of Mathematics
**优先级**：⭐⭐⭐ — 与 d19 椭圆曲线**完全同构**的现代论文，给出 multi-N pair 概念的 rank-等价定理。
**状态**：PDF 已获取、§1-3 精读完成
**本地 PDF**：`../pdfs/halbeisen-hungerbuhler-2021-pairing-pythagorean-pairs.pdf`
**抽取文本**：`../pdfs/halbeisen-hungerbuhler-2021-pairing-pythagorean-pairs.txt`

---

## 一句话总结

H-H 给定义了"double-pythapotent / quadratic-pythapotent pair"概念，并证明这些性质**严格等价于**特定椭圆曲线（恰是 d19 的 E_{A, B}）有正秩。他们的曲线、torsion 群、参数化全和 d19 重合，但**关注的"特殊点类型"和我们不同**。

## 核心方程：与 d19 完全相同

```text
Halbeisen-Hungerbühler 2021                d19 (docs/MATH.md §8)
─────────────────────────────────         ────────────────────────────
Γ_{a, b}: y² = x³ + (a² + b²) x²           E_{A, B}: Y² = X(X + A²)(X + B²)
                  + a² b² x                       = X³ + (A² + B²) X²
        = x(x + a²)(x + b²)                          + A² B² X
```

**两者是同一个椭圆曲线**（只是字母大小写不同）。torsion 群也一致：

```text
torsion (Γ_{a, b}) ⊇ Z/2Z × Z/4Z   （对任意 (a, b)）
特殊情形 a² + b² = □：             看 §3 Proposition 7
特殊情形 (a, b) Pythagorean
       与 Γ_{a², b²}：              torsion = Z/2Z × Z/8Z（升级）
```

## 关键定义（论文 §1）

```text
1. pythagorean pair (a, b):  a² + b² = □

2. double-pythapotent pair:
   (a, b) Pythagorean,
   ∃ (k, l) Pythagorean s.t. (a·k, b·l) Pythagorean
   即三个条件:  a²+b²=□, k²+l²=□, (ak)²+(bl)²=□

3. quadratic-pythapotent pair:
   (a, b) Pythagorean,
   ∃ (k, l) Pythagorean (k,l 与 (a,b) 不互为倍数)
   s.t. (a²·k, b²·l) Pythagorean
```

## 关键定理（论文 §2-3）

```text
Theorem 2 (quadratic case):
  (a, b) is quadratic-pythapotent  ⇔  Γ_{a², b²} has positive rank over Q

Theorem 8 (double case):
  (a, b) is double-pythapotent     ⇔  Γ_{a, b} has positive rank over Q

Proposition 1 (torsion):
  (a, b) Pythagorean ⇒ Γ_{a², b²} torsion = Z/2Z × Z/8Z
  Moreover, every Γ with torsion Z/2Z × Z/8Z is isomorphic to some Γ_{a², b²}

Corollary 6 (side result):
  (a, b) quadratic-pythapotent ⇒ 有无穷多 (k, l) Pythagorean 使 (a²k, b²l) Pythagorean
  （同样适用于 double-pythapotent）
```

## 与 d19 的关系：同曲线、不同特殊点

**最关键的对应表**：

| 维度 | Halbeisen-Hungerbühler | d19 |
|---|---|---|
| 椭圆曲线 | Γ_{a, b} = x(x+a²)(x+b²) | E_{A, B} = X(X+A²)(X+B²) ✓ 完全同构 |
| (a, b) 条件 | 要求 a²+b²=□（Pythagorean pair） | 不要求（任意正整数对）|
| 关心的点 | rational points with "compatible (k, l)" structure | square-x points (x = N²) |
| 名字 | double-pythapotent / pythapotent of degree h | multi-N pair (k=n) |
| 等价定理 | (a,b) p.-potent ⇔ Γ_{a,b} 正秩 | multi-N 不等价于正秩，但 multi-N ⇒ 正秩 |

**核心差别**：
- H-H 的 "double-pythapotent": (a, b) Pythagorean 自身，存在另一 Pythagorean pair (k, l) 使乘积 (ak, bl) 也是 Pythagorean。是个**乘法配对**关系。
- d19 的 "multi-N": (A, B) 任意，存在 N₁, N₂ 使 (N_i, A) 和 (N_i, B) 都是 Pythagorean。是个**共享公共点**关系。

两者都是椭圆曲线 E_{A, B} 上的有理点问题，但**特殊点类型不同**：
- H-H 关心一般正秩点（→ pythapotent 配对）
- d19 关心 x = N² 形式的特殊点（→ concordant N）

## 对 d19 的可用结论

```text
1. ✅ E_{A, B} = Γ_{A, B} 同构 → d19 的 EC 工具栈可以直接对接 H-H 的所有 lemma/proposition
2. ✅ Torsion 分析、Kubert 参数化、点加倍公式 都已被 H-H 严格证明
3. ⚠️ "Γ_{a, b} 正秩 ⇔ double-pythapotent" 不直接告诉我们 "multi-N pair k≥2"
       两者都需要 Γ 正秩，但 multi-N 多了额外约束 (square-x)
4. ⚠️ H-H 的 main theorems 不直接给出 multi-N pair 的判据
```

## 与 Ono 1996 的关系

Ono 1996 用同一个曲线 E_{A, B} = E_Q(A², B²)，但用 ternary quadratic forms 处理
twist family rank。H-H 用 Schroeter/Kubert 参数化处理 torsion 升级。两者互补。

## Action items 与 d19 衔接

| 优先 | 任务 |
|---|---|
| ⭐⭐⭐ | 把 d19 multi-N pair 在 H-H 语言下**精确表述**，写进 PARTNER_GRAPH_THEORY.md |
| ⭐⭐ | 检查我们 K_8/K_7 实例 (P_a, P_b) 是否其中 (P_a, P_b) 自身是 Pythagorean pair（i.e. P_a² + P_b² = □），若是则 H-H 全套定理适用 |
| ⭐⭐ | H-H 的 Lemma 4/10 给出 doubling 公式 x_2 = (x_1² − B)² / (2y_1)²，对应 Ono Prop 1 的 P_N ∈ 2E(Q)，可以直接复用 |
| ⭐ | 跟踪 H-H 引用的 Bremner-Guy 1989, Knapp 1992 等历史源 |
