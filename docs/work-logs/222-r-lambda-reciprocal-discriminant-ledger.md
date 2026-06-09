# wl222 — `R_lambda` reciprocal discriminant ledger

日期：2026-06-09

## 1. 本轮目标

wl220 已经把 full-plane reciprocal / mirror 分支分成四条关系：

```text
sum=A+B
sum=|A-B|
diff=A+B
diff=|A-B|
```

wl221 又把每个 reciprocal root 的 squareclass 记了下来。

本轮继续把还没完全写清楚的两条判别式分支单独摊开：

```text
sum=|A-B|
diff=A+B
```

普通话说：

```text
前两条是“直接碰到 1”的门，
后两条是“有根但还得看平方类”的门。
```

## 2. 新增 helper

新增：

```text
reciprocal_closure_discriminant_ledger(lambda_ratio, relation)
```

返回：

```text
ReciprocalClosureDiscriminantLedger
```

记录：

```text
lambda_numerator
lambda_denominator
target
discriminant
discriminant_numerator
discriminant_denominator
discriminant_is_square
discriminant_squareclass
discriminant_integer_squareclass
roots
true_roots
branch_closed
```

其中 `roots` 复用 wl221 的 root-level squareclass 账本：

```text
ReciprocalClosureSquareclassRoot
```

## 3. 只给两条门开账

这个 helper 只定义给：

```text
sum=|A-B|
diff=A+B
```

因为它们才是需要判别式的两条 reciprocal 分支。

对应公式：

```text
sum=|A-B|:
  target = |lambda-1|
  discriminant = target^2 - 4lambda

diff=A+B:
  target = lambda + 1
  discriminant = target^2 + 4lambda
```

前两条 forced-root 分支仍然留给 wl220：

```text
sum=A+B
diff=|A-B|
```

## 4. 样本

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from fractions import Fraction
from rational_distance.concordant.rational_ratio import reciprocal_closure_discriminant_ledger

for lam, relation in [
    (Fraction(6), "sum=|A-B|"),
    (Fraction(3, 2), "diff=A+B"),
]:
    ledger = reciprocal_closure_discriminant_ledger(lam, relation)
    print("lambda", lam, "relation", relation)
    print(" target", ledger.target)
    print(" discriminant", ledger.discriminant)
    print(" is_square", ledger.discriminant_is_square)
    print(" squareclass", ledger.discriminant_squareclass)
    print(" roots", [(row.r, row.unit_squareclass, row.lambda_squareclass, row.true_member) for row in ledger.roots])
    print(" true_roots", ledger.true_roots)
    print(" branch_closed", ledger.branch_closed)
PY
```

结果：

```text
lambda 6 relation sum=|A-B|
 lambda_numerator 6
 lambda_denominator 1
 target 5
 discriminant 1
 discriminant_numerator 1
 discriminant_denominator 1
 is_square True
 squareclass 1
 integer_squareclass 1
 roots [(2, 5, 10, False), (3, 10, 5, False)]
 true_roots ()
 branch_closed True

lambda 3/2 relation diff=A+B
 lambda_numerator 3
 lambda_denominator 2
 target 5/2
 discriminant 49/4
 discriminant_numerator 49
 discriminant_denominator 4
 is_square True
 squareclass 1
 integer_squareclass 1
 roots [(3, 10, 5, False)]
 true_roots ()
 branch_closed True
```

普通话说：

```text
这两条判别式门，样本里都能开出有理根，
但根都不是 R_lambda 真成员。
```

## 5. 失败机制

这轮最有用的不是“又多了一个 ledger”，而是把失败方式写清楚了：

```text
sum=|A-B| 的根 2/3 互换出 (5,10)/(10,5)
diff=A+B 的根 3 也是 (10,5)
```

现在还能顺手把分子分母记下来，方便后面写整数版 proof note：

```text
lambda = a/b
discriminant = m/n
```

而不是每次都手动把 Fraction 还原成整数形式。

也就是：

```text
unit_squareclass
lambda_squareclass
```

总是卡在非平凡平方类上。

普通话说：

```text
不是单纯“没有根”，
而是“有根，但平方类不对”。
```

## 6. 对证明的影响

现在 reciprocal / mirror 分支可以再分一层：

```text
forced-root-1 branches:
  sum=A+B
  diff=|A-B|

discriminant branches:
  sum=|A-B|
  diff=A+B
```

后两条的证明目标现在更具体了：

```text
先有判别式平方；
再有 roots 的 unit_squareclass / lambda_squareclass；
最后还要排除 true_roots。
```

这还不是定理，但已经不是“看图猜门”了。

## 7. 解释边界

可以说：

```text
判别式 reciprocal 分支现在有 root-level squareclass ledger。
样本失败机制已经能直接读出来。
```

不能说：

```text
sum=|A-B| 和 diff=A+B 已经对所有 lambda 全局关闭。
```

因为还没有把 squareclass 非平凡性对所有 lambda 推出来。

## 8. 下一步

下一步可以专门做 `sum=|A-B|` 的符号化：

```text
r+s = |lambda-1|
rs = lambda
```

若 `lambda > 1`，就是：

```text
r+s = lambda-1
```

于是：

```text
(lambda-1)^2 - 4lambda
```

必须是平方。

然后要继续问：

```text
这些根能不能同时让 r^2+1 和 r^2+lambda^2 都是平方？
```

普通话总结：

```text
这轮不是证明完成，
而是把“有根但不真成员”的那两条门，
变成了下一篇 proof note 可以直接拿去算的代数对象。
```

## 9. 验证

```bash
uv run pytest tests/test_rational_ratio.py tests/test_fixed_ratio_exact.py tests/test_scan_fixed_ratio_exact.py -q
```

```text
59 passed
```

```bash
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

```text
All checks passed
```
