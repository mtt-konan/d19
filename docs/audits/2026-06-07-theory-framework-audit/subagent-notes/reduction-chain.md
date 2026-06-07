Slice:
reduction-chain

Files inspected:
- `README.md`
- `docs/MATH.md`
- `docs/GLOSSARY.md`
- `docs/DIRECTIONS.md`
- `docs/CURRENT_FINDINGS.md`
- `docs/PROJECT_STATUS.md`
- `docs/MULTI_CONCORDANT_N_STRATEGY.md`
- `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md`
- `docs/work-logs/074-path-a-k2-closure-fiber-analysis.md`
- `docs/work-logs/075-theory-direction-survey-and-path-a-pickup.md`
- `docs/work-logs/076-conjecture-a1-proof-sketch.md`
- `docs/work-logs/077-direction-2-height-bound-and-pivot-to-path-b.md`
- `docs/work-logs/078-path-b-mod-p2-kill-audit.md`
- `docs/work-logs/079-path-b-phase4a-multi-n-mod-pattern.md`
- `docs/work-logs/080-path-b-closeout-and-recap-073-079.md`
- `docs/work-logs/081-path-a-pickup-algebraic-step-a-strict.md`
- `docs/work-logs/082-path-a-A2-hard-proven-Gaussian.md`
- `docs/work-logs/083-conjecture-a1-fully-proven.md`
- `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md`
- Current-fix context: `docs/work-logs/093-closure-necessity-linear-relations-A9.md`, `docs/work-logs/094-gen-closure-landing-A9.md`
- `src/rational_distance/concordant/analysis.py`
- `src/rational_distance/concordant/chain_closure_sieve.py`
- `src/rational_distance/concordant/dual_closure_sieve.py`
- `src/rational_distance/concordant/factor_search.py`
- `src/rational_distance/concordant/fast_multi_n.py`
- `src/rational_distance/concordant/pairs.py`
- `src/rational_distance/concordant/safe_pair_sieve.py`
- `src/rational_distance/concordant/workflow.py`
- `src/rational_distance/concordant/half_points.py`
- `src/rational_distance/concordant/cycle_relations.py`
- `src/rational_distance/chain_fast/api.py`
- `src/rational_distance/chain_fast/kernel.py`
- `src/rational_distance/chain_fast/mod_sieve.py`
- `src/rational_distance/chain_fast/safe_pair_sieve.py`
- `src/rational_distance/chain_fast/workflow.py`
- Related call-sites checked for current ledger impact: `src/rational_distance/proof_status/methods.py`, `src/rational_distance/cli/search/runners.py`, `src/rational_distance/math_utils.py`, `src/rational_distance/_legacy/search_chain.py`
- `tests/test_concordant.py`
- `tests/test_half_points.py`
- `tests/test_cycle_relations.py`
- Related regression tests checked: `tests/test_proof_status.py`, `tests/test_chain_fast.py`, `tests/test_chain.py`, `tests/test_dual_closure_sieve.py`

Commands run:
- `pwd`
- `rg --files`
- `git status --short`
- `find docs/audits/2026-06-07-theory-framework-audit -maxdepth 3 -type f -print`
- `ls -la docs/audits/2026-06-07-theory-framework-audit/subagent-notes`
- `test -e docs/audits/2026-06-07-theory-framework-audit/subagent-notes/reduction-chain.md`
- Several targeted `rg -n` searches for `4-chain`, `common-leg`, `N1+N2`, `X=N^2`, `reduced`, `primitive`, `gcd`, `closure`, `gen_closure_hit`, `full_plane`, `check_chain_compatibility`, `factor_concordant`, `fast_multi_concordant_pairs`.
- Targeted `nl -ba ... | sed -n ...` reads for every line reference below.
- No test suite was run; this was a source/document audit only.

Claims checked:
- Point/square-distance to integer 4-chain: sound only for the stated positive inside-square model unless the later GEN-CLOSURE four-relation upgrade is used.
- 4-chain to common-leg `N`: the old `b=A+B-N` form only encodes the inside-square sum relation.
- Common-leg `N` to concordant curve `Y^2=X(X+A^2)(X+B^2)`: sound only after verifying the two individual square conditions, not merely `X=N^2` on the curve.
- `X=N^2` to actual concordant `N`: current code correctly treats square-x as necessary but not sufficient.
- Reduced pair / primitive pair generation: current pair generators intentionally emit coprime reduced pairs, not a WLOG replacement for all non-coprime legs.
- Closure `N1+N2=A+B`: fatal if used as a full-plane Harborth condition; current proof-status path has a full-plane replacement.
- gcd / primitive / sorting / positivity: sorting is not the problem; positivity and gcd are the real boundary conditions.

Fatal findings:
1. The old closure reduction `N1+N2=A+B` is not a full-plane Harborth condition.

   Evidence:
   - `docs/MULTI_CONCORDANT_N_STRATEGY.md:66-90` states `反例 => ... N1 + N2 = A + B` as the key necessary condition.
   - `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md:75-90` and `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md:230-238` use the same sum-only closure in the claimed effective lemma for reduced coprime pairs up to 2,000,000.
   - `docs/work-logs/074-path-a-k2-closure-fiber-analysis.md:14-23`, `docs/work-logs/075-theory-direction-survey-and-path-a-pickup.md:49-57`, `docs/work-logs/077-direction-2-height-bound-and-pivot-to-path-b.md:46-53`, and `docs/work-logs/078-path-b-mod-p2-kill-audit.md:94-102` all build on the sum-only form.
   - The current correction says this explicitly: `docs/MATH.md:252-260` and `docs/work-logs/093-closure-necessity-linear-relations-A9.md:15-24` state that sum closure only covers points inside the unit square, while the full-plane condition is `{N1+N2, |N1-N2|} intersect {A+B, |A-B|} != empty`.
   - Code evidence: `src/rational_distance/concordant/analysis.py:284-295` says `check_chain_compatibility` is the sum-only inside-square check; `src/rational_distance/concordant/analysis.py:298-315` implements `gen_closure_hit` for the full-plane GEN-CLOSURE condition.

   Impact:
   Any upper claim that cites wl073-wl080 as "unconditional no Harborth counterexample" is too strong unless it is explicitly limited to inside-square closure or revalidated via the current GEN-CLOSURE path. Current `proof_status` appears repaired: `src/rational_distance/proof_status/methods.py:11-27`, `src/rational_distance/proof_status/methods.py:167-170`, and `src/rational_distance/proof_status/methods.py:213-287` route terminal decisions through `full_plane=True` and `gen_closure_hit`. So this is fatal for stale ledger wording, not for the current `proof_status` implementation.

2. Reduced coprime `(A,B)` is not WLOG; the gcd-scaling gap remains independent of the closure fix.

   Evidence:
   - `src/rational_distance/concordant/pairs.py:23-36` divides by `gcd(A,B)` and emits only sorted reduced pairs; `tests/test_concordant.py:31-33` and `tests/test_concordant.py:42-49` assert all generated pairs are coprime.
   - `src/rational_distance/concordant/fast_multi_n.py:185-191` documents that it returns reduced coprime pairs; `src/rational_distance/concordant/fast_multi_n.py:214-219` skips even-even and non-coprime candidates.
   - `docs/MATH.md:498-513` says directly that `gcd(A,B)=1` is a search-space normalization, not a lossless reduction.
   - `src/rational_distance/concordant/safe_pair_sieve.py:3-17` says the reduced-pair sieve is sound only on coprime input and that non-coprime `(A,B)` is the §8.6 gap.
   - `docs/work-logs/093-closure-necessity-linear-relations-A9.md:31-34` and `docs/work-logs/094-gen-closure-landing-A9.md:94-96` state that GEN-CLOSURE fixes inside vs outside, but does not fix gcd-scaling.
   - `src/rational_distance/proof_status/methods.py:19-27` likewise limits the all-rank factor decider to reduced coprime legs and calls out non-coprime legs as a separate sub-problem.

   Impact:
   Any upper claim of a global Harborth proof or global finite search result cannot be supported by the reduced-pair pipeline alone. It must say "over reduced coprime legs" or cite a separate non-coprime/fullspace argument. The newer `gcd_aware_kills` is a sound partial sieve for arbitrary `(A,B)`, but it is not by itself a full analytic closure of the non-coprime half-space.

High-risk findings:
1. User-facing concordant diagnostics still use the old inside-square meaning of `chain_compatible`.

   Evidence:
   - `src/rational_distance/concordant/workflow.py:149-172` computes `b=A+B-n` and `chain_ok=check_chain_compatibility(...)`; it does not call `gen_closure_hit`.
   - `src/rational_distance/cli/search/runners.py:42-56` and `src/rational_distance/cli/search/runners.py:86-96` print `chain_compatible` using `check_chain_compatibility`.
   - `src/rational_distance/cli/search/runners.py:441-476` increments "Pairs with chain-compatible N" and prints "HARBORTH SOLUTIONS EXIST" from `result.has_chain_solution`, which is populated by the sum-only check in `src/rational_distance/concordant/analysis.py:367-381`.

   Impact:
   This is not a proof-status bug, but it is a communication risk. A reader can easily interpret "no chain-compatible N" as "no full-plane GEN-CLOSURE hit." The CLI should label this as "inside-square/sum closure" or also report `gen_closure_hit` when using exhaustive factor search.

2. `dual_closure_sieve` remains a legacy sum-only module.

   Evidence:
   - `src/rational_distance/concordant/dual_closure_sieve.py:10-18` states closure as `N_i + N_j = A + B`.
   - `src/rational_distance/concordant/dual_closure_sieve.py:66-69` calls `killed_at_modulus(a,b,m)` without `full_plane=True`, so it uses the default sum-only mode from `src/rational_distance/concordant/chain_closure_sieve.py:146-173`.
   - `tests/test_dual_closure_sieve.py:21-33` tests the old dual kill behavior, not the full-plane GEN-CLOSURE behavior.

   Impact:
   This module should not be cited as a full-plane obstruction unless upgraded or explicitly labeled "inside-square only." This is especially important because wl073-wl080 use dual closure in their strongest "pure mod arithmetic" claims.

3. The coprime-only safe sieve has no runtime guard in the method wrapper.

   Evidence:
   - `src/rational_distance/concordant/safe_pair_sieve.py:3-17` says `classify_reduced_pair` is conditional on coprime/reduced input.
   - `src/rational_distance/proof_status/methods.py:103-107` calls `classify_reduced_pair(A,B)` directly and returns a terminal method result from that classification; there is no `gcd(A,B)==1` assertion at this boundary.

   Impact:
   Inside the generated reduced-pair pipeline this is fine. For manual `--pair` or future non-coprime scans it is unsafe unless callers normalize the domain or use `gcd_aware_kills` / GEN-CLOSURE instead.

Medium/low findings:
1. wl081-wl083's A1 "strict proof" is already invalidated by wl084.

   Evidence:
   - `docs/work-logs/083-conjecture-a1-fully-proven.md:56-85` states Theorem A1 as proven for reduced coprime safe-pass pairs with exactly two concordant N.
   - `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md:73-92` says the proof chain is not strict and the key Gaussian uniqueness step fails.
   - `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md:127-140` gives the honest status: empirical A1 still holds up to the tested range, strict proof not complete.

   Impact:
   This is not a separate closure-reduction bug, but the main ledger should not list A1 as a theorem. It should be "empirical up to max_hyp=1M; proof gap open."

2. `gen_closure_hit` and `multi_n_sieve` disagree in wording about self-pairing.

   Evidence:
   - `src/rational_distance/concordant/analysis.py:322-329` allows `i == j` for sum relations, so a single N with `2N in {A+B, |A-B|}` could return a GEN-CLOSURE hit.
   - `src/rational_distance/proof_status/methods.py:301-307` says closure needs at least two distinct concordant integers.
   - `src/rational_distance/concordant/dual_closure_sieve.py:60-65` treats `N_i == N_j` as degenerate/killed.

   Impact:
   This is more likely to create a false positive `solution_found` than a false `no_solution`, so it does not currently threaten the no-solution ledger. Still, the project should decide whether symmetric points with equal legs are valid Harborth candidates or intentionally excluded degeneracies, and then make all three call-sites say the same thing.

3. `chain` / `chain-fast` exclude repeated `a,b,c,d` values as a baseline-search convention.

   Evidence:
   - `src/rational_distance/_legacy/search_chain.py:451-458` returns only cycles with all four values distinct and `ac != bd`.
   - `tests/test_chain.py:31-37` and `tests/test_chain_fast.py:86-91` enforce the distinct-value exclusion.
   - `docs/work-logs/034-hypotenuse-identity.md:18-20` records repeated-value cycles as degenerate.

   Impact:
   This is acceptable as a baseline convention if the ledger says so. It should not be used as a proof of the full rational-distance problem unless a separate theorem excludes the symmetric/repeated-leg cases.

Non-issues worth noting:
- The `X=N^2` issue is handled correctly in current code. `docs/MATH.md:376-388` warns that square-x on the cubic is not enough; `src/rational_distance/concordant/analysis.py:263-275` verifies both `N^2+A^2` and `N^2+B^2`; `tests/test_concordant.py:125-136` and `tests/test_concordant.py:548-560` assert this.
- The PARI-free factor search looks complete for positive unequal `(A,B)`: `src/rational_distance/concordant/factor_search.py:1-23` gives the divisor-pair completeness argument, and `src/rational_distance/concordant/factor_search.py:118-133` enumerates all divisor pairs and returns sorted distinct positive N.
- Sorting/order normalization itself is not a soundness leak. `src/rational_distance/concordant/pairs.py:27-36`, `src/rational_distance/concordant/factor_search.py:105-133`, and `tests/test_concordant.py:568-581` handle order and dedup consistently. The soundness issue is the gcd reduction, not the sort.
- Primitive Pythagorean triple generation includes both orientations and enforces the standard coprime/opposite-parity conditions: `src/rational_distance/math_utils.py:30-50`. I did not find a primitive/orientation omission in the inspected chain-fast path.
- The current proof-status terminal path is much better than the old concordant CLI diagnostics: `src/rational_distance/proof_status/methods.py:213-287` uses exhaustive factor enumeration plus full-plane `gen_closure_hit`.

Open uncertainties:
- Whether the main claim ledger already downgraded every wl073-wl080 "unconditional" statement to "inside-square / historical" or revalidated it under wl094 full-plane semantics.
- Whether a full analytic treatment of non-coprime `(A,B)` exists outside the inspected files. Current docs present empirical scans and `gcd_aware_kills`, but still label §8.6/gcd-scaling as an independent gap.
- Whether self-paired `N1=N2` / symmetric midpoint cases are intended to be excluded as degenerate, or should count as valid rational-distance candidates. The codebase currently sends mixed signals.
- Whether ordinary `scripts/search.py concordant` should be considered a proof-producing command. As written, it should be treated as diagnostic only.

Recommended updates to main claim ledger:
- Add or keep a ledger item: "RC-1 GEN-CLOSURE: `N1+N2=A+B` is inside-square only. Full-plane closure requires `{N1+N2, |N1-N2|} intersect {A+B, |A-B|} != empty`. Current `proof_status` uses the full-plane form; old wl073-wl080 claims are historical/sum-only unless re-run under `full_plane=True`."
- Add or keep a fatal/open ledger item: "RC-2 gcd-scaling: reduced coprime `(A,B)` is not WLOG. Global Harborth conclusions require a separate non-coprime/fullspace argument."
- Mark `dual_closure_sieve` as "legacy inside-square only" unless upgraded to pass `full_plane=True` and re-audited.
- Mark `search.py concordant` / `diagnose_pair.chain_compatible` as "inside-square diagnostic" and prefer `proof_status.run_factor_concordant` for all-rank full-plane reduced-pair decisions.
- Downgrade A1 strict theorem claims from wl083 to the wl084 status: empirical support only, strict proof gap open.
- Clarify self-pair policy (`N1=N2`) once, then align `gen_closure_hit`, `multi_n_sieve`, and `dual_closure_sieve`.

Plain-language summary:
The main leak is simple: "two vertical legs add up to the two horizontal legs" only describes a point inside the square. A point outside the square can satisfy a difference relation instead. The repository now has the right full-plane condition in `proof_status`, but several older strategy docs and legacy modules still speak as if `N1+N2=A+B` were the whole story.

The second serious leak is gcd. Reducing `(A,B)` to a coprime pair is convenient, but not free: a non-coprime real counterexample might disappear when you divide by the gcd because its integer `N` values need not scale down with `(A,B)`. So the reduced-pair pipeline can support "no solution for reduced coprime legs"; it cannot, by itself, support a global Harborth proof.
