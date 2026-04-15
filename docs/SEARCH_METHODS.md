# 搜索方法词典

这份文档只解释项目里 5 个子命令分别做什么。  
它不负责决定当前主线，也不负责写项目现状。那些内容请看 [docs/DIRECTIONS.md](./DIRECTIONS.md) 和 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md)。

## 一、先看状态标签

当前统一状态是：

- `concordant` = `active`
- `chain-fast` = `baseline`
- `parametric` / `ec` / `chain` = `paused`

这里的意思不是“暂停的就没用了”，而是：

- `active`：当前最值得继续推进
- `baseline`：继续保留，负责做可信对照
- `paused`：先保留，不删，但不是当前主战场

## 二、五个子命令分别在做什么

### 1. `parametric`（`paused`）

命令：

```bash
uv run python scripts/search.py parametric --scale 200
```

大白话解释：

- 先从本原勾股数出发
- 再选一个有理比例
- 生成候选点
- 检查这个点到正方形顶点的距离里，有几个是有理数

它更像：

- 最直观的三顶点基线
- 一条方便做 CPU / `numpy` / `torch` 对照的工程路线

适合什么时候用：

- 想看三顶点解长什么样
- 想验证共享判定逻辑有没有写错
- 想做 CPU 和加速后端一致性对照

### 2. `ec`（`paused`）

命令：

```bash
uv run python scripts/search.py ec --max-m 30
```

大白话解释：

- 不是从零开始乱试
- 而是先从已有三顶点解里找 seed
- 再沿椭圆曲线轨道扩出更多相关解

它更像：

- 三顶点研究工具
- 轨道结构分析工具

适合什么时候用：

- 想研究某类三顶点 seed 怎么扩展
- 想把结果存进 SQLite 继续分析

### 3. `chain`（`paused`）

命令：

```bash
uv run python scripts/search.py chain --max-val 500
```

大白话解释：

- 它不直接找点坐标
- 而是改成找四个整数 `a,b,c,d`
- 要求四条边都能和相邻边拼成勾股对

也就是检查：

- `a^2 + b^2`
- `b^2 + c^2`
- `c^2 + d^2`
- `d^2 + a^2`

都是否为平方数。

要注意：

- 这条线默认更像“长方形问题”
- 只有再加上 `a + c = b + d`，才真正回到单位正方形主问题

适合什么时候用：

- 想理解四边闭环结构
- 想看 chain 化简前后的关系

### 4. `chain-fast`（`baseline`）

命令：

```bash
uv run python scripts/search.py chain-fast --max-hyp 20000
```

大白话解释：

- 不再直接枚举所有 `a,b,c,d`
- 而是枚举两组本原勾股数
- 由这两组数推出候选结构
- 再检查后面真正卡人的平方条件

这条线的特点是：

- 直接瞄准正方形主问题
- 覆盖比一般参数化搜索更完整
- 已经有 `numpy`、profile、SQLite、near-miss、结构桶统计这些工程底座

现在怎么理解它最合适：

- 它是当前最可信的基线搜索器
- 也是以后验证新剪枝、新数学条件时最该对照的地方

### 5. `concordant`（`active`）

命令：

```bash
uv run python scripts/search.py concordant --pair 264,420
```

大白话解释：

- 固定一组 `(A,B)`
- 看能不能找到共同腿 `N`
- 让 `N^2 + A^2` 和 `N^2 + B^2` 同时是平方

它对应的就是 concordant form / 椭圆曲线这条数论路线。

要注意：

- 它不是单纯再做一次搜索器
- 它更像分析工具
- 目标是弄清哪些 `(A,B)` 有戏，哪些从结构上就不值得继续配

## 三、常见使用场景速查

如果你的目标是：

- 看三顶点基线：用 `parametric`
- 看三顶点轨道：用 `ec`
- 看四边闭环长什么样：用 `chain`
- 做正方形主问题基线搜索：用 `chain-fast`
- 固定 `(A,B)` 研究共同腿 `N`：用 `concordant`

## 四、最容易混的地方

最容易混的是 `chain-fast` 和 `concordant`。

简单区分：

- `chain-fast` 是“从三元组对出发，直接搜正方形主问题”
- `concordant` 是“固定 `(A,B)` 后，研究共同腿 `N` 的数论结构”

它们不是互相取代，而是现在分工不同：

- `chain-fast` 做 `baseline`
- `concordant` 做 `active`

另外，`tmp.txt` 后面那条“固定 `(A,B)`，研究共同腿 `N`”的路线，本质上就属于现在的 `concordant` 主线，只是切入角度不同。

## 五、辅助脚本怎么理解

除了这 5 个子命令，项目里还有几类辅助脚本。它们不是新的搜索方法，只是配套工具：

- `scripts/analyze_ec_db.py`：分析 `ec` 的 SQLite 结果
- `scripts/analyze_chain_db.py`：分析 `chain-fast` 的 SQLite 结果
- `scripts/compare_parametric.py`：对照 CPU 和加速后端是否一致
- `scripts/visualize.py`：读取 JSON 结果并生成 HTML 可视化

最简单的理解方式是：

- 搜索本身，先看 `scripts/search.py`
- 结果分析和可视化，再看这些辅助脚本
