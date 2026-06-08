# wl121 — `sum=A+B` 四斜率模型的 squareclass 阻碍扫描

日期：2026-06-09

## 1. 本轮问题

wl120 把 `sum=A+B` 分支换成了四斜率模型：

```text
x = r/λ
y = s/λ
λ = 1/(x+y-1)
r = λx
s = λy
```

真实条件不是只看 closure，而是四个数都必须是勾股斜率：

```text
x, y, λx, λy
```

也就是说：

```text
z 是勾股斜率
<=> z^2 + 1 是有理平方
```

本轮做的事情很小：不证明全局，只把假候选“死在哪里”记录清楚。

普通话说：

```text
先挑两个已经能成直角三角形的 x,y。
closure 自动算出 λ。
然后看乘上 λ 后的两个新数，还能不能继续成直角三角形。
```

如果不能，就记录 `z^2+1` 差哪个 squareclass。

---

## 2. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增 dataclass：

```text
LegRatioSquareclass
SumAbSlopeObstruction
```

新增 API：

```text
pythagorean_leg_ratios(max_m)
leg_ratio_squareclass(z)
sum_ab_slope_obstruction(x, y)
```

含义：

```text
pythagorean_leg_ratios(max_m)
```

用欧几里得参数 `m,n` 生成一批 primitive 勾股斜率。注意这个 bound 是 `m` 的 bound，不是分子、分母或斜边的 bound。

```text
leg_ratio_squareclass(z)
```

计算 `z^2+1` 的有理 squareclass。如果 squareclass 是 `1`，说明它是有理平方；否则说明它卡在哪些素因子上。

```text
sum_ab_slope_obstruction(x, y)
```

对同一个 closure 候选输出四项：

```text
x
y
r = λx
s = λy
```

各自的 squareclass。

这只是诊断工具，不是高速筛，也不是证明器。

---

## 3. 最小样例

取：

```text
x = 3/4
y = 4/3
```

它们本身都是勾股斜率：

```text
(3/4)^2 + 1 = 25/16 = (5/4)^2
(4/3)^2 + 1 = 25/9  = (5/3)^2
```

closure 给出：

```text
λ = 1/(x+y-1) = 12/13
r = λx = 9/13
s = λy = 16/13
```

但：

```text
r^2+1 = (9/13)^2 + 1 = 250/169
s^2+1 = (16/13)^2 + 1 = 425/169
```

对应 squareclass：

```text
r: 10
s: 17
```

所以这个候选满足 closure，也满足 `x,y` 两个斜率条件，但不满足真实 `R_λ` membership。

这正是 wl119 之后要避免的坑：不要只看被压扁后的弱条件，要检查四个单项。

---

## 4. bounded scan

扫描方式：

```text
slopes = pythagorean_leg_ratios(max_m)
枚举 x<=y
要求 x+y-1>0
令 λ=1/(x+y-1)
检查 x,y,λx,λy
```

结果：

| max_m | slopes | candidates | true hits | 两边缩放都失败 | 只 r 失败 | 只 s 失败 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 12 | 68 | 0 | 67 | 0 | 1 |
| 10 | 44 | 833 | 0 | 829 | 1 | 3 |
| 15 | 94 | 3,735 | 0 | 3,729 | 3 | 3 |
| 20 | 172 | 12,486 | 0 | 12,474 | 3 | 9 |
| 30 | 372 | 58,113 | 0 | 58,090 | 4 | 19 |
| 40 | 662 | 183,506 | 0 | 183,465 | 14 | 27 |

这不是证明。

它只说明在这个 bounded 斜率池里没有小 true hit，而且绝大多数假候选死在同一个地方：

```text
x,y 已经是勾股斜率，
但 λx, λy 同时不再是勾股斜率。
```

这个现象值得理论化。

---

## 5. 代表假候选

### 两边都失败

```text
x = 3/4
y = 3/4
λ = 2
r = 3/2
s = 3/2
squareclass: x=1, y=1, r=13, s=13
```

```text
x = 3/4
y = 4/3
λ = 12/13
r = 9/13
s = 16/13
squareclass: x=1, y=1, r=10, s=17
```

```text
x = 3/4
y = 5/12
λ = 6
r = 9/2
s = 5/2
squareclass: x=1, y=1, r=85, s=29
```

### 只一边失败

这些样例重要，因为它们说明障碍不是简单的“如果一个坏，另一个自动坏”。

只 `r` 失败：

```text
x = 3/4
y = 240/161
λ = 644/799
r = 483/799
s = 960/799
squareclass: x=1, y=1, r=871690, s=1
```

```text
x = 21/20
y = 12/35
λ = 28/11
r = 147/55
s = 48/55
squareclass: x=1, y=1, r=24634, s=1
```

只 `s` 失败：

```text
x = 4/3
y = 304/297
λ = 297/403
r = 396/403
s = 304/403
squareclass: x=1, y=1, r=1, s=10193
```

```text
x = 15/8
y = 7/24
λ = 6/7
r = 45/28
s = 1/4
squareclass: x=1, y=1, r=1, s=17
```

这些“一边通过、一边失败”的点，后续很适合拿来拆条件。

---

## 6. 目前能说什么

可以安全说：

```text
四斜率模型比弱 p 模型更接近原问题。
bounded scan 到 max_m=40 没有 true hit。
假候选主要失败在 λx, λy 的勾股斜率条件。
```

不能说：

```text
sum=A+B 分支已证明无解。
所有 λ 都被排除了。
finite scan 说明 theorem 成立。
```

这里最容易犯的错，还是把有限实验当证明。

---

## 7. 下一步理论切口

### 切口 A：参数化四斜率条件

写：

```text
x = (u^2-v^2)/(2uv)
y = (p^2-q^2)/(2pq)
λ = 1/(x+y-1)
```

然后要求：

```text
λx 是勾股斜率
λy 是勾股斜率
```

目标不是先扫，而是把这两个要求变成显式方程或显式 squareclass 条件。

### 切口 B：研究“一边通过”的样例

一边通过说明：

```text
x,y 是勾股斜率
λx 是勾股斜率
```

并不自动推出：

```text
λy 是勾股斜率
```

这可以作为中间曲线来研究：

```text
三项通过时，第四项为什么失败？
```

这跟 closure-first near-miss 的“三条边对，第四条差一点”很像。

### 切口 C：不要只追 `p≡3 mod 4`

样例里很多失败 squareclass 不是单纯的 `3 mod 4` 素数障碍。

例如：

```text
r=9/13 失败于 squareclass 10 = 2*5
s=16/13 失败于 squareclass 17
```

所以如果走模障碍，可能需要更宽的 squareclass / Hilbert-symbol 语言，而不是只盯 `p≡3 mod 4`。

---

## 8. 验证

新增测试：

```text
test_pythagorean_leg_ratios_generate_bounded_slope_pool
test_leg_ratio_squareclass_explains_pythagorean_failure
test_sum_ab_slope_obstruction_identifies_scaled_leg_failures
```

运行：

```text
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
14 passed
```

本轮没有改动全局结论，只补了 `sum=A+B` 四斜率模型的诊断层。
