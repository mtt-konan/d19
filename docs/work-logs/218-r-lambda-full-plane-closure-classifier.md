# wl218 — `R_lambda` full-plane closure classifier

日期：2026-06-09

## 1. 本轮目标

主理论目标是：

```text
若 r,s in R_lambda 且满足 full-plane closure，
是否必须 s = lambda/r？
```

普通话说：

```text
两个点如果都能配上左右两边距离，
并且刚好把正方形闭合，
它们是不是只能是一对镜像点？
```

之前仓库已经有很多 `sum=A+B` 工具。
但 full-plane closure 有四种线性关系：

```text
r+s     = lambda+1
r+s     = |lambda-1|
|r-s|   = lambda+1
|r-s|   = |lambda-1|
```

当 `lambda=1` 时，`|lambda-1|=0`。
旧的 `find_rational_ratio_hits` 不枚举这个 zero target；
新 helper 也保持同一口径，对 `sum=|A-B|` / `diff=|A-B|`
的 zero target 直接拒绝。

所以本轮先补一个不会误把 sum-only 当 full-plane 的分类账本。

## 2. 新增 helper

新增：

```text
full_plane_true_closure_relation(lambda_ratio, r, s, relation)
scan_full_plane_true_closure_relations(...)
```

返回：

```text
FullPlaneTrueClosureRelation
```

它记录：

```text
relation
target
closure_value
closes_relation
closes_sum_ab
closes_sum_diff
closes_diff_ab
closes_diff_diff
r_true_member
s_true_member
both_true_members
reciprocal_pair
centerline
branch
```

其中危险分支是：

```text
true-nonreciprocal
```

普通话说：

```text
这就是“真的闭合、两个点也都是真的 R_lambda 成员，
但不是镜像 reciprocal pair”的坏东西。
```

## 3. 不是 sum-only

测试刻意覆盖：

```text
lambda = 7
r = 2
s = 10
relation = diff=A+B
```

因为：

```text
|10-2| = 8 = lambda+1
```

但：

```text
2+10 != lambda+1
```

所以这个样本能证明新 helper 不是旧 `sum_ab_true_closure_relation`
换了个名字。

## 4. 小池诊断

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from collections import Counter
from fractions import Fraction
from rational_distance.concordant.rational_ratio import scan_full_plane_true_closure_relations

relations = scan_full_plane_true_closure_relations(
    lambda_ratios=(Fraction(1), Fraction(7)),
    max_numerator=10,
    max_denominator=10,
    include_centerline=True,
)
print("count", len(relations))
for key, value in sorted(Counter((item.relation, item.branch) for item in relations).items()):
    print(key, value)
print("danger", [item for item in relations if item.branch == "true-nonreciprocal"])
PY
```

结果：

```text
count 48
('diff=A+B', 'false-residual') 17
('diff=|A-B|', 'false-reciprocal') 1
('diff=|A-B|', 'false-residual') 3
('sum=A+B', 'false-centerline') 2
('sum=A+B', 'false-reciprocal') 1
('sum=A+B', 'false-residual') 18
('sum=|A-B|', 'false-centerline') 1
('sum=|A-B|', 'false-residual') 5
danger []
```

普通话说：

```text
四种 full-plane 关系都能出现。
但这个小池里没有 true-nonreciprocal。
```

## 5. 解释边界

这不是证明。

它只说明：

```text
我们现在有一个统一账本，
能把 full-plane 四关系里的危险分支单独抓出来。
```

不能说：

```text
有限扫描没有 true-nonreciprocal，
所以数学上不存在 true-nonreciprocal。
```

## 6. 下一步

下一步不该只是放大有限扫描。

更有用的是把危险分支写成方程：

```text
r,s in R_lambda
closure relation holds
rs != lambda
```

然后对四种 relation 分别看：

```text
1. product p = rs 的平方条件；
2. 判别式是否强迫某些 squareclass 相等；
3. p != lambda 时是否会落入 centerline / reciprocal / impossible squareclass。
```

普通话总结：

```text
这轮不是拿到证明，
而是把“要证明什么”从 sum-only 升级成 full-plane 版。
后面再攻 reciprocal theorem，就不会打错靶。
```

## 7. 验证

```bash
uv run pytest tests/test_rational_ratio.py -q
```

```text
46 passed
```

```bash
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

```text
All checks passed
```
