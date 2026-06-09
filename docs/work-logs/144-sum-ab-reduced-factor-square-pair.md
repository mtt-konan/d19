# wl144 — `sum=A+B` reduced factor square-pair diagnostics

日期：2026-06-09

## 1. 本轮问题

wl143 暴露了：

```text
(H-P, H+P)
gcd(H-P, H+P)
reduced factor pair
```

这轮继续推进到最接近标准勾股参数化的一步：

```text
reduced factor pair 是否由两个平方数组成？
```

普通话说：

```text
把共同因子剥掉后，
剩下两块如果互素、乘积又是平方，
那它们很可能就各自是平方。
我们先让代码直接告诉我们是不是这样。
```

---

## 2. 新增属性

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbSameOrientationSharedLegTerms` 新增：

```text
other_reduced_factor_pair_gcd
failed_reduced_factor_pair_gcd
other_reduced_factor_pair_square_roots
failed_reduced_factor_pair_square_roots
other_reduced_factor_pair_is_square_pair
failed_reduced_factor_pair_is_square_pair
```

如果对应方程不通过，则返回：

```text
None
False
```

---

## 3. 固定样例

样例：

```text
N = 105
P = 360
H = 375
```

已有：

```text
(H-P, H+P) = (15,735)
gcd = 15
reduced = (1,49)
```

现在新增：

```text
gcd(1,49) = 1
(1,49) = (1^2, 7^2)
```

所以：

```text
other_reduced_factor_pair_gcd = 1
other_reduced_factor_pair_square_roots = (1,7)
other_reduced_factor_pair_is_square_pair = True
```

failed 项不通过：

```text
failed_reduced_factor_pair_gcd = None
failed_reduced_factor_pair_square_roots = None
failed_reduced_factor_pair_is_square_pair = False
```

---

## 4. 为什么这有用

如果：

```text
H-P = gR
H+P = gS
```

并且：

```text
gcd(R,S)=1
RS 是平方
```

那么通常可推出：

```text
R = r^2
S = s^2
```

然后：

```text
P = (gS - gR) / 2 = g(s^2-r^2)/2
N = g r s
```

普通话说：

```text
这就是从“平方检测”走向“参数化”的桥。
```

---

## 5. 当前能说什么

可以说：

```text
通过的 shared-leg 方程现在能直接显示 reduced pair 是否为平方对。
```

不能说：

```text
same orientation 已关闭。
所有 reduced pair 都会是平方对。
递降已经成立。
```

原因：

```text
这只是对已通过单个方程的诊断；
same orientation 需要两个方程同时通过，才进入真正矛盾或递降。
```

---

## 6. 下一步

下一步建议：

```text
1. 找一个假设 both-pass 的符号框架：
   other reduced pair = (r1^2, s1^2)
   failed reduced pair = (r2^2, s2^2)

2. 分别还原：
   P = bc
   Q = ad

3. 比较同一个 N 的两套参数。
```

普通话说：

```text
现在要做的是：
如果 other 和 failed 都通过，
它们会给同一个 N 生成两套平方因子。
这两套因子能不能同时存在，就是下一步的核心。
```

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_shared_leg_terms_expose_square_difference -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
All checks passed
```
