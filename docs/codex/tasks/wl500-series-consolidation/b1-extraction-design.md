# B1 Extraction Design

## Verdict

```text
worker_outcome = b1_extraction_design_ready
controller_accepted = true
implementation_status = complete
```

`wl528-wl529` can share one protected B1 module and one focused test file. B1
consumes tracked B0 rows and one tracked Sage certificate; runtime never reads
ignored results.

## Paths And API

```text
data/theory/aa_bb/wl500/b1-sage-certificate.v1.json
scripts/theory/aa_bb/b1_prototype.py
tests/theory/aa_bb/test_b1_prototype.py
```

`consolidation_inputs.py` and the manifest may be extended only to materialize
and bind this certificate.

```python
load_sage_certificate(path) -> SageCertificate
refresh_sage_certificate(output, sage="sage") -> Path
build_b1(*, b0, sage_certificate) -> B1Evidence
project_b1(b1, work_log) -> dict
semantic_projection(payload, work_log) -> dict
```

## Protected Mathematics

- Keep `Q(r,y)/(y^2-(5*r^4-264*r^2+2000))` and all five complete-`d`
  identities/maps.
- Keep `t,z,N,M`, the leg-1 source square, AA/BB symmetry, and
  `(N^2+16)(M^2+16)`.
- Recompute the specialization `r=10,y=160,t=6,N=11/2,M=-1/2`, its cover and
  elliptic points, all nine prerequisites, and nonsquare `12025/16`.
- Keep the square locus `U^2=t^4+78*t^2+7921`, projective quadrics, and the
  one-way degree-two map `X=t^2,Y=tU` to
  `Y^2=X^3+78X^2+7921X`. Do not claim birationality or a converse from an
  arbitrary quotient point.
- Validate the Sage proof boundary: proved rank zero, proof method, torsion
  invariants `[4]`, full torsion points, and square-X values `['0']`. A cached
  rank boolean alone is invalid.
- Keep the separate `t=0` branch, `y=0`, quadratic
  `5*x^2-264*x+2000`, discriminant `29696=2^10*29`, and no rational lift.
- Keep `|t|<5`, positive `N,M`, chart exclusions `r=0`, `r^2=20`, `X+p=0`,
  and all unclassified zero loci. The checked specialization has `M<0` and is
  not itself a positivity-domain point.
- Keep every theorem/no-claim flag false.

## Sage Boundary

The tracked artifact stores curve coefficients, exact Sage marker and program
provenance, proved rank/method, torsion data, full torsion points, and square-X
classification. `refresh_sage_certificate` runs the existing Sage program once
with explicit temporary `DOT_SAGE` and `TMPDIR`; normal loading has no Sage or
results fallback. The manifest binds both source and projection bytes.

## Parity And Size

Old/new semantic projections compare both exact legacy result payloads for B0
rows, scope, formulas/maps, specialization, square locus, Sage proof,
discriminant/no-lift, positivity, exceptions, proof fields, and no-claim flags.
They ignore prose, JSON order, readiness caches, and CLI formatting.

One test file covers identities, B0 parity, fail-closed mutations, quotient
direction, `t=0`, no-claim boundaries, old/new parity, and one shared Python
CLI smoke. Sage refresh is an explicit integration command, not a default test.
Hard limits: 650 module lines, 750 test lines, certificate under 3 KB. No
cutover or deletion occurs in this slice.

## Controller Acceptance

B1 is accepted with one explicit size exception: the genuinely formatted,
readable module is 766 lines rather than 650. The first implementation reached
the nominal cap only by disabling `E501` and creating lines up to 833
characters; that version was rejected. The final module has no line over 100
characters and passes `ruff format --check`. Splitting another helper module
would violate the accepted one-module shape, while further compression would
remove proof obligations or reintroduce dense formatting.

Final validation is 63 focused tests, exact `wl528`/`wl529` semantic parity,
targeted Ruff, formatter check, direct CLI, deterministic full materialization,
checked-in byte parity, manifest loading with three auxiliary bindings,
`py_compile`, and `git diff --check`. The Sage refresh command is implemented
but was not rerun; the tracked certificate retains the previously proved Sage
result and exact source hash.
