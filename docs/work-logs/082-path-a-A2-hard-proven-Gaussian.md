# wl082 — Conjecture A2-hard (d_2=d_3=1) 用 Gaussian integers 严格证明

> ⚠️ **后续修正 (wl084)**: 本 wl 论证有 **bug**. Gaussian uniqueness 假设
> 仅对 `c` prime/prime-power 成立; 对 `c` composite (多 prime ≡ 1 mod 4 因子)
> 失效. k=4 实证存在 counterexample (`(A,B,N) = (426496, 482625, 352800)`,
> `c = 1073 = 29·37`). 论证 invalid. 详见
> `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md`.


承接 wl081 (A2 收窄). 本 wl 把 A2 进一步分成 "hard" 与 "easy"  子情形, 
**严格证明 hard case 不可能**, 把 A2 的 algebraic gap 缩到 "easy" 案.

## 一、Pythagorean parameterization 复述

对 concordant `(A, B, N)`:

```
r_2 = √(N² + A²),  r_3 = √(N² + B²)

由 (r_2+N)(r_2-N) = A², sf(r_2+N) = sf(r_2-N) =: d_2 (两 squarefree, 乘积 □).
同理 sf(r_3±N) = d_3.

⟹ r_2 + N = s² d_2,  r_2 - N = u² d_2,  A = s u d_2,  2N = (s²-u²) d_2
   r_3 + N = p² d_3,  r_3 - N = q² d_3,  B = p q d_3,  2N = (p²-q²) d_3
```

`s, u, p, q ∈ ℤ_{>0}`, `gcd(s,u)=1`, `gcd(p,q)=1`, opposite parity for each pair.

## 二、d_2 = d_3 ⟹ d_2 = d_3 = 1 (algebraic)

```
A = s u d_2,  B = p q d_3.
若 d_2 = d_3 = d ≥ 2,  则 d | A 且 d | B  ⟹  d | gcd(A, B).
但 (A, B) reduced coprime  ⟹  gcd(A, B) = 1  ⟹  d ≤ 1.
∴ d_2 = d_3 = 1.
```

实证: 1879 pair / 3758 chosen N 中 d_2=d_3 案恰 59/3758 (1.57%), 全部 (1,1).

## 三、A2 在 d_2 = d_3 = 1 案的简化

```
A2 ⟺ (r_2+r_3)(r_2+N) ∉ □
   ⟺ d_2 · sf(r_2+r_3) ≠ 1 mod sq
   
r_2 + r_3 = u² d_2 + p² d_3 = u² + p²  (当 d_2 = d_3 = 1)

⟹ (r_2+r_3)(r_2+N) = (u²+p²) · s² = s² (u²+p²)
   sf = sf(u²+p²) · 1 = sf(u²+p²).

A2 ⟺ u² + p² ∉ □.
```

## 四、严格证明: d_2 = d_3 = 1 ⟹ u² + p² ∉ □

**Claim**: 对 valid k=2 multi-N pair `(A, B, N)` with `d_2 = d_3 = 1`,
`u² + p² ∉ □`.

**证明** (反证 + Gaussian integers):

假设 `u² + p² = c²` (整数 `c > 0`). 已知:

```
s² = u² + 2N
q² = p² - 2N
```

把 `2N = s² - u²` 代入第二个: `q² = p² - s² + u² = (u² + p²) - s² = c² - s²`.

⟹ `s² + q² = c²`. ☆

所以 **`(u, p)` 与 `(s, q)` 都是 `c²` 的两平方和整数表示**。

由 Gaussian integer 因子分解, `c²` 在 `ℤ[i]` 中的所有 (有序) 两平方和表示是:
`c² = (u + ip)(u - ip) = (s + iq)(s - iq)`. 在 `ℤ[i]` 中 `c² = c · c` 的因子
分解给出有限多 `α, ᾱ` 配对, 其中 `α · ᾱ = c²` 和 `α = a + ib`, `a² + b² = c²`.

对 primitive Pythagorean `(u, p, c)` (`gcd(u, p) = 1`), `c² ∈ ℤ[i]` 的两平方
和分解 essentially 唯一 (up to unit `{1, -1, i, -i}` 与 conjugation):

```
c² = (u + ip)(u - ip) (= u² + p² 主分解)
```

⟹ 所有整数 `(s, q)` 与 `s² + q² = c²` 必 `(s + iq) = ε · (u + ip)` 或
`ε · (u - ip)` 或 `ε · (p + iu)` 或 `ε · (p - iu)`, `ε ∈ {1, -1, i, -i}`.

⟹ `(s, q) ∈ {(u, p), (-u, -p), (p, -u), (-p, u), (-u, p), (u, -p), (-p, -u), (p, u)}`.

`s, q > 0` (Pythagorean parameter) ⟹ `(s, q) ∈ {(u, p), (p, u)}`.

**Case 1**: `(s, q) = (u, p)` ⟹ `s = u` ⟹ `2N = s² - u² = 0` ⟹ `N = 0`. ⨯ (need `N > 0`)

**Case 2**: `(s, q) = (p, u)` ⟹ `s = p`, `q = u`. 
   `A = s u d_2 = p u`,  `B = p q d_3 = p u`. 
   ⟹ `A = B`. ⨯ (need `A ≠ B` for non-degenerate Harborth fixed point)

**Non-primitive case** `gcd(u, p) = g > 1`: 记 `u = g u'`, `p = g p'`, 
`gcd(u', p') = 1`, `u'² + p'² = (c/g)² =: c'²`. 则 `s² + q² = g² c'²`. 
注意 `g² c'² = (g u')² + (g p')² = (g c')²`. 由 `g c'` 的整数两平方和表示
理论, `s² + q² = (g c')²` 的所有表示形如 `s + iq = ε · (g c' ξ)` 其中 `ξ`
枚举 `g²` 在 `ℤ[i]` 的两平方和表示. 因 `c' = √(u'² + p'²)` 已 fixed, 
表示仍然回归 Case 1 / Case 2 (degeneracy) 或 引入 gcd-factor 不一致.

更严格: 由 `gcd(u, p)` 与 `(s, q)` 互动, 若 `g = gcd(u, p) > 1` 则
`g | A` 且 `g | B` (从 `A = us d_2`, `s` 与 `u` coprime ⟹ `g | u | A`; 
`B = p q d_3`, `g | p | B`). 矛盾于 `gcd(A, B) = 1`. ⨯

∴ **`d_2 = d_3 = 1` 且 valid k=2 multi-N pair 在 algebraic 上不可能让 `u² + p² ∈ □`**.

∴ **A2-hard case 严格证毕**. ∎

## 五、剩余 gap: A2-easy (d_2 ≠ d_3)

```
A2-easy ⟺ (u d_2)² + (d_2 d_3) p² ∉ □
       ⟺ 不存在整数 z 让 z² - (u d_2)² = (d_2 d_3) p²
       ⟺ 不存在整数 z 让 (z - u d_2)(z + u d_2) = (d_2 d_3) p²
```

设 `m = d_2 d_3` (squarefree, 因 d_2, d_3 不同 squarefree ⟹ m squarefree 或
有 nontrivial gcd). 实际上 `gcd(d_2, d_3) | gcd(A, B) = 1` ⟹ `d_2, d_3` 互素
⟹ `m = d_2 d_3` squarefree.

⟹ A2-easy 即 `(u d_2)² + m p² ≠ z² in ℤ`.

等价于 imaginary quadratic field `K = ℚ(√(-m))`: A2-easy ⟺ `u d_2 + p √(-m)`
不是 `K` 中某 element 的范的平方根 (即范不是完全平方).

## 六、A2-easy 的实证 + 攻击方向

实证 (max_hyp=1M, 3699 chosen N with d_2 ≠ d_3): 0/3699 violations.

可能的 algebraic 攻击:

1. **2-adic** / **3-adic**: 看 `(u d_2)² + m p² mod 4` 或 `mod 9` 的 QR
   限制.
2. **Hilbert symbol**: A2-easy ⟺ Hilbert symbol `(-(m p²), u² d_2²)_p` 在
   某 p 上 = -1.
3. **Class number argument**: 用 `K = ℚ(√(-m))` 的 class number, 若 1 则
   norm form principal ideal 唯一表示 → 排除非平凡解.

## 七、当前 A1 严格证明状态

```
Step (a) Q ≢ T_A, T_B mod 2 E   :  ✅ 严格 (wl081)
Step (b) Q ∉ 2 E(ℚ)              :  
   - hard case (d_2=d_3=1)        :  ✅ 严格 (本 wl, Gaussian integers)
   - easy case (d_2≠d_3)          :  ⏳ 实证 universal, algebraic 在 imag.
                                       quadratic field 的 norm form 上.
Step Q_{N_1} ≢ Q_{N_2} mod E[2]  :  ✅ (wl076 Step 2 用 N_1 ≠ N_2)
F₂-rank ⟹ rank ≥ 2              :  ✅ (基于 dim image α = rank + 1)
```

A2-easy 是最后 algebraic gap. 如果攻下, **A1 完全严格证完**.

## 八、文件 / 引用

```
docs/work-logs/076-conjecture-a1-proof-sketch.md  原 sketch
docs/work-logs/081-path-a-pickup-algebraic-step-a-strict.md  step a + A2 收窄
scripts/audit_halfpoint_factorization.py          step (b) gap 实证
scripts/analyze_a2_pythagorean.py                 本 wl: Pythagorean 参数
```

## 九、状态

- ✅ d_2 = d_3 ⟹ d_2 = d_3 = 1 (algebraic, primitivity)
- ✅ A2 在 d_2 = d_3 = 1 案 ⟺ `u² + p² ∉ □`
- ✅ **A2-hard (`u² + p² ∉ □`) 严格证明** — Gaussian integer 两平方和 唯一
  分解 ⟹ Case 1 (N=0) 或 Case 2 (A=B)
- ⏳ A2-easy (d_2 ≠ d_3) — norm form in `ℚ(√(-d_2 d_3))`, 实证 universal
