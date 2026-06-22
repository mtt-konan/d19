# wl270 — wl218 bridge centerline branch restrictions

日期：2026-06-22

## 1. 本轮目标

接 wl269。

wl269 把：

```text
C = (t-u)(t+u)(tu-1)(tu+1)
```

拆成四条 p-adic 管道。自然的下一步是问：

```text
如果真的落在其中一条因子 C_i=0 上，
两个 bridge-square 分子会变成什么？
```

普通话说：

```text
上一轮知道“靠近中线”不是一条线。
这轮先看四条线本身长什么样。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeBridgeCenterlineBranchRestriction
```

新增 helper：

```text
sum_ab_dual_slope_bridge_centerline_branch_restrictions(t)
```

它不调用正参数验证；这里只是在 bridge numerator 多项式层面做代入：

```text
u = t
u = -t
u = 1/t
u = -1/t
```

并记录：

```text
X_bridge_numerator
Y_bridge_numerator
E
```

---

## 3. 四条分支的精确限制

令：

```text
Q(t) = t^4 + 8t^3 + 18t^2 - 8t + 1.
```

### 分支 1: t-u=0

代入 `u=t`：

```text
X = Y = (t-1)^2 (t+1)^2 Q(t)
E = (t-1)(t+1)(t^2+2t-1)
```

这是 centerline-quartic 型。

普通话说：

```text
真正的中心线会回到已有的 Q(t) 中线问题。
```

### 分支 2: t+u=0

代入 `u=-t`：

```text
X = Y = (t-1)^2 (t+1)^2 (t^2+1)^2
E = (t-1)^2 (t+1)^2
```

这是 trivial-square 型。

普通话说：

```text
这条模意义的管道上，bridge 分子自动是显式平方。
所以它不会被一阶 square test 轻易杀掉。
```

### 分支 3: tu-1=0

代入 `u=1/t`：

```text
X = Y = (t-1)^2 (t+1)^2 (t^2+1)^2 / t^4
E = -(t-1)^2 (t+1)^2 / t^2
```

这也是 trivial-square 型。

普通话说：

```text
这条管道和 t+u=0 一样，bridge 分子本身已经是平方形状。
符号会影响平方类，但不会改变 valuation。
```

### 分支 4: tu+1=0

代入 `u=-1/t`：

```text
X = Y = (t-1)^2 (t+1)^2 Q(t) / t^4
E = -(t-1)(t+1)(t^2+2t-1) / t^2
```

这是 centerline-quartic 型。

普通话说：

```text
tu+1=0 是 t-u=0 的倒置/符号版本，
同样回到 Q(t)。
```

---

## 4. 对证明路线的影响

现在 C-near 管道可以分成两类：

```text
centerline-quartic:
  t-u = 0
  tu+1 = 0

trivial-square:
  t+u = 0
  tu-1 = 0
```

这解释了 wl268/wl269 里的现象：

```text
C 被 p 整除时，E 可以是单位。
```

因为在 `t+u=0`、`tu-1=0` 两条管道上，bridge 分子已经是显式平方，
不需要靠 `E=0`。

普通话说：

```text
E=0 只管住一部分门。
另外两条门是“平方条件天然放行”的局部门，必须另找约束。
```

---

## 5. 当前证明状态

可以安全说：

```text
1. 四条 C_i=0 分支的精确限制已明确；
2. 两条回到 centerline quartic；
3. 两条是 trivial-square 型，解释了局部幸存；
4. C-near branch 还没有关闭。
```

不能说：

```text
sum=A+B 已证明。
C-near branch 已证明无解。
全平面倒数定理已证明。
```

---

## 6. 下一步

下一步应该处理 trivial-square 型管道：

```text
u = -t + h
u = 1/t + h
```

把 `X`、`Y`、`E` 展开到一阶/二阶。

普通话说：

```text
这两条线本身不会死。
要看离开这条线一点点时，两个平方条件是否强迫 h 继续更高阶可除，
或者强迫另一个因子一起可除。
```

---

## 7. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_bridge_branch_restrictions_split_quartic_from_square -q
```

结果：

```text
1 passed
```
