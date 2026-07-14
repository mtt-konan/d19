# D4 Extraction Design: wl586 and wl593

## Verdict

~~~text
worker_outcome = d4_extraction_design_ready
design_ready = true
implementation_status = not_started
scope = wl586 and wl593 only
protected_kernels = wl587, wl589, wl590, wl591, wl592
wl594_entered = false
~~~

D4 should replace only the two route-level checkpoints wl586 and wl593. It
should orchestrate the five protected D kernels in their existing order, but
must not merge their proof code or copy their full payloads into a new
monolith. The existing zero-argument public builders remain behaviorally and
signature compatible. To avoid rebuilding the same D0 certificates inside
each local kernel, the implementation may add narrow sibling builders that
accept already validated predecessor payloads; those adapters must call the
same formula/evidence code and prove exact equality with the zero-argument
outputs. The canonical result has two semantic stage projections, wl586 and
wl593, plus derived composition metadata. The D0 and local-image kernels
remain independently importable, testable, and reviewable.

This is a design-only result. It does not implement D4, switch a consumer,
materialize a result, delete an old artifact, edit a protected kernel, add a
prime or local row, or enter wl594.

## Owned Assets

The current 586-593 slice has seven worklog triplets. wl588 is not an owned
artifact and must not be synthesized during extraction.

| WL | Worklog | Legacy script | Legacy test | Result status | Owned semantic role |
| --- | --- | --- | --- | --- | --- |
| wl586 | docs/work-logs/586-route-selection.md | scripts/theory/aa_bb/wl586_route_selection.py | tests/theory/aa_bb/test_wl586_route_selection.py | No repository result; CLI requires --out and tests use a temporary file | Cross-family generic squareclass audit and pure-v route-death decision |
| wl587 | docs/work-logs/587-pure-u7-d0-relative-2-descent.md | scripts/theory/aa_bb/wl587_pure_u7_d0_relative_2_descent.py | tests/theory/aa_bb/test_wl587_pure_u7_d0_relative_2_descent.py | Default ignored output path exists in the CLI contract but the file is absent from the current worktree | Protected pure-u_7 D0 certificate |
| wl589 | docs/work-logs/589-mixed-d0-relative-2-descent.md | scripts/theory/aa_bb/wl589_mixed_d0_relative_2_descent.py | tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py | Default ignored output path exists in the CLI contract but the file is absent from the current worktree | Protected mixed D0 certificate |
| wl590 | docs/work-logs/590-p5-factor-twist-local-image-comparison.md | scripts/theory/aa_bb/wl590_p5_factor_twist_local_image_comparison.py | tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py | No repository result; --out is optional and current validation used a temporary path | Protected shared p=5 local-image certificate |
| wl591 | docs/work-logs/591-mixed-p7-factor-twist-local-image.md | scripts/theory/aa_bb/wl591_mixed_p7_factor_twist_local_image.py | tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py | No repository result; --out is optional and current validation used a temporary path | Protected mixed p=7 local-image certificate |
| wl592 | docs/work-logs/592-mixed-p17-factor-twist-local-image.md | scripts/theory/aa_bb/wl592_mixed_p17_factor_twist_local_image.py | tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py | No repository result; --out is optional and current validation used a temporary path | Protected mixed p=17 local-image certificate |
| wl593 | docs/work-logs/593-factor-twist-generalization-route-death.md | scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py | tests/theory/aa_bb/test_wl593_factor_twist_generalization_route_death.py | No repository result; CLI writes only when --out is supplied | Fixed-representative factor-twist generalization route death |

The two D0 JSON paths are optional ignored/generated parity-oracle locations,
not current files and not tracked assets. No result file is a D4 runtime input.
There is no current result asset for wl586-wl593 to preserve or infer.

## Current Dependency Audit

The old execution edges are not the target runtime graph:

~~~text
old wl586 -> legacy wl585 builder
          -> wl505 result payload
          -> wl522 result payload
          -> wl527 result payload

old wl593 -> wl587 builder
          -> wl589 builder
          -> wl590 builder
          -> wl591 builder
          -> wl592 builder
~~~

wl586_route_selection.py imports the legacy wl585 module and accepts three
JSON-shaped payloads. It checks old readiness summaries, selects three
representatives from wl522 and wl527, computes two generic witnesses from
wl505, and performs a read-only quartic review. Its tests use reduced synthetic
wl505, wl522, and wl527 fixtures, test representative drift, test a non-ready
wl585, and make one temporary CLI output.

wl593_factor_twist_generalization_route_death.py imports all five protected
modules and calls their zero-argument builders. It compares the two D0
payloads, the p=5 image disagreement, the mixed p=7 chain, the mixed p=17
target exclusion, and retained boundary checks. It does not import A0, A2,
C3, or any result file.

The protected modules also have real code-level dependencies that D4 must
preserve. wl590 imports the wl587 and wl589 modules for their frozen source
and factor symbols; wl591 and wl592 import the wl589 module for the frozen
mixed formulas and identities. Those imports are not permission to merge the
modules. They are part of the protected kernel contract.

## Canonical Dependency Graph

~~~text
tracked A0: a0-ledger, a0-witnesses, a0-taxonomy, a0-inventory
       |
       +--> A1 certificates --> A2 evidence
       |                         |        |
       |                         |        +--> D4 wl586 projection
       |                         |
       |                         +--> representative selection and scope
       |
canonical C2 --> canonical C3 --> C3 wl585 projection --+
                                                         |
protected D0u: wl587 -----------------------------------+
protected D0m: wl589 -----------------------------------+--> D4 wl593 projection
protected D5:  wl590 -----------------------------------+
protected D7:  wl591 -----------------------------------+
protected D17: wl592 ----------------------------------+
~~~

The implementation order of the protected local chain remains:

~~~text
D0u and D0m -> D5 -> D7 -> D17 -> D4
~~~

The existing zero-argument local builders do not receive predecessor payloads:
wl590 rebuilds wl587 and wl589, while wl591 and wl592 each rebuild wl589. A
naive D4 composition that directly calls all five zero-argument entrypoints
would therefore evaluate wl587 twice and wl589 four times. That is not an
acceptable canonical graph for this consolidation: it preserves recursive
proof-prefix execution instead of removing it.

The future implementation must retain the old zero-argument behavior while
adding dependency-aware sibling entrypoints:

~~~python
build_wl590_from_d0(pure_payload, mixed_payload) -> dict[str, Any]
build_wl591_from_mixed_d0(mixed_payload) -> dict[str, Any]
build_wl592_from_mixed_d0(mixed_payload) -> dict[str, Any]
~~~

The old builders become compatibility wrappers around those entrypoints and
their existing D0 builders. D4 calls D0u and D0m exactly once, then calls each
dependency-aware local kernel exactly once in D5, D7, D17 order, validates
every returned certificate, and enforces predecessor/survivor relationships
at the composition boundary. Adapter output must be recursively identical to
the old zero-argument output. D4 must not call legacy wl593, because that would
execute every protected builder again.

The canonical D4 runtime consumes A0Bundle, A2Evidence, and C3Evidence
directly. A0Bundle.to_wl522_view(), A0Bundle.to_wl527_view(), and
A0Bundle.to_wl586_inputs() are compatibility views for old/new parity tests
only; they are not the D4 runtime API.

## Proposed D4 Shape

The future implementation adds these D4-owned files:

~~~text
scripts/theory/aa_bb/d4_factor_twist.py
tests/theory/aa_bb/test_d4_factor_twist.py
~~~

It may also make only the dependency-injection edits described above in the
three protected local modules and their existing focused tests. No D0 module,
formula, representative, branch table, output field, zero-argument signature,
CLI behavior, or worklog may change. Before those stable modules are touched,
the Controller must record the required Chinese stable-module protection
judgment: protected behavior, why the adapter is necessary, exact files and
scope, explicit non-goals, and parity/regression commands.

The proposed public API is:

~~~python
D4_STAGES = ("wl586", "wl593")

@dataclass(frozen=True)
class D4Evidence:
    stages: dict[str, dict[str, Any]]

def build_d4(*, a0, a2, c3, kernels=None) -> D4Evidence
def project_stage(evidence, work_log) -> dict[str, Any]
def semantic_projection(payload, work_log) -> dict[str, Any]
~~~

kernels is an in-process test injection point, not a result loader. In the
production path, D4 invokes each D0 builder once and passes those validated
payloads to the dependency-aware D5/D7/D17 entrypoints once each. A supplied
entry is accepted only after the same structural checks as a production
result; an arbitrary ready=True fixture is insufficient.

The in-memory D4Evidence may retain the five protected payloads for composition
checks, but the serialized D4 result must contain only the two stage
projections and small derived dependency metadata. It must not copy the full
D0/local certificate payloads into a sixth aggregate proof object.

The CLI should assemble canonical inputs through existing APIs, then invoke
build_d4 once:

~~~text
load_a0(data_dir)
load_certificates(data_dir / "a1-certificates.v1.json")
build_a1(a0, certificates)
load_boundary_spec(data_dir / "a2-boundary-spec.v1.json")
build_a2(a0, a1, boundary_spec)
build_c3()
build_d4(a0=a0, a2=a2, c3=c3)
~~~

The strict CLI should print one aggregate result, such as stage_count=2 and
status=ok|issues, and exit nonzero if either stage or any protected kernel is
not structurally ready.

## A0, A2, And C3 Projection

### A0 requirements

D4 must validate the canonical A0 bundle before selecting any row. The exact
input facts are:

~~~text
ledger rows      = 43
witness rows     = 8
taxonomy rows    = 22
inventory rows   = 15
~~~

For the old wl586 readiness projection, D4 derives the equivalent wl505 view
from the eight canonical witnesses and requires:

~~~text
status = ok
ready = true (derived, never trusted)
work_log = wl505
wl491_filter_applied_count = 8
~~~

The two generic rows are selected by exact candidate ID. D4 must recompute root
values from p and sqrt_q, use canonical cover and elliptic points, and preserve
the witness equations. It must not use a synthetic fixture in the runtime path.

### A2 requirements

D4 uses A2Evidence.taxonomy, A2Evidence.inventory, and canonical project_a2
projections for wl522 and wl527. It requires the same old readiness facts,
derived from validated data:

~~~text
wl522 taxonomy summary:
  globally soluble but not AA+BB cover families = 15
  globally soluble but not AA+BB entries        = 29

wl527 inventory rows = 15
ready for uniform squareclass attempt           = false
missing data class = uniform_function_field_model_maps_and_squareclass_certificate
~~~

For each selected representative, D4 must require taxonomy classification
globally_soluble_but_not_aa_bb_admissible, failure mode
common_source_aa_bb_admissibility_failure, entry count 2, source sides
["AA", "BB"], matching L, T, and exact d_vector. It must preserve the
inventory distinction between an explicit model and a label-only family.

### C3 wl585 requirements

The pure-v representative is the only representative with a post-wl527
explicit prototype. D4 must take this fact from the canonical C3 wl585 stage,
not import the legacy wl585 script. Required semantic checks are:

~~~text
work_log = wl585
status = ok
cover_certificate.cover_degree = 16
cover_certificate.genus = 17
proof_status.combined_rational_elliptic_quotient_proved_here = true
proof_status.restricted_combined_elliptic_image_solved_here = false
proof_status.uniform_full_wl535_obstruction_proved_here = false
advance_to_m3 = false
~~~

The C3 stage remains a fixed-ell genus-seventeen and quotient certificate. It
does not provide a restricted-image solution or a wl535 exclusion.

## Fixed Representatives And Witnesses

### Three wl586 representatives

The representative comparison must preserve all three rows, including the
pure-v context row that has no D0/local-image kernel in this slice.

| Role | Cover family | Support | L | T | d vector | Post-wl527 model |
| --- | --- | --- | ---: | ---: | --- | --- |
| pure-v base | support=v_5\|L=1\|T=5\|d=(5,1,5) | v_5 | 1 | 5 | (5,5,1) in named fields d_minus_p,d_neg_2sqrt_q,d_pos_2sqrt_q | Yes: inherited wl528-wl585 prototype and exact lifts |
| pure-u | support=u_7\|L=7\|T=9\|d=(7,7,1) | u_7 | 7 | 9 | (7,1,7) in named fields | No: wl527 has labels and L,T,d only |
| mixed | support=u_3+v_5+w_17\|L=3\|T=10\|d=(15,51,85) | u_3+v_5+w_17 | 3 | 10 | (15,85,51) in named fields | No: wl527 has labels and L,T,d only |

The tuple notation in the table follows the named
(d_minus_p,d_neg_2sqrt_q,d_pos_2sqrt_q) order. The human-facing cover-family
labels use the historical (d_minus_p,d_pos_2sqrt_q,d_neg_2sqrt_q) order. D4
must preserve the named fields and must not silently reorder them.

### Two generic nonsquare witnesses

The generic cross-family function is exactly:

~~~text
t = Y/(2*(X+p))
N = (A+B+t)/2
M = A+B-N
P_op = (N^2+B^2)*(M^2+B^2)
~~~

The two and only two generic certificates in wl586 are:

| Candidate | Family | Input point | t | N | M | P_op | Required checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AA_A7_B2_u_7_m_tail_shell7_candidate | pure u_7 | X=1562, Y=61824, (u0,u+,u-)=(16,12,46), p=230, d=(7,7,1) | 69/4 | 105/8 | -33/8 | 15172945/4096 | positive, not a rational square, nonzero denominator, geometrically integral biquadratic cover, nonzero Jacobian minor |
| AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate | mixed | X=1088, Y=32640, (u0,u+,u-)=(8,4,4), p=-128, d=(15,51,85) | 17 | 27/2 | -7/2 | 226625/16 | positive, not a rational square, nonzero denominator, geometrically integral biquadratic cover, nonzero Jacobian minor |

For both rows D4 must recompute:

~~~text
d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q is a square
X-e_minus = d_minus_p*u_minus_p^2
X-e_pos   = d_pos_2sqrt_q*u_pos_2sqrt_q^2
X-e_neg   = d_neg_2sqrt_q*u_neg_2sqrt_q^2
Y = sqrt(d_product)*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q
2*(X+p) != 0
~~~

The conclusion is only that the same P_op definition is nonsquare in the two
displayed function fields. It is not a proof that all rational specializations
are nonsquare. A square specialization creates a new double cover R^2=P_op,
which is why the uniform exclusion flag remains false.

The pure-v row is representative and inherited prototype context, not a third
generic witness. D4 must not manufacture a new pure-v witness or family model.

### Quartic refinement stop

The wl586 read-only refinement is part of the semantic projection and must not
be silently dropped. Its exact object is the parameter-prime quartic character
of B/(2*r):

~~~text
positive norm formula:
  theta_ell = Legendre(a, ell)
negative norm formula:
  theta_ell = chi4_ell(-1)*Legendre(b, ell)
sign comparison:
  Legendre(a,ell)*Legendre(b,ell) = Legendre(2,ell) = chi4_ell(-1)
determined values:
  ell = 1 mod 8:                         +1
  ell = 5 mod 8 and canonical r = 1 mod 8: +1
  ell = 5 mod 8 and canonical r = 7 mod 8: -1
dependency set = [ell_mod_8, canonical_r_mod_8]
verdict = automatic_collapse_to_existing_gaussian_data
independent_invariant = false
wl588_permitted_by_stop_rule = false
~~~

This review does not create wl588 and does not add a parameterized character
or another family.

### wl586 tool-feasibility rows

The exact four feasibility rows must remain visible:

| Tool | Families with inputs | Cross-family ready | Independent on pure-v | Verdict |
| --- | --- | --- | --- | --- |
| parameter-prime Gaussian characters | pure-v base only | false | false | route_dead |
| restricted elliptic image | pure-v base only | false | false | route_dead_as_current_quotient |
| opposite-side function-field divisor parity | pure-v, pure-u, mixed | true | true | generic_nonsquare_only_not_uniform_point_obstruction |
| point-level common-source nonsquare | pure-v, pure-u, mixed | true | false | finite_signal_only |

The reasons are semantic obligations: existing Gaussian data makes the first
character automatic; the restricted image restores original lifts; a
nonsquare function can specialize to a square; and pointwise failures do not
define a uniform family invariant.

### wl586 exact route decision

The route fields must remain:

~~~text
reenter_wl535_now = false
pure_v_ell_equivalent_model_route = route_dead
pure_v_ell_parameter_character_route = route_dead
representative_only_divisor_parity_route = route_dead_as_uniform_exclusion
wl588_created = false
cross_family_uniform_invariant_proved_here = false
cross_family_generic_invariant_proved_here = true
selected_next_route = none_without_parameterized_family_level_input
next_route_success_gate = not_entered
supporting_models_are_not_progress_by_themselves = true
accepted_outcome = route_death_certificate
~~~

The generic-versus-uniform boundary must remain:

~~~text
same_function_definition_on_two_cover_families = true
function_field_nonsquare_on_two_cover_families = true
all_rational_specializations_nonsquare_proved = false
uniform_aa_bb_exclusion_invariant_proved = false
reason = a nonsquare function-field element may specialize to a square;
         each square-specialization locus is a new double cover
~~~

The wl586 certificate scope must retain these exact route-death values:

~~~text
kills_all_possible_future_invariants = false
kills_current_pure_v_equivalent_models = true
kills_characters_derived_only_from_existing_gaussian_factors = true
kills_unrestricted_fixed_ell_rank_tables = true
kills_generic_nonsquare_as_uniform_exclusion = true
proves_wl535 = false
finds_strict_counterexample = false
proves_complete_selmer_upper_bound = false
~~~

## Protected Kernel APIs And Content

The following zero-argument APIs are retained exactly. D4 may validate their
returned dictionaries and consume selected fields, but it must not change
their signatures or move their formula/evidence code into d4_factor_twist.py.
For D5/D7/D17, the dependency-aware sibling APIs defined above are added in
the same kernel modules and must return dictionaries recursively identical to
these compatibility builders.

| Kernel | Existing API | Required retained content |
| --- | --- | --- |
| D0u | build_wl587_pure_u7_d0_relative_2_descent() | Fixed Spec(Q) source, complete-d equations, quartic/source maps, degree/genus and divisor data, Picard versus factor-cover separation, Q(S,2) 256 candidates and real/Q_2 16 candidates, all rational exceptional branches, exact AA+BB lift, and unevaluated odd bad-fiber boundary |
| D0m | build_wl589_mixed_d0_relative_2_descent() | Fixed mixed Spec(Q) source, conic parameterization and tangent/infinity maps, quartic/divisor/Jacobian data, 256 Q(S,2) candidates and 16 real/Q_2 candidates, all D/A/B/W and factor-zero branches, both AA/BB orientations, and unevaluated odd bad-fiber boundary |
| D5 | build_wl590_p5_factor_twist_local_image_comparison() | Exact pure and mixed Q_5 images, all residue/valuation/pole/infinity/zero/factor-zero strata, Hensel inclusion, named mapping, fixed-cover R, and frozen AA+BB maps |
| D7 | build_wl591_mixed_p7_factor_twist_local_image() | Exact mixed Q_7 image, complete affine and infinity strata, D/A pole branches, zero and factor-zero/R branches, Hensel inclusion, named mapping, fixed-cover R, and exact AA+BB maps |
| D17 | build_wl592_mixed_p17_factor_twist_local_image() | Exact mixed Q_17 image, chart identity, integral and negative-valuation/infinity strata, empty D/A pole branches, factor-zero/R and zero-value branches, Hensel inclusion, named mapping, fixed-cover R, positivity, and exact AA+BB maps |

The protected D0 APIs return status, ready, work_log, source_cover,
divisors_and_branch_cover, local/factor-twist data, aa_bb_lift, verification,
and proof_boundary. The local APIs return exact local image fields, named
survivor mappings, proof certificates, verification maps, and proof boundaries.
D4 must require full structural verification maps and scope/proof-boundary
fields; it must never accept a cached ready=True in isolation.

D0 candidate generation is also protected input semantics:

~~~text
each D0 factor-twist set has 2^8 = 256 Q(S,2) classes
real and Q_2 filtering leaves exactly 16 candidates
no odd bad-prime local filter is applied by either D0 kernel
wl587 odd bad-prime support = [2,3,5,7,53,97,277]
wl589 odd bad-prime support = [2,3,5,7,17,29,37]
~~~

The D4 p=5 ledger is the first odd-prime filter and must not be mistaken for
a theorem about either full D0 candidate set.

## Local-Image Ledger

### Exact local quantifier

For each frozen representative j, selected prime p, and class
[d] in Q_p^*/Q_p^{*2}:

~~~text
I_(p,j) = { [d] : exists a Q_p point (c,a_plus,a_minus,R)
  on the already audited complete normalized factor-cover charts, with
  d in Q_p^*,
  F_plus(c)  = d*a_plus^2,
  F_minus(c) = d*a_minus^2,
  R          = d*a_plus*a_minus }
~~~

The charts include finite source points, denominator-pole charts, projective
infinity charts, factor-zero charts, and the R=0 boundary. At a pole, the
equalities mean the normalized valuation statement obtained from the frozen
cleared equations. A factor-zero branch permits the corresponding square root
to be zero. The real positivity interval and exact AA+BB source-product lift
remain global conditions and are not inserted into the p-adic quantifier.

### D5: p=5

The squareclass basis is ([1],[u],[5],[5u]).

| Frozen cover | Complete branches retained | Exact conclusion |
| --- | --- | --- |
| pure u_7 | eight smooth affine source rows; no r=0 source; no finite r^2+112=0 pole; no infinity point; pure factor-zero resultant has no root modulo 25; t=11 or 14 mod 25; factor valuation pairs (0,1) or (1,0) | I_(5,u)=empty; all 16 D0 pure representatives are deleted |
| mixed u_3+v_5+w_17 | six regular affine rows; singular r=5*x chart with eight lifted rows and the x=3 nonsquare branch; r=1+5*x empty; D=0 and A=0 pole branches empty; two infinity disks; t=8 or 17 mod 25; both factor-zero Hensel branches; explicit [5] inclusion at r=4, W=276 mod 625, t=67 mod 625 | I_(5,m)={[5]} |

The complete D5 named ledgers are:

~~~text
pure D0 candidates, all deleted:
1, 97, 105, 265, 1113, 1385, 5817, 10185,
14681, 25705, 107961, 134345, 564249, 1424057, 1541505, 149525985

mixed D0 candidates, p=5 survivors:
5, 3045, 66045, 91205

mixed D0 candidates deleted at p=5:
21, 29, 37, 85, 357, 493, 629, 3885, 5365, 22533,
51765, 383061
~~~

The p=5 images disagree. This is fixed-representative evidence, not a shared
local exclusion and not a parameterized coefficient lemma.

### D7: p=7 on the frozen mixed cover

The squareclass basis is ([1],[u],[7],[7u]). D7 must retain:

~~~text
complete affine source table: 10 rows
regular D-unit rows: 6 rows
D-pole rows: 4 rows; D has simple roots 2 and 5 mod 7
A=0: no Q_7 branch because its discriminant is -51 = 5 mod 7
projective infinity: exactly two disks, (v,t) mod 7 = (3,4),(4,3)
t=0, N=0, M=0 formal zero-value branches
F_plus=0 and F_minus=0: no Q_7 factor-zero branch
R=0: empty because it is contained in the factor-zero divisors
Hensel inclusion: r=1, W=2 mod 7, W=16 mod 49, t=4 mod 49
~~~

Every non-pole and pole stratum forces [d]=[1], and the inclusion disk proves
the reverse containment:

~~~text
I_(7,m) = {[1]}
5      -> [u]  -> delete
3045   -> [7]  -> delete
66045  -> [7u] -> delete
91205  -> [1]  -> survive
~~~

### D17: p=17 on the frozen mixed cover

The squareclass basis is ([1],[u],[17],[17u]). D17 must retain:

~~~text
integral chart: complete 16-row source table; D and A units
negative-valuation chart: s=1/(17*r), y=17*s^2*W
projective infinity: included as s=0; complete 16-row infinity table
D=0: no branch because r^2=5/17 has odd valuation
A=0: no branch because discriminant -51 has odd 17-adic valuation
factor-zero: roots have t residues {2,5,12,15}, outside t in 17*Z_17
R=0: empty on the frozen source
t=0, N=0, M=0 formal zero-value branches
Hensel inclusion: r=0, W=5, t=17, d=5 with class [u]
~~~

All source points have t in 17*Z_17, hence both nonzero normalized factors
have unit class [u]:

~~~text
I_(17,m) = {[u]}
91205 = 17*5365, 5365 = 10 mod 17, so [91205]=[17u]
[91205] not in I_(17,m)
~~~

This exhausts the mixed frozen ledger after D5 and D7. It does not compute a
pure-family p=7 or p=17 image.

### Fixed-cover and global lift maps

Every local kernel must retain the normalized factor map and the global
AA+BB boundary. The exact maps are:

~~~text
pure u_7:
  F_plus  = d*a_plus^2
  F_minus = d*a_minus^2
  R       = d*a_plus*a_minus
  R^2     = (N^2+4)*(M^2+4)
  AA+BB   = (N^2+49)*(M^2+49) = (Z/4)^2
  positivity = -9 < t < 9
  source leg = 7, opposite leg = 2

mixed u_3+v_5+w_17:
  F_plus  = d*a_plus^2
  F_minus = d*a_minus^2
  R       = d*a_plus*a_minus
  R^2     = (N^2+49)*(M^2+49)
  AA+BB   = (N^2+9)*(M^2+9) = (Z/4)^2
  positivity = -10 < t < 10
  source leg = 3, opposite leg = 7
~~~

For the cleared charts, the normalized square roots are
a_plus=s_plus/(2*T_denominator) and
a_minus=s_minus/(2*T_denominator), with
T_denominator=4*r*(r^2+112) on the pure cover and
T_denominator=(17*r^2-5)*(17*r^2-17*r+5) on the mixed cover. No individual
factor-square condition is added to the AA+BB lift. D4 must preserve the
distinction between the fixed-cover coordinate R and any cleared polynomial
coordinate.

## wl593 Route-Death Projection

D4 must reproduce the wl593 comparison from the five in-memory protected
payloads. The fixed D0 snapshots preserve:

~~~text
pure u_7:
  base = Spec(Q)
  parameters = L=7, T=9, p=230, q=76729, sqrt_q=277, d=(7,7,1)
  source = W^2=7*r^4+2864*r^2+87808
  t = W*(r^2-112)/(4*r*(r^2+112))
  F_plus=(t^2+18*t+97)/4
  F_minus=(t^2-18*t+97)/4
  bad primes = [2,3,5,7,53,97,277]

mixed u_3+v_5+w_17:
  base = Spec(Q)
  parameters = L=3, T=10, p=-128, q=18496, sqrt_q=136, d=(15,51,85)
  source = W^2=289*r^4-408*r^3+274*r^2-120*r+25
  t = -17*(17*r^2-20*r+5)*W/((17*r^2-5)*(17*r^2-17*r+5))
  F_plus=(t^2+20*t+296)/4
  F_minus=(t^2-20*t+296)/4
  bad primes = [2,3,5,7,17,29,37]
~~~

D4 must require all four input-difference checks to remain true:

~~~text
coefficient_data_differ = true
source_data_differ = true
factor_data_differ = true
bad_prime_supports_differ = true
~~~

The p=5 comparison must remain I_(5,u)=empty, I_(5,m)={[5]}, with
images_disagree=true. The mixed chain must remain exactly:

~~~text
p=5 survivors = [5, 3045, 66045, 91205]
p=7 image    = [[1]], survivors = [91205]
p=17 image   = [[u]], target = 91205, target class = [17u], in image = false
~~~

The local-image object layer remains selected-prime and selected-cover only:

~~~text
wl590: p=5 images for frozen wl587 and wl589 only
wl591: frozen wl589 mixed cover at p=7 only
wl592: frozen wl589 mixed cover at p=17 only
~~~

The later p=7 and p=17 rows are not a family quantifier and are not a pure
cover calculation.

## Exact Semantic Projections

D4_STAGES is exactly (wl586, wl593). project_stage must reject unknown,
missing, or mislabeled stages. semantic_projection must use explicit
allowlists, compare recursively, preserve formula strings, signs, witness
coordinates, list order, branch labels, and proof flags, and never normalize
them into a weaker summary.

### wl586 projection

The semantic allowlist is every old top-level field except execution metadata
status, ready, and violations:

~~~text
work_log
input_work_logs
object_layer
representative_selection_basis
representative_cover_family_comparison
cross_family_generic_squareclass_certificates
generic_vs_uniform_boundary
quartic_refinement_read_only_review
invariant_tool_feasibility
route_decision
accepted_outcome
certificate_scope
shell11_executed_here
new_supports_computed_here
new_c_d_solubility_tested_here
finite_search_used_as_progress
equivalent_model_created_here
quotient_created_here
fixed_ell_rank_table_created_here
advance_to_m3
~~~

The projection must preserve the exact three representative rows, two generic
witness rows, all four tool-feasibility rows, quartic dependency set and
values, generic-versus-uniform distinction, route decision, and all false
certificate-scope flags.

### wl593 projection

The semantic allowlist is:

~~~text
work_log
accepted_outcome
input_work_logs
object_layer
local_image_quantifier
fixed_input_comparison
p5_comparison
mixed_instance_chain
frozen_boundaries
conclusion
proof_boundary
verification.checks
~~~

verification.violations and verification.strict_certificate are derived
execution/prose fields and are excluded from semantic equality. Every actual
check value, no-edit/no-other-prime/no-D2 value nested in the protected
certificates, fixed-cover equation, positivity interval, AA+BB source product,
and proof-boundary value remains semantic. This keeps branch obligations
machine-checkable without making prose a proof input.

The old/new parity test must compare both projections independently. It must
not compare only accepted_outcome, ready, or a single aggregate boolean.

## No-Claim And Route Boundaries

The following are protected false values in the D4 stage and its input
contract:

~~~text
wl586:
  reenter_wl535_now = false
  cross_family_uniform_invariant_proved_here = false
  all_rational_specializations_nonsquare_proved = false
  uniform_aa_bb_exclusion_invariant_proved_here = false
  proves_wl535 = false
  finds_strict_counterexample = false
  proves_complete_selmer_upper_bound = false
  shell11_executed_here = false
  new_supports_computed_here = false
  new_c_d_solubility_tested_here = false
  finite_search_used_as_progress = false
  equivalent_model_created_here = false
  quotient_created_here = false
  fixed_ell_rank_table_created_here = false
  advance_to_m3 = false

wl593:
  all_relative_2_descent_impossible = false
  family_level_local_image_theorem = false
  new_parameterized_family_added = false
  new_prime_or_local_row_added = false
  new_equivalent_model_or_quotient_added = false
  rank_computation = false
  rational_point_search = false
  D2 = false
  D5 = false
  Selmer_claim = false
~~~

The protected kernels retain their own boundaries and D4 must assert them:

~~~text
wl587: rational_point_classification=false, family_exclusion=false,
       theorem_level_selmer_claim=false, advance_to_D1=false
wl589: odd_bad_prime_filtering=false, rational_point_classification=false,
       family_exclusion=false, theorem_level_selmer_claim=false,
       advance_to_D1=false
wl590: no other prime, no D1/D2, no rational search or family claim
wl591: rational_point_classification=false, rank_or_selmer_claim=false,
       family_exclusion=false, advance_to_D2=false
wl592: rational_point_classification=false, rank_or_selmer_claim=false,
       family_exclusion=false, advance_to_D2=false,
       positivity_retained_as_global_condition=true
~~~

The positive statements are also scoped: wl586 proves a generic nonsquare
function-field class on two fixed covers, while wl593 proves only that the
current fixed-representative factor-twist mechanism cannot be promoted from
these inputs. The exact reopening requirement is new parameterized
family-level coefficient and local-image input. This is not a statement that
all relative 2-descent is impossible.

## Fail-Closed Contract

D4 must return status=issues, ready=false, and no accepted route decision when
any of the following occurs:

~~~text
missing or malformed A0/A2/C3 canonical object
wrong A0 cardinality, candidate ID, support, L/T/d, coordinate, or equation
wrong A2 taxonomy/inventory count or missing-data class
missing or non-ready canonical C3 wl585 stage
wrong C3 genus/degree/restricted-image/no-claim field
missing, duplicated, extra, or mislabeled protected kernel
protected kernel status, work_log, verification, scope, or proof boundary drift
wrong D5 image or named ledger
wrong D7 survivor chain or class labels
wrong D17 target class or inclusion decision
changed local branch coverage, fixed-cover R identity, positivity, or AA+BB map
changed old semantic field, formula, witness, list order, or route flag
~~~

On failure, D4 must not substitute an empty image, cached result, reduced
stage, or synthetic representative. A failed predecessor must prevent later
chain acceptance. --strict must exit nonzero. No ignored results/ path may be
searched, globbed, or used as fallback.

## Runtime And Result Rules

The D4 runtime may read only tracked canonical data under
data/theory/aa_bb/wl500 and code-level canonical builders. It may import the
five protected D modules, A0/A1/A2 loaders/builders, and C3. It must not:

~~~text
load results/ JSON
import legacy wl586 or wl593 builders
import a legacy wl585 builder
invoke a per-WL subprocess
glob or rglob legacy paths
use a cached ready/status/violations value as proof
read wl594/wl595 or any downstream result
~~~

The old wl586 result shape can be recreated in memory from A0/A2/C3 for parity.
Existing ignored D0 results can be read only by a separate explicit parity
audit, never by D4 runtime. Protected builder outputs are recomputed in
process and are not result inputs.

The D4 CLI should write one deterministic temporary or caller-selected output
when --out is supplied. It should not default to a repository results/ path.
Serialization must be stable and the strict command must have one subprocess
smoke test, not one subprocess per stage or protected kernel.

## Focused Validation Design

The future D4 test file should cover these obligations without duplicating the
full protected-kernel test suites:

1. Exact D4_STAGES order, stage allowlists, and deterministic serialization.
2. One-call orchestration of D0u, D0m, dependency-aware D5, D7, and D17 in
   required order, with call counters proving that no D0 certificate is
   rebuilt through a nested zero-argument wrapper.
3. Exact recursive equality between each dependency-aware local builder and
   its existing zero-argument compatibility builder; existing CLI output and
   public zero-argument behavior remain unchanged.
4. Direct A0/A2/C3 input acceptance and exact three-representative selection.
5. Both generic witness values, equation checks, Jacobian/cover checks, and
   nonsquare values.
6. Old/new wl586 semantic projection parity using the legacy builder only as a
   test oracle and canonical A0 compatibility views only in that test.
7. Old/new wl593 semantic projection parity against the legacy route-death
   builder, with protected outputs otherwise checked through their own APIs.
8. Exact D5 images, all p=5 survivor/deletion lists, and both fixed-cover maps.
9. Exact D7 image, four Q7 classes, survivor/deletion mapping, and branch map.
10. Exact D17 image, 91205 -> [17u], target exclusion, and branch map.
11. All fixed-cover R identities, positivity intervals, and exact AA+BB source
    products remain present without individual factor-square conditions.
12. A0 representative mutation, A2 inventory mutation, C3 wl585 proof-flag
    mutation, protected-kernel mutation, missing-kernel, and wrong-order
    failures all fail closed.
13. A static runtime scan rejects results/, legacy wl586/wl593 imports,
    subprocess, glob, rglob, wl594, wl595, and any new route into D2, a second
    D5 prime/local row, or M3. Literal `D2` and `D5` keys are allowed only in
    the exact inherited false proof-boundary projection, and the required
    protected D5 kernel import remains allowed.
14. One strict CLI subprocess writes a deterministic two-stage payload and
    exits nonzero on malformed canonical input.

The existing focused tests remain the protected kernel tests and are not
replaced by the aggregator:

~~~bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/theory/aa_bb/test_wl587_pure_u7_d0_relative_2_descent.py \
  tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py \
  tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py \
  tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py \
  tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py \
  tests/theory/aa_bb/test_d4_factor_twist.py
~~~

Targeted implementation checks should additionally run Ruff, format checking,
py_compile, deterministic temporary CLI output, and git diff --check. This
design task itself does not authorize running the full suite.

## Reference Scans

The implementation and cutover work must use explicit path scans, not inferred
filename matches. Before cutover, record all current references with:

~~~bash
rg -n -uu --glob '!**/__pycache__/**' \
  'wl586|wl593|wl586_route_selection|wl593_factor_twist_generalization_route_death' \
  docs scripts tests data
~~~

Also scan the protected dependency boundary:

~~~bash
rg -n -uu --glob '!**/__pycache__/**' \
  'wl587|wl589|wl590|wl591|wl592|D0u|D0m|D5|D7|D17' \
  scripts/theory/aa_bb tests/theory/aa_bb docs/codex/tasks/wl500-series-consolidation
~~~

After a non-destructive cutover, direct runtime consumers of the old scripts
must be zero except for explicit legacy parity/deletion tests and provenance
records. Update A0 manifest consumer paths, consolidation_inputs.py,
README/control references, and direct test imports before deletion. Narrative
references in route-status docs may remain when identifying historical
provenance, but must not point a runtime loader at an old result.

The scan must additionally confirm that the new D4 module has no results/
literal, no legacy audit_closure_ import, no importlib fallback, no per-stage
subprocess, and no wl594 dependency. A reference to protected module names is
required; a reference to wl593 as a legacy builder is not.

## Separate Deletion Gate

Deletion is a later Controller decision and is not part of D4 implementation.
The gate must remain closed until all conditions below are independently met:

1. D4 strict readiness and focused tests pass, including exact wl586 and wl593
   semantic parity.
2. All five protected kernel tests pass unchanged, with no protected formula,
   representative, local row, result schema, or public builder signature edit.
3. Canonical A0/A2/C3 inputs are loaded without ignored-result fallback, and
   the manifest records the new D4 consumer/projection paths.
4. Explicit reference scans show no unreviewed runtime import, path, test,
   README, or manifest consumer still requiring the old wl586/wl593 triplet.
5. Old worklogs, scripts, and tests have documented provenance mapping to the
   two D4 projections and five retained kernels.
6. Separate Controller approval authorizes removal. The first D4 replacement
   change must not delete an old artifact in the same change.
7. Deletion is limited to superseded wl586 and wl593 worklog/script/test
   assets. The protected wl587, wl589, wl590, wl591, and wl592 kernels, tests,
   optional ignored D0 output locations, and all mathematical worklogs remain.
8. A post-deletion reverse scan, git diff --check, targeted tests, and final
   full-suite/performance gate pass. Missing or ambiguous dependency reopens
   the gate rather than deleting optimistically.

## Final Design Decision

D4 is a two-stage route-level orchestrator, not a sixth merged D kernel. It
replaces wl586 and wl593, consumes direct tracked A0/A2/C3 projections, and
computes D0u, D0m, D5, D7, and D17 exactly once through dependency-aware
kernel entrypoints. It preserves exact generic witnesses, fixed
representatives, local charts, images, survivor ledgers, quantifiers,
route-death statements, and no-claim flags, and fails closed on every input or
boundary drift. The existing zero-argument builders remain compatibility APIs;
wl587, wl589, wl590, wl591, and wl592 remain separate protected kernels. The
destructive deletion gate is closed.

Changed file for this design task: this file only.
