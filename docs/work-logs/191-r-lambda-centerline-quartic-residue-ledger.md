# wl191 — `R_lambda` centerline quartic residue ledger

日期：2026-06-09

## 1. 本轮目标

wl190 得到中心线剩余四次式：

```text
Q(t) = t^4 + 8t^3 + 18t^2 - 8t + 1
```

本轮把：

```text
t = u/v
```

写成整数形式，并做小模数 residue 诊断。

普通话说：

```text
现在不只看有理 t，
而是看整数 u,v 下这个四次式在模 p 里像不像平方。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_integer_equation(u, v)
```

返回：

```text
SumAbCenterlineQuarticIntegerEquation
```

记录：

```text
value
denominator_square
reduced_lambda_value
squareclass
is_square
residue(modulus)
residue_is_square(modulus)
```

另新增：

```text
sum_ab_centerline_quartic_residue_summary(modulus)
```

返回：

```text
SumAbCenterlineQuarticResidueSummary
```

---

## 3. 整数形式

若：

```text
t = u/v
```

则：

```text
Q(t) = F(u,v) / v^4
```

其中：

```text
F(u,v) =
u^4 + 8u^3v + 18u^2v^2 - 8uv^3 + v^4
```

而：

```text
center^2 + lambda^2
= Q(t) / (1-t^2)^2
= F(u,v) / (v^2-u^2)^2
```

普通话说：

```text
分母已经是平方，
所以剩下就是 F(u,v) 能不能是平方。
```

---

## 4. 样本

输入：

```text
u = 3
v = 5
```

得到：

```text
F(3,5) = 2836
(v^2-u^2)^2 = 256
reduced_lambda_value = 709/64
squareclass = 709
is_square = False
```

模 5：

```text
F(3,5) ≡ 1 mod 5
```

而 1 是平方剩余。

普通话说：

```text
这个样本不是被 mod 5 杀掉的；
它在 mod 5 看起来还像平方。
```

---

## 5. 小模数诊断

跑了：

```text
modulus = 3,5,7,8,11,13,16
```

结果：

```text
mod 3 : total=9,   square=5,   nonsquare=4,   zero=1
mod 5 : total=25,  square=21,  nonsquare=4,   zero=9
mod 7 : total=49,  square=25,  nonsquare=24,  zero=1
mod 8 : total=64,  square=64,  nonsquare=0,   zero=16
mod 11: total=121, square=61,  nonsquare=60,  zero=1
mod 13: total=169, square=61,  nonsquare=108, zero=25
mod 16: total=256, square=256, nonsquare=0,   zero=64
```

普通话解释：

```text
没有一个小模数直接把所有类排光。
mod 8 / 16 完全没有障碍。
mod 13 排除比例比较高，但仍然有很多活类。
```

---

## 6. 可以说 / 不能说

可以说：

```text
centerline quartic 已有整数形式 F(u,v)。
小模数诊断没有发现一刀切障碍。
mod 13 比较有筛选力，但不是证明。
```

不能说：

```text
centerline 有解。
centerline 无解。
mod 13 已经证明无解。
有理比例主定理已经证明。
```

因为：

```text
这只是所有 residue class 的粗统计，
还没有加入 gcd、parity、primitive 条件，
也没有证明所有活类不可提升。
```

---

## 7. 下一步

更有价值的下一步：

```text
1. 加 primitive 条件 gcd(u,v)=1。
2. 分析 v^2-u^2 不能为 0。
3. 对活类做 CRT / 多模数组合，看是否能覆盖。
4. 如果模筛不够，转成四次曲线 / 椭圆曲线研究。
```

普通话总结：

```text
这条路没有被一个小模数秒杀。
要么加更多结构筛，
要么进入曲线理论。
```

---

## 8. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_quartic_integer_equation_tracks_residues -q
```

结果：

```text
1 passed
```

小模数探针：

```text
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_centerline_quartic_residue_summary,
)

for modulus in (3, 5, 7, 8, 11, 13, 16):
    summary = sum_ab_centerline_quartic_residue_summary(modulus)
    print(
        modulus,
        summary.total_classes,
        summary.square_residue_classes,
        summary.non_square_residue_classes,
        summary.zero_residue_classes,
        summary.square_residues,
    )
PY
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
