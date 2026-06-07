# Risk Register

严重程度按本次目标定义：能改变上层结论或路线状态的，才算 fatal/high。旧文档中已被后续文件纠正的问题，仍会列入风险，因为未来 agent 很容易误引用。

## F1: Sum-Only Closure 被当成全平面闭合

Severity: fatal if cited as current full-plane theorem; high as current documentation drift.

Claim:
旧策略把 Harborth 反例的闭合条件写成 `N1 + N2 = A + B`。

Where it appears:
- `docs/MULTI_CONCORDANT_N_STRATEGY.md:64-92`
- `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md:75-112`
- `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md:228-238`
- `src/rational_distance/concordant/dual_closure_sieve.py:10-18`

Why it matters:
普通话说，这一步把“点在正方形内部”的闭合方式，当成了“平面里任何位置”的闭合方式。正方形外的点满足差关系，不一定满足和关系。若把旧说法当成全平面证明，会漏掉外部反例。

Evidence:
- wl093 明确纠正：sum-only 只覆盖正方形内，full-plane 条件是 `{N1+N2, |N1-N2|} ∩ {A+B, |A-B|} != empty`，见 `docs/work-logs/093-closure-necessity-linear-relations-A9.md:15-34`。
- `MATH.md` 已把这个 caveat 写进 §7 注释，见 `docs/MATH.md:252-260`。
- current production `proof_status` 已修复，`run_chain_closure_mod_sieve` 用 `full_plane=True`，`run_factor_concordant` 用 `gen_closure_hit`，见 `src/rational_distance/proof_status/methods.py:137-170` 和 `src/rational_distance/proof_status/methods.py:213-287`。

Reproduction or check:
- `uv run pytest -q tests/test_proof_status.py` 覆盖 `full_plane=True` 和 GEN-CLOSURE 回归。

Affected top-level conclusions:
- "反例必须满足 `N1+N2=A+B`" 只能保留为 inside-square 版本。
- wl073-wl080 的 "unconditional mod p^2" 结论不能直接作为 full-plane 当前结论引用。

Recommended action:
- 在主文档中把 `MULTI_CONCORDANT_N_STRATEGY.md` 标成 historical/reduced/inside-square，或更新为 GEN-CLOSURE。
- 把 `dual_closure_sieve` 标为 legacy inside-square，或升级为 `full_plane=True` 后重跑。

Plain-language explanation:
如果点在正方形中间，左右两段长度相加等于正方形边长；如果点在外面，就变成两段长度相减等于边长。旧公式只看了第一种情况。

## F2: Reduced/Coprime `(A,B)` 不是 WLOG

Severity: fatal if used to claim global Harborth proof; high as active scope boundary.

Claim:
把 `(A,B)` 除以 `gcd(A,B)` 后只搜互素 pair，并不等于覆盖所有可能反例。

Where it appears:
- Correctly warned in `docs/MATH.md:498-513`
- Correctly warned in `src/rational_distance/concordant/safe_pair_sieve.py:1-23`
- Reduced generation in `src/rational_distance/concordant/pairs.py:23-36`
- Current proof_status caveat in `src/rational_distance/proof_status/methods.py:19-28`

Why it matters:
普通话说，`A,B` 可以一起缩小，但对应的整数 `N` 不一定也能一起缩小。一个最小反例只保证四个量整体互素，不保证 `A,B` 两个量互素。

Evidence:
- `MATH.md` 明确说最小反例只保证 `gcd(A,B,N1,N2)=1`，推不出 `gcd(A,B)=1`。
- `generate_ab_pairs()` 直接输出 reduced/coprime pair。
- wl104 已补上 full-space finite scans，但仍说缺少 "闭合永不发生" 的全局证明，见 `docs/work-logs/104-phase-summary-coprime-to-fullspace.md:66-74`。

Reproduction or check:
- `PYTHONPATH=src uv run python` 探针显示非互素 `(6,15)` 有 concordant `N=8`；旧 coprime-only safe classification 会把它标成 `mixed_parity`。

Affected top-level conclusions:
- reduced-pair proof_status 不能单独证明 Harborth 猜想。
- coprime-only finite scans必须标 scope。

Recommended action:
- 所有 "no_solution" 汇总都加上 source domain：reduced coprime、full-space finite scan、或 arbitrary `(A,B)`。
- 对非互素路线继续用 wl104 三段管线：`gcd_aware_kills -> full_plane chain_closure -> GEN-CLOSURE`。

Plain-language explanation:
不能因为把分数约分很方便，就默认所有整数关系也会跟着约分。这里的 `N` 会破坏这个偷懒。

## H1: `results/proof_status.db` 是旧语义快照

Severity: high.

Claim:
`results/catalog.json` 把 `proof_status.db` 标为 authoritative，但数据库内容仍是 pre-wl094 语义。

Where it appears:
- `results/catalog.json` lists `proof_status.db` as authoritative.
- SQLite check shows `factor_concordant|inconclusive|4989` and `hard_case|4653`.

Why it matters:
当前代码已经把 reduced coprime pair 的 `factor_concordant` 变成 terminal GEN-CLOSURE 判定器。旧 DB 的 `hard_case` 若被当成当前状态，会误导路线优先级。

Evidence:
- wl094 说 `max_hyp=2000` 当前默认 pipeline 应为 `99,311 no_solution, 0 hard_case`，见 `docs/work-logs/094-gen-closure-landing-A9.md:53-66`。
- 本次 SQLite 查询现有 DB：`hard_case=4653`，`factor_concordant inconclusive=4989`。

Reproduction or check:
- `sqlite3 -readonly results/proof_status.db "SELECT method, outcome, COUNT(*) FROM pair_method_attempts GROUP BY method, outcome;"`

Affected top-level conclusions:
- proof_status result snapshots.

Recommended action:
- Rebuild `results/proof_status.db` or mark it stale in `results/catalog.json`.
- Do not cite this DB for current hard_case counts.

Plain-language explanation:
这像一本旧账本：账本格式还在，但里面的判定规则已经换代。不能拿旧账本代表今天的状态。

## H2: Coprime-Only `safe_sieve` 缺少边界保护

Severity: high for manual/non-coprime use; medium inside current reduced pipeline.

Claim:
`run_safe_sieve` wraps `classify_reduced_pair` but does not assert `gcd(A,B)==1`; manual `scripts/prove_no_solution.py --pair A,B` input can therefore enter a coprime-only proof step without the reduced-pair generator's protection.

Where it appears:
- `src/rational_distance/concordant/safe_pair_sieve.py:1-23`
- `src/rational_distance/proof_status/methods.py:103-128`
- `scripts/prove_no_solution.py:45-57`
- `scripts/prove_no_solution.py:137-149`

Why it matters:
The theorem behind `safe_sieve` uses coprimality. On non-coprime pairs it can give an invalid reason for rejection.

Evidence:
- `(6,15)` has concordant `N=8`, but `classify_reduced_pair(6,15)` returns `mixed_parity`.
- `gcd_aware_kills` exists as the arbitrary-pair replacement.
- Normal batch generation is safer because `generate_ab_pairs()` reduces by `gcd(A,B)` before yielding pairs.
- The `--pair` path only checks parsing, positivity, and ordering, then can let `run_safe_sieve` store terminal `outcome="no_solution"` for a method whose own helper says it is reduced/coprime-only.
- Safe-filters subagent sampled non-coprime examples such as `(51,975)` and `(75,495)` where old `safe_sieve` rejects but `gcd_aware_kills` does not. No concrete false GEN-CLOSURE closure was found, so this is a certificate/precondition risk rather than proof that the current headline result is false.

Reproduction or check:
- `PYTHONPATH=src uv run python - <<'PY' ... safe_pair_sieve ... PY`

Affected top-level conclusions:
- Any future non-coprime proof_status run if it reuses `run_safe_sieve` directly.

Recommended action:
- Add a guard or rename wrapper to `run_reduced_safe_sieve`.
- For `scripts/prove_no_solution.py --pair`, either reject non-coprime pairs before `safe_sieve`, skip `safe_sieve`, or record a weaker/non-terminal diagnostic until a gcd-aware/full-plane method runs.
- Use `gcd_aware_kills` for full-space scans.

Plain-language explanation:
这把筛子只适合已经约成互素的 pair。拿它直接筛非互素 pair，就像拿英寸尺读厘米数。

## H3: `dual_closure_sieve` Still Uses Sum-Only Closure

Severity: high if cited as full-plane; medium as legacy tool.

Claim:
Dual closure module and `prove_no_solution_multi_first.py` still use old sum-only closure.

Where it appears:
- `src/rational_distance/concordant/dual_closure_sieve.py:10-27`
- `src/rational_distance/concordant/dual_closure_sieve.py:66-69`
- `scripts/prove_no_solution_multi_first.py:85-103`

Why it matters:
The module underpins old wl073-wl080 "pure modular" claims. It is not full-plane unless upgraded.

Evidence:
- It calls `killed_at_modulus(a,b,m)` without `full_plane=True`.
- Tests for this module check the old behavior, not the full-plane version.

Reproduction or check:
- `uv run pytest -q tests/test_dual_closure_sieve.py`

Affected top-level conclusions:
- Path B and multi-N-first historical claims.

Recommended action:
- Mark the module legacy inside-square.
- If path B is revived, update it to full-plane and re-run.

Plain-language explanation:
这个脚本还在用旧闭合公式。它不是坏掉了，但它回答的问题比现在需要的问题窄。

## H4: `concordant` CLI Diagnostics Are Not Proof-Status Decisions

Severity: high for user interpretation; low for code correctness.

Claim:
Default `concordant` CLI uses bounded PARI `ellratpoints` and sum-only `chain_compatible` diagnostics.

Where it appears:
- `src/rational_distance/concordant/analysis.py:284-295`
- `src/rational_distance/concordant/analysis.py:336-381`
- CLI help says default `ec` has `--ec-bound`.

Why it matters:
The same pair can show fewer `N` in default CLI than in exhaustive factor path. If a reader treats that as proof, they undercount candidates.

Evidence:
- `concordant --pair 264,420` found `[77,315]`.
- `concordant --pair 264,420 --concordant-method factor` found `[77,315,352,1440]`.
- `run_factor_concordant(264,420)` used all 4 and returned no GEN-CLOSURE.

Reproduction or check:
- See `commands-run.md`.

Affected top-level conclusions:
- Any ad hoc CLI-derived "no closure" statement.

Recommended action:
- Label CLI output as diagnostic.
- Use factor/proof_status for authoritative reduced-pair claims.

Plain-language explanation:
默认 CLI 是一盏手电，不是全屋照明。它能帮你看局部，但不能当完整证明。

## H5: Old Result Stores Can Be Misread As Current Authority

Severity: high for result provenance; medium for theory.

Claim:
`results/chain.db` and `results/proof_status.db` are exposed as top-level results but are not both current authoritative artifacts.

Where it appears:
- `results/README.md:7-12`
- `results/catalog.json`

Why it matters:
Old schemas and stale statuses can leak into future claim ledgers.

Evidence:
- `chain.db` has old `chain_runs` schema and is not listed in catalog.
- `proof_status.db` is listed authoritative but stale after wl094.

Recommended action:
- Rebuild or relabel both DBs.
- Add "generated under code version / wl semantic version" metadata.

Plain-language explanation:
文件在，不代表它还代表今天的结论。结果文件需要身份证，不然很容易认错人。

## M1: A1 Strict Proof Was Withdrawn

Severity: medium/high depending on citation.

Claim:
wl083 says A1 is fully proven; wl084 retracts the strict proof.

Where it appears:
- `docs/work-logs/083-conjecture-a1-fully-proven.md`
- `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md:73-92`

Why it matters:
Rank explanations built on A1 must stay empirical/open, not theorem-level.

Recommended action:
- Ledger should cite wl084 as authoritative.

## M2: Partner Graph Naming Overstates Graph Object

Severity: medium/high for graph conclusions.

Claim:
Some docs call `K_n` a subgraph/clique or call finite windows "full G_M".

Where it appears:
- `docs/PARTNER_GRAPH_THEORY.md:134-155`
- `docs/work-logs/063-full-gm-closure-scan-no-counterexample.md`

Why it matters:
`K_n` is a shared-partner star in `G_M`, not necessarily a clique. Finite window scans are strong experiments, not infinite graph proofs.

Recommended action:
- Use `k=n hub/star` and `catalog-seeded W=... graph`.

## M3: Heegner / Height Wording Is Mixed

Severity: medium.

Claim:
Advanced docs both mark Heegner-height no-solution upgrade redundant and later describe adding height bounds to upgrade no-solution.

Where it appears:
- `docs/THEORY_DIRECTIONS_ADVANCED.md:17-24`
- `docs/THEORY_DIRECTIONS_ADVANCED.md:145-156`
- `docs/THEORY_DIRECTIONS_ADVANCED.md:398-420`

Why it matters:
Heegner currently does not prove no-solution; factor_concordant already exhausts integer `N` for reduced legs.

Recommended action:
- Keep Heegner as witness/diagnostic unless a new certified height theorem is written.

## M4: Finite Experiments Are Mostly Worded Carefully, But Some Phrases Are Too Strong

Severity: medium.

Claim:
Several worklogs use phrases like "彻底不存在" for finite windows.

Why it matters:
Finite zero-hit scans support strategy, not global proof.

Recommended action:
- Always attach bounds: `max_hyp`, `window W`, catalog seed, coprime/full-space scope.
