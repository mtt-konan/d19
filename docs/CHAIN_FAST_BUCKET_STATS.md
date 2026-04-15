# Chain-Fast 结构桶统计

这份文档讲的是一件很具体的事：

- 这版不是直接加新剪枝
- 而是先把 `chain-fast` 扫过的 pair，按结构分桶记下来
- 以后要不要剪掉某一类 pair，先看数据再说

## 为什么先做这个

前面已经知道几件事：

- `chain-fast` 现在的主复杂度还是 `O(n^2)`
- `mod` 预筛能少做一部分 `C3`，但总时间不一定更快
- 真正值钱的优化，更可能来自“哪类 pair 基本没戏”

问题在于，之前缺的不是猜想，而是证据。

比如你会想问：

- `g = gcd(t1, s2)` 大的时候，是不是更容易活到 `C3`
- `s1-t1`、`s2-t2` 的某些符号或大小区间，是不是几乎必死
- 某些模类组合只是出现得多，还是真的更有命中率

没有分桶统计，这些都只能靠感觉。

## 这版到底存了什么

命令开关：

```bash
uv run python scripts/search.py chain-fast --max-hyp 5000 --db results/chain.db --bucket-stats
```

注意：

- `--bucket-stats` 现在必须和 `--db` 一起用
- 它只存聚合结果，不存每一对 `(T1,T2)` 的明细
- 默认关闭，不改原来的搜索语义

每个桶都会累计这些量：

- `n_total`
- `n_after_basic`
- `n_c3_pass`
- `n_c4_pass`
- `n_near_miss`
- `best_sq4_deficit`
- `best_sq3_deficit`
- 一条最接近解的 sample：`(a,b,c,d)`

这里的意思很简单：

- `n_total`：这一类结构一共出现了多少次
- `n_after_basic`：过了基础筛以后还剩多少
- `n_c3_pass`：真的过了 `C3`
- `n_c4_pass`：真的过了 `C4`
- `n_near_miss`：过了 `C3` 但死在 `C4`

所以后面分析时，最常看的比率就是：

- `c3_rate = n_c3_pass / n_after_basic`
- `near_miss_rate = n_near_miss / n_after_basic`

## 为什么不存全量 pair

原因很现实：

- 全量 pair 太大，长期积累很容易把库撑大
- 真正要找规律时，第一步通常不需要每条明细
- 先看“哪类结构命中率高/低”，就已经能筛掉很多没价值方向

所以这版采用折中方案：

- 扫描时做内存聚合
- run 结束后一次性写 SQLite
- 不在内层循环逐条写 DB

这样后面还能继续跑大范围，不会因为“想分析”先把 IO 弄炸。

不过要先说明一个后来的实测结果：

- 这套第一版聚合逻辑在 `max_hyp=100000` 上已经明显偏重
- 它更适合“定点采证据”，还不适合默认挂在所有长跑任务上

如果想直接看首轮实测读出了什么，可以看：

- [docs/CHAIN_FAST_STRUCTURE_FINDINGS.md](./CHAIN_FAST_STRUCTURE_FINDINGS.md)

## 三类固定桶

第一版固定只记三类，不开放自定义。

### 1. `g_bucket`

这里的 `g` 指：

```text
g = gcd(t1, s2)
```

分桶方式：

- `1` 到 `16` 单独记
- 再往上按区间记：`17-32`、`33-64`、`65-128`、`129-256`、`257-512`、`513+`

它主要想回答的是：

- `g` 小和 `g` 大，活下来的概率有没有明显差别

### 2. `delta_bucket`

这里看的是：

- `delta1 = s1 - t1`
- `delta2 = s2 - t2`

每个 `delta` 都记三件事：

- 符号：`pos` / `neg`
- 绝对值区间：`1-3`、`4-7`、`8-15`、`16-31`、`32-63`、`64-127`、`128+`
- `abs(delta) mod 8`

它主要想回答：

- 哪些“差值结构”其实一开始就不值得配对

### 3. `residue_bucket`

这里直接记：

- `s1 mod 8`
- `t1 mod 8`
- `s2 mod 8`
- `t2 mod 8`

它不是最终答案，但很适合先看：

- 哪些模类组合只是常见
- 哪些模类组合是真的更容易过 `C3`

## 怎么分析

分析入口：

```bash
uv run python scripts/analyze_chain_db.py --db results/chain.db --run latest
uv run python scripts/analyze_chain_db.py --db results/chain.db --run latest --bucket-type g_bucket
uv run python scripts/analyze_chain_db.py --db results/chain.db --run latest --min-after-basic 1000 --top 20
```

第一版只做终端摘要和可选 JSON：

```bash
uv run python scripts/analyze_chain_db.py --db results/chain.db --out-json chain_analysis.json
```

默认会忽略 `n_after_basic` 太小的桶，因为样本太小时很容易出现假象。

## 怎么读结果

一个桶排在前面，不一定说明“这类结构最好”，可能只是：

- 样本够多
- `C3` 命中率确实更高
- 或者 near-miss 更接近解

所以读结果时，至少同时看三件事：

- `n_after_basic` 有没有大到值得信
- `c3_rate` 是不是明显高于别的桶
- `best_sq4_deficit` 是不是反复接近 0

如果某类桶同时满足这几条，才值得继续往“新剪枝”方向推进。

## 这版的定位

这版不是为了立刻变快。

它的定位更像是：

- 给后续剪枝准备证据
- 给 triple 结构分析准备底座
- 把“感觉上这类 pair 没戏”变成能查、能比、能复现的统计结果

如果后面真要做更强的结构剪枝，这一步基本绕不过去。

但同样要记住：

- 这一步是分析底座，不是免费加速
- 真正长期长跑时，未必应该一直把 `--bucket-stats` 打开
