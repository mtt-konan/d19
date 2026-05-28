# wl081 — Path A 接续: algebraic step (a) 严格化 + (b) gap 收窄

承接 wl076 (Conjecture A1 sketch + F₂-rank 实证 1879/1879). 本 wl 重审 sketch, 
找出 **algebraic gap**, 严格证明其中一部分 (step a), 并把剩余 gap (step b)
收窄成一个干净的 conjecture A2.

## 一、wl076 sketch 的真实 gap

wl076 §四 Step 4 写:

> Q_{N_i} ∉ E[2] + δ injective ⟹ δ(Q_{N_i}) ∉ E[2] image ⟹ v_i ≠ 0

**这一步逻辑跳了**。"`Q_{N_i} ∉ E[2]` (作为点)" ≠ "`Q_{N_i} mod 2 E(ℚ) ∉ E[2] mod 2 E(ℚ)`".

正确路径需分两半:

```
(a) δ(Q_{N_i}) ≠ δ(T_A), δ(T_B) in (ℚ*/ℚ*²)²
(b) δ(Q_{N_i}) ≠ 0 即 Q_{N_i} ∉ 2 E(ℚ)
```

(a) ⟺ Q_{N_i} ≢ T_A, T_B  mod 2 E(ℚ)
(b) ⟺ Q_{N_i} ∉ 2 E(ℚ)

⟹ Q_{N_i} mod 2 E(ℚ) ∉ {0, T_A mod, T_B mod} = α(E[2](ℚ)).

加上 F₂-rank 验证 `δ(Q_{N_1}) ≠ δ(Q_{N_2}) mod δ(E[2])` ⟹ rank ≥ 2.

## 二、Half-point X 坐标的代数因式分解

`enumerate_half_points_for_concordant_N` 对每个 `(s_1, s_2, s_3) ∈ {±1}³` 算:

```
x = N² + s_1 s_2 N r_2 + s_1 s_3 N r_3 + s_2 s_3 r_2 r_3
y = (s_1 r_1 + s_2 r_2)(s_1 r_1 + s_3 r_3)(s_2 r_2 + s_3 r_3)
```

其中 `r_2 = √(N²+A²)`, `r_3 = √(N²+B²)`. 当 `s_2 s_3 = +1` 时:

| 选 (s_1, s_2, s_3) | x_Q 因式分解 | x_Q 符号 |
|---|---|---|
| `(+,+,+)` | `(N + r_2)(N + r_3)` | 正 (`≥ N²`) |
| `(+,-,-)` | `(r_2 - N)(r_3 - N)` | 正 (两 r > N) |
| `(-,+,-)` | `(N - r_2)(N + r_3) = -(r_2-N)(N+r_3)` | 负 |
| `(-,-,+)` | `(N + r_2)(N - r_3) = -(N+r_2)(r_3-N)` | 负 |

且对 `s_2 s_3 = +1` 中两 positive choices:

```
(+,+,+) :  x_Q = (N+r_2)(N+r_3)
           x_Q + A² = (N+r_2)(r_2+r_3)
           x_Q + B² = (N+r_3)(r_2+r_3)

(+,-,-) :  x_Q = (r_2-N)(r_3-N)
           x_Q + A² = (r_2-N)(r_2+r_3)
           x_Q + B² = (r_3-N)(r_2+r_3)
```

(用恒等式 `(r_2-N)(r_2+N) = A²`，`(r_3-N)(r_3+N) = B²` 推得。)

## 三、`_pick_positive_halfpoint` 的实际选择

代码逻辑: enumerate 后 sort by `(|x|, |y|, x, y)` ascending, 选第一个 `sig[0] > 0`. 

⟹ 因 `(r_2-N)(r_3-N) < (N+r_2)(N+r_3)`, **chosen half-point 永远是
`(s_1, s_2, s_3) = (+,-,-)` sign**.

实证 (max_hyp=1M, 1879 pair, `scripts/audit_halfpoint_factorization.py`):

```
chosen half-point sign distribution:
   (+--): 3758/3758 (100.00%)   ← 全部！
```

⟹ chosen `Q_{N_i}`:
```
x_Q = (r_2 - N)(r_3 - N)       > 0
x_Q + A² = (r_2 - N)(r_2 + r_3) > 0
x_Q + B² = (r_3 - N)(r_2 + r_3) > 0
```

## 四、Algebraic step (a) 严格证明

**Claim**: `δ(Q_{N_i}) ≠ δ(T_A)` and `δ(Q_{N_i}) ≠ δ(T_B)` in `(ℚ*/ℚ*²)²`.

**证明**: 取 `δ_1` (第一分量, in `ℚ*/ℚ*²`):

```
δ_1(Q_{N_i}) = sf(x_Q) = sf((r_2 - N)(r_3 - N)) ∈ ℤ_{>0}/ℚ*²
δ_1(T_A) = sf(-A²) = -1
δ_1(T_B) = sf(-B²) = -1
```

`(ℚ*/ℚ*²)` 中, 正数 coset 与 `-1` coset 不同 (因 `-1` 不是 `ℚ` 上的平方).

⟹ `δ_1(Q_{N_i}) ≠ δ_1(T_A)` and `δ_1(Q_{N_i}) ≠ δ_1(T_B)`
⟹ `δ(Q_{N_i}) ≠ δ(T_A), δ(T_B)` (第一分量已不同). ∎

**实证验证 (max_hyp=1M)**:
```
Q1_sig[0] > 0:           1879/1879 (100.00%)
Q2_sig[0] > 0:           1879/1879 (100.00%)
```

★ **Step (a) algebraic 严格证明完成**。

## 五、Algebraic step (b): 收窄成 Conjecture A2

**剩余 gap**: 证 `δ(Q_{N_i}) ≠ 0` 即 `Q_{N_i} ∉ 2 E(ℚ)`.

`δ(Q_{N_i}) = 0` ⟺ `sf(x_Q) = 1` AND `sf(x_Q + A²) = 1`
            ⟺ `x_Q ∈ ℚ*²` AND `x_Q + A² ∈ ℚ*²`
            ⟺ `(r_2 - N)(r_3 - N) ∈ □` AND `(r_2 - N)(r_2 + r_3) ∈ □`

**实证 (max_hyp=1M, 3758 chosen half-points)**:

```
x_Q ∈ □:        59/3758  (1.57%)   ← 有 59 个 (r_2-N)(r_3-N) ∈ □
x_Q + A² ∈ □:   0/3758   (0.00%)   ← 没有一个 (r_2-N)(r_2+r_3) ∈ □
δ(Q) = 0:       0/3758   (0.00%)   ← (b) gap 实证 universal
```

利用 `(r_2 - N) = A²/(r_2 + N)`:
```
x_Q + A² = (r_2 - N)(r_2 + r_3) = A² · (r_2 + r_3) / (r_2 + N)
```
⟹ `x_Q + A² ∈ □  ⟺  (r_2 + r_3)(r_2 + N) ∈ □` (mod squares).

**Conjecture A2 (新)**:

> 对 reduced coprime safe-pass 的 multi-N pair `(A, B)` 与任意 concordant `N`,
> `(r_2 + r_3)(r_2 + N) ∉ ℚ*²`，其中 `r_2 = √(N²+A²)`, `r_3 = √(N²+B²)`.

实证 (max_hyp=1M): 0/3758 violations.

**A1 ⟸ Conjecture A2** 严格代数化：

```
Conjecture A2 (任意 N) ⟹ Q_{N_i} ∉ 2 E(ℚ)
              ⟹ δ(Q_{N_i}) ≠ 0
              ⟹ δ(Q_{N_i}) ∉ δ(E[2](ℚ)) = {0, δ(T_A)=δ(T_B)}  (by step a + step b)
              ⟹ v_i ≠ 0 in F₂^rank
            ＋ N_1 ≠ N_2 ⟹ δ(Q_{N_1}) ≠ δ(Q_{N_2})  (by Step 2 of wl076)
              ⟹ v_1 ≠ v_2
              ⟹ {v_1, v_2} F₂-独立
              ⟹ rank ≥ 2  ∎
```

## 六、Conjecture A2 的初步分析

`(r_2 + r_3)(r_2 + N) ∈ □` 是个数论条件. 几个 reformulation:

```
(r_2 + r_3)(r_2 + N) = r_2² + r_2 N + r_2 r_3 + N r_3
                     = (N² + A²) + r_2(N + r_3) + N r_3
```

或:
```
(r_2 + r_3)(r_2 + N)  ≡  (r_2 + r_3) · (r_2 + N)  in ℚ*/ℚ*²
                      ≡  sf(r_2 + r_3) · sf(r_2 + N)
```

⟹ `Conjecture A2 ⟺ sf(r_2 + r_3) ≠ sf(r_2 + N)` in `ℚ*/ℚ*²`.

具体例子 `(A,B,N) = (25, 91, 60)`:
- `r_2 = 65`, `r_3 = 109`
- `r_2 + N = 125 = 5³`, `sf = 5`
- `r_2 + r_3 = 174 = 2·3·29`, `sf = 174`
- `5 ≠ 174 in ℚ*/ℚ*²` ✓

`(A,B,N) = (264, 420, 77)`:
- `r_2 = 275`, `r_3 = 427`
- `r_2 + N = 352 = 2⁵·11`, `sf = 22`
- `r_2 + r_3 = 702 = 2·3³·13`, `sf = 78`
- `22 ≠ 78 in ℚ*/ℚ*²` ✓

## 七、对比 wl076 论证现状

| Step | wl076 sketch | 本 wl 现状 |
|------|---|---|
| Q_{N_i} ∉ E[2] (as point) | ✅ sign argument | ✅ (trivial) |
| Q_{N_i} ≢ T_A, T_B mod 2 E (step a) | ⚠️ logic gap | ✅ **本 wl 严格** |
| Q_{N_i} ∉ 2 E(ℚ) (step b) | ⚠️ via F₂-rank 实证 | ⏳ 收窄成 Conjecture A2, 实证 universal max_hyp=1M |
| Q_{N_1} ≢ Q_{N_2} mod E[2] | ✅ (N_1 ≠ N_2) | ✅ |
| {v_1, v_2} F₂-独立 | ⚠️ via 实证 | ✅ (assuming A2) |
| rank ≥ 2 | ✅ (基于上述) | ✅ (assuming A2) |

**新 cleaner formulation**: A1 ⟸ Conjecture A2 (单一干净的代数条件).

## 八、下一步攻 Conjecture A2

Conjecture A2 是个**纯数论命题**, 与 elliptic curve 解耦. 攻击方向:

1. **2-adic / 3-adic 分析**: `(r_2+r_3)(r_2+N) mod p^k` 的 quadratic-residue 限制.
2. **直接 ad hoc 推**: 用 `r_2² = N² + A²`, `r_3² = N² + B²` 写出 `(r_2+r_3)(r_2+N)` 的 explicit form, 看是否能用恒等式排除 □.
3. **Hilbert symbol**: A2 ⟺ Hilbert symbol `(r_2+r_3, r_2+N)_p = 1` 对**某个** p (即至少一个 prime 上 product 非平方).
4. **descent on Pythagorean side**: 已知 r_2² = N²+A² 和 r_3² = N²+B² 各自标准 Pythagorean 参数化. 把 (r_2+r_3)(r_2+N) 用参数表达.

最 promising 看 (2): 直接展开看看.

## 九、文件 / 引用

```
docs/work-logs/076-conjecture-a1-proof-sketch.md  原 sketch (含 logic gap)
docs/MATH.md §8.3                                  E_{A,B} torsion = Z/2×Z/4
src/rational_distance/concordant/half_points.py    enumerate + signature
scripts/analyze_k2_f2_rank.py                      F₂-rank 实证 (wl076)
scripts/audit_halfpoint_factorization.py           本 wl: sign + (b) gap audit
results/k2_f2_rank_max1m.jsonl                     1879 pair audit dump
```

复现命令:
```bash
uv run python scripts/audit_halfpoint_factorization.py
```

## 十、状态

- ✅ wl076 sketch logic gap 找出
- ✅ Half-point chosen sign universal = (+,-,-)，因式分解 algebraic 干净
- ✅ Step (a) (`Q ≢ T_A, T_B mod 2 E`) 严格证明 — sign argument
- ✅ Step (b) gap 收窄为 Conjecture A2: `(r_2+r_3)(r_2+N) ∉ ℚ*²`
- ✅ Conjecture A2 实证 1879/1879 universal at max_hyp=1M
- ⏳ Conjecture A2 algebraic 证明 — 下一步主攻
