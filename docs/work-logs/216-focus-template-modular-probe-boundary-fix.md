# wl216 — focus template modular probe boundary fix

日期：2026-06-09

## 1. 本轮目标

wl215 的 modular probe 有一个边界问题：

```text
它把正整数参数 u,v,w,p,q,... 在模 M 下不为 0，
当成了 residue side condition。
```

这太强。

普通话说：

```text
一个正整数当然可以 mod 5 等于 0。
所以不能因为某个 residue 是 0，
就说它不可能来自正整数。
```

本轮修正 probe：

```text
默认 mode=residue：只保留真正能投影到 residue 层的 primitive 条件。
额外 mode=strict_residue_units：保留 wl215 的旧强筛，只当诊断对照。
```

---

## 2. 正确边界

primitive 条件：

```text
gcd(m,n)=1
```

投影到模 `M` 后，不是：

```text
m != 0 mod M
n != 0 mod M
```

而是：

```text
gcd(m mod M, n mod M, M) = 1
```

例如：

```text
(m,n) ≡ (0,1) mod 5
```

可以来自互素整数。

但：

```text
(m,n) ≡ (0,0) mod 5
```

不可能来自 `gcd(m,n)=1`。

scale 正性：

```text
u,v,w > 0
```

在纯 residue 层不能推出：

```text
u,v,w != 0 mod M
```

所以默认 residue 模式不再排除 scale 为 0 的 residue。

---

## 3. 代码变化

修改：

```text
scripts/theory/probe_focus_template_modular.py
tests/test_probe_focus_template_modular.py
```

新增：

```text
mode=residue
mode=strict_residue_units
```

默认：

```text
mode=residue
```

含义：

```text
gcd(pair, modulus)=1
偶模数时检查 opposite parity
不强迫 scale residue 非零
不强迫每个 m,n residue 非零
```

旧强筛：

```text
mode=strict_residue_units
```

含义：

```text
u,v,w 非零
m,n 非零
gcd(pair, modulus)=1
偶模数时检查 opposite parity
```

这个模式只用于诊断对照，不能当必要条件。

---

## 4. 修正后运行

已运行：

```text
uv run python scripts/theory/probe_focus_template_modular.py 3 5 7 --sample-limit 1
```

默认 `mode=residue` 结果：

| modulus | side_condition_pass | closure_pass | missing_square_pass | obstructed |
|---:|---:|---:|---:|---:|
| 3 | 13824 | 1024 | 768 | 256 |
| 5 | 1728000 | 29696 | 21504 | 8192 |
| 7 | 37933056 | 317952 | 297216 | 20736 |

已运行旧强筛对照：

```text
uv run python scripts/theory/probe_focus_template_modular.py \
  3 5 --mode strict_residue_units --sample-limit 1
```

结果仍是 wl215 的强筛口径：

| modulus | side_condition_pass | closure_pass | missing_square_pass | obstructed |
|---:|---:|---:|---:|---:|
| 3 | 512 | 128 | 128 | 0 |
| 5 | 262144 | 5120 | 4096 | 1024 |

普通话说：

```text
默认 residue 模式更宽，也更诚实。
它仍然没有被 mod 3/5/7 杀光。
```

---

## 5. 对 wl215 的修正

wl215 的结果不能当作必要 residue 筛。

更准确地说：

```text
wl215 跑的是 strict_residue_units 口径。
它可以当“强筛诊断”，不能当“所有整数解必须满足的 residue 条件”。
```

修正后的结论：

```text
在更诚实的 residue 投影下，
mod 3/5/7 仍有大量 survivor。
```

所以：

```text
单个小模数平方剩余障碍仍然没有直接杀光 focus 模板。
```

---

## 6. 下一步

后续如果继续 residue 路线，建议：

```text
1. 用 mode=residue 做 CRT 合并，而不是 strict_residue_units。
2. 把 strict_residue_units 只作为“强筛对照”。
3. 如果要用正性或 valuation，就必须显式进入 p-adic / exact 参数层。
```

普通话说：

```text
纯 residue 层只能说 residue 能不能活。
正整数大小、scale 是否被 p 整除、valuation 分配，
这些都不是纯 residue 能完整表达的。
```

---

## 7. 验证

已运行：

```text
uv run pytest \
  tests/test_probe_focus_template_modular.py \
  tests/test_equationize_closure_first_near_miss.py \
  tests/test_summarize_closure_first_d4_invariants.py \
  tests/test_closure_first_three_square_search.py -q
```

结果：

```text
18 passed
```

已运行：

```text
uv run ruff check \
  scripts/theory/probe_focus_template_modular.py \
  tests/test_probe_focus_template_modular.py
```

结果：

```text
All checks passed
```
