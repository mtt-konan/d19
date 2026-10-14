# scripts/ - Script Entry Index

This file indexes usable entry points. Historical WL-by-WL narration belongs
in `docs/work-logs/`; this page keeps the current executable graph and the
small set of general-purpose tools.

Executable availability is not a task selection. Research activity is routed
through [NEXT_RESEARCH_GATE.md](../docs/NEXT_RESEARCH_GATE.md); preserved AA+BB
tools do not imply that the old route should resume automatically.

## Start Here

| Area | Entry point |
| --- | --- |
| Main search | `search.py` (`--help` for chain-fast, EC, and parametric modes) |
| Hard-case proof pipeline | `prove_no_solution.py` |
| Multi-N proof variant | `prove_no_solution_multi_first.py` |
| Concordant lookup | `lookup_multi_n.py` |
| Preserved AA+BB graph | `theory/aa_bb/` below |

## General Tools

### `benchmark/`

Performance and ordering checks:

- `benchmark_candidate_generators.py`
- `benchmark_ab_sieve_orders.py`
- `benchmark_parallel_executor.py`
- `bench_mod_sieve.py`

### `multi_n/`

Enumeration and result-directory tools:

- `fast_multi_concordant_scan.py`
- `multi_concordant_n_scan.py` (slow reference implementation)
- `non_coprime_multi_n_scan.py`
- `build_results_catalog.py`
- `k_distribution_audit.py`
- `validate_fast_multi_n.py`
- `dscale_kn_generator.py`

### `partner/`

Partner graph and `K_n` analysis:

- `partner_bfs.py`, `partner_full_bfs.py`, `partner_full_graph.py`
- `partner_full_graph_query.py`, `partner_pair_graph.py`
- `partner_pair_k_distribution.py`
- `partner_bfs_analyze.py`, `partner_bfs_plot.py`
- `partner_kn_subgraphs.py`, `comp0_analyze.py`
- `export_gephi_component.py`, `find_partner_origin.py`
- `verify_missing_partner.py`, `verify_kn_equivalence.py`
- `full_gm_closure_scan.py`, `full_gm_delta_stats.py`
- `k8_ellrank.py`, `k9_inspect.py`, `k10_extract_and_ellrank.py`
- `cycle_ellrank.py`

### `theory/`

Earlier closure and rank experiments remain available as historical or
diagnostic tools. The preserved AA+BB graph is under `theory/aa_bb/` below.
Other useful families include:

- Path A: `analyze_k2_closure_fiber.py`, `analyze_k2_f2_rank.py`,
  `analyze_k2_height_bound.py`, `analyze_kn_f2_rank.py`
- Pythagorean / half-points: `analyze_a2_pythagorean.py`,
  `analyze_multi_n_half_points.py`, `audit_halfpoint_factorization.py`
- F2 rank: `classify_multi_n_by_f2_rank.py`, `pari_rank_high_f2.py`,
  `k4_rank.py`, `k4_two_descent_rank.py`,
  `rank_mixed_closure_curves.py`

### `utility/`

- `magma_calculator.py`: submit a `.m` file to the free University of Sydney
  Magma Calculator, parse its XML transcript, and distinguish success from a
  Magma error or the public 60-second timeout.

```bash
uv run python scripts/utility/magma_calculator.py \
  scripts/theory/berry_sextic_magma_capabilities.m

uv run python scripts/utility/magma_calculator.py \
  scripts/theory/berry_sextic_magma_two_selmer.m \
  --json-out /private/tmp/berry-magma-two-selmer.json

uv run python scripts/utility/magma_calculator.py \
  scripts/theory/berry_sextic_magma_capabilities.m --print-url
```

The fast probe should exit `0`. The full selected `TwoSelmerGroup` probe
currently exits `2` because the public service terminates it at 60 seconds;
that exit code is a service result, not an arithmetic obstruction.

## Preserved AA+BB Graph

The canonical `wl500-wl593` executable graph is:

```text
A0 -> A1 -> A2
B0 -> B1
C1 -> C2 -> C3
D0u ----\
D0m -----+-> D5 -> D7 -> D17 -> D4 -> wl586, wl593 projections
A0/A2/C3 /
```

Stage ownership:

| Stage | WL coverage | Canonical module |
| --- | --- | --- |
| A0/A1/A2 | `wl500-wl527` | `consolidation_inputs.py`, `a1_certificates.py`, `a2_evidence.py` |
| B1 | `wl528-wl529` | `b1_prototype.py` |
| C1 | `wl530-wl541` | `c1_pure_v_ell.py` |
| C2 | `wl542-wl568` | `c2_pure_v_ell.py` |
| C3 | `wl569-wl585` | `c3_pure_v_ell.py` |
| D4 | `wl586`, `wl593` | `d4_factor_twist.py` |

`wl586` and `wl593` are semantic projections of D4, not separate current
executables. The old per-WL scripts were removed after full parity checks;
their paths remain only as provenance strings where needed.

Human reading order:

1. [491-522 history](../docs/work-logs/491-522-aa-bb-admissibility-taxonomy-consolidated.md)
2. [523-529 history](../docs/work-logs/523-529-common-source-function-field-squareclass-consolidated.md)
3. [530-585 history](../docs/work-logs/530-585-pure-v-ell-m1-m2-consolidated-checkpoint.md)
4. [D4](theory/aa_bb/d4_factor_twist.py)
5. Protected appendices: [wl587](../docs/work-logs/587-pure-u7-d0-relative-2-descent.md), [wl589](../docs/work-logs/589-mixed-d0-relative-2-descent.md), [wl590](../docs/work-logs/590-p5-factor-twist-local-image-comparison.md), [wl591](../docs/work-logs/591-mixed-p7-factor-twist-local-image.md), and [wl592](../docs/work-logs/592-mixed-p17-factor-twist-local-image.md)

## Canonical Commands

Use a temporary uv cache outside the repository.

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m scripts.theory.aa_bb.a1_certificates \
  --data-dir data/theory/aa_bb/wl500

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m scripts.theory.aa_bb.b1_prototype \
  --data-dir data/theory/aa_bb/wl500 \
  --sage-artifact data/theory/aa_bb/wl500/b1-sage-certificate.v1.json \
  --out /private/tmp/d19-b1.json --strict

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m scripts.theory.aa_bb.c1_pure_v_ell \
  --out /private/tmp/d19-c1.json --strict

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m scripts.theory.aa_bb.c2_pure_v_ell \
  --out /private/tmp/d19-c2.json --strict

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m scripts.theory.aa_bb.c3_pure_v_ell \
  --out /private/tmp/d19-c3.json --strict

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python -m scripts.theory.aa_bb.d4_factor_twist \
  --data-dir data/theory/aa_bb/wl500 \
  --out /private/tmp/d19-d4.json --strict
```

The A0 loader and A2 builder are callable APIs; they do not have standalone
builder CLIs. `consolidation_inputs.py` also provides the explicit materializer
CLI for the 30 frozen ignored source payloads. Default tests use tracked
canonical inputs and do not read `results/`; regeneration checks live in
`manual_tests/`.

## Protected D Kernels

These five kernels remain separate. D4 composes them without merging their
builders, tests, formulas, local images, survivor ledgers, or no-claim bounds.

| WL | Module | Boundary |
| --- | --- | --- |
| `wl587` / D0u | `wl587_pure_u7_d0_relative_2_descent.py` | Fixed pure-`u_7` D0 schema; odd bad-prime filtering and D1 remain unevaluated. |
| `wl589` / D0m | `wl589_mixed_d0_relative_2_descent.py` | Independent mixed D0 schema; selected odd bad-prime images remain a later gate. |
| `wl590` / D5 | `wl590_p5_factor_twist_local_image_comparison.py` | `I_{5,u}=empty set`, `I_{5,m}={[5]}`; no later-prime or D2 claim. |
| `wl591` / D7 | `wl591_mixed_p7_factor_twist_local_image.py` | `I_{7,m}={[1]}`; only `91205` survives the selected p=7 row. |
| `wl592` / D17 | `wl592_mixed_p17_factor_twist_local_image.py` | `I_{17,m}={[u]}` excludes `[91205]=[17u]`; no D2 entry. |

The downstream `wl594` G0 input, `wl595` G4 route-death certificate, and
`wl596` exact `H_RL` Q0 divisor-allocation blocker have their own scripts and
worklogs. The existing `wl597_hrl_closure_discriminant.py` certifies the scoped
symmetric closure discriminant and dyadic branch reduction without claiming a
family theorem. It is not an automatically selected research assignment.

## Other Directories

- `modular/`: mod-p2 class and CRT experiments.
- `utility/`: small standalone utilities such as `extract_pdf_text.py`.
- `archive/`: historical scripts; do not add new work there.

## Path Convention

Scripts under a nested directory should derive the repository root explicitly:

```python
ROOT = Path(__file__).parent.parent.parent
```

Top-level entry points use `Path(__file__).parent.parent`. New accepted AA+BB
mathematical checkpoints use the short triplet pattern:

```text
docs/work-logs/<wl>-<short-topic>.md
scripts/theory/aa_bb/wl<wl>_<short_topic>.py
tests/theory/aa_bb/test_wl<wl>_<short_topic>.py
```

Other research modules keep their own ownership boundaries; a new method is
not required to live under `aa_bb/`. Documentation maintenance and exploratory
task preparation do not create a WL. Task selection is recorded in
[NEXT_RESEARCH_GATE.md](../docs/NEXT_RESEARCH_GATE.md).
