# Frontier Target Handoff: 1625,5643 AA

Date: 2026-07-07

## Question

Can the first external rank-proof target from the residual frontier strategy,
`(1625,5643) AA`, be packaged for stricter cover-level work?

This target covers residual priorities `5` and `7`, with cover indices `4` and
`3`. It already has a 600-second Sage rank retry timeout, so this work does not
try another short rank proof. It prepares the actual cover equations, maps, and
diagnostics needed for an external rank proof, Mordell-Weil sieve, deeper
descent, or direct `Sha[2]` obstruction.

## Handoff Export

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/export_mixed_closure_residual_handoff.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --target 1625,5643,AA \
  --cover-index 4 \
  --cover-index 3 \
  --out-dir results/mixed_closure_residual_handoffs \
  --name priority_005_1625_5643_AA_covers_4_3
```

Outputs:

```text
results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json
results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.sage
results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.magma
```

The two target quartics are:

```text
cover 4:
2510769*x^4 - 4527908*x^3 - 7744107*x^2 + 3743936*x + 3498741

cover 3:
444809*x^4 + 3153444*x^3 - 2778939*x^2 - 15767220*x + 11120225
```

The handoff records `strict_proof_status = open`. The BSD diagnostic row is
`pari-error`, so there is no BSD conditional rank-zero support for this target.

## Map Verification

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_verify_mixed_closure_handoff_maps.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_map_verify.json \
  --timeout 60 \
  --strict
```

Result:

```text
status = ok
all_verified = True
verified covers = [4, 3]
```

This checks that the stored rational maps satisfy the elliptic curve equation.
It does not prove the covers have no rational points.

## Local Witness Probe

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_probe_mixed_closure_local_witnesses.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_local_witnesses.json \
  --timeout 60 \
  --search-bound 300 \
  --max-denominator-power 3 \
  --strict
```

Result:

```text
status = ok
all_bad_primes_witnessed = True
```

This confirms the two quartics are locally soluble at the checked bad primes.
That is useful because it keeps the problem in the expected Selmer/Sha[2]
bucket; it is not a no-point proof.

## Sage Handoff Probe

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

Result:

```text
status = ok
rank_bounds = [0, 2]
rank_proof_status = runtime-error
rank_probable = 0
selmer_rank = 4
torsion_two_dimension = 2
cover_point_counts = [0, 0]
```

This bounded Sage probe is diagnostic only. The rank bounds did not close, and
the zero point counts are bounded-search evidence, not a proof.

## Boundary

This handoff improves the next external proof step for the first residual
frontier target. It does not change the strict theorem. The paper-ready strict
certificate remains the existing rank-zero `AA/BB` torsion pullback package.
