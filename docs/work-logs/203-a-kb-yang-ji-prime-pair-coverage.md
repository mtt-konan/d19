# wl203 — `A=kB` Yang Ji prime-pair coverage table

日期：2026-06-09

## 1. 本轮目标

wl202 已经把中心线关成一个本地 proof note。

下一步沿用户说的路线走：

```text
从 A=B 推到 A=kB。
先看整数 k。
先看 Yang Ji fixed-n 条件能覆盖哪些 k。
```

这轮只做覆盖表，不声称证明所有表中分支。

普通话说：

```text
先把地图画出来。
哪些 k 已经像是有现成论文路线，
哪些 k 完全没被那条路线碰到。
```

---

## 2. fixed-ratio 和 fixed-line 的对应

固定：

```text
A = kB
```

把所有长度除以 `B`：

```text
A/B = k
N_i/B = r_i
```

full-plane closure 有四个目标：

```text
r1+r2 = k+1
r1+r2 = k-1       (k>1)
|r1-r2| = k+1
|r1-r2| = k-1     (k>1)
```

几何上，这些分支等价于：

```text
正方形边长 = n * 点到某条边的距离
```

其中：

```text
inside  n = k + 1
outside n = k - 1
```

中心线是：

```text
k = 1
```

已由 wl202 / Yang Ji Theorem 2 关闭。

---

## 3. Yang Ji fixed-n 条件

Yang Ji 论文还声称一个 fixed-n 特殊情形：

```text
如果 n 是素数，且 n^2+4 也是素数，
则 fixed-line 分支无解。
```

但必须保留 wl111 的审查边界：

```text
Yang Ji Theorem 3 不能在 d19 里直接当已审计黑盒。
wl111 找到原文辅助方程的字面反例。
```

所以本 wl 用标签：

```text
paper-claimed prime-pair
```

不用：

```text
proved closed
```

普通话说：

```text
这张表告诉我们“论文路线可能覆盖哪里”，
不告诉我们“仓库已经证明哪里”。
```

---

## 4. prime-pair n

小范围 `n <= 100` 中，同时满足：

```text
n prime
n^2 + 4 prime
```

的 `n` 是：

```text
3, 5, 7, 13, 17, 37, 47, 67, 73, 97
```

于是：

```text
inside  k = n - 1:
2, 4, 6, 12, 16, 36, 46, 66, 72, 96

outside k = n + 1:
4, 6, 8, 14, 18, 38, 48, 68, 74, 98
```

`k=4` 和 `k=6` 同时被 inside/outside 的 paper-claimed 条件碰到：

```text
k=4: inside n=5, outside n=3
k=6: inside n=7, outside n=5
```

---

## 5. `k <= 40` 覆盖表

| k | inside n=k+1 | inside status | outside n=k-1 | outside status |
|---:|---:|---|---:|---|
| 1 | 2 | center-line closed | - | center-line closed |
| 2 | 3 | paper-claimed prime-pair | 1 | open |
| 3 | 4 | open | 2 | open |
| 4 | 5 | paper-claimed prime-pair | 3 | paper-claimed prime-pair |
| 5 | 6 | open | 4 | open |
| 6 | 7 | paper-claimed prime-pair | 5 | paper-claimed prime-pair |
| 7 | 8 | open | 6 | open |
| 8 | 9 | open | 7 | paper-claimed prime-pair |
| 9 | 10 | open | 8 | open |
| 10 | 11 | open | 9 | open |
| 11 | 12 | open | 10 | open |
| 12 | 13 | paper-claimed prime-pair | 11 | open |
| 13 | 14 | open | 12 | open |
| 14 | 15 | open | 13 | paper-claimed prime-pair |
| 15 | 16 | open | 14 | open |
| 16 | 17 | paper-claimed prime-pair | 15 | open |
| 17 | 18 | open | 16 | open |
| 18 | 19 | open | 17 | paper-claimed prime-pair |
| 19 | 20 | open | 18 | open |
| 20 | 21 | open | 19 | open |
| 21 | 22 | open | 20 | open |
| 22 | 23 | open | 21 | open |
| 23 | 24 | open | 22 | open |
| 24 | 25 | open | 23 | open |
| 25 | 26 | open | 24 | open |
| 26 | 27 | open | 25 | open |
| 27 | 28 | open | 26 | open |
| 28 | 29 | open | 27 | open |
| 29 | 30 | open | 28 | open |
| 30 | 31 | open | 29 | open |
| 31 | 32 | open | 30 | open |
| 32 | 33 | open | 31 | open |
| 33 | 34 | open | 32 | open |
| 34 | 35 | open | 33 | open |
| 35 | 36 | open | 34 | open |
| 36 | 37 | paper-claimed prime-pair | 35 | open |
| 37 | 38 | open | 36 | open |
| 38 | 39 | open | 37 | paper-claimed prime-pair |
| 39 | 40 | open | 38 | open |
| 40 | 41 | open | 39 | open |

---

## 6. 这张表说明什么

The table has two messages.

First, the prime-pair condition is sparse. In `k <= 40`, it touches only:

```text
k = 2, 4, 6, 8, 12, 14, 16, 18, 36, 38
```

plus the already closed `k=1`.

Second, most small `k` remain outside that paper-claimed route:

```text
3, 5, 7, 9, 10, 11, 13, 15, 17, 19, ..., 35, 37, 39, 40
```

So even if Yang Ji Theorem 3 were fully audited, it would not close all integer
`k`. It would close a sparse subsequence.

普通话说：

```text
Yang Ji fixed-n 路线有用，
但它不是一把横扫所有整数 k 的刀。
```

---

## 7. 下一步

有两条合理后续。

### A. 审计 Yang Ji fixed-n 证明

目标：

```text
确认 paper-claimed prime-pair 条件到底能不能严格引用。
```

需要处理 wl111 的问题：

```text
(a^2+b^2)^2 + (n a b)^2 = e^2
```

按原文并非无整数解。

如果能找出缺失条件，就能把 `paper-claimed prime-pair` 升级成：

```text
proved by audited Yang Ji fixed-n theorem
```

### B. 对未覆盖小 k 写曲线模型

优先从小 k 开始：

```text
k = 3, 5, 7, 9, 10, 11
```

每个固定 `k` 都转成 fixed-line 方程：

```text
y^2 + 1^2             = square
y^2 + (n±1)^2         = square
(n-y)^2 + 1^2         = square
(n-y)^2 + (n±1)^2     = square
```

再尝试：

```text
参数化第一条勾股条件。
把第二条变成 quartic / elliptic curve。
加入 y -> n-y 的镜像条件。
查 rank 0、torsion pullback、或模障碍。
```

普通话总结：

```text
下一步别再问“所有 A=kB 行不行”。
先把 k=3 或 k=5 打成一条具体曲线。
能拿下一个小 k，就有模板。
```

---

## 8. 验证

本轮只用一个短 Python 脚本生成表格。

命令形状：

```text
python3 - <<'PY'
import math

def is_prime(n):
    ...

for k in range(1, 41):
    inside = k + 1
    outside = k - 1 if k > 1 else None
    ...
PY
```

没有改代码，没有运行测试。
