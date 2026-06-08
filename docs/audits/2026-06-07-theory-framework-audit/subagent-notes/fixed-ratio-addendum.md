# Fixed-Ratio Addendum

Slice:
fixed-ratio / rational-ratio route（controller 2026-06-09 补审）

Files inspected:
- `docs/work-logs/106-d4-point-plot-and-centerline-branch.md`
- `docs/work-logs/107-theory-transfer-routes-and-fixed-ratio.md`
- `docs/work-logs/108-fixed-ratio-sieve-boundary.md`
- `docs/work-logs/109-fixed-ratio-exact-multin-ratio-scan.md`
- `docs/work-logs/110-fixed-ratio-reciprocal-orbit-proof-boundary.md`
- `docs/work-logs/111-fixed-ratio-cross-orbit-line-problem.md`
- `docs/work-logs/112-fixed-line-curve-model-and-rs-target.md`
- `docs/work-logs/113-fixed-ratio-square-rectangle-model.md`
- `docs/work-logs/114-fixed-ratio-translation-curve-and-2adic-boundary.md`
- `docs/work-logs/115-rational-ratio-upgrade-strategy.md`
- `docs/work-logs/116-rational-ratio-module-and-proof-boundary.md`
- `src/rational_distance/concordant/fixed_ratio_exact.py`
- `src/rational_distance/concordant/fixed_ratio_sieve.py`
- `src/rational_distance/concordant/rational_ratio.py`
- `tests/test_fixed_ratio_exact.py`
- `tests/test_fixed_ratio_sieve.py`
- `tests/test_rational_ratio.py`
- `tests/test_scan_fixed_ratio_exact.py`

Commands run:
- `uv run ruff check src/rational_distance/concordant/fixed_ratio_exact.py src/rational_distance/concordant/fixed_ratio_sieve.py src/rational_distance/concordant/rational_ratio.py scripts/theory/scan_fixed_ratio_exact.py tests/test_fixed_ratio_exact.py tests/test_fixed_ratio_sieve.py tests/test_rational_ratio.py tests/test_scan_fixed_ratio_exact.py`
- `uv run pytest tests/test_rational_ratio.py tests/test_fixed_ratio_exact.py tests/test_fixed_ratio_sieve.py tests/test_scan_fixed_ratio_exact.py -q`
- `uv run pytest -q`

Claims checked:
- Center-line / `A=B` is a low-dimensional branch, not the whole problem.
- Fixed integer ratio `A=kB` is a real proof slice, but it covers only integer ratios.
- Pure residue sieves cannot close fixed-ratio branches because `B≡0, N1≡1, N2≡-1 (mod M)` survives every modulus in that model.
- Exact fixed-ratio scans must use true concordant `N`, not arbitrary residue survivors.
- Same reciprocal orbit can be handled in the integer fixed-ratio setting, but cross-orbit closure remains open.
- Any route that hopes to touch the full normalized square problem must upgrade from integer `k` to rational `λ=A/B`.

Fatal findings:
- None as a current top-level claim. The worklogs now state the boundary: integer `A=kB` is not a global proof route by itself.

High-risk findings:
- Integer fixed-ratio closure would become a fatal overclaim if a future report says it covers the full square problem. A normalized candidate gives `λ=A/B∈Q_{>0}`, not necessarily an integer.
- The old integer proof trick `k^2+1` is not a rational square does not survive the upgrade to rational `λ`. Example: `λ=3/4` gives `λ^2+1=(5/4)^2`.
- A quadratic same-orbit equation can have rational roots without producing true `R_λ` members. The tests cover `λ=6` and `λ=3/2` danger samples.
- A residue survivor is not a true concordant `N`. The fixed-ratio sieve module exists mostly to record this negative fact.

Medium/low findings:
- The center-line branch remains worth a local proof note, but it is a special-position theorem.
- The integer fixed-ratio exact scan is useful as a pattern finder. It found reciprocal-paired ratios in small data and no non-center closure hit for the recorded scan window, but this is finite evidence.
- The rational-ratio module records exact `Fraction` identities and theorem targets; it does not generate integer candidates or prove `A=λB` impossible.

Non-issues worth noting:
- The fixed-ratio work did not modify the production `proof_status` pipeline.
- `fixed_ratio_sieve.py` names a negative result plainly: pure congruence certificates cannot kill the branch.
- `rational_ratio.py` separates three things that the audit cares about: algebraic roots, true membership in `R_λ`, and real closure equalities.

Open uncertainties:
- No proof currently shows that two `R_λ` points satisfying full-plane closure must be reciprocal mates `s=λ/r`.
- No proof currently closes all rational ratios `λ`.
- Yang Ji's fixed-line special cases help with low-dimensional branches, but the repo has not converted them into a full local proof note or a global theorem.

Recommended updates to main claim ledger:
- Add fixed-ratio as an open theory slice, not a closed branch.
- Add rational-ratio theorem target as the correct next form:
  `r,s∈R_λ` plus full-plane closure should force `s=λ/r`, if that theorem is true.
- Add an overclaim risk: "all integer `k` closed" would still not prove all rational `λ`.

Plain-language summary:
固定比例这条线没有死，但它不能当总证明。证明 `A=kB` 像证明某些斜率的直线；真正候选会给出有理比例 `λ=A/B`。下一步如果继续走这条线，应该攻 `R_λ` 上的平移/反射交点，而不是继续把整数 `k` 扫大。
