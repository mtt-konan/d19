# wl148 — `sum=A+B` P=Q primitive branch

日期：2026-06-09

## 1. 本轮问题

wl147 说明 same orientation 下：

```text
P-Q = ±2(mu+nv)(nu-mv)
```

其中：

```text
P = bc
Q = ad
```

这轮把 `P=Q` 分支写严谨。

普通话说：

```text
如果两个分母真的相等，
它到底是不是同一组 Euclid 参数？
```

---

## 2. 正参数下 P=Q 等价于 nu=mv

same orientation 中：

```text
P-Q = ±2(mu+nv)(nu-mv)
```

因为：

```text
m,n,u,v > 0
```

所以：

```text
mu+nv > 0
```

因此：

```text
P=Q
```

等价于：

```text
nu-mv = 0
```

也就是：

```text
nu = mv
```

---

## 3. primitive 条件下推出同一组参数

假设：

```text
gcd(m,n)=1
gcd(u,v)=1
nu = mv
```

由：

```text
nu = mv
```

因为：

```text
gcd(m,n)=1
```

可得：

```text
m | u
```

所以存在整数 `t`：

```text
u = tm
```

代回：

```text
nu = mv
```

得到：

```text
n(tm) = mv
```

消去正整数 `m`：

```text
v = tn
```

再用：

```text
gcd(u,v)=1
```

得到：

```text
gcd(tm,tn)=t*gcd(m,n)=t=1
```

因此：

```text
t=1
u=m
v=n
```

结论：

```text
primitive positive case 下，P=Q 强制 (u,v)=(m,n)。
```

普通话说：

```text
两个分母相等不是“另一组不同参数”；
在 primitive 情况下就是同一组参数。
```

---

## 4. 几何/比例含义

如果：

```text
(u,v)=(m,n)
```

same orientation 下：

```text
c=a
d=b
```

所以：

```text
r = c/d = a/b = x
```

也就是已知的两个 slope 实际相同。

普通话说：

```text
P=Q 分支不是新的四通过结构。
它退回到同一条勾股斜率重复使用。
```

这和主理论里的镜像/互反目标对齐：

```text
s = lambda/r
```

但注意：

```text
这里还只是 sum=A+B same-orientation 的局部分支。
不能直接当成全局 R_lambda 定理。
```

---

## 5. 能说什么，不能说什么

可以说：

```text
same orientation 的 P=Q 分支在 primitive positive 参数下退化为同一组 Euclid 参数。
```

不能说：

```text
both-pass 会推出 P=Q。
same orientation 已关闭。
sum=A+B 已关闭。
```

本轮只处理：

```text
如果 P=Q，会发生什么。
```

还没有处理：

```text
P != Q
```

也就是：

```text
nu-mv != 0
```

---

## 6. 下一步

现在 same orientation 剩余核心变成：

```text
both-pass 且 nu-mv != 0
```

下一步可以尝试：

```text
1. 假设 both-pass 且 nu-mv != 0。
2. 用 other/failed 两套 (g,r,s) 参数表达 P,Q。
3. 结合 P-Q = ±2(mu+nv)(nu-mv)。
4. 尝试构造更小的 both-pass，走递降。
```

普通话说：

```text
P=Q 分支已经不神秘了。
真正剩下的是 P 不等于 Q 的非退化分支。
```
