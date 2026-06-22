# wl289 — wl218 q-adic shadow Gaussian bridge cycle

日期：2026-06-23

## 1. 本轮目标

接 wl288。

wl288 说明 `p+lambda` q-adic shadow 的生成样本里，恢复平方类不含
`3 mod 4` 素数，只剩：

```text
2
1 mod 4 素数
```

本轮检查这些剩余 squareclass 是否能被已有 Gaussian bridge/cycle 解释。

普通话说：

```text
3 mod 4 那扇门没关上。
那就问：剩下这些 1 mod 4 因子是不是另一个已知机关，
也就是两个斜率之间的 Gaussian 角差？
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicNormBridgeLedger
SumAbDualSlopeQAdicNormBridgeSummary
```

新增 helper：

```text
sum_ab_dual_slope_qadic_norm_bridge_summary(
    prime=q,
    exponent=e,
    representative_bound=H,
    sample_limit=N,
)
```

它对每个 generated q-adic sample 同时计算：

```text
1. q-adic norm ledger；
2. Gaussian cross-bridge cycle；
3. recovery squareclass 是否等于 bridge squareclass；
4. generated slope 的好坏是否等于 bridge slope 的好坏。
```

普通话说：

```text
它不是再造新数学。
它只是把 wl288 的 q-adic 影子样本接到 wl264 的角差桥上。
```

---

## 3. q=31 的测试样本

测试命令：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_bridge_summary_rewrites_recovery_as_bridges \
  -q
```

核心断言：

```text
sample_count = 4
recovery_matches_bridge_squareclass_count = 4
generated_flags_match_bridge_flags_count = 4
all_cross_bridges_pythagorean_count = 0
```

第一个样本：

```text
(t,u) = (61/64, 5/77)

recovery squareclasses =
  (113231540023993, 54204260682434)

bridge squareclasses =
  (113231540023993, 54204260682434)
```

普通话说：

```text
恢复平方类不是凭空冒出来的；
它正好就是 generated slope 到 dual slope 的两条角差桥的平方类。
```

---

## 4. q=31,47,79 的生成探针

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_dual_slope_qadic_norm_bridge_summary,
)

for q, bound in ((31, 80), (47, 220), (79, 260)):
    s = sum_ab_dual_slope_qadic_norm_bridge_summary(
        prime=q,
        exponent=2,
        representative_bound=bound,
        sample_limit=8,
    )
    print(
        q,
        s.sample_count,
        s.recovery_matches_bridge_squareclass_count,
        s.generated_flags_match_bridge_flags_count,
        s.all_cross_bridges_pythagorean_count,
    )
PY
```

输出：

```text
q=31: samples=8, squareclass matches=8, flags match=8, all bridges good=0
q=47: samples=8, squareclass matches=8, flags match=8, all bridges good=0
q=79: samples=8, squareclass matches=8, flags match=8, all bridges good=0
```

普通话说：

```text
三个 shadow prime 的样本都一样：
q-adic recovery 条件完全等价于 cross-bridge 条件；
但这些样本仍然不是四平方真闭环，因为两条 bridge 没有同时变成好斜率。
```

---

## 5. 对证明路线的影响

这一轮把 wl288 的剩余障碍进一步定位了：

```text
3 mod 4 valuation
  -> 找到 p+lambda shadow，但不直接关门；

q-adic norm Q(t), Q(u)
  -> 记录 shadow prime q 的偶次吸收；

Gaussian bridge cycle
  -> 说明 recovery squareclass 正是两条角差桥的 squareclass；

剩余问题
  -> 排除两条 cross bridge 同时为勾股斜率的非中心 q-adic shadow。
```

普通话说：

```text
我们没有证明无解。
但已经把“坏素数去哪了”说清楚了：
它们没有消失，而是变成了两条角差桥自己的勾股条件。
```

因此原关键引理应改写为：

```text
在 p+lambda shadow 中，
3 mod 4 赋值只负责定位 shadow；
norm 负责追踪 q 的偶次吸收；
Gaussian bridge 把 recovery squareclass 改写成 bridge squareclass；
最后还需要一个 bridge-cycle 无非中心真闭环引理。
```

---

## 6. 现在能说和不能说

可以安全说：

```text
1. q=31,47,79 的生成 q^2 样本都满足：
   recovery squareclasses = Gaussian bridge squareclasses。
2. generated slope 是否为好斜率，与 cross bridge 是否为好斜率逐项一致。
3. 这些样本没有任何一个 all_cross_bridges_are_pythagorean。
4. p+lambda shadow 的剩余问题已经转成 bridge-cycle 问题。
```

不能说：

```text
bridge-cycle 问题已证明无解；
sum=A+B 已证明；
全平面倒数定理已证明。
```

---

## 7. 下一步

下一步不应再只数 recovery squareclass prime。

应直接研究两条 bridge ratio：

```text
k_x = (x - dual_y)/(dual_y*x + 1)
k_y = (y - dual_x)/(dual_x*y + 1)
```

目标引理：

```text
在 p+lambda q-adic shadow 上，
k_x^2+1 和 k_y^2+1 不可能同时为有理平方，
除非回到 centerline / reciprocal / p=lambda 退化。
```

可行路线：

```text
1. 对 k_x,k_y 建立 q-adic norm ledger；
2. 检查 bridge difference factorization 中的 E 因子和 new curve 因子；
3. 分离 2-adic parity，因为奇素数已经全在 1 mod 4。
```

---

## 8. 验证

TDD 过程：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_bridge_summary_rewrites_recovery_as_bridges \
  -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_norm_bridge_summary'
```

实现后：

```text
1 passed
```
