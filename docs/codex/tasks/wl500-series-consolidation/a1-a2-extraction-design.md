# A1/A2 Extraction Design

## Verdict

```text
worker_outcome = a1_a2_extraction_design_ready
controller_accepted = true
implementation_started = false
```

A0 already preserves all 43 ledger IDs, eight exact `wl505` witnesses, 22
taxonomy rows, and 15 proof-data inventory rows. A1/A2 needs no additional
ignored canonical input. It adds only the arithmetic certificates and boundary
specification that cannot be reconstructed from A0.

## Obligation Split

- `A1-SHELL`: primitive shell enumeration, `L/T/sqrt_q`, exact `M_tail`
  matrices, ranks, kernels, basis supports, active rows, and duplicate guards.
- `A1-COVER`: complete `C_d` equations and elliptic product map, exact ambient
  points, four MW/no-lift certificates, deferred semantics, and the reusable
  `wl491` centered-even pullback/filter.
- `A2-TAX`: staged ledger synthesis and final support/cover taxonomy.
- `A2-LEMMA`: point-level opposite-side square obstruction, with squareclass,
  positivity, and exceptional branches separated.
- `A2-SCOPE`: failed uniform promotion, four route choices, exact missing
  proof-data class, and theorem/no-claim boundary.
- `A1/A2-BOUNDARY`: route-only checkpoints become provenance projections and
  no longer execute recursive predecessor builders.

## Per-WL Destination

```text
500 A1-COVER       501 A1-BOUNDARY  502 A1-SHELL
503 A1-BOUNDARY    504 A1-SHELL     505 A1-COVER
506 A1-COVER       507 A1-BOUNDARY  508 A1-SHELL
509 A1-BOUNDARY    510 A1-SHELL     511 A1-COVER
512 A1-COVER       513 A1-BOUNDARY  514 A1-COVER
515 A1-BOUNDARY    516 A1-SHELL     517 A1-COVER
518 A2-TAX         519 A1-COVER     520 A2-BOUNDARY
521 A2-TAX         522 A2-TAX       523 A2-LEMMA
524 A2-BOUNDARY    525 A2-BOUNDARY  526 A2-BOUNDARY
527 A2-SCOPE
```

## Canonical Shape

```text
data/theory/aa_bb/wl500/a1-certificates.v1.json
data/theory/aa_bb/wl500/a2-boundary-spec.v1.json
scripts/theory/aa_bb/a1_shells.py
scripts/theory/aa_bb/a1_ambient.py
scripts/theory/aa_bb/a1_certificates.py
scripts/theory/aa_bb/a2_evidence.py
tests/theory/aa_bb/test_a1_shells.py
tests/theory/aa_bb/test_a1_ambient.py
tests/theory/aa_bb/test_a1_a2_parity.py
tests/theory/aa_bb/test_a1_a2_cli.py
```

Public API:

```python
evaluate_shell(a0, shell_bound) -> ShellResult
verify_cover_certificate(certificate) -> CertificateChecks
build_a1(a0, certificates) -> A1Evidence
project_a1(a1, work_log) -> dict
build_a2(a0, a1, boundary_spec) -> A2Evidence
project_a2(a2, work_log) -> dict
```

The 12 deduplicated cover certificates are four no-lift cases and eight exact
point cases. A0 witnesses are referenced, not copied. Large rationals use
reduced `numerator/denominator` strings. Stage projections retain the exact
deferred counts and consume a certificate only at its original checkpoint.

## Required Parity

- Shell summaries:
  `6=(8,8,0,0,0,0)`, `7=(24,12,12,14,12,2)`,
  `8=(16,14,2,2,0,2)`, `9=(24,16,8,8,8,0)`, and
  `10=(16,6,10,10,10,0)` for
  `(sample, full-rank, kernel, basis-support, active, excluded)`.
- Recompute all three `C_d` equations and the elliptic `Y` product.
- Recompute the `wl491` pullback
  `t=Y/(2(X+p))`, `z=X/2-t^2`, `N=(A+B+t)/2`, `M=A+B-N`, both source
  products, positivity, and denominator-zero branches.
- Retain the `wl506` `-49G+T` lift, the `wl514` rank-one mod-17 empty
  rational-image/lift intersection, and the exact `wl519` rational point.
- Retain the A0 `43/8/22/15` identities and exact witness equation checks.
- Retain `43/13/22`, entry counts `10/29/4`, cover counts `5/15/2`, 29
  squareclass failures, 15 not-ready families, and the one missing explicit
  `d`-vector.
- Keep every Selmer/rank/Sha/uniform-full-rank/family-exclusion/new-local-row/
  final-candidate claim false.

Old/new comparisons ignore JSON order, cached readiness, route rank, prose,
and CLI formatting. They compare IDs, supports, `L/T/d`, matrices, kernels,
coordinates, MW image/lift checks, filter reasons, counts, route choices, and
no-claim flags.

## Runtime And Size Gate

Replace 28 scripts, 28 test files, 129 test functions, and 28 subprocess calls
only after parity. Keep one shared CLI smoke test and roughly 20-28 in-process
semantic assertions. `wl528-wl529` remain under B1 and keep their external
Sage/rank/torsion/preimage boundary.

The implementation target is four modules under 2,500 lines total and four
test files under 1,800 lines total. Reject any design that copies the existing
payload-builder chain into a new 5,000-line monolith. No consumer cutover or
deletion occurs in the implementation slice.
