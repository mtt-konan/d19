# wl129 — `sum=A+B` three-pass Möbius model

日期：2026-06-09

## 1. 本轮问题

wl122 把 `sum=A+B` 的 near-miss 层拆出来：

```text
x, y, λx, λy
```

四项里有三项是勾股斜率，第四项失败。

这轮不扩大搜索。目标是把“三项通过、一项失败”写成更像方程的形式。

普通话说：

```text
不是再数有多少个差一点；
而是问：三条边一旦给定，第四条是不是已经被公式锁死？
```

答案是：在 `sum=A+B` 斜率坐标里，是的。

---

## 2. 方程

从 wl120：

```text
r = λx
s = λy
r+s = λ+1
```

如果我们选中已经通过的两项：

```text
x
r = λx
```

那么：

```text
λ = r/x
```

closure 强制：

```text
λx + λy = λ + 1
```

代入 `λ=r/x`：

```text
r + (r/x)y = r/x + 1
```

解出：

```text
y = 1 - x + x/r
```

于是第四项：

```text
s = λy = 1 - r + r/x
```

所以三通过 near-miss 可以看成一个 Möbius 模型：

```text
输入: x, r
输出: y = 1 - x + x/r
     s = 1 - r + r/x
```

如果：

```text
x, r, y 都是勾股斜率
s 不是勾股斜率
```

就得到 `x,r,y` 三通过、`s` 失败的 near-miss。

交换角色可以得到另一边失败的同类模型。

---

## 3. 固定样例

wl122 的标准样例：

```text
x = 15/8
y = 7/24
λ = 6/7
r = 45/28
s = 1/4
```

用本轮公式只输入：

```text
x = 15/8
r = 45/28
```

得到：

```text
λ = r/x = 6/7
y = 1 - x + x/r = 7/24
s = 1 - r + r/x = 1/4
```

squareclass：

```text
x: 1
r: 1
y: 1
s: 17
```

这正是三通过 near-miss。

---

## 4. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增 dataclass：

```text
SumAbThreePassMobiusModel
```

新增 API：

```text
sum_ab_three_pass_mobius_model(slope, scaled_term)
```

返回：

```text
lambda_ratio
slope
other_slope
scaled_term
failed_scaled_term
四项 squareclass
```

并有三个布尔属性：

```text
closes_sum_ab
three_terms_are_pythagorean
failed_term_is_pythagorean
```

---

## 5. 新增测试

文件：

```text
tests/test_rational_ratio.py
```

新增：

```text
test_sum_ab_three_pass_mobius_model_reconstructs_missing_term
```

测试固定：

```text
sum_ab_three_pass_mobius_model(15/8, 45/28)
```

必须重建：

```text
λ = 6/7
y = 7/24
s = 1/4
failed squareclass = 17
```

TDD 红灯时，失败原因是函数尚不存在。

---

## 6. 能说什么，不能说什么

可以说：

```text
sum=A+B 的三通过 near-miss 已经有一个二变量 Möbius 方程模型。
给定 x 和 r=λx 后，y 和 s 被 closure 唯一决定。
```

不能说：

```text
三通过 near-miss 已经证明不能升级成四通过。
sum=A+B 分支已关闭。
所有 near-miss 都由这个方向的 x,r 参数解释。
```

这轮只是把 near-miss 从“扫描结果”推进到“方程对象”。

---

## 7. 下一步

最自然的理论问题变成：

```text
找正有理 x,r，使得
x, r, y=1-x+x/r 都是勾股斜率。
问 s=1-r+r/x 什么时候也能是勾股斜率？
```

如果能证明：

```text
x, r, y 勾股
=> s 的 squareclass 永远非 1
```

就能关闭 `sum=A+B` 的一个三通过入口。

更现实的下一小步：

```text
把 x 和 r 都用 Euclid 参数表示，
把 y 是勾股斜率改写成一个显式四变量曲线。
```

这会把 wl122 的 near-miss 方程化继续往前推。

---

## 8. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
20 passed
All checks passed
```
