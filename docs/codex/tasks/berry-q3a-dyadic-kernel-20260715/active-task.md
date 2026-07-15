# Active Task: Berry Q3a Dyadic Fake Kernel

- Status: active
- Updated: 2026-07-15
- Task id: `berry-q3a-dyadic-kernel-20260715`
- Scope: only the dyadic local divisibility of `D_inf=[P_+-P_-]` for the
  selected `C_1: v^2=g6(t)` at `K_varpi=Q_2(i)`, and the resulting exact
  fake-map kernel/image dimensions.
- Inputs: Q1 fake-descent hierarchy, Q2a local Kummer basis, Q2c global
  localization data, and the segmented local target dimension `5`.
- Forbidden: Q3b-Q3d, Q4, new Berry rows, bounded/finite-precision searches
  as proof, edits to `wl587`-`wl596`, and creation of `wl597`.

## Required Evidence

1. Set up the exact dyadic local algebra and the fake evaluation map.
2. Prove or disprove `D_inf in 2J(K_varpi)` by an explicit divisor/function,
   formal-group, or exact local Kummer computation.
3. Derive the fake-map kernel dimension and local fake-image target dimension
   from the proved divisibility result and the exact source dimension, without
   treating the source dimension alone as an image computation.

## Working Boundary

No conclusion is accepted from apparent p-adic stabilization, bounded search,
finite-precision factorization, or the number `dim J(K_varpi)/2J(K_varpi)=5` by
itself. If the divisibility proof cannot be completed, record the concrete
local algebra/formal/Kummer setup and the precise missing theorem instead of
promoting a heuristic.

## Recovery Record

The two prior Q3a Worker attempts were stopped after prolonged Sage/local
calculation with no verifiable mathematical payload. The session records are:

| session | task | last observable step | exit reason |
|---|---|---|---|
| `019f65ae-bf56-7152-9009-9fbac1e604fc` | Q3a `D_inf` local 2-divisibility | Sage/local exact calculation exploration; no accepted divisor, formal-group, or Kummer certificate | no new observable output; Worker stopped |
| `019f65ca-5184-74b1-82ea-cde6f2cac671` | fresh Q3a retry, same divisibility target | read/setup phase followed by Sage/local exact calculation exploration; no accepted certificate | user-aborted Worker run; no mathematical payload |

These are recorded as failed/incomplete attempts, not as an arithmetic
blocker. The anchor remains independent because Q3a has its own required
divisibility proof and must not be merged into the main classification anchor
until Controller review accepts the evidence.

The subsequent Q3a1 dispatch `57477` (`ask_codex` session not exposed as a
separate worker id) was terminated after roughly forty minutes of exploratory
Sage/API and local-squareclass probing. Its last observable command was an
unbounded residue-class enumeration for `v_(1+i)`; it produced no report,
changed files, or accepted Q3a1 certificate. This is another incomplete
attempt, not an arithmetic blocker.

The fresh Q3a1 Worker `019f6631-fbe8-7bf3-825a-16767f0693b5` produced
`q3a1-dyadic-fake-kernel-boundary.md`. Controller review accepted it as an
object-and-boundary setup only: it fixes `A_varpi`, `W_varpi`, `F_varpi`,
`H_varpi`, the formal localization map, and transported norm rows, while
leaving the dyadic basis, `D_inf mod 2`, `I_varpi`, and `kappa_varpi`
unresolved. The focused Q1/Q2a/Q2c regression run passed (`10 passed`).

Current next step: Q3a2, compute the exact localization matrix from the
16-dimensional ambient space into the now-defined dyadic target. Q3a3 remains
independent and is not inferred from the source dimension `5`.

## Q3a2 Attempt Record

A fresh Q3a2 Worker was dispatched under the exact Controller contract. Its
Worker session id is `unknown`; the controller PTY was `11368`. The last
observable work consisted of reading the exact Q3a1/Q2c/segmented-factor
artifacts and repeated Sage commands against the absolute degree-12 field.
No exact dyadic coordinate basis, localization column, changed file, or test
result was produced before the Worker was terminated after the same Sage path
repeated without output. This is a failed computational attempt, not a
mathematical blocker and not evidence for any Selmer or image dimension.

The exact remaining Q3a2 input is a certified coordinate presentation of
`W_varpi=A_varpi^*/A_varpi^{*2}` (including the two degree-2/4 local factors),
its diagonal base-field quotient, and its norm kernel. Formal transport of
the Q2c norm rows alone does not determine the 16 localization columns in
`H_varpi`.

A second Q3a2 attempt using the independent free-Magma route was also
started. Its Worker session id is `unknown`; controller PTY was `26155`. The
Worker completed artifact/API inspection and proxy/service probes before
termination; no Magma source, raw certificate, local basis, or localization
matrix was produced. This is an incomplete tool attempt, not an arithmetic
blocker or a service-based mathematical conclusion.

The theorem-only Q3a2 Worker `019f6658-c364-7022-b468-a48abcf9bd31` produced
`q3a2-factor-degree-dimension-audit.md`. Controller review accepts the exact
degree-only result: `dim W_varpi=16`, while `dim F_varpi` and `dim H_varpi`
are `12,8` or `13,10` according as the degree-2 factor field embeds in the
degree-4 factor field. The report proves this using local squareclass and
Hilbert norm-restriction duality, and correctly does not choose between the
two alternatives or claim localization columns. Its focused regression run
passed (`5 passed`).

Current exact substep: determine the quadratic-subfield/embedding bit from
coefficient-level local data, then obtain coordinates for the 16 global
classes. This dimension audit is not a Selmer, image, or D_inf result.

The embedding-bit Worker session id is `unknown`; its controller PTY was
`88286`. It repeated unavailable/long-running Sage maximal-order
commands and produced no certificate or file before termination. This does
not decide the embedding bit and is recorded only as an incomplete tool path.

A pure-SymPy exact-number-field embedding attempt was dispatched in this
continuation. Its Worker session id is `unknown`; controller PTY was `79403`.
The Worker reached exact `round_two`/`prime_decomp` and trace-module probing,
but the subsequent prime-ideal valuation/subfield calculation did not emit a
certificate before termination. No embedding conclusion is drawn from this
tool failure.

A fresh exact embedding-bit Worker was dispatched in this continuation. Its
Worker session id is `unknown`; controller PTY was `27489`. It read the exact
payload and attempted number-field prime/subfield calculations, but the Sage
maximal-order path repeated without producing a certificate or changed file.
It was terminated as a tool-path failure; the embedding bit remains
undetermined and no mathematical blocker is claimed.
