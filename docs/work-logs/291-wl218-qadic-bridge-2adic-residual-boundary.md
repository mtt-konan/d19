# wl291 — wl218 q-adic bridge 2-adic residual boundary

日期：2026-06-23

## 1. 本轮目标

接 wl290。

wl290 说明 `p+lambda` q-adic shadow 在 bridge 层落在：

```text
C_i 全是 q-adic units
E 二阶可除
k_x^2+1, k_y^2+1 是 q-adic units
```

本轮检查剩下的 2-adic 桶能不能直接杀掉这些样本。

普通话说：

```text
奇素数那边没直接坏。
那就看 2-adic：如果某个桥值的 2-adic 赋值是奇数，
它绝不可能是有理平方。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicBridgeTwoAdicSummary
```

新增 helper：

```text
sum_ab_dual_slope_qadic_bridge_2adic_summary(
    prime=q,
    exponent=e,
    representative_bound=H,
    sample_limit=N,
)
```

它复用 wl290 的 valuation rows，并统计：

```text
sample_count
parity_killed_count
two_adic_local_square_count
bridge_value_2adic_pair_counts
local_square_unit_mod8_pair_counts
```

判定规则：

```text
1. 若 v_2(k_x^2+1) 或 v_2(k_y^2+1) 是奇数，则 parity killed；
2. 若两个 v_2 都是偶数，再看去掉 2 幂后的 odd unit 是否都是 1 mod 8；
3. unit pair = (1,1) 表示两个桥值都通过 Q_2 局部平方测试。
```

普通话说：

```text
先看 2 的指数偶不偶；
指数过了，再看剩下的奇数部分是不是 1 mod 8。
```

---

## 3. TDD 固定结果

测试：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_2adic_summary_separates_parity_survivors \
  -q
```

核心断言：

```text
q=31:
sample_count = 8
parity_killed_count = 8
two_adic_local_square_count = 0
bridge_value_2adic_pair_counts = {(0,1): 4, (1,0): 4}

q=47:
sample_count = 8
parity_killed_count = 6
two_adic_local_square_count = 2
bridge_value_2adic_pair_counts = {(-6,-6): 2, (0,1): 3, (1,0): 3}
local_square_unit_mod8_pair_counts = {(1,1): 2}
```

普通话说：

```text
31 这批样本被 2-adic parity 全杀。
但 47 已经有两个样本在 Q_2 里也过了。
```

---

## 4. q=31,47,79 探针

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_dual_slope_qadic_bridge_2adic_summary,
)

for q, bound in ((31, 80), (47, 220), (79, 260)):
    s = sum_ab_dual_slope_qadic_bridge_2adic_summary(
        prime=q,
        exponent=2,
        representative_bound=bound,
        sample_limit=8,
    )
    print(q, s.parity_killed_count, s.two_adic_local_square_count)
    print(s.bridge_value_2adic_pair_counts)
    print(s.local_square_unit_mod8_pair_counts)
PY
```

输出：

```text
q=31
parity killed = 8
Q_2 local-square survivors = 0
v2 buckets = {(0,1): 4, (1,0): 4}
unit mod8 survivor buckets = {}

q=47
parity killed = 6
Q_2 local-square survivors = 2
v2 buckets = {(-6,-6): 2, (0,1): 3, (1,0): 3}
unit mod8 survivor buckets = {(1,1): 2}

q=79
parity killed = 4
Q_2 local-square survivors = 4
v2 buckets = {(-6,-6): 2, (-4,-4): 2, (0,1): 2, (1,0): 2}
unit mod8 survivor buckets = {(1,1): 4}
```

普通话说：

```text
2-adic 能杀一部分，甚至能杀 q=31 的这批样本；
但它不是统一证明。
q=47,79 已经有真正通过 Q_2 局部平方测试的 E-near 样本。
```

---

## 5. 对证明路线的影响

现在 `p+lambda` shadow 的局部图像更清楚：

```text
3 mod 4 valuation:
  只能定位 shadow，不能直接关门；

q-adic bridge valuation:
  shadow 落在 E-near tube，不落在 centerline-near tube；

2-adic:
  能杀部分 generated representatives，但存在 Q_2-local-square survivors。
```

所以不能把关键引理写成：

```text
3 mod 4 + 2-adic 局部赋值直接矛盾。
```

更准确的证明目标应变成：

```text
E-near tube 中，
同时满足全局有理平方的点不存在；
局部 q-adic 和 2-adic 条件本身还不足以证明这一点。
```

普通话说：

```text
局部路口都看过了：
有些路口会挡车，但不是每个方向都挡。
剩下的车必须用更高阶的 Hensel 展开或全局递降来处理。
```

---

## 6. 现在能说和不能说

可以安全说：

```text
1. 2-adic parity 能杀 q=31 的 generated q^2 样本；
2. q=47,79 有 generated 样本通过 Q_2 局部平方测试；
3. 因此 2-adic 不是统一关闭 E-near tube 的一刀切；
4. sum=A+B 的剩余核心仍是 E-near Hensel/global 问题。
```

不能说：

```text
E-near tube 已关闭；
sum=A+B 已证明；
倒数定理已证明。
```

---

## 7. 下一步

下一步应避免继续只看单点 generated representatives。

更有证明价值的是：

```text
1. 在 E=0 smooth q-adic branch 附近写 Hensel 参数 h；
2. 展开 k_x^2+1 和 k_y^2+1 的 square condition 到 q^3/q^4；
3. 检查 Q_2-local-square survivor 是否能同时满足高阶 q-adic square；
4. 若仍能提升，则转向全局曲线/递降，而不是局部赋值。
```

---

## 8. 验证

TDD 过程：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_2adic_summary_separates_parity_survivors \
  -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_bridge_2adic_summary'
```

实现后：

```text
1 passed
```
