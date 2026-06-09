# wl212 — focus sample equation network

日期：2026-06-09

## 1. 本轮目标

wl211 把第一 shared-role 桶的 `sum=A+B` 子桶导出后，最强入口是：

```text
(A,B,N1,N2) = (7,45,24,28)
relation = sum=A+B
missing = A-N2
```

本轮把它从“JSON 账本”再翻成一个可直接读的方程网络：

```text
shared equations
closure equation
missing square question
```

普通话说：

```text
之前我们知道三条边各自是勾股。
现在要把它写成：

哪两个变量被重复生成？
closure 怎么接上？
最后缺的那条边到底问什么平方问题？
```

---

## 2. 代码变化

修改：

```text
scripts/theory/equationize_closure_first_near_miss.py
tests/test_equationize_closure_first_near_miss.py
```

`equationize_sample(...)` 新增：

```text
equation_network
```

字段包括：

```text
shared_equations
closure_equation
missing_square_questions
```

这不是新筛子，也不做证明。

它只是把已有 Euclid 参数和 shared-variable ledger 翻译成方程形式。

---

## 3. 小样本网络

样本：

```text
(A,B,N1,N2) = (7,45,24,28)
relation = sum=A+B
```

共享变量：

```text
B = 45 = 3*(4^2-1^2) = 1*(7^2-2^2)
```

```text
N1 = 24 = 1*(2*4*3) = 3*(2*4*1)
```

closure：

```text
N1 + N2 = A + B = 52
```

缺边问题：

```text
A^2 + N2^2 = 7^2 + 28^2 = 833
29^2 = 841
signed_delta = -8
```

普通话说：

```text
这个 focus 样本现在已经不是“三条边通过，一条边失败”的描述。
它是一个小网络：

B  是两个 odd-leg 生成式的同一个值；
N1 是两个 even-leg 生成式的同一个值；
closure 再把 N2 和 A 接进来；
最后只剩 A-N2 是否能成平方。
```

---

## 4. 下一步怎么证

对这个 focus 子桶，建议先别从四条边同时展开，而是从两个共享变量开始：

```text
B  = v*(r^2-s^2) = w*(x^2-y^2)
N1 = u*(2pq)     = v*(2rs)
```

再加：

```text
N1 + N2 = A + B
```

最后问：

```text
A^2 + N2^2 是否能为平方？
```

可能攻击点：

```text
同一个 B 有两种 odd-leg 生成方式，可能给递降；
同一个 N1 有两种 even-leg 生成方式，可能给因子分配限制；
closure 把 N2 固定后，A^2+N2^2 可能出现平方剩余障碍。
```

---

## 5. 边界

可以说：

```text
focus 样本已经被整理成可直接代数操作的方程网络。
```

不能说：

```text
这个网络已经说明第四条边不可能成平方。
```

原因：

```text
本轮只是翻译账本。
还没有做消元、递降、模检验或一般参数证明。
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
  scripts/theory/summarize_closure_first_d4_invariants.py \
  tests/test_equationize_closure_first_near_miss.py \
  tests/test_summarize_closure_first_d4_invariants.py
```

结果：

```text
All checks passed
```
