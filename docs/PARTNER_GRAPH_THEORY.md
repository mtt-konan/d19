# Partner Graph 理论 — multi-N pair 的图论 framing 与文献定位

本文档把 d19 项目在 wl048-wl056 通过实验逐步发现的 partner / K_n 结构，
和现有文献（Ono 1996, Halbeisen-Hungerbühler 2021/2024, Knaf-Selder-Spindler 2019,
Bremner-Ulas 2016）做严格对接。目的是建立后续讨论的**共同语言**，避免在术语模糊处来回打转。

> 本文不重复 [`MATH.md §8`](./MATH.md) 已有的椭圆曲线代数推导，只在必要处引用。
> 阅读顺序建议：先看本文 §2 定义，再回头看 MATH.md §8。

---

## 0. 字典：d19 术语 ↔ 文献术语

| d19 用语 | 文献用语 | 来源 |
|---|---|---|
| Pythagorean pair (a, b): a² + b² = □ | 同名 | 标准 |
| concordant N for (A, B) | concordant N | Ono 1996 |
| multi-N pair (A, B), k = n | (没有标准名，"strongly concordant pair" 略接近) | — |
| partner pair (P_a, P_b) of (A, B) | 无文献对应 | d19 wl054 |
| K_n subgraph (shared partner) | 无文献对应 | d19 wl055 |
| partner graph BFS from (A, B) | 无文献对应 | d19 wl056 起 |
| double-pythapotent pair (a, b) | 同名 | Halbeisen-Hungerbühler 2021 |
| pythapotent pair of degree h | 同名 | Halbeisen-Hungerbühler-Zargar 2024 |
| E_{A, B}: Y² = X(X+A²)(X+B²) | Γ_{a, b}, E_Q(A², B²) | H-H 2021, Ono 1996 |

---

## 1. 范围与不在范围

**在范围**：
- multi-N pair 的图论结构（partner、K_n、BFS）
- 与现有椭圆曲线框架（Ono / H-H / KSS）的精确对应
- 反例（Harborth 4-chain）搜索的代数翻译

**不在范围**（其他文档处理）：
- E_{A, B} 的 Weierstrass 化推导（见 MATH.md §8.2）
- 因子分解搜索 N 的算法（见 THEORY_DIRECTIONS.md 方向一）
- 4-chain 的 a+c=b+d closure 条件（见 MULTI_CONCORDANT_N_STRATEGY.md §2）
- BSD / Selmer / Heegner 高阶工具（见 THEORY_DIRECTIONS_ADVANCED.md）

---

## 2. 核心定义

### 2.1 Pythagorean graph G_P

```text
顶点集 V(G_P) = ℤ_{>0}（正整数）
边集 E(G_P) = { {a, b} : a² + b² ∈ □, a ≠ b }
（即 (a, b) 是 Pythagorean pair）
```

这是个**无穷图**。多数顶点孤立（不属于任何 Pythagorean pair）；非孤立顶点
之间形成密集子图（基于 Pythagorean parametrization (m² − n², 2mn)）。

### 2.2 concordant N（Ono 1996 framework）

给定正整数对 (A, B)，A < B，定义：

```text
concordant_N(A, B) := { N ∈ ℤ_{>0} :  N² + A² ∈ □  ∧  N² + B² ∈ □ }
                    = { N : {N, A}, {N, B} 都是 G_P 边 }
                    = N(A) ∩ N(B)  （Pythagorean graph 上 A 和 B 的公共邻居）
```

椭圆曲线对应（Ono 1996）：

```text
N ∈ concordant_N(A, B)  ⇔  E_{A, B} 上有点 P_N = (N², N·√(N²+A²)·√(N²+B²))
                              即 x-coordinate 为 N²（square-x 点）
```

### 2.3 multi-N pair（d19 项目用语）

```text
multi-N pair = (A, B) s.t. |concordant_N(A, B)| ≥ 2

k(A, B) := |concordant_N(A, B)|       k 是 multiplicity / 阶数
```

**几何意义**：(A, B) 在 Pythagorean graph 上**有至少 2 个公共邻居**。

### 2.4 partner pair（d19 wl054 引入）

```text
对 multi-N pair (A, B) 与 N_i, N_j ∈ concordant_N(A, B) (i ≠ j)，
对 (N_i, N_j) （sorted, smaller first）称为 (A, B) 的一个 partner pair。

记: partners(A, B) := { sorted(N_i, N_j) : N_i ≠ N_j ∈ concordant_N(A, B) }
                   = { 大小 2 的子集 } C(k, 2) 个
```

### 2.5 partner identity（d19 wl054 实证、wl055 数学化）

**定理（partner identity）**:

```text
对任意 (A, B) multi-N pair，对任意 (N_i, N_j) ∈ partners(A, B)：
(N_i, N_j) 自身也是 multi-N pair，且 A, B ∈ concordant_N(N_i, N_j)。
```

**证明**（直接展开）:

```text
N_i, N_j ∈ concordant_N(A, B)
⇒ N_i² + A² = □ ∧ N_i² + B² = □ ∧ N_j² + A² = □ ∧ N_j² + B² = □
⇒ A² + N_i² = □ ∧ A² + N_j² = □ ∧ B² + N_i² = □ ∧ B² + N_j² = □
⇒ A ∈ concordant_N(N_i, N_j) ∧ B ∈ concordant_N(N_i, N_j)
⇒ |concordant_N(N_i, N_j)| ≥ 2
⇒ (N_i, N_j) 是 multi-N pair，且 A, B 都是它的 concordant N
```

**图论意义**：multi-N 性质对四元组 {A, B, N_i, N_j} 是**对称**的。如果
把它们排成 K_{2, 2} 完全二部图 `{A, B} × {N_i, N_j}`，所有 4 条边都属于
Pythagorean graph G_P。也即：

```text
(A, B) 与 (N_i, N_j) 同时是 multi-N pair
⇔ K_{2, 2} `{A, B} × {N_i, N_j}` 嵌入 G_P
```

### 2.6 partner graph G_M

```text
顶点集 V(G_M) = { (A, B) : (A, B) 是 multi-N pair }
                即 G_P 中至少有 2 个公共邻居的 unordered 顶点对

边集 E(G_M) = { {(A, B), (N_i, N_j)} : N_i, N_j ∈ concordant_N(A, B) }
              ≡ partner identity 给出的对偶关系
```

注意 G_M 是无向的（partner identity 对称）。

### 2.7 K_n subgraph（d19 wl055）

```text
n 个数 {N_1, ..., N_n} ⊆ concordant_N(A, B)（同一 (A, B) 的 n 个公共邻居）
⇒ {A, B} × {N_1, ..., N_n} = K_{2, n} 嵌入 G_P

在 G_M 中：这 C(n, 2) 个 partner pair 全都连到 (A, B)，且它们彼此也通过 G_M 相连。
我们称此结构为 "shared-partner K_n"。
```

**wl055 等价定理**:

```text
(A, B) 是 k=n multi-N pair
⇔
其 N 列表 [N_1, ..., N_n] 上的 C(n, 2) 个 partner pair 全部以 (A, B) 为
shared-partner，且这 n 个 N 彼此两两在 G_M 中相邻
⇔
{A, B} × {N_1, ..., N_n} 是 K_{2, n} 嵌入 G_P
```

即 "K_n 子图" ≡ "k=n multi-N pair"，**不是新结构，是对偶视角**。

### 2.8 partner graph BFS（用户在 wl056 提出）

```text
从 (A, B) ∈ V(G_M) 出发的 partner BFS：
  level 0:  { (A, B) }
  level 1:  partners(A, B) = C(k(A,B), 2) 个新顶点
  level 2:  对每个 level-1 顶点继续展开
  ...
  叶子条件: 当某个顶点 (X, Y) 满足 k(X, Y) = 2 时，它没有可展开的新 partner
            （只有 1 个 partner，且已经包含上一层节点）
```

这是 G_M 上的标准 BFS。**未解决问题**：

```text
Q1.  G_M 的连通分量结构是怎样的？
Q2.  从 (A, B) 出发的 BFS 是否一定能到达所有"接近"的 multi-N pair？
Q3.  存在与 (A, B) 完全断开的孤立 multi-N pair 吗？
     → wl056 数据给出 yes：(15, 48) ↔ (20, 36) 形成与 catalog 断开的 2-cycle
Q4.  partner graph 是否分层（按 (A, B) 的大小）？
     → wl056 数据：partner 反推偏向大 (A, B)，小 (A, B) 通常在 G_M 内孤立
```

---

## 3. 与文献的精确对接

### 3.1 椭圆曲线方程：完全同构

```text
d19 (MATH.md §8):     E_{A, B}: Y² = X(X + A²)(X + B²)
Ono 1996:             E_Q(M, N): y² = x(x + M)(x + N) [取 M=A², N=B²]
Halbeisen-Hungerbu.:  Γ_{a, b}: y² = x(x + a²)(x + b²) [a, b 任意，但本文要求 Pythagorean]

→ 三者是同一曲线（符号不同）。Ono 1996 提供 framework，H-H 2021 在 (a, b)
  Pythagorean 的子族上做 torsion 升级分析。
```

### 3.2 Torsion 群

```text
E_{A, B} torsion 一般 ⊇ Z/2Z × Z/4Z       （docs/MATH.md §8.3 已证）

H-H 2021 Proposition 1 / 2024 Proposition 1:
  当 A = a², B = b² 且 (a, b) Pythagorean (a² + b² = □) 时:
    Γ_{a², b²} torsion = Z/2Z × Z/8Z      （多一个 8-阶点）

  当 A = aʰ, B = bʰ 且 (a, b) Pythagorean, h ≠ 2:
    Γ_{aʰ, bʰ} torsion = Z/2Z × Z/4Z      （与一般情形相同）
```

**对 d19 的意义**: 我们多数样本 (A, B) **不**满足 A = a², B = b² 且 (a, b) Pythagorean，
所以 torsion 是 Z/2Z × Z/4Z。但如果某些 multi-N pair 恰好满足该条件，那 H-H 2021
Theorem 2 给出额外的 sieve（用 Schroeter 几何）。

### 3.3 P_N ∈ 2E(ℚ)：Ono 1996 Prop 1

```text
对 concordant N 点 P_N = (N², N · √(N²+A²) · √(N²+B²))，
三个 x-coordinate factor (N², N²+A², N²+B²) 全部是平方
⇒ 存在 Q_N ∈ E(ℚ) s.t. 2 Q_N = P_N
```

这是 d19 与 Ono 框架对接的最关键结果。它意味着：

```text
multi-N pair (A, B) k=n
⇔ E_{A, B} 上有 n 个 square-x 点 P_{N_1}, ..., P_{N_n}
⇔ E_{A, B} 上有 n 个 half-points Q_{N_1}, ..., Q_{N_n}（在 E(ℚ)/2-torsion 里独立）

⇒ rank(E_{A, B}) ≥ ? 关于 n 的下界（具体多少需要 Mordell-Weil 分析）
```

KSS 2019 §6.3：rank=2 例子里每个 homogeneous space 通常只给一个 generator；
multi-N pair k=3 对应"多个不同 homogeneous spaces"。

### 3.4 与 Halbeisen-Hungerbühler 的 "pythapotent" 关系

```text
Definition (H-H 2021):
  (a, b) Pythagorean ∧ ∃ (k, l) Pythagorean s.t. (ak, bl) Pythagorean
  ⇔ double-pythapotent pair
  ⇔ Γ_{a, b} has positive rank

Definition (d19):
  (A, B) ∧ ∃ N s.t. N² + A² = □ ∧ N² + B² = □
  ⇔ A, B 有公共 Pythagorean 邻居
  ⇔ E_{A, B} 有非平凡 square-x 有理点
```

两者**不同**：
- H-H 要求 (a, b) 自身 Pythagorean，关心一般 rational point
- d19 不要求 (A, B) Pythagorean，关心 square-x rational point

但**关联**：

```text
若 (A, B) multi-N pair，则 E_{A, B} 必有非平凡有理点（Ono Prop 1 / KSS）
⇒ rank(E_{A, B}) ≥ 1
⇒ 在 H-H 语义下（如果 A² + B² = □）：(A, B) 是 double-pythapotent
   (但 H-H 反向：rank ≥ 1 ⇏ multi-N 必然 ≥ 2)
```

也即 **multi-N ⊊ "正秩"**，正秩是 multi-N 的必要不充分条件。

### 3.5 与 Bremner-Ulas 2016 "rational distance" 的关系

```text
B-U 2016: 5 vertices in ℚ² with pairwise rational distances
       ⇔ K_5 嵌入 "rational distance graph G_d(ℚ²)"

d19 / Harborth: 4-chain (cycle C_4) 嵌入 G_d(ℚ²) 满足额外约束（边在 unit square）
d19 / multi-N: K_{2, n} 嵌入 G_P (Pythagorean graph on ℤ_{>0})
```

注意 G_P 跟 G_d(ℚ²) 不是同一个图，但关联紧密（Pythagorean pair 是平面 ℚ²
上有理距离的整数案例）。Bremner-Ulas 的 5-vertex 工具栈对 d19 的 K_{2, n}
分析部分适用。

---

## 4. 新观察 vs 已知结果（贡献边界）

| 内容 | 状态 | 来源 |
|---|---|---|
| E_{A, B} 的 Weierstrass 化 | 已知 | Ono 1996 / KSS / H-H |
| Torsion = Z/2Z × Z/4Z (一般情形) | 已知 | Kubert / Mazur |
| P_N ∈ 2E(ℚ) (square-x ⇒ doubling) | 已知 | Ono 1996 Prop 1 |
| Rank > 0 ⇒ infinitely many primitive solutions | 已知 | Ono 1996 |
| (A, B) k=n ⇒ rank ≥ ? (下界) | 部分已知 | KSS 2019 §6.3 (rank=2 例子) |
| **partner identity（K_{2, 2} 嵌入对称性）** | **d19 自证** | wl054 |
| **K_n 等价定理 (K_n shared-partner ≡ k=n multi-N)** | **d19 自证** | wl055 |
| **partner graph G_M 连通分量结构** | **d19 部分实证** | wl056 |
| **(15, 48) ↔ (20, 36) 类孤立 cycle 的存在性** | **d19 自证** | wl056 |
| reduce 不保 multi-N（gcd 归约不保 square-x） | 已知 | MATH.md §8.6 / Ono Prop |

### 关于 partner identity 的原创性

严格地说，partner identity 是 Ono framework 内的**自然推论**（K_{2, 2} 嵌入
对称性 ⇒ 4 个 Pythagorean 边互相蕴含）。它不算独立定理，但 d19 wl054 是
**首次把它用作搜索加速器**（从 catalog 反推非互素 multi-N）。

### 关于 K_n 等价定理

同样是 partner identity 的直接推论。wl055 的贡献是**把它写清楚**，并指出
"K_n shared-partner enumeration" 等价于 "k=n multi-N pair 枚举"，从而把图论
问题降级为 1 维问题。

---

## 5. 反例搜索的代数翻译

### 5.1 Harborth 4-chain 反例的 multi-N 描述

```text
4-chain 反例 (a, b, c, d) 满足:
  a² + b² = □    (Pythagorean pair (a, b))
  b² + c² = □    (Pythagorean pair (b, c))
  c² + d² = □    (Pythagorean pair (c, d))
  d² + a² = □    (Pythagorean pair (d, a))
  a + c = b + d  (closure)

把 A := b, B := d, N₁ := a, N₂ := c：
  N₁² + A² = a² + b² = □
  N₁² + B² = a² + d² = □
  N₂² + A² = c² + b² = □
  N₂² + B² = c² + d² = □
  N₁ + N₂ = A + B   ← closure

⇒ 反例 ⇔ ∃ (A, B) k≥2 multi-N pair, ∃ N₁, N₂ ∈ concordant_N(A, B) with N₁+N₂=A+B
```

### 5.2 当前数据的反例排除范围

```text
max_hyp=100000 全 catalog（互素 + partner 反推非互素）:
  multi-N pair k≥2:  10,333 互素 + 10,533 partner 反推
  closure pair (N₁+N₂=A+B):  0
  
真实非互素 multi-N pair (wl056 直接扫描):
  M=2000 范围内  1,802 个 (partner 反推只覆盖 6.1%)
  closure pair:  0
```

**结论**：在已扫描范围内，**全部 multi-N pair 都不满足 closure** ⇒
不存在 Harborth 反例。但这是在有限范围内，不是证明。

### 5.3 K_n 高阶与反例的关系

```text
反例需要 (A, B) 至少 k=2 + closure (N₁+N₂=A+B)
⇒ K_n (n≥2) 中只有 n=2 必须，K_n n≥3 不增加新约束（任意两个 N 都可以试 closure）

但 K_n 高阶给我们更多 (N_i, N_j) 对去 test closure：
  k=2: 1 对 (N₁, N₂) 检查 N₁+N₂=A+B
  k=3: 3 对 (N_i, N_j) 检查
  k=4: 6 对
  ...
  k=8: 28 对

⇒ K_n 高阶样本的 closure 检查更可能命中
⇒ wl055 发现的 K_8 (55440, 445536) 和 (58800, 98280) 是值得特别审视的
   注：两者都已 K_n 框架内验证 closure 失败
```

### 5.4 已知 K_8 实例的 closure 状况

```text
K_8  (55440, 445536)  A+B = 500976
     N=[7552, 27027, 35700, 59670, 93177, 413952, 608580, 913920]
     C(8,2) = 28 pairs of (N_i, N_j), 检查 N_i + N_j = 500976:
     - 没有一对命中。完全没有 closure。

K_8  (58800, 98280)  A+B = 157080
     N=[7875, 25792, 28665, 73710, 78400, 179046, 201600, 733824]
     同样 28 pairs, 检查命中 157080:
     - 没有一对命中。完全没有 closure。
```

⇒ K_8 顶端样本也不给反例。closure 条件**结构上**与 multi-N 条件**正交**。

---

## 6. 未解决的理论问题

1. **closure 条件的代数障碍是什么？**
   - 经验上 max_hyp=100000 全部 0 closure pair
   - 是否可证明 closure ⇔ E_{A, B} 上的某个 Mordell-Weil 偏差消失？
   - 是否对应某种 Brauer-Manin 障碍？
   - 见 [`THEORY_DIRECTIONS_ADVANCED.md`](./THEORY_DIRECTIONS_ADVANCED.md) 方向七、八

2. **partner graph G_M 的全局结构**
   - 连通分量数？
   - 直径？
   - "孤立 cycle" (如 (15,48)↔(20,36)) 的密度？
   - 是否所有 multi-N pair 都能从某个"中心" (A, B) 通过有限 BFS 到达？

3. **K_n 与 rank 的精确关系**
   - K_n 实例的 ellrank 是否严格 ≥ ⌈n/2⌉？
   - 实测 (153, 560) k=3 rank=3
   - K_8 实例需要跑 ellrank 验证

4. **non-coprime 在椭圆曲线视角下的对应**
   - 我们 wl056 发现 gcd>1 的 (A, B) multi-N 大量存在
   - 在 Ono 框架下 E_{A, B} 与 E_{A/g, B/g} 同构（gcd=g）
   - 但 concordant N 不保持（reduce 不保 multi-N）
   - 这是个有趣的 anomaly，可能反映 Mordell-Weil 结构的某种 scale 依赖

---

## 7. 文献清单

直接相关：

- **Ono 1996** *Euler's concordant forms*. Acta Arithmetica 78(2), 101-123.
  → `docs/literature/notes/ono-1996-concordant.md`
- **Knaf, Selder, Spindler 2019** *An Algorithm to Find Rational Points on Elliptic Curves Related to the Concordant Form Problem*. arXiv:1907.02148.
  → `docs/literature/notes/knaf-selder-spindler.md`
- **Halbeisen, Hungerbühler 2021** *Pairing Pythagorean Pairs*. arXiv:2101.08163.
  → `docs/literature/notes/halbeisen-hungerbuhler-2021.md`
- **Halbeisen, Hungerbühler, Shamsi Zargar 2024** *Pairing Powers of Pythagorean Pairs*. arXiv:2405.12989.
  → `docs/literature/notes/halbeisen-hungerbuhler-voznyy-2024.md`

间接相关：

- **Bremner-Ulas 2016** *Points at rational distances from the vertices of certain geometric objects*. J. Number Theory 158, 104-133.
- **Zargar 2020** *On the rank of elliptic curves arising from Pythagorean quadruplets*. Kodai Math. J. 43(1), 129-142.
- **Bremner-Guy 1989** *The delta-lambda configurations in tiling the square*. J. Number Theory 32(3), 263-280.

---

## 8. 下一步路径

| 优先 | 任务 | 类型 |
|---|---|---|
| ⭐⭐⭐ | K_8 / K_7 实例的 ellrank + F2-rank 审计 (wl055 钩子) | 实证 |
| ⭐⭐ | 在 H-H 2024 Corollary 7/8 框架下，找我们 catalog 中形如 (aʰ, bʰ) 的 multi-N 子集 | 实证 |
| ⭐⭐ | partner graph G_M 全连通分量统计（多大的 max component？） | 实证 + 算法 |
| ⭐⭐ | M=10000 直接非互素扫描（wl056 钩子）| 实证 |
| ⭐ | (15, 48) ↔ (20, 36) 这类孤立 cycle 的代数解释（为什么 catalog 不能到达？）| 理论 |
| ⭐ | closure 条件的局部障碍（mod p 是否就排除？）| 理论 |
| ⭐ | Mordell-Weil sieve on K_8 实例（KSS §6.3 风格分析）| 理论 + 工具 |
