# wl290 — mixed closure quotient rank smoke

## 结论

按 `tmp.txt` 建议，先测试“看得见闭合关系”的四条 genus-one 商曲线：

- `AA`: `(N^2 + A^2)((A+B-N)^2 + A^2)`
- `BB`: `(N^2 + B^2)((A+B-N)^2 + B^2)`
- `AB`: `(N^2 + A^2)((A+B-N)^2 + B^2)`
- `BA`: `(N^2 + B^2)((A+B-N)^2 + A^2)`

在 archived `320` 个 hard-case pair 上，PARI `ellfromeqn + ellrank(effort=1)` 全部跑通。

最重要的实测结果：

- `AA/BB` 有大量 certified rank `0`。
- `AB/BA` 在这批样本里没有 certified rank `0`。

所以“闭合商曲线确实给出新信号”成立，但 `tmp.txt` 里猜的 `AB` 头号 rank-0 候选暂时没命中。

## 命令

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320.jsonl
```

输出 summary：

```text
wrote 1280 rows for 320 pairs to results/mixed_closure_rank_hard_cases_320.jsonl
status_counts={'ok': 1280}
rank_counts={'0/0': 216, '0/2': 11, '1/1': 560, '1/3': 5, '2/2': 347, '3/3': 127, '4/4': 14}
```

按曲线拆分：

```text
AA {'0/0': 113, '0/2': 5, '1/1': 162, '2/2': 36, '3/3': 4}
AB {'1/1': 117, '1/3': 2, '2/2': 137, '3/3': 57, '4/4': 7}
BA {'1/1': 117, '1/3': 2, '2/2': 137, '3/3': 57, '4/4': 7}
BB {'0/0': 103, '0/2': 6, '1/1': 164, '1/3': 1, '2/2': 37, '3/3': 9}
```

## 实现

- `src/rational_distance/concordant/mixed_closure_curves.py`
- `scripts/theory/rank_mixed_closure_curves.py`
- `tests/test_mixed_closure_curves.py`
- `tests/test_mixed_closure_rank_cli.py`

## 解释边界

这还不是新的 `proof_status` 判定方法。

原因很简单：rank `0` 的商曲线只说明这条 genus-one 商上的有理点是有限/可枚举的候选；要把它升级成 `no_solution`，还必须把 torsion 点回拉到原始 `N`，确认没有非平凡闭合点。当前脚本只负责第一步筛出值得做回拉认证的 pair。

## 后续更新

### 2026-07-06 更新：rank-0 quartic 点回拉烟测

新增 `--pullback-height` 后，对同一批 `320` 个 archived hard-case pair 跑：

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320_pullback_h100000.jsonl \
  --pullback-height 100000
```

结果：

```text
rank0 rows = 216
point_count distribution = {2: 216}
AA {2: 113}
BB {2: 103}
full_closed_points = 0
non_midpoint_points = 0
non_positive_points = 0
```

普通话解释：

- 所有 `AA/BB` certified rank `0` 商曲线，在高度 `100000` 内都只回拉到两个点。
- 这两个点都是同一个中点 `N = M = (A+B)/2`，只是 `y` 正负不同。
- 没有任何点同时让四个平方条件成立。

边界仍然要说清楚：这还不是完整证明。`hyperellratpoints` 是高度枚举；要把它升级成严格
`no_solution`，下一步仍需要把 `ellfromeqn` 的双有理映射/所有 torsion 点逐点回拉，或给出等价的
手算回拉证明。

## 下一步

1. 把 `AA/BB` rank `0` 的中点-only 现象做成严格 torsion 回拉认证。
2. 对 `0/2`、`1/3` 这些 uncertified rank bounds 换成更直接的 2-descent / Selmer / 模型化处理。
3. 把 `C_lambda` 闭合曲线和 4 条商曲线写成正式引理，作为后续论文/规范入口。

### 2026-07-06 更新：uncertified rank bounds 复核

对全量结果里 `16` 条上下界不闭合的曲线，单独跑了 `ellrank(effort=2)` 和
`ellrank(effort=3)`。

结果：全部不变。

```text
0/2 -> 0/2
1/3 -> 1/3
```

所以这批不确定 rank 不能靠简单提高 PARI effort 解决。后续如果要收紧，应该换成更直接的
2-descent / Selmer / 模型化处理，而不是继续加 effort。

### 2026-07-06 更新：rank-0 `AA/BB` torsion 严格回拉

新增 `--certify-rank0-torsion`，并给 rank 输出补充 `root_number`。这次不再用
`hyperellratpoints` 的高度枚举，而是利用
`AA/BB` 的中点对称结构：

```text
t = 2N - (A+B),  z = 4y
z^2 = t^4 + p t^2 + q
```

其中

```text
p = 8L^2 - 2(A+B)^2
q = ((A+B)^2 + 4L^2)^2
```

`L=A` 对应 `AA`，`L=B` 对应 `BB`。偶四次到椭圆曲线的显式模型是：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
X = 2(z + t^2)
V = 2t(X+p)
```

反向回拉为：

```text
t = V / (2(X+p))
z = X/2 - t^2
N = ((A+B)+t)/2
```

当 PARI 认证 `rank=0/0` 时，`E(Q)` 就是 torsion。于是枚举 `elltors(E)` 的全部点并逐点回拉，
可以严格列出原四次曲线的全部仿射有理点；`X=-p` 的 2-torsion 点对应无穷远，不给仿射点。

命令：

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --certify-rank0-torsion
```

统计：

```text
rows = 1280
rank0 torsion certificates = 216
certificate status = {'certified': 216}
curve split = {'AA': 113, 'BB': 103}
root_number missing = 0
torsion_point_count = {4: 216}
affine_preimage_count = {2: 216}
certifies_no_full_closed_square = {True: 216}
all_affine_preimages_are_midpoints = {True: 216}
map_errors = 0
non_midpoint affine preimages = 0
full_closed affine preimages = 0
```

普通话解释：

- 320 个 hard-case pair 里，`AA/BB` 的 `216` 条 certified rank `0` 商曲线现在已经严格回拉完。
- 每条曲线的全部 torsion 点只有两个仿射回拉点。
- 这两个仿射点都是中点 `N=M=(A+B)/2`。
- 没有任何一个点同时让四个闭合平方条件成立。

所以 `AA/BB` 的 rank-0 信号已经从“高度 `100000` 内只看到中点”的实验观察，升级成了
“在这些 rank-0 商曲线上，全部仿射有理点都已列出且无完整闭合点”的严格认证。

同一轮还补了 root number。320 hard cases 按曲线拆分：

```text
AA root_number {-1: 166, 1: 154}
AB root_number { 1: 144, -1: 176}
BA root_number { 1: 144, -1: 176}
BB root_number { 1: 146, -1: 174}
```

边界：

- 这只认证 `AA/BB` 且 `rank_lower=rank_upper=0` 的行。
- `AB/BA` 在这批 320 个 hard cases 里没有 rank `0`，所以没有形成 `tmp.txt` 预期的 `AB` rank-0 击杀器。
- `0/2`、`1/3` 这些上下界不闭合的曲线仍需 2-descent / Selmer 或其它模型化处理。

### 2026-07-06 更新：64 个 local-global residual pair

`tmp.txt` 的实验设计还点名了 wl100 的 `64` 个 local-global 残留对。它们来自：

```text
results/multi_n/non_coprime_scan_max2000.jsonl
gcd_aware_kills 未杀
STANDARD chain_closure 模 p² 未杀
p²<=300 + 若干素数幂仍未杀
```

导出到：

```text
results/mixed_closure_localglobal_residual64_pairs.jsonl
```

然后跑：

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/mixed_closure_localglobal_residual64_pairs.jsonl \
  --out results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --certify-rank0-torsion
```

结果：

```text
rows = 256
status = {'ok': 256}
rank_counts = {'0/0': 59, '1/1': 104, '2/2': 75, '3/3': 14, '4/4': 4}
```

按曲线拆分：

```text
AA {'0/0': 27, '1/1': 34, '2/2': 3}
AB {'1/1': 20, '2/2': 35, '3/3': 7, '4/4': 2}
BA {'1/1': 20, '2/2': 35, '3/3': 7, '4/4': 2}
BB {'0/0': 32, '1/1': 30, '2/2': 2}
```

root number：

```text
AA { 1: 30, -1: 34}
AB {-1: 27,  1: 37}
BA {-1: 27,  1: 37}
BB { 1: 34, -1: 30}
```

torsion 严格回拉：

```text
rank0 torsion certificates = 59
certificate status = {'certified': 59}
curve split = {'AA': 27, 'BB': 32}
affine_preimage_count = {2: 59}
certifies_no_full_closed_square = {True: 59}
all_affine_preimages_are_midpoints = {True: 59}
map_errors = 0
non_midpoint affine preimages = 0
full_closed affine preimages = 0
```

普通话解释：

- 64 个 local-global 残留对里，`AA/BB` 仍然有 rank `0` 新信号，共 `59` 条。
- 这些 rank `0` 信号也全部严格回拉完，只给中点，不给完整闭合点。
- `AB/BA` 仍然没有 rank `0`，所以 `tmp.txt` 猜的 `AB` 头号候选没有兑现。
- 这批 residual pair 没有 rank 上下界不闭合的问题；所有 `256` 行都是 certified rank。
