# wl194 — `R_lambda` centerline live residue classes

日期：2026-06-09

## 1. 本轮目标

wl193 说：

```text
mod 143 还有 3600 个活类。
```

但只有数量还不够。

本轮把活类本身列出来：

```text
(u, v, F(u,v) mod M)
```

普通话说：

```text
之前只知道“还有很多门没关”；
现在知道是哪几扇门没关。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_live_residue_classes(modulus)
```

返回：

```text
tuple[SumAbCenterlineQuarticLiveResidueClass, ...]
```

每个活类记录：

```text
u
v
residue
```

筛选条件：

```text
gcd(u,v,modulus)=1
v^2-u^2 != 0 mod modulus
F(u,v) 是平方剩余 mod modulus
```

---

## 3. mod 5 活类

测试固定：

```text
modulus = 5
```

活类是：

```text
(0,1,1)
(0,2,1)
(0,3,1)
(0,4,1)
(1,0,1)
(1,2,1)
(2,0,1)
(2,4,1)
(3,0,1)
(3,1,1)
(4,0,1)
(4,3,1)
```

总数：

```text
12
```

普通话说：

```text
mod 5 下，活类不多，
而且 residue 全是 1。
```

---

## 4. mod 143 活类

跑了：

```text
modulus = 143
```

结果：

```text
live_count = 3600
```

前几个：

```text
(0,1,1)
(0,2,16)
(0,3,81)
(0,4,113)
(0,5,53)
(0,6,9)
(0,7,113)
(0,8,92)
(0,9,126)
(0,10,133)
(0,12,1)
(0,14,92)
```

residue 分布前几项：

```text
78  -> 288
104 -> 288
130 -> 288
91  -> 288
26  -> 288
1   -> 96
16  -> 96
81  -> 96
113 -> 96
53  -> 96
9   -> 96
92  -> 96
```

普通话说：

```text
mod 143 不只是“有活类”，
而且活类结构很成批。
这提示单纯继续乘模数，可能会增长很快。
```

---

## 5. 可以说 / 不能说

可以说：

```text
centerline quartic 的活类现在可以枚举。
mod 143 有 3600 个活类。
这些活类可作为 CRT 传播输入。
```

不能说：

```text
活类能提升成有理解。
活类不能提升成有理解。
centerline 已经证明有解或无解。
```

因为：

```text
模活类只是必要条件。
```

---

## 6. 下一步

下一步如果继续模筛：

```text
1. 实现 live class CRT 合并。
2. 观察活类数量是否快速归零。
3. 若不归零，停止盲目乘模数，改走曲线/递降。
```

普通话总结：

```text
现在筛子终于不只是报数量，
而是能把“幸存者名单”交给下一轮。
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
from collections import Counter
from rational_distance.concordant.rational_ratio import (
    sum_ab_centerline_quartic_live_residue_classes,
)

for modulus in (5, 143):
    live = sum_ab_centerline_quartic_live_residue_classes(modulus)
    residues = Counter(item.residue for item in live)
    print('mod', modulus, 'count', len(live))
    print('first', [(item.u, item.v, item.residue) for item in live[:12]])
    print('top residues', residues.most_common(12))
PY
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
