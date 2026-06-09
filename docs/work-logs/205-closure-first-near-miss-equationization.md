# wl205 — closure-first near-miss equationization

日期：2026-06-09

## 1. 本轮目标

wl204 把 D4 点换成不变量表后，建议下一步别继续整体聚类，而是挑低 delta / 高 raw_count 点方程化。

本轮把三个样本拆成：

```text
closure 方程
四条边的平方状态
已通过边的 primitive Pythagorean triple
失败边离最近平方差多少
```

普通话说：

```text
不要只说“三条边过，第四条差一点”。
把哪三条怎么过、第四条差在哪，全部写成账本。
```

---

## 2. 新脚本

新增：

```text
scripts/theory/equationize_closure_first_near_miss.py
```

用法：

```text
uv run python scripts/theory/equationize_closure_first_near_miss.py \
  --sample '17745,53911,60840,132496,diff=A+B' \
  --sample '7,45,24,28,sum=A+B' \
  --sample '12,63,16,35,sum=|A-B|'
```

输出每个样本的：

```text
A,B,N1,N2
closure target / left / holds
square_count
missing_edges
edge ledger
```

每条已过边会拆成：

```text
leg1^2 + leg2^2 = hypotenuse^2
primitive triple
scale
```

失败边会给：

```text
value
nearest_root
nearest_square
nearest_delta
signed_delta
```

---

## 3. 样本 1：唯一 delta=1 点

样本：

```text
(A,B,N1,N2) = (17745, 53911, 60840, 132496)
relation = diff=A+B
```

closure：

```text
|N1-N2| = 71656
A+B     = 71656
```

三条已过边：

| edge | equation | primitive | scale |
|---|---|---|---:|
| `A-N1` | `17745^2 + 60840^2 = 63375^2` | `(7,24,25)` | 2535 |
| `A-N2` | `17745^2 + 132496^2 = 133679^2` | `(15,112,113)` | 1183 |
| `B-N1` | `53911^2 + 60840^2 = 81289^2` | `(319,360,481)` | 169 |

失败边：

```text
B-N2:
53911^2 + 132496^2 = 20461585937
143044^2            = 20461585936
signed_delta        = +1
```

普通话说：

```text
它不是差一个“边长单位”。
它是第四条平方数正好比 143044^2 大 1。
```

---

## 4. 样本 2：高 raw_count + inside sum

样本：

```text
(A,B,N1,N2) = (7, 45, 24, 28)
relation = sum=A+B
raw_count = 5793
```

closure：

```text
N1+N2 = 52
A+B   = 52
```

三条已过边：

| edge | equation | primitive | scale |
|---|---|---|---:|
| `A-N1` | `7^2 + 24^2 = 25^2` | `(7,24,25)` | 1 |
| `B-N1` | `45^2 + 24^2 = 51^2` | `(8,15,17)` | 3 |
| `B-N2` | `45^2 + 28^2 = 53^2` | `(28,45,53)` | 1 |

失败边：

```text
A-N2:
7^2 + 28^2 = 833
29^2       = 841
signed_delta = -8
```

普通话说：

```text
这个小点很像 delta=1 大点的缩小版：
它也含 (7,24,25)，但失败边在平方下方差 8。
```

---

## 5. 样本 3：高 raw_count + outside sum

样本：

```text
(A,B,N1,N2) = (12, 63, 16, 35)
relation = sum=|A-B|
raw_count = 4444
```

closure：

```text
N1+N2 = 51
|A-B| = 51
```

三条已过边：

| edge | equation | primitive | scale |
|---|---|---|---:|
| `A-N1` | `12^2 + 16^2 = 20^2` | `(3,4,5)` | 4 |
| `A-N2` | `12^2 + 35^2 = 37^2` | `(12,35,37)` | 1 |
| `B-N1` | `63^2 + 16^2 = 65^2` | `(16,63,65)` | 1 |

失败边：

```text
B-N2:
63^2 + 35^2 = 5194
72^2        = 5184
signed_delta = +10
```

---

## 6. 观察

可以说：

```text
三个样本都能写成“三个 primitive triple 约束 + 一个 signed_delta”。
delta=1 样本和 (7,45,24,28) 都含 primitive (7,24,25)。
高 raw_count 点确实是方程化的好入口，不只是统计噪音。
```

不能说：

```text
这些样本已经证明了 near-miss 不可能变成 hit。
所有低 delta 点都来自同一个家族。
```

原因：

```text
本轮只方程化 3 个代表点。
还没有把 primitive triple 参数联立成一般方程。
```

普通话总结：

```text
现在该从“样本账本”进入“参数方程”。
```

---

## 7. 下一步

最自然的下一步是从样本 2 开始。

它最小：

```text
(7,45,24,28)
```

而且三条已过边是：

```text
(7,24,25)
3*(8,15,17)
(28,45,53)
```

可以尝试把它推广为：

```text
A-N1 = one primitive triple
B-N1 = another scaled primitive triple
B-N2 = third primitive triple
N1+N2 = A+B
```

然后问：

```text
A^2 + N2^2
```

为什么落在平方下方 8。

如果这个模板能参数化，再回头代入 delta=1 大点，检查它是不是同一模板的放大/变形。

---

## 8. 验证

RED：

```text
uv run pytest tests/test_equationize_closure_first_near_miss.py -q
```

先失败于模块不存在。

GREEN：

```text
uv run pytest tests/test_equationize_closure_first_near_miss.py -q
```

结果：

```text
3 passed
```

代码风格：

```text
uv run ruff check scripts/theory/equationize_closure_first_near_miss.py tests/test_equationize_closure_first_near_miss.py
```

结果：

```text
All checks passed!
```
