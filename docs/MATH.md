# 数学参考文档

这份文档只保留项目数学骨架。当前证明主线见
[PROJECT_STATUS.md](./PROJECT_STATUS.md) 和
[CLOSURE_QUOTIENT_MAINLINE.md](./CLOSURE_QUOTIENT_MAINLINE.md)。

## 1. Harborth 问题

Harborth 猜想：平面内不存在一点到单位正方形四个顶点的距离全为有理数。

单位正方形顶点取

```text
A=(0,0), B=(1,0), C=(1,1), D=(0,1)
```

点 `P=(x,y)` 到四顶点距离平方为

```text
dA^2 = x^2 + y^2
dB^2 = (x-1)^2 + y^2
dC^2 = (x-1)^2 + (y-1)^2
dD^2 = x^2 + (y-1)^2
```

已知三顶点有理距离点有无穷多个；四顶点有理距离点尚未找到，也尚未被全局证明不存在。

## 2. 三顶点参数化

若 `dA` 有理，可用本原勾股三元组 `(p,q,r)` 和有理比例 `k=a/b` 写

```text
x = ap/(br)
y = aq/(br)
p^2 + q^2 = r^2
gcd(p,q)=1
```

于是

```text
dA = a/b
```

其余三个距离化为整数完全平方判断：

```text
tB = (ar - bp)^2 + (bq)^2
tD = (ar - bq)^2 + (bp)^2
tC = (ar - b(p+q))^2 + (b(p-q))^2
```

即

```text
dB rational <=> tB is square
dD rational <=> tD is square
dC rational <=> tC is square
```

工程上全部用整数 `isqrt` 判断。

## 3. D4 对称

正方形有 8 个 D4 对称。若一个点满足三顶点有理距离，其 D4 像也满足同类条件。

常用去重方式：

```text
canonical_xy(x,y) = min(D4 orbit of (x,y))
```

轨道大小可能为 `8,4,2,1`，分别对应一般位置、落在对称轴、落在多个对称轴、顶点等特殊情形。

## 4. Chain 化简

内部四顶点反例通分后可转成正整数 chain：

```text
a^2+b^2 = square
b^2+c^2 = square
c^2+d^2 = square
d^2+a^2 = square
a+c = b+d
```

注意：`a+c=b+d` 是内部点的和闭合。全平面还要考虑差闭合；完整语言是 GEN-CLOSURE：

```text
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}
```

用两条本源三元组确定

```text
A = q1 q2
B = p1 p2
N = p2(p1-q1) + q1 q2
```

则合法后续三元组要求

```text
A^2 + N^2 = square
B^2 + N^2 = square
```

也就是 `(A,B)` 的 concordant `N`。这把原来的四元组搜索压成了“找同时和 A、B 成勾股的 N”。

## 5. Concordant 椭圆曲线

给定 `A != B`，concordant 问题是求

```text
N^2 + A^2 = S^2
N^2 + B^2 = T^2
```

令

```text
X = N^2
Y = N*S*T
```

得到椭圆曲线

```text
E_{A,B}: Y^2 = X(X+A^2)(X+B^2)
```

重要警告：曲线上 `X=N^2` 的点只说明

```text
(N^2+A^2)(N^2+B^2)
```

是平方，不自动说明两个因子分别是平方。因此从曲线点回到 concordant `N` 时必须再做整数平方检查。

generic torsion 结构为

```text
Z/2Z x Z/4Z
```

其中 2-torsion 的 `X` 坐标是 `0,-A^2,-B^2`，4-torsion 出现在 `X=+-AB`。

## 6. Closure Quotient

旧 `E_{A,B}` 忘掉闭合腿。closure quotient 把

```text
M = c - N
c in {A+B, |A-B|}
```

放回对象中。四条商曲线为

```text
AA: y^2 = (N^2+A^2)(M^2+A^2)
BB: y^2 = (N^2+B^2)(M^2+B^2)
AB: y^2 = (N^2+A^2)(M^2+B^2)
BA: y^2 = (N^2+B^2)(M^2+A^2)
```

当前严格可用判据是：

```text
AA/BB rank=0 + torsion pullback
```

它能列尽对应四次曲线的仿射有理点。当前已认证行只回拉到中点，随后由 Yang Ji 中线定理排除。`AB/BA` 有万能点，不能作为 rank-zero 刀。

细节见 [CLOSURE_QUOTIENT_MAINLINE.md](./CLOSURE_QUOTIENT_MAINLINE.md)。

## 7. 模定理与 gcd 警告

若 `gcd(A,B)=1` 且 `N` 是 concordant 值，则

```text
12 | N
```

证明只用平方数模 `3` 和模 `8`。非互素情形需用

```text
g = gcd(A,B)
```

修正：

```text
3 not divide g => 3 | N
4 not divide g => 4 | N
```

因此把搜索限制到 `gcd(A,B)=1` 不是 WLOG。整体最小反例只保证四个量共同互素，不保证腿对 `(A,B)` 互素。非互素腿正是旧筛法的主要盲区。

## 8. 当前数学瓶颈

项目现在不缺样本，缺的是能跨 ratio family 生效的证明。当前主线瓶颈是：

```text
AA/BB rank-zero family theorem
  via local image + dyadic condition + Selmer dimension bound
```

若 global Selmer dimension bound 做不出来，继续增加 certificate count、required count 或局部 package 数，都只是材料堆积，不是 Harborth 全局证明。
