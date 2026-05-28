# Multi-Concordant N 研究路线

本文整理 `multi_concordant_n_scan.py` 得到的新路线：先找多 concordant N 的 `(A,B)`，再研究这些 pair 为什么仍不能闭合成 Harborth 4-chain。

## 1. 当前结论

在 reduced `(A,B)` 搜索域 `max_hyp <= 10000` 内：

```text
总 pair:                         30,397,485
multi-N pair (k >= 2):                  854
chain closure pair:                       0
max concordant N count:                   3
max-k example:                    (153,560)
```

`(153,560)` 的数据：

```text
A + B = 713
concordant N = [204, 420, 3900]

204 + 420  = 624  != 713
204 + 3900 = 4104 != 713
420 + 3900 = 4320 != 713
```

对应椭圆曲线：

```text
E_{153,560}: y^2 = x(x + 153^2)(x + 560^2)
rank(E) = 3
```

这确认 multi-N 不是搜索误差，而是椭圆曲线高 rank 现象。

### Ground-truth storage

`max_hyp=10000` 的 authoritative multi-N 数据集保存在：

```text
results/multi_concordant_N_max10000.jsonl
```

配套索引和查询命令：

```bash
uv run python scripts/multi_n/build_results_catalog.py
uv run python scripts/lookup_multi_n.py 153 560
uv run python scripts/theory/analyze_multi_n_half_points.py 153 560
```

其中：

- `results/README.md` 负责人工可读索引
- `results/catalog.json` 负责机器可读索引
- `lookup_multi_n.py` 用来把后续“快速算法”的候选和 ground truth 对照
- `analyze_multi_n_half_points.py` 用来检查 half-points 与 squarefree 2-descent signature

筛选层级与快速算法切入点见：

- [`docs/MULTI_N_FILTER_LADDER.md`](MULTI_N_FILTER_LADDER.md)

## 2. 关键必要条件

Harborth 4-chain 反例 `(a,b,c,d)` 给出：

```text
A = b
B = d
N1 = a
N2 = c
```

于是必须满足：

```text
N1^2 + A^2 是平方
N1^2 + B^2 是平方
N2^2 + A^2 是平方
N2^2 + B^2 是平方
N1 + N2 = A + B
```

因此：

```text
反例 => (A,B) 至少有两个 concordant N
反例 => 这两个 N 还必须满足线性闭合 N1 + N2 = A + B
```

我们的扫描先找第一层条件，再检查第二层条件。第一层已经很稀少，第二层目前没有出现。

## 3. 椭圆曲线翻译

固定 `(A,B)`，考虑曲线：

```text
E_{A,B}: y^2 = x(x + A^2)(x + B^2)
```

若 `N` 是 concordant，则：

```text
x = N^2
```

给出曲线上的有理点：

```text
(N^2, N * sqrt(N^2 + A^2) * sqrt(N^2 + B^2))
```

所以 multi-N pair 等价于曲线上出现多个 `x = square` 的特殊点。

这条翻译解释了实验数据：

- 大多数 `(A,B)` 没有任何 square-x 点。
- 少数 pair 有一个 square-x 点。
- 有两个或三个 square-x 点的 pair 很少。
- `(153,560)` 有三个 square-x 点，PARI/GP 算出 rank 为 3。

## 3.5 文献定位：multi-N 应看作正秩 concordant curve 的特殊点问题

Ono (1996) 使用的模型是：

```text
E_Q(M,N): y^2 = x^3 + (M+N)x^2 + MNx = x(x+M)(x+N)
```

这与本项目的 `E_{A,B}` 相同，只是取：

```text
M = A^2
N = B^2
```

Ono 的关键结论可直接翻译为：

```text
rank(E_Q(M,N)) > 0
=> Euler concordant form 方程有 infinitely many primitive integer solutions
```

但这还不是我们的 multi-N 条件。原因是 Ono 的 primitive solution 允许一般的
`(X,Y,Z,W)`，而本项目的 concordant `N` 固定在 `Y = 1`：

```text
X^2 + A^2 = Z^2
X^2 + B^2 = W^2
```

所以：

```text
positive rank 解释“解很多”
multi-N 要求这些解里有多个落在 Y=1 / x=N^2 的稀有截面上
chain closure 还要求两个 N 满足 N1+N2=A+B
```

这也解释了 `(153,560)` 的意义：它不是普通正秩曲线，而是正秩曲线里已经命中
三个 `Y=1` 特殊解的稀有样本。

### 文献术语：strongly concordant pair

后续搜索不要只搜 “multi-N”。更接近文献的关键词是：

```text
strongly concordant pair
positive rank concordant forms
Euler concordant forms
rational squares in arithmetic progression
theta-congruent numbers
```

文献中 “strongly concordant pair” 通常指相应曲线正秩，因此有无限多 primitive
解。它能帮助生成候选 `(A,B)` 或 `(M,N)`，但仍需额外筛选 `Y=1` / `x=N^2`
特殊点。

### 对生成算法的含义

可落地的生成路线有四类：

1. **Ono torsion families**：给出 torsion 导致的非平凡解分类。对本项目低优先级，
   因为当 `M=A^2,N=B^2` 时主要落在 `Z2 × Z4` 情形，Ono 的 corollary 说明该
   情形 torsion 不给非平凡 primitive 解；要有大量解仍靠正秩。
2. **Ono quadratic twist families**：用 ternary quadratic form 表示数判断某些
   twist 的 rank 正/零。这是批量生成或排除 concordant curves 的理论入口。
3. **Strongly concordant / ratio of congruent numbers**：固定比例生成无限多正秩
   pair 或 theta-congruent pair。适合先生成正秩曲线，再筛 `M,N` 是否是平方、
   是否有多个 `Y=1` 解。
4. **Knaf-Selder-Spindler homogeneous-space algorithm**：不是 rank 判定算法，而是
   在已知/预期正秩时找小高度 rational points。对 `(153,560)`、26 个 `k=3`
   multi-N pair 的 Mordell-Weil 结构分析最有用。

## 3.6 两下降视角：每个 concordant N 点本身都是一个 double

Ono 1996 Proposition 1 / Corollary 2 说明：对曲线

```text
E: y^2 = (x-\alpha)(x-\beta)(x-\gamma)
```

若点 `P=(x',y')` 满足 `x'-\alpha, x'-\beta, x'-\gamma` 都是有理平方，则存在 `Q` 使

```text
2Q = P
```

对 d19 的 concordant 点

```text
P_N = (N^2, N * sqrt(N^2+A^2) * sqrt(N^2+B^2))
```

三项

```text
x = N^2
x + A^2
x + B^2
```

本来就全是平方，因此 **每个 concordant `N` 对应的点 `P_N` 自动落在 `2E(Q)` 里**。

这有一个重要后果：

```text
不能用 P_N 自己的 2-descent image 区分不同 N
因为 P_N 在 E(Q)/2E(Q) 里是平凡类
```

真正应该研究的是它的 **half-points** `Q_N`，以及这些 `Q_N` 落在哪些 homogeneous spaces。

### `(153,560)` 的显式 half-points

对三个 concordant `N`，可取下列整点 `Q_N`，满足 `2Q_N = P_N`：

```text
N =  204  ->  Q_204  = (19992,  -17013192)
N =  420  ->  Q_420  = ( 7560,   -8671320)
N = 3900  ->  Q_3900 = (  120,    -941160)
```

这说明 `(153,560)` 上那三个 square-x 点并不是“最原始”的生成元；它们已经是更小点的二倍。

### 下一层问题

接下来要算的不是 `P_N` 的 image，而是这些 `Q_N` 的 image：

```text
phi(Q) = (x(Q), x(Q)+A^2)   mod squares
```

当前已知三个 `Q_N` 的原始 squarefree 类不同，但还没按 2-torsion equivalence 做商：

```text
Q_204  -> (102, 43401, 1702)
Q_420  -> (210,  3441, 80290)
Q_3900 -> ( 30, 23529, 78430)
```

若这些类在 2-torsion quotient 后仍彼此不同，那么 multi-N 现象就可能与“多个不同
homogeneous spaces 同时给出有理点”直接相关。

## 4. 反例为什么更难出现

高 rank 只说明曲线上有更多有理点，不说明这些点的 x 坐标是整数平方，也不说明两个 square root 会满足：

```text
sqrt(x(P)) + sqrt(x(Q)) = A + B
```

反例需要同时满足三层条件：

```text
1. E_{A,B} rank 较高或有足够多特殊点
2. 至少两个有理点的 x 坐标是整数平方
3. 这两个平方根满足 N1 + N2 = A + B
```

`(153,560)` 已经满足前两层，但不满足第三层。它是重要的反例候选模型：rank 高、multi-N 明确、但 closure 失败。

## 5. 下一阶段任务

### 任务 A：rank audit 所有 multi-N pair

输入：`results/multi_concordant_N_max10000.jsonl`

输出：每个 pair 的：

```text
A, B
concordant N list
rank lower/upper bound
torsion structure
generators if available
closure_pairs
```

目的：验证 `k=2`、`k=3` 与 rank 的关系。重点看 26 个 `k=3` pair 是否都 rank >= 3，或是否存在 rank 2 + 依赖点结构。

### 任务 B：研究 26 个 k=3 pair

先不要扩大到 `max_hyp=50000`。26 个 k=3 pair 是最有价值的样本。

要统计：

```text
N 的大小分布
N 与 A+B 的距离
所有 N_i + N_j - (A+B)
rank
generator 高度
prime factor pattern of A, B, B^2-A^2
```

目标：找 closure 失败的共同原因。

### 任务 C：把 closure 条件做成局部筛

已有 `chain_closure_mod_sieve` 检查单个 `(A,B)` 是否存在局部 obstruction。

下一步要针对 multi-N pair 加强：

```text
给定 A,B 和模数 m，枚举所有 N mod m 使：
N^2 + A^2, N^2 + B^2 都是平方 mod m

再检查是否存在 n1,n2 满足：
n1 + n2 = A + B mod m
```

如果某个模数已经无解，则该 pair 不可能闭合。

### 任务 D：固定 pair 的 Mordell-Weil sieve

对 `(153,560)` 这种 rank=3 样本，用 Mordell-Weil 群解释所有已找到的 square-x 点。

目标不是再找点，而是证明：

```text
不存在两个 square-x 点 P,Q，使 sqrt(x(P)) + sqrt(x(Q)) = A+B
```

这条路线可能成为证明 Harborth 猜想的局部模板。

### 任务 E：文献笔记

已下载并可抽取文本：

```text
docs/literature/pdfs/ono-1996-eulers-concordant-forms.pdf
docs/literature/pdfs/knaf-selder-spindler-2019-algorithm.pdf
```

文本抽取：

```bash
uv run python scripts/utility/extract_pdf_text.py docs/literature/pdfs/*.pdf
```

需要从文中提取：

1. concordant forms 与 elliptic curve 的精确对应公式
2. rank > 0 的判据
3. torsion 点对应的平凡解
4. 是否有关于多个解、多个 square-x 点的定理
5. KSS homogeneous-space 算法如何找独立点

补充阅读：

- Selder & Spindler, arXiv:1408.1522 / Mathematics 2015
- Li & Hu, arXiv:1005.5579, ratio of theta-congruent numbers
- Rajan & Ramaroson, ratio of congruent numbers
- Knaf, Selder & Spindler, arXiv:1907.02148
- MathPages: Concordant Forms

## 6. 优先级

短期不要扩大搜索。先做结构分析。

```text
P0: 修正并保存 max_hyp=10000 数据和 worklog
P1: rank audit 854 个 multi-N pair
P2: 深入分析 26 个 k=3 pair
P3: 实现 multi-N closure local sieve
P4: 写 Ono + KSS 论文阅读笔记
P5: 再决定是否跑 max_hyp=50000
```

理由：`max_hyp=10000` 已经给出足够多的 multi-N 样本。继续扩大搜索会多消耗数小时，但未必增加理解。rank audit 和 k=3 分类能直接告诉我们下一步证明应该盯哪里。

## 7. 当前判断

当前证据支持以下工作假设：

```text
Harborth 反例不存在。
```

更精确地说：反例若存在，必须来自高 rank concordant curve 上两个满足线性闭合的 square-x 点。`max_hyp <= 10000` 的 854 个 multi-N pair 已经全部失败，说明 closure 条件比 multi-N 条件更强。下一步应把 closure 条件从实验检查提升为可证明的局部或 Mordell-Weil 障碍。
