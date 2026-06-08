# wl117 — 审查后的下一阶段理论路线图

日期：2026-06-09

这份 wl 接在理论框架审查和 wl107-wl116 之后。

当前状态：

```text
审查完成了。
Harborth / d19 数学问题没有完成。
```

审查给出的最重要边界是：

```text
不能把有限搜索当证明。
不能把 sum-only closure 当 full-plane closure。
不能把 coprime reduced pair 当 WLOG。
不能把整数 A=kB 当全局有理比例 A/B。
```

所以后续路线要同时满足两个条件：

```text
1. 能真的推进数学结构；
2. 不会把局部结论误写成全局证明。
```

---

## 1. 路线总览

我现在认为后续最像七条路，但优先级不同。

| 路线 | 一句话 | 优先级 | 角色 |
|---|---|---|---|
| 有理比例 `R_λ` translation theorem | 证明 closure 交点只能来自 `r <-> λ/r` | P0 | 主理论突破口 |
| 推广 Yang Ji / 固定线 | 从中线、边线、固定整数比例往外推 | P1 | 可读证明样板 |
| closure-first near-miss 方程化 | 把“差一点”变成可证明的障碍 | P1 | 找隐藏结构 |
| D4 对称变量重写 | 用不变量替代散点图肉眼观察 | P1 | 降维和找坐标 |
| 非互素 / full-space 缺口 | 修补 reduced/coprime 非 WLOG | P1/P2 | 地基 |
| 工程安全清理 | 防止旧筛和旧 DB 误导后续 | P2 | 风险控制 |
| 中心线 / 特殊线 proof note | 把已知特殊位置整理成本地证明 | P2 | 文档和样板 |

我的建议：

```text
主攻 P0。
并行做 P1 里的 near-miss / D4 小工具，给 P0 找结构。
工程安全清理不要拖太久，但不要抢主理论时间。
```

---

## 2. P0：有理比例 `R_λ` translation theorem

### 问题

归一化：

```text
λ = A/B ∈ Q_{>0}
r = N/B
```

定义：

```text
R_λ = { r∈Q_{>0} :
        r^2 + 1   是有理平方，
        r^2 + λ^2 是有理平方 }
```

full-plane closure 是：

```text
r+s   = λ+1
r+s   = |λ-1|
|r-s| = λ+1
|r-s| = |λ-1|
```

目标命题：

```text
若 r,s∈R_λ 且满足一条 full-plane closure，
是否必须有 s = λ/r？
```

普通话说：

```text
两个点各自都能和左右两边配成勾股距离。
如果它们还刚好把正方形闭上，
那它们是不是只能是一对镜像点？
```

如果这条成立，再排除 reciprocal orbit closure，就会关闭一大块有理比例空间。

### 为什么值得做

这条路比整数 `A=kB` 更接近全局，因为候选比例本来就是有理数。

它也比盲扫更硬，因为它把问题变成：

```text
同一条 R_λ 曲线和它的平移/反射交点问题。
```

### 已有工具

```text
src/rational_distance/concordant/rational_ratio.py
tests/test_rational_ratio.py
docs/work-logs/115-rational-ratio-upgrade-strategy.md
docs/work-logs/116-rational-ratio-module-and-proof-boundary.md
```

模块已经记录：

```text
r -> λ/r reciprocal 对称
product identity:
  B_p - λ^2 A_p = (λ^2-1)(λ^2-p^2)
square-rectangle model:
  (M-T)^2+4, (M+T)^2+4,
  (M-T)^2+4λ^2, (M+T)^2+4λ^2
```

### 第一小步

不要先尝试“证明所有 λ”。

先做一个 proof note / algebra worksheet：

```text
固定 closure target T。
设 r+s=T, p=rs。
把 r,s∈R_λ 全部翻译成 p,T,λ 的平方条件。
问：这些条件是否强迫 p=λ？
```

如果能推出 `p=λ`，就得到：

```text
rs = λ
=> s = λ/r
```

### 成功信号

至少得到一条下面形式的局部定理：

```text
在 sum=A+B 分支，
r,s∈R_λ 且 r+s=λ+1
=> rs=λ。
```

哪怕先只证明 `λ` 满足某些 squareclass / parity 条件，也值得。

### 失败信号

如果能构造出：

```text
r,s∈R_λ
closure 成立
但 rs≠λ
```

那 P0 的主猜想就错了。这个不是坏消息，它会直接给出新的核心结构。

---

## 3. P1：推广 Yang Ji / 固定线

### 问题

已知特殊位置：

```text
中线
边线及其延长线
对角线及其延长线
```

这些位置没有四个有理距离点。仓库已经把中心线和 `A=B` 作为低维分支讨论过。

下一层是：

```text
A = kB
```

先不要说全体有理 `k`。可以先看：

```text
整数 k
小素数条件
k±1 的素因子条件
模条件覆盖
```

### 为什么值得做

这条路最容易产出人能读的证明。

它也能给 P0 提供样板：如果固定整数线能证明，看看证明里哪些步骤不依赖整数性，哪些步骤必须换成有理 `λ`。

### 已有边界

wl115-wl116 已经说明：

```text
整数 k 不是终点。
k^2+1 不为有理平方 这种整数夹逼不能搬到有理 λ。
```

所以这条路要保持诚实：

```text
固定整数 k 证明是切片证明，不是全局证明。
```

### 第一小步

写本地 proof note：

```text
center-line-impossibility.md
```

内容：

```text
A=B / N1=N2 为什么不行。
它和 Yang Ji midline theorem 怎么对应。
哪些地方用了“点在特殊线”。
```

然后再写：

```text
fixed-integer-ratio-proof-boundary.md
```

列出 Yang Ji fixed-n / prime-pair 条件能覆盖哪些 `k±1`，不能覆盖哪里。

### 成功信号

得到一个可引用定理：

```text
若 A=kB 且 k 落在某个明确整数集合 K，
则 full-plane closure 不可能。
```

集合 `K` 不必很大，但条件必须清楚。

### 失败信号

如果证明每次都退化成“需要处理任意有理 λ 的 R_λ 交点”，那就说明 P0 才是主路，固定整数线只是样本库。

---

## 4. P1：closure-first near-miss 方程化

### 问题

之前 closure-first 搜索发现很多 `3/4` near-miss：

```text
closure 已经满足；
四个平方条件里有三个满足；
第四个总差一点。
```

只看 `delta=1..10` 的统计不够。真正要问：

```text
为什么第四条总差一点？
这个“差一点”能不能写成一个无解方程？
```

### 为什么值得做

near-miss 是最接近反例的地方。它们可能暴露：

```text
隐藏递降
平方剩余障碍
局部-全局缺口
固定 squareclass
```

### 第一小步

把 near-miss 从“结果行”改写成方程模板。

例如固定 closure 和三条勾股条件：

```text
a^2 + n_1^2 = square
n_1^2 + b^2 = square
b^2 + n_2^2 = square
n_2^2 + a^2 = almost square
closure relation holds exactly
```

然后记录第四条的差：

```text
square_candidate - nearest_square
```

不要只统计 delta 数字，要统计：

```text
delta 的因子分解
mod p 模式
squareclass
和 A,B,N1,N2 gcd 的关系
```

### 成功信号

发现某个稳定模式：

```text
第四条失败量总落在某个不可能 squareclass；
或者总被某个 p≡3 mod 4 的奇次幂卡住；
或者递降到更小 near-miss。
```

### 失败信号

delta 模式跟普通随机平方间距差不多。这时 near-miss 更像搜索线索，不像证明入口。

---

## 5. P1：D4 对称变量重写

### 问题

480 个 D4 合并后的点图没有肉眼规律。

但“图没规律”不代表“代数没规律”。也许我们看错了坐标。

### 候选变量

不要直接看 `(x,y)`。改看 D4 对称量：

```text
x(1-x)
y(1-y)
x+y
|x-y|
min distances to opposite sides
A+B
|A-B|
N1+N2
|N1-N2|
rs
r+s
```

特别是 ratio 版本：

```text
λ = A/B
r = N/B
s = N'/B
p = rs
T = r+s 或 |r-s|
```

这些变量和 P0 能直接接上。

### 第一小步

写一个小分析脚本，不画散点为主，而是输出表：

```text
D4 orbit representative
λ
r,s
p-ratio: p/λ
closure relation
failed squareclass
```

### 成功信号

发现 near-miss 在某个变量上集中，比如：

```text
p/λ 接近 1
某个 squareclass 固定
某个 D4 invariant 只取少数值
```

这会反哺 P0 的 `p=λ` 目标。

### 失败信号

所有 D4 invariant 都散。这不会杀死 P0，只说明 near-miss 数据不给提示。

---

## 6. P1/P2：非互素 / full-space 缺口

### 问题

reduced coprime `(A,B)` 不是 WLOG。

普通话说：

```text
A,B 可以一起约分，
但 N1,N2 不一定跟着约分。
```

所以只证明互素世界，不等于证明全空间。

### 为什么值得做

这是地基问题。它不一定给出漂亮证明，但能防止全局声明漏 case。

### 第一小步

把 full-space pipeline 写成固定流程：

```text
gcd_aware_kills
full_plane chain_closure_mod_sieve
exact factor_concordant + GEN-CLOSURE
```

然后为非互素样本建一个小型 catalog：

```text
被 coprime safe_sieve 错域拒绝的例子
gcd-aware 能杀的例子
gcd-aware 不能杀但 mod/full GEN-CLOSURE 能杀的例子
```

### 成功信号

得到一个清晰的非互素分层：

```text
哪些 gcd 类型被 D_g 直接杀；
哪些 gcd 类型必须上 full-plane mod；
哪些是真 residual。
```

### 失败信号

残余变成 local-global gap。那就把这条路移交给 Brauer-Manin / Chabauty 长线。

---

## 7. P2：工程安全清理

这条不直接证明数学，但能减少后续误判。

建议清理：

```text
1. 给 run_safe_sieve 加 coprime guard 或重命名为 run_reduced_safe_sieve。
2. 标记 results/proof_status.db、results/chain.db 的语义版本或 stale 状态。
3. 给 dual_closure_sieve 加 legacy inside-square 标记。
4. 把 docs/MULTI_CONCORDANT_N_STRATEGY.md 的 sum-only 文字改成 GEN-CLOSURE 或标 historical。
5. CLI 输出里把 chain_compatible 标成 inside-square/sum diagnostic。
```

成功信号很简单：

```text
后续 agent 不能再靠名字误把 safe/proof/no_solution 当全局证明。
```

---

## 8. 推荐执行顺序

### 第一阶段：一周内

```text
1. 写 P0 的 p=rs algebra worksheet。
2. 同时写 D4 invariant / near-miss 表脚本，给 P0 找模式。
3. 写 center-line proof note，作为低维证明样板。
```

### 第二阶段：两到三周

```text
1. 若 P0 有进展，尝试证明 sum=A+B 分支的 p=λ。
2. 若 P0 卡住，用 near-miss 和 D4 invariant 查反例结构。
3. 开始非互素 catalog，确认 full-space 残余长什么样。
```

### 第三阶段：更长线

```text
1. Yang Ji 固定线推广：整数 k、小素数条件、模条件覆盖。
2. 若 residual local-global gap 稳定，转 Brauer-Manin / Chabauty。
3. 若 D4 invariant 给出简单模式，把它转成正式筛或定理。
```

---

## 9. 我会怎么选

我会把主线放在：

```text
P0: R_λ translation theorem
```

原因：

```text
它最接近全局有理比例；
它能吸收固定比例路线；
它能吃掉 D4 invariant 和 near-miss 反馈；
它成功后不是多砍一点搜索空间，而是关闭一个结构层。
```

同时保留两个侦察方向：

```text
near-miss 方程化
D4 对称变量重写
```

这两条像探照灯，不一定自己证明结论，但可能告诉 P0 该盯哪个变量。

工程安全清理应该穿插做，不要再让旧 sum-only / coprime-only 结论污染新路线。
