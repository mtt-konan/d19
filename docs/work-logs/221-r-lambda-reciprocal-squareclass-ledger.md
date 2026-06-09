# wl221 — `R_lambda` reciprocal squareclass ledger

日期：2026-06-09

## 1. 本轮目标

wl220 把 full-plane reciprocal / mirror 分支列成四关系账本。

本轮继续补 root 级 squareclass：

```text
对每个 reciprocal root r，
记录 r^2+1 和 r^2+lambda^2 的 squareclass。
```

普通话说：

```text
上一轮知道哪些根不是真点。
这轮记录它们具体死在哪个平方类上。
```

## 2. 新增 helper

新增：

```text
reciprocal_closure_squareclass_ledger(lambda_ratio, relation)
```

返回：

```text
ReciprocalClosureSquareclassRoot
```

每个 row 记录：

```text
r
relation
unit_value        = r^2 + 1
lambda_value      = r^2 + lambda^2
unit_squareclass
lambda_squareclass
true_member
```

## 3. 样本

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from fractions import Fraction
from rational_distance.concordant.rational_ratio import reciprocal_closure_squareclass_ledger

for lam, relation in [
    (Fraction(6), "sum=|A-B|"),
    (Fraction(3, 2), "diff=A+B"),
    (Fraction(1), "sum=A+B"),
    (Fraction(7), "diff=|A-B|"),
]:
    print("lambda", lam, "relation", relation)
    for row in reciprocal_closure_squareclass_ledger(lam, relation):
        print(" ", row.r, "unit_sc", row.unit_squareclass, "lambda_sc", row.lambda_squareclass, "true", row.true_member)
PY
```

结果：

```text
lambda 6 relation sum=|A-B|
  2 unit_sc 5 lambda_sc 10 true False
  3 unit_sc 10 lambda_sc 5 true False

lambda 3/2 relation diff=A+B
  3 unit_sc 10 lambda_sc 5 true False

lambda 1 relation sum=A+B
  1 unit_sc 2 lambda_sc 2 true False

lambda 7 relation diff=|A-B|
  1 unit_sc 2 lambda_sc 2 true False
  7 unit_sc 2 lambda_sc 2 true False
```

普通话说：

```text
forced root 1 的失败是最干净的：squareclass 是 2。
判别式分支的样本失败是 5/10 互换。
```

## 4. 对证明的影响

现在 reciprocal 分支可以更细地拆成：

```text
forced-root-1 branches:
  sum=A+B
  diff=|A-B|

discriminant branches:
  sum=|A-B|
  diff=A+B
```

前两条的 obstruction 是：

```text
1^2+1 = 2
```

后两条下一步要证明的是：

```text
如果 reciprocal roots 存在，
则至少一个 root 的 unit_squareclass 或 lambda_squareclass 非 1。
```

更强一点的希望是：

```text
判别式分支里两个 squareclass 被迫成非平凡互换，
像样本中的 (5,10) / (10,5)。
```

这还不是定理，只是证明靶子。

## 5. 解释边界

可以说：

```text
reciprocal roots 现在有 root-level squareclass ledger。
样本失败机制已经能直接读出来。
```

不能说：

```text
判别式 reciprocal branches 已经全局证明无真点。
```

因为还没有把 squareclass 非平凡性对所有 `lambda` 推出来。

## 6. 下一步

下一步可以对 `sum=|A-B|` 先做代数化：

```text
r+s = |lambda-1|
rs = lambda
```

设 `lambda > 1`，则：

```text
r+s = lambda-1
```

要有正根，必须：

```text
(lambda-1)^2 - 4lambda 是有理平方。
```

也就是：

```text
lambda^2 - 6lambda + 1 是平方。
```

然后研究 roots 的：

```text
r^2+1
r^2+lambda^2
```

是否可能同时为平方。

普通话总结：

```text
现在不是在扩大扫描，
而是在把“为什么这些根不是真点”
变成下一篇 proof note 可以接手的平方类条件。
```

## 7. 验证

```bash
uv run pytest tests/test_rational_ratio.py tests/test_fixed_ratio_exact.py tests/test_scan_fixed_ratio_exact.py -q
```

```text
57 passed
```

```bash
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

```text
All checks passed
```
