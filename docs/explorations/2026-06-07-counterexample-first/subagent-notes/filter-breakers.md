# Slice

filter-breakers

# Goal

Find samples that break incorrect shortcuts in the counterexample-first exploration. These are not claimed as true Harborth counterexamples; they only show that some filters or reductions are too strong if used outside their stated scope.

# Files inspected

- `docs/audits/2026-06-07-theory-framework-audit/risk-register.md`: H2 safe-sieve boundary (`:106-138`), H4 bounded CLI warning (`:175-203`).
- `src/rational_distance/concordant/safe_pair_sieve.py`: coprime-only warning and gcd-aware replacement (`:1-23`, `:30-43`, `:61-93`).
- `src/rational_distance/concordant/chain_closure_sieve.py`: sum-only versus full-plane modular closure (`:146-182`, `:185-197`).
- `src/rational_distance/concordant/fast_multi_n.py`: exact integer N enumeration and coprime-only batch generator (`:142-155`, `:185-221`).
- `src/rational_distance/concordant/analysis.py`: bounded `ellratpoints`, sum-only diagnostic, and full-plane `gen_closure_hit` (`:208-333`, `:336-381`).
- `scripts/search.py`, `src/rational_distance/cli/search/parser.py`, `src/rational_distance/cli/search/runners.py`: default `ec` method and factor method CLI paths (`parser.py:352-393`, `runners.py:16-143`, `runners.py:246-315`).
- `tests/test_fast_multi_n.py`: exact method regression including the scaled k=14 hub (`:125-143`).
- `results/multi_n/non_coprime_scan_max2000_summary.json`, `results/multi_n/k14_search.jsonl`, `results/multi_n/k14_search_ladder.json`, `results/counterexample_first/2026-06-07/near_misses_max100000.json`.
- Selected work logs `docs/work-logs/093-104*.md` for scope checks on GEN-CLOSURE, gcd-aware filtering, and non-coprime scans.

# Commands run

- `rg` / `nl -ba` read-only inspections over the files above.
- `jq '.' results/multi_n/non_coprime_scan_max2000_summary.json`.
- `jq` probes over `results/counterexample_first/2026-06-07/near_misses_max100000.json` and `results/multi_n/k14_search_ladder.json`.
- `PYTHONPATH=src uv run python - <<'PY' ... noncoprime/sum-only/bounded/high-k search probes ... PY`.
- `uv run python scripts/search.py concordant --pair 264,420`.
- `uv run python scripts/search.py concordant --pair 264,420 --concordant-method factor`.

# Search domain

- Non-coprime old-safe breakers: scanned `2 <= A < B <= 2000`, `gcd(A,B)>1`, old `classify_reduced_pair(A,B) != "pass"`, `gcd_aware_kills(A,B) == false`, and exact concordant N nonempty.
- Sum-only/full-plane breakers: scanned `2 <= A < B <= 8000` until 30 hits with `k>=2`, where `STANDARD_MODULI` sum-only had a killer modulus but `STANDARD_MODULI` full-plane had none.
- Bounded undercount: direct smoke on `(264,420)` with default `ec_bound=100000`, compared to factor/exact enumeration.
- High-k no-closure: exact checks of known high-k catalog samples and a small full-plane modular survivor.

# Closure predicate

The full-plane predicate used here is:

`{N1+N2, |N1-N2|} ∩ {A+B, |A-B|} != empty`.

That is the `gen_closure_hit` predicate in `analysis.py:298-333`. The old inside-square shortcut only checks `N1+N2 = A+B`; `chain_closure_sieve.py:149-165` explicitly says that is narrower than the full-plane condition.

# Exact or bounded

All sample rows except the bounded-EC demonstration use `exact_concordant_pair(A,B)`, which `fast_multi_n.py:148-155` describes as the complete integer concordant set with no elliptic-curve sampling bound.

The bounded-EC breaker intentionally uses the default `concordant` CLI / `find_concordant_integers`, where `analysis.py:208-281` calls PARI `ellratpoints(E, ec_bound)`. CLI help says `ec` is default and has an upper bound, while `factor` is unbounded and finds all integer solutions (`parser.py:359-393`).

# Hits

- Non-coprime old-safe breaker scan found 731 samples in `A,B <= 2000`.
- Sum-only/full-plane scan found 30 `k>=2` samples before early stop in `A,B <= 8000`.
- Bounded EC undercount reproduced on `(264,420)`: default EC found `[77, 315]`; factor/exact found `[77, 315, 352, 1440]`.
- High-k no-closure checks verified `k=14`, `k=11`, and `k=5` samples with no GEN-CLOSURE hit.

# Filter-breaking samples

| Type | Pair `(A,B)` | Exact N | Breaks | Not a true counterexample because |
| --- | --- | --- | --- | --- |
| Non-coprime old-safe misuse | `(51,975)` | `[140,1300]` | `classify_reduced_pair` returns `odd_odd_wrong_mod4`, but `gcd_aware_kills=false` | exact GEN-CLOSURE has no hit |
| Non-coprime old-safe misuse | `(75,495)` | `[100,308]` | old safe rejects, gcd-aware does not; also sum-only kills while full-plane does not | exact GEN-CLOSURE has no hit |
| Non-coprime old-safe misuse | `(975,1995)` | `[684,2340]` | old safe rejects, gcd-aware does not, no full-plane modular killer in standard moduli | exact GEN-CLOSURE has no hit |
| Sum-only/full-plane split | `(120,792)` | `[160,594,715]` | sum-only first killer `M=169`; full-plane has no standard-moduli killer | exact GEN-CLOSURE has no hit |
| Sum-only/full-plane split | `(152,3080)` | `[1440,5775]` | sum-only first killer `M=9`; full-plane has no standard-moduli killer | exact GEN-CLOSURE has no hit |
| Bounded EC undercount | `(264,420)` | exact `[77,315,352,1440]`; bounded EC `[77,315]` | default bounded CLI misses exact integer N | all exact N still fail GEN-CLOSURE |
| High-k no closure | `(2598960,28274400)` | 14 exact N | many half-solutions do not force closure | exact GEN-CLOSURE has no hit |
| High-k no closure | `(277200,1009008)` | 11 exact N | high rank/high k is not a closure certificate | exact GEN-CLOSURE has no hit |
| High-k modular survivor no closure | `(840,3120)` | `[448,1575,1664,3094,5850]` | `k=5`, sum-only kills at `M=289`, full-plane standard moduli do not | exact GEN-CLOSURE has no hit |

Full JSON details are in `results/counterexample_first/2026-06-07/filter-breakers.json`.

# Observed patterns

- The old safe sieve is a reduced/coprime statement. `safe_pair_sieve.py:1-23` says this directly, and `gcd_aware_kills` is the arbitrary-pair replacement (`:82-93`). Non-coprime samples can have exact concordant N while the old coprime-only classifier says reject.
- Sum-only modular killing is easy to overstate. Several samples are impossible for `N1+N2=A+B` modulo a standard modulus, but still have a full-plane modular residue path through `|A-B|` relations.
- Bounded EC output is useful diagnostics, not a complete integer-N catalog. `(264,420)` is the clean smoke: default EC reports two N, exact/factor reports four.
- Large k helps create dense near-miss material, but does not by itself create closure. The k=14 sample has 14 exact N and still no full-plane relation.

# What this rules out

- It rules out treating coprime-only `safe_sieve` as a sound arbitrary non-coprime pair rejection.
- It rules out citing old sum-only closure/modular kills as full-plane GEN-CLOSURE kills.
- It rules out using the default bounded `concordant` CLI output as if it were exhaustive.
- It rules out the informal shortcut "many concordant N, high k, or high rank should force closure."

# What this does not rule out

- It does not rule out Harborth counterexamples globally.
- It does not prove any listed pair is a Harborth counterexample. In fact, every listed exact sample has `gen_closure_hit = null`.
- It does not prove the current full-plane pipeline is globally complete beyond the inspected scope.
- It does not invalidate reduced/coprime uses of `classify_reduced_pair`; the problem is using it outside that precondition.

# Recommended next attack

Use these filter-breakers as regression seeds for claim wording and future search dashboards. For counterexample-first exploration, prioritize exact full-plane survivors where all cheap filters fail and the closest GEN-CLOSURE delta is small; `(75,495)`, `(120,792)`, `(840,3120)`, and catalogued high-k hubs are good seeds. The most useful next metric is not just `k`, but "full-plane survivor plus small delta to one of the four closure relations."

# Plain-language summary

这些样本的意思很简单：有些筛子只适合特定场景，不能拿来当万能裁判。非互素 pair 不能直接套互素筛；只检查 `N1+N2=A+B` 也不能代表整张平面；默认 EC 搜索有高度上限，会少看到一些 N；就算一个 pair 有很多个半解，也不等于这些半解能拼成完整方形解。本切片只是在拆掉这些错误捷径，不是在宣布找到真反例。
