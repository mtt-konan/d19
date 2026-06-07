# Closure-First 3/4 Square Near-Misses

Date: 2026-06-07

## What This Route Means

普通话版：先别筛，也别先假设点在正方形内部。我们先强行让四个数
`A, B, N1, N2` 满足一个 full-plane 闭合关系，也就是图形的“框架”先闭上：

```text
N1 + N2      = A + B
N1 + N2      = |A - B|
|N1 - N2|    = A + B
|N1 - N2|    = |A - B|
```

然后再看四条边：

```text
A^2 + N1^2
B^2 + N1^2
B^2 + N2^2
A^2 + N2^2
```

这条路线专门收集“闭合已经精确成立，但四条边只有三条是勾股边”的样本。用户指出的形状就是：

```text
A-N1, N1-B, B-N2 都是勾股边；
N2-A 不是。
```

这次脚本不只固定这一条坏边，而是记录四种坏边各自出现多少次。

## Why It Was Previously Set Aside

我没有找到“这条路被证明不可能”的记录。更像是被工程和路线选择自然挤走了：

- 旧 `chain_fast` 会让内部闭合 `a+c=b+d` 自动成立，然后检查 C3/C4。
- `results/chain.db` 里已有 `202` 个 near-miss，正是“闭合成立、三条边过、第四条失败”。
- `wl033` 后来试图用 dual EC `rank=0` 给这些 near-miss 找免费障碍，但 `150` 个 D4-distinct 样本里 `0` 个 certified rank=0，所以这把刀没砍动。
- `wl024` 的大范围 `chain_fast @ max_hyp=100000` 看到 `250,042,288` 个基础候选里只有 `318` 个过 C3、`0` 个过 C4，于是注意力转去 `g_bucket` 和 `mod 8`。
- `wl093` 才明确 full-plane 闭合有四种关系；早期 chain 路线主要对应内部关系 `N1+N2=A+B`，不能自动覆盖外部点。

所以这条路不是“死路”，更准确说是：以前的一个后续 obstruction 没成功，后来项目换了更强的主线。

## New Probe

New script:

```text
scripts/theory/closure_first_three_square_search.py
```

The script:

- forces all four full-plane closure relations;
- uses exact `isqrt` square checks;
- precomputes Pythagorean partner sets;
- uses the fast `three_edge_common_n` strategy: a `3/4` candidate forces `A,B` to share at least one common `N`, so the script skips all `(A,B)` pairs without a common partner;
- constructs candidates from three already-square edges, instead of testing the large mass of `1/4` and `2/4` candidates;
- saves JSON with relation counts, missing-edge counts, gcd profiles, exact-hit samples, and top near-misses.

Important boundedness:

- For sum relations, the scan is exhaustive for `1 <= A < B <= max_leg`.
- For difference relations, the scan is bounded by `--diff-tail`, because `|N1-N2| = target` leaves infinitely many positive shifts.

## Main Run

Command:

```bash
PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 2000 --diff-tail 5000 --top-k 200
```

Output:

```text
results/counterexample_first/2026-06-07/closure_first_3of4_max2000_tail5000.json
```

Summary:

| Item | Value |
|---|---:|
| `A,B` bound | `A < B <= 2000` |
| difference tail | `1 <= min(N1,N2) <= 5000` |
| common-partner `(A,B)` pairs | `20,863` |
| three-edge candidates checked | `682` |
| exact `4/4` closure hits | `0` |
| exact `3/4` near-misses | `682` |
| elapsed | `0.034s` |

Before the speed-up, the same boundary checked `5,300,295` union candidates and took about `19.17s`. The fast strategy gives the same `3/4` near-misses and exact-hit count, but avoids the `1/4` and `2/4` candidates entirely.

Benchmark comparison:

| Bound | Legacy time | Fast time | Speed-up |
|---:|---:|---:|---:|
| `max_leg=100`, `tail=300` | `0.0322s` | `0.0008s` | `40.9x` |
| `max_leg=500`, `tail=1500` | `1.0225s` | `0.0090s` | `113.5x` |
| `max_leg=2000`, `tail=5000` | `19.1705s` | `0.0348s` | `550.9x` |

Large fast runs:

| Bound | Fast time | `3/4` near-misses | Exact `4/4` hits |
|---:|---:|---:|---:|
| `max_leg=10000`, `tail=25000` | `0.687s` | `3,901` | `0` |
| `max_leg=50000`, `tail=125000` | `5.993s` | `20,623` | `0` |
| `max_leg=100000`, `tail=250000` | `15.988s` before micro-optimization, `8.49s` benchmark after micro-optimization | `41,736` | `0` |

## Full-Plane Relations Matter

The `682` near-misses are not confined to the old internal relation:

| Relation | `3/4` near-misses |
|---|---:|
| `diff=A+B` | `206` |
| `diff=|A-B|` | `202` |
| `sum=A+B` | `174` |
| `sum=|A-B|` | `100` |

Plain-language takeaway: outside-square closures are producing just as much structure as the inside-square closure. Treating this as only an old chain-fast issue would miss real data.

## Missing Edge Distribution

| Missing edge | Count |
|---|---:|
| `A-N1` | `197` |
| `B-N1` | `184` |
| `A-N2` | `182` |
| `B-N2` | `119` |

This means the failure is not only one named edge. The user’s specific `A-N2` shape is real and common enough to study, but the obstruction should probably be phrased symmetrically.

## Delta 1-10 Distribution

The `max_leg=100000`, `diff_tail=250000` fast run gives the first useful low-delta picture:

| absolute delta | Count |
|---:|---:|
| `1` | `1` |
| `2` | `0` |
| `3` | `0` |
| `4` | `0` |
| `5` | `0` |
| `6` | `6` |
| `7` | `6` |
| `8` | `4` |
| `9` | `2` |
| `10` | `6` |

Plain-language takeaway: the very small band is not smoothly populated. In this bounded run, nothing lands at delta `2..5`; then a small cluster starts at `6`. The lone delta-`1` sample appears only after pushing to `max_leg=100000`.

By relation:

| Relation | Delta `1..10` count |
|---|---:|
| `diff=A+B` | `8` |
| `diff=|A-B|` | `8` |
| `sum=|A-B|` | `7` |
| `sum=A+B` | `2` |

So low deltas mostly come from outside-square full-plane relations. The old inside relation `sum=A+B` contributes only the two delta-`8` transposed samples `(7,45,24,28)` and `(24,28,7,45)`.

By missing edge:

| Missing edge | Delta `1..10` count |
|---|---:|
| `A-N1` | `16` |
| `B-N2` | `5` |
| `A-N2` | `2` |
| `B-N1` | `2` |

This says the low-delta set is heavily biased toward the `A-N1` missing edge, except for the single best delta-`1` sample, which misses `B-N2`.

Signed nearest-square deltas in the same band:

| signed delta | Count |
|---:|---:|
| `-10` | `4` |
| `-9` | `2` |
| `-8` | `4` |
| `-7` | `4` |
| `-6` | `4` |
| `1` | `1` |
| `6` | `2` |
| `7` | `2` |
| `10` | `2` |

Most low-delta failures are just below a square. The delta-`1` case is just above a square:

```text
53911^2 + 132496^2 = 143044^2 + 1
```

This sign asymmetry is worth checking modulo small prime powers. It may be a real obstruction signal, or just a finite-window artifact.

Across increasing bounds:

| Bound | `3/4` near-misses | Delta `<=10` count | Delta `1..10` values seen |
|---:|---:|---:|---|
| `max_leg=2000`, `tail=5000` | `682` | `13` | `6,8,9,10` |
| `max_leg=10000`, `tail=25000` | `3,901` | `19` | `6,7,8,9,10` |
| `max_leg=50000`, `tail=125000` | `20,623` | `24` | `6,7,8,9,10` |
| `max_leg=100000`, `tail=250000` | `41,736` | `25` | `1,6,7,8,9,10` |

The low-delta set grows slowly compared with total `3/4` near-misses. The jump from `50000` to `100000` adds the first delta-`1` example but otherwise leaves the `6..10` counts unchanged in this window.

## Smallest Near-Misses

Best overall:

```text
(A,B,N1,N2) = (17745,53911,60840,132496)
relation    = |N1-N2| = A+B = 71656
missing     = B-N2
nearest-square delta = 1
```

This appears in the `max_leg=100000`, `tail=250000` run. The three passing checks are:

```text
17745^2 + 60840^2  = 63375^2
17745^2 + 132496^2 = 133679^2
53911^2 + 60840^2  = 81289^2
```

The failed check is:

```text
53911^2 + 132496^2 = 20461585937
nearest square      = 143044^2 = 20461585936
delta               = 1
```

Best small-bound sample:

```text
(A,B,N1,N2) = (13,112,15,84)
relation    = N1+N2 = |A-B| = 99
missing     = A-N1
nearest-square delta = 6
```

The user’s exact orientation appears very early:

```text
(A,B,N1,N2) = (7,45,24,28)
relation    = N1+N2 = A+B = 52

24^2 + 7^2  = 25^2
24^2 + 45^2 = 51^2
28^2 + 45^2 = 53^2
28^2 + 7^2  = 833, nearest square is 29^2 = 841, delta = 8
```

So the old remembered object is not imaginary; it is exactly reproduced.

## What This Does And Does Not Say

This run says:

- the closure-first 3/4 route is real enough to revive;
- full-plane outside relations are not rare in this near-miss slice;
- no exact `4/4` hit appeared within this bounded probe;
- the failure can be extremely close to square: the `100000` fast run found a delta-`1` `3/4` near-miss.

This run does not say:

- no counterexample exists globally;
- no exact hit exists beyond the stated finite bounds;
- difference relations are exhausted beyond their stated `diff_tail`;
- finite near-miss counts prove a modular obstruction.

## Next Cut

The most natural next proof/construction target is:

```text
For forced closure + three Pythagorean edges,
explain why the fourth value lands near a square but not on one.
```

Concretely:

- Start with the smallest templates `(13,112,15,84)` and `(7,45,24,28)`.
- Split by relation type and missing edge.
- For the failed value, tabulate residues modulo small primes and prime squares.
- Compare transposed pairs where `(A,B)` and `(N1,N2)` swap gcd profiles.
- If a residue obstruction appears for delta `0`, turn it into a lemma; if not, use the same templates as counterexample generators.
