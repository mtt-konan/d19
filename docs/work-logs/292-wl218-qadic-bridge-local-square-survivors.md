# wl292 — wl218 q-adic bridge local-square survivors

日期：2026-06-23

## 1. 本轮目标

接 wl291。

wl291 说明 2-adic parity 能杀部分 E-near 样本，但 q=47,79 仍有
`Q_2` 局部平方幸存者。本轮继续检查这些幸存者在 shadow prime `q` 上是否也
通过局部平方测试。

普通话说：

```text
2-adic 已经放行了一些车。
现在看这些车到了原来的 q-adic 路口，会不会又被拦住。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicBridgeLocalSquareSummary
```

新增 helper：

```text
sum_ab_dual_slope_qadic_bridge_local_square_summary(
    prime=q,
    exponent=e,
    representative_bound=H,
    sample_limit=N,
)
```

它统计：

```text
sample_count
two_adic_local_square_count
q_adic_local_square_count
combined_q_and_2_adic_local_square_count
q_adic_local_square_flag_pair_counts
combined_survivor_parameter_pairs
```

这里的 `q_adic_local_square` 用完整的 `Q_q` 局部平方判定：

```text
v_q(value) 偶数
去掉 q 的幂后 unit 是 mod q 平方
```

普通话说：

```text
对奇素数 q 来说，只要这两条过了，Hensel 会把平方根升到所有 q^k。
所以这不是只看一层余数。
```

---

## 3. TDD 固定结果

测试：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_local_square_summary_keeps_survivors \
  -q
```

核心断言：

```text
q=47:
sample_count = 8
q_adic_local_square_count = 8
two_adic_local_square_count = 2
combined_q_and_2_adic_local_square_count = 2
q_adic_local_square_flag_pair_counts = {(True, True): 8}

q=79:
sample_count = 8
q_adic_local_square_count = 8
two_adic_local_square_count = 4
combined_q_and_2_adic_local_square_count = 4
```

普通话说：

```text
所有样本在 q-adic 上都过。
剩下多少，完全由 2-adic 先筛掉多少决定。
```

---

## 4. q=31,47,79 探针

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_dual_slope_qadic_bridge_local_square_summary,
)

for q, bound in ((31, 80), (47, 220), (79, 260)):
    s = sum_ab_dual_slope_qadic_bridge_local_square_summary(
        prime=q,
        exponent=2,
        representative_bound=bound,
        sample_limit=8,
    )
    print(q, s.q_adic_local_square_count, s.two_adic_local_square_count)
    print(s.combined_q_and_2_adic_local_square_count)
    print(s.combined_survivor_parameter_pairs)
PY
```

输出：

```text
q=31
q-adic local-square = 8
2-adic local-square = 0
combined survivors = 0

q=47
q-adic local-square = 8
2-adic local-square = 2
combined survivors = 2
survivors:
  (3/86, 27/50)
  (27/50, 3/86)

q=79
q-adic local-square = 8
2-adic local-square = 4
combined survivors = 4
survivors:
  (151/176, 49/108)
  (37/41, 19/161)
  (49/108, 151/176)
  (19/161, 37/41)
```

普通话说：

```text
q-adic 高阶平方条件没有把 E-near 管道关掉。
q=47 和 q=79 甚至同时通过了 q-adic 与 2-adic 的局部平方测试。
```

---

## 5. 对证明路线的影响

现在可以更清楚地修正原关键引理：

原设想：

```text
用 q == 3 mod 4 的赋值，强制 lambda^2-p^2 矛盾。
```

当前证据显示，在 `p+lambda` shadow 上：

```text
1. q == 15 mod 16 的 shadow prime q 只定位 E-near 管道；
2. bridge values 在 Q_q 上全是局部平方；
3. 2-adic 能杀一部分，但 q=47,79 有 Q_q 与 Q_2 同时幸存者；
4. 因此单个 q-adic 高阶局部平方 + 2-adic 仍不足以关闭。
```

普通话说：

```text
这条路不是“局部自动坏掉”。
如果要证明无解，必须用全局有理平方的分子分母结构、
多素数联动，或一个真正的递降/曲线论证。
```

---

## 6. 现在能说和不能说

可以安全说：

```text
1. bridge values 的 Q_q 局部平方条件在 q=31,47,79 的样本里全部通过；
2. q=47,79 有同时通过 Q_q 和 Q_2 的 E-near generated samples；
3. 这排除了“单 q 高阶局部平方自动失败”的短证明；
4. sum=A+B 的 p+lambda shadow 剩余核心已变成 global/descent 问题。
```

不能说：

```text
E-near 管道存在全局有理解；
E-near 管道已关闭；
sum=A+B 已证明；
倒数定理已证明。
```

---

## 7. 下一步

下一步应转向更全局的对象，而不是继续只查单素数局部：

```text
1. 对 combined survivors 计算全局 bridge squareclasses；
2. 看是否总会引入另一个 3 mod 4 素数；
3. 若没有，则尝试构造递降映射：
   E-near point -> 更小高度的 E-near point 或 centerline point；
4. 或把 E-near survivor 落到已有 new-curve/z-lemma/centerline pullback 上。
```

普通话说：

```text
局部门已经基本试过了。
接下来要么找“另一个坏素数”，要么证明这种点会递降回中线。
```

---

## 8. 验证

TDD 过程：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_local_square_summary_keeps_survivors \
  -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_bridge_local_square_summary'
```

实现后：

```text
1 passed
```
