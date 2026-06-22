# wl290 — wl218 q-adic bridge valuation E-near tube

日期：2026-06-23

## 1. 本轮目标

接 wl289。

wl289 把 `p+lambda` q-adic shadow 的 recovery squareclass 改写成两条
Gaussian cross bridge 的 squareclass。本轮继续问：

```text
这些 q-adic shadow 样本在 bridge 差分因式分解里，
到底靠近 centerline，还是靠近 E=0？
```

普通话说：

```text
桥已经搭好了。
现在看这些样本走的是哪条桥下的窄路：
是贴着四条中线，还是贴着 E=0 那扇门。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicBridgeValuationRow
SumAbDualSlopeQAdicBridgeValuationSummary
```

新增 helper：

```text
sum_ab_dual_slope_qadic_bridge_valuation_summary(
    prime=q,
    exponent=e,
    representative_bound=H,
    sample_limit=N,
)
```

它对 generated q-adic samples 记录：

```text
v_q(t-u), v_q(t+u), v_q(tu-1), v_q(tu+1)
v_q(E)
v_q((k_x^2+1) - (k_y^2+1))
v_q(k_x^2+1), v_q(k_y^2+1)
v_2(k_x^2+1), v_2(k_y^2+1)
```

其中：

```text
E =
t^2u^2 + t^2u - t^2
+ tu^2 - t - u^2 - u + 1.
```

普通话说：

```text
这张表不是判断是不是平方；
它只是看 q-adic shadow 贴在哪个局部管道上。
```

---

## 3. q=31 的 TDD 样本

测试：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_valuation_summary_tracks_e_near_tube \
  -q
```

核心断言：

```text
sample_count = 8
centerline_factor_valuation_counts = {(0,0,0,0): 8}
extra_factor_valuation_counts = {2: 8}
bridge_difference_valuation_counts = {2: 8}
bridge_value_valuation_pair_counts = {(0,0): 8}
bridge_value_2adic_pair_counts = {(0,1): 4, (1,0): 4}
```

普通话说：

```text
q=31 的这些样本完全不贴中线；
四个中线因子都是 31-adic 单位。
它们贴的是 E=0，而且贴到二阶。
```

---

## 4. q=31,47,79 的生成探针

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_dual_slope_qadic_bridge_valuation_summary,
)

for q, bound in ((31, 80), (47, 220), (79, 260)):
    s = sum_ab_dual_slope_qadic_bridge_valuation_summary(
        prime=q,
        exponent=2,
        representative_bound=bound,
        sample_limit=8,
    )
    print(q)
    print(s.centerline_factor_valuation_counts)
    print(s.extra_factor_valuation_counts)
    print(s.bridge_difference_valuation_counts)
    print(s.bridge_value_valuation_pair_counts)
    print(s.bridge_value_2adic_pair_counts)
PY
```

输出：

```text
q=31
C factors:  {(0, 0, 0, 0): 8}
E:          {2: 8}
bridge diff:{2: 8}
bridge q:   {(0, 0): 8}
bridge 2:   {(0, 1): 4, (1, 0): 4}

q=47
C factors:  {(0, 0, 0, 0): 8}
E:          {2: 8}
bridge diff:{2: 8}
bridge q:   {(0, 0): 8}
bridge 2:   {(-6, -6): 2, (0, 1): 3, (1, 0): 3}

q=79
C factors:  {(0, 0, 0, 0): 8}
E:          {2: 8}
bridge diff:{2: 8}
bridge q:   {(0, 0): 8}
bridge 2:   {(-6, -6): 2, (-4, -4): 2, (0, 1): 2, (1, 0): 2}
```

普通话说：

```text
三个 shadow prime 都给同一个 q-adic 图像：
不靠中线，靠 E=0；
bridge 的两个平方值本身都是 q-adic 单位，
但它们的差因为 E 二阶可除而二阶可除。
```

---

## 5. 对证明路线的影响

这轮把 `p+lambda` shadow 的位置更精确了：

```text
不是 centerline-near tube:
  v_q(t-u), v_q(t+u), v_q(tu-1), v_q(tu+1) 全为 0；

而是 E-near tube:
  v_q(E) = 2；

bridge-square values:
  v_q(k_x^2+1) = v_q(k_y^2+1) = 0；

difference:
  v_q((k_x^2+1)-(k_y^2+1)) = 2。
```

所以，继续用 q 本身的 valuation 很难直接杀掉这条管道：

```text
k_x^2+1, k_y^2+1 都是 q-adic 单位；
q 只出现在两者差和 E 中。
```

普通话说：

```text
q 不是把某个桥值变坏；
q 只是让两条桥值非常接近。
这更像“贴着 E=0 的提升问题”，不是一个普通的坏素数平方类问题。
```

---

## 6. 现在能说和不能说

可以安全说：

```text
1. q=31,47,79 的 q^2 generated shadow 样本全在 E-near 管道；
2. 它们不在 centerline-near 管道；
3. q 本身不造成 bridge value 的奇赋值；
4. 2-adic 分桶存在多个形态，暂时没有一刀切 parity 矛盾。
```

不能说：

```text
E-near 管道已关闭；
bridge-cycle 问题已证明无解；
sum=A+B 已证明；
全平面倒数定理已证明。
```

---

## 7. 下一步

最直接的下一步是研究：

```text
E = q^2 * unit
C_i 全为 q-adic units
k_x^2+1, k_y^2+1 都为有理平方
```

是否能无限提升。

可拆成两条：

```text
1. E-near Hensel tube:
   在 F=E=0 的 smooth q-adic branch 附近，
   写出 bridge-square 条件的首项展开。

2. 2-adic residual:
   按 bridge_value_2adic_pair_counts 的几个桶分别展开，
   看是否有固定 parity obstruction。
```

如果这两条仍不关门，就说明 `sum=A+B` 证明需要全局曲线/递降，
而不是单素数局部 valuation。

---

## 8. 验证

TDD 过程：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_valuation_summary_tracks_e_near_tube \
  -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_bridge_valuation_summary'
```

实现后：

```text
1 passed
```
