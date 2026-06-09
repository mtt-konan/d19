# wl207 — generated-leg ledger for closure-first near-misses

日期：2026-06-09

## 1. 本轮目标

wl206 已经给每条已通过边加了 Euclid 参数 `(m,n)`。

本轮再补一个更适合推导的字段：

```text
generated_legs
```

它记录：

```text
A/B/N1/N2 中的某个变量，
到底对应 primitive triple 的 odd_leg 还是 even_leg，
以及它应当写成哪条公式。
```

普通话说：

```text
之前知道一条边是 45^2 + 24^2 = 51^2。
现在还知道：

45 = 3*(4^2 - 1^2)
24 = 3*(2*4*1)
```

这样后续不用再人工猜谁是奇腿、谁是偶腿。

---

## 2. 代码变化

修改：

```text
scripts/theory/equationize_closure_first_near_miss.py
tests/test_equationize_closure_first_near_miss.py
```

每条已成平方的边现在输出：

```text
triple.generated_legs.<label> = {
  value,
  primitive_value,
  role,
  formula
}
```

其中 `formula` 只有两种：

```text
scale*(m^2-n^2)
scale*(2*m*n)
```

这不是新筛子，也不改变搜索结果，只是把已有勾股边翻译成可联立的方程账本。

---

## 3. 小样本账本

样本：

```text
(A,B,N1,N2) = (7,45,24,28)
relation = sum=A+B
closure: N1+N2 = A+B = 52
missing edge: A-N2
```

三条已通过边现在可写成：

| edge | scale | Euclid | generated legs |
|---|---:|---|---|
| `A-N1` | 1 | `m=4,n=3` | `A=1*(m^2-n^2)`, `N1=1*(2mn)` |
| `B-N1` | 3 | `m=4,n=1` | `B=3*(m^2-n^2)`, `N1=3*(2mn)` |
| `B-N2` | 1 | `m=7,n=2` | `B=1*(m^2-n^2)`, `N2=1*(2mn)` |

代回具体数：

```text
A  = 4^2 - 3^2        = 7
N1 = 2*4*3            = 24

B  = 3*(4^2 - 1^2)    = 45
N1 = 3*(2*4*1)        = 24

B  = 7^2 - 2^2        = 45
N2 = 2*7*2            = 28
```

失败边：

```text
A^2 + N2^2 = 7^2 + 28^2 = 833
29^2 = 841
signed_delta = -8
```

普通话说：

```text
这个 near-miss 的关键不是“三条边各自很巧”。
更关键的是它们共享变量：

N1 同时被两组三元组生成；
B  同时被两组三元组生成；
closure 又要求 N1+N2=A+B。

后续如果要找理论障碍，应当从这些共享变量入手。
```

---

## 4. 可能的下一步

对 `(7,45,24,28)` 这类 `sum=A+B`、缺 `A-N2` 的形状，可以尝试写一般模板：

```text
A  = u*(p^2-q^2)
N1 = u*(2pq)

B  = v*(r^2-s^2)
N1 = v*(2rs)

B  = w*(x^2-y^2)
N2 = w*(2xy)

N1 + N2 = A + B
```

再问：

```text
A^2 + N2^2 是否可能也是平方？
```

这里有两个自然攻击点：

```text
共享变量 N1、B 可能给出递降；
第四条边可能有平方剩余障碍。
```

---

## 5. 验证

已运行：

```text
uv run pytest tests/test_equationize_closure_first_near_miss.py tests/test_closure_first_three_square_search.py -q
```

结果：

```text
9 passed
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

## 6. 边界

可以说：

```text
near-miss 方程化现在能显示变量级的 Euclid 生成关系。
这使“把三条过边联立”变得更直接。
```

不能说：

```text
这已经证明了 closure-first near-miss 永远不能补齐第四条边。
```

原因：

```text
本轮仍是账本工具和样本模板。
真正证明还需要把共享变量方程变成递降、模障碍或参数族排除。
```
