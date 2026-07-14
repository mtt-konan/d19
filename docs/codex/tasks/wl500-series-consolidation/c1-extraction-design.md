# C1 Extraction Design

## Verdict

```text
worker_outcome = c1_extraction_design_ready
controller_accepted = true
implementation_status = complete
```

`wl530-wl541` can be extracted without new mathematics or tracked input data.
Every symbolic identity, finite table, cutoff, and witness is recomputed in
code. Ignored results remain test-only parity sources.

## Paths

```text
scripts/theory/aa_bb/c1_pure_v_ell.py
scripts/theory/aa_bb/c1_wl535.py
scripts/theory/aa_bb/c1_local_tables.py
scripts/theory/aa_bb/c1_wl539.py
scripts/theory/aa_bb/c1_wl540.py
scripts/theory/aa_bb/c1_wl541.py
tests/theory/aa_bb/test_c1_pure_v_ell.py
tests/theory/aa_bb/test_c1_cli.py
```

```python
build_c1() -> C1Evidence
project_stage(evidence, work_log) -> dict
semantic_projection(payload, work_log) -> dict
```

`build_c1()` executes every kernel once and returns stages `wl530-wl541`. It
must not import legacy builders, results, the consolidated script, A/B loaders,
or `wl542+`.

## Kernel Boundaries

- `c1_pure_v_ell.py`: shared symbolic reductions and separate projections for
  `wl530-wl534`.
- `c1_wl535.py`: protected direct q-root kernel, including both inverse
  patches, removable branches, antipode sign switch, and exact converse.
- `c1_local_tables.py`: one parameterized engine with independent tables and
  statements for `wl536-wl538`.
- `c1_wl539.py`: protected Weil cutoff and exhaustive finite certificate.
- `c1_wl540.py`: parameter-prime valuation/Hensel kernel.
- `c1_wl541.py`: protected genus-three Hasse-Weil, small witnesses, and
  simultaneous Hensel certificate.

## Required Evidence

- `wl530`: symbolic `p,q,sqrt_q`, every complete-`d` equation/chart/map,
  `t,N,M`, positivity, both products, square-locus quartic and quotient,
  discriminants, and exact `ell=5` recovery.
- `wl531`: paired quadratics, `A_ell/B_ell`, cross identity, every zero branch,
  converse reconstruction, positivity, and `ell=7/13` examples.
- `wl532-wl534`: the `Q=16/A` reduction, mod-4 exclusion, nonzero branches,
  circle parameterization and inverse patches, visible exceptions, antipode,
  `C/Y/S/R/T`, discriminant `4*ell`, automatic lower branch, and exact
  examples.
- `wl535`: exact proposition requiring squares `ell-q^2`, `ell*q^2+4`, strict
  positivity `ell*q^4+4*q^2-4*ell>0`, and `V^2=G_ell(q^2)`.
- `wl536-wl538`: all residue rows, values, failure reasons, square sets, and
  exact classes `5 mod 28`, `21 mod 44`, `53 mod 76`.
- `wl539`: degrees `[1,1,1,4]`, coefficient `41`, zero bound `7`, cutoff
  `1907`, degenerate `e=1,2`, exact pairs `(7,5),(11,10),(19,15),(23,5)`, and
  the added class `5 mod 92`.
- `wl540`: unit valuations, discriminant `2^29`, Gaussian factorization,
  simple-root identity, `ell=1 mod 8` root branch, and `ell=5 mod 8` unit-only
  conclusion.
- `wl541`: degree-eight genus-three curve, two infinity and twelve removable
  points, cutoff `61`, Hasse-Weil bound, all seven small-prime witnesses,
  simultaneous derivatives, and `real_positivity_addressed=False`.

## Parity

Use an explicit twelve-file legacy result map, never globbing. Per-stage
semantic allowlists compare formulas, checks, converse data, examples, tables,
proof status, boundaries, and no-claim flags. Ignore JSON order, CLI text,
`ready`, and cached violations. The unowned
`wl536_q_square_tangent_cubic_obstruction.json` does not enter C1.

The `wl530-wl585` consolidated result is a secondary read-only oracle only;
assert its independent symbolic review and M2-open/M3-closed boundary without
creating a runtime dependency.

One shared strict CLI replaces twelve subprocess tests. Honest formatted target
is 2400-3000 code lines across six kernels and 1000-1500 test lines across two
files, with no formatter suppression. All theorem-level claims and
`advance_to_m3` remain false. No cutover, deletion, or `wl542+` change occurs.

## Controller Acceptance

C1 is accepted at 3241 formatted implementation lines and 267 focused test
lines. The code is slightly above the estimate because the protected
`wl530-wl535` reduction chain is retained explicitly; no formatter suppression
or dense-line workaround is used. The smaller test surface is accepted because
23 tests include exact twelve-file semantic parity plus dedicated protected
kernel and fail-closed assertions.

Controller validation with all prior slices is 86 focused tests passing.
Targeted Ruff, formatter check, `py_compile`, the strict twelve-stage CLI,
the consolidated secondary oracle, and `git diff --check` pass. Runtime C1
contains no legacy builder, results, glob, A/B loader, or `wl542+` dependency.
