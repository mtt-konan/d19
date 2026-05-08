# 方法对比与选型

这份文档只做一件事：把项目里几条主要方法的实测数据放在一起，方便下次直接选路。

先看一句最重要的话：

- 这 5 个子命令不在解同一个子问题
- 所以不能拿一个数字给它们排总名次
- 你应该先看它在找什么，再看速度和产出

## 一、先把 5 条方法分成 3 组

### 1. 三顶点方向

- `parametric`
- `ec`

这两条线都在找“正方形里有一个点，它到 4 个顶点里先有 3 个距离是有理数”的样例。

### 2. 四边链方向

- `chain`
- `chain-fast`

这两条线都和四条边闭环有关。

- `chain` 更像长方形 4-cycle 搜索器
- `chain-fast` 直接瞄正方形主问题

### 3. `(A,B)` / 共同腿方向

- `concordant`

这条线固定一对 `(A,B)`，问是否存在共同腿 `N`，使：

- `N^2 + A^2` 是平方
- `N^2 + B^2` 是平方

它更像诊断工具，不像直接出最终解的搜索器。

## 二、这份对比里的基准怎么跑的

为了先得到一份可复用的参照，这里固定用了下面这组小范围基准：

### 三顶点方向

```bash
uv run python scripts/search.py parametric --max-m 20 --max-k-num 160 --max-k-den 160 --backend numpy --no-progress --top 5
uv run python scripts/search.py ec --max-m 20 --max-k-num 160 --max-k-den 160 --max-steps 8 --backend numpy --no-progress --top 5
```

### 四边链方向

```bash
uv run python scripts/search.py chain --max-val 500 --no-progress --top 5
uv run python scripts/search.py chain --max-val 500 --require-square --no-progress --top 5
uv run python scripts/search.py chain-fast --max-hyp 500 --backend auto --workers 1 --no-progress --top 5
```

### `(A,B)` / 共同腿方向

```bash
uv run python scripts/search.py concordant --max-hyp 500 --ec-bound 100000 --profile --no-progress --top 5
uv run python scripts/search.py concordant --max-hyp 500 --ec-bound 100000 --profile --safe-pair-sieve --no-progress --top 5
uv run python scripts/search.py concordant --max-hyp 500 --ec-bound 400000 --no-progress --top 0
```

这份表只适合拿来做“方法选型参考”，不适合当最终性能结论。

## 三、实测总表

### 1. 三顶点方向：`parametric` 和 `ec`

| 方法 | 时间 | 产出对象 | 数量 | 备注 |
|------|-----:|----------|-----:|------|
| `parametric` | `0.245s` | `3/4` 有理距离点 | `11` | 这次跑得更全一些 |
| `ec` | `0.042s` | `3/4` 有理距离点 | `6` | 这次更快 |

要注意两件事：

- 这两条线这次都只找到 `3/4` 点，没有 `4/4`
- 它们这次产出的点集不是同一批

我按 `(x,y,dA,dB,dC,dD)` 精确比过一遍：

- `parametric` 总数：`11`
- `ec` 总数：`6`
- 交集：`0`

所以你不能把它们理解成“同一批结果谁更快”。  
更准确的理解是：它们都在三顶点方向上产样例，但走的是不同轨道。

### 2. 四边链方向：`chain` 和 `chain-fast`

| 方法 | 时间 | 产出对象 | 数量 | 备注 |
|------|-----:|----------|-----:|------|
| `chain` | `0.006s` | 长方形 4-cycle | `10` | 不强制正方形条件 |
| `chain --require-square` | `0.005s` | 正方形 4-cycle | `0` | 这次没有命中 |
| `chain-fast` | `0.006s` | 正方形主问题基线搜索 | `0` | 和上面这次一致 |

这里能直接比较的是：

- `chain --require-square`
- `chain-fast`

因为这两条都在盯正方形版本。  
这次小范围里，两者都没有结果。

普通 `chain` 的 `10` 条结果不能直接拿来和 `chain-fast=0` 硬比。  
原因很简单：`chain` 默认找的是长方形四边闭环，不是正方形最终条件。

### 3. `(A,B)` / 共同腿方向：`concordant`

| 模式 | 时间 | 原始 pair 数 | 实际分析 pair 数 | 至少有 1 个 `N` 的 pair | 完整 chain-compatible |
|------|-----:|-------------:|-----------------:|------------------------:|----------------------:|
| `concordant` | `6.18s` | `6172` | `6172` | `498` | `0` |
| `concordant --safe-pair-sieve` | `0.57s` | `6172` | `540` | `81` | `0` |

这张表最容易看错，所以把口径写死：

- 左边这一行看的是“全量 concordant 现象”
- 右边这一行看的是“更偏完整链导向的筛后 pair”

所以 `498 -> 81` 不是结果丢了，而是语义变了。  
右边这一行先砍掉了很多不适合继续走完整链的 pair。

## 四、`concordant` 里，一个 pair 常见有几个 `N`

这个问题单独列出来，因为它最容易和旧 `chain` 的直觉混掉。

### 1. `ec_bound = 100000`

在 `max_hyp = 500` 时，`6172` 个 reduced `(A,B)` pair 的分布是：

| `concordant_n` 个数 | pair 数 |
|---------------------|--------:|
| `0` | `5674` |
| `1` | `489` |
| `2` | `9` |

### 2. `ec_bound = 400000`

同样在 `max_hyp = 500` 时，分布变成：

| `concordant_n` 个数 | pair 数 |
|---------------------|--------:|
| `0` | `5286` |
| `1` | `864` |
| `2` | `22` |

这组数据说明两件事：

- 默认小范围里，大多数 pair 根本没有共同腿 `N`
- 有两个 `N` 的 pair 确实存在，但数量很少

这也是为什么你会觉得：

- 三顶点方法很快出很多样例
- `concordant` 很慢，却很少直接给出“像完整链那样”的东西

## 五、几个最有代表性的例子

### 1. `parametric` 样例

点：

- `P = (65/44, 18/11)`

距离：

- `dA = 97/44`
- `dB = 75/44`
- `dC = 35/44`
- `dD` 不是有理数

这就是典型的 `3/4` 三顶点样例。

### 2. `ec` 样例

点：

- `P = (28/15, 16/9)`

距离：

- `dA = 116/45`
- `dB = 89/45`
- `dD = 91/45`
- `dC` 不是有理数

这也是 `3/4` 样例，但它不是上面那条 `parametric` 结果的简单重写。

### 3. `chain` 样例

长方形 4-cycle：

- `(25, 60, 91, 312)`

意思是下面这四个勾股三角形首尾接起来：

- `25^2 + 60^2 = 65^2`
- `60^2 + 91^2 = 109^2`
- `91^2 + 312^2 = 325^2`
- `312^2 + 25^2 = 313^2`

这条结果很有代表性，因为它已经是完整四边闭环了。

### 4. `concordant` 的单腿样例

pair：

- `(A,B) = (5,9)`

共同腿：

- `N = 12`

意思是：

- `12^2 + 5^2 = 13^2`
- `12^2 + 9^2 = 15^2`

这说明 `(5,9)` 这对数共享一条共同腿 `12`。  
但这还只是半成品，不等于完整四边链。

### 5. `concordant` 的双腿样例

pair：

- `(A,B) = (25,91)`

共同腿：

- `N = 60`
- `N = 312`

这组最值得记住，因为它和上面的 `chain` 样例正好对应起来：

- `(25,60,91,312)`

也就是说，一个 pair 如果有两条合适的共同腿，就有机会拼回旧 `chain` 里的完整 4-cycle。

## 六、下次怎么选方法

如果你想：

- 快速拿很多三顶点样例，用 `parametric`
- 从三顶点 seed 往外扩更多轨道，用 `ec`
- 快速看真实的四边闭环结构，用 `chain`
- 直接做正方形主问题基线搜索，用 `chain-fast`
- 固定 `(A,B)` 研究共同腿 `N`，看它为什么活或为什么死，用 `concordant`

把这句话再压缩一下：

- `parametric / ec`：高产样例线
- `chain`：四边结构参考线
- `chain-fast`：最终主问题基线
- `concordant`：`(A,B)` 诊断线

## 七、当前最容易选错的地方

### 1. 不能把 `parametric / ec` 和 `chain-fast` 直接按数量比较

原因是它们在找不同对象：

- 前者找 `3/4` 点
- 后者找最终正方形条件

### 2. 不能把 `chain=10` 和 `chain-fast=0` 直接说成谁更强

原因是：

- `chain` 默认找长方形 4-cycle
- `chain-fast` 直接找正方形主问题

### 3. 不能把 `concordant` 里的 “有 1 个 `N`” 当成已经有完整链

因为完整链至少还要把另外一侧 `b = A + B - N` 拉回来检查。  
这一步会砍掉绝大多数只靠共同腿活下来的 pair。
