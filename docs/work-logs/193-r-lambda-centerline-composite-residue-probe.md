# wl193 — `R_lambda` centerline composite residue probe

日期：2026-06-09

## 1. 本轮目标

wl192 说：

```text
mod 11 / 13 有筛选力，
但单个模数没有排光。
```

本轮看组合模数：

```text
11*13 = 143
```

以及几个小组合。

普通话说：

```text
单个筛子筛不干净，
就把两个筛子叠起来看看。
```

---

## 2. 复用 helper

本轮没有新增生产 API。

直接复用：

```text
sum_ab_centerline_quartic_primitive_residue_summary(modulus)
```

并新增测试固定：

```text
modulus = 143
```

的计数，防止后续改坏。

---

## 3. mod 143 结果

```text
modulus = 143
primitive_classes = 20160
degenerate_denominator_classes = 480
total_classes = 19680
square_residue_classes = 3600
non_square_residue_classes = 16080
zero_residue_classes = 0
```

普通话说：

```text
11 和 13 合起来确实杀掉了大部分类，
但仍有 3600 个活类。
```

所以：

```text
mod 143 不是一刀切证明。
```

---

## 4. 小组合表

跑了：

```text
55  = 5*11
65  = 5*13
77  = 7*11
91  = 7*13
143 = 11*13
```

结果：

```text
mod 55:
  primitive=2880,  degenerate=160, total=2720,  square=1040, nonsquare=1680, zero=0

mod 65:
  primitive=4032,  degenerate=192, total=3840,  square=1200, nonsquare=2640, zero=192

mod 77:
  primitive=5760,  degenerate=240, total=5520,  square=1440, nonsquare=4080, zero=0

mod 91:
  primitive=8064,  degenerate=288, total=7776,  square=1440, nonsquare=6336, zero=0

mod 143:
  primitive=20160, degenerate=480, total=19680, square=3600, nonsquare=16080, zero=0
```

普通话解释：

```text
组合模数筛选力明显增强，
但仍没有把活类筛空。
```

---

## 5. 可以说 / 不能说

可以说：

```text
mod 143 下仍有 3600 个 primitive 非退化平方剩余活类。
组合模数筛还没关闭 centerline。
```

不能说：

```text
centerline 有解。
centerline 无解。
mod 143 已经证明无解。
有理比例主定理已经证明。
```

因为：

```text
活类仍然存在。
```

---

## 6. 下一步

继续模筛有两条更合理路线：

```text
1. 做 CRT 活类传播：
   不只统计数量，而是保留活类并继续叠模数。

2. 对活类加更强约束：
   gcd(u,v)=1 的整数提升、
   parity、
   v^2-u^2 非零、
   lambda > 0。
```

如果这仍不闭合：

```text
转四次曲线 / 椭圆曲线。
```

普通话总结：

```text
筛子有用，但还不够锋利。
下一步要么保留活类继续组合，
要么换曲线工具。
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

组合模数探针：

```text
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_centerline_quartic_primitive_residue_summary,
)

for modulus in (11*13, 5*11, 5*13, 7*11, 7*13):
    s = sum_ab_centerline_quartic_primitive_residue_summary(modulus)
    print(
        modulus,
        s.primitive_classes,
        s.degenerate_denominator_classes,
        s.total_classes,
        s.square_residue_classes,
        s.non_square_residue_classes,
        s.zero_residue_classes,
    )
PY
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
