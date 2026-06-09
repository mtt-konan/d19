# wl201 — centerline terminology and proof-status lock

日期：2026-06-09

## 1. 为什么要写这篇

用户指出一个关键混淆：

```text
正方形几何中心线不是已经被 Yang Ji 论文证明过了吗？
```

是的。

后续文档里凡是写“centerline 还没关闭”，必须先问它说的是哪一层。

普通话说：

```text
几何中线已经关了。
仓库里最近没补完的是 R_lambda 变量里的本地翻译和假阳性账本。
不能把“缺本地翻译”说成“几何中线还开放”。
```

---

## 2. 同一条几何中线，几套变量语言

### 2.1 几何中心线

这是正方形坐标系里的直线条件：

```text
点在正方形的一条中线上。
```

在 d19 变量里常见成：

```text
A = B
```

或由坐标轴交换得到：

```text
N1 = N2
```

用 closure 语言写时，还会出现：

```text
N1 = N2 = n
a + b = 2n
```

或外侧版本：

```text
N1 = N2 = n
|a - b| = 2n
```

这些不是新的“中心线型”条件。它们就是几何中线，只是换了配对方式。

这就是 Yang Ji 的中线 special case 覆盖的对象。当前项目应把它视为：

```text
理论上已关闭。
```

还缺的不是结论，而是本地翻译笔记：

```text
把 Yang Ji 的中线递降证明改写成 A,B,N1,N2 语言。
```

### 2.2 `R_lambda` 里的 centerline 写法

最近 wl188 到 wl200 说的 centerline，多数是这个代数分支：

```text
sum = A + B
r = s
r + s = lambda + 1
```

所以：

```text
r = s = (lambda + 1) / 2
```

它在代码里对应：

```text
sum_ab_centerline_equations(lambda_ratio)
sum_ab_centerline_remaining_quartic(parameter)
sum_ab_centerline_quartic_pari_diagnostics()
```

这一层是在 `R_lambda` product/closure 账本里解释假阳性：

```text
r=s 会让两个坏平方类自己乘自己，
所以 product-square 看起来通过。
```

它仍然来自几何中线，不是第三条新线。

区别只在证明状态：

```text
几何结论已经由 Yang Ji 关闭。
R_lambda 账本还需要把这个结论翻译成本地变量，
并解释为什么 r=s 会制造 product-square 假阳性。
```

---

## 3. 正确状态

可以说：

```text
几何中线 A=B / N1=N2 已由 Yang Ji 关闭。
a+b=2n / |a-b|=2n 是同一几何中线的 closure 写法。
R_lambda centerline 是这条几何中线在归一化变量里的 r=s 写法。
wl188-wl200 在补本地代数说明和 product-square 假阳性解释。
PARI rank 0 诊断只服务于本地自足证明，不改变 Yang Ji 已关闭的结论。
```

不能说：

```text
Yang Ji 没有关掉中心线。
几何中心线仍然开放。
a+b=2n 只是“中心线型”，不是真几何中线。
PARI rank 0 诊断已经等于严格证明。
wl188-wl200 推翻或替代了 Yang Ji 的中线证明。
```

普通话总结：

```text
Yang Ji 已经关了几何门。
R_lambda 工作是在给同一扇门写仓库变量版说明书。
```

---

## 4. 为什么还值得保留 wl188-wl200

如果几何中线已经关闭，为什么还要看 `R_lambda` centerline？

原因有三个。

第一，它能防止误读扫描结果：

```text
product-square hit 很多来自 r=s。
这批不是真 R_lambda 成员，只是平方类自乘的假象。
```

第二，它给固定比例路线做样板：

```text
A = B
```

推广成：

```text
A = kB
```

时，我们仍然需要把几何线条件翻译成平方方程、参数、模条件或椭圆曲线。

第三，它能训练主线 `R_lambda` 的证明方式：

```text
把 closure 条件先降维。
再把剩余条件写成曲线。
最后用递降、rank 0、torsion pullback 或模障碍列尽。
```

这正是主目标：

```text
若 r,s in R_lambda 且 full-plane closure，
是否必须 s = lambda / r？
```

的低维试验场。

---

## 5. 当前缺口

几何层面的缺口：

```text
缺一篇本地 proof note。
内容是把 Yang Ji 的中线定理翻译成 A=B / N1=N2，
并说明 a+b=2n / |a-b|=2n 是同一分支的 closure 写法。
```

代数层面的缺口：

```text
wl200 只拿到 PARI 的 rank 0 椭圆曲线诊断。
还没有写出 quartic <-> Weierstrass 的显式双有理映射。
```

所以代数 `R_lambda centerline` 的自足证明还不能写成定理。正确标签仍是：

```text
needs-birational-pullback
```

---

## 6. 后续怎么走

短期最稳的顺序：

```text
1. 写 center-line impossibility proof note。
   目标不是新证明，而是把 Yang Ji 中线结论翻译成 A,B,N1,N2 和 a+b=2n。

2. 给 wl188-wl200 的代数 centerline 保留 diagnostic 标签。
   不把有限搜索、CRT live class 或 PARI rank 0 直接当证明。

3. 继续攻 A=kB。
   先做整数 k、小素数 n=k±1、模条件覆盖。

4. 回到 R_lambda 主线。
   重点证明 true closure 是否强迫 s=lambda/r。
```

普通话说：

```text
中线本身不是新战场。
它现在的价值是做翻译模板，
然后把这个模板推到 A=kB 和 R_lambda。
```

---

## 7. 对旧 worklog 的读法

读到旧文档里的：

```text
centerline 还没关闭
centerline 分支就可以真正关掉
```

请按下面方式理解：

```text
这通常指 R_lambda 的 r=s 代数分支还缺自足证明。
不是说 Yang Ji 的几何中线结论仍然开放。
a+b=2n 这类 closure 写法也属于几何中线。
```

这条术语锁以后优先级高于旧 worklog 的随手说法。

---

## 8. 验证

本轮只改文档，没有跑数学代码。

检查项：

```text
git status --short
```

提交前应只看到本 worklog 和少量术语提醒改动。
