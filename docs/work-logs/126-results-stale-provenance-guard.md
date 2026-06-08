# wl126 — results stale provenance guard

日期：2026-06-09

## 1. 本轮问题

审计里已经指出一个数据来源风险：

```text
results/proof_status.db
```

相对 wl094 之后的 full-plane closure 语义已经 stale，但旧目录仍把它写成：

```text
authoritative=true
```

普通话说：

```text
旧数据库像一张旧地图。
它能告诉我们当时怎么走过，但不能当成现在的道路证明。
```

同类问题还有：

```text
results/chain.db
```

README 之前把它写成 chain-fast SQLite 结果库，但审计已经确认它是 legacy schema。当前 chain-fast 代码不能把这个旧库当作当前 schema 的权威证据。

---

## 2. 证据

本轮读到：

```text
results/catalog.json
```

其中旧条目：

```json
{
  "path": "proof_status.db",
  "category": "proof-status",
  "authoritative": true
}
```

同时审计笔记已经记录：

```text
results/proof_status.db has hard_case|4653
```

这些计数来自旧 workflow 快照，不能直接代表当前 full-plane/gcd-aware 语义。

还读到：

```text
results/README.md
```

其中旧表述：

```text
chain.db = chain-fast SQLite 结果库
proof_status.db = proof-status workflow 状态
```

这两个说法都太像“当前证据”。后续 agent 很容易把它们接到上层结论里。

---

## 3. 修改

### 3.1 catalog 生成器

文件：

```text
src/rational_distance/results/catalog.py
```

修改两类元数据。

第一，multi-N 文件路径改成当前目录结构：

```text
multi_n/multi_concordant_N_max10000.jsonl
multi_n/multi_concordant_N_max20000_fast.jsonl
...
```

之前 catalog 指向顶层旧路径：

```text
multi_concordant_N_max10000.jsonl
```

但当前数据在：

```text
results/multi_n/
```

第二，`proof_status.db` 降级：

```text
authoritative=false
description="Stale local proof-status workflow snapshot; historical only unless rebuilt with current full-plane/gcd-aware semantics."
```

### 3.2 catalog 回归测试

文件：

```text
tests/test_results_catalog.py
```

新增保护：

```text
test_build_results_catalog_marks_stale_proof_status_snapshot
```

检查：

```text
proof_status.db authoritative == false
description contains "stale"
```

也更新 multi-N 测试，要求目录路径是：

```text
multi_n/multi_concordant_N_max10000.jsonl
```

### 3.3 README

文件：

```text
results/README.md
```

新增“先读这个：哪些结果能当证据？”。

关键边界：

```text
authoritative=true 只表示有限范围实验的原始/基准数据；
不表示全空间证明。
```

并明确：

```text
proof_status.db 是 stale workflow snapshot。
chain.db 是 legacy chain-fast DB。
```

---

## 4. 能说什么，不能说什么

可以说：

```text
results catalog 不再把 proof_status.db 标成当前权威证据。
README 已经把 proof_status.db / chain.db 标成 stale 或 legacy。
multi-N catalog 路径和当前 results/multi_n/ 布局一致。
```

不能说：

```text
proof_status.db 已经按当前语义重建。
chain.db 已经迁移到当前 schema。
旧 hard_case/no_solution 计数仍可直接引用为当前证明状态。
```

这轮是 provenance guard，不是数学证明，也不是 DB 迁移。

---

## 5. 剩余边界

`results/catalog.json` 在本机被 ignore 规则挡住：

```text
.git/info/exclude: results/
```

所以本轮修改的可提交保护在：

```text
src/rational_distance/results/catalog.py
tests/test_results_catalog.py
results/README.md
docs/work-logs/126-results-stale-provenance-guard.md
```

本机已用生成脚本重建：

```text
uv run python scripts/multi_n/build_results_catalog.py
```

但如果要让 `results/catalog.json` 也进入 git，需要单独处理 ignore 规则或强制 add。当前更稳的做法是提交生成器和测试，让任何人重建时都得到降级后的 catalog。

---

## 6. 验证

TDD 红灯：

```text
uv run pytest tests/test_results_catalog.py -q
```

修改前失败点：

```text
catalog path was multi_concordant_N_max10000.jsonl
proof_status.db authoritative was true
```

修改后运行：

```text
uv run pytest tests/test_results_catalog.py -q
```

结果：

```text
2 passed
```

另运行：

```text
uv run python scripts/multi_n/build_results_catalog.py
```

本机 `results/catalog.json` 现在显示：

```text
proof_status.db authoritative=false
description contains stale / full-plane / gcd-aware
```

---

## 7. 下一步

如果继续工程安全清理，优先处理两个点：

```text
1. 把 scripts/archive/* 里默认读取 results/proof_status.db 的入口标成 historical；
2. 把 sum-only / inside-square 旧文档和脚本入口继续降级，避免和 full-plane GEN-CLOSURE 混用。
```

数学主线不受这轮影响。后续仍按 wl117 路线推进：

```text
rational-ratio λ
closure-first near-miss equationization
D4 对称变量
fixed-ratio / Yang Ji 推广
non-coprime full-space gap
```
