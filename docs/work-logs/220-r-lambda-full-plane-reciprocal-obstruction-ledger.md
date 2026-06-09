# wl220 — `R_lambda` full-plane reciprocal obstruction ledger

日期：2026-06-09

## 1. 本轮目标

wl187 已经关闭：

```text
sum=A+B reciprocal / mirror branch
```

但主目标是 full-plane：

```text
r+s     = lambda+1
r+s     = |lambda-1|
|r-s|   = lambda+1
|r-s|   = |lambda-1|
```

本轮补一个 full-plane reciprocal 账本，避免把 sum-only 的结论误当成四关系结论。

普通话说：

```text
镜像分支不只在一条线上出现。
现在把四条线都列出来，看每条线有没有真点残留。
```

## 2. 新增 helper

新增：

```text
full_plane_reciprocal_obstruction(lambda_ratio)
```

返回：

```text
FullPlaneReciprocalObstruction
```

其中每个 relation 对应：

```text
ReciprocalClosureObstruction
```

记录：

```text
roots
true_roots
branch_closed
```

普通话说：

```text
roots 是 reciprocal/mirror 方程给出的候选根。
true_roots 是其中真的属于 R_lambda 的根。
如果 true_roots 为空，这条 reciprocal 分支就关了。
```

## 3. 四关系账本

reciprocal / mirror 条件是：

```text
p = rs = lambda
```

四个 closure relation 给出不同二次方程：

```text
sum=A+B:
  r+s = lambda+1
  roots = {1, lambda}

diff=|A-B|:
  |r-s| = |lambda-1|
  roots = {1, lambda}
```

这两条都直接碰到：

```text
1 notin R_lambda
```

因为：

```text
1^2 + 1 = 2
```

而 2 不是有理平方。

另外两条：

```text
sum=|A-B|:
  r+s = |lambda-1|

diff=A+B:
  |r-s| = lambda+1
```

先看判别式有没有有理平方。
有理根存在时，还要逐个检查是否属于 `R_lambda`。

## 4. 样本诊断

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from fractions import Fraction
from rational_distance.concordant.rational_ratio import full_plane_reciprocal_obstruction

for lam in [Fraction(1), Fraction(3, 4), Fraction(3, 2), Fraction(6), Fraction(7)]:
    summary = full_plane_reciprocal_obstruction(lam)
    print("lambda=", lam, "all_closed=", summary.all_branches_closed)
    for relation, row in summary.by_relation.items():
        print(" ", relation, "roots=", row.roots, "true_roots=", row.true_roots)
PY
```

结果摘要：

```text
lambda = 1      all_closed = True
lambda = 3/4    all_closed = True
lambda = 3/2    all_closed = True
lambda = 6      all_closed = True
lambda = 7      all_closed = True
```

具体例子：

```text
lambda=6
  sum=A+B       roots=(1, 6)      true_roots=()
  sum=|A-B|     roots=(2, 3)      true_roots=()
  diff=A+B      roots=()          true_roots=()
  diff=|A-B|    roots=(1, 6)      true_roots=()
```

普通话说：

```text
这些样本里 reciprocal/mirror 分支都没有真点。
有些关系连有理根都没有；
有些有根，但根不是 R_lambda 成员。
```

## 5. 解释边界

可以说：

```text
现在有 full-plane reciprocal 分支的统一账本。
sum=A+B 和 diff=|A-B| 两条都落到 {1, lambda}，因此有清楚本地障碍。
```

不能说：

```text
四条 full-plane reciprocal 分支已经全部对所有 lambda 证明关闭。
```

原因：

```text
sum=|A-B| 和 diff=A+B 还需要把“有根时也不是真 R_lambda 成员”
写成独立 proof note。
```

## 6. 下一步

下一步可以把 reciprocal 分支正式分成两类：

```text
直接 forced root 1:
  sum=A+B
  diff=|A-B|

判别式分支:
  sum=|A-B|
  diff=A+B
```

对判别式分支，目标是证明：

```text
若 roots rational 且 rs=lambda，
则 roots 不可能同时属于 R_lambda。
```

普通话总结：

```text
这轮没有宣布 reciprocal 全关。
但它把四条 reciprocal 门都编号了；
下一轮可以逐门上锁。
```

## 7. 验证

```bash
uv run pytest tests/test_rational_ratio.py -q
```

```text
49 passed
```

```bash
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

```text
All checks passed
```
