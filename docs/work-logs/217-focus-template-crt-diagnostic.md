# wl217 — focus template CRT diagnostic

日期：2026-06-09

## 1. 本轮目标

wl216 修正了 focus template 的模筛边界：

```text
residue mode 只排除真正不能提升为 primitive pair 的余数类。
它允许单个参数为 0 mod M。
```

本轮继续问：

```text
如果 mod 3、5、7 单独都杀不掉，
把它们用 CRT 合并后会不会突然变强？
```

普通话说：

```text
不是重新枚举 mod 105 的 105^9 个点。
只是把互素模数里的“活余数类数量”按 CRT 乘起来，
看小模数合起来是不是已经很像障碍。
```

## 2. 代码变化

新增 count-level CRT helper：

```text
crt_summary(moduli, sample_limit=5, mode="residue")
crt_summary_from_rows(rows, mode="residue")
probe_many(..., include_crt_summary=True)
```

命令行新增：

```text
--crt-summary
```

边界：

```text
只接受两两互素模数。
非互素模数会先拒绝，再做任何枚举。
只支持 mode="residue"。
```

这样可以避免 `crt_summary([3, 9])` 这种输入误跑 `9^9` 枚举。

也避免把 `strict_residue_units` 误当成 CRT 兼容条件：

```text
每个小模数里非零
```

不等于：

```text
合并模数里非零。
```

所以 strict 模式仍可做单模数诊断，但不提供 CRT summary。

## 3. 结果

命令：

```bash
uv run python scripts/theory/probe_focus_template_modular.py 3 5 --sample-limit 0 --crt-summary
```

得到：

```text
combined_modulus          = 15
total_assignments         = 38,443,359,375
side_condition_pass       = 23,887,872,000
shared_constraint_pass    = 432,537,600
closure_pass              = 30,408,704
missing_square_pass       = 16,515,072
missing_square_obstructed = 13,893,632
```

命令：

```bash
uv run python scripts/theory/probe_focus_template_modular.py 3 5 7 --sample-limit 0 --crt-summary
```

得到：

```text
combined_modulus          = 105
total_assignments         = 1,551,328,215,978,515,625
side_condition_pass       = 906,139,986,296,832,000
shared_constraint_pass    = 648,764,876,390,400
closure_pass              = 9,668,508,254,208
missing_square_pass       = 4,908,543,639,552
missing_square_obstructed = 4,759,964,614,656
```

普通话说：

```text
模 105 下 closure 活类还非常多。
missing edge 是平方余数的活类也非常多。
```

所以这条小模数路线目前不像能直接证明 focus template 无解。

## 4. 解释边界

这只是：

```text
count-level CRT diagnostic
```

它不是：

```text
构造整数解；
证明存在整数解；
证明不存在整数解；
证明第四条边真的可以成为平方。
```

更具体地说：

```text
combined_missing_square_pass > 0
```

只能说明：

```text
这些小模数没有排除所有余数类。
```

不能说明：

```text
一定有真正整数解。
```

## 5. 对下一步的影响

focus template 还值得研究，但“靠 mod 3/5/7 小筛一刀切”不太像主路。

更自然的下一步是：

```text
1. 找更结构化的约束，比如共享变量方程里的 gcd / parity / scale 关系。
2. 试较少但更有针对性的素数，而不是盲目堆小模数。
3. 把 focus template 和 A=kB / R_lambda 主线接起来，看能不能降维成曲线问题。
```

普通话总结：

```text
小模数没有给我们一把锁。
但它帮我们排除了一个幻想：
focus bucket 不是那种 mod 105 就会自动死掉的结构。
```

## 6. 验证

```bash
uv run pytest tests/test_probe_focus_template_modular.py -q
```

```text
10 passed
```

```bash
uv run pytest tests/test_probe_focus_template_modular.py tests/test_equationize_closure_first_near_miss.py tests/test_summarize_closure_first_d4_invariants.py tests/test_closure_first_three_square_search.py -q
```

```text
24 passed
```

```bash
uv run ruff check scripts/theory/probe_focus_template_modular.py tests/test_probe_focus_template_modular.py
```

```text
All checks passed
```
