Slice:
safe-filters（安全筛 / 证明标签）。本报告只审本切片，不判断整个 d19 框架 sound/unsound。

Files inspected:
- `docs/PROOF_STATUS_FAST_MODE.md`
- `docs/MULTI_N_FILTER_LADDER.md`
- `docs/archive/CHAIN_FAST_SAFE_FILTERS.md`
- `docs/archive/CONCORDANT_SAFE_FILTERS.md`
- `docs/work-logs/067-104*.md` 中与 `safe_sieve`、`fast-core`、`GEN-CLOSURE`、`gcd-aware` 相关段落
- `src/rational_distance/chain_fast/safe_pair_sieve.py`
- `src/rational_distance/chain_fast/api.py`
- `src/rational_distance/concordant/pairs.py`
- `src/rational_distance/concordant/safe_pair_sieve.py`
- `src/rational_distance/concordant/chain_closure_sieve.py`
- `src/rational_distance/concordant/dual_closure_sieve.py`
- `src/rational_distance/concordant/analysis.py`
- `src/rational_distance/concordant/fast_multi_n.py`
- `src/rational_distance/proof_status/types.py`
- `src/rational_distance/proof_status/schema.py`
- `src/rational_distance/proof_status/methods.py`
- `src/rational_distance/proof_status/workflow.py`
- `src/rational_distance/proof_status/fast_core.py`
- `scripts/prove_no_solution.py`
- `scripts/prove_no_solution_multi_first.py`
- `tests/test_proof_status.py`
- `tests/test_proof_status_fast_core.py`
- `tests/test_chain_fast.py`
- `tests/test_coprime_mod12.py`

Commands run:
- `git status --short`
- `ls -la docs/audits/2026-06-07-theory-framework-audit/subagent-notes`
- `rg --files docs/work-logs | rg '0(67|...|104)'`
- `rg -n "fast-core|no_solution|summary|safe_sieve|full-plane|GEN-CLOSURE|gcd-aware|unconditional" docs/work-logs`
- `rg -n "def generate_ab_pairs|def iter_ab_pairs" src scripts tests`
- `rg -n "iter_ab_pairs|generate_ab_pairs" scripts/prove_no_solution.py src/rational_distance/proof_status`
- Many targeted `nl -ba ... | sed -n ...` reads for line-number evidence.
- `PYTHONPATH=src uv run python` smoke check of `run_safe_sieve` on `(6,15)`, `(8,20)`, `(12,24)`.
- `PYTHONPATH=src uv run python` search for non-coprime pairs killed by `safe_sieve` but not by `gcd_aware_kills`.
- `PYTHONPATH=src uv run python` search for safe-surviving multi-N pairs where old sum-only `find_killer_modulus` kills but `full_plane=True` does not.

Claims checked:
- Reduced `(A,B)` safe filter: `A` odd, `B` odd, `(A+B) % 4 == 0`.
- Pair-level `mod1680` empty sieve.
- `chain-fast --safe-pair-sieve` orientation / `v2` / post-construction `N % 4` conditions.
- `gcd-aware` mod-12 / guaranteed divisor `D_g`.
- Full-plane `GEN-CLOSURE` versus old inside-square sum-only closure.
- `dual_closure_sieve` and `prove_no_solution_multi_first.py` use of closure sieve.
- `proof_status` labels: `no_solution`, method outcome terminal behavior, and fast-core summary semantics.
- Whether docs distinguish proof, necessary condition, finite scan, and engineering status.

Fatal findings:
- None identified in this slice for the current default `proof_status --max-hyp` path. The current default `proof_status` path uses full-plane `GEN-CLOSURE` for `chain_closure_mod_sieve` and exhaustive `gen_closure_hit` in `factor_concordant`.

High-risk findings:
- H1. `proof_status --pair` can feed arbitrary non-coprime input into a coprime-only `safe_sieve`, then store a terminal `no_solution` label.
  Evidence: `scripts/prove_no_solution.py` parses `--pair` by checking only positivity and ordering; it does not check `gcd(A,B)=1` or that the pair came from the reduced generator (`scripts/prove_no_solution.py:45-57`). The help text says `--pair` processes a single `'A,B'` pair, while only `--max-hyp` explicitly says “reduced” (`scripts/prove_no_solution.py:137-149`). The file docstring even shows `--pair 264,420`, which is non-coprime (`scripts/prove_no_solution.py:15-17`).
  Evidence: the batch generator does reduce: it divides by `gcd(A,B)` before yielding (`src/rational_distance/concordant/pairs.py:27-36`). So the risk is mainly the manual `--pair` / direct API path, not the normal `--max-hyp` stream.
  Evidence: `run_safe_sieve` calls `classify_reduced_pair(A,B)` and returns terminal `outcome="no_solution"` for `mixed_parity` and `odd_odd_wrong_mod4` (`src/rational_distance/proof_status/methods.py:103-128`). But the called helper says its soundness is conditional on coprime/reduced input and explicitly says it is not valid for non-coprime `(A,B)` (`src/rational_distance/concordant/safe_pair_sieve.py:1-22`, `src/rational_distance/concordant/safe_pair_sieve.py:30-43`).
  Evidence: the stored meaning of `no_solution` is strong: “mathematically proven” in the status type and schema comments (`src/rational_distance/proof_status/types.py:13-18`, `src/rational_distance/proof_status/schema.py:13-18`). The workflow stops at the first terminal `no_solution` and writes it (`src/rational_distance/proof_status/workflow.py:229-258`).
  Smoke check: `(6,15)` is non-coprime, but `run_safe_sieve(6,15)` returns `no_solution` with `classification='mixed_parity'`. That exact pair is also killed by the newer gcd-aware condition, so it is not a false result example; it is evidence that the coprime-only method is reachable without its precondition.
  Stronger smoke check: examples such as `(51,975)` and `(75,495)` are non-coprime, are killed by old `safe_sieve` as `odd_odd_wrong_mod4`, are not killed by `gcd_aware_kills`, and have at least two concordant `N` values. In the sampled cases `gen_closure_hit` was still `None`, so I did not find a false `no_solution`; the risk is a proof-label/precondition mismatch.
  Why this matters in plain language: the code can say “proved impossible” after using a rule whose own file says “only use me after reducing to coprime input.” Even if sampled outputs happened to be true, the certificate path is not clean.

- H2. `scripts/prove_no_solution_multi_first.py` and `dual_closure_sieve.py` still use the old sum-only closure sieve while their wording can be read as full Harborth no-solution proof.
  Evidence: `chain_closure_sieve.killed_at_modulus(..., full_plane=False)` is explicitly the old inside-square sum relation only (`src/rational_distance/concordant/chain_closure_sieve.py:146-173`). Full-plane soundness needs `full_plane=True` and all four sum/difference relations impossible (`src/rational_distance/concordant/chain_closure_sieve.py:153-165`).
  Evidence: current production `proof_status` knows this and calls `find_killer_modulus(..., full_plane=True)` (`src/rational_distance/proof_status/methods.py:137-169`). That is the good path.
  Evidence: `dual_closure_sieve.dual_pair_killed` calls `killed_at_modulus(a,b,m)` without `full_plane=True` (`src/rational_distance/concordant/dual_closure_sieve.py:66-69`). `scripts/prove_no_solution_multi_first.py` calls `find_killer_modulus(a,b,moduli)` and then `find_surviving_n_pair(...)`, again with default sum-only behavior (`scripts/prove_no_solution_multi_first.py:85-103`).
  Evidence: the multi-first script describes itself as a “Harborth no-solution prover” and says its pipeline proves no Harborth counterexample using dual-closure sieve (`scripts/prove_no_solution_multi_first.py:1-16`, `scripts/prove_no_solution_multi_first.py:269-273`). The summary output reports “primary killed” and “dual killed” as killed counts without warning that this is sum-only (`scripts/prove_no_solution_multi_first.py:306-317`).
  Evidence: wl073 contains stale strong wording: “unconditional 全杀” and an “effective, unconditional” lemma up to `max_hyp <= 2,000,000` based on `chain_closure_mod_sieve(STANDARD_MODULI)` (`docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md:205-238`). Later wl094 correctly says the old production判据 only checked `N1+N2=A+B` inside the square and that full-plane requires the upgraded four-relation `GEN-CLOSURE` (`docs/work-logs/094-gen-closure-landing-A9.md:5-13`, `docs/work-logs/094-gen-closure-landing-A9.md:19-45`).
  Smoke check after applying the script's actual `allow_reduced_pair` filter: at `max_hyp=100000`, I found safe-surviving multi-N pairs where old sum-only primary sieve kills but full-plane primary sieve does not, for example `(11339,37765)` with `Ns=[3480,222300]`, old killer `361`, full-plane `None`; `(10207,78793)` with old killer `9`, full-plane `None`; `(10879,30821)` with `Ns=[8772,31080,233772]`, old killer `361`, full-plane `None`.
  Why this matters in plain language: the old script can reject a pair because it cannot close in one geometric position, while the full Harborth question allows other positions. The current main `proof_status` route fixed this, but the old multi-first route and its docs still look too strong.

Medium/low findings:
- M1. `chain_closure_sieve` keeping `full_plane=False` as the default is backwards-compatible but easy to misuse. The docstring is honest (`src/rational_distance/concordant/chain_closure_sieve.py:146-165`), but callers making all-plane claims must remember to opt in. Current `proof_status` does; `multi_first` and `dual_closure_sieve` do not.
- M2. Some docs still state safe/core methods too broadly. `docs/IMPLEMENTATION.md` says `safe_sieve` and `factor_concordant` are strict necessary conditions without restating the reduced/coprime caveat for `safe_sieve` (`docs/IMPLEMENTATION.md:120-127`). This is mostly a documentation risk, because later docs are clearer, but it can mislead someone using the API manually.
- M3. `fast-core` summary is aggregate, not a full pair-by-pair certificate for killed pairs. This is documented correctly in the fast-mode docs: killed pairs only enter summary and DB usually only stores survivors (`docs/PROOF_STATUS_FAST_MODE.md:24-34`, `docs/PROOF_STATUS_FAST_MODE.md:184-194`; also wl069 `docs/work-logs/069-proof-status-fast-core-mode.md:10-16`, `docs/work-logs/069-proof-status-fast-core-mode.md:87-100`). The risk is only if a reader treats a summary count as a full audit trail.
- M4. Archived `CONCORDANT_SAFE_FILTERS.md` correctly limits the three reduced-pair conditions to `generate_ab_pairs()` output (`docs/archive/CONCORDANT_SAFE_FILTERS.md:12-22`, `docs/archive/CONCORDANT_SAFE_FILTERS.md:143-159`), but it predates the newer gcd-aware replacement for arbitrary non-coprime `(A,B)`. It should remain marked historical/archived when cited.

Non-issues worth noting:
- The reduced `(A,B)` safe condition itself is not overclaimed in the current helper file. `classify_reduced_pair` is narrow, and the file explicitly says to use `gcd_aware_kills` / `guaranteed_divisor` for non-coprime input (`src/rational_distance/concordant/safe_pair_sieve.py:1-22`, `src/rational_distance/concordant/safe_pair_sieve.py:61-93`).
- The pair-level `mod1680` sieve is documented as an empty sieve, not as a proof route: `N=0 mod m` always passes, so the `mod1680` table is all true (`docs/archive/CONCORDANT_SAFE_FILTERS.md:29-67`).
- `chain-fast --safe-pair-sieve` looks internally consistent in this slice. The doc lists four proven necessary conditions (`docs/archive/CHAIN_FAST_SAFE_FILTERS.md:58-179`), the implementation applies only orientation / `v2` / post-construction `N % 4` checks (`src/rational_distance/chain_fast/safe_pair_sieve.py:11-68`), tests cover those exact helpers (`tests/test_chain_fast.py:118-176`), and the API refuses non-Python backend use (`src/rational_distance/chain_fast/api.py:183-188`).
- The current default `proof_status` pipeline has been upgraded to full-plane `GEN-CLOSURE`: method docs say `chain_closure_mod_sieve` is full-plane and `factor_concordant` uses exhaustive `gen_closure_hit` (`src/rational_distance/proof_status/methods.py:1-28`, `src/rational_distance/proof_status/methods.py:213-287`, `src/rational_distance/proof_status/methods.py:705-714`). Tests also assert the full-plane call path (`tests/test_proof_status.py:108-129`) and the `factor_concordant` `no_solution` behavior (`tests/test_proof_status.py:37-50`).
- `gcd-aware` / `D_g` is framed as a necessary-condition sieve, not a full Harborth proof. The implementation says `guaranteed_divisor` divides every concordant `N` and `gcd_aware_kills` is sound for any `(A,B)` (`src/rational_distance/concordant/safe_pair_sieve.py:61-93`). Tests exercise small exhaustive ranges and boundary non-coprime counterexamples (`tests/test_coprime_mod12.py:66-155`). wl099/wl104 also say these are necessary conditions and finite scans, with the global problem still open (`docs/work-logs/099-gcd-aware-Dg-sound-sieve.md:26-53`, `docs/work-logs/104-phase-summary-coprime-to-fullspace.md:17-35`, `docs/work-logs/104-phase-summary-coprime-to-fullspace.md:66-74`).

Open uncertainties:
- I did not run the full test suite.
- I did not exhaustively search for a concrete false `safe_sieve` terminal `no_solution` on non-coprime input. I found the precondition mismatch and sampled non-coprime cases where old `safe_sieve` is not justified by `gcd_aware_kills`, but sampled cases still had no `GEN-CLOSURE` hit.
- I did not re-run `prove_no_solution_multi_first.py` end-to-end under a full-plane rewrite. I only checked code paths and sampled safe-surviving primary mismatches up to `max_hyp=100000`.
- I did not prove that `dual_closure_sieve` has an actual dual-only false kill under full-plane semantics; the risk is from direct inspection that it calls the old default and from the stale wording around the multi-first route.

Recommended updates to main claim ledger:
- Add / keep a ledger item: `safe_sieve` is rigorous only on reduced/coprime `(A,B)` input. For arbitrary `--pair`, either enforce `gcd(A,B)=1`, skip `safe_sieve`, or replace the first-stage arbitrary-pair kill with `gcd_aware_kills`.
- Add a method-precondition field to any proof ledger / DB export: a `no_solution` row should record not only the method name, but also the input assumptions the method needed.
- Split closure terminology in the ledger: `sum-only / inside-square closure` is not the same as `full-plane GEN-CLOSURE`. Mark `scripts/prove_no_solution_multi_first.py` and `dual_closure_sieve.py` as legacy inside-square unless upgraded to pass `full_plane=True` and re-audited.
- Mark wl073 “unconditional full kill” style claims as historical/sum-only unless revalidated through the current full-plane `proof_status` or an upgraded multi-first route.
- Keep `gcd-aware` / `D_g` as “proved necessary conditions for arbitrary `(A,B)`,” not as a global impossibility proof. Keep finite scans labeled as finite scans.
- Keep fast-core summary counts separate from full audit rows. A summary count can support a claim ledger entry, but it is not itself a per-pair proof log.

Plain-language summary:
The current main `proof_status` route is mostly careful: it now uses the full four-relation closure test and does not rely on bounded experiments as proof. The main safety problem is at the edges. First, the manual `--pair` path can run a coprime-only safe rule on non-coprime input and still write the strong label `no_solution`. Second, the older `multi_first` / dual-closure route still uses the old “inside the square only” closure sieve while its wording sounds like a full Harborth proof. In simple terms: the strongest labels are mostly okay on the main reduced/coprime production path, but some entry points and old documents make the proof look broader than the code actually justifies.
