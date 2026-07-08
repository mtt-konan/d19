# Open Directions

这份文档只保留当前还值得推进的方向。旧的长清单已经归档到
[archive/EXPLORATION_MAP.md](./archive/EXPLORATION_MAP.md) 和阶段 worklog。

## P0: Finish Or Falsify The Rank-Zero Selmer Route

当前第一优先级。

目标：

```text
for AA / BB / AA+BB rank-zero families:
  prove local image constraints
  prove dyadic local condition
  prove global Selmer dimension bound
  conclude rank(E_lambda)=0
```

已有材料：

- odd-prime formal-lift reviewable segments for several kernels;
- package ledgers under `results/closure_quotient_rank_zero_selmer_packages/`;
- intake/materialization scripts and tests.

还缺：

- complete dyadic theorem;
- complete local-image theorem;
- global Selmer dimension bound;
- final rank-zero theorem.

判定标准很简单：如果不能推出 global Selmer dimension bound，就不要把 package
数量增长当成证明进展。

## P1: Closure Quotient Certificate Ledger

保留并清理当前严格证书账：

```text
AA/BB rank=0
  -> torsion enumeration
  -> pullback
  -> midpoint only
  -> Yang Ji midpoint exclusion
```

这条线的用途是记录已经严格排除的 ratio / pair。它不是通用证明，但它是当前最干净的
有限证据。

## P1: Residual Two-Cover / Sha[2] Frontier

当前 residual covers 是 explicit candidates，不是 no-point proofs。

可做方向：

- Mordell-Weil sieve;
- Cassels-Tate pairing;
- external Magma/Sage certificate;
- Brauer-Manin style obstruction.

优先级低于 rank-zero Selmer，因为它更偏逐个 residual target，不如 family theorem
有杠杆。

## P2: Lambda / Root-Number Map

给 `lambda=A/B` 画地形图：

- 哪些 ratio class 已有 rank-zero certificate；
- 哪些被 root number 奇偶性挡住；
- 哪些落入 two-cover residual；
- 哪些需要新工具。

这能帮助判断 rank-zero 刀的理论覆盖上限，但本身不是证明。

## Closed Or Paused

下面这些不再当主线：

- more pair counting / larger `required_count`;
- `AB/BA` rank-zero knife;
- pure mod-`p^2` universal obstruction;
- old fixed-ratio `sum=A+B` proof route;
- partner graph / high-`k` as proof route;
- Heegner height as global decider;
- raw proof_status scaling as proof progress.

## Rule Of Thumb

新的 work 只有满足下面之一，才算主线进展：

- 产生可复核 theorem/proof segment；
- 缩小 global Selmer bound 的缺口；
- 把 candidate 变成 strict certificate；
- 证明某条旧路线确实不能用，从而减少搜索空间。

只增加样本数、package 数、候选数，不算主线进展。
