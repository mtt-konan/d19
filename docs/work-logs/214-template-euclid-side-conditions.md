# wl214 — Euclid side conditions for focus templates

日期：2026-06-09

## 1. 本轮目标

wl213 已经把 focus 样本提升成符号模板。

本轮补上模板的必要边界：

```text
Euclid side conditions
```

普通话说：

```text
p,q,r,s,x,y 不是随便取的整数。
它们必须是 primitive 勾股三元组的 Euclid 参数。
```

如果不写这些条件，后续证明会在一个太大的假空间里推导，容易走歪。

---

## 2. 代码变化

修改：

```text
scripts/theory/equationize_closure_first_near_miss.py
tests/test_equationize_closure_first_near_miss.py
```

`template_constraints.passed_edge_templates[]` 现在新增：

```text
side_conditions
```

每组 Euclid 参数都会列出：

```text
m > n > 0
gcd(m,n) = 1
m,n opposite parity
scale > 0
```

并给出本样本赋值是否满足。

---

## 3. 小样本 side conditions

`A-N1`：

```text
A  = u*(p^2-q^2)
N1 = u*(2*p*q)

u=1, p=4, q=3

p > q > 0                  true
gcd(p,q) = 1               true
p and q opposite parity    true
u > 0                      true
```

`B-N1`：

```text
B  = v*(r^2-s^2)
N1 = v*(2*r*s)

v=3, r=4, s=1

r > s > 0                  true
gcd(r,s) = 1               true
r and s opposite parity    true
v > 0                      true
```

`B-N2`：

```text
B  = w*(x^2-y^2)
N2 = w*(2*x*y)

w=1, x=7, y=2

x > y > 0                  true
gcd(x,y) = 1               true
x and y opposite parity    true
w > 0                      true
```

---

## 4. 对证明的意义

可以从模板出发：

```text
B  = v*(r^2-s^2) = w*(x^2-y^2)
N1 = u*(2*p*q)   = v*(2*r*s)
N1 + N2 = A + B
A^2 + N2^2 = square?
```

但每组参数还必须满足：

```text
gcd(p,q)=gcd(r,s)=gcd(x,y)=1
p,q / r,s / x,y 奇偶相反
p>q>0, r>s>0, x>y>0
u,v,w > 0
```

普通话说：

```text
这些条件是“证明时能用的力”。
比如互素和奇偶条件经常能给出模 2、模 4、因子分配或递降限制。
```

---

## 5. 边界

可以说：

```text
focus 模板现在带有 primitive Euclid 参数的必要 side conditions。
```

不能说：

```text
side conditions 已经排除了 focus 桶。
```

原因：

```text
本轮只是补齐约束。
还没有对这些约束做消元、递降或模分析。
```

---

## 6. 验证

已运行：

```text
uv run pytest \
  tests/test_equationize_closure_first_near_miss.py \
  tests/test_summarize_closure_first_d4_invariants.py \
  tests/test_closure_first_three_square_search.py -q
```

结果：

```text
14 passed
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
