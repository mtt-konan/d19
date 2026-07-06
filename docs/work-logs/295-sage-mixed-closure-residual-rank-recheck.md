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

## 7. 后续更新：AA/BB 批处理增强与 `second_limit=20` 边界

继续推进时，脚本补了三个实用能力：

```text
--curve AA --curve BB       只跑指定曲线类型
--target A,B,CURVE          只跑指定残余行
elapsed_seconds             每条结果记录实际耗时
```

这让后续可以只攻主线上的 `AA/BB` 残余，不把 `AB/BA` 混进来。

真实烟测：

```bash
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_target_smoke.jsonl \
  --target 115,297,AA \
  --second-limit 13 \
  --timeout 180
```

结果：

```text
[1/1] (115,297) AA status=ok final=0/2 elapsed=25.518334s
```

AA/BB 过滤烟测：

```bash
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_aabb_filter_smoke.jsonl \
  --curve AA \
  --curve BB \
  --limit 2 \
  --second-limit 13 \
  --timeout 180
```

结果：

```text
[1/2] (115,297) AA status=ok final=0/2 elapsed=25.521335s
[2/2] (209,5355) BB status=ok final=1/3 elapsed=49.859545s
```

然后试了一次更高档：

```bash
uv run python scripts/theory/sage_recheck_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_aabb_recheck_limit20.jsonl \
  --curve AA \
  --curve BB \
  --second-limit 20 \
  --timeout 300
```

第一条就超时：

```text
[1/12] (115,297) AA status=timeout final=missing elapsed=300.003987s
```

随后观察第 2 条 60 秒仍无输出，手动中止。这个结果不提供 rank 结论，但提供了成本边界：

```text
second_limit=20 不能作为前台批量常规参数。
后续如果继续用 Sage，应改成按单条目标后台长跑，或者换 Selmer / 2-cover 数据来做更结构化判断。
```

普通话说：

```text
13 档能给基线，但不收敛。
20 档成本明显上升，第一条 5 分钟都没跑完。
所以不能靠简单调高 Sage 参数来收敛 tmp 方向。
```

## 8. 后续更新：Selmer 与 analytic-rank 诊断

继续推进时新增轻量诊断脚本：

```text
scripts/theory/sage_diagnose_mixed_closure_residuals.py
tests/test_sage_diagnose_mixed_closure_residuals.py
```

它和 recheck 脚本不同：默认不做重型 `two_descent(second_limit=...)`，只收集 Sage 能较快给出的结构信息：

```text
rank_bounds
selmer_rank_pari
selmer_rank_mwrank
torsion_order
torsion_invariants
torsion_two_dimension
root_number
conductor
rank_plus_sha2_dimension = selmer_rank_pari - torsion_two_dimension
```

命令：

```bash
uv run python scripts/theory/sage_diagnose_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --curve AA \
  --curve BB \
  --timeout 120
```

结果：

```text
wrote 12 Sage diagnostic rows to results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl
status_counts={'ok': 12}
selmer_rank_counts={'4': 10, '5': 1, '6': 1}
```

逐条摘要：

```text
115 297 AA       bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
209 5355 BB      bounds [1,3] selmer 5 tors2dim 2 rank+sha2 3 root -1
209 21735 BB     bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
391 9009 BB      bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
567 3757 BB      bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
575 4641 AA      bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
1449 12155 BB    bounds [0,4] selmer 6 tors2dim 2 rank+sha2 4 root  1
1625 5643 AA     bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
5075 17901 AA    bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
5083 12825 BB    bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
5301 38675 BB    bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
8075 8613 AA     bounds [0,2] selmer 4 tors2dim 2 rank+sha2 2 root  1
```

普通话解释：

```text
多数 AA/BB 残余都不是“没有 Selmer 信息”。
它们的 2-Selmer 维数正好比满 2-torsion 多 2。
所以问题被压成：这多出来的 2 维到底来自真实 rank，还是来自 Sha[2]。
```

对 10 条 `root_number=+1, selmer_rank=4` 的行，当前形态是：

```text
rank 0 + Sha[2] 维数 2
或
rank 2 + Sha[2] 维数 0
```

这就是剩余 AA/BB 残余的真正核心。要把它们变成 rank-0 证书，不能只靠普通 rank bounds；
需要严格地区分“真实 Mordell-Weil 点”与“2-Selmer 里的 Sha 元素”。

脚本也支持 probable analytic rank 探针：

```bash
uv run python scripts/theory/sage_diagnose_mixed_closure_residuals.py \
  --sage /usr/local/bin/sage \
  --summary results/mixed_closure_rank_summary.json \
  --out results/sage_mixed_closure_aabb_analytic_rank_pari_probe.jsonl \
  --curve AA \
  --curve BB \
  --limit 4 \
  --analytic-rank pari \
  --timeout 45
```

结果：

```text
[1/4] (115,297) AA status=ok
[2/4] (209,5355) BB status=timeout
[3/4] (209,21735) BB status=timeout
[4/4] (391,9009) BB status=timeout

status_counts={'ok': 1, 'timeout': 3}
```

第一条 `(115,297) AA` 得到：

```text
analytic_rank_pari = 0
```

前面手工还确认过：

```text
analytic_rank_sympow = 0
```

边界必须说清楚：Sage 文档把 `analytic_rank()` 描述为 “probably”。所以这只是强证据，不是严格
rank-0 证书。它说明 `(115,297) AA` 很可能是：

```text
rank 0 + Sha[2] 维数 2
```

而不是：

```text
rank 2
```

但要写进严格主线，还需要可认证的 L 值非零 / Sha[2] 证书 / 2-cover 无点证书。

## 9. 后续更新：PARI ell2cover 显式 cover 探针

继续推进时新增：

```text
scripts/theory/pari_ell2cover_mixed_residuals.py
tests/test_pari_ell2cover_mixed_residuals.py
```

目的：把上面的 Selmer 维数拆成具体的 2-cover 四次曲线，看看哪些 cover 找得到有理点，哪些
cover 是 Sha[2] 候选。

第一条 `(115,297) AA` 手工和脚本都得到：

```text
ellrank = [0, 2, 0, []]
ell2cover count = 4
height <= 100000:
  cover 1: 4 points
  cover 2: 2 points
  cover 3: 0 points
  cover 4: 0 points
```

命令：

```bash
uv run python scripts/theory/pari_ell2cover_mixed_residuals.py \
  --summary results/mixed_closure_rank_summary.json \
  --out results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --curve AA \
  --curve BB \
  --height 100000 \
  --effort 1
```

结果：

```text
wrote 12 ell2cover rows to results/pari_ell2cover_mixed_aabb_h100000.jsonl
status_counts={'ok': 12}
covers_without_points_counts={'2': 10, '3': 1, '4': 1}
```

逐条摘要：

```text
115 297 AA       rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
209 5355 BB      rank+sha2 3  covers_without_points 3  point_counts [12,2,0,0,0]
209 21735 BB     rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
391 9009 BB      rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
567 3757 BB      rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
575 4641 AA      rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
1449 12155 BB    rank+sha2 4  covers_without_points 4  point_counts [4,2,0,0,0,0]
1625 5643 AA     rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
5075 17901 AA    rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
5083 12825 BB    rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
5301 38675 BB    rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
8075 8613 AA     rank+sha2 2  covers_without_points 2  point_counts [4,2,0,0]
```

普通话解释：

```text
这些 residual 不是乱的。
对 10 条最典型的 AA/BB [0,2] 残余，ell2cover 都呈现同一个形状：
4 个 cover 里前 2 个有点，后 2 个在高度 100000 内没点。
```

这和 Selmer 诊断完全对齐：

```text
selmer_rank - torsion_two_dimension = covers_without_points
```

边界：

- `hyperellratpoints` 没找到点不是严格“无点证明”。
- 但这已经给出 explicit Sha[2] candidate cover。
- 下一步若要把 `(115,297) AA` 或 10 条典型残余变成严格 rank-0 证书，需要证明这些 no-point cover
  真的全局无有理点，或者给出等价的 Cassels-Tate / Brauer-Manin / L 值非零证书。

当前收敛判断：

```text
tmp 方向的 residual 已经从“16 条 rank bounds 不闭合”
进一步压成“AA/BB 的 explicit 2-cover no-point candidates”。
这是继续严格化 Sha[2] 的正确入口。
```
