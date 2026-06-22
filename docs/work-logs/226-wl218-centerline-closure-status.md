# wl226 — wl218 centerline closure status

日期：2026-06-22

## 1. 本轮目标

wl225 发现第 3 步的弱翻译：

```text
A_p square
r^2+lambda^2 square
s^2+lambda^2 square
```

会留下系统性中心线假阳性：

```text
r=s=(lambda+1)/2
```

这轮专门处理这个中心线分支。

普通话说：

```text
估值路线里有一批“看起来过了弱门”的假点。
它们其实都站在正方形中线上。
先把这条中线单独关掉，后面才能专心打非中心线。
```

---

## 2. 结论先说

中心线分支可以作为已关闭分支使用，但要说清楚证据来源：

```text
几何层面：已由 Yang Ji 中线定理关闭。
R_lambda 本地代数层面：已化为 rank-0 quartic/elliptic diagnostics，
但自足 proof note 还缺显式 birational pullback。
```

也就是说：

```text
centerline 不应继续作为 sum=A+B 的开放危险分支。
```

但如果要求完全不引用外部论文，只靠仓库本地代数证明，则仍需补最后一步。

---

## 3. R_lambda 中心线方程

`sum=A+B` 的中心线是：

```text
r=s
r+s=lambda+1
```

所以：

```text
r=s=(lambda+1)/2。
```

真成员要求：

```text
((lambda+1)/2)^2 + 1        是有理平方
((lambda+1)/2)^2 + lambda^2 是有理平方
```

普通话说：

```text
中心线不是二维问题。
lambda 一定，点的位置就被钉死了。
```

---

## 4. 几何证明来源

已有 proof note：

```text
docs/explorations/2026-06-07-next-step-hard-layer/center-line-impossibility.md
```

它引用：

```text
Yang Ji, "Several special cases of a square problem", arXiv:2105.05250
```

其中 Theorem 2 关闭正方形中线，Remark 1 说明 special-case 证明不只限于正方形内部。

d19 翻译是：

```text
lambda = A/B
r = N1/B
s = N2/B
```

中心线：

```text
N1 = N2
N1 + N2 = A + B
```

正好变成：

```text
r=s
r+s=lambda+1
```

因此：

```text
r=s=(lambda+1)/2
```

就是 Yang Ji 已经排除的几何中线。

普通话说：

```text
这不是“像中线”。
它就是中线换了变量名。
```

---

## 5. 本地 quartic 账本

如果不引用 Yang Ji，而想在 `R_lambda` 变量里自足证明，可以先参数化第一条平方：

```text
center^2 + 1 是平方
```

令参数为 `t`，得到：

```text
center = 2t/(1-t^2)
lambda = (t^2+4t-1)/(1-t^2)
```

第二条平方变成：

```text
Y^2 = Q(t)
Q(t)=t^4+8t^3+18t^2-8t+1
```

一个有用恒等式是：

```text
Q(t) = (t^2+4t-1)^2 + (2t)^2。
```

如果 `t=0`，则：

```text
center=0
lambda=-1
```

不在本问题的正有理 `lambda` 与正 `r` 范围内。

所以本地代数目标是：

```text
证明 Y^2=Q(t) 的有理点只有 (t,Y)=(0,±1)
```

或至少证明没有能产生：

```text
lambda>0, center>0
```

的有理点。

---

## 6. PARI 诊断

当前 helper：

```text
sum_ab_centerline_quartic_pari_diagnostics()
```

给出：

```text
ellfromeqn(Y^2-Q(t)) = [0,18,0,-68,56]
```

即：

```text
E: Y^2 = X^3 + 18X^2 - 68X + 56
```

PARI 结果：

```text
ellrank(E) = [0,0,0,[]]
elltors(E) = [4,[4],[[-2,16]]]
ellratpoints(E,1000) = [(-2,16), (-2,-16), (2,0)]
```

对原 quartic：

```text
hyperellratpoints(Q,10000) = [(0,1),(0,-1)]
```

普通话说：

```text
椭圆曲线那边是 rank 0，只有 torsion。
原四次曲线高度 10000 也只看到退化点。
```

但纪律上仍要说：

```text
这还不是完整本地证明。
```

因为还没有把 `ellfromeqn` 的双有理映射和 torsion 回拉逐点写出来。

---

## 7. 当前可用规则

后续处理 wl218 `sum=A+B` 时可以使用：

```text
若 r=s 且 r,s in R_lambda 且 r+s=lambda+1，
则矛盾。
```

证据引用优先级：

```text
1. Yang Ji Theorem 2 + Remark 1 + d19 center-line translation note。
2. 本地 quartic/PARI 诊断作为独立复核和未来自足证明入口。
```

所以在 valuation 路线中，中心线假阳性应被归类为：

```text
weak-product artifact, already geometrically excluded
```

而不是：

```text
possible true R_lambda closure pair
```

---

## 8. 还不能说什么

不能说：

```text
R_lambda centerline 已有完全自足的仓库内代数证明。
sum=A+B 分支已证明。
倒数定理已证明。
```

原因：

```text
非中心线 true-nonreciprocal 仍未关闭。
本地 quartic 还缺显式 birational pullback。
```

普通话说：

```text
中线可以移出主危险列表。
但整场仗还没打完。
```

---

## 9. 对下一步的影响

wl225 给出的两个下一步里，A 分支现在可以暂时视为完成到“可引用外部定理”的程度。

接下来应回到 non-center：

```text
r != s
r+s=lambda+1
r,s in R_lambda
rs != lambda
```

更具体地，攻修正版 valuation 引理：

```text
r != s
r+s=lambda+1
A_p square
r^2+lambda^2 square
s^2+lambda^2 square
centerline excluded
=> A_p 的共同 squareclass 不能非平凡
```

或者继续使用 wl224 的四斜率模型，攻：

```text
same orientation both-pass => P=Q。
```

---

## 10. 验证命令

```bash
PYTHONPATH=src uv run python - <<'PY'
import cypari2
pari = cypari2.Pari()
print(pari('ellfromeqn(y^2-(x^4+8*x^3+18*x^2-8*x+1))'))
print(pari('E=ellinit([0,18,0,-68,56]); elltors(E)'))
print(pari('E=ellinit([0,18,0,-68,56]); ellratpoints(E,1000)'))
print(pari('hyperellratpoints(x^4+8*x^3+18*x^2-8*x+1,10000)'))
PY
```

当前输出：

```text
[0,18,0,-68,56]
[4,[4],[[-2,16]]]
[[-2,16],[-2,-16],[2,0]]
[[0,1],[0,-1]]
```

常规验证：

```bash
uv run pytest tests/test_rational_ratio.py -q
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```
