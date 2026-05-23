# 术语对照表（d19 项目专用）

这份文档只回答一件事：项目里那些数学/工程英文术语，对应中文叫什么、一句话是什么意思。

对照原则：

- 优先用中文叫法（左边给英文，右边给中文 + 一句话解释）
- 给每个术语标注**在 d19 项目里第一次正式出现的位置**，方便溯源
- 不写完整数学定义，只够"日常对话用"

如果讨论时双方默契用同一套词，下面这张表是基准。

---

## 1. 椭圆曲线与有理点

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| elliptic curve `E` | **椭圆曲线** | 形如 $y^2 = $ 三次多项式的光滑曲线；d19 里专指 `y² = x(x + A²)(x + B²)` | [MATH.md](MATH.md) §3 |
| `E(\mathbb{Q})` | **E 的有理点群** | 椭圆曲线上坐标都是有理数的点构成的群 | [MATH.md](MATH.md) §3 |
| rank | **秩** / "独立解个数" | $E(\mathbb{Q})$ 里独立有理点的个数（不算挠点） | [wl 033](work-logs/033-dual-ec-probe.md) |
| generator | **基础解** | 由它能生成 $E(\mathbb{Q})$ 中所有有理点的几个特殊点 | [wl 033](work-logs/033-dual-ec-probe.md) |
| torsion / `E[n](\mathbb{Q})` | **挠点** / "n-挠点" | 满足 $nP = O$ 的有理点；d19 case 始终 $E[2](\mathbb{Q}) = (\mathbb{Z}/2)^2$ | [wl 035](work-logs/035-pari-selmer-api.md) |
| height (of a point) | **高度** | 衡量有理点"复杂程度"的数；坐标分母分子越大越高 | [wl 031](work-logs/031-heegner-height-diagnostic.md) |

## 2. 局部 vs 全局，沙群与塞尔默群

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| local solubility | **局部可解** | 在某个 $p$ 进数 $\mathbb{Q}_p$ 或实数 $\mathbb{R}$ 上有点 | [wl 037](work-logs/037-finite-descent-on-hard-cases.md) |
| global solubility | **全局可解** | 在有理数 $\mathbb{Q}$ 上有点 | [wl 037](work-logs/037-finite-descent-on-hard-cases.md) |
| Hasse principle | **哈塞原则** | "局部都可解 ⟹ 全局可解"——很多场景错 | [wl 037](work-logs/037-finite-descent-on-hard-cases.md) |
| Sha / Ш / `Sha(E)` | **沙群** | 局部都可解但全局无解的"覆盖"集合；衡量 Hasse 原则失败程度 | [wl 035](work-logs/035-pari-selmer-api.md) |
| Sha[2] / `Sha(E)[2]` | **沙群的 2 部分** | 沙群里阶数 ≤ 2 的元素 | [wl 036](work-logs/036-compute-rank-fix-and-ell2cover-batch.md) |
| Selmer group / Sel(E, n) | **塞尔默群** | 局部上每个素数都没破绽的 n-覆盖集；包含沙群 | [wl 035](work-logs/035-pari-selmer-api.md) |
| 2-cover / 2-descent | **两层覆盖 / 二层下降** | 通过"开根号"得到的辅助曲线，用来约束 $E(\mathbb{Q})$ | [wl 035](work-logs/035-pari-selmer-api.md) |
| 2-isogeny | **2-同源映射** | 椭圆曲线之间一个 2-to-1 的特殊映射 | [wl 035](work-logs/035-pari-selmer-api.md) |
| 2-isogeny cover | **2-同源覆盖** | ell2cover 输出的那些四次方程曲线 | [wl 036](work-logs/036-compute-rank-fix-and-ell2cover-batch.md) |
| sha2_lower | **沙下界** | PARI 算出的 $\dim_{\mathbb{F}_2} \Sha[2]$ 的最小可能值 | [wl 036](work-logs/036-compute-rank-fix-and-ell2cover-batch.md) |
| Cassels-Tate pairing | **CT 配对** | 一个能从一对覆盖算出 0 或 1/2 的工具，用来证沙群非平凡 | [PROJECT_STATUS](PROJECT_STATUS.md) §9.9 |

## 3. PARI/GP 工具

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| `ellrank(E, effort)` | **秩计算** | PARI 算 $\text{rank}(E)$ 的内置函数；返回 `[rank_lo, rank_hi, sha2_lower, gens]` | [wl 035](work-logs/035-pari-selmer-api.md) |
| effort | **力度** | PARI 算法的努力等级（1 浅，3 深） | [wl 033](work-logs/033-dual-ec-probe.md) |
| `ell2cover(E)` | **两层覆盖工具** | PARI 返回所有 2-同源覆盖的四次方程 | [wl 036](work-logs/036-compute-rank-fix-and-ell2cover-batch.md) |
| `hyperellratpoints(g, h)` | **曲线找点** | PARI 在 $y^2 = g(x)$ 上找 $|x|, |y| \leq h$ 范围内的有理点 | [wl 036](work-logs/036-compute-rank-fix-and-ell2cover-batch.md) |
| `compute_rank` | **秩工具封装** | 项目里包装 `ellrank` 的 4 元组接口 | [wl 035](work-logs/035-pari-selmer-api.md) |

## 4. d19 项目特有概念

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| concordant form | **协同型** / "共轭对" | $\exists N: N^2+A^2, N^2+B^2$ 同为平方的 $(A, B)$ 对 | [MATH.md](MATH.md) §2 |
| chain / 4-chain | **链 / 4-链** | 4 个边距离都是有理数的四顶点配置 | [DIRECTIONS](DIRECTIONS.md) |
| hard_case | **疑难对** | 暂时既没找到解也没证无解的 $(A, B)$ 对 | [wl 030](work-logs/030-large-range-proof-stats.md) |
| no_solution | **已证无解** | 用 cheap sieve（mod 1680, modular obstruction）证完全没有 N 满足条件的 (A, B) | [wl 030](work-logs/030-large-range-proof-stats.md) |
| safe_sieve | **安全前筛** | 不会误杀真解的快速过滤（mod 8, mod 1680 等） | [CHAIN_FAST_SAFE_FILTERS](CHAIN_FAST_SAFE_FILTERS.md) |
| max_hyp | **最大斜边** | 扫描时给 $\sqrt{A^2+B^2}$ 设的上界 | [wl 030](work-logs/030-large-range-proof-stats.md) |
| chain-fast | **基线搜索器** | 当前最可信的 4 顶点搜索实现 | [DIRECTIONS](DIRECTIONS.md) §1.4 |

## 5. 模式狩猎 / 统计

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| chi² test | **卡方检验** | 看两组分布差异是否显著 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| feature / fingerprint | **特征 / 特征向量** | 用一组数刻画 (A, B) 的属性（squarefree、max_exp 等） | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| stratify | **分层** | 按某个特征把样本切成子组分别看 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| outlier | **异常项** | 偏离一般模式的特殊 case | [wl 039](work-logs/039-ell2cover-sha2-explicit.md) |
| n_covers | **覆盖数** | `ell2cover(E)` 返回的覆盖个数 | [wl 039](work-logs/039-ell2cover-sha2-explicit.md) |
| n_without_pt | **无点覆盖数** | 没找到有理点的覆盖个数（h=10⁴ 或 10⁵ 内） | [wl 039](work-logs/039-ell2cover-sha2-explicit.md) |
| max_exp(n) | **最大素幂次** | n 的素因子分解里出现的最大指数 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| squarefree | **无平方因子** | 素因子分解里所有指数都是 1 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |

## 6. 重型工具（长期方向）

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| Heegner point | **复乘点** / "Heegner 点" | 用复数二次域构造的特殊高度有理点，对秩=1 case 特效 | [THEORY_DIRECTIONS_ADVANCED](THEORY_DIRECTIONS_ADVANCED.md) |
| Mordell-Weil sieve | **MW 高度筛** | 用已知基础解逆向筛掉覆盖上不存在的点的位置 | [wl 039](work-logs/039-ell2cover-sha2-explicit.md) |
| Chabauty method | **Chabauty 方法** | 用 p 进解析方法限制曲线上有理点 | [THEORY_DIRECTIONS_ADVANCED](THEORY_DIRECTIONS_ADVANCED.md) |
| Brauer-Manin obstruction | **BM 障碍** | 比沙群更细的"局部-全局失败"度量 | [THEORY_DIRECTIONS_ADVANCED](THEORY_DIRECTIONS_ADVANCED.md) |
| K3 surface | **K3 曲面** | 高维代数几何对象；4-chain 问题在某种意义上是 K3 上的有理点问题 | [THEORY_DIRECTIONS_ADVANCED](THEORY_DIRECTIONS_ADVANCED.md) |
| finite descent | **有限下降** | Peschmann §7 风格的"枚举有限多个候选" 方法 | [wl 037](work-logs/037-finite-descent-on-hard-cases.md) |
| Stoll sieve | **Stoll 筛** | 类似 MW 高度筛但更精细的高度约束方法 | [PROJECT_STATUS](PROJECT_STATUS.md) §9.9 |

## 7. 工程实现术语

| 英文 | 中文叫法 | 一句话意思 | 首现 |
|---|---|---|---|
| worker | **单任务子进程** | 一次只处理一个 (A, B) 的脚本 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| driver / batch_*_v2 | **批量调度器** | 把任务分发给多个 worker，处理超时和续跑 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| timeout-safe | **超时安全** | 单个任务卡住不影响整体扫描 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| subprocess isolation | **子进程隔离** | 用独立子进程跑 PARI，避免 cypari2 内存泄漏污染主进程 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |
| JSONL | **JSON 行格式** | 每行一个 JSON 对象的纯文本格式，便于流式 append 和 grep | [wl 030](work-logs/030-large-range-proof-stats.md) |
| resume / resumable | **断点续跑** | 中断后从上次进度继续，不重复已完成的任务 | [wl 038](work-logs/038-large-scale-sha2-pattern-hunt.md) |

---

## 用法说明

- 写 worklog 或 commit message 时，**第一次出现英文术语**带中文括号；后续可直接用中文
- 例如：第一次写 `Sha[2]（沙群的 2 部分）`，后续直接写"沙[2]"
- PARI 函数名、git 命令等代码符号保留英文（换中文反而看不懂）
- 见到不熟的术语 → 查这张表 → 如果表里没，补一行
