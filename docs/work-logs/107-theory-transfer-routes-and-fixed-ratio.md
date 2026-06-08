# wl107 — 类似问题的证明套路与固定比例路线备忘

日期：2026-06-08

本 wl 记录一次理论方向讨论。问题是：

```text
Yang Ji 只能证明中线、边线、对角线等特殊位置无解。
类似数学问题通常怎样从这些低维分支往外推进？
普通意义上的极限能不能用？
对 d19 后续最值得实现/证明的路线是什么？
```

结论先写在前面：

```text
普通实数极限不是主路。
可用的是数论版的“极限”：无限递降、p-adic/模极限、高度/Chabauty/Mordell-Weil sieve、Brauer-Manin。
当前最划算的可执行方向是推广中心线证明，先攻 A = kB 的整数固定比例分支。
```

---

## 1. 为什么普通极限不够

如果只在实数坐标里看，near-miss 可以无限接近平方，但这不能推出存在精确命中，也不能推出永远不能命中。

原因很朴素：

```text
有理数本身很密。
勾股条件也能产生大量近似。
“差 1”“差 8”“差很小”只是实数距离近，不是数论上可整除或可下降。
```

所以 closure-first 的 `3/4` near-miss 图和 delta 统计可以当线索，但不能当证明。要变成证明，必须把“差一点”翻译成下面某种硬结构：

```text
同余类永远避开 0
假设命中会产生更小命中
命中点落在一条可列尽有理点的曲线/曲面上
局部处处可解但全局不解，需要 Brauer-Manin / Sha 类型障碍
```

---

## 2. 类似问题常用的证明形态

### 2.1 特殊线 + 无限递降

代表：

```text
Yang Ji, "Several special cases of a square problem", arXiv:2105.05250
https://arxiv.org/abs/2105.05250
```

他证明点在正方形中线、边线、对角线等特殊位置时，不可能到四个顶点距离全为有理数。证明风格是：

```text
几何条件降成两个勾股条件
清分母成整数
用勾股参数化
把假设解变成更小解
无限递降，矛盾
```

对 d19 的直接作用：

```text
A = B     -> 竖直中线
N1 = N2   -> 水平中线
```

这两条分支可以视为理论关闭，但仓库还需要一篇本地 proof note，把 Yang Ji 的中线证明翻译成我们的 `A,B,N1,N2` 语言。

### 2.2 固定比例切片

Yang Ji 还有一个更一般的特殊情形：

```text
正方形边长 = n * 点到某条边的距离
且 n 和 n^2 + 4 都是素数
```

则无解。

这和用户提出的 `A = kB` 直接相连。

如果点在两条竖边之间：

```text
side = A + B = (k + 1)B
```

对应 Yang Ji 的参数：

```text
n = k + 1
```

如果点在外侧，且 `k > 1`：

```text
side = |A - B| = (k - 1)B
```

对应：

```text
n = k - 1
```

所以 Yang Ji 已经覆盖一部分整数 `k`：

```text
inside:  k + 1 和 (k + 1)^2 + 4 都是素数
outside: k - 1 和 (k - 1)^2 + 4 都是素数
```

没有覆盖的 `k` 不是自动可行，只是需要新证明。复合 `n` 时，原证明里的因子分裂可能失败，这正是后续可以攻的地方。

### 2.3 椭圆曲线 / 高亏格曲线列尽有理点

代表：

```text
Bremner-Ulas 2016, "Points at rational distances from the vertices of certain geometric objects"
https://arxiv.org/abs/1502.07312
```

常见做法：

```text
把几何条件转成椭圆曲线或高亏格曲线上的有理点
用 rank、Selmer、Chabauty、Mordell-Weil sieve 列尽或排除点
```

这和 d19 已有路线一致：

```text
固定 (A,B) 后看 concordant N
closure 条件再切出更薄的子问题
```

风险也一致：这类方法通常很强，但证明成本高，需要 Sage/Magma/PARI 级工具，且每个切片要小心证明“列尽”。

### 2.4 代数曲线上的 rational-distance set

代表：

```text
Solymosi-de Zeeuw, Erdos-Ulam rational distance 相关工作
https://arxiv.org/abs/0806.3095
```

哲学上有用的点：

```text
能承载很多有理距离点的代数曲线很特殊。
如果反例存在，它大概率不在随机位置，而在某个隐藏代数结构里。
```

这不能直接证明 Harborth 方形问题，但能指导搜索：不要只看散点图，要找低维结构、重复家族、固定比例、固定同余。

### 2.5 local-global / Brauer-Manin

d19 已经遇到这类味道：

```text
wl100 记录了 residual local-global gap。
一些残余候选在很多模数下都局部可解，但整数 GEN-CLOSURE 仍然失败。
```

这说明单纯加更多模数未必能完成证明。若要理论化这层，可能需要：

```text
Sha / Selmer obstruction
Brauer-Manin obstruction
Chabauty + Mordell-Weil sieve
```

这条路很重，暂时更适合做 hard-case 解释，不适合作为下一步第一选择。

---

## 3. 对 d19 的可执行路线

### Route A: 写中心线 proof note

目标：

```text
把 Yang Ji Theorem 2 改写成 d19 变量。
证明 A = B 和 N1 = N2 不可能。
```

需要覆盖：

```text
点在正方形内部
点在正方形外部
closure 的 sum 分支和 diff 分支
```

建议文件：

```text
docs/explorations/2026-06-07-next-step-hard-layer/center-line-impossibility.md
```

这条路线主要是整理，不是新数学。

### Route B: 推广到 A = kB

目标：

```text
固定整数 k，证明 A = kB 分支无解，或至少证明一大批 k 无解。
```

第一步做一张表：

```text
k
inside n = k + 1
outside n = k - 1
Yang Ji 是否覆盖
n 是否素数
n^2 + 4 是否素数
剩余状态
```

第二步对未覆盖的复合 `n` 拆 Yang Ji 的递降证明，找失败点：

```text
是因为 gcd 分裂不可控？
是因为 primitive triple 参数多了一个公共因子？
是否能加 gcd 条件补救？
是否能分成 n 的素因子逐个下降？
```

这条路线最值得优先做，因为它同时减少变量和扩大已知理论分支。

### Route C: 把 closure-first near-miss 写成方程

当前数据：

```text
max_leg=100000
raw 3/4 near-miss records = 41,736
same coordinate points = 857
D4 point orbits = 480
4/4 hits = 0
```

不要继续只画图。下一步应选一个高重复或小 delta 家族，把它写成整数方程。

优先样本：

```text
delta = 1 样本:
(A,B,N1,N2) = (17745, 53911, 60840, 132496)
relation = |N1 - N2| = A + B
missing = B - N2
```

要问的问题：

```text
三条勾股边 + 一条 full-plane closure 是否强制第四条边落入非平方同余类？
delta = 1 是否来自某个参数族，而不是偶然样本？
能不能从 delta = 1 方程反推无限递降？
```

### Route D: 换 D4 不变量看点

480 个点图没有肉眼规律，但 D4 对称后还可以换变量。

可试变量：

```text
x(1-x)
y(1-y)
x + y
x - y
min(x,1-x)
min(y,1-y)
A+B
|A-B|
N1+N2
|N1-N2|
```

目的不是再画更漂亮的图，而是看：

```text
高 raw_count 轨道是否共享同一个不变量
小 delta 轨道是否落在固定同余类
内部点和外部点是否对应不同 closure relation
```

---

## 4. 建议优先级

下一轮如果走理论：

```text
1. 写 center-line-impossibility proof note。
2. 做 A = kB 小 k 覆盖表。
3. 拆 Yang Ji 的固定 n 证明，标出复合 n 的失败点。
4. 选 delta=1 样本写 mini note，尝试变成参数方程。
```

下一轮如果走实验：

```text
1. 不扩大盲扫。
2. 从 closure-first JSON 里按 D4 orbit raw_count 排序。
3. 对 top orbit 和 delta<=10 orbit 输出不变量表。
4. 用表反哺 Route B / Route C 的证明猜想。
```

当前判断：

```text
A = kB 是最划算的理论入口。
普通极限不值得单独追。
near-miss 数据应该服务于找递降、同余或曲线切片，而不是继续靠视觉观察。
```

---

## 5. 文献入口

```text
Yang Ji, Several special cases of a square problem
https://arxiv.org/abs/2105.05250

Bremner-Ulas, Points at rational distances from the vertices of certain geometric objects
https://arxiv.org/abs/1502.07312

Solymosi-de Zeeuw, On a question of Erdos and Ulam
https://arxiv.org/abs/0806.3095

Bruin-Stoll, The Mordell-Weil sieve: proving non-existence of rational points on curves
https://arxiv.org/abs/0906.1934
```
