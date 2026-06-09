# wl134 — `sum=A+B` Euclid orientation equations

日期：2026-06-09

## 1. 本轮问题

wl133 已经把 `sum=A+B` 三通过 near-miss 写成未约分平方方程：

```text
(bc - ac + ad)^2 + (bc)^2 = Q^2
(ad - ac + bc)^2 + (ad)^2 = H^2
```

其中：

```text
x = a/b
r = c/d
```

这轮向 Euclid 参数再推进一步。

普通话说：

```text
现在不只说 x=15/8、r=45/28。
而是说 15/8 来自 (m,n)=(4,1) 的某条勾股腿，
45/28 来自 (u,v)=(7,2) 的某条勾股腿。

同一组 (m,n)、(u,v) 有 4 种腿的方向选择：
odd/odd, odd/even, even/odd, even/even。
这轮把 4 种都列成整数平方方程。
```

---

## 2. 新增模型

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增：

```text
SumAbEuclidOrientationEquation
sum_ab_euclid_orientation_equations(...)
```

输出每个 orientation case 的：

```text
slope_orientation
scaled_term_orientation
slope_terms
scaled_term_terms
other_slope_polynomial_equation
failed_polynomial_equation
```

其中 square equation 格式仍是：

```text
(unreduced_numerator, unreduced_denominator, hypotenuse_or_none)
```

---

## 3. 固定样例

输入：

```text
slope_m=4, slope_n=1
scaled_term_m=7, scaled_term_n=2
```

四种输出：

```text
odd/odd:
  slope_terms=(15, 8)
  scaled_term_terms=(45, 28)
  other=(105, 360, 375)
  failed=(105, 420, None)

odd/even:
  slope_terms=(15, 8)
  scaled_term_terms=(28, 45)
  other=(479, 224, None)
  failed=(479, 675, None)

even/odd:
  slope_terms=(8, 15)
  scaled_term_terms=(45, 28)
  other=(539, 675, None)
  failed=(539, 224, None)

even/even:
  slope_terms=(8, 15)
  scaled_term_terms=(28, 45)
  other=(556, 420, None)
  failed=(556, 360, None)
```

可以看到，wl133 的三通过样例正是 `odd/odd`：

```text
other=(105,360,375) 通过
failed=(105,420,None) 失败
```

---

## 4. 为什么这一步有用

这个 helper 把下一步理论问题变成：

```text
对任意 m>n>0, u>v>0，
四种 orientation 下，
研究这两个平方方程何时同时成立。
```

也就是从：

```text
扫到很多 near-miss
```

推进到：

```text
直接研究四参数整数方程
```

这更适合做：

```text
模筛
因式分解
squareclass 固定
无限递降
特殊比例 A=kB 的切片分析
```

---

## 5. 能说什么，不能说什么

可以说：

```text
sum=A+B 分支现在有四种 Euclid orientation 的方程入口。
后续可以系统检查每个 orientation 的模条件和因式结构。
```

不能说：

```text
四种 orientation 已经证明不可能。
odd/odd 的 failed 项永远不是平方。
sum=A+B 分支已关闭。
```

这仍然只是 equationization，不是 proof。

---

## 6. 下一步

建议下一步不要先全量展开巨型多项式。

更稳的路线是：

```text
1. 对四种 orientation 分别做小模数 residue table。
2. 先问：other 方程成立时，failed 方程是否被某些模数强制失败。
3. 如果小模数不够，再展开因式结构或 squareclass。
```

普通话说：

```text
先别一口吃掉四参数方程。
先看“第三条刚好通过”会不会自动把第四条卡在非平方余数里。
```

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_euclid_orientation_equations_expand_four_cases -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
All checks passed
```
