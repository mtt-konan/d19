Slice:
safe-filters-controller（controller 本地补审；原 safe-filters subagent 未在可用时间内返回）

Files inspected:
- `docs/MATH.md`
- `docs/PROJECT_STATUS.md`
- `docs/CURRENT_FINDINGS.md`
- `docs/PROOF_STATUS_FAST_MODE.md`
- `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md`
- `docs/work-logs/093-closure-necessity-linear-relations-A9.md`
- `docs/work-logs/094-gen-closure-landing-A9.md`
- `docs/work-logs/104-phase-summary-coprime-to-fullspace.md`
- `src/rational_distance/concordant/safe_pair_sieve.py`
- `src/rational_distance/concordant/chain_closure_sieve.py`
- `src/rational_distance/concordant/dual_closure_sieve.py`
- `src/rational_distance/concordant/analysis.py`
- `src/rational_distance/proof_status/methods.py`
- `src/rational_distance/proof_status/fast_core.py`
- `src/rational_distance/proof_status/workflow.py`
- `tests/test_coprime_mod12.py`
- `tests/test_proof_status.py`
- `tests/test_dual_closure_sieve.py`
- `results/README.md`
- `results/catalog.json`
- `results/proof_status.db`

Commands run:
- `uv run pytest -q tests/test_coprime_mod12.py tests/test_proof_status.py tests/test_proof_status_fast_core.py tests/test_prove_no_solution_fast_mode.py tests/test_dual_closure_sieve.py`
- `uv run python scripts/prove_no_solution.py --pair 7,45 --db /tmp/d19-audit-proof-status.sqlite3 --force --no-progress`
- `PYTHONPATH=src uv run python - <<'PY' ... run_factor_concordant ... PY`
- `PYTHONPATH=src uv run python - <<'PY' ... safe_pair_sieve ... PY`
- `sqlite3 -readonly results/proof_status.db "SELECT status, COUNT(*) FROM pair_proof_status GROUP BY status ORDER BY status;"`
- `sqlite3 -readonly results/proof_status.db "SELECT method, outcome, COUNT(*) FROM pair_method_attempts GROUP BY method, outcome ORDER BY method, outcome;"`

Claims checked:
- `safe_sieve` 的 two-adic 拒绝是否真是必要条件。
- `safe_sieve` 是否只在 reduced/coprime 输入上 sound。
- `gcd_aware_kills` 是否是任意 `(A,B)` 上的 sound 推广。
- `chain_closure_mod_sieve` 当前 production 路径是否使用 full-plane GEN-CLOSURE。
- `factor_concordant` 的 `no_solution` 是否来自穷尽整数 `N` 加 GEN-CLOSURE，而不是有限 EC 搜索。
- `proof_status` 的 fast-core 是否只是 reduced-pair 工程诊断，不是全局 Harborth 证明。
- 结果 DB 是否和当前代码语义一致。

Fatal findings:
- None as an active production-code false-rejection bug.
- Two fatal-if-misused scope boundaries are confirmed and are recorded in the main risk register:
  - sum-only closure is inside-square only;
  - reduced/coprime `(A,B)` is not WLOG.

High-risk findings:
- `run_safe_sieve(A,B)` directly calls `classify_reduced_pair(A,B)` without asserting `gcd(A,B)==1`. The implementation file explicitly limits `classify_reduced_pair` to coprime/reduced input (`safe_pair_sieve.py:1-23`), but the method wrapper does not guard manual or future non-coprime calls (`proof_status/methods.py:103-128`). Inside `generate_ab_pairs()` this is fine; outside that domain it can falsely reject a non-coprime pair. Example probe: `(6,15)` is classified as `mixed_parity`, while it has concordant `N=8`. The full `factor_concordant` still reports no GEN-CLOSURE for that pair, but the safe-sieve reason alone would be invalid on non-coprime input.
- `results/proof_status.db` is stale relative to current wl094 semantics. The DB has `hard_case|4653` and `factor_concordant|inconclusive|4989`, while current `run_factor_concordant` is terminal for reduced coprime legs via GEN-CLOSURE. `results/catalog.json` still marks `proof_status.db` authoritative. This is a data-provenance risk: readers may cite old `hard_case` counts as current.
- `dual_closure_sieve` still calls `killed_at_modulus(..., full_plane=False)` by default and phrases closure as `N_i+N_j=A+B`. Treat it as legacy/inside-square unless upgraded.
- `concordant` CLI's default PARI path is bounded by `--ec-bound`; a smoke run for `(264,420)` found only `[77,315]`, while `factor_concordant` finds `[77,315,352,1440]`. CLI diagnostics should not be read as a proof unless using the factor path or proof_status.

Medium/low findings:
- `proof_status` fast-core summary names `no_solution` for reduced pairs. This is appropriate if the caller remembers the reduced-pair source domain. The docs should not let the phrase drift into "Harborth globally proved."
- `PROJECT_STATUS.md` says local sieves cannot prove no-solution in a broad paragraph, while later sections correctly say chain-closure mod p^2 can prove pair-level no-solution. The safer wording is "cannot prove global Harborth no-solution by themselves."
- The repo-level `ruff check .` fails on many existing style issues, including archived scripts and tests. This is not a theory-soundness issue, but it means "lint clean" cannot be used as a current quality gate without a cleanup pass.

Non-issues worth noting:
- Current `proof_status.methods.run_chain_closure_mod_sieve` calls `find_killer_modulus(..., full_plane=True)`.
- Current `run_factor_concordant` enumerates all integer concordant `N` by factorization and applies `gen_closure_hit`.
- `gcd_aware_kills` implements a sound arbitrary-pair divisibility screen via `D_g`; it is not the old coprime-only safe sieve.
- The focused safe/proof-status tests passed: 68 passed.

Open uncertainties:
- The original safe-filters subagent later returned a detailed report in `safe-filters.md`; this controller note is kept as an independent cross-check.
- I did not reprove every modular theorem beyond checking the stated proof, implementation, and tests.

Recommended updates to main claim ledger:
- Mark `safe_sieve` as "proved only for reduced/coprime inputs."
- Mark `gcd_aware_kills` as "proved necessary filter for arbitrary `(A,B)`, not a complete proof."
- Mark `proof_status.db` as stale unless rebuilt after wl094.
- Prefer `run_factor_concordant` / proof_status over default `concordant` CLI when citing proof-producing reduced-pair decisions.

Plain-language summary:
这些筛子本身没有发现新的误杀 bug。真正要防的是把筛子的适用范围说大。旧 `safe_sieve` 像一把只适合互素 pair 的钥匙，不能拿去开非互素那扇门；现在的 `gcd_aware_kills` 才是给非互素场景补上的安全钥匙。当前 production proof_status 已经用 full-plane 和穷尽 `N` 判定，但旧 DB 和旧 dual 脚本还停在上一代语义。
