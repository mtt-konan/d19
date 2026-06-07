Slice:

concordant-multi-n（多 N / 高秩 / 闭合条件 / Ono-Peschmann-HH 文献翻译）

Files inspected:

- `docs/MULTI_CONCORDANT_N_STRATEGY.md`
- `docs/MULTI_N_FILTER_LADDER.md`
- `docs/THEORY_DIRECTIONS.md`
- `docs/THEORY_DIRECTIONS_ADVANCED.md`
- `docs/literature/notes/ono-1996-concordant.md`
- `docs/literature/notes/peschmann-2604-09328.md`
- `docs/literature/notes/halbeisen-hungerbuhler-2021.md`
- `docs/literature/notes/halbeisen-hungerbuhler-voznyy-2024.md`
- `docs/work-logs/046-multi-concordant-n-scan-10k.md`
- `docs/work-logs/047-literature-and-multi-n-tooling.md`
- `docs/work-logs/048-fast-pivot-on-n-scanner.md`
- `docs/work-logs/049-f2-rank-classifier-on-multi-n-catalog.md`
- `docs/work-logs/050-pari-ellrank-on-110-high-f2-candidates.md`
- `docs/work-logs/051-f2-rank-method-in-proof-status.md`
- `docs/work-logs/052-max-hyp-100k-scan-and-rank-audit.md`
- `docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md`
- `docs/work-logs/074-path-a-k2-closure-fiber-analysis.md`
- `docs/work-logs/075-theory-direction-survey-and-path-a-pickup.md`
- `docs/work-logs/076-conjecture-a1-proof-sketch.md`
- `docs/work-logs/081-path-a-pickup-algebraic-step-a-strict.md`
- `docs/work-logs/082-path-a-A2-hard-proven-Gaussian.md`
- `docs/work-logs/083-conjecture-a1-fully-proven.md`
- `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md`
- `docs/work-logs/091-f4-peschmann-sieve-vs-mod-p2-closure.md`
- `docs/work-logs/092-direction5-heegner-decider-redundant.md`
- `docs/work-logs/093-closure-necessity-linear-relations-A9.md`
- `docs/work-logs/104-phase-summary-coprime-to-fullspace.md`
- `src/rational_distance/concordant/factor_search.py`
- `src/rational_distance/concordant/fast_multi_n.py`
- `src/rational_distance/concordant/half_points.py`
- `src/rational_distance/concordant/heegner_height.py`
- `src/rational_distance/concordant/two_descent_rank.py`
- `src/rational_distance/concordant/analysis.py`
- `src/rational_distance/concordant/chain_closure_sieve.py`
- `scripts/multi_n/multi_concordant_n_scan.py`
- `scripts/multi_n/validate_fast_multi_n.py`
- `scripts/multi_n/noncoprime_full_scan_fast.py`
- `scripts/theory/analyze_multi_n_half_points.py`
- `scripts/theory/classify_multi_n_by_f2_rank.py`
- `scripts/theory/k4_two_descent_rank.py`
- `scripts/theory/k4_rank.py`
- `scripts/theory/heegner_vs_factor_decider.py`
- `scripts/theory/closure_necessity_relations.py`
- `tests/test_fast_multi_n.py`
- `tests/test_half_points.py`
- `tests/test_two_descent_rank.py`
- `results/multi_n/non_coprime_scan_max500_summary.json`
- `results/multi_n/non_coprime_scan_max2000_summary.json`
- `results/multi_n/full_scan_max2000.json`
- `results/multi_n/full_scan_max10000.json`
- `results/multi_n/full_scan_max100000.json`

Commands run:

- `pwd && ls`
- `find .. -name AGENTS.md -print`
- `sed -n '1,260p' docs/MULTI_CONCORDANT_N_STRATEGY.md`
- `sed -n '1,260p' docs/MULTI_N_FILTER_LADDER.md`
- `sed -n '1,260p' docs/THEORY_DIRECTIONS.md`
- `sed -n '1,300p' docs/THEORY_DIRECTIONS_ADVANCED.md`
- `rg --files docs/literature/notes docs/work-logs src/rational_distance/concordant scripts/multi_n scripts/theory tests results/multi_n`
- `rg -n "multi[- ]?N|closure|rank|Ono|Peschmann|Heegner|2-descent|square-x|Y=1|Harborth" ...`
- `nl -ba ... | sed -n ...` on the docs, worklogs, source files, scripts, and tests listed above
- `ls -lh results/multi_n/*summary* results/multi_n/full_scan_max2000.json results/multi_n/full_scan_max10000.json results/multi_n/full_scan_max100000.json`
- `sed -n '1,220p' results/multi_n/non_coprime_scan_max500_summary.json`
- `sed -n '1,220p' results/multi_n/non_coprime_scan_max2000_summary.json`
- `sed -n '1,220p' results/multi_n/full_scan_max2000.json`
- `uv run pytest -q tests/test_fast_multi_n.py tests/test_half_points.py tests/test_two_descent_rank.py`
- `git status --short`

Claims checked:

1. Whether a `multi-N pair` is only "there are multiple concordant integer N values" rather than a complete square / full Harborth configuration.
2. Whether rank, positive rank, F2-rank, "strongly concordant", or 2-descent images are being used as sufficient conditions for multi-N or closure.
3. Whether `N1 + N2 = A + B` is kept as a necessary condition with the right scope, and whether later full-plane GEN-CLOSURE corrections are reflected.
4. Whether Ono / Peschmann / Halbeisen-Hungerbuhler notes keep external theorem scope narrow instead of importing broader conclusions.
5. Whether implementation matches the conservative theory story: exact integer-N enumeration, half-point analysis, F2-rank as lower-bound evidence only, and Heegner as diagnostic only.

Fatal findings:

1. **Sum-only closure is still stated as a Harborth necessary condition in the main strategy doc, but later project work shows it is only the inside-square case.**

   `docs/MULTI_CONCORDANT_N_STRATEGY.md` states that a Harborth 4-chain counterexample must satisfy `N1 + N2 = A + B` (lines 64-92), and its current judgment repeats that a counterexample must come from square-x points satisfying this linear closure (lines 394-402). That is too broad unless the target is explicitly "point inside the unit square".

   Later work corrects the geometry. `docs/work-logs/093-closure-necessity-linear-relations-A9.md` says the existing `b=A+B-N` / reflection test only checks the inside-square sum relation (lines 15-24), derives the full-plane condition `{N1+N2, |N1-N2|} ∩ {A+B, |A-B|} != empty` (lines 59-85), and explicitly says sum-only failure only rules out inside-square counterexamples (lines 86-105). Current code now reflects that split: `check_chain_compatibility` is documented as the sum / inside-square constraint, while `gen_closure_hit` implements full-plane GEN-CLOSURE and carries the gcd-scaling caveat (`src/rational_distance/concordant/analysis.py:284-315`). `chain_closure_sieve.killed_at_modulus` also has `full_plane=False` default and documents the four-relation full-plane mode (`src/rational_distance/concordant/chain_closure_sieve.py:146-165`).

   Impact: any main ledger claim of "no Harborth counterexample" based only on `N1+N2=A+B` is unsound for the all-plane formulation. It is sound only for the inside-square formulation. The ledger should use GEN-CLOSURE for full-plane/reduced claims, and the full-space non-coprime pipeline for non-coprime claims.

2. **Any ledger entry still citing `wl083` / early A1 as a strict proof must be downgraded.**

   `docs/work-logs/076-conjecture-a1-proof-sketch.md` tries to prove `k=2 => rank >= 2`, but the key jump is "Q is not a 2-torsion point, therefore its 2-descent image is not in the 2-torsion image" (lines 102-113). `docs/work-logs/081-path-a-pickup-algebraic-step-a-strict.md` correctly identifies this as a logic gap: being unequal as a point is not the same as being unequal modulo `2E(Q)` (lines 13-33). `docs/work-logs/083-conjecture-a1-fully-proven.md` then overclaims a complete proof (lines 54-99 and 152-156), but `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md` records a concrete k=4 counterexample to the Gaussian uniqueness step (lines 20-37), identifies the root cause (lines 38-71), and concludes the A1 strict proof is not complete and remains open (lines 73-92 and 125-152).

   Impact: `k=2 => rank >= 2` is currently empirical evidence, not an algebraic theorem. This does not break the exact N enumeration or closure scans, but it does break any proof narrative that relies on A1 as established.

High-risk findings:

1. **The Heegner / height direction is internally mixed: current code is conservative, but parts of `THEORY_DIRECTIONS_ADVANCED.md` still read like a future no-solution decider.**

   The implementation is safe: `src/rational_distance/concordant/heegner_height.py` says the finite scan is not a global non-existence proof and must return diagnostics / inconclusive without a certified bound (lines 10-16), and the scan notes repeat no negative conclusion is claimed (lines 402-405). `docs/work-logs/092-direction5-heegner-decider-redundant.md` goes further: `factor_concordant` already exhaustively decides integer concordant N for all ranks, before Heegner runs (lines 10-14, 17-29, 31-38), and the true remaining gap is closure-necessity, not height (lines 79-100).

   However, `docs/THEORY_DIRECTIONS_ADVANCED.md` still contains older direction-five language: directly compute a rank-1 generator and, if its X is not an integer square and MW is generated, "strictly prove no concordant integer N" (lines 109-113), plus a later "medium target" suggesting canonical height work could upgrade 37% of hard cases to `proven_no_solution` (lines 398-420). That should be either removed or clearly marked historical/outdated, because the same document's top table already says height-bound upgrade was judged redundant (lines 17-24).

2. **F2-rank is correctly implemented as informational now, but stale worklog language still makes it sound like a no-solution shortcut.**

   `docs/work-logs/049-f2-rank-classifier-on-multi-n-catalog.md` says F2-rank can shrink the search pool with "rank=0/1 -> impossible" and suggests `F2-rank <= 2 -> rank <= 0` / no 4-chain (lines 98-119). That is false as a theorem. `docs/work-logs/050-pari-ellrank-on-110-high-f2-candidates.md` corrects it: F2-rank can both under- and over-estimate actual rank; the strict relation is only `F2-rank <= min(k, rank + 2)` and `F2-rank >= 3 => rank >= 1` (lines 49-55), with explicit caution that F2-rank=2 can still have rank 2 (lines 100-103). `docs/work-logs/051-f2-rank-method-in-proof-status.md` implements the correction: F2-rank is an evidence recorder, not a no-solution decider (lines 9-20).

   Current source mostly follows the corrected version: `two_descent_rank.py` describes F2-rank as a "proxy" and only gives the lower-bound style relation (`src/rational_distance/concordant/two_descent_rank.py:8-19`). The main ledger should still explicitly say "F2-rank gives lower-bound/evidence only; never terminal."

3. **"multi-N is high rank" should be phrased as a pattern / source of examples, not a theorem.**

   `docs/MULTI_CONCORDANT_N_STRATEGY.md` says `(153,560)` confirms multi-N is "elliptic curve high-rank phenomenon" (line 35). `docs/work-logs/046-multi-concordant-n-scan-10k.md` goes further and says multiple concordant N means rank >= 2 (lines 133-140). Later evidence shows the relationship is weaker: k=4 does not mean rank >= 4 (`docs/work-logs/048-fast-pivot-on-n-scanner.md:108-126`), rank 5 can have only k=3 (`docs/work-logs/050-pari-ellrank-on-110-high-f2-candidates.md:107-108`), and high rank does not mean many square-x / integer-N points. The safer statement is: concordant N values give special square-x points; multi-N often signals positive/higher rank structure, but rank alone neither guarantees multiple integer N nor closure.

Medium/low findings:

1. **The main `MULTI_CONCORDANT_N_STRATEGY` doc is older than later full-plane / non-coprime corrections.**

   It correctly presents L2 multi-N and L4 closure as separate layers (lines 85-92 and 274-282), and it carefully distinguishes Ono positive rank from d19's `Y=1` / `x=N^2` special section (lines 145-162). But it still frames the dataset and current judgment around reduced coprime pairs and sum closure. Later work says reduced coprime is not WLOG for full-space search: `docs/work-logs/104-phase-summary-coprime-to-fullspace.md` says a minimal counterexample only forces `gcd(A,B,N1,N2)=1`, not `gcd(A,B)=1`, and old coprime-only filters missed the non-coprime half-space (lines 8-14). The strategy doc should be labeled "reduced coprime / inside-square historical strategy" or updated to the full-space pipeline.

2. **`chain_closure_sieve` default remains sum-only.**

   This is not wrong because the function now documents the default as inside-square only and exposes `full_plane=True` (`src/rational_distance/concordant/chain_closure_sieve.py:146-165`). The risk is operational: callers must choose full-plane mode when making all-plane claims. The non-coprime full scan does so (`scripts/multi_n/noncoprime_full_scan_fast.py:88-103`).

3. **Peschmann note contains a good warning, but main docs should inherit it.**

   `docs/literature/notes/peschmann-2604-09328.md` says d19 still needs a strict "Harborth chain -> EC/rational-point" lemma (lines 32-43), and `docs/work-logs/091-f4-peschmann-sieve-vs-mod-p2-closure.md` fixes the category error between Peschmann's per-point modular search and d19's parameter/closure sieve (lines 11-29 and 68-78). This is good, but the same caveat should be in the main claim ledger, not only in literature notes/worklogs.

Non-issues worth noting:

1. **Fast multi-N generation is not pretending to find full square solutions.**

   `fast_multi_n.py` returns reduced coprime `(A,B)` pairs with at least two shared concordant N values (`src/rational_distance/concordant/fast_multi_n.py:185-221`). The docstring says pairs sharing two or more N are exactly multi-concordant pairs, not closure candidates or Harborth solutions (lines 185-191). Tests compare it with brute force / factor search and passed in this audit (`tests/test_fast_multi_n.py`, 17 total tests across fast/half/F2 modules passed).

2. **Integer-N enumeration is exact and height-free.**

   `factor_search.py` proves completeness by mapping every integer solution `(N,h3,h4)` to a divisor pair of `B^2-A^2` (lines 20-23) and the public function has no upper-bound parameter (lines 88-104). `fast_multi_n.exact_concordant_pair` intersects exact per-leg divisor enumerations and also documents no EC sampling dependency (`src/rational_distance/concordant/fast_multi_n.py:142-155`).

3. **Ono translation is mostly careful.**

   The Ono note explicitly says positive rank gives infinitely many primitive solutions in Ono's general `(x,y,t,z)` form, while d19 fixes `y=1`, `x=N`, i.e. a square-x / special-section problem (lines 31-71). The strategy doc repeats the same boundary (lines 138-162). This avoids the main literature-scope error.

4. **Halbeisen-Hungerbuhler translation is mostly careful.**

   The H-H 2021 note says the curve is the same but the special point type differs; H-H's positive-rank equivalences do not directly give d19 multi-N criteria (lines 69-97). The H-H-Z 2024 note narrows applicability to a measure-zero subfamily where `(A,B)=(a^h,b^h)` and `(a,b)` is Pythagorean (lines 85-95). That is appropriately limited.

5. **Peschmann translation is appropriately bounded after wl091.**

   The Peschmann note explicitly says the paper does not prove non-existence and has a remaining gap (lines 11-30 and 65-72). wl091 distinguishes Peschmann's per-point modular search from d19's closure-reflection sieve and warns not to drop `p ≡ 3 mod 4` primes in d19 (lines 57-78).

Open uncertainties:

1. I did not independently re-derive Ono/Peschmann/H-H from the PDFs or browse external sources; this audit used the local literature notes and worklogs. The local notes are internally cautious, but formal claim-ledger entries should still cite the actual theorem statements if they become proof dependencies.

2. GEN-CLOSURE is documented as full-plane for reduced legs, but `analysis.gen_closure_hit` keeps the `MATH §8.6` gcd-scaling caveat (`src/rational_distance/concordant/analysis.py:311-315`). Later full-space scans address non-coprime cases empirically and with gcd-aware necessary conditions (`docs/work-logs/104-phase-summary-coprime-to-fullspace.md:30-75`), but this remains finite evidence rather than a global theorem.

3. `k=2 => rank >= 2` remains empirically strong on sampled safe-pass pairs (`docs/work-logs/074-path-a-k2-closure-fiber-analysis.md:304-321`, `docs/work-logs/084-A1-bug-finding-and-honest-reassessment.md:134-152`), but the algebraic proof is open.

Recommended updates to main claim ledger:

1. Replace any unqualified "Harborth counterexample requires `N1+N2=A+B`" with:

   "For points inside the unit square, closure is `N1+N2=A+B`. For the full plane, use GEN-CLOSURE: `{N1+N2, |N1-N2|} ∩ {A+B, |A-B|} != empty`. Reduced-pair claims still carry the gcd-scaling caveat unless using the full-space non-coprime pipeline."

2. Record `multi-N` as:

   "At least two integer concordant N values for the same `(A,B)`. This is a necessary half-solution layer, not a complete square / Harborth solution. A closure relation is still required."

3. Record rank claims as:

   "Positive rank / strongly concordant / H-H pythapotent theorems generate or explain general rational/primitive solutions, but d19 needs the rarer `Y=1` / `x=N^2` section. High rank is neither sufficient for multi-N nor for closure."

4. Record F2-rank claims as:

   "F2-rank of half-point images is evidence / lower-bound structure only. It is not a no-solution shortcut and does not give an upper bound on Mordell-Weil rank."

5. Mark `wl083` as superseded by `wl084` in the ledger:

   "A1 proof attempted, bug found; A1 remains empirical/open."

6. Mark Heegner-height decider as superseded by `wl092`:

   "Heegner/height scan is a witness finder / diagnostic. Integer concordant N are already exhaustively enumerated by factorization; remaining proof work is closure/global geometry, not height coverage."

Plain-language summary:

Think of `multi-N` as "the same two horizontal lengths can pair with several possible vertical lengths to make right triangles." That is useful, but it is still only a pile of half-finished pieces. A real Harborth configuration also needs two of those vertical lengths to line up with the square's geometry. For an inside-square point that line-up is `N1+N2=A+B`; for a point outside the square there are three more sum/difference possibilities.

The current code is mostly careful and has moved toward the right model: exact N enumeration, a full-plane closure helper, non-coprime scans, conservative Heegner, and F2-rank as evidence. The main risk is stale theory text: older docs still make sum-only closure and A1/rank statements sound stronger than the later corrected worklogs allow.
