# Halbeisen, Hungerbühler & Zargar 2024 — "Pairing Powers of Pythagorean Pairs"

**全名**: Halbeisen, L., Hungerbühler, N. & Shamsi Zargar, A. (2024). *Pairing Powers of Pythagorean Pairs*. arXiv:2405.12989.
**作者机构**: ETH Zürich + University of Mohaghegh Ardabili
**优先级**：⭐⭐ — H-H 2021 的推广到任意 degree h，给出参数化判据
**状态**：PDF 已获取、§1-2 精读完成
**本地 PDF**：`../pdfs/halbeisen-hungerbuhler-voznyy-2024-pairing-powers.pdf`
**抽取文本**：`../pdfs/halbeisen-hungerbuhler-voznyy-2024-pairing-powers.txt`

---

## 一句话总结

把 H-H 2021 的 double-pythapotent (h=1) 和 quadratic-pythapotent (h=2) 推广到任意
degree h ≥ 3，证明 (a, b) 是 pythapotent of degree h 当且仅当椭圆曲线
Γ_{aʰ, bʰ} 正秩。h=2 特殊给出 Z/2Z × Z/8Z torsion，其他 h 都是 Z/2Z × Z/4Z。

## 推广定义

```text
pythapotent pair of degree h:
  (a, b) Pythagorean,
  ∃ (k, l) Pythagorean (不互为倍数)
  s.t. (aʰ·k, bʰ·l) is Pythagorean
  即:  a²+b²=□, k²+l²=□, (aʰk)²+(bʰl)²=□
```

退化情形：
- h=1: double-pythapotent (H-H 2021)
- h=2: quadratic-pythapotent (H-H 2021)
- h=3: cubic pythapotent (本文新定义)
- h=4: quartic pythapotent
- ...

## 关键定理（论文 §2）

```text
Theorem 2:
  (a, b) is pythapotent of degree h  ⇔  Γ_{aʰ, bʰ} has positive rank over Q

Proposition 1 (torsion):
  Γ_{aʰ, bʰ}: y² = x³ + (a^(2h) + b^(2h)) x² + a^(2h) b^(2h) x
            = x(x + a^(2h))(x + b^(2h))

  torsion = Z/2Z × Z/4Z       for h ≠ 2
  torsion = Z/2Z × Z/8Z       for h = 2 only
```

**注意**：曲线 Γ_{aʰ, bʰ} = E_{aʰ, bʰ}（d19 语言），即把 d19 的 (A, B) 取为 (aʰ, bʰ)
其中 (a, b) Pythagorean。这是 d19 曲线族的**一个特殊子族**。

## 具体例子（论文 §1）

```text
Cubic pythapotent (h=3):
  (a, b) = (3, 4)        ← (3, 4) Pythagorean: 3² + 4² = 5²
  (k, l) = (8, 15)       ← (8, 15) Pythagorean: 8² + 15² = 17²
  (3³·8, 4³·15) = (216, 960)
  216² + 960² = 984²     ✓ Pythagorean

  Γ_{3⁴, 4⁴} = Γ_{81, 256} 的 rank = 1 ⇒ (3, 4) 同时是 quartic pythapotent

Quartic pythapotent (h=4):
  (a, b) = (3, 4),  (k, l) = (176, 57)
  (3⁴·176, 4⁴·57) = (14256, 14592)
  14256² + 14592² = 20400²   ✓ Pythagorean

  但 Γ_{3⁵, 4⁵} rank = 0 ⇒ (3, 4) 不是 quintic pythapotent
```

## 参数化判据（论文 Corollary 7, 8）

```text
Corollary 7:
  设 (a, b) = (m² − n², 2mn) Pythagorean。
  若 5m² − n² = □ 或 m² + 3mn + n² = □，则 (a, b) is double-pythapotent.

Corollary 8:
  设 (a, b) = (m² − n², 2mn) Pythagorean。
  若 (some condition on m, n) = □，则 (a, b) is quadratic-pythapotent.
```

这些 **giant sieve**：用 m, n 的代数条件直接判定，不需要 PARI ellrank。

## 与 d19 的关系

```text
Γ_{aʰ, bʰ} ≡ E_{aʰ, bʰ} (d19 语言)
            ≡ Ono framework E_Q(M, N) with M = a^(2h), N = b^(2h)
```

H-H-Z 2024 的特殊曲线族（要求 a, b 来自 Pythagorean pair）是 d19 曲线族 E_{A, B} 的
一个 measure-zero 子族（因为大多数 (A, B) 都不是 (aʰ, bʰ) 形式）。但当 d19 的样本
**恰好**满足 A = aʰ, B = bʰ 且 (a, b) Pythagorean 时，H-H-Z 的 sieving conditions
（Corollary 7/8）可以直接搬过来当快速判据。

## Action items

| 优先 | 任务 |
|---|---|
| ⭐⭐ | 在我们的 multi-N catalog 里搜索 (A, B) 形如 (aʰ, bʰ) 且 (a, b) Pythagorean 的子集，看 H-H-Z 的 corollary 7/8 是否能加速判定 multi-N |
| ⭐ | H-H-Z 2024 §3 的具体证明可能给出 pythapotent → multi-N 的连接 |
| ⭐ | 跟踪 Zargar 2020 (Kodai Math J) "On the rank of elliptic curves arising from Pythagorean quadruplets"，可能更直接对应 K_{2, n} 子图 |
