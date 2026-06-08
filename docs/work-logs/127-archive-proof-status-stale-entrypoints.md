# wl127 — archive proof_status stale entrypoints

日期：2026-06-09

## 1. 本轮问题

wl126 已经把 `results/proof_status.db` 从 catalog 当前权威里降级。但还有一类入口会误导后续 agent：

```text
scripts/archive/* --db results/proof_status.db
```

这些脚本本来就是 wl036-wl041 一带的历史工具。问题不在算法，而在入口太安静：

```text
默认读旧 DB；
help 文本不提醒 stale；
输出里的 hard_case 容易被当成当前 proof-status。
```

普通话说：

```text
门上写着“数据库入口”，但没写“这是一扇通往旧楼层的门”。
```

---

## 2. 处理范围

本轮只处理默认读取 `results/proof_status.db` 的 archive 脚本：

```text
scripts/archive/batch_ell2cover_hard_cases.py
scripts/archive/batch_sha2_scan_v2.py
scripts/archive/finite_descent_hard_cases.py
scripts/archive/finite_descent_layer2.py
scripts/archive/pattern_hunt_hard_cases.py
scripts/archive/probe_chain_closure_mod_sieve.py
```

这些脚本仍可复跑历史分析。我们不改数学逻辑，也不迁移 DB。

---

## 3. 修改

每个脚本加 provenance note：

```text
default results/proof_status.db is stale/historical
do not use hard_case counts as current proof-status evidence
unless rebuilt under current full-plane/gcd-aware semantics
```

每个 `--db` 参数的 help 也加同样边界。这样用户运行：

```text
uv run python scripts/archive/<name>.py --help
```

会直接看到：

```text
Stale/historical proof_status SQLite database
```

另外更新：

```text
scripts/archive/README.md
```

明确 archive 脚本默认 DB 的正确引用方式：

```text
基于 stale/historical proof_status.db 的历史分析
```

不能写成：

```text
当前 hard_case / no_solution 计数
```

---

## 4. 新增测试

文件：

```text
tests/test_archive_script_provenance.py
```

测试逐个运行六个脚本：

```text
python scripts/archive/<name>.py --help
```

并检查 help 文本包含：

```text
results/proof_status.db
stale
historical
```

TDD 红灯时，测试失败在：

```text
batch_ell2cover_hard_cases.py
```

原因是 help 文本只写了 `proof_status SQLite database`，没有 stale/historical。

---

## 5. 能说什么，不能说什么

可以说：

```text
archive proof_status 默认入口现在会提醒 stale/historical 边界。
后续 agent 跑 --help 时能看到旧 DB 不能当当前证明证据。
```

不能说：

```text
这些 archive 脚本已升级到 full-plane/gcd-aware 当前语义。
results/proof_status.db 已经重建。
旧 hard_case 分析已经被当前理论重新验证。
```

这轮是入口防误用，不是数学证明。

---

## 6. 验证

运行：

```text
uv run pytest tests/test_archive_script_provenance.py -q
```

结果：

```text
1 passed
```

后续还应运行全量测试，确认 archive help 文本改动没有破坏其他测试。

---

## 7. 下一步

工程安全清理剩下两类：

```text
1. sum-only / inside-square 旧文档和脚本入口继续标成 historical；
2. docs/THEORY_DIRECTIONS_ADVANCED.md 等旧策略文档中 hard_case/rank 说法继续降级。
```

数学主线仍应回到：

```text
rational-ratio λ
closure-first near-miss equationization
D4 对称变量
fixed-ratio / Yang Ji 推广
non-coprime full-space gap
```
