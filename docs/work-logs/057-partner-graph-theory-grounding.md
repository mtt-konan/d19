# wl057 — Partner Graph 理论 grounding：对接 Halbeisen-Hungerbühler 系列

## 触发

用户在 wl056 数据出来之后明确说：

> "我觉得需要整理一下理论部分了，不能再这样一直来回打转了，我觉得这个互为 pair
> 和图的性质比较有意思，但是需要先把理论部分整理好。如果可以的话你可以看看项目里
> 的论文，或者看看网上是否有类似的理论，就不用我们自己从头开始写理论了。"

也就是说：数据层已经积累足够（wl048-056 8 个 worklog），是时候停下扫描、把术语对齐
到现有文献，避免之后讨论时还在重新发明轮子。

## 工作

### 1. 复盘项目内已有理论积累

阅读以下文档确认 d19 已有的理论基础：

- `docs/MATH.md §8` — 椭圆曲线 concordant 分析（最完整的代数推导）
- `docs/MULTI_CONCORDANT_N_STRATEGY.md` — multi-N 战略框架 + half-points
- `docs/MULTI_N_FILTER_LADDER.md` — 筛选层级
- `docs/THEORY_DIRECTIONS.md` + `THEORY_DIRECTIONS_ADVANCED.md` — 理论方向地图
- `docs/literature/notes/ono-1996-concordant.md` — Ono framework
- `docs/literature/notes/knaf-selder-spindler.md` — KSS algorithm + homogeneous space
- `docs/literature/notes/bremner-ulas-2016.md` — 5-vertex rational distance

**结论**：项目里已经有 Ono / KSS / Bremner-Ulas 的笔记，但缺**partner identity
和 K_n 等价定理的代数 framing**。partner pair / K_n 是 wl054-055 才引入的术语，
没有跟现有文献做严格对接。

### 2. 网上搜索发现 Halbeisen-Hungerbühler 系列

`search_web` 搜索 "Pythagorean pair graph clique multi-concordant elliptic curve rank"
立即命中：

- **arXiv:2101.08163 — Halbeisen, Hungerbühler (2021) "Pairing Pythagorean Pairs"**
- **arXiv:2405.12989 — Halbeisen, Hungerbühler, Zargar (2024) "Pairing Powers of Pythagorean Pairs"**

两篇论文恰好用我们 d19 的椭圆曲线 E_{A, B}（他们记 Γ_{a, b}），定义了
"double-pythapotent / quadratic-pythapotent / pythapotent of degree h" 概念，
证明这些性质等价于 Γ 正秩。是与 d19 **直接对接**的论文。

下载 PDF + 提取文本：

```bash
curl -sL -o docs/literature/pdfs/halbeisen-hungerbuhler-2021-pairing-pythagorean-pairs.pdf \
     https://arxiv.org/pdf/2101.08163
curl -sL -o docs/literature/pdfs/halbeisen-hungerbuhler-voznyy-2024-pairing-powers.pdf \
     https://arxiv.org/pdf/2405.12989
uv run python scripts/extract_pdf_text.py docs/literature/pdfs/halbeisen-*.pdf
```

### 3. 精读：Γ_{a, b} ≡ E_{A, B}

```text
Halbeisen-Hungerbühler 2021                d19 (docs/MATH.md §8)
─────────────────────────────────         ────────────────────────────
Γ_{a, b}: y² = x³ + (a² + b²) x²           E_{A, B}: Y² = X(X + A²)(X + B²)
                  + a² b² x                       = X³ + (A² + B²) X²
        = x(x + a²)(x + b²)                          + A² B² X
```

**完全同一个椭圆曲线，只是符号差异（大小写）**。这意味着 H-H 的所有 Lemma / 
Proposition / Theorem 都可以在 d19 直接使用。

但有**关键差别**：

- H-H 要求 (a, b) **自身**是 Pythagorean pair (a² + b² = □)
- d19 不要求 (A, B) Pythagorean

这导致 torsion 分析、特殊点类型都不同：

- H-H：关心**一般 rational point** 在 Γ_{a, b}（与 double-pythapotent 配对）
- d19：关心**square-x rational point**（即 x = N², 对应 concordant N）

两者是**同一曲线上的不同特殊点类型问题**。

### 4. 输出三个文档

#### `docs/literature/notes/halbeisen-hungerbuhler-2021.md` (新建)

笔记内容：abstract、关键定义、Theorem 2 / 8、Proposition 1 (torsion)、
精确字典对齐 d19 ↔ H-H。

#### `docs/literature/notes/halbeisen-hungerbuhler-voznyy-2024.md` (新建)

笔记内容：推广到 degree h 的 Theorem 2、具体例子 (3, 4) cubic-pythapotent、
Corollary 7/8 参数化判据。

#### `docs/PARTNER_GRAPH_THEORY.md` (新建，本次主要交付物)

8 章 ~350 行：

```text
0. 字典: d19 术语 ↔ 文献术语
1. 范围与不在范围
2. 核心定义:
   2.1 Pythagorean graph G_P
   2.2 concordant N (Ono framework)
   2.3 multi-N pair
   2.4 partner pair (d19 wl054)
   2.5 partner identity (wl054 实证、wl055 数学化)
   2.6 partner graph G_M
   2.7 K_n subgraph (wl055)
   2.8 partner graph BFS (用户 wl056 提出)
3. 与文献的精确对接:
   3.1 椭圆曲线方程完全同构
   3.2 Torsion 群
   3.3 P_N ∈ 2E(ℚ) (Ono Prop 1)
   3.4 与 Halbeisen-Hungerbühler 的 pythapotent 关系
   3.5 与 Bremner-Ulas 2016 rational distance graph 的关系
4. 新观察 vs 已知结果（贡献边界）
5. 反例搜索的代数翻译:
   5.1 Harborth 4-chain ↔ multi-N + closure 翻译
   5.2 当前数据的反例排除范围
   5.3 K_n 高阶与反例的关系
   5.4 K_8 实例的 closure 状况（已验证全部失败）
6. 未解决的理论问题
7. 文献清单
8. 下一步路径
```

## 关键结论

1. **partner identity 不是新定理**，是 Ono framework 内 K_{2, 2} 嵌入对称性的
   自然推论。但 d19 wl054 是**首次把它用作搜索加速器**（从 catalog 反推非互素
   multi-N）。

2. **K_n 等价定理**（wl055）同样是 partner identity 的直接对偶。wl055 的贡献是
   把"K_n shared-partner 枚举"明确等价于"k=n multi-N pair 枚举"，把图论问题
   降级为 1 维问题。

3. **partner graph BFS**（wl056 起）是 G_M（multi-N pair 图）上的标准遍历。
   wl056 数据表明 G_M 存在**孤立 cycle**（如 (15, 48) ↔ (20, 36) 完全与 catalog 断开），
   所以单凭 BFS 不能枚举全部 multi-N pair。

4. **Halbeisen-Hungerbühler 的 double-pythapotent ≠ d19 的 multi-N**：
   - H-H 要 (a, b) Pythagorean + 配对 (k, l)
   - d19 要 (A, B) 任意 + 公共邻居 N
   - 两者都对应 Γ_{a, b} = E_{A, B} 有非平凡有理点，但关心**不同类型的点**

5. **反例搜索的代数翻译**（PARTNER_GRAPH_THEORY.md §5.1）：

   ```text
   Harborth 反例 ⇔ ∃ multi-N pair (A, B) 含 N₁, N₂ 满足 N₁ + N₂ = A + B
   ```

   在 max_hyp=100000 全 catalog（互素 + partner 反推非互素）+ wl056 M=2000 直接
   非互素扫描中，**没有任何 multi-N pair 满足 closure**。

6. **K_8 实例都不给反例**：
   - (55440, 445536) k=8 的 28 个 (N_i, N_j) 没一对命中 N_i + N_j = A + B = 500976
   - (58800, 98280) k=8 的 28 个同样全部 miss

## 没做的事 (留给后续 worklog)

1. **跑 K_8 / K_7 实例的 PARI ellrank** —— wl055 钩子 + PARTNER_GRAPH_THEORY §8。
2. **M=10000 直接非互素扫描** —— wl056 钩子。
3. **(15, 48) ↔ (20, 36) 类孤立 cycle 的代数解释** —— 为什么 catalog 不能到达？
4. **closure 局部障碍** (mod p 是否就能排除？) —— PARTNER_GRAPH_THEORY §6 Q1.
5. **partner graph G_M 全连通分量统计** —— PARTNER_GRAPH_THEORY §6 Q2.

## 文件

```text
docs/literature/notes/halbeisen-hungerbuhler-2021.md            新建笔记
docs/literature/notes/halbeisen-hungerbuhler-voznyy-2024.md     新建笔记
docs/literature/pdfs/halbeisen-hungerbuhler-2021-pairing-pythagorean-pairs.pdf  下载
docs/literature/pdfs/halbeisen-hungerbuhler-2021-pairing-pythagorean-pairs.txt  抽取
docs/literature/pdfs/halbeisen-hungerbuhler-voznyy-2024-pairing-powers.pdf      下载
docs/literature/pdfs/halbeisen-hungerbuhler-voznyy-2024-pairing-powers.txt      抽取
docs/literature/README.md                                       新增两行
docs/literature/timeline.md                                     新增"2020s pythapotent"节
docs/PARTNER_GRAPH_THEORY.md                                    新建理论整合主文档
docs/work-logs/057-partner-graph-theory-grounding.md            本文件
```

## 元注：这次工作不跑数据

用户明确指示"不能再这样一直来回打转"。本次 worklog 的产出是**纯文档**：
- 0 行新数据
- 0 行新代码
- 7 个新/更新文档
- 234 测试不受影响

目的是把术语对齐到文献，让后续讨论有共同的概念基础。下一次再做实证（K_8
ellrank 审计、M=10000 扫描、closure 局部障碍）时，可以直接引用本次写的术语。
