# Closure Quotient Mainline

这份文档只保留当前主线。详细逐轮材料已经进 worklog；这里负责回答：

- closure quotient 到底证明了什么；
- 哪些数字只是统计，不是证明进展；
- 下一步如果继续走 rank-zero Selmer，缺口在哪里。

入口：

- [PROJECT_STATUS.md](./PROJECT_STATUS.md)
- [OPEN_DIRECTIONS.md](./OPEN_DIRECTIONS.md)
- [wl294 closure quotient foundation](./work-logs/294-closure-quotient-foundation-consolidated.md)
- [wl386 rank-zero Selmer package](./work-logs/386-rank-zero-selmer-package-consolidated.md)

## 1. 核心对象

旧 concordant 曲线只问：

```text
N^2 + A^2 = square
N^2 + B^2 = square
```

它会忘掉闭合腿。内部闭合时取

```text
M = A + B - N
```

全平面 GEN-CLOSURE 还需要同时考虑差关系；本质上常数只剩

```text
c_plus  = A + B
c_minus = |A - B|
M = c - N
```

对固定 `c`，四个平方条件是：

```text
NA = N^2 + A^2
NB = N^2 + B^2
MA = M^2 + A^2
MB = M^2 + B^2
```

取两两乘积得到四条 genus-one 商曲线：

```text
AA: y^2 = NA * MA
BB: y^2 = NB * MB
AB: y^2 = NA * MB
BA: y^2 = NB * MA
```

完整闭合点必须落在这四条商曲线上。任何一条商曲线能严格排除非平凡仿射点，就能排除原闭合点。

## 2. 已经严格可用的证书

当前唯一干净证书是：

```text
AA/BB rank = 0
  -> enumerate torsion
  -> pull back to quartic
  -> only midpoint points
  -> Yang Ji midpoint theorem excludes them
```

`AA/BB` 有中点对称。令

```text
t = 2N - c
z = 4y
```

则偶四次为

```text
z^2 = t^4 + p t^2 + q
p = 8L^2 - 2c^2
q = (c^2 + 4L^2)^2
```

其中 `L=A` 对应 `AA`，`L=B` 对应 `BB`。对应椭圆曲线可取：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
X = 2(z + t^2)
V = 2t(X+p)
```

仿射反向回拉：

```text
t = V / (2(X+p))
z = X/2 - t^2
N = (c+t)/2
```

所以只要 `rank_lower=rank_upper=0` 被认证，`E(Q)` 就只剩 torsion；枚举 `elltors(E)` 并回拉即可列尽原四次曲线的仿射有理点。`O` 不给仿射点，`X=-p` 对应四次曲线无穷远点。

当前统计口径：

```text
rank-zero certificate rows = 275
strictly excluded distinct (A,B) candidates = 220
```

这 275 行都只回拉到中点 `N=M=c/2`，没有 full-closed square point。注意：这是严格有限证书，但只覆盖已经认证 rank-zero 的行；它不是全局 Harborth 证明。

## 3. AB/BA 的结论

`AB/BA` 不是 rank-zero 击杀器。它们有结构性万能点，例如在 `c=A+B` 时取

```text
N = A
M = B
y = 2AB
```

于是

```text
(N^2+A^2)(M^2+B^2) = 2A^2 * 2B^2 = (2AB)^2
```

这解释了为什么两批样本里 `AB/BA rank 0 = 0`。以后 `AB/BA` 可以作为结构校验或生成元来源，不要再当 rank-zero 刀。

## 4. 射线账本

商曲线齐次。若 `(A,B,N,y)` 是点，则

```text
(A,B,N,y) -> (kA,kB,kN,k^2 y)
```

保持方程同形。因此证书天然按比例

```text
lambda = A/B
```

生效，而不是只按单个整数 pair 生效。正确账本应该按本原射线 `(a:b)` 建键，记录：

```text
c_plus_cert
c_minus_cert
AA_or_BB
rank_certificate
torsion_pullback_audit
midpoint_exclusion_reference
ray_dead = c_plus_cert and c_minus_cert
```

`c_minus=|A-B|` 是完整射线证书的必要另一半；`lambda=1` 时 `c_minus=0` 退化，需单独走中线定理。

## 5. Selmer Family Route

有限证书只能杀一批 ratio。若想变成证明线，需要把 `AA/BB` 的 rank-zero 现象提升为 family theorem：

```text
local image theorems
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank(E_lambda)=0
```

最近 worklog 的 package 段落是在补这条链的材料。它们的意义是“证明段落更可审阅”，不是“命题已经更接近完成”。真正跨步只看一件事：

```text
能否推出 global Selmer dimension bound
```

当前压缩状态：

- odd-prime formal-lift 段落已经有多份 reviewable package；
- dyadic 分支已经把点级 2-primary compatibility 压到 `(1,1,1)`；
- 剩余核心不是继续采样，而是把点级 compatibility lift 到 Selmer 层；
- 没有 Selmer-layer lift，就没有 rank-zero family theorem。

最近的完整 `d`-坐标主线已经放弃旧 package-`x` 的 `S~` 桥，改走
`C_d` / `M_tail`。`wl489` 只处理一个点级问题：`AA, A=3, B=1` 的
`d=(3,3,1)` 全局点可回拉到 `AA` 四次商上的 `N=4, M=0`，但同一
common source 在 `BB` 侧给出 `(N^2+B^2)(M^2+B^2)=17`，不是平方。
所以这个点不是 AA+BB common-source 闭合点。`wl490` 只把它从当前
obstruction / admissible ledgers 移到“ambient globally soluble but not
AA+BB-admissible”诊断账本，并把下一窄门选为 reusable
ambient-`C_d`-to-AA+BB admissibility filter；这仍不是 Selmer 上界、
rank-zero 结论或 family exclusion。

## 6. 不要再主线化的东西

下面这些不要写成证明进展：

- certificate count / required count 继续增加；
- 更大范围的 pair counting；
- `AB/BA` rank-zero 尝试；
- 单纯 root number 观察；
- 单纯 mod-`p^k` 筛；
- residual two-cover 的 bounded search no-point candidate。

它们可以是诊断或候选材料，但不是全局证明。

## 7. 保留入口

常用脚本：

```text
scripts/theory/rank_mixed_closure_curves.py
scripts/theory/summarize_mixed_closure_results.py
scripts/theory/audit_mixed_closure_rank0_certificates.py
scripts/theory/audit_mixed_closure_even_model_identities.py
```

常用结果：

```text
results/mixed_closure_rank_summary.json
results/mixed_closure_rank0_certificate_audit.json
results/mixed_closure_even_model_identity_audit.json
results/closure_quotient_rank_zero_selmer_packages/
```

## 8. 停止条件

继续这条线的判断标准很简单：

```text
If global Selmer dimension bound appears possible:
    keep formalizing
else:
    stop treating package growth as proof progress
```

当前主线仍值得保留，但它的瓶颈已经很明确：不是数据不够，而是 Selmer 层兼容性还没证明。
