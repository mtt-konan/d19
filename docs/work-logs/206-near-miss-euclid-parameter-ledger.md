# wl206 — near-miss Euclid parameter ledger

日期：2026-06-09

## 1. 本轮目标

wl205 已经把 closure-first near-miss 拆成：

```text
closure 方程
四条边的平方状态
已通过边的 primitive Pythagorean triple
失败边离最近平方差多少
```

本轮再往下拆一层：

```text
每条已通过边的 primitive triple 来自哪组 Euclid 参数 (m,n)
```

普通话说：

```text
不要只说 7-24-25 是勾股数。
还要写出它是 m=4,n=3 生成的：

7  = 4^2 - 3^2
24 = 2*4*3
25 = 4^2 + 3^2
```

这样后续才能把 near-miss 从“样本账本”推向“参数方程”。

---

## 2. 代码变化

修改：

```text
scripts/theory/equationize_closure_first_near_miss.py
```

每条已成平方的边现在输出：

```text
triple.euclid = {
  m,
  n,
  odd_leg,
  even_leg
}
```

脚本会从 primitive triple 反推出：

```text
odd_leg  = m^2 - n^2
even_leg = 2mn
hyp      = m^2 + n^2
```

并做自检。如果 primitive triple 不能还原成标准 Euclid 形式，脚本会报错，而不是静默产出假参数。

---

## 3. 样本确认

`(A,B,N1,N2)=(7,45,24,28)`，`relation=sum=A+B`：

| edge | primitive | scale | Euclid |
|---|---|---:|---|
| `A-N1` | `(7,24,25)` | 1 | `m=4,n=3` |
| `B-N1` | `(8,15,17)` | 3 | `m=4,n=1` |
| `B-N2` | `(28,45,53)` | 1 | `m=7,n=2` |

对应失败边仍是：

```text
A-N2:
7^2 + 28^2 = 833
29^2       = 841
signed_delta = -8
```

普通话说：

```text
这个样本现在可以写成三组 (m,n) 互相咬合：

(4,3), scale 1
(4,1), scale 3
(7,2), scale 1

下一步不是再看图，而是问：
为什么这三组参数同时满足 closure 后，
第四条边只能落在平方附近，不能正好落上去？
```

---

## 4. 验证

已运行：

```text
uv run pytest tests/test_equationize_closure_first_near_miss.py -q
```

结果：

```text
3 passed
```

已运行：

```text
uv run ruff check \
  scripts/theory/equationize_closure_first_near_miss.py \
  tests/test_equationize_closure_first_near_miss.py
```

结果：

```text
All checks passed
```

---

## 5. 边界

可以说：

```text
closure-first near-miss 的已通过边，现在能追溯到 Euclid 参数。
这给“把 near-miss 变成方程”提供了更细的变量层。
```

不能说：

```text
Euclid 参数账本已经证明 near-miss 不可能变成 hit。
```

原因：

```text
本轮只是工具层和样本层。
还没有把三组 Euclid 参数联立成一般定理。
```

下一步建议：

```text
优先挑 (7,45,24,28) 这个小样本，
把三条过边的 Euclid 参数写成联立方程，
看 closure N1+N2=A+B 是否强迫第四条边出现固定平方差或模障碍。
```
