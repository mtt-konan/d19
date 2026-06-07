Slice:
gcd-strata-search

Goal:
在 full-space multi-N 搜索里，把非互素 `(A,B)` 按 `g=gcd(A,B)` 分层，找出 `gcd_aware_kills` 和 full-plane modular GEN-CLOSURE 最弱的层。重点看 `3|g`、`4|g`、`12|g`、`D_g=1`，并收集 exact GEN-CLOSURE hit 或最近的 near-miss。

Files inspected:
- `docs/superpowers/plans/2026-06-07-counterexample-first-exploration-goal.md`
- `scripts/multi_n/noncoprime_full_scan_fast.py`
- `src/rational_distance/concordant/safe_pair_sieve.py`
- `src/rational_distance/concordant/chain_closure_sieve.py`
- `src/rational_distance/concordant/fast_multi_n.py`
- `results/multi_n/full_scan_max10000.json`
- `results/multi_n/full_scan_max100000.json`
- `results/multi_n/full_scan_max1000000.json`

Commands run:
- `sed -n '1,240p' docs/superpowers/plans/2026-06-07-counterexample-first-exploration-goal.md`
- `sed -n '240,430p' docs/superpowers/plans/2026-06-07-counterexample-first-exploration-goal.md`
- `ls -la results/multi_n results/counterexample_first/2026-06-07 docs/explorations/2026-06-07-counterexample-first/subagent-notes`
- `git status --short`
- `git status --short --untracked-files=all`
- `git rev-parse HEAD`
- `rg -n "gcd|D_g|gcd_aware|GEN-CLOSURE|full_plane|chain_closure|closure|noncoprime|multi-N|strata|stratum" ...`
- `nl -ba scripts/multi_n/noncoprime_full_scan_fast.py | sed -n '1,210p'`
- `nl -ba src/rational_distance/concordant/chain_closure_sieve.py | sed -n '146,182p'`
- `python3 -m json.tool results/multi_n/full_scan_max10000.json | sed -n '1,220p'`
- `python3 -m json.tool results/multi_n/full_scan_max100000.json | sed -n '1,80p'`
- `python3 -m json.tool results/multi_n/full_scan_max1000000.json | sed -n '1,80p'`
- `uv run python - <<'PY' ... custom gcd-strata exact near-miss scan ... PY`
- `uv run python - <<'PY' ... summarize gcd-strata-search.json ... PY`
- `wc -c results/counterexample_first/2026-06-07/gcd-strata-search.json`

Search domain:
- Primary computed domain: full-space multi-N pairs with `A < B <= 10000`.
- Includes coprime and non-coprime pairs; no reduced-only filter.
- Pair generation reused `scripts/multi_n/noncoprime_full_scan_fast.py::multi_n_pkeys(max_hyp=10000)`, which uses the Cython generator with `coprime_only=False`.
- Total computed pairs: `17748`.
- Coprime pairs: `854`.
- Non-coprime pairs: `16894`.
- Read-only comparison: existing `results/multi_n/full_scan_max100000.json` and `results/multi_n/full_scan_max1000000.json` survivor gcd distributions were used only to see whether the same weak strata persist at larger bounds.

Closure predicate:
Only full-plane GEN-CLOSURE was used:

```text
{N_i + N_j, |N_i - N_j|} intersects {A + B, |A - B|}
```

The custom scan used distinct pairs `i < j` of exact concordant `N` values. Sum-only `N_i + N_j = A+B` was not used as a full-plane conclusion.

Exact or bounded:
- Bounded by `A < B <= 10000`.
- Exact inside that bound: for every multi-N pair, the script called `exact_concordant_pair(A,B)` and computed exact integer GEN-CLOSURE deltas.
- Modular stage used `find_killer_modulus(..., full_plane=True, moduli=STANDARD_MODULI)`.
- Larger `100000` and `1000000` observations are read-only aggregate summaries, not recomputed near-miss scans in this slice.
- Machine data written to `results/counterexample_first/2026-06-07/gcd-strata-search.json` with commit `3a44a6f08a8d9e7af40e4d77c39882af26ea42fe`.

Hits:
- Exact GEN-CLOSURE hits at `max_hyp <= 10000`: `0`.
- Existing read-only summaries also report `closures: 0` at `max_hyp=100000` and `max_hyp=1000000`.

Top near-misses or weak strata:
Top exact residual near-misses after both `gcd_aware_kills` and full-plane modular sieve failed to kill:

| rank | `(A,B)` | `g` | `D_g` | `k` | closest relation | delta | `N` pair |
|---:|---|---:|---:|---:|---|---:|---|
| 1 | `(1080,1428)` | 12 | 1 | 2 | `sum=A+B` | 3 | `[1071,1440]` |
| 2 | `(3960,6300)` | 180 | 1 | 5 | `diff=|A-B|` | 4 | `[5280,7616]` |
| 3 | `(460,2200)` | 20 | 3 | 2 | `diff=A+B` | 5 | `[2625,5280]` |
| 4 | `(2160,2856)` | 24 | 1 | 2 | `sum=A+B` | 6 | `[2142,2880]` |
| 5 | `(5940,6384)` | 12 | 1 | 2 | `sum=A+B` | 7 | `[6080,6237]` |
| 6 | `(3240,4284)` | 36 | 1 | 2 | `sum=A+B` | 9 | `[3213,4320]` |
| 7 | `(920,4400)` | 40 | 3 | 2 | `diff=A+B` | 10 | `[5250,10560]` |
| 8 | `(2508,5292)` | 12 | 1 | 4 | `diff=A+B` | 12 | `[3969,11781]` |
| 9 | `(75,495)` | 15 | 4 | 2 | `sum=|A-B|` | 12 | `[100,308]` |
| 10 | `(1485,1995)` | 15 | 4 | 2 | `diff=A+B` | 12 | `[1296,4788]` |

Weak gcd strata by final residual count at `max_hyp<=10000`:

| `g` | pairs | final residual | min delta | comment |
|---:|---:|---:|---:|---|
| 12 | 1066 | 135 | 1 | largest residual stratum; `D_g=1` |
| 60 | 315 | 69 | 4 | `12|g`, high residual rate |
| 24 | 606 | 65 | 1 | `12|g`, `D_g=1` |
| 36 | 322 | 37 | 3 | `12|g`, `D_g=1` |
| 120 | 175 | 32 | 8 | `12|g`, high residual rate |
| 48 | 282 | 30 | 4 | `12|g`, `D_g=1` |
| 15 | 499 | 29 | 5 | `3|g`, `D_g=4`, not killed often after Dg survivor |
| 3 | 1161 | 23 | 1 | `3|g`, `D_g=4` |
| 20 | 393 | 22 | 1 | `4|g`, `D_g=3` |
| 40 | 241 | 22 | 3 | `4|g`, `D_g=3` |

High-k note:
- Highest `k` found at `max_hyp<=10000` was `6`.
- Most `k=6` pairs were killed by modular sieve or `gcd_aware_kills`.
- Best high-k residual was `(3960,6300)`, `g=180`, `D_g=1`, `k=5`, closest delta `4`.

Observed patterns:
- The final residual set is almost entirely non-coprime: `866/866` residual pairs are non-coprime at `max_hyp<=10000`.
- `12|g` is the main weak zone. It has `4915` pairs, `0` killed by `gcd_aware_kills`, `4330` killed by full-plane modular sieve, and `585` final residuals.
- `D_g=1` exactly matches `12|g` in this run. This is the clearest weak stratum because the gcd-aware divisibility argument has no force there.
- `3|g` and `4|g` are both broad weak umbrellas, but their intersection `12|g` is where the most resistant pairs live.
- The larger read-only summaries show the same pattern strengthening with bound:
  - `max_hyp=100000`: `19219` final survivors, `13988` have `12|g` / `D_g=1`.
  - `max_hyp=1000000`: `332373` final survivors, `256774` have `12|g` / `D_g=1`.
- Top survivor gcd values are stable across larger summaries: `g=12`, `60`, `24`, `120`, `36`, `48`, `180` dominate.
- Closest residual near-misses are not only inside-square sums. The top 10 include `sum=A+B`, `sum=|A-B|`, `diff=A+B`, and `diff=|A-B|`, which confirms that full-plane relation tracking matters.

What this rules out:
- Within the bounded domain `A < B <= 10000`, all full-space multi-N pairs were checked with exact concordant `N`; none satisfy full-plane GEN-CLOSURE.
- In this bounded domain, the most promising exact residual near-miss still misses by delta `3`; no delta `0` exists among residuals.
- For this domain, simple "look in any non-coprime stratum" is too broad. The real pressure point is narrower: `12|g`, equivalently `D_g=1`.

What this does not rule out:
- No global counterexample is ruled out.
- Bounds above `10000` were not recomputed with exact near-miss deltas in this slice.
- A full Harborth point outside this bounded `(A,B)` domain remains untouched.
- Existing `100000` and `1000000` summaries were read as prior data; this slice did not independently regenerate them.
- The scan does not prove why `12|g` residuals fail GEN-CLOSURE; it only identifies them as the main weak stratum.
- This does not rule out bugs in the Cython generator or exact pair enumeration, though both are existing project paths.

Recommended next attack:
1. Run the same exact near-miss collection at `max_hyp=100000`, but store only residuals plus top deltas to keep the file small.
2. Focus proof work on `12|g` / `D_g=1`, especially the scaled families with `g in {12,24,36,48,60,120,180}`.
3. Try a constructive search inside `D_g=1`: force one of the four full-plane relations first, then test concordance. The nearest residuals suggest this is more targeted than blind full-space extension.
4. Compare `(1080,1428)` and scaled/related pairs around it. It is the best exact residual miss in this run: `g=12`, `D_g=1`, `N=[1071,1440]`, `N1+N2 = A+B-3`.
5. For each dominant `g`, compute congruence of the closest delta modulo small primes and modulo `g/12`. If the deltas are forced away from `0`, this could become a lemma.

Plain-language summary:
这轮没有找到真正闭合的例子。最有用的发现是：非互素空间里真正难的不是所有 gcd，而是 `g` 同时含 `3` 和 `4` 的层，也就是 `12|g`。在这一层里，原来的 gcd-aware 整除筛完全使不上力，因为 `D_g=1`，只能靠 full-plane 模筛和最后的 exact GEN-CLOSURE。到 `10000` 为止，最接近的残余样本只差 `3`，所以下一步不该泛泛扩大搜索，而应该专门攻击 `12|g / D_g=1` 的闭合差值为什么总偏离 `0`。
