# wl135 — `sum=A+B` Euclid residue summaries

日期：2026-06-09

## 1. 本轮问题

wl134 已经把 `sum=A+B` 的 near-miss 方程写成四种 Euclid orientation：

```text
odd/odd
odd/even
even/odd
even/even
```

下一步不是马上展开巨型四参数多项式，而是先问一个更小的问题：

```text
在模 M 下，
如果 other 方程看起来像平方，
failed 方程是否也必须看起来像平方？
```

普通话说：

```text
先用小模数试探：
第三条边已经像平方时，第四条边是不是会被余数条件卡住？
```

---

## 2. 新增模型

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增：

```text
SumAbEuclidResidueSummary
sum_ab_euclid_residue_summaries(modulus=M)
```

这个 helper 枚举：

```text
m,n,u,v mod M
```

并分别统计四种 orientation 下：

```text
total_classes
other_square_classes
failed_square_classes
both_square_classes
other_only_classes
failed_only_classes
neither_square_classes
```

其中：

```text
other_only_classes = other 像平方，但 failed 不像平方的 residue class 数
```

如果：

```text
other_only_classes == 0
```

则记录：

```text
other_square_forces_failed_square = True
```

含义只是：

```text
在这个模数下，other 通过平方余数检查会推出 failed 也通过平方余数检查。
```

这不是说 failed 真的是整数平方。

---

## 3. 重要安全约定

这个 residue helper 故意不加：

```text
m > n
u > v
gcd(m,n)=1
gcd(u,v)=1
奇偶 primitive 条件
分母非零条件
```

原因：

```text
这是一个保守的模诊断。
先看纯 residue 世界有没有必要条件。
不要把搜索筛子误写成证明。
```

后续如果要加 primitive residue 版本，必须另写 helper，并在名字里标清楚。

---

## 4. `mod 8` 结果

新增测试固定 `modulus=8`，结果：

```text
odd/odd:
  total=4096
  other=4096
  failed=4096
  both=4096
  other_only=0
  failed_only=0

odd/even:
  total=4096
  other=4096
  failed=3072
  both=3072
  other_only=1024
  failed_only=0

even/odd:
  total=4096
  other=3072
  failed=4096
  both=3072
  other_only=0
  failed_only=1024

even/even:
  total=4096
  other=4096
  failed=4096
  both=4096
  other_only=0
  failed_only=0
```

普通话解释：

```text
mod 8 对 odd/odd 和 even/even 太弱，完全不卡。

mixed orientation 有方向性：
odd/even 中，other 总像平方，但 failed 有 1024 类不像平方。
even/odd 中，failed 总像平方，但 other 有 1024 类不像平方。
```

这说明小模数确实能看到结构，但 `mod 8` 单独还不能关闭 near-miss。

---

## 5. 能说什么，不能说什么

可以说：

```text
sum=A+B 现在有 residue table 入口。
mod 8 暴露了 mixed orientation 的非对称余数结构。
```

不能说：

```text
mod 8 证明了 failed 永远失败。
四种 orientation 被关闭。
near-miss 已被解释完。
```

---

## 6. 下一步

建议下一步做两个分支：

```text
1. 扫 M in {3,5,7,8,11,13,16,17,19,23,29,31}，
   记录哪些 modulus 对哪些 orientation 有 other_only=0 或 both=0。

2. 加一个条件版 helper：
   在 residue 层加入 primitive/parity/denominator-nonzero 标记，
   但不要替换当前 conservative helper。
```

如果发现某个模数或模数组合让：

```text
other_square_classes > 0
both_square_classes = 0
```

那会是强信号：

```text
other 可以通过，但 failed 被模条件强制失败。
```

如果一直没有这种情况，就说明这条证明可能需要因式分解或递降，而不是简单平方剩余。

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_euclid_residue_summaries_count_square_residue_obstructions -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
All checks passed
```
