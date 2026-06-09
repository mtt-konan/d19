# wl192 — `R_lambda` centerline primitive residue filter

日期：2026-06-09

## 1. 本轮目标

wl191 做了粗 residue 统计，但还没加入：

```text
gcd / primitive 条件
v^2-u^2 != 0
```

本轮补一个更贴近有理参数的 residue summary。

普通话说：

```text
不是所有模类都像真正的 u/v。
这轮先把明显不该算的类过滤掉。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_primitive_residue_summary(modulus)
```

返回：

```text
SumAbCenterlineQuarticPrimitiveResidueSummary
```

记录：

```text
primitive_classes
degenerate_denominator_classes
total_classes
square_residue_classes
non_square_residue_classes
zero_residue_classes
square_residues
```

---

## 3. 过滤条件

对模 `M` 的 `(u,v)`：

```text
gcd(u,v,M) = 1
```

作为 primitive 近似。

再排除：

```text
v^2-u^2 ≡ 0 (mod M)
```

因为中心线剩余表达式有分母：

```text
(v^2-u^2)^2
```

普通话说：

```text
分母在模 M 下变成 0 的类，
不能直接拿来判断平方剩余。
```

---

## 4. 测试样本：mod 5

```text
primitive_classes = 24
degenerate_denominator_classes = 8
total_classes = 16
square_residue_classes = 12
non_square_residue_classes = 4
zero_residue_classes = 0
square_residues = (0,1,4)
```

普通话说：

```text
过滤后，mod 5 仍只能排除 4/16 的活类。
它有筛选力，但不是证明。
```

---

## 5. 小模数探针

跑了：

```text
modulus = 3,5,7,8,11,13,16
```

结果：

```text
mod 3:
  primitive=8,   degenerate=4,  total=4,   square=4,   nonsquare=0,  zero=0

mod 5:
  primitive=24,  degenerate=8,  total=16,  square=12,  nonsquare=4,  zero=0

mod 7:
  primitive=48,  degenerate=12, total=36,  square=24,  nonsquare=12, zero=0

mod 8:
  primitive=48,  degenerate=16, total=32,  square=32,  nonsquare=0,  zero=0

mod 11:
  primitive=120, degenerate=20, total=100, square=40,  nonsquare=60, zero=0

mod 13:
  primitive=168, degenerate=24, total=144, square=60,  nonsquare=84, zero=24

mod 16:
  primitive=192, degenerate=32, total=160, square=160, nonsquare=0,  zero=0
```

普通话解释：

```text
mod 3 / 8 / 16 没有障碍。
mod 11 / 13 比较有筛选力。
但没有任何一个小模数直接排光。
```

---

## 6. 可以说 / 不能说

可以说：

```text
primitive + 非退化分母过滤后，小模数仍没有给出一刀切证明。
mod 11 / 13 是后续组合筛更值得看的模数。
```

不能说：

```text
centerline 有解。
centerline 无解。
mod 11 或 mod 13 已经证明无解。
有理比例主定理已经证明。
```

因为：

```text
仍然存在 square-residue 活类。
```

---

## 7. 下一步

更值得做：

```text
1. 组合多个模数做 CRT 活类传播。
2. 对活类加入 parity / gcd(u,v)=1 的更强整数条件。
3. 如果模筛仍不闭合，转椭圆曲线或递降。
```

普通话总结：

```text
小模数没有直接开门杀。
centerline 可能需要曲线理论，或者更聪明的多模数组合。
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

小探针命令：

```text
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_centerline_quartic_primitive_residue_summary,
)

for modulus in (3, 5, 7, 8, 11, 13, 16):
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
