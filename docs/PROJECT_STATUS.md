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

The current narrow handoff is more specific and is recorded in
[NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md):

```text
wl527_completed_function_field_proof_data_scope_not_ready
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

`wl524` chose the next narrow route: attempt that new uniform cover-family
squareclass obstruction lemma later, using `wl523` as input. It did not enter
the proof attempt, execute shell 11, compute supports, test new ambient
`C_d` solubility, apply `wl491` to a new point, select a final obstruction
candidate, or claim theorem-level Selmer progress.

`wl525` entered that selected proof attempt at the cover-family statement
layer. The attempted promotion failed from the current inputs: the finite
15 cover-family / 29 entry taxonomy has no cover-family function-field
squareclass certificate, divisor parity data, or specialization argument. This
does not mathematically refute a possible future uniform lemma; it only
refutes promoting the finite taxonomy to that theorem. No next roadmap step is
entered by `wl525`.

`wl526` is the post-`wl525` route-choice audit. It compares the four explicit
route families: gather minimal function-field squareclass proof data, return
to finite shell / `M_tail` diagnostics, name a theorem-level complete-Selmer
local/Hilbert row obligation, or abandon this obstruction line and select a
different candidate. It selects only the first as the later narrow gate,
because that is the smallest move addressing the missing proof-data failure.
`wl526` does not enter the gate, build function-field models, prove the
uniform lemma, name a Selmer row, select a candidate, execute shell 11, or
claim theorem-level progress.

`wl527` enters only the `wl526` selected proof-data scoping gate. It inventories
the 15 named globally soluble but not AA+BB-admissible cover families and finds
the current data is not ready for a later uniform squareclass proof attempt:
zero cover families are ready. The exact missing class is explicit
cover-family function-field model/map/squareclass-certificate data: models,
rational source-side maps, `N,M` as function-field elements, an opposite-side
product squareclass or divisor-parity certificate, and exceptional
specialization / positivity separation. This is not a proof or refutation of
the possible uniform lemma, and no next roadmap step is entered.

## Current Stop Rules

Do not execute shell 11, compute new supports, test new ambient `C_d`
solubility, apply `wl491` to a new point, select a final obstruction candidate,
or run broad rank/Selmer diagnostics unless the user explicitly asks for that
route. After `wl527`, do not treat proof-data scoping as a ready proof attempt.
Do not treat the `wl522` finite taxonomy, the `wl524` route choice, the failed
`wl525` promotion attempt, the `wl526` route choice, or the `wl527` scoping
inventory as proof of a uniform cover-family lemma.
