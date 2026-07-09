# Project Status

This is the current status entry. Old run-by-run records live in the
[worklog index](./work-logs/README.md).

## Current Mainline

The active mainline is:

```text
closure quotient
  -> lambda = A/B ray ledger
  -> AA/BB rank-zero certificates
  -> rank-zero Selmer family proof attempt
```

Entry points:

- [CLOSURE_QUOTIENT_MAINLINE.md](./CLOSURE_QUOTIENT_MAINLINE.md)
- [NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md)
- [OPEN_DIRECTIONS.md](./OPEN_DIRECTIONS.md)
- [GLOSSARY.md](./GLOSSARY.md)
- [worklog index](./work-logs/README.md)

普通话说：现在不是继续数更多 `(A,B)`，而是想证明一整批
`lambda=A/B` ratio family 的 `AA/BB` quotient rank 为 0。

## What Is Proved

Strictly proved or safely usable:

- GEN-CLOSURE 是正确的全平面闭合语言：
  `{N1+N2, |N1-N2|}` 必须和 `{A+B, |A-B|}` 相交。
- 旧 concordant 曲线会漏掉闭合腿 `M=A+B-N` 的信息。
- `AA/BB rank=0 + torsion pullback` 是严格有限证书。
- 已认证的 `AA/BB rank=0` 行只回拉到中点，没有完整闭合点。
- 中点分支由 Yang Ji 定理关闭。
- `AB/BA` 不是 rank-zero 击杀器。

## What Is Not Proved

还没有证明：

- Harborth 全局命题。
- 所有 `lambda` family 的 rank-zero 定理。
- residual two-cover / Sha[2] candidate 没有有理点。
- theorem-level `Sel_2(E_L/Q)` upper bound.

Counts, samples, package totals, and candidate totals are not proof progress by
themselves. They matter only when they shrink a named proof gap or produce a
strict certificate.

## Current Bottleneck

The high-level bottleneck remains the Selmer/rank-zero family proof:

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

The current narrow gate is more specific and is recorded in
[NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md):

```text
post_wl523_route_choice_not_entered_here
```

`wl522` compressed the `wl491`-`wl521` AA+BB admissibility ledgers into a
support/cover taxonomy. `wl523` then tried the isolated lemma candidate:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

The point-level obstruction is already proved by the existing `wl491`
machinery: a certified centered-even pullback with non-square opposite-side
common-source product cannot enter the AA+BB admissible ledger. The stronger
uniform cover-family reading is still unproved and would need a new lemma. It
is not a Selmer upper bound, not a rank-zero theorem, and not a family
exclusion.

## Current Stop Rules

Do not execute shell 11, compute new supports, test new ambient `C_d`
solubility, apply `wl491` to a new point, select a final obstruction candidate,
or run broad rank/Selmer diagnostics unless the user explicitly asks for that
route. The next narrow mathematical move, if selected, is a post-`wl523` route
choice: attempt a new uniform cover-family squareclass lemma, or return later
to finite-shell diagnostics.
