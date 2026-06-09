# wl202 — center-line impossibility proof note

日期：2026-06-09

## 1. 本轮目标

wl201 锁定术语：

```text
a+b=2n / |a-b|=2n 不是“像中心线”。
它就是几何中线的 closure 写法。
```

本轮把这个结论落成正式 proof note：

```text
docs/explorations/2026-06-07-next-step-hard-layer/center-line-impossibility.md
```

普通话说：

```text
以后看到 A=B、N1=N2、a+b=2n，
不用再重新问它是不是中心线。
它就是中心线，Yang Ji 已经关掉。
```

---

## 2. 新 proof note 写了什么

proof note 做三件事。

第一，引用 Yang Ji 的已知定理：

```text
Yang Ji, "Several special cases of a square problem", arXiv:2105.05250
```

其中 Theorem 2 处理正方形中线，Remark 1 说明证明不只限于正方形内部。

第二，把 d19 坐标翻译清楚：

```text
P = (u/L, v/L)
A  = |u|
B  = |u-L|
N1 = |v|
N2 = |v-L|
```

如果点在水平中线：

```text
N1 = N2 = n
L = 2n
```

所以 closure 语言就是：

```text
A+B=2n
```

或外侧版本：

```text
|A-B|=2n
```

第三，把 `R_lambda` 写法接上：

```text
lambda = A/B
r = N1/B
s = N2/B
```

于是：

```text
N1=N2, N1+N2=A+B
```

变成：

```text
r=s=(lambda+1)/2
```

---

## 3. 现在可以说什么

可以说：

```text
几何中线分支已关闭。
A=B 和 N1=N2 是同一条中线的轴交换。
a+b=2n / |a-b|=2n 是同一条中线的 closure 写法。
R_lambda 的 r=s centerline 是同一条中线的归一化写法。
```

不能说：

```text
我们已经独立重写完 Yang Ji 的全部 Fermat 递降证明。
A=kB 的 k!=1 分支也因此关闭。
R_lambda 主定理因此关闭。
```

普通话总结：

```text
这次补的是“引用证明 + 本地翻译”。
不是新数学大招。
但它足够让中心线不再占用主线注意力。
```

---

## 4. 对后续路线的影响

中心线现在可以当作固定比例路线的样板：

```text
k=1 已关闭。
下一步看 k!=1。
```

最自然的下一张表：

```text
k
inside n = k + 1
outside n = k - 1
Yang Ji prime-pair condition 是否覆盖
未覆盖的 n 有哪些小素数/模障碍
```

这样推广 Yang Ji 时，不会从空白开始。

---

## 5. 边界

本轮没有关闭：

```text
A=kB, k!=1
一般有理比例 lambda
closure-first 3/4 near-miss
D4 不变量路线
非互素 full-space gap
```

这些仍然属于总目标的开放部分。

---

## 6. 验证

本轮只改文档。

检查：

```text
git diff --check
git status --short
```

没有运行代码测试。
