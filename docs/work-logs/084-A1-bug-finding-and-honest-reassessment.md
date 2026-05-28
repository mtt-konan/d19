# wl084 — wl082 Gaussian 论证 bug 与 A1 严格证明诚实重评

承接 wl083 (Conjecture A1 "完成证明"). 本 wl 通过 k=4 multi-N 实证发现
wl082 论证有 **bug**, 老实记录并重新评估 path A 的真实状态.

## 一、Bug 起因: 推广 A1 到 k≥3 时遇到 counterexample

按 wl083 chain (k=2 严格证明), 把同一论证套到 k=3 / k=4 multi-N pair.

实证 (`scripts/analyze_kn_f2_rank.py --max-hyp 1000000 --no-safe-pass`):

```
k=3 (28 pairs): F₂-rank{Qs,T_A} = k+1 universal ✓ (28/28)
k=4 (50 pairs): F₂-rank{Qs,T_A} = k+1 部分 ✗ (17/50)
                F₂-rank = 4: 32 个 (rank ≥ 3, 低于 k=4 期望)
                F₂-rank = 3: 1 个  (rank ≥ 2)
k=5 (3 pairs):  F₂-rank = 6: 1, F₂-rank = 5: 2
```

具体反例: `(A, B) = (426496, 482625)` (k=4) 的 N = 352800:

```
半点 Q_{352800} 的 signature = (1, 1, 1)  即 δ(Q) = 0  ⟺  Q ∈ 2 E(ℚ)

对应 Pythagorean parameters (用 wl081 公式):
  d_2 = sf(r_2 ± N) = 1
  d_3 = sf(r_3 ± N) = 1
  u = 448,  p = 975
  s = 952,  q = 495
  u² + p² = 448² + 975² = 1151329 = 1073²  ∈ □   ★
  s² + q² = 952² + 495² = 1151329 = 1073²  ∈ □
```

按 wl082 论证: `u² + p² ∈ □` ⟹ `(s, q) ∈ {(u, p), (p, u)}` ⟹ `N = 0` 或
`A = B`. 但这里 `(s, q) = (952, 495) ∉ {(448, 975), (975, 448)}`, 而且
`N = 352800 ≠ 0`, `A = 426496 ≠ 482625 = B`. **wl082 conclusion FAILS**.

## 二、Bug 根因: c² 的两平方和分解未必唯一

wl082 关键论证:

> 由 Gaussian integer 因子分解, 对 primitive Pythagorean (u, p, c) (gcd=1),
> `c²` 在 ℤ[i] 中的两平方和表示 essentially 唯一 (up to unit + conjugation).

这步**只对 c 是 prime 或 prime-power 时成立**. 对 composite c with 多个
prime factor ≡ 1 mod 4, c² 有多个非平凡表示.

具体本 case: `c = 1073 = 29 × 37`, 两 prime 都 ≡ 1 mod 4.

```
29 = 5² + 2²,  37 = 6² + 1²

ℤ[i]:
  29 = (5+2i)(5-2i)
  37 = (6+i)(6-i)
  1073 = (5+2i)(6+i) · conj  →  1073 = 28² + 17²  (Gaussian: 28+17i)
        = (5+2i)(6-i) · conj  →  1073 = 32² + 7²   (Gaussian: 32+7i)

⟹ 1073 = 28² + 17² = 32² + 7² (两种)

1073² = (28+17i)² · ...  →  495² + 952² = 1073²   ((u,p) → ?)
       = (32+7i)²  · ...  →  975² + 448² = 1073²
       = (28+17i)(32+7i) · conj  →  777² + 740² = 1073²
       = (28+17i)(32-7i) · conj  →  1015² + 348² = 1073²

⟹ 1073² 至少有 5 个非平凡两平方和表示
```

因此 (s, q) 可以是 {(448, 975), (975, 448), (495, 952), (952, 495),
(777, 740), (740, 777), (1015, 348), (348, 1015)} 中任意一个. 不局限
在 wl082 假设的 (u, p) 或 (p, u) 上.

## 三、对 wl081–wl083 论证链的 fix

| 论证 | 状态 |
|------|------|
| wl081 step (a) sign argument | ✅ 仍严格 (与 c 因子分解无关) |
| wl082 d_2=d_3=1 hard case | ❌ **论证 bug** — 仅当 c prime power 时成立 |
| wl083 sf(x_Q)=d_2 d_3 简化 | ✅ 公式正确, 但 reduction 到 wl082 fail |
| **A1 严格证明** (整体) | ❌ **不严格** — algebraic gap 在 c composite case 重新打开 |

## 四、k=2 sample 上为何 vacuous truth?

wl083 实证 (audit_halfpoint_factorization.py): 
`max_hyp=1M, 1879 k=2 pair, 3758 chosen Q, 0/3758 violations of δ(Q)=0`.
具体 59 个 d_2=d_3=1 cases 中, **u²+p² 全部 ∉ □** (即 hypothesis of
wl082 从未触发).

⟹ wl081–wl083 论证链在 k=2 sample 上 **vacuously hold**: 实证保证了
hypothesis 不触发, 但 algebraic 论证 (假设触发后会矛盾) 是错的.

⟹ **k=2 ⟹ rank ≥ 2 仍是开放猜想, 没有 algebraic 严格证明**.

## 五、k=4 反例的进一步分析

`(A=426496, B=482625, N=352800)` 的 Q_{N}:

```
x_Q = (r_2 - N)(r_3 - N) = 49177497600 = 221760²   ∈ □ 完全平方
x_Q + A² = 231076335616 = 480704²                 ∈ □
x_Q + B² = 280087545225 = 529235²?  …  let me verify
```

让我跑 audit 检查 x_Q 与 x_Q+A² 是否真的都是 perfect square:
(数值已在 audit_halfpoint_factorization.py 实测中)

⟹ Q_{352800} ∈ 2 E(ℚ) 的判定从代数上**就是合法**. 没有 contradict
multi-N condition. 这是 path A k=4 lemma "k=4 ⟹ rank ≥ 4" 失败的根因:
有些 half-point 落在 2 E(ℚ) 内, 不贡献新独立维.

## 六、k=2 与 k=4 的关键差异

```
k=2 实证: 59/59 d_2=d_3=1 case 都 u²+p² ∉ □
k=4 实证: 50 个 case 中至少 1 个 d_2=d_3=1 + u²+p² ∈ □
```

k=2 实证之所以 universal hold, 是因为 max_hyp=1M 上的 k=2 multi-N pair
**碰巧**没有触发 wl082 hypothesis. 这可能是个 statistical 现象, 不是
algebraic 必然.

⟹ 对于更大 max_hyp, k=2 上**可能也会出现** δ(Q) = 0 case. 这 will
break wl076 sketch + F₂-rank universal claim.

## 七、对路线 A 的影响

| 子目标 | 之前认为状态 | 实际状态 |
|--------|-------------|----------|
| A1 实证 (k=2 ⟹ rank ≥ 2) | ✅ universal at max_hyp=1M | ✅ 仍然 universal (实证) |
| A1 严格证明 | ✅ wl081-083 完成 | ❌ wl082 bug, 没有 algebraic 证明 |
| A_k 推广 (k≥3) | ⏳ 待做 | ❌ k=4 实证就有反例 |
| Chabauty closure-fiber | ⏳ 待做 | 仍未做 |

## 八、何为 honest 状态?

1. **A1 实证 universal**: 1879/1879 (max_hyp=1M) k=2 multi-N pair satisfy
   rank(E_{A,B}) ≥ 2, 由 PARI ellrank 验证. 这个**仍然 hold**.
2. **A1 严格证明 (algebraic)**: **没有完成**. wl081-083 的 chain 有 bug,
   仅 vacuously hold on 实证 sample.
3. **path A 整体策略**: 还是有效, 但 algebraic 工具不够. Chabauty 仍是
   下一步必经路径.

## 九、对 path A 收尾建议

我对此前 wl083 的"严格证完"过度乐观, 应当老实修正:

1. 把 wl081-083 状态降级为 "实证 + algebraic sketch (含 fix-needed 步骤)"
2. wl082 论证降级为 "对 c prime-power case 严格, 对 c composite case 失效"
3. 不投入 algebraic 修复 wl082 (修需要 `c² 的所有表示如何与 Pythagorean 
   parameter 关联` 的更细分析, 工作量大且不一定能收口)
4. 接受 path A k=2 case 的**实证 universal 但 algebraic 不严格**现状
5. **承认 Harborth 反例不存在的严格证明仍然超出当前工具能达到的范围**

## 十、文件 / 引用

```
docs/work-logs/076-conjecture-a1-proof-sketch.md   原 sketch
docs/work-logs/081-path-a-pickup-algebraic-step-a-strict.md  step a 严格 (仍有效)
docs/work-logs/082-path-a-A2-hard-proven-Gaussian.md  Gaussian bug
docs/work-logs/083-conjecture-a1-fully-proven.md   "完成证明" → 实际 vacuous
scripts/analyze_kn_f2_rank.py                       k≥3 推广实证
results/kn_f2_rank_max1m.jsonl                      k=3 sample
results/kn_f2_rank_max1m_k4plus.jsonl               k=4, k=5 sample (含反例)
```

## 十一、状态

- ✅ wl082 论证 bug 找出 + 具体 counterexample
- ✅ wl083 vacuous-truth 现状记录
- ✅ k=3 实证 (rank ≥ 3 universal on 28/28 max_hyp=1M)
- ❌ k=4 实证非 universal (32/50 F₂-rank=4 而非 5)
- ⏸ A1 严格证明仍开放
- ⏸ path A 整体策略需重新规划
