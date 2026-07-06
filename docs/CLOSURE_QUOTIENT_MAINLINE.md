# Closure Quotient Mainline

这份文档把 `tmp.txt` 里的混合闭合商曲线方向正式并入 `concordant` 主线。它负责回答：

- 固定 `(A,B)` 后，怎样把被旧曲线忘掉的闭合腿 `M=A+B-N` 放回问题里；
- 哪些闭合商曲线已经能给出严格判据；
- 哪些地方还只是实验信号，不能写进 `proof_status`。

如果只想看临时判断，读 [wl294](work-logs/294-tmp-mixed-closure-answer.md)。如果要接着做这条线，
从本文开始。

## 1. 主线位置

当前项目仍以 `concordant` 为 active 主线。closure quotient 是 `concordant` 下面的新子方向。

旧主线问：

```text
是否存在 N，使 N^2 + A^2 与 N^2 + B^2 同时为平方？
```

closure quotient 问：

```text
若 M = A+B-N，也要求 M^2 + A^2 与 M^2 + B^2 为平方，会发生什么？
```

普通话说：旧曲线能解释半解，closure quotient 才开始看完整闭合。

## 2. 四条商曲线

内部和闭合关系取：

```text
M = A+B-N
```

四个平方条件是：

```text
NA: N^2 + A^2
NB: N^2 + B^2
MA: M^2 + A^2
MB: M^2 + B^2
```

把其中两个相乘，得到四条看见闭合关系的 genus-one 商曲线：

```text
AA: y^2 = NA * MA
BB: y^2 = NB * MB
AB: y^2 = NA * MB
BA: y^2 = NB * MA
```

完整闭合点必须落在这四条商曲线上。任何一条商曲线能严格排除非平凡点，就能排除原闭合点。

## 3. 已经可用的判据

### 3.1 `AA/BB rank=0` torsion 回拉

`AA/BB` 有中点对称。令：

```text
t = 2N - (A+B)
z = 4y
```

它们化为偶四次：

```text
z^2 = t^4 + p t^2 + q
```

其中 `L=A` 对应 `AA`，`L=B` 对应 `BB`：

```text
p = 8L^2 - 2(A+B)^2
q = ((A+B)^2 + 4L^2)^2
```

对应的椭圆曲线是：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
X = 2(z + t^2)
V = 2t(X+p)
```

反向回拉：

```text
t = V / (2(X+p))
z = X/2 - t^2
N = ((A+B)+t)/2
```

所以当 PARI 认证 `rank_lower=rank_upper=0` 时，`E(Q)` 全由 torsion 点组成。枚举 `elltors(E)` 并回拉，
即可列出原四次曲线的全部仿射有理点。

当前实现：

```text
src/rational_distance/concordant/mixed_closure_curves.py
  certify_rank_zero_even_quotient()

scripts/theory/rank_mixed_closure_curves.py
  --certify-rank0-torsion
```

这个判据已经跑过两批样本：

```text
320 hard cases:
  AA/BB rank-0 certificates = 216
  all certified
  all affine preimages are midpoint N=M=(A+B)/2
  full closed affine preimages = 0

64 local-global residual pairs:
  AA/BB rank-0 certificates = 59
  all certified
  all affine preimages are midpoint N=M=(A+B)/2
  full closed affine preimages = 0
```

这已经是严格判据，不再是高度枚举。

### 3.2 root number 只作诊断

rank 输出现在记录 `root_number`。它帮助观察 parity pattern，但当前不作为无条件判据。

320 hard cases：

```text
AA root_number {-1: 166, 1: 154}
AB root_number { 1: 144, -1: 176}
BA root_number { 1: 144, -1: 176}
BB root_number { 1: 146, -1: 174}
```

64 residual pairs：

```text
AA { 1: 30, -1: 34}
AB {-1: 27,  1: 37}
BA {-1: 27,  1: 37}
BB { 1: 34, -1: 30}
```

## 4. 不能主线化的说法

不要把这条线写成“已经证明 Harborth 猜想”。

不要说 `AB` 是 rank-0 击杀器。两批样本里 `AB/BA` 都没有 rank `0`。

不要把 `AA/BB rank=0` 当作全体 pair 的判定器。它只处理 rank 已经 certified 为 `0/0` 的
`AA/BB` 行。

不要把 root number 当作无条件证明。它目前只是诊断字段。

## 5. 主线任务表

### P0：保持已完成结论可复现

已完成。

复现命令：

```bash
PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/archive/ell2cover_hard_cases.jsonl \
  --out results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --certify-rank0-torsion

PARI_MT_ENGINE=single uv run python scripts/theory/rank_mixed_closure_curves.py \
  --pairs-jsonl results/mixed_closure_localglobal_residual64_pairs.jsonl \
  --out results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --certify-rank0-torsion
```

### P1：收紧不确定 rank bounds

320 hard cases 里仍有：

```text
0/2 = 11
1/3 = 5
```

`ellrank(effort=2/3)` 没收紧。下一步要换 2-descent / Selmer / 模型化处理。

### P2：解释 `AB/BA` 无 rank 0

两批样本中 `AB/BA` 全部 rank 正。需要判断这是偶然，还是闭合结构强迫。

如果能证明一个结构性正秩点族，`AB/BA rank=0` 路线应停止押注。

### P3：把 `AA/BB rank=0` 写成论文级引理

当前已有代码证明型证据。下一步要把下面这句话写成独立引理：

```text
对 AA/BB，若 centered even model 的椭圆曲线 rank 为 0，
则枚举 torsion 并按显式反向映射回拉，可列尽原四次曲线的仿射有理点。
若回拉点全为中点，则该商曲线排除完整闭合点。
```

### P4：决定是否接入 `proof_status`

现在先不要默认接入。等 P1/P2 有结果后再决定。

可选接法：

```text
factor_concordant / GEN-CLOSURE 后
  -> rank_mixed_closure_curves
  -> only when AA/BB rank=0 and torsion certificate says no full closed square
```

## 6. 主线停止条件

这条线继续推进时，必须设置停止条件。

可以继续的信号：

- `AA/BB rank=0` 覆盖越来越多 hard/residual pair；
- 不确定 rank bounds 能被 Selmer 收紧；
- `AB/BA` 出现可解释的结构，而不是只给分布表。

应该降级为辅助工具的信号：

- `AA/BB rank=0` 覆盖率停在小子集；
- `AB/BA` 被证明一般正秩；
- P1 的不确定 rank 需要重型工具但收益很小。

## 7. 入口清单

代码：

- `src/rational_distance/concordant/mixed_closure_curves.py`
- `scripts/theory/rank_mixed_closure_curves.py`

测试：

- `tests/test_mixed_closure_curves.py`
- `tests/test_mixed_closure_rank_cli.py`

结果：

- `results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl`
- `results/mixed_closure_localglobal_residual64_pairs.jsonl`
- `results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl`

工作日志：

- [wl290](work-logs/290-mixed-closure-quotient-rank-smoke.md)
- [wl294](work-logs/294-tmp-mixed-closure-answer.md)

数学总入口：

- [docs/MATH.md](MATH.md) §8.4.1
