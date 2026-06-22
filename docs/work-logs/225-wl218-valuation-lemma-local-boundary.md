# wl225 — wl218 valuation lemma local boundary

日期：2026-06-22

## 1. 本轮目标

继续推进倒数定理的第一分支：

```text
r,s in R_lambda
r+s = lambda+1
=> rs = lambda
```

用户提出的路线是：

```text
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

并希望用各个 `q = 3 mod 4` 的 valuation 逼出：

```text
p = rs = lambda。
```

这轮专门检查这个 valuation / local 思路的边界。

普通话说：

```text
先别急着写“估值矛盾”。
先问：只看局部平方条件时，危险分支会不会已经被杀光？
如果没杀光，就要知道漏在哪里。
```

---

## 2. 单素数局部平方剩余杀不掉 `p != lambda`

在有限域 `F_l` 上枚举：

```text
lambda != 0
r != 0
s != 0
r+s = lambda+1
```

并要求四个真成员条件在模 `l` 下都是平方剩余：

```text
r^2+1
s^2+1
r^2+lambda^2
s^2+lambda^2
```

然后只看危险类：

```text
rs != lambda mod l
```

小素数结果：

```text
l=5   danger=2
l=11  danger=4
l=13  danger=10
l=17  danger=10
l=19  danger=12
l=29  danger=46
```

例子：

```text
mod 5:
lambda=4, r=2, s=3, rs-lambda=2

mod 11:
lambda=10, r=2, s=9, rs-lambda=8
```

结论：

```text
单个小素数的平方剩余条件不能直接证明 p=lambda。
```

这不是反例；它只是说明局部平方剩余层太弱。

---

## 3. CRT 合并小模数仍有危险活类

继续把多个小素数合并成模数 `M`，要求：

```text
gcd(lambda,r,s,M)=1
四个成员表达式都是平方剩余 mod M
r+s=lambda+1 mod M
rs != lambda mod M
```

结果仍有危险活类：

```text
M=35       danger=6
M=55       danger=8
M=77       danger=12
M=385      danger=24
M=715      danger=80
M=1001     danger=120
M=5005     danger=240
```

例子：

```text
M=385:
lambda=274, r=57, s=218, rs-lambda=217

M=5005:
lambda=274, r=57, s=218, rs-lambda=2142
```

普通话说：

```text
把几个模数拼起来，危险类还是能活。
所以“模平方剩余”本身不是那把最终钥匙。
```

---

## 4. 对第 3 步翻译的修正

用户第 3 步说：

```text
把 "r,s 是真成员" 翻译成 A_p,B_p,
以及 r^2+lambda^2, s^2+lambda^2 全是平方。
```

这还差一点。

原因是：

```text
A_p = (r^2+1)(s^2+1)
B_p = (r^2+lambda^2)(s^2+lambda^2)
```

如果已经单独要求：

```text
r^2+lambda^2
s^2+lambda^2
```

是平方，那么 `B_p` 自动是平方，不再额外提供信息。

但 `A_p` 是平方只说明：

```text
r^2+1 和 s^2+1 在同一个 squareclass
```

不说明它们各自是平方。

所以真成员必须保留为：

```text
A_p 是平方
r^2+1 是平方
s^2+1 是平方
r^2+lambda^2 是平方
s^2+lambda^2 是平方
```

或者更直接：

```text
四个单项都平方。
```

普通话说：

```text
两个数乘起来是平方，只说明它们“坏得一样”。
不说明它们“不坏”。
```

---

## 5. 中心线给出系统性假阳性

精确有理扫描显示，如果只要求：

```text
r+s=lambda+1
p=rs != lambda
A_p=(r^2+1)(s^2+1) 是平方
r^2+lambda^2 是平方
s^2+lambda^2 是平方
```

那么中心线 `r=s` 会留下很多系统性假阳性。

例子：

```text
lambda = 2
r = s = 3/2
p = 9/4 != 2
```

此时：

```text
r^2+lambda^2 = s^2+lambda^2 = 25/4  是平方
r^2+1 = s^2+1 = 13/4               不是平方
A_p = (13/4)^2                     是平方
```

squareclass 写法：

```text
unit squareclasses   = (13,13)
lambda squareclasses = (1,1)
```

更多同类样本：

```text
lambda=3/5,  r=s=4/5,   unit squareclass=(41,41)
lambda=5/19, r=s=12/19, unit squareclass=(505,505)
lambda=4/11, r=s=15/22, unit squareclass=(709,709)
lambda=15,   r=s=8,     unit squareclass=(65,65)
```

结论：

```text
A_p + 两个 lambda 单项平方
仍然不等于真 R_lambda membership。
```

必须额外要求 `r^2+1` 与 `s^2+1` 各自为平方，或先用中心线定理排除这一整族。

---

## 6. 非中心线小扫描

同一个弱条件下，排除 `r=s` 后，小有理网格到 bound 70 没看到幸存者：

```text
non-center hits:
n=20 0
n=30 0
n=40 0
n=50 0
n=70 0
```

这不是证明。

但它提示一个可能的分层：

```text
1. 先单独关闭 centerline。
2. 再在 non-center 情况下尝试证明：
   A_p square + lambda-side 单项 square => unit-side 单项 square 或 p=lambda。
```

不过目前还没有完成这条引理。

---

## 7. 当前判断

可以安全说：

```text
纯局部平方剩余不能直接逼出 p=lambda。
CRT 小模数组合也不能直接杀掉 p!=lambda。
第 3 步的翻译必须保留四个单项平方；只保留 A_p 会留下中心线假阳性。
```

不能说：

```text
valuation 路线失败。
sum=A+B 已证明。
non-center 弱条件已全局无解。
```

更准确的说法是：

```text
valuation 路线需要更强输入：
完整 squareclass / Hilbert-symbol 数据，
或先关闭 centerline 后再攻 non-center。
```

---

## 8. 下一步

下一步建议二选一。

### A. 先关 centerline

证明：

```text
r=s=(lambda+1)/2
r in R_lambda
```

无正有理解。

仓库已有 centerline quartic / PARI diagnostics，下一步要把它整理成自足 proof note，
而不是只引用 rank-zero 诊断。

### B. 攻 non-center valuation 引理

目标改成：

```text
r != s
r+s=lambda+1
A_p square
r^2+lambda^2 square
s^2+lambda^2 square
=> r^2+1 和 s^2+1 不可能同非平凡 squareclass
```

如果这条成立，就能把第 3 步修补回来。

普通话说：

```text
现在不是“估值法没用”，而是“估值法不能只看 A_p 这一层”。
它得带上中心线处理，或者带上完整平方类信息。
```

---

## 9. 探针命令

单素数局部探针：

```bash
PYTHONPATH=src uv run python - <<'PY'
def qr_set(p):
    return {x*x % p for x in range(p)}

def survivors(p):
    qr = qr_set(p)
    rows = []
    for lam in range(1, p):
        for r in range(1, p):
            s = (lam + 1 - r) % p
            if s == 0:
                continue
            vals = (r*r+1, s*s+1, r*r+lam*lam, s*s+lam*lam)
            if all((v % p) in qr for v in vals):
                rows.append((lam, r, s, (r*s-lam) % p))
    return rows

for p in [5, 7, 11, 13, 17, 19]:
    rows = survivors(p)
    danger = [row for row in rows if row[3] != 0]
    print(p, len(rows), len(danger))
PY
```

弱翻译中心线探针：

```bash
PYTHONPATH=src uv run python - <<'PY'
from fractions import Fraction
from math import isqrt
from rational_distance.concordant.rational_ratio import positive_rational_ratios

def is_square(q):
    return q >= 0 and isqrt(q.numerator)**2 == q.numerator and isqrt(q.denominator)**2 == q.denominator

for r in positive_rational_ratios(10, 10):
    s = r
    lam = r + s - 1
    if lam <= 0 or r*s == lam:
        continue
    unit = r*r + 1
    lam_side = r*r + lam*lam
    if is_square(unit*unit) and is_square(lam_side):
        print(lam, r, unit, lam_side)
PY
```
