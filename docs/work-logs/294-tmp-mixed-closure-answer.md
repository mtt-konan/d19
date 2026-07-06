# wl294 - tmp.txt 混合闭合商曲线方向的临时回答

日期：2026-07-06

这份文档只回答 `tmp.txt` 里那一轮判断。它不是 Harborth 猜想的最终路线图，也不替代后续继续收敛
`tmp.txt` 方向的工作。

## 一句话结论

`tmp.txt` 的核心判断对了一半，也错了一半。

对的部分：旧的 concordant 曲线 $E_{A,B}$ 确实漏掉了闭合关系。把闭合腿
$M=A+B-N$ 放回对象以后，混合闭合商曲线给出了旧工具看不到的新信号。

错的部分：`tmp.txt` 猜 `AB` 会是 rank-0 击杀的头号候选。实测没有兑现。两批样本里
`AB/BA` 都没有 rank `0`。真正出现 rank `0` 的是 `AA/BB`。

## 已经查清楚的事实

这次看的四条商曲线是：

```text
AA: (N^2 + A^2)((A+B-N)^2 + A^2)
BB: (N^2 + B^2)((A+B-N)^2 + B^2)
AB: (N^2 + A^2)((A+B-N)^2 + B^2)
BA: (N^2 + B^2)((A+B-N)^2 + A^2)
```

### 1. 320 个 hard cases

输入：

```text
results/archive/ell2cover_hard_cases.jsonl
```

输出：

```text
results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl
```

结果：

```text
1280 rows = 320 pairs x 4 curves
status ok = 1280

rank_counts:
0/0 = 216
0/2 = 11
1/1 = 560
1/3 = 5
2/2 = 347
3/3 = 127
4/4 = 14
```

按曲线看：

```text
AA: 113 条 rank 0
BB: 103 条 rank 0
AB: 0 条 rank 0
BA: 0 条 rank 0
```

### 2. 64 个 local-global residual pairs

输入：

```text
results/mixed_closure_localglobal_residual64_pairs.jsonl
```

输出：

```text
results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl
```

结果：

```text
256 rows = 64 pairs x 4 curves
status ok = 256

rank_counts:
0/0 = 59
1/1 = 104
2/2 = 75
3/3 = 14
4/4 = 4
```

按曲线看：

```text
AA: 27 条 rank 0
BB: 32 条 rank 0
AB: 0 条 rank 0
BA: 0 条 rank 0
```

这批 residual pair 没有 `0/2` 或 `1/3` 这种 rank 上下界不闭合的问题。

## rank-0 的含义已经严格化

`AA/BB` 有一个中点对称结构。设：

```text
t = 2N - (A+B)
z = 4y
```

`AA/BB` 会变成偶四次：

```text
z^2 = t^4 + p t^2 + q
```

它对应的椭圆曲线模型是：

```text
E: V^2 = X^3 + pX^2 - 4qX - 4pq
X = 2(z + t^2)
V = 2t(X+p)
```

反向回拉是：

```text
t = V / (2(X+p))
z = X/2 - t^2
N = ((A+B)+t)/2
```

所以当 PARI 认证 rank 是 `0/0` 时，$E(\mathbb Q)$ 只有 torsion 点。枚举全部 torsion 点，再按上面的公式回拉，
就能列出原四次曲线的全部仿射有理点。这里没有再用高度枚举。

严格回拉结果：

```text
320 hard cases:
rank0 torsion certificates = 216
certified = 216
affine_preimage_count = {2: 216}
full_closed affine preimages = 0
non_midpoint affine preimages = 0

64 residual pairs:
rank0 torsion certificates = 59
certified = 59
affine_preimage_count = {2: 59}
full_closed affine preimages = 0
non_midpoint affine preimages = 0
```

普通话解释：这些 rank-0 的 `AA/BB` 商曲线确实全部只回拉到中点
`N=M=(A+B)/2`。它们没有给出完整闭合平方点。

## 对 tmp.txt 里几个判断的回答

### 判断 1：旧 $E_{A,B}$ 选错对象，漏掉闭合关系

临时回答：成立。

旧曲线只看 $N$，不看 $M=A+B-N$。这会看到很多半解，却不能判断完整闭合。`AA/BB/AB/BA`
这些商曲线至少把 $N$ 和 $M$ 放进同一个对象里。实测也说明它们产生了旧 rank 过滤没有给出的信号。

### 判断 2：`AB` 可能是 rank-0 击杀的头号候选

临时回答：不成立，至少当前两批样本不支持。

320 个 hard cases 和 64 个 residual pairs 里，`AB/BA` 都没有 rank `0`。`AB/BA` 仍然有用，因为它们是闭合曲线的商，但它们没有按 `tmp.txt` 预期变成第一把 rank-0 刀。

### 判断 3：`AA/BB` 的中点是万能点，可能解释 rank-0 现象

临时回答：部分成立，而且现在比“可能”更强。

在 rank-0 的 `AA/BB` 行里，严格 torsion 回拉已经列完所有仿射点。结果只有两个点，都是中点，正负号不同。
这说明 `AA/BB` 的 rank-0 信号不是反例通道，而是一个“只剩中点”的闭合障碍。

### 判断 4：混合商曲线能否成为新筛法

临时回答：能成为局部新筛，但现在还不能直接接成通用 `proof_status` 判定器。

原因：

- 对 `AA/BB rank=0` 的行，已经可以严格判掉完整闭合点。
- 对 `AB/BA`，没有 rank `0` 命中。
- 对 320 hard cases 中的 `0/2`、`1/3`，PARI effort 2/3 也没收紧，需要 2-descent / Selmer 或其它模型处理。

所以它现在是一个可靠的局部结论，不是全局判定器。

### 判断 5：高级工具为什么不是直接赢

临时回答：原因仍然是“作用域不够统一”。

逐对问题已经有 `factor_concordant` 和 GEN-CLOSURE，很多时候不需要高级工具。逐射线问题才是
Chabauty / Mordell-Weil sieve 的主场。全族问题要求一次管住所有 $\lambda$，现在没有现成工具能做到。

这次 `AA/BB` 的 torsion 回拉说明高级工具不是没用，而是要放在正确对象上。它能把一个局部 rank-0 信号变成严格点集结论。

## 目前不能说的话

不能说“混合闭合商曲线证明了无反例”。

不能说“`AB` 是新击杀器”。

不能说“所有 hard cases 都被 `AA/BB rank=0` 杀掉”。它只覆盖命中的 rank-0 子集。

不能说“`C_\lambda` 方向已经收敛”。这次只是把 `tmp.txt` 里第一轮实验判断回答清楚了。

## 后续继续收敛 tmp.txt 方向时该做什么

后续是另一个任务。优先级可以这样排：

1. 处理 320 hard cases 里的 `0/2`、`1/3` rank bounds，换 2-descent / Selmer 或更直接模型。
2. 把 `AA/BB rank=0 -> only midpoint` 写成更正式的引理，减少对脚本证据的依赖。
3. 对 `AB/BA` 做结构解释：为什么它们在这两批样本里没有 rank `0`。
4. 再考虑逐射线的 $C_\lambda$ Mordell-Weil sieve 或 Chabauty。

当前临时回答只到这里：`tmp.txt` 的混合商曲线实验方向值得保留，但第一把刀不是 `AB`，而是
`AA/BB rank=0` 的中点-only 障碍。
