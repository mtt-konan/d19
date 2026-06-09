# wl208 — shared-variable ledger for closure-first near-misses

日期：2026-06-09

## 1. 本轮目标

wl207 已经能把每条已通过边写成：

```text
变量 = scale * Euclid 公式
```

本轮再自动提取：

```text
哪些变量被多条已通过边同时生成？
```

普通话说：

```text
如果 B 同时出现在 B-N1 和 B-N2 两条勾股边里，
那 B 就不是孤立数字。
它是一条“连接两组三元组”的绳子。
```

这种共享变量是后续找递降、平方剩余障碍、参数联立的入口。

---

## 2. 代码变化

修改：

```text
scripts/theory/equationize_closure_first_near_miss.py
tests/test_equationize_closure_first_near_miss.py
```

`equationize_sample(...)` 现在新增顶层字段：

```text
shared_variables
```

它只收集已经成平方的边。

每个变量如果只出现一次，就不列出；出现两次或更多，才列出它在哪些 edge 中出现，以及对应：

```text
edge
value
scale
euclid m,n
role
formula
```

这不是新筛子，只是把已有账本中“变量重复出现”的结构自动标出来。

---

## 3. 小样本结果

样本：

```text
(A,B,N1,N2) = (7,45,24,28)
relation = sum=A+B
closure: N1+N2 = A+B = 52
missing edge: A-N2
```

自动提取出的共享变量是：

```text
B
N1
```

具体等式：

```text
B = 45
  = 3*(4^2 - 1^2)
  = 1*(7^2 - 2^2)
```

```text
N1 = 24
   = 1*(2*4*3)
   = 3*(2*4*1)
```

普通话说：

```text
这个 near-miss 不是三条边各自巧合。
它有两个公共接口：

B  把 B-N1 和 B-N2 接起来；
N1 把 A-N1 和 B-N1 接起来。

再加上 closure:

N1 + N2 = A + B

整个样本已经像一个小方程网络。
```

---

## 4. 对下一步的意义

对这个 `sum=A+B`、缺 `A-N2` 的形状，最小模板可以从共享变量开始写：

```text
B  = v*(r^2-s^2) = w*(x^2-y^2)
N1 = u*(2pq)     = v*(2rs)
N1 + N2 = A + B
```

而不是从四条边全部展开。

这样做的好处是：

```text
先抓住变量复用处，方程数更少。
如果存在递降，往往会从“同一个数有两种生成方式”冒出来。
如果存在模障碍，也更容易先对 B 或 N1 下手。
```

可能的下一步：

```text
把所有低 delta / 高 raw_count 样本的 shared_variables 统计出来，
看共享变量的 role 模式是否集中。
```

比如先问：

```text
是不是常见 near-miss 都有一个变量两次作为 odd_leg，
另一个变量两次作为 even_leg？
```

如果是，这比散点图更接近理论入口。

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

还用 CLI 打印过小样本 `shared_variables`：

```text
uv run python scripts/theory/equationize_closure_first_near_miss.py \
  --sample '7,45,24,28,sum=A+B'
```

---

## 6. 边界

可以说：

```text
工具现在能自动指出 near-miss 的共享变量接口。
这把“三条勾股边”变成了“小方程网络”。
```

不能说：

```text
共享变量接口已经证明第四条边不可能补齐。
```

原因：

```text
本轮仍是结构提取。
证明还需要把这些共享变量等式变成递降、模障碍或一般参数排除。
```
