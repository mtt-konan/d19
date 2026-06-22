# wl266 — wl218 extra factor reduces to z-lemma/centerline

日期：2026-06-22

## 1. 本轮目标

接 wl265。

wl265 把两条 Gaussian cross bridge 的平方值差拆成：

```text
(k_x^2+1) - (k_y^2+1)
= centerline factor * E * square-ish factors.
```

其中额外出口是：

```text
E =
t^2u^2 + t^2u - t^2
+ tu^2 - t - u^2 - u + 1.
```

本轮处理：

```text
E = 0
```

普通话说：

```text
桥差分除了“回到中线”之外，还留下一个门 E=0。
这轮证明这个门不是新世界：它会先进入 wl240 的新曲线，
再进入 wl241 的 z 引理，最后回到中线 quartic。
```

---

## 2. E=0 强迫新曲线

把 `E` 看成 `u` 的二次式：

```text
E = (t^2+t-1)u^2 + (t^2-1)u + (1-t-t^2).
```

若 `E=0` 有有理 `u`，则判别式必须是有理平方：

```text
5t^4 + 8t^3 - 6t^2 - 8t + 5 = square.
```

这就是 wl240 的新曲线。

---

## 3. 新曲线进入 z 引理

令：

```text
z = t - 1/t.
```

则：

```text
(5t^4 + 8t^3 - 6t^2 - 8t + 5)/t^2
= 5z^2 + 8z + 4.
```

同时：

```text
z^2 + 4 = (t + 1/t)^2.
```

所以 `E=0` 给出的新曲线平方点会给出 wl241 的 z 引理条件：

```text
z^2 + 4          square
5z^2 + 8z + 4   square.
```

---

## 4. z 引理进入 centerline quartic

用第一条 conic 的参数：

```text
m = (t-1)/(t+1)
```

则：

```text
z = -4m / ((m-1)(m+1)).
```

wl241 已经记录：

```text
5z^2 + 8z + 4
= 4R(m)/((m-1)^2(m+1)^2)
```

其中：

```text
R(m) = m^4 - 8m^3 + 18m^2 + 8m + 1.
```

而：

```text
R(m) = Q(-m)
Q(a) = a^4 + 8a^3 + 18a^2 - 8a + 1.
```

也就是说：

```text
E=0
=> 新曲线有理点
=> z 引理
=> centerline quartic.
```

普通话说：

```text
E=0 不需要单独开一条新证明线。
它完全复用中线分支的证明责任。
```

---

## 5. 引用 Yang Ji 时的状态

wl226 / wl241 的证据边界是：

```text
几何层面：Yang Ji Theorem 2 + Remark 1 关闭中线；
本地代数层面：PARI rank 0 诊断已复核，但还缺显式 birational pullback。
```

因此如果本轮允许引用 Yang Ji 中线定理，则：

```text
z 引理关闭
=> E=0 非退化出口关闭.
```

在当前 positive dual-slope 参数范围里：

```text
0 < t < 1,
```

而 z 引理关闭会给：

```text
z = 0
=> t = ±1.
```

正参数内只剩：

```text
t = 1,
```

但 `t=1` 让：

```text
dual_x = (1-t^2)/(2t) = 0,
```

不属于正斜率分支。

普通话说：

```text
接受 Yang Ji 后，E=0 这扇门在真正的正参数问题里打不开。
```

---

## 6. 新 helper

新增 dataclass：

```text
SumAbBridgeExtraFactorZLemmaReduction
```

新增 helper：

```text
sum_ab_bridge_extra_factor_z_lemma_reduction(t)
```

它记录：

```text
z = t - 1/t
m = (t-1)/(t+1)
new_curve_value_t
scaled_new_curve_value
z_recovery_square
z_lemma_new_curve_square
centerline_bridge
extra_factor_reduces_to_centerline
```

新增测试：

```text
test_sum_ab_bridge_extra_factor_reduces_to_z_lemma_centerline
```

固定样例：

```text
t = 1/4
z = -15/4
m = -3/5
new_curve_value_t = 709/256
scaled_new_curve_value = 709/16
centerline_parameter = 3/5
centerline_quartic = 2836/625
```

---

## 7. 当前证明状态

可以安全说：

```text
1. bridge 差分的额外出口 E=0 已归约到 wl241 z 引理；
2. z 引理已归约到 centerline quartic；
3. 若引用 Yang Ji 中线定理，则 E=0 非退化出口关闭；
4. 若要求仓库内完全自足代数证明，则 E=0 继承 centerline pullback 缺口。
```

不能说：

```text
sum=A+B 已证明。
整个 bridge 差分路线已关闭。
E != 0 的 valuation/descent 已完成。
全平面倒数定理已证明。
```

---

## 8. 下一步

回到 wl265 的二分：

```text
A. E=0 分支：已归约到 centerline/Yang Ji。
B. E!=0 分支：还要用 bridge 差分里的 centerline factor 做 valuation/descent。
```

所以接下来不该再把注意力放在 E=0 上，而应处理：

```text
E != 0,
k_x^2+1 square,
k_y^2+1 square,
centerline factor != 0
```

是否会造成某个 `3 mod 4` 素数赋值矛盾。

---

## 9. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_bridge_extra_factor_reduces_to_z_lemma_centerline -q
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py -q
PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
git diff --check
```

结果：

```text
1 passed
90 passed
All checks passed
git diff --check passed
```
