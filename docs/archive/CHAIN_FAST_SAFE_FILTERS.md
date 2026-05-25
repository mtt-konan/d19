# Chain-Fast 安全前筛说明

这份文档只回答三件事：

- 这版 `--safe-pair-sieve` 到底筛什么
- 为什么这些条件是“安全的必要条件”，不会误杀真正解
- 它在当前 Python 实现里到底有没有带来加速

结论先说：

- 这四条条件都可以直接证明，所以它们是**安全硬筛**
- 这版实现已经接到 `chain-fast --safe-pair-sieve` 里，但只支持 `backend=python`
- 它会把大约 `70.8%` 的 ordered pair 提前砍掉
- 但当前 wall time 明显更慢，所以它现在只能保留为**实验开关**

更关键的一点是：

- 三组基准里，`after_basic_filters` 和基线完全一样
- 这说明它虽然更早砍 pair，但砍掉的基本都是**现有 basic filter 本来就会便宜地排掉的 pair**
- 数学上是新结论，工程上暂时还不是更快的实现

## 一、记号和代码变量对齐

对一组 ordered triple pair

- `T1 = (s1, t1, h1)`
- `T2 = (s2, t2, h2)`

定义：

- `g = gcd(t1, s2)`
- `u = t1 / g`
- `v = s2 / g`
- `A = u * t2`
- `B = v * s1`
- `N = A + v * (s1 - t1)`

在代码里，这些变量对应的是：

- `src/rational_distance/chain_fast/kernel.py`
- `src/rational_distance/chain_fast/safe_pair_sieve.py`

`chain-fast` 后面真正要做的关键整数检查之一是：

- `C3: A^2 + N^2` 是否为完全平方数

这版安全前筛做的，就是在进入现有 basic filter 和 `C3` 之前，先用已经证明的必要条件排掉一批 pair。

## 二、朝向定义

本原勾股数一条腿一定奇、一条腿一定偶。这里固定记两种朝向：

- `OE`：`s` 奇，`t` 偶
- `EO`：`s` 偶，`t` 奇

项目里的 triple 生成器本来就会把 `(a, b, c)` 和 `(b, a, c)` 都列出来，所以朝向本身就是搜索状态的一部分，不是额外假设。

## 三、四条已经证明的必要条件

### 1. 同朝向 `(OE, OE)` 必死

若 `T1=OE` 且 `T2=OE`，那么：

- `t1` 偶，`s2` 奇，所以 `g = gcd(t1, s2)` 一定是奇数
- 因而 `u = t1 / g` 是偶数，`v = s2 / g` 是奇数
- 又因为 `t2` 偶、`s1` 奇，所以：
  - `A = u * t2` 是偶数
  - `B = v * s1` 是奇数

但 `chain-fast` 的现有 basic filter 里，首先就要求 `A` 和 `B` 同奇偶。  
这里它们一奇一偶，所以这一类 pair 不可能走到后面。

所以：

- `(OE, OE)` 可以安全剪掉

### 2. 同朝向 `(EO, EO)` 必死

这和上一条是对称的。

若 `T1=EO` 且 `T2=EO`，那么：

- `t1` 奇，`s2` 偶，所以 `g` 仍然只能是奇数
- 因而 `u` 是奇数，`v` 是偶数
- 又因为 `t2` 奇、`s1` 偶，所以：
  - `A = u * t2` 是奇数
  - `B = v * s1` 是偶数

同样得到：

- `A` 和 `B` 奇偶不同
- 这一类 pair 也一定过不了 basic filter

所以：

- `(EO, EO)` 也可以安全剪掉

### 3. 对 `T1=OE, T2=EO`，必须满足 `v2(t1) = v2(s2)`

这里 `v2(n)` 表示整数 `n` 里 2 的指数，也就是“最多能除以多少次 2”。

现在设：

- `T1=OE`，所以 `t1` 偶、`s1` 奇
- `T2=EO`，所以 `s2` 偶、`t2` 奇

于是：

- `A = u * t2` 的奇偶只看 `u`
- `B = v * s1` 的奇偶只看 `v`

而 basic filter 仍然要求：

- `A` 和 `B` 同奇偶

注意 `u` 和 `v` 是把 `g = gcd(t1, s2)` 除掉之后得到的，所以它们必互素。  
如果 `A` 和 `B` 同奇偶，那么 `u` 和 `v` 也必须同奇偶。  
但互素的两个整数不可能同时为偶数，所以只能是：

- `u` 奇
- `v` 奇

这句话翻回 `t1` 和 `s2`，意思就是：

- `g` 已经把 `t1` 和 `s2` 里的全部 2 因子都除掉了
- 因而 `t1` 和 `s2` 的 2 进指数必须相同

也就是：

- `v2(t1) = v2(s2)`

所以：

- 对 `T1=OE, T2=EO`，如果 `v2(t1) != v2(s2)`，就可以安全剪掉

### 4. 同一类 `T1=OE, T2=EO`，构造出 `N` 后还必须满足 `N ≡ 0 (mod 4)`

在上一条已经知道：

- `u`、`v` 都必须是奇数

而这一类里 `t2` 也是奇数，所以：

- `A = u * t2` 一定是奇数

现在看 `C3` 条件：

- `A^2 + N^2` 必须是完全平方数

因为 `A` 是奇数，所以：

- `A^2 ≡ 1 (mod 8)`

平方数模 8 只能是：

- `0`
- `1`
- `4`

于是：

- 如果 `N` 是奇数，那么 `N^2 ≡ 1 (mod 8)`，总和变成 `2 (mod 8)`，不可能是平方
- 如果 `N ≡ 2 (mod 4)`，那么 `N^2 ≡ 4 (mod 8)`，总和变成 `5 (mod 8)`，也不可能是平方

唯一还可能的情况就是：

- `N^2 ≡ 0 (mod 8)`

也就是：

- `N ≡ 0 (mod 4)`

所以：

- 对 `T1=OE, T2=EO`，即使已经过了前面的朝向和 `v2` 条件，构造出 `N` 后仍必须满足 `N % 4 == 0`

## 四、这四条条件在代码里怎么落地

这版实现只把上面四条已经证明的条件接成硬筛，不夹带任何统计启发式。

入口：

- `scripts/search.py chain-fast --safe-pair-sieve`

实现模块：

- `src/rational_distance/chain_fast/safe_pair_sieve.py`

执行顺序：

1. 先看 triple 朝向
2. 再看 `v2` 条件
3. 只有通过的 pair，才去构造 `g / A / B / N`
4. 对 `T1=OE, T2=EO` 再检查 `N % 4 == 0`
5. 通过后才进入原来的 basic filter

这轮明确**没有**写成硬筛的内容：

- `g_bucket`
- `delta_bucket`
- residue 统计里出现的高命中桶

这些目前都还只是“线索”，不是已证明的必要条件。

## 五、固定基准结果

命令固定是：

```bash
uv run python scripts/search.py chain-fast --max-hyp 5000 --backend python --workers 1 --profile --no-progress
uv run python scripts/search.py chain-fast --max-hyp 5000 --backend python --workers 1 --profile --no-progress --safe-pair-sieve

uv run python scripts/search.py chain-fast --max-hyp 50000 --backend python --workers 1 --profile --no-progress
uv run python scripts/search.py chain-fast --max-hyp 50000 --backend python --workers 1 --profile --no-progress --safe-pair-sieve

uv run python scripts/search.py chain-fast --max-hyp 100000 --backend python --workers 8 --profile --no-progress
uv run python scripts/search.py chain-fast --max-hyp 100000 --backend python --workers 8 --profile --no-progress --safe-pair-sieve
```

结果如下：

| `max_hyp` | workers | 模式 | `pairs total` | `after_safe_pair` | `after_basic` | `c3_pass` | wall time | `time_safe_pair_sieve_s` | 结果一致性 |
|-----------|---------|------|---------------|-------------------|---------------|-----------|-----------|--------------------------|------------|
| `5000` | `1` | baseline | `2,509,056` | `2,509,056` | `620,292` | `37` | `0.9s` | `0.000s` | 一致 |
| `5000` | `1` | safe sieve | `2,509,056` | `732,468` | `620,292` | `37` | `1.7s` | `1.025s` | 一致 |
| `50000` | `1` | baseline | `253,446,400` | `253,446,400` | `62,546,538` | `202` | `88.9s` | `0.000s` | 一致 |
| `50000` | `1` | safe sieve | `253,446,400` | `73,949,824` | `62,546,538` | `202` | `170.0s` | `102.676s` | 一致 |
| `100000` | `8` | baseline | `1,013,658,244` | `1,013,658,244` | `250,042,288` | `318` | `81.7s` | `0.000s` | 一致 |
| `100000` | `8` | safe sieve | `1,013,658,244` | `295,677,849` | `250,042,288` | `318` | `149.2s` | `694.233s` | 一致 |

这里的“结果一致”指的是：

- 解集完全一致
- 这六次固定基准里都没有出现解，也没有 near-miss
- 自动化测试另外验证了小范围下开关前后结果和 near-miss 回调完全一致

## 六、这些结果说明了什么

### 1. 它确实能提前砍掉很多 pair

三组数据都很稳定：

- `after_safe_pair` 大约只剩原来的 `29.2%`
- 也就是大约提前砍掉了 `70.8%` 的 ordered pair

如果只看“提前砍了多少”，这次实验是成功的。

### 2. 但它没有减少 `after_basic`

三组里最值得注意的其实不是 `after_safe_pair`，而是：

- `after_basic_filters` 和 baseline 完全一样

这意味着：

- 安全前筛砍掉的 pair，几乎全都是**原来的 basic filter 本来就会排掉的 pair**

换句话说，这次实验没有把“真正会进入后面阶段的候选”继续压小，只是把一批必死 pair 更早认出来。

### 3. 当前纯 Python 写法的判断成本太高

目前 profile 里能直接看到：

- 省下来的主要是 `time_filter_s`
- 新增的大头是 `time_safe_pair_sieve_s`

而 `time_safe_pair_sieve_s` 比省下来的时间更多，所以 wall time 明显更慢。

大白话就是：

- 这版筛法数学上没问题
- 但当前工程上是在用一套额外的 Python 判断，去重复一部分本来已经很便宜的奇偶 / `mod 4` 逻辑

所以它现在还不划算。

## 七、当前结论

这轮实验的结论可以压缩成一句话：

- 这组朝向 / `v2` / `N mod 4` 条件是**安全的数学必要条件**
- 但按当前插入方式写成独立 Python 前筛后，**没有提速价值**

因此现在最合理的处理方式是：

- 保留 `--safe-pair-sieve` 作为实验开关
- 不改默认行为
- 后续如果还想沿这条线继续做，重点不该是“再多写几条 Python 判断”，而应该是：
  - 把这套信息压进更便宜的 per-triple 预计算
  - 或者继续寻找能让 `after_basic` 真正下降的新必要条件
