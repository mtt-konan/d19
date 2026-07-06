# wl295 - SageMath installed and mixed-closure residual rank recheck

日期：2026-07-06

## 一句话结论

SageMath 已经装好并接入当前项目。它现在能稳定复查 `tmp.txt` 方向留下的 `16` 条 rank
不闭合残余，但在低档 `two_descent(second_limit=13)` 下还没有把任何一条收敛成精确 rank。

普通话说：

```text
装 Sage 是一个大节点：后面不再卡在“没有工具”。
但第一轮 Sage 复查说明，剩下 16 条不是按一下按钮就没了。
```

这次产物是一个可复现批处理工具和一条基线结果，不是 Harborth 证明。

## 1. 环境状态

Sage 可执行文件：

```text
/usr/local/bin/sage
```

版本：

```text
SageMath version 10.9, Release Date: 2026-05-04
```

用第一条残余曲线做过手工烟测：

```bash
sage -c 'E=EllipticCurve([0,196194,0,-699602500,-137257812885000]); print(E.rank_bounds()); print(E.rank(proof=True))'
```

结果要点：

```text
rank_bounds = (0, 2)
rank(proof=True) 未能证明 rank 精确值
```

再跑：

```bash
sage -c 'E=EllipticCurve([0,196194,0,-699602500,-137257812885000]); print(E.two_descent(second_limit=13)); print(E.rank_bounds())'
```

仍没有收紧：

```text
rank_bounds = (0, 2)
```

## 2. 新增脚本

新增：

```text
scripts/theory/sage_recheck_mixed_closure_residuals.py
tests/test_sage_recheck_mixed_closure_residuals.py
```

脚本输入：

```text
results/mixed_closure_rank_summary.json
```

它只读取其中的：

```text
uncertain_rank_rows
```

也就是 PARI 留下的 rank 上下界不闭合行。

核心设计：

- 每条曲线单独启动一个 Sage 子进程。
- 每条曲线有独立超时。
- 输出逐行写入 JSONL，中途停止也不会丢掉已经完成的结果。
- Sage 的 verbose 输出只保留尾部，避免结果文件爆炸。

普通话说：以前是“手工试一条曲线”；现在是“可以批量、可中断、可复跑地试所有残余曲线”。

## 3. 完整 16 条 residual recheck

命令：

```bash
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_residual_recheck_limit13.jsonl \
  --second-limit 13 \
  --timeout 60
```

输出摘要：

```text
wrote 16 Sage recheck rows to results/sage_mixed_closure_residual_recheck_limit13.jsonl
status_counts={'ok': 11, 'timeout': 5}
final_rank_counts={'0/2': 9, '0/4': 1, '1/3': 1}
```

逐条结果：

```text
115 297 AA input 0/2 -> ok      final 0/2
189 475 AB input 1/3 -> timeout final missing
189 475 BA input 1/3 -> timeout final missing
209 5355 BB input 1/3 -> ok      final 1/3
209 21735 BB input 0/2 -> ok     final 0/2
391 9009 BB input 0/2 -> ok      final 0/2
567 3757 BB input 0/2 -> ok      final 0/2
575 4641 AA input 0/2 -> ok      final 0/2
1215 27209 AB input 1/3 -> timeout final missing
1215 27209 BA input 1/3 -> timeout final missing
1449 12155 BB input 0/2 -> ok    final 0/4
1625 5643 AA input 0/2 -> ok     final 0/2
5075 17901 AA input 0/2 -> ok    final 0/2
5083 12825 BB input 0/2 -> ok    final 0/2
5301 38675 BB input 0/2 -> ok    final 0/2
8075 8613 AA input 0/2 -> timeout final missing
```

解释：

- `ok` 只表示 Sage 子进程正常结束。
- `timeout` 只表示 60 秒内没跑完，不表示 rank 有结论。
- `final 0/2`、`1/3`、`0/4` 都仍是不闭合 rank bounds。
- 所以这轮没有新增 rank-0 严格证书。

特别注意 `(1449,12155) BB`：

```text
PARI summary input: 0/2
Sage initial/final: 0/4
```

这说明不同工具/模型的 rank bound 口径会有差异。这里不能把 `0/4` 理解成退步或反例，只能记录为
Sage 在该模型上的当前 bounds。

## 4. 本轮修掉的工程问题

第一版批处理在全量 16 条跑完后暴露了一个 bug：

```text
TimeoutExpired.stdout/stderr 在 text=True 时仍可能是 bytes
```

这会导致最终 `json.dumps` 失败。已补测试并修复：

```text
test_recheck_rows_records_timeout_output_when_sage_returns_bytes
```

同时把 CLI 改成逐条落盘。以后长跑即使中途停掉，已经完成的曲线也会保留。

## 5. 对 tmp.txt 方向的影响

这次之后，`tmp.txt` 的下一层问题更清楚了：

```text
AA/BB rank-0 torsion 回拉主线已经严格。
剩下 16 条 residual 不是简单提高 PARI effort 或 Sage low-limit two_descent 就能收。
```

所以后续如果继续收敛，应该分成两路：

1. 对 `AA/BB 0/2` 残余单独加预算，尝试更高 `second_limit` 或换显式 2-cover/Selmer 数据。
2. 对 `AB/BA 1/3` 先不要追 rank-0 证书，因为它们已有通用非 torsion 点；更合理的是解释结构，而不是期待它们变成击杀器。

这和 wl294 的判断一致：主刀仍是 `AA/BB rank=0 -> only midpoint`。Sage 这轮只是确认了
“剩余 rank bounds 需要更重的后续工具”，没有改变主线判断。

## 6. 验证

单元测试：

```bash
uv run pytest tests/test_sage_recheck_mixed_closure_residuals.py -q
```

结果：

```text
3 passed
```

lint：

```bash
uv run ruff check \
  scripts/theory/sage_recheck_mixed_closure_residuals.py \
  tests/test_sage_recheck_mixed_closure_residuals.py
```

结果：

```text
All checks passed!
```

真实 Sage 烟测：

```bash
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_residual_recheck_smoke.jsonl \
  --limit 1 \
  --second-limit 13 \
  --timeout 180
```

结果：

```text
status_counts={'ok': 1}
final_rank_counts={'0/2': 1}
```
