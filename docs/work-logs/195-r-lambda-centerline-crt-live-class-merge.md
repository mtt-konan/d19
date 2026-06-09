# wl195 — `R_lambda` centerline CRT live-class merge

日期：2026-06-09

## 1. 本轮目标

wl194 已经能列出中心线四次方程的活余数类：

```text
F(u,v)=u^4+8u^3v+18u^2v^2-8uv^3+v^4
```

本轮问一个更具体的问题：

```text
如果 mod m 和 mod n 都有活类，
它们用 CRT 合成 mod mn 后，会不会明显减少？
```

普通话说：

```text
不是继续盲目加筛子，
而是先看筛子合起来有没有变锋利。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_crt_live_residue_classes(left_modulus, right_modulus)
sum_ab_centerline_quartic_crt_live_residue_summary(left_modulus, right_modulus)
```

要求：

```text
left_modulus 和 right_modulus 必须互素。
```

summary 会记录：

```text
两个小模数各自有多少 square primitive class
其中多少是 live class
其中多少是 denominator-degenerate square class
CRT 后得到多少 live class
直接枚举 combined modulus 得到多少 live class
两者是否一致
```

---

## 3. 关键发现：不能只合并 live × live

一开始自然会想：

```text
mod 5 live_count = 12
mod 7 live_count = 24
所以 mod 35 应该是 12*24 = 288？
```

但直接枚举给出：

```text
mod 35 live_count = 480
```

差出来的：

```text
480 - 288 = 192
```

原因是：

```text
某些类在 mod 5 下 denominator-degenerate，
也就是 v^2-u^2 = 0 mod 5；
但同一个 CRT 合成类在 mod 7 下不退化，
所以在 mod 35 下 v^2-u^2 != 0 mod 35。
```

普通话说：

```text
小模数里“撞到墙”的类，
合到大模数后不一定还撞墙。
所以 CRT 传播要保留单边退化类。
```

只有一种必须丢掉：

```text
两边都退化。
```

因为这时：

```text
v^2-u^2 = 0 mod m
v^2-u^2 = 0 mod n
```

于是：

```text
v^2-u^2 = 0 mod mn
```

---

## 4. 数据

探针：

```text
5 x 7 = 35
square primitive: 20, 24
live: 12, 24
degenerate square: 8, 0
live_live: 288
one_sided_degenerate: 192
both_degenerate: 0
merged/direct/match: 480 / 480 / True
```

```text
11 x 13 = 143
square primitive: 60, 60
live: 40, 60
degenerate square: 20, 0
live_live: 2400
one_sided_degenerate: 1200
both_degenerate: 0
merged/direct/match: 3600 / 3600 / True
```

更多 sanity check：

```text
5 x 11 = 55
merged/direct/match: 1040 / 1040 / True

7 x 11 = 77
merged/direct/match: 1440 / 1440 / True

5 x 13 = 65
merged/direct/match: 1200 / 1200 / True

7 x 13 = 91
merged/direct/match: 1440 / 1440 / True
```

---

## 5. 这说明什么

可以说：

```text
合成模数的 live class 可以用 CRT 精确解释。
mod 35 的 480、mod 143 的 3600 不是枚举 bug。
多出来的类来自单边 denominator-degenerate class。
```

不能说：

```text
centerline 已经证明有解。
centerline 已经证明无解。
继续乘模数一定会归零。
继续乘模数一定不会归零。
```

因为：

```text
这仍然只是必要条件筛。
```

---

## 6. 对路线的影响

这轮结果让“盲目加模数”看起来没那么诱人。

原因：

```text
活类不是简单 live×live，
还会吃进单边退化类。
所以合成后数量可能很快膨胀。
```

更值得走的下一步：

```text
1. 把中心线 quartic 转成曲线问题，尝试找有理点/递降证明。
2. 固定小整数 k，试 A=kB 是否也能化成类似 quartic 或 elliptic curve。
3. closure-first near-miss 方向继续方程化，查“第四边总差一点”的平方剩余障碍。
```

普通话总结：

```text
CRT 已经把筛子的结构看清楚了。
它没有立刻杀死中心线，
但告诉我们：下一步最好别只靠堆模数，要转向曲线或递降。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_quartic_integer_equation_tracks_residues -q
```

结果：

```text
1 passed
```

探针：

```text
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_centerline_quartic_crt_live_residue_summary,
)

for left, right in ((5,7),(11,13),(5,11),(7,11),(5,13),(7,13)):
    s = sum_ab_centerline_quartic_crt_live_residue_summary(left, right)
    print(left, right, s.merged_live_classes, s.direct_live_classes, s.matches_direct)
PY
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
