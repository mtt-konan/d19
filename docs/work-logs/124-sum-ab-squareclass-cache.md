# wl124 — `sum=A+B` squareclass 局部缓存

日期：2026-06-09

## 1. 本轮问题

wl123 做 ratio-shadow orbit 时，`max_m=40` 统计要一分钟级别。

慢点不在 closure 本身，而在这里：

```text
leg_ratio_squareclass(z)
```

它会分解：

```text
z^2 + 1
```

同一个斜率 `z` 会在许多 pair 里反复出现。之前每次都重新 `factorint`，属于重复劳动。

普通话说：

```text
不是数学又变难了，
是我们每次都在重复算同一杯咖啡豆。
```

---

## 2. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增内部 helper：

```text
_cached_leg_ratio_squareclass(ratio, squareclass_cache)
_sum_ab_slope_obstruction_with_squareclass_cache(...)
```

`scan_sum_ab_slope_obstructions(...)` 现在在一次扫描内部维护：

```text
squareclass_cache: dict[Fraction, LegRatioSquareclass]
```

这样同一个 ratio 在同一扫描中只算一次 squareclass。

外部 API 不变：

```text
sum_ab_slope_obstruction(x, y)
scan_sum_ab_slope_obstructions(slopes, pass_count=None)
```

---

## 3. 回归测试

新增测试：

```text
test_scan_sum_ab_slope_obstructions_reuses_squareclass_diagnostics
```

测试做法：

```text
monkeypatch leg_ratio_squareclass
记录每个 ratio 被请求几次
运行 scan_sum_ab_slope_obstructions
确认 max(calls.values()) == 1
```

这不是测时间，而是测行为：

```text
同一个 ratio 在一次扫描内不会重复分解。
```

---

## 4. 结果是否改变

没有改变。

缓存后重新跑 wl123 的 orbit 统计：

| max_m | slopes | three-pass near-miss | ratio-shadow orbits | orbit size 分布 | seconds |
| ---: | ---: | ---: | ---: | --- | ---: |
| 20 | 172 | 12 | 9 | `{1: 6, 2: 3}` | 1.523 |
| 30 | 372 | 23 | 16 | `{1: 9, 2: 7}` | 10.186 |
| 40 | 662 | 41 | 29 | `{1: 17, 2: 12}` | 40.903 |

关键数字仍是：

```text
max_m=40:
three-pass near-miss = 41
ratio-shadow orbits = 29
```

所以这只是工程加速，不是新的数学结论。

---

## 5. 加速效果和限制

上一轮 `max_m=40` 的统计约一分钟多，这轮约 40.9 秒。

它有帮助，但不是终点。

原因：

```text
x,y 的 squareclass 会大量复用；
但 r=λx, s=λy 往往是新 ratio；
这些新 ratio 仍然需要 factorint。
```

所以后续若想继续提速，可能要做两件事：

```text
1. 把 cache 提升到更长生命周期，比如跨统计复用；
2. 先用更便宜的平方判定/模筛过滤，再做完整 factorint。
```

但要小心：

```text
便宜筛只能当 prefilter；
不能把“不通过某个实验筛”写成证明。
```

---

## 6. 下一步

### A. 研究 singleton

现在性能足够支撑 `max_m=40` 的反复检查，可以转向 wl123 留下的 17 个 singleton。

问题：

```text
这些 singleton 是 bound 太小，还是 ratio-shadow key 太弱？
```

下一轮可以列出 singleton，并尝试找它们在更高 `max_m` 的 mate。

### B. 更强缓存

如果继续往 `max_m>40` 推，应考虑：

```text
scan 级别 cache
plus 可选外部 cache
```

例如让调用者传入：

```text
squareclass_cache={}
```

这样多个统计之间也能复用。

### C. 便宜平方类 prefilter

现在 `factorint` 是完整分解。

后续可以先做：

```text
is_rational_square(z^2+1)
```

如果已经是平方，就不用 factorint；只有失败项需要完整 squareclass。

不过这会改变诊断路径，必须 TDD。

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
19 passed
```

本轮只做工程安全加速，没有改变任何 theorem / conjecture 状态。
