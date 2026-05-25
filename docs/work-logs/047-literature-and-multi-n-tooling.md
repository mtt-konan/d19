# wl047 — Literature review + reusable multi-N tooling

## 背景

wl046 用 10 核 multiprocessing 在 `max_hyp=10000` 上跑出 854 条 multi-N pair（`results/multi_concordant_N_max10000.jsonl`），但留下两个问题：

1. **结果一堆没整理**：`results/` 下文件越来越多，没有索引也没有查询入口，后续“快速算法”要拿什么作 ground truth 都说不清。
2. **理论基础没夯实**：multi-N 现象到底是 Ono 1996 已经处理过的“primitive solution”，还是新的特殊截面问题？没有文献定位就开始写算法是不负责任的。

本 worklog 记录 wl046 完成后到 wl048（pivot-on-N 快速扫描器）开始之前，这两条线的所有动作。

## 1. 文献基础设施

### 1.1 PDF 文本抽取工具

为后续阅读和摘录方便，加了一条文本抽取通道：

- `src/rational_distance/literature/pdf_text.py`
- `scripts/extract_pdf_text.py`
- `tests/test_pdf_text.py`
- `docs/literature/pdfs/.gitignore` 改成允许提交 `.txt`，但仍忽略 `.pdf`

用法：

```bash
uv run python scripts/extract_pdf_text.py docs/literature/pdfs/*.pdf
```

抽取结果以 `.txt` 形式与 PDF 同目录，被纳入 git，方便 grep。

### 1.2 五篇文献的本地文本

完成抽取并入库：

```text
docs/literature/pdfs/ono-1996-eulers-concordant-forms.txt
docs/literature/pdfs/knaf-selder-spindler-2019-algorithm.txt
docs/literature/pdfs/asiryan-2025-cuboid-poly.txt
docs/literature/pdfs/peschmann-2026-quartic-reductions.txt
docs/literature/pdfs/bremner-ulas-2016-rational-distances.txt
```

PDF 本身按既有约定不入库。

### 1.3 文献笔记的关键结论

- `docs/literature/notes/ono-1996-concordant.md` 已确认：
  - Ono 1996 模型 `E_Q(M,N)` 与本项目 `E_{A,B}` 在 `M=A^2, N=B^2` 取值下相同
  - `rank > 0 ⇔ Euler concordant form 有无限 primitive 解`
  - 但 Ono 的 primitive solution 是一般 `(X,Y,Z,W)`；本项目的 multi-N 还要求落在 `Y=1` / `x=N^2` 的稀有截面上
  - torsion 类对应的是平凡解，正秩仍然是“多解”的真正来源

- `docs/literature/notes/knaf-selder-spindler.md` 已确认：
  - KSS 2019 不是 rank 判定算法，而是“在已知/预期正秩时找小高度有理点”
  - homogeneous-space 算法对 rank>=2 的独立点搜索最有意义
  - 适用于 `(153, 560)` 这类 Mordell-Weil 结构需要审计的样本

- 其余三篇定位较外围，列入参考。

### 1.4 术语澄清

引入并写进 strategy 文档的关键概念：

```text
strongly concordant pair  正秩 concordant 曲线 (Ono / Selder-Spindler 文献用法)
half-points Q_N           满足 2Q_N = P_N 的点（每个 concordant N 点都是 double）
squarefree signature      Q_N 的 (x, x+A^2, x+B^2) mod squares 三元组
homogeneous-space class   2-descent 中独立点所属的二次扩张类
```

`docs/MULTI_CONCORDANT_N_STRATEGY.md` 第 3.5、3.6 两节专门记录这些。

## 2. results 目录的整理

### 2.1 人类可读 + 机器可读的索引

```text
results/README.md      authoritative artifact 的人工说明
results/catalog.json   由 build_results_catalog.py 生成的机器可读清单
```

### 2.2 catalog 与 multi-concordant 数据集模块

新增 `src/rational_distance/results/` 包：

```text
__init__.py
catalog.py              CuratedArtifact / ResultsCatalog / build_results_catalog
multi_concordant.py     MultiConcordantPair, lookup_multi_concordant_pair, ...
```

把 `multi_concordant_N_max10000.jsonl` 注册为 authoritative，并提供按 `(A, B)` 反向查询的索引 API。

### 2.3 short, reusable 的 half-point 模块

`src/rational_distance/concordant/half_points.py` 提供：

```text
enumerate_half_points_for_concordant_N(A, B, N)  ->  list[HalfPointAnalysis]
HalfPointAnalysis.signature                       =  (sf(x), sf(x+A^2), sf(x+B^2))
squarefree_part(n)
```

并以 `(153, 560, 204)` 已知 half-point `(19992, -17013192)` 作为 TDD 的金样本。

### 2.4 三个 CLI 入口

```bash
uv run python scripts/build_results_catalog.py
uv run python scripts/lookup_multi_n.py 153 560
uv run python scripts/analyze_multi_n_half_points.py 153 560
```

涵盖：catalog 生成、ground-truth 反查、half-point + signature 分析。

### 2.5 测试

新增三组 TDD：

```text
tests/test_results_catalog.py
tests/test_multi_concordant_results.py
tests/test_half_points.py
```

`test_half_points` 直接断言 `(153, 560, 204)` 产出 8 个 half-points，包含已知整点 `(19992, -17013192)`。

## 3. 战略文档结构化

### 3.1 strategy 文档大改

`docs/MULTI_CONCORDANT_N_STRATEGY.md` 现在包含：

```text
1   实验事实 + (153, 560) 数据
2   Harborth 4-chain 的必要条件
3   椭圆曲线翻译
3.5 文献定位：multi-N 是正秩 concordant curve 的特殊点问题
3.6 两下降视角：每个 concordant N 点本身都是 double
4   反例为什么更难出现
5   下一阶段任务 A-E
6   优先级
```

并嵌入 ground-truth storage 段，把 catalog/lookup/half-point 三个 CLI 入口固定下来。

### 3.2 筛选阶梯文档

新建 `docs/MULTI_N_FILTER_LADDER.md`，把全部筛选层和执行策略明确成阶梯：

```text
L0  reduced coprime pair                    ~30,000,000
L1  >=1 concordant N                          稀少
L2  >=2 concordant N (multi-N pair)              854
L3  >=3 concordant N (k=3)                        26
L4  multi-N + closure                              0
L5  Harborth 4-chain                          目标
```

并把策略 A（慢路 / 暴力）和策略 B（pivot-on-N，wl048 实施）作为两种执行选择对照。

## 4. 静态分析与命令行问题

顺手收掉：

- `tests/test_pdf_text.py` 与 `src/.../pdf_text.py`、`scripts/extract_pdf_text.py` 中 basedpyright 抱怨的若干警告
- 长命令阻塞终端的问题，改成短命令 + 复用脚本

## 5. 验收

```text
uv run pytest -q                    220 passed
uv run ruff check <new files>       All checks passed
uv run python scripts/build_results_catalog.py
uv run python scripts/lookup_multi_n.py 153 560        正确返回
uv run python scripts/analyze_multi_n_half_points.py 153 560
    -> 8 half-points × 3 个 N，签名与 strategy 文档 3.6 节一致
```

## 6. 与 wl048 的关系

本 worklog 写完，下一步即 wl048：在阶梯文档第 4 节定义的“切入点 = L1 之前”动手实现策略 B 的 v0。

## 文件

新增模块：

```text
src/rational_distance/literature/__init__.py
src/rational_distance/literature/pdf_text.py
src/rational_distance/results/__init__.py
src/rational_distance/results/catalog.py
src/rational_distance/results/multi_concordant.py
src/rational_distance/concordant/half_points.py
```

新增脚本：

```text
scripts/extract_pdf_text.py
scripts/build_results_catalog.py
scripts/lookup_multi_n.py
scripts/analyze_multi_n_half_points.py
```

新增/更新文档：

```text
docs/MULTI_CONCORDANT_N_STRATEGY.md       更新
docs/MULTI_N_FILTER_LADDER.md             新建
docs/literature/notes/ono-1996-concordant.md          更新
docs/literature/notes/knaf-selder-spindler.md         更新
docs/literature/README.md                 更新
docs/literature/pdfs/README.md            更新
docs/literature/pdfs/.gitignore           更新
docs/literature/pdfs/*.txt                新增
results/README.md                         新建
results/catalog.json                      新建（自动生成）
```

新增测试：

```text
tests/test_pdf_text.py
tests/test_results_catalog.py
tests/test_multi_concordant_results.py
tests/test_half_points.py
```
