# wl267 — wl218 bridge projective residue boundary

日期：2026-06-22

## 1. 本轮目标

接 wl266。

现在 `E=0` 已归约到 z-lemma/centerline/Yang Ji。剩下的活分支是：

```text
E != 0,
centerline factor != 0,
k_x^2+1 square,
k_y^2+1 square.
```

普通话说：

```text
桥差分里那扇 E=0 的门已经知道通向中线。
现在要看如果不走这扇门，会不会被模素数直接卡住。
```

---

## 2. 为什么要用 projective residue

只枚举 affine `t,u mod p` 不够严谨，因为有理参数的分母可能被 `p`
整除。

所以这轮改成枚举：

```text
(t,u) in P^1(F_p) x P^1(F_p).
```

对两个 bridge 平方条件，用双齐次化后的分子：

```text
k_x^2+1 square  <=>  NX(t,u) square
k_y^2+1 square  <=>  NY(t,u) square
```

在有限域里计数。

普通话说：

```text
这次不是只看普通分数余数；
连“分母为 0 的方向”也一起看。
```

---

## 3. 新 helper

新增 dataclass：

```text
SumAbDualSlopeBridgeProjectiveResidueSummary
```

新增 helper：

```text
sum_ab_dual_slope_bridge_projective_residue_summary(p)
```

它记录：

```text
projective_class_count
both_bridge_square_classes
centerline_square_classes
noncenter_square_classes
noncenter_extra_factor_zero_classes
noncenter_extra_factor_nonzero_classes
noncenter_extra_factor_nonzero_examples
```

新增测试：

```text
test_sum_ab_dual_slope_bridge_residue_summary_routes_mod5_11_to_extra_factor
```

---

## 4. 关键结果

`mod 5`：

```text
projective_class_count = 36
both_bridge_square_classes = 15
centerline_square_classes = 11
noncenter_square_classes = 4
noncenter_extra_factor_zero_classes = 4
noncenter_extra_factor_nonzero_classes = 0
```

`mod 11`：

```text
projective_class_count = 144
both_bridge_square_classes = 36
centerline_square_classes = 28
noncenter_square_classes = 8
noncenter_extra_factor_zero_classes = 8
noncenter_extra_factor_nonzero_classes = 0
```

也就是说：

```text
mod 5 和 mod 11 中，
both-bridge-square 且非 centerline 的 projective residue
全部落在 E=0。
```

普通话说：

```text
如果真有 E!=0 的非中线解，
它在 5 和 11 这两个素数下不会有普通的非退化余类。
它必须贴着 centerline 或 E=0 的 p-adic 邻域。
```

---

## 5. 为什么这还不是证明

这不是全局证明。

原因：

```text
有理数 E 或 centerline factor 非零，
但它们的分子仍可能被 5 或 11 整除。
```

所以模 5/11 的结论只能说明：

```text
任意 E!=0 非中线真解，在 p=5 和 p=11 上必须满足
v_p(E) > 0 或 v_p(centerline factor) > 0
```

更准确地说，它把问题推到 p-adic 邻域里，下一步要做 lifting /
valuation，而不是停在 residue counting。

---

## 6. 反例护栏

这个现象不是任意素数都成立。

`mod 7`：

```text
noncenter_extra_factor_nonzero_classes = 32
```

普通话说：

```text
模 7 已经有非中线、E 非零、两桥都过平方的余类。
所以不能写成“所有模素数都杀掉”。
真正有用的是 5 和 11 这两个特殊入口。
```

---

## 7. 当前证明状态

可以安全说：

```text
1. E=0 分支已归约到 centerline/Yang Ji；
2. E!=0 非中线分支在 mod 5 和 mod 11 没有 projective 非退化余类；
3. 因此下一步应研究 5-adic / 11-adic lifting 或 valuation；
4. mod 7 显示这个局部现象不是普遍素数筛。
```

不能说：

```text
E!=0 分支已证明无解。
sum=A+B 已证明。
全平面倒数定理已证明。
```

---

## 8. 下一步

最具体的下一步：

```text
在 p=5 或 p=11 下，对 both-bridge-square 条件做 p-adic lifting。
目标是证明：

E!=0 且 centerline factor!=0 的有理解
不能无限提升；
或者会强迫某个 3 mod 4 / 5 / 11 相关赋值矛盾。
```

普通话说：

```text
现在模 5/11 已经把路口堵得很窄。
下一步不是再扫更大范围，而是看这些窄口能不能 p-adically 继续走。
```

---

## 9. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_residue_summary_routes_mod5_11_to_extra_factor -q
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_residue_summary_routes_mod5_11_to_extra_factor tests/test_rational_ratio.py::test_sum_ab_bridge_extra_factor_reduces_to_z_lemma_centerline -q
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py -q
PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
git diff --check
```

结果：

```text
1 passed
2 passed
91 passed
All checks passed
git diff --check passed
```
