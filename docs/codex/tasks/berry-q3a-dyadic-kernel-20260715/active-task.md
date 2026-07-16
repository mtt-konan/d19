# Active Task: Berry Q3a Dyadic Fake Kernel

- Status: complete
- Updated: 2026-07-16
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

The exact Q3a2 coordinate presentation is now complete.  The two primary
quotients `O/P_1^9` and `O/P_2^17` give the 16-dimensional product
squareclass space, the diagonal matrix has rank `4`, the product norm and its
induced fake-quotient map have rank `4`, and therefore
`dim F_varpi=12`, `dim H_varpi=8`.  All sixteen global ambient localization
columns are computed in the same basis and have rank `16`; after the diagonal
quotient their rank is `12`.

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

## Final Q3a2 Embedding-Bit Check

A single final free-Magma Calculator wrapper submission was prepared from
`q3a2-embedding-bit.m`. The 1,712-byte source uses exact `Completion`,
`Factorization`, `ext`, `Roots`, and `IsIrreducible` operations to construct
`K=Q(i)`, complete at `P=<1+i>`, define the degree-2 and degree-4 factor
fields, and test whether the quadratic factor becomes reducible over the
quartic field. The request used the public 60-second limit.

The wrapper failed before receiving calculator XML with
`status=transport_error` and
`<urlopen error [Errno 1] Operation not permitted>`. No Magma intrinsic was
executed remotely, no exact embedding bit was obtained, and no raw JSON was
preserved. The detailed boundary is recorded in
`q3a2-embedding-bit-service-gap.md`. This is a service/sandbox gap, not an
arithmetic conclusion. Worker session id:
`019f6677-001b-7f92-8c64-455f1559f895`. The focused regression run passed
(`9 passed`).

## Reopened Boundary

The prior `precise_C1_etale_descent_blocker` judgment from `692f49d` is
withdrawn as a modeling error and retained as a historical failed-boundary
record. Do not use the finite-precision `Factorization(g6v)` display or the
derived `E_2 subset E_4` branch as a required theorem. The next exact task is
`construct_dyadic_diagonal_and_norm_matrices_from_global_prime_completions`:
construct the absolute degree-4/degree-8 completions from the two certified
global prime ideals above `2`, restrict the four base-field squareclasses,
and compute the diagonal image, norm map, and `H_varpi` by exact matrix rank.

On 2026-07-16 the existing 1,712-byte submission was retried once by Worker
`019f6683-5f7d-7e13-99ce-118ae414970d` with the mandated proxy and 60-second
timeout. It failed again before a calculator response; no raw JSON or exact
embedding bit was produced. The source and task files remained unchanged.

## Accepted Q3a2 Exact Matrix Checkpoint

The withdrawn embedding-bit model is replaced by the exact global-prime
completion computation in `q3a2-dyadic-diagonal-norm-matrices.md`.
`scripts/theory/berry_sextic_q3a_dyadic_matrices.sage` generates the exact
primary-quotient, diagonal, norm, quotient, kernel, and sixteen-column
localization payload.  The standalone Python verifier reconstructs the
finite quotient squareclass cosets and checks all matrices and ranks.

Accepted exact values:

```text
dim W_varpi = 16
rank B_varpi = 4
dim F_varpi = 12
rank Nbar_varpi = 4
dim H_varpi = 8
rank(global ambient localization) = 16
rank(fake localization) = 12
```

This completes Q3a2 only.  The next exact step is Q3a3: construct the local
fake Kummer image `I_varpi` inside the explicit eight-dimensional
`H_varpi`, and decide `D_inf in 2J(K_varpi)` by an exact divisor/function,
formal-group, or local Kummer calculation.  The source dimension `5` and the
Q3a2 matrix ranks alone do not determine either result.

## Q3a3 Worker Boundary

The current worker pass added `q3a3-exact-kummer-boundary.md`. It certifies
the reciprocal-chart divisor normalization and the local class of
`D_i=[(i,v_i)-P_+]` in the frozen Q3a2 coordinates, giving the lower bound
`dim(I_varpi)>=1`. It did not produce the remaining divisor/formal-group
certificates and did not decide `D_inf in 2J(K_varpi)`. This is an incomplete
worker result, not an arithmetic blocker or a Q3b/Q4 transition.

Controller review independently reproduced this class from the exact primary
quotients and accepted it with
`scripts/theory/berry_sextic_q3a3_exact_class.sage`, its serialized payload,
standalone verifier, and focused test.  The accepted vector is
`H_varpi=(0,1,1,1,0,1,1,0)`, so the current rigorous bounds are still only
`dim(I_varpi)>=1` and `dim(kappa_varpi)<=4`.  Q3a3 remains active; the next
exact step is the complete formal-group/divisor basis and the independent
`D_inf` half-divisor decision.

## Q3a3 D_inf Worker Certificate

The exact worker certificate in
`q3a3-dinf-local-divisibility.md` decides the independent binary theorem:

```text
D_inf=[P_+-P_-] is not in 2J(K_varpi).
```

The proof reduces every even-degree Mumford representation branch to the
identity `w^2-f=c*u^2`, rules out the degree-zero and degree-one branches by
exact coefficient identities, and rules out the degree-two branch by the
monic degree-10 elimination polynomial and its exact lambda-adic residue
tree.  The reciprocal chart, both infinity points, tangent/factor-zero, and
the local Weierstrass branch are retained.  The pure-Python verifier and
exact Sage elimination script pass their focused checks.

Controller review accepts the binary theorem after correcting the first
residue-tree terminal base from `1+lambda^2+lambda^3` to
`1+lambda^2+lambda^3+lambda^4`, strengthening the Sage degree-zero/one
coefficient checks, and rerunning both exact certificates.  Consequently
`D_inf` is a nonzero one-dimensional subspace of the fake-map kernel, so
`dim(kappa_varpi)>=1` and `dim(I_varpi)<=4`.  This does not complete the
remaining local fake image or the full kernel.  The next exact step is to
construct three further independent image classes (or an equivalent complete
formal-group image computation) and decide whether the kernel has any class
beyond the certified `D_inf` line.

## Q3a3c Incomplete Worker Pass

Worker `019f69e7-2eff-79e2-85c1-42727046def9` searched for three further
exact image classes.  Its rational-point experiments did not certify the
initial apparent rank-four vectors: after correcting the local square test,
they supplied at most the existing `D_i` line and the unreviewed factor-zero
class below.  This invalidates the exploratory rank-four claim.

The pass did produce one unreviewed exact candidate: the degree-two
factor-zero Mumford class attached to the Hensel factor `h_2` of `g6`, with
proposed vector

```text
H_varpi = 01111010.
```

Its current producer uses a strict generalized-Hensel factorization margin
and tangent normalization, and the standalone verifier reconstructs the
Q3a2 quotient coordinates.  Controller acceptance still requires checking
that the Hensel correction precision preserves both primary-quotient
squareclasses and that the factor-zero evaluation formula covers both
infinity points.  Even if accepted, this raises the certified image rank only
to `2`; two more independent exact degree-two or formal-group classes remain.

The Worker was stopped after a subsequent Sage calculation consumed roughly
fourteen CPU minutes without output.  This is an incomplete tool path, not an
arithmetic blocker.  The next narrow task is to construct exactly the two
missing independent degree-two Mumford/formal-group classes, using exact
multivariate Hensel or local Cantor certificates rather than another
rational-point search.

## Q3a3 Exact-Sequence Closure

The explicit-class search is superseded by the exact cohomological kernel
calculation in `q3a3-fake-kernel-exact-sequence.md`.  For
`R=Res_(A_varpi/K_varpi)(mu_2)` and `Q=R/mu_2`, even degree gives

```text
1 -> J[2] -> Q -> mu_2 -> 1.
```

Q3a2 proves that the four-dimensional base squareclass space restricts
injectively to `A_varpi`, so `Q(K_varpi)=R(K_varpi)/mu_2(K_varpi)`.  The two
field factors have relative degrees `2,4`; their sole sign class modulo the
diagonal has trivial norm because both degrees are even.  Hence the
cohomological fake kernel has dimension exactly one.  The accepted nonzero
class `D_inf` realizes it.  Therefore

```text
ker(delta_varpi)=<D_inf>,
dim ker(delta_varpi)=1,
dim I_varpi=5-1=4.
```

Controller verification is in
`scripts/theory/berry_sextic_q3a3_fake_kernel.py` and its focused test.  The
unreviewed Q3a3c payload and its apparent vectors are discarded.  Q3a3 is
complete; Q3b-Q4 and every global Selmer/rank conclusion remain closed.

The first independent audit, Worker
`019f6a76-899a-7ab3-932f-349fd93d45cf`, correctly rejected an implicit
identification of all `H^1(K_varpi,Q)` with the fake quotient because an
even-degree Brauer cokernel remains.  The proof was revised to retain that
cokernel and use the injective fake-quotient map plus the divisor-evaluation/
Kummer commutative square.  Fresh Worker
`019f6a82-ba58-7021-845c-575b4fe6419a` accepted the revised implication after
an adversarial read-only audit.  The Brauer class affects the cokernel and
does not enlarge the kernel computed above.
