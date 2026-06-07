Slice
constructive-families（counterexample-first / 反向构造族）。

Goal
先强制 full-plane GEN-CLOSURE 的线性闭合关系，再用精确整数平方检查验证同一组 `(A,B)` 是否同时让 `N1,N2` concordant。目标是找真命中；若找不到，就保存最接近、最有结构的失败族。

Files inspected
- `src/rational_distance/concordant/analysis.py:298-333`：项目里的 full-plane `GEN-CLOSURE` 四关系。
- `src/rational_distance/concordant/fast_multi_n.py:114-155`：精确枚举单腿 / 双腿 concordant 的整数方法。
- `tests/test_coprime_mod12.py:33-35`：测试里使用 `isqrt` 的整数平方检查口径。
- `tests/test_proof_status.py:37-50`：`factor_concordant` 用 exhaustive concordant set 做 full-plane closure 的回归测试。
- `scripts/multi_n/noncoprime_full_scan_fast.py:38-64`：全空间 multi-N pair 生成思路，用作反向共同腿搜索的参考。

Commands run
- `git rev-parse HEAD`
- `git status --short`
- `ls -la docs/explorations/2026-06-07-counterexample-first/subagent-notes results/counterexample_first/2026-06-07`
- `nl -ba src/rational_distance/concordant/analysis.py | sed -n '280,345p'`
- `nl -ba src/rational_distance/concordant/fast_multi_n.py | sed -n '114,160p'`
- `PYTHONPATH=src uv run python - <<'PY' ...` scale probes for `iter_concordant_a_n` and `fast_multi_concordant_pairs`
- `PYTHONPATH=src uv run python - <<'PY' ...` attempted direct rectangle `A,B<=250`, `diff_tail<=1500`; this exceeded useful runtime and was not used as a result set
- `PYTHONPATH=src uv run python - <<'PY' ...` direct forced relation sanity search with `A,B<=100`, `diff_tail<=300`
- `PYTHONPATH=src uv run python - <<'PY' ...` generated `results/counterexample_first/2026-06-07/constructive-families.json`
- `jq ... results/counterexample_first/2026-06-07/constructive-families.json`

Search domain
Commit: `3a44a6f08a8d9e7af40e4d77c39882af26ea42fe`.

Output JSON: `results/counterexample_first/2026-06-07/constructive-families.json`.

Search 1: direct forced relation sanity.

| Field | Value |
|---|---:|
| `A` range | `1..100` |
| `B` range | `A+1..100` |
| Sum relations | all positive `N1<N2` forced by target |
| Difference relations | `N2=N1+target`, `1<=N1<=300` |
| Candidates checked | `3,295,900` |

Search 2: reverse common-leg full-square search.

| Field | Value |
|---|---:|
| `N1,N2` range | `1<=N1<N2<=50,000` |
| Pythagorean `(N, X)` pairs emitted | `763,042` |
| Common-leg buckets | `458,419` |
| `N`-pairs with at least two common legs | `138,692` |
| `(A,B)` choices checked from common legs | `182,838` |
| Max common legs for one `N`-pair | `8` |

Closure predicate
For positive integers with `A<B` and `N1<N2`, a hit must satisfy all four exact square checks:

```text
N1^2 + A^2 is square
N1^2 + B^2 is square
N2^2 + A^2 is square
N2^2 + B^2 is square
```

and at least one full-plane linear relation:

```text
sum_ab    : N1 + N2      = A + B
sum_diff  : N1 + N2      = |A - B|
diff_ab   : |N1 - N2|    = A + B
diff_diff : |N1 - N2|    = |A - B|
```

Exact or bounded
All arithmetic checks are exact integer checks using `isqrt`: `x` is accepted as a square only when `isqrt(x)^2 == x`.

The searches are bounded. This rules out hits only inside the domains above. It is not a proof of global non-existence.

Hits
No true hit found.

| Search | Hit count |
|---|---:|
| direct forced relation sanity | `0` |
| reverse common-leg full-square search | `0` |

Top near-misses
The strongest near-misses came from the reverse common-leg search. These already satisfy all four exact square checks; only the linear full-plane closure misses, often by `1`.

| `A` | `B` | `N1` | `N2` | nearest relation | gap | `gcd(A,B)` | `gcd(N1,N2)` |
|---:|---:|---:|---:|---|---:|---:|---:|
| 60 | 84 | 63 | 80 | `sum_ab` | 1 | 12 | 1 |
| 63 | 80 | 60 | 84 | `sum_ab` | 1 | 1 | 12 |
| 84 | 780 | 112 | 585 | `sum_diff` | 1 | 12 | 1 |
| 112 | 585 | 84 | 780 | `diff_ab` | 1 | 1 | 12 |
| 92 | 440 | 525 | 1056 | `diff_ab` | 1 | 4 | 3 |
| 182 | 7475 | 624 | 8280 | `diff_ab` | 1 | 13 | 24 |
| 357 | 480 | 360 | 476 | `sum_ab` | 1 | 3 | 4 |
| 360 | 476 | 357 | 480 | `sum_ab` | 1 | 4 | 3 |

Concrete example:

```text
(A,B,N1,N2) = (60,84,63,80)

63^2 + 60^2 = 87^2
63^2 + 84^2 = 105^2
80^2 + 60^2 = 100^2
80^2 + 84^2 = 116^2

N1 + N2 = 143
A + B   = 144
gap     = 1
```

The direct forced-relation sanity search found no 4/4 square hit. Its best records had the forced closure relation exactly right but only `3/4` square checks true. Example:

```text
(A,B,N1,N2) = (7,45,24,28)
N1 + N2 = A + B = 52

24^2 + 7^2  = 25^2
24^2 + 45^2 = 51^2
28^2 + 45^2 = 53^2
28^2 + 7^2  is not square; nearest-square delta = 8
```

Observed patterns
- The best structural failures often appear in transposed pairs: swapping the role of `(A,B)` and `(N1,N2)` keeps the four-square structure but swaps which side has the large gcd.
- The smallest gap observed in the reverse full-square domain is `1`. There are `29` records with best closure gap `1` and `94` records with best gap `7` among the `gap<=10` bucket.
- In the reverse search, the nearest relation counts were `sum_diff: 82,929`, `sum_ab: 53,789`, `diff_ab: 24,080`, `diff_diff: 22,040`. This says the outside-square sum relation was often closest, but it is only a finite-domain statistic.
- Direct forced closure is much harsher: among `3,295,900` directly forced candidates, the square-count histogram was `0: 3,211,379`, `1: 82,360`, `2: 2,145`, `3: 16`, `4: 0`.

What this rules out
- Within `A,B<=100` and `diff_tail<=300`, no directly forced closure candidate satisfied all four exact square equations.
- Within `1<=N1<N2<=50,000`, no reverse common-leg candidate with at least two exact common legs satisfied any of the four full-plane closure equations.
- The saved gap-1 families show that the obstruction is not simply “hard to make four Pythagorean faces”; four faces happen, but the final linear closure lands just off target.

What this does not rule out
- No global non-existence statement follows from this run.
- It does not rule out larger `N1,N2`, larger direct `diff_tail`, degenerate conventions not counted here, or rational/non-integer variants.
- It does not prove that the gap-1 families cannot be parametrically shifted into gap 0.
- It does not cover every possible non-coprime scaling pattern beyond the stated bound.

Recommended next attack
- Treat the gap-1 transposed families as Diophantine templates. Start with `(60,84,63,80)` and `(357,480,360,476)` and derive the parameter equations for “four Pythagorean faces plus `N1+N2=A+B±1`.”
- Run the reverse common-leg search at `N1,N2<=250,000` or `1,000,000`, but store only aggregate counts and top gaps to avoid huge JSON.
- Add a modular residue audit for the gap value. In plain terms: check whether the same congruence pattern that allows gap `1` systematically forbids gap `0`.
- Split future searches by gcd profile, especially transposed profiles like `gcd(A,B)=1` versus `gcd(N1,N2)=12`.

Plain-language summary
I did not find a counterexample in this bounded constructive search. The most useful output is a family of “almost counterexamples”: all four distance-square checks are exactly true, but the final full-plane closure equation misses by `1`. That is a good next target because it is much closer than random noise: the geometry is already right, and only the last linear equality fails.
