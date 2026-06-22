"""Rational fixed-ratio ``A / B = lambda`` identities.

This module is the proof-side analogue of :mod:`fixed_ratio_exact`.  It does
not generate integer candidates.  Instead it records exact ``Fraction``-level
identities that still make sense after replacing an integer ratio ``k`` by an
arbitrary positive rational ratio ``lambda``.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import comb, isqrt
from math import gcd as _gcd

from sympy import factorint

REL_SUM_AB = "sum=A+B"      # r + s = λ + 1
REL_SUM_DIFF = "sum=|A-B|"  # r + s = |λ - 1|
REL_DIFF_AB = "diff=A+B"    # |r - s| = λ + 1
REL_DIFF_DIFF = "diff=|A-B|" # |r - s| = |λ - 1|


@dataclass(frozen=True, order=True)
class PythagoreanLegParam:
    """Euclid parameters for one rational Pythagorean leg ratio.

    ``orientation="odd"`` returns ``(m²-n²)/(2mn)``.
    ``orientation="even"`` returns ``(2mn)/(m²-n²)``.
    """

    m: int
    n: int
    orientation: str = "odd"

    def ratio(self) -> Fraction:
        numerator, denominator = self.leg_terms()
        return Fraction(numerator, denominator)

    def leg_terms(self) -> tuple[int, int]:
        """Return the unreduced numerator/denominator leg terms."""
        if self.m <= self.n or self.n <= 0:
            raise ValueError("Euclid parameters must satisfy m > n > 0")
        odd_leg = self.m * self.m - self.n * self.n
        even_leg = 2 * self.m * self.n
        if self.orientation == "odd":
            return odd_leg, even_leg
        if self.orientation == "even":
            return even_leg, odd_leg
        raise ValueError("orientation must be 'odd' or 'even'")


@dataclass(frozen=True, order=True)
class RationalRatioHit:
    """A ratio-level full-plane closure hit for rational ``A/B``."""

    r1: Fraction
    r2: Fraction
    relation: str
    centerline: bool


@dataclass(frozen=True, order=True)
class RationalRatioHitProductDiagnostic:
    """Product-side diagnostic for a ratio-level full-plane closure hit."""

    lambda_ratio: Fraction
    r1: Fraction
    r2: Fraction
    relation: str
    product: Fraction
    product_equals_lambda: bool
    reciprocal_pair: bool
    true_member_pair: bool


@dataclass(frozen=True)
class ProductIdentityTerms:
    """Terms in the ``p = rs`` product identity for a closure target."""

    lambda_ratio: Fraction
    target: Fraction
    product: Fraction
    a_term: Fraction
    b_term: Fraction
    b_minus_lambda_sq_a: Fraction


@dataclass(frozen=True)
class ClosureProductSquareConditions:
    """Square checks after replacing a closure pair by ``T`` and ``p=rs``."""

    lambda_ratio: Fraction
    target: Fraction
    product: Fraction
    relation: str
    identity_terms: ProductIdentityTerms
    discriminant: Fraction
    discriminant_is_square: bool
    roots: tuple[Fraction, ...]
    centerline: bool
    reciprocal_pair: bool
    product_square_bucket: str
    product_terms_are_squares: bool
    member_square_flags: tuple[bool, bool, bool, bool] | tuple[()]
    member_squareclasses: tuple[int, int, int, int] | tuple[()]
    member_squareclass_pair: tuple[int, int] | tuple[()]
    member_squareclasses_pairwise_equal: bool
    product_square_explained_by_pairwise_squareclasses: bool
    member_squareclasses_all_equal: bool
    member_squareclasses_all_trivial: bool
    centerline_obstruction: str | None
    true_member_pair: bool


@dataclass(frozen=True)
class ClosureMemberProductSquareLedger:
    """Individual member-square values and their product-level shadow terms."""

    lambda_ratio: Fraction
    target: Fraction
    product: Fraction
    relation: str
    identity_terms: ProductIdentityTerms
    roots: tuple[Fraction, ...]
    unit_values: tuple[Fraction, Fraction] | tuple[()]
    lambda_values: tuple[Fraction, Fraction] | tuple[()]
    unit_product: Fraction | None
    lambda_product: Fraction | None
    unit_product_is_square: bool
    lambda_product_is_square: bool
    member_squareclasses: tuple[int, int, int, int] | tuple[()]
    member_squareclass_pair: tuple[int, int] | tuple[()]
    member_squareclasses_pairwise_equal: bool
    member_squareclasses_all_trivial: bool
    true_member_pair: bool


@dataclass(frozen=True, order=True)
class ClosureMemberPrimeValuationRow:
    """Valuations at one prime for member terms and product identity terms."""

    prime: int
    member_valuations: tuple[int, int, int, int]
    identity_valuations: tuple[int | None, int | None, int | None, int | None, int | None]
    all_member_valuations_even: bool
    product_valuations_even: bool


@dataclass(frozen=True)
class ClosureMemberPrimeValuationLedger:
    """Prime-valuation ledger for the member-product square bridge."""

    member_ledger: ClosureMemberProductSquareLedger
    primes: tuple[int, ...]
    three_mod_four_primes: tuple[int, ...]
    member_squareclass_primes: tuple[int, ...]
    three_mod_four_member_squareclass_primes: tuple[int, ...]
    rows: tuple[ClosureMemberPrimeValuationRow, ...]
    three_mod_four_rows: tuple[ClosureMemberPrimeValuationRow, ...]
    rows_by_prime: dict[int, ClosureMemberPrimeValuationRow]


@dataclass(frozen=True, order=True)
class ClosureIdentityThreeModFourBalanceRow:
    """Three-mod-four identity parity row for one prime."""

    prime: int
    identity_valuations: tuple[int | None, int | None, int | None, int | None, int | None]
    identity_difference_odd: bool
    lambda_squared_minus_one_odd: bool
    lambda_squared_minus_product_squared_odd: bool
    shared_odd_compensation: bool


@dataclass(frozen=True)
class ClosureIdentityThreeModFourBalanceLedger:
    """Parity balance summary for ``(lambda^2-1)(lambda^2-p^2)``."""

    valuation_ledger: ClosureMemberPrimeValuationLedger
    rows: tuple[ClosureIdentityThreeModFourBalanceRow, ...]
    rows_by_prime: dict[int, ClosureIdentityThreeModFourBalanceRow]
    odd_identity_difference_primes: tuple[int, ...]
    odd_lambda_squared_minus_product_squared_primes: tuple[int, ...]
    shared_odd_lambda_squared_minus_one_primes: tuple[int, ...]
    unshared_odd_lambda_squared_minus_product_squared_primes: tuple[int, ...]


@dataclass(frozen=True, order=True)
class ClosureIdentitySharedGcdRow:
    """Shared-gcd row for ``lambda^2-1`` and ``lambda^2-p^2``."""

    prime: int
    lambda_squared_minus_one_valuation: int | None
    lambda_squared_minus_product_squared_valuation: int | None
    p_squared_minus_one_valuation: int | None
    closure_discriminant_valuation: int | None
    shared_odd_compensation: bool
    p_squared_minus_one_carries_shared_factor: bool
    closure_discriminant_valuation_even: bool


@dataclass(frozen=True)
class ClosureIdentitySharedGcdLedger:
    """GCD bridge from shared odd compensation to ``p^2-1`` and discriminant."""

    balance_ledger: ClosureIdentityThreeModFourBalanceLedger
    closure_discriminant: Fraction
    rows: tuple[ClosureIdentitySharedGcdRow, ...]
    rows_by_prime: dict[int, ClosureIdentitySharedGcdRow]
    shared_odd_compensation_primes: tuple[int, ...]
    unshared_odd_lambda_squared_minus_product_squared_primes: tuple[int, ...]


@dataclass(frozen=True, order=True)
class SumAbSharedOddPrimeResidueCase:
    """One surviving shared-prime sign case for the ``sum=A+B`` branch."""

    prime: int
    lambda_residue: int
    product_residue: int
    target_residue: int
    discriminant_residue: int
    root_residues: tuple[tuple[int, int], ...]
    member_square_residue_pairs: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class SumAbSharedOddPrimeResidueSummary:
    """Finite-field residue summary for shared odd ``q == 3 mod 4`` primes."""

    prime: int
    prime_mod_8: int
    prime_mod_16: int
    cases: tuple[SumAbSharedOddPrimeResidueCase, ...]
    case_keys: tuple[tuple[int, int], ...]
    killed_case_keys: tuple[tuple[int, int], ...]
    all_cases_killed: bool


@dataclass(frozen=True)
class SumAbSharedOddPrimePowerLiftSummary:
    """Prime-power lifts for shared-prime residue shadows."""

    prime: int
    exponent: int
    modulus: int
    total_lifts: int
    pattern_counts: dict[tuple[int, int, int, int, tuple[int, int, int, int]], int]
    examples_by_pattern: dict[
        tuple[int, int, int, int, tuple[int, int, int, int]],
        tuple[int, int, int, int, tuple[int, int, int, int]],
    ]
    p_minus_lambda_shadow_count: int
    p_plus_lambda_shadow_count: int


@dataclass(frozen=True)
class ProductSquareBucketSummary:
    """Bucket counts for finite ``sum=A+B`` product-square diagnostics."""

    bucket_counts: dict[str, int]
    true_member_counts: dict[str, int]
    squareclass_pair_counts_by_bucket: dict[str, dict[tuple[int, int], int]]
    examples_by_bucket: dict[str, ClosureProductSquareConditions]


@dataclass(frozen=True)
class ResidualPrimeClassSummary:
    """Prime-class buckets for finite product-layer residuals."""

    total_residuals: int
    bucket_counts: dict[str, int]
    squareclass_prime_counts: dict[tuple[int, ...], int]
    three_mod_four_squareclass_prime_counts: dict[tuple[int, ...], int]
    examples_by_bucket: dict[str, ClosureProductSquareConditions]


@dataclass(frozen=True, order=True)
class SquareclassTwoSquareAbsorption:
    """Absorb a ``1 mod 4`` squareclass through a two-square factor."""

    ratio: Fraction
    squareclass: int
    two_square_decomposition: tuple[int, int]
    absorbed_plus: Fraction
    absorbed_minus: Fraction
    absorbed_plus_value: Fraction
    absorbed_minus_value: Fraction
    absorbed_plus_is_member: bool
    absorbed_minus_is_member: bool


@dataclass(frozen=True, order=True)
class ResidualGaussianAbsorptionLedger:
    """Pair-level Gaussian absorption for a product-layer residual."""

    condition: ClosureProductSquareConditions
    squareclass: int
    r_absorption: SquareclassTwoSquareAbsorption
    s_absorption: SquareclassTwoSquareAbsorption
    common_absorbed_members: tuple[Fraction, ...]
    centerline_shadow: bool


@dataclass(frozen=True)
class GaussianShadowSummary:
    """Bounded root-grid summary of Gaussian absorption shadows."""

    total_residuals: int
    centerline_shadow_count: int
    nonshadow_count: int
    common_absorbed_member_counts: dict[tuple[Fraction, ...], int]
    examples_by_bucket: dict[str, ClosureProductSquareConditions]


@dataclass(frozen=True)
class GaussianShadowObstructionSummary:
    """Bounded summary of unit-square obstructions for Gaussian shadows."""

    total_residuals: int
    centerline_shadow_count: int
    unit_obstructed_count: int
    nonobstructed_count: int
    obstruction_reason_counts: dict[str, int]
    examples_by_bucket: dict[str, ClosureProductSquareConditions]


@dataclass(frozen=True)
class InverseGaussianAbsorptionPair:
    """Pair generated by inverse Gaussian absorption from one absorbed slope."""

    absorbed: Fraction
    squareclass: int
    two_square_decomposition: tuple[int, int]
    r_branch: str
    s_branch: str
    r: Fraction
    s: Fraction
    lambda_ratio: Fraction
    product: Fraction
    condition: ClosureProductSquareConditions


@dataclass(frozen=True)
class InverseGaussianAbsorptionPairTerms:
    """Factor ledger for the inverse Gaussian ``plus,minus`` branch."""

    pair: InverseGaussianAbsorptionPair
    identity_terms: ProductIdentityTerms
    denominator_product: Fraction
    lambda_numerator: Fraction
    product_numerator: Fraction
    lambda_minus_product_left_factor: Fraction
    lambda_minus_product_right_factor: Fraction
    lambda_minus_product_factorized: Fraction
    lambda_plus_product_z_factor: Fraction
    lambda_plus_product_factorized: Fraction
    lambda_squared_minus_product_squared_factorized: Fraction
    lambda_squared_minus_one_extra_factor: Fraction
    lambda_squared_minus_one_factorized: Fraction
    r_unit_value_factorized: Fraction
    s_unit_value_factorized: Fraction
    r_lambda_value_factorized: Fraction
    s_lambda_value_factorized: Fraction
    a_term_factorized: Fraction
    b_term_minus_factor: Fraction
    b_term_plus_factor: Fraction
    b_term_factorized: Fraction
    b_minus_lambda_sq_a_factorized: Fraction
    member_factorization_holds: bool
    factorization_holds: bool


@dataclass(frozen=True)
class InverseGaussianCenterlineShadowObstruction:
    """Unit-square obstruction for a nontrivial Gaussian centerline shadow."""

    terms: InverseGaussianAbsorptionPairTerms
    absorbed_unit_value: Fraction
    absorbed_unit_value_is_square: bool
    squareclass_is_trivial: bool
    r_unit_squareclass: int
    s_unit_squareclass: int
    unit_squareclass_obstruction: bool
    true_member_pair_blocked: bool
    obstruction_reason: str | None


@dataclass(frozen=True)
class ResidualSquareclassEquations:
    """Squareclass equation ledger for one ``sum=A+B`` root pair."""

    lambda_ratio: Fraction
    r: Fraction
    s: Fraction
    unit_values: tuple[Fraction, Fraction]
    lambda_values: tuple[Fraction, Fraction]
    unit_squareclasses: tuple[int, int]
    lambda_squareclasses: tuple[int, int]
    unit_product_is_square: bool
    lambda_product_is_square: bool
    closes_sum_ab: bool
    reciprocal_pair: bool
    all_terms_are_squares: bool
    squareclasses_all_trivial: bool


@dataclass(frozen=True)
class SquareRectangleTerms:
    """Four square-candidate corners after a closure linear relation."""

    lambda_ratio: Fraction
    target: Fraction
    mover: Fraction
    x: Fraction
    y: Fraction
    z: Fraction
    w: Fraction


@dataclass(frozen=True, order=True)
class ReciprocalClosureRoot:
    """A same-orbit closure root and whether it is a true ``R_lambda`` point."""

    r: Fraction
    relation: str
    true_member: bool


@dataclass(frozen=True, order=True)
class ReciprocalClosureSquareclassRoot:
    """Squareclass diagnostics for one reciprocal closure root."""

    r: Fraction
    relation: str
    unit_value: Fraction
    lambda_value: Fraction
    unit_squareclass: int
    lambda_squareclass: int
    true_member: bool


@dataclass(frozen=True)
class ReciprocalClosureDiscriminantLedger:
    """Discriminant ledger for the reciprocal branches that have a quadratic."""

    lambda_ratio: Fraction
    lambda_numerator: int
    lambda_denominator: int
    relation: str
    target: Fraction
    discriminant: Fraction
    discriminant_numerator: int
    discriminant_denominator: int
    discriminant_is_square: bool
    discriminant_squareclass: int | None
    discriminant_integer_squareclass: int | None
    roots: tuple[ReciprocalClosureSquareclassRoot, ...]
    true_roots: tuple[Fraction, ...]
    branch_closed: bool


@dataclass(frozen=True)
class ReciprocalClosureObstruction:
    """One full-plane reciprocal closure branch and whether true roots remain."""

    relation: str
    roots: tuple[Fraction, ...]
    true_roots: tuple[Fraction, ...]
    branch_closed: bool


@dataclass(frozen=True)
class FullPlaneReciprocalObstruction:
    """Proof ledger for reciprocal/mirror branches across all full-plane relations."""

    lambda_ratio: Fraction
    by_relation: dict[str, ReciprocalClosureObstruction]
    all_branches_closed: bool


@dataclass(frozen=True, order=True)
class SumAbSlopePoint:
    """A sum=A+B candidate expressed by scaled Pythagorean slopes."""

    lambda_ratio: Fraction
    r1: Fraction
    r2: Fraction
    slope1: Fraction
    slope2: Fraction
    product: Fraction
    reciprocal_pair: bool
    true_member_pair: bool

    @property
    def closes_sum_ab(self) -> bool:
        return self.r1 + self.r2 == self.lambda_ratio + 1


@dataclass(frozen=True, order=True)
class SumAbTrueClosureRelation:
    """Classify one ``sum=A+B`` closure pair against true ``R_lambda`` membership."""

    lambda_ratio: Fraction
    r: Fraction
    s: Fraction
    closes_sum_ab: bool
    r_true_member: bool
    s_true_member: bool
    both_true_members: bool
    reciprocal_pair: bool
    centerline: bool
    branch: str


@dataclass(frozen=True, order=True)
class FullPlaneTrueClosureRelation:
    """Classify one full-plane closure relation against true ``R_lambda`` membership."""

    lambda_ratio: Fraction
    relation: str
    target: Fraction
    r: Fraction
    s: Fraction
    closure_value: Fraction
    closes_relation: bool
    closes_sum_ab: bool
    closes_sum_diff: bool
    closes_diff_ab: bool
    closes_diff_diff: bool
    r_true_member: bool
    s_true_member: bool
    both_true_members: bool
    reciprocal_pair: bool
    centerline: bool
    branch: str


@dataclass(frozen=True)
class FullPlaneClosureProductLedger:
    """Product ledger attached to one full-plane closure classification."""

    classification: FullPlaneTrueClosureRelation
    conditions: ClosureProductSquareConditions
    target: Fraction
    product: Fraction
    product_equals_lambda: bool
    danger_branch: bool


@dataclass(frozen=True)
class FullPlaneClosureProductSummary:
    """Finite diagnostic summary for full-plane closure product ledgers."""

    total_relations: int
    branch_counts: dict[str, int]
    relation_branch_counts: dict[tuple[str, str], int]
    product_bucket_counts: dict[tuple[str, str], int]
    danger_count: int


@dataclass(frozen=True, order=True)
class SumAbReciprocalObstruction:
    """Proof ledger showing why ``sum=A+B`` reciprocal roots are not true."""

    lambda_ratio: Fraction
    roots: tuple[Fraction, Fraction]
    forced_unit_root: Fraction
    unit_leg_value: Fraction
    unit_leg_is_square: bool
    true_roots: tuple[Fraction, ...]
    branch_closed: bool


@dataclass(frozen=True, order=True)
class SumAbCenterlineEquations:
    """Equation ledger for the ``sum=A+B`` centerline ``r=s=(lambda+1)/2``."""

    lambda_ratio: Fraction
    center: Fraction
    unit_value: Fraction
    lambda_value: Fraction
    unit_is_square: bool
    lambda_is_square: bool
    unit_squareclass: int
    lambda_squareclass: int
    true_member: bool
    obstruction: str | None


@dataclass(frozen=True, order=True)
class SumAbCenterlineUnitLegParam:
    """Centerline model after parameterizing ``center^2+1`` as a square."""

    parameter: Fraction
    center: Fraction
    lambda_ratio: Fraction
    unit_hypotenuse: Fraction
    equations: SumAbCenterlineEquations
    remaining_squareclass: int
    true_member: bool


@dataclass(frozen=True, order=True)
class SumAbCenterlineRemainingQuartic:
    """Remaining quartic square test after the centerline unit-leg parameter."""

    parameter: Fraction
    coefficients: tuple[int, int, int, int, int]
    quartic_value: Fraction
    denominator_square: Fraction
    lambda_value: Fraction
    squareclass: int
    is_square: bool


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticSelfSimilarity:
    """Self-similarity ledger for the centerline quartic square condition."""

    parameter: Fraction
    quartic_value: Fraction
    first_square_term: Fraction
    second_square_term: Fraction
    quadratic_coefficients: tuple[Fraction, Fraction, Fraction]
    quadratic_discriminant: Fraction
    quadratic_root_sum: Fraction | None
    quadratic_root_product: Fraction | None
    roots_are_negative_reciprocals: bool
    direct_positive_descent_warning: str
    has_rational_lift: bool
    lift_roots: tuple[Fraction, ...]


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticNegativeReciprocalQuotient:
    """Quotient ledger for the involution ``t -> -1/t`` on the quartic."""

    parameter: Fraction
    negative_reciprocal: Fraction
    quotient_variable: Fraction
    quartic_value: Fraction
    negative_reciprocal_quartic_value: Fraction
    negative_reciprocal_symmetry_holds: bool
    scaled_quartic_value: Fraction
    quotient_quadratic_value: Fraction
    reconstructing_quadratic_coefficients: tuple[Fraction, Fraction, Fraction]
    reconstruction_discriminant: Fraction
    reconstruction_discriminant_is_square: bool
    reconstruction_roots: tuple[Fraction, ...]


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuotientWParameterization:
    """Parameterize ``W^2=u^2+4`` in the centerline quotient model."""

    parameter: Fraction
    quotient_variable: Fraction
    w_value: Fraction
    w_condition_holds: bool
    remaining_quartic_value: Fraction
    z_square_value: Fraction
    z_square_value_is_square: bool
    negative_reciprocal_parameter: Fraction
    negative_reciprocal_remaining_quartic_value: Fraction
    negative_reciprocal_symmetry_holds: bool
    second_quotient_variable: Fraction
    second_quotient_quadratic_value: Fraction
    remaining_quartic_over_parameter_square: Fraction


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticPARIDiagnostics:
    """PARI elliptic-curve diagnostics for centerline quartic models."""

    available: bool
    centerline_model: tuple[int, int, int, int, int] | tuple[()]
    centerline_rank_bounds: tuple[int, int] | tuple[()]
    centerline_sha2_lower: int | None
    centerline_generators: tuple[tuple[str, str], ...]
    centerline_torsion_order: int | None
    centerline_small_points: tuple[tuple[int, int], ...]
    w_parameterized_model: tuple[int, int, int, int, int] | tuple[()]
    w_parameterized_rank_bounds: tuple[int, int] | tuple[()]
    w_parameterized_sha2_lower: int | None
    w_parameterized_generators: tuple[tuple[str, str], ...]
    w_parameterized_torsion_order: int | None
    w_parameterized_small_points: tuple[tuple[int, int], ...]
    proof_status: str
    notes: str


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticIntegerEquation:
    """Integer form of the centerline quartic for ``t=u/v``."""

    u: int
    v: int
    value: int
    denominator_square: int
    reduced_lambda_value: Fraction
    squareclass: int
    is_square: bool

    def residue(self, modulus: int) -> int:
        """Return the quartic value modulo ``modulus``."""
        if modulus <= 0:
            raise ValueError("modulus must be positive")
        return self.value % modulus

    def residue_is_square(self, modulus: int) -> bool:
        """Return whether the quartic residue is a square modulo ``modulus``."""
        residue = self.residue(modulus)
        residues = {value * value % modulus for value in range(modulus)}
        return residue in residues


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticResidueSummary:
    """Residue counts for the centerline quartic modulo one modulus."""

    modulus: int
    total_classes: int
    square_residue_classes: int
    non_square_residue_classes: int
    zero_residue_classes: int
    square_residues: tuple[int, ...]


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticPrimitiveResidueSummary:
    """Residue counts after primitive and nonzero-denominator filters."""

    modulus: int
    primitive_classes: int
    degenerate_denominator_classes: int
    total_classes: int
    square_residue_classes: int
    non_square_residue_classes: int
    zero_residue_classes: int
    square_residues: tuple[int, ...]


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticLiveResidueClass:
    """One primitive nondegenerate class where the quartic is a square residue."""

    u: int
    v: int
    residue: int


@dataclass(frozen=True, order=True)
class SumAbCenterlineQuarticCRTLiveResidueSummary:
    """CRT merge diagnostic for centerline quartic live residue classes."""

    left_modulus: int
    right_modulus: int
    combined_modulus: int
    left_square_primitive_classes: int
    right_square_primitive_classes: int
    left_live_classes: int
    right_live_classes: int
    left_degenerate_square_classes: int
    right_degenerate_square_classes: int
    live_live_pairs: int
    one_sided_degenerate_pairs: int
    both_degenerate_pairs: int
    merged_live_classes: int
    direct_live_classes: int
    matches_direct: bool


@dataclass(frozen=True, order=True)
class LegRatioSquareclass:
    """Squareclass diagnostic for the Pythagorean-leg test ``z^2 + 1``."""

    ratio: Fraction
    value: Fraction
    is_square: bool
    squarefree_part: int
    squareclass_primes: tuple[int, ...]
    three_mod_four_primes: tuple[int, ...]


@dataclass(frozen=True, order=True)
class SumAbSlopeObstruction:
    """Four-term squareclass diagnostic for one ``sum=A+B`` slope candidate."""

    lambda_ratio: Fraction
    slope1: Fraction
    slope2: Fraction
    r1: Fraction
    r2: Fraction
    failed_terms: tuple[str, ...]
    passed_terms: tuple[str, ...]
    term_squareclasses: tuple[tuple[str, int], ...]

    @property
    def pass_count(self) -> int:
        return len(self.passed_terms)

    @property
    def failure_count(self) -> int:
        return len(self.failed_terms)

    @property
    def three_pass_near_miss(self) -> bool:
        return self.pass_count == 3 and self.failure_count == 1


@dataclass(frozen=True, order=True)
class SumAbThreePassMobiusModel:
    """Möbius reconstruction for a ``sum=A+B`` three-pass near-miss.

    Given one slope ``x`` and its scaled mate ``r = lambda*x``, closure forces:

        lambda = r/x
        y = 1 - x + x/r
        s = lambda*y = 1 - r + r/x

    If ``x``, ``r``, and ``y`` are Pythagorean leg ratios but ``s`` is not,
    this is the three-pass near-miss layer in equation form.
    """

    lambda_ratio: Fraction
    slope: Fraction
    other_slope: Fraction
    scaled_term: Fraction
    failed_scaled_term: Fraction
    slope_squareclass: int
    other_slope_squareclass: int
    scaled_term_squareclass: int
    failed_squareclass: int

    @property
    def closes_sum_ab(self) -> bool:
        return self.scaled_term + self.failed_scaled_term == self.lambda_ratio + 1

    @property
    def three_terms_are_pythagorean(self) -> bool:
        return (
            self.slope_squareclass == 1
            and self.other_slope_squareclass == 1
            and self.scaled_term_squareclass == 1
        )

    @property
    def failed_term_is_pythagorean(self) -> bool:
        return self.failed_squareclass == 1


@dataclass(frozen=True, order=True)
class SumAbThreePassEuclidModel:
    """Euclid-parameter view of the ``sum=A+B`` Möbius model."""

    slope_param: PythagoreanLegParam
    scaled_term_param: PythagoreanLegParam
    mobius: SumAbThreePassMobiusModel
    other_slope_square_equation: tuple[Fraction, Fraction | None]
    failed_square_equation: tuple[Fraction, Fraction | None]
    other_slope_integer_equation: tuple[int, int, int | None]
    failed_integer_equation: tuple[int, int, int | None]
    other_slope_polynomial_terms: tuple[int, int]
    failed_polynomial_terms: tuple[int, int]
    other_slope_polynomial_equation: tuple[int, int, int | None]
    failed_polynomial_equation: tuple[int, int, int | None]

    @property
    def failed_squareclass(self) -> int:
        return self.mobius.failed_squareclass


@dataclass(frozen=True, order=True)
class SumAbEuclidOrientationEquation:
    """One orientation case after substituting Euclid leg terms into ``sum=A+B``."""

    slope_orientation: str
    scaled_term_orientation: str
    slope_terms: tuple[int, int]
    scaled_term_terms: tuple[int, int]
    other_slope_polynomial_equation: tuple[int, int, int | None]
    failed_polynomial_equation: tuple[int, int, int | None]


@dataclass(frozen=True, order=True)
class SumAbEuclidResidueSummary:
    """Residue-class counts for one ``sum=A+B`` Euclid orientation modulo M."""

    modulus: int
    slope_orientation: str
    scaled_term_orientation: str
    total_classes: int
    other_square_classes: int
    failed_square_classes: int
    both_square_classes: int
    other_only_classes: int
    failed_only_classes: int
    neither_square_classes: int

    @property
    def other_square_forces_failed_square(self) -> bool:
        return self.other_only_classes == 0


@dataclass(frozen=True, order=True)
class SumAbSameOrientationBothPassResidueSummary:
    """Residue counts for same-orientation shared-leg both-pass classes."""

    modulus: int
    total_classes_by_orientation: dict[str, int]
    p_equals_q_count_by_orientation: dict[str, int]
    noncenter_survivor_count_by_orientation: dict[str, int]
    noncenter_examples_by_orientation: dict[str, tuple[tuple[int, ...], ...]]


@dataclass(frozen=True, order=True)
class SumAbSameOrientationBothPassLiftSummary:
    """One-step lift counts for a same-orientation both-pass residue class."""

    modulus: int
    next_modulus: int
    orientation: str
    residue: tuple[int, int, int, int]
    prime: int
    lift_count: int
    diff_valuation_counts: dict[int, int]
    examples: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, order=True)
class SumAbSameOrientationDifferenceFactorValuationSummary:
    """Valuation split for ``P-Q = ±2(mu+nv)(nu-mv)`` survivors."""

    modulus: int
    orientation: str
    prime: int
    total_survivors: int
    pattern_counts: dict[tuple[int, int, int], int]
    examples: dict[tuple[int, int, int], tuple[int, ...]]


@dataclass(frozen=True, order=True)
class SumAbSameOrientationCombinedValuationSummary:
    """Combined factor valuation patterns for same-orientation survivors."""

    modulus: int
    orientation: str
    prime: int
    total_survivors: int
    pattern_count: int
    top_patterns: tuple[tuple[tuple[int, ...], int], ...]
    zero_offset_pattern_count: int
    examples: dict[tuple[int, ...], tuple[int, ...]]


@dataclass(frozen=True, order=True)
class SumAbSameOrientationSharedLegTerms:
    """Shared-leg square equations for one same-orientation ``sum=A+B`` case."""

    orientation: str
    slope_terms: tuple[int, int]
    scaled_term_terms: tuple[int, int]
    shared_numerator: int
    other_denominator: int
    failed_denominator: int
    other_square_equation: tuple[int, int, int | None]
    failed_square_equation: tuple[int, int, int | None]

    @property
    def square_difference(self) -> int:
        other_value = (
            self.shared_numerator * self.shared_numerator
            + self.other_denominator * self.other_denominator
        )
        failed_value = (
            self.shared_numerator * self.shared_numerator
            + self.failed_denominator * self.failed_denominator
        )
        return other_value - failed_value

    @property
    def denominator_square_difference(self) -> int:
        return (
            self.other_denominator * self.other_denominator
            - self.failed_denominator * self.failed_denominator
        )

    @property
    def other_hypotenuse_factor_pair(self) -> tuple[int, int] | None:
        return _hypotenuse_factor_pair(self.other_square_equation)

    @property
    def failed_hypotenuse_factor_pair(self) -> tuple[int, int] | None:
        return _hypotenuse_factor_pair(self.failed_square_equation)

    @property
    def other_factor_pair_gcd(self) -> int | None:
        return _factor_pair_gcd(self.other_hypotenuse_factor_pair)

    @property
    def failed_factor_pair_gcd(self) -> int | None:
        return _factor_pair_gcd(self.failed_hypotenuse_factor_pair)

    @property
    def other_reduced_factor_pair(self) -> tuple[int, int] | None:
        return _reduced_factor_pair(self.other_hypotenuse_factor_pair)

    @property
    def failed_reduced_factor_pair(self) -> tuple[int, int] | None:
        return _reduced_factor_pair(self.failed_hypotenuse_factor_pair)

    @property
    def other_reduced_factor_pair_gcd(self) -> int | None:
        return _factor_pair_gcd(self.other_reduced_factor_pair)

    @property
    def failed_reduced_factor_pair_gcd(self) -> int | None:
        return _factor_pair_gcd(self.failed_reduced_factor_pair)

    @property
    def other_reduced_factor_pair_square_roots(self) -> tuple[int, int] | None:
        return _factor_pair_square_roots(self.other_reduced_factor_pair)

    @property
    def failed_reduced_factor_pair_square_roots(self) -> tuple[int, int] | None:
        return _factor_pair_square_roots(self.failed_reduced_factor_pair)

    @property
    def other_reduced_factor_pair_is_square_pair(self) -> bool:
        return self.other_reduced_factor_pair_square_roots is not None

    @property
    def failed_reduced_factor_pair_is_square_pair(self) -> bool:
        return self.failed_reduced_factor_pair_square_roots is not None

    @property
    def other_factor_pair_parameterization(self) -> tuple[int, int, int] | None:
        return _factor_pair_parameterization(
            self.other_factor_pair_gcd,
            self.other_reduced_factor_pair_square_roots,
        )

    @property
    def failed_factor_pair_parameterization(self) -> tuple[int, int, int] | None:
        return _factor_pair_parameterization(
            self.failed_factor_pair_gcd,
            self.failed_reduced_factor_pair_square_roots,
        )

    @property
    def other_parameterized_shared_numerator(self) -> int | None:
        return _parameterized_shared_numerator(self.other_factor_pair_parameterization)

    @property
    def failed_parameterized_shared_numerator(self) -> int | None:
        return _parameterized_shared_numerator(self.failed_factor_pair_parameterization)

    @property
    def other_parameterized_denominator(self) -> int | None:
        return _parameterized_denominator(self.other_factor_pair_parameterization)

    @property
    def failed_parameterized_denominator(self) -> int | None:
        return _parameterized_denominator(self.failed_factor_pair_parameterization)

    @property
    def other_parameterized_hypotenuse(self) -> int | None:
        return _parameterized_hypotenuse(self.other_factor_pair_parameterization)

    @property
    def failed_parameterized_hypotenuse(self) -> int | None:
        return _parameterized_hypotenuse(self.failed_factor_pair_parameterization)


@dataclass(frozen=True, order=True)
class SumAbSameOrientationDenominatorFactorization:
    """Factorization of ``P±Q`` for same-orientation denominators."""

    orientation: str
    shared_numerator: int
    other_denominator: int
    failed_denominator: int
    denominator_difference: int
    denominator_sum: int
    shared_minus_other_denominator: int
    shared_minus_failed_denominator: int
    nu_minus_mv: int
    difference_factorization: tuple[int, int, int]
    sum_factorization: tuple[int, int, int]
    shared_minus_other_factorization: tuple[int, int]
    shared_minus_failed_factorization: tuple[int, int]


@dataclass(frozen=True, order=True)
class SumAbSameOrientationCrossGcdTerms:
    """Cross-gcd diagnostics for ``P=bc`` and ``Q=ad`` denominators."""

    orientation: str
    slope_terms: tuple[int, int]
    scaled_term_terms: tuple[int, int]
    other_denominator: int
    failed_denominator: int
    denominator_difference: int
    denominator_sum: int
    gcd_a_b: int
    gcd_c_d: int
    gcd_a_c: int
    gcd_a_d: int
    gcd_b_c: int
    gcd_b_d: int
    gcd_p_q: int
    difference_factorization: tuple[int, int, int]
    sum_factorization: tuple[int, int, int]

    @property
    def primitive_cross_gcd_product(self) -> int:
        return self.gcd_a_c * self.gcd_b_d

    @property
    def primitive_cross_gcd_identity_holds(self) -> bool:
        return (
            self.gcd_a_b == 1
            and self.gcd_c_d == 1
            and self.gcd_p_q == self.primitive_cross_gcd_product
        )

    @property
    def denominator_difference_over_gcd(self) -> int | None:
        if self.gcd_p_q == 0 or self.denominator_difference % self.gcd_p_q != 0:
            return None
        return self.denominator_difference // self.gcd_p_q

    @property
    def denominator_sum_over_gcd(self) -> int | None:
        if self.gcd_p_q == 0 or self.denominator_sum % self.gcd_p_q != 0:
            return None
        return self.denominator_sum // self.gcd_p_q

    @property
    def normalized_denominator_pair(self) -> tuple[int, int] | None:
        if (
            self.gcd_p_q == 0
            or self.other_denominator % self.gcd_p_q != 0
            or self.failed_denominator % self.gcd_p_q != 0
        ):
            return None
        return (
            self.other_denominator // self.gcd_p_q,
            self.failed_denominator // self.gcd_p_q,
        )

    @property
    def difference_factorization_over_gcd(self) -> tuple[Fraction, int, int] | None:
        if self.gcd_p_q == 0:
            return None
        coefficient, first_factor, second_factor = self.difference_factorization
        return Fraction(coefficient, self.gcd_p_q), first_factor, second_factor

    @property
    def sum_factorization_over_gcd(self) -> tuple[Fraction, int, int] | None:
        if self.gcd_p_q == 0:
            return None
        coefficient, first_factor, second_factor = self.sum_factorization
        return Fraction(coefficient, self.gcd_p_q), first_factor, second_factor


@dataclass(frozen=True, order=True)
class SumAbNormalizedNearMissExample:
    """One same-orientation near-miss with gcd-normalized denominators."""

    orientation: str
    slope_params: tuple[int, int]
    scaled_term_params: tuple[int, int]
    shared_numerator: int
    other_denominator: int
    failed_denominator: int
    gcd_p_q: int
    gcd_n_p_q: int
    normalized_denominator_pair: tuple[int, int]
    normalized_shared_leg_triple: tuple[int, int, int]
    normalized_other_squareclass: int
    normalized_failed_squareclass: int
    denominator_difference_over_gcd: int
    denominator_sum_over_gcd: int
    other_square_passes: bool
    failed_square_passes: bool


@dataclass(frozen=True)
class SumAbSquareclassFamilyEdge:
    """A candidate relation between two canonical triples in one squareclass."""

    source: tuple[int, int, int]
    target: tuple[int, int, int]
    target_uses_source_failed_leg: bool
    target_uses_source_shared_leg: bool

    @property
    def source_max(self) -> int:
        return max(self.source)

    @property
    def target_max(self) -> int:
        return max(self.target)

    @property
    def target_max_delta(self) -> int:
        return self.target_max - self.source_max

    @property
    def target_n_delta(self) -> int:
        return self.target[0] - self.source[0]

    @property
    def decreases_n(self) -> bool:
        return self.target_n_delta < 0

    @property
    def decreases_max(self) -> bool:
        return self.target_max_delta < 0


@dataclass(frozen=True)
class SumAbNormalizedNearMissSummary:
    """Small bounded scan summary for same-orientation normalized near-misses."""

    max_m: int
    total_near_misses: int
    abs_difference_over_gcd_counts: dict[int, int]
    failing_squareclass_counts: dict[int, int]
    normalized_pair_counts: dict[tuple[tuple[int, int], str], int]
    examples_by_abs_difference: dict[int, tuple[SumAbNormalizedNearMissExample, ...]]
    examples_by_failing_squareclass: dict[
        int, tuple[SumAbNormalizedNearMissExample, ...]
    ]
    canonical_triples_by_failing_squareclass: dict[
        int, tuple[tuple[int, int, int], ...]
    ]
    family_edges_by_failing_squareclass: dict[
        int, tuple[SumAbSquareclassFamilyEdge, ...]
    ]
    n_descending_edge_count: int
    n_descending_continuation_count: int


@dataclass(frozen=True)
class SumAbFourSlopeSquareclassSummary:
    """Bounded four-slope squareclass diagnostic for ``sum=A+B``."""

    max_m: int
    slope_count: int
    equal_unit_squareclass_pairs: int
    centerline_equal_unit_squareclass_pairs: int
    noncenter_equal_unit_squareclass_pairs: int
    true_four_pass_pairs: int
    centerline_squareclasses: dict[int, int]


@dataclass(frozen=True, order=True)
class SumAbFourSlopeSquareclassWitness:
    """One bounded equal-squareclass witness in the four-slope model."""

    slope1: Fraction
    slope2: Fraction
    lambda_ratio: Fraction
    r: Fraction
    s: Fraction
    unit_squareclass: int
    centerline: bool
    true_four_pass: bool


@dataclass(frozen=True, order=True)
class SumAbFourSquareDualSlopeModel:
    """Dual-slope ledger for the four individual square conditions."""

    slope_x: Fraction
    slope_y: Fraction
    common_leg: Fraction
    dual_slope_x: Fraction
    dual_slope_y: Fraction
    x_is_pythagorean: bool
    y_is_pythagorean: bool
    dual_x_is_pythagorean: bool
    dual_y_is_pythagorean: bool
    all_four_slopes_are_pythagorean: bool
    dual_denominator: Fraction
    reconstructed_x: Fraction
    reconstructed_y: Fraction
    reconstructed_common_leg: Fraction
    self_dual_identity_holds: bool


@dataclass(frozen=True, order=True)
class SumAbDualSlopeParameterization:
    """Parameterize the dual slopes and recover the original slopes."""

    parameter_t: Fraction
    parameter_u: Fraction
    dual_slope_x: Fraction
    dual_slope_y: Fraction
    dual_denominator: Fraction
    generated_x: Fraction
    generated_y: Fraction
    common_leg: Fraction
    generated_x_recovery_value: Fraction
    generated_y_recovery_value: Fraction
    generated_x_is_pythagorean: bool
    generated_y_is_pythagorean: bool
    generated_x_minus_y: Fraction
    generated_x_minus_y_factorized: Fraction
    recovery_value_difference_factorized: Fraction
    centerline_factor: Fraction
    centerline_factor_zero: bool
    centerline_recovery_quartic: Fraction


@dataclass(frozen=True, order=True)
class SumAbDualSlopeValuationRow:
    """Prime-valuation row for dual-slope recovery square conditions."""

    prime: int
    recovery_valuations: tuple[int, int]
    recovery_difference_valuation: int | None
    centerline_factor_valuation: int | None
    all_recovery_valuations_even: bool


@dataclass(frozen=True)
class SumAbDualSlopeValuationLedger:
    """Prime-valuation ledger for the dual-slope recovery values."""

    parameterization: SumAbDualSlopeParameterization
    recovery_squareclasses: tuple[int, int]
    recovery_squareclass_primes: tuple[int, ...]
    three_mod_four_recovery_squareclass_primes: tuple[int, ...]
    primes: tuple[int, ...]
    three_mod_four_primes: tuple[int, ...]
    rows: tuple[SumAbDualSlopeValuationRow, ...]
    rows_by_prime: dict[int, SumAbDualSlopeValuationRow]


@dataclass(frozen=True)
class SumAbDualSlopeQAdicNormLedger:
    """Global squareclass ledger for the ``p+lambda`` q-adic norm shadow."""

    parameterization: SumAbDualSlopeParameterization
    parameter_pairs: tuple[Fraction, Fraction]
    prime: int
    q_norm_values: tuple[Fraction, Fraction]
    q_norm_valuations: tuple[int | None, int | None]
    q_norm_squareclasses: tuple[int, int]
    odd_q_norm_squareclass_primes: tuple[tuple[int, ...], tuple[int, ...]]
    recovery_squareclasses: tuple[int, int]
    recovery_squareclass_primes: tuple[tuple[int, ...], tuple[int, ...]]
    recovery_valuations_at_prime: tuple[int | None, int | None]
    shadow_prime_balanced_in_recovery_squareclasses: bool


@dataclass(frozen=True)
class SumAbDualSlopeQAdicNormSummary:
    """Batch summary for q-adic norm shadow squareclass ledgers."""

    prime: int
    sample_count: int
    shadow_prime_balanced_count: int
    recovery_contains_shadow_prime_count: int
    recovery_has_three_mod_four_prime_count: int
    recovery_has_only_two_or_one_mod_four_primes_count: int
    q_norm_valuation_pair_counts: dict[tuple[int | None, int | None], int]
    recovery_prime_mod4_counts: dict[int, int]
    recovery_prime_mod8_counts: dict[int, int]
    recovery_prime_mod16_counts: dict[int, int]
    examples_by_bucket: dict[str, SumAbDualSlopeQAdicNormLedger]


@dataclass(frozen=True)
class SumAbDualSlopeQAdicNormGeneratedSummary:
    """Generated q-adic shadow samples plus their norm squareclass summary."""

    prime: int
    exponent: int
    modulus: int
    representative_bound: int
    root_count_mod_prime: int
    lift_count: int
    lifted_residue_pairs: tuple[tuple[int, int], ...]
    parameter_pairs: tuple[tuple[Fraction, Fraction], ...]
    summary: SumAbDualSlopeQAdicNormSummary


@dataclass(frozen=True)
class SumAbDualSlopeQAdicNormBridgeLedger:
    """One q-adic norm shadow sample rewritten as a Gaussian bridge cycle."""

    norm_ledger: SumAbDualSlopeQAdicNormLedger
    bridge_cycle: SumAbDualSlopeGaussianBridgeCycle
    recovery_matches_bridge_squareclasses: bool
    generated_flags_match_bridge_flags: bool


@dataclass(frozen=True)
class SumAbDualSlopeQAdicNormBridgeSummary:
    """Batch bridge-cycle summary for generated q-adic norm shadow samples."""

    generated_summary: SumAbDualSlopeQAdicNormGeneratedSummary
    ledgers: tuple[SumAbDualSlopeQAdicNormBridgeLedger, ...]
    sample_count: int
    recovery_matches_bridge_squareclass_count: int
    generated_flags_match_bridge_flags_count: int
    all_cross_bridges_pythagorean_count: int
    first_ledger: SumAbDualSlopeQAdicNormBridgeLedger | None


@dataclass(frozen=True, order=True)
class SumAbDualSlopeQAdicBridgeValuationRow:
    """Valuation row for one generated q-adic bridge-cycle sample."""

    parameter_pairs: tuple[Fraction, Fraction]
    centerline_factor_valuations: tuple[int | None, int | None, int | None, int | None]
    extra_factor_valuation: int | None
    bridge_difference_valuation: int | None
    bridge_value_valuation_pair: tuple[int | None, int | None]
    bridge_value_2adic_pair: tuple[int | None, int | None]


@dataclass(frozen=True)
class SumAbDualSlopeQAdicBridgeValuationSummary:
    """Batch valuation summary for q-adic bridge-cycle samples."""

    generated_summary: SumAbDualSlopeQAdicNormGeneratedSummary
    rows: tuple[SumAbDualSlopeQAdicBridgeValuationRow, ...]
    sample_count: int
    centerline_factor_valuation_counts: dict[
        tuple[int | None, int | None, int | None, int | None],
        int,
    ]
    extra_factor_valuation_counts: dict[int | None, int]
    bridge_difference_valuation_counts: dict[int | None, int]
    bridge_value_valuation_pair_counts: dict[tuple[int | None, int | None], int]
    bridge_value_2adic_pair_counts: dict[tuple[int | None, int | None], int]
    first_row: SumAbDualSlopeQAdicBridgeValuationRow | None


@dataclass(frozen=True)
class SumAbDualSlopeQAdicBridgeTwoAdicSummary:
    """Two-adic square obstruction summary for q-adic bridge samples."""

    valuation_summary: SumAbDualSlopeQAdicBridgeValuationSummary
    sample_count: int
    parity_killed_count: int
    two_adic_local_square_count: int
    bridge_value_2adic_pair_counts: dict[tuple[int | None, int | None], int]
    local_square_unit_mod8_pair_counts: dict[tuple[int, int], int]


@dataclass(frozen=True)
class SumAbDualSlopeQAdicBridgeLocalSquareSummary:
    """Odd-q and two-adic local-square summary for bridge samples."""

    two_adic_summary: SumAbDualSlopeQAdicBridgeTwoAdicSummary
    sample_count: int
    two_adic_local_square_count: int
    q_adic_local_square_count: int
    combined_q_and_2_adic_local_square_count: int
    q_adic_local_square_flag_pair_counts: dict[tuple[bool, bool], int]
    combined_survivor_parameter_pairs: tuple[tuple[Fraction, Fraction], ...]


@dataclass(frozen=True)
class SumAbDualSlopeGaussianAbsorption:
    """Gaussian absorption of one failed dual-slope recovery value."""

    parameterization: SumAbDualSlopeParameterization
    failed_side: str
    failed_slope: Fraction
    failed_value: Fraction
    failed_squareclass: int
    two_square_decomposition: tuple[int, int]
    absorbed_plus: Fraction | None
    absorbed_minus: Fraction | None
    matching_absorptions: tuple[tuple[str, str, Fraction], ...]
    absorbs_to_existing_dual_slope: bool


@dataclass(frozen=True)
class SumAbDualSlopeGaussianBridge:
    """Gaussian angle bridge from a failed slope to one dual slope."""

    parameterization: SumAbDualSlopeParameterization
    failed_side: str
    target_side: str
    failed_slope: Fraction
    target_slope: Fraction
    failed_squareclass: int
    bridge_ratio: Fraction
    bridge_value: Fraction
    bridge_squareclass: int
    squareclass_matches_failure: bool
    recovered_target: Fraction
    recovery_identity_holds: bool


@dataclass(frozen=True)
class SumAbDualSlopeGaussianBridgeCycle:
    """Cross-bridge ledger for the dual-slope four-square loop."""

    parameterization: SumAbDualSlopeParameterization
    x_to_dual_y: SumAbDualSlopeGaussianBridge
    y_to_dual_x: SumAbDualSlopeGaussianBridge
    generated_slopes: tuple[Fraction, Fraction]
    dual_slopes: tuple[Fraction, Fraction]
    bridge_ratios: tuple[Fraction, Fraction]
    generated_squareclasses: tuple[int, int]
    bridge_squareclasses: tuple[int, int]
    generated_pythagorean_flags: tuple[bool, bool]
    bridge_pythagorean_flags: tuple[bool, bool]
    generated_flags_match_bridge_flags: bool
    all_generated_slopes_are_pythagorean: bool
    all_cross_bridges_are_pythagorean: bool


@dataclass(frozen=True)
class SumAbDualSlopeBridgeDifferenceFactorization:
    """Factorization ledger for the two cross-bridge square values."""

    bridge_cycle: SumAbDualSlopeGaussianBridgeCycle
    bridge_value_difference: Fraction
    centerline_factor: Fraction
    extra_equal_bridge_factor: Fraction
    bridge_difference_factorized: Fraction
    factorization_holds: bool
    extra_factor_u_quadratic_coefficients: tuple[Fraction, Fraction, Fraction]
    extra_factor_u_discriminant: Fraction
    new_curve_value_t: Fraction
    extra_factor_discriminant_matches_new_curve: bool


@dataclass(frozen=True, order=True)
class SumAbSquareclassRatioZReduction:
    """The ``A/B`` squareclass-ratio equation after ``z = u - 1/u``."""

    t: Fraction
    u: Fraction
    z: Fraction
    direct_ratio: Fraction
    reduced_ratio: Fraction
    ratio_is_square: bool
    u_recovery_square: Fraction


@dataclass(frozen=True, order=True)
class SumAbSquareclassRatioZParameterization:
    """The ``z^2+4`` parameterization returns the original ratio shape."""

    t: Fraction
    parameter: Fraction
    z: Fraction
    reduced_ratio: Fraction
    self_similar_ratio: Fraction
    ratio_is_square: bool
    centerline_factor: Fraction


@dataclass(frozen=True, order=True)
class SumAbSquareclassRatioTUQuotientModel:
    """The quotient model using ``T=t-1/t`` and ``U=u-1/u``."""

    t_quotient: Fraction
    u_quotient: Fraction
    numerator_quadratic: Fraction
    denominator_quadratic: Fraction
    ratio: Fraction
    ratio_is_square: bool
    t_recovery_square: bool
    u_recovery_square: bool


@dataclass(frozen=True, order=True)
class SumAbSquareclassRatioSlopeQuadraticModel:
    """The squareclass-ratio model directly in Pythagorean slopes ``x,y``."""

    slope_x: Fraction
    slope_y: Fraction
    numerator_quadratic: Fraction
    denominator_quadratic: Fraction
    ratio: Fraction
    ratio_is_square: bool
    numerator_is_square: bool
    denominator_is_square: bool
    individual_unit_terms_are_squares: bool
    x_recovery_square: bool
    y_recovery_square: bool


@dataclass(frozen=True, order=True)
class SumAbSlopeRatioYDiscriminantLedger:
    """Discriminant ledger for ``P = KQ`` as a quadratic in ``y``."""

    slope_x: Fraction
    square_ratio: Fraction
    quadratic_coefficients: tuple[Fraction, Fraction, Fraction]
    y_discriminant: Fraction
    y_discriminant_inner: Fraction
    inner_as_quadratic_in_square_ratio: Fraction
    inner_square_ratio_discriminant: Fraction
    pythagorean_recovery_square: Fraction
    slope_x_is_pythagorean: bool
    new_curve_factor: Fraction
    new_curve_factor_is_square: bool


@dataclass(frozen=True, order=True)
class SumAbNewCurveResidueSummary:
    """Residue summary for ``Y^2 = 5t^4+8t^3-6t^2-8t+5``."""

    modulus: int
    primitive_classes: int
    square_classes: int
    boundary_square_classes: int
    nonboundary_square_classes: int
    boundary_examples: tuple[tuple[int, int, int], ...]
    nonboundary_examples: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True, order=True)
class SumAbNewCurveZReduction:
    """Reduction of the new quartic by ``z=t-1/t``."""

    parameter_t: Fraction
    z_value: Fraction
    original_quartic_value: Fraction
    scaled_quartic_value: Fraction
    z_recovery_square: Fraction
    new_curve_square: Fraction
    identity_holds: bool
    z_recovery_is_square: bool
    new_curve_is_square: bool


@dataclass(frozen=True, order=True)
class SumAbZLemmaCenterlineBridge:
    """Bridge from the ``z`` lemma to the centerline quartic."""

    parameter: Fraction
    z_value: Fraction
    denominator_square: Fraction
    scaled_second_square: Fraction
    remaining_quartic: Fraction
    centerline_parameter: Fraction
    centerline_quartic: Fraction
    identity_holds: bool
    remaining_quartic_is_square: bool


@dataclass(frozen=True, order=True)
class SumAbBridgeExtraFactorZLemmaReduction:
    """Reduction of the bridge extra factor to the z-lemma centerline quartic."""

    parameter_t: Fraction
    z_value: Fraction
    z_parameter_m: Fraction
    new_curve_value_t: Fraction
    scaled_new_curve_value: Fraction
    z_recovery_square: Fraction
    z_lemma_new_curve_square: Fraction
    z_reduction_identity_holds: bool
    centerline_bridge: SumAbZLemmaCenterlineBridge
    centerline_bridge_identity_holds: bool
    extra_factor_reduces_to_centerline: bool


@dataclass(frozen=True, order=True)
class SumAbDualSlopeBridgeProjectiveResidueSummary:
    """Projective residue counts for the dual-slope bridge square conditions."""

    modulus: int
    projective_class_count: int
    both_bridge_square_classes: int
    centerline_square_classes: int
    noncenter_square_classes: int
    noncenter_extra_factor_zero_classes: int
    noncenter_extra_factor_nonzero_classes: int
    noncenter_extra_factor_nonzero_examples: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class SumAbDualSlopeBridgePrimePowerLiftSummary:
    """Prime-power lift counts for bridge square valuation pairs."""

    prime: int
    exponent: int
    modulus: int
    projective_class_count: int
    both_bridge_square_classes: int
    valuation_pair_counts: dict[tuple[int, int], int]
    centerline_unit_extra_unit_classes: int
    centerline_unit_classes: int
    centerline_unit_min_extra_valuation: int | None


@dataclass(frozen=True)
class SumAbDualSlopeBridgeCenterlineFactorLiftSummary:
    """Prime-power lift counts after splitting the centerline factor."""

    prime: int
    exponent: int
    modulus: int
    projective_class_count: int
    both_bridge_square_classes: int
    factor_extra_valuation_counts: dict[tuple[int, int, int, int, int], int]
    centerline_factor_valuation_counts: dict[tuple[int, int, int, int], int]
    max_centerline_factor_extra_valuation_counts: dict[tuple[int, int], int]


@dataclass(frozen=True, order=True)
class SumAbDualSlopeBridgeCenterlineBranchRestriction:
    """Exact bridge-numerator restriction on one centerline-factor branch."""

    branch: str
    restriction_kind: str
    parameter_t: Fraction
    parameter_u: Fraction
    x_bridge_numerator: Fraction
    y_bridge_numerator: Fraction
    common_bridge_numerator: Fraction
    predicted_common_bridge_numerator: Fraction
    extra_factor: Fraction
    predicted_extra_factor: Fraction
    bridge_numerators_equal: bool
    common_identity_holds: bool
    extra_identity_holds: bool


@dataclass(frozen=True)
class SumAbDualSlopeBridgeTrivialTubeExpansion:
    """Expansion of bridge numerators around one trivial-square tube."""

    branch: str
    parameter_t: Fraction
    base_u: Fraction
    x_coefficients: tuple[Fraction, ...]
    y_coefficients: tuple[Fraction, ...]
    extra_coefficients: tuple[Fraction, ...]
    difference_coefficients: tuple[Fraction, ...]
    bridge_constants_equal: bool
    common_constant: Fraction
    common_constant_square_root: Fraction | None
    common_constant_is_square: bool
    nonzero_square_constant: bool


@dataclass(frozen=True, order=True)
class SumAbDualSlopeCenterlineFactorPositiveDomainRow:
    """Positive-domain status of one exact centerline-factor branch."""

    branch: str
    restriction_kind: str
    parameter_t: Fraction
    parameter_u: Fraction
    parameter_u_in_unit_interval: bool
    dual_slope_y: Fraction | None
    dual_slope_y_positive: bool
    dual_denominator: Fraction | None
    dual_denominator_positive: bool
    admissible_positive_parameterization: bool


@dataclass(frozen=True, order=True)
class SumAbDualSlopePositiveTrivialTubeLocalWitness:
    """Positive real point in a trivial tube that survives local square tests."""

    branch: str
    prime: int
    parameter_t: Fraction
    parameter_u: Fraction
    tube_value: Fraction
    tube_valuation: int
    dual_denominator: Fraction
    generated_slopes: tuple[Fraction, Fraction]
    recovery_values: tuple[Fraction, Fraction]
    local_square_flags: tuple[bool, bool]
    rational_square_flags: tuple[bool, bool]
    admissible_positive_parameterization: bool
    recovery_values_are_local_squares: bool
    recovery_values_are_rational_squares: bool


@dataclass(frozen=True)
class SumAbDualSlopePositiveTrivialTubeSquareclassLedger:
    """Global squareclasses for a positive trivial-tube local witness."""

    witness: SumAbDualSlopePositiveTrivialTubeLocalWitness
    recovery_squareclasses: tuple[int, int]
    recovery_squareclass_primes: tuple[tuple[int, ...], tuple[int, ...]]
    one_mod_four_squareclass_primes: tuple[int, ...]
    three_mod_four_squareclass_primes: tuple[int, ...]
    all_squareclass_primes_are_one_mod_four: bool


@dataclass(frozen=True)
class SumAbDualSlopePositiveTrivialTubeMemberLedger:
    """Full member-term squareclasses for a positive trivial-tube witness."""

    witness: SumAbDualSlopePositiveTrivialTubeLocalWitness
    lambda_ratio: Fraction
    ratios: tuple[Fraction, Fraction]
    product: Fraction
    member_values: tuple[Fraction, Fraction, Fraction, Fraction]
    member_squareclasses: tuple[int, int, int, int]
    member_squareclass_primes: tuple[
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
    ]
    one_mod_four_member_squareclass_primes: tuple[int, ...]
    three_mod_four_member_squareclass_primes: tuple[int, ...]
    closes_sum_ab: bool
    unit_terms_are_squares: bool
    lambda_terms_are_squares: bool
    true_member_pair: bool


@dataclass(frozen=True, order=True)
class SumAbKDiscriminantQuarticCompletion:
    """Completion-of-square ledger for the remaining ``K`` quartic."""

    parameter: Fraction
    square_ratio: Fraction
    centerline_quartic: Fraction
    remaining_quartic: Fraction
    linear_square_term: Fraction
    positive_square_term: Fraction
    positive_remainder: Fraction
    left_side: Fraction
    right_side: Fraction
    identity_holds: bool


@dataclass(frozen=True, order=True)
class SumAbKSquareCandidateYDiscriminant:
    """Ledger separating the ``K`` quartic layer from the actual ``y`` layer."""

    parameter: Fraction
    slope_x: Fraction
    square_ratio: Fraction
    square_ratio_is_square: bool
    remaining_quartic: Fraction
    remaining_quartic_is_square: bool
    y_discriminant: Fraction
    y_discriminant_is_square: bool


@dataclass(frozen=True, order=True)
class SumAbKSquareYDiscriminantFactorization:
    """Layer-3 factorization when the squareclass ratio is explicitly ``k^2``."""

    parameter: Fraction
    slope_x: Fraction
    square_ratio_root: Fraction
    square_ratio: Fraction
    minus_factor: Fraction
    plus_factor: Fraction
    y_discriminant: Fraction
    factorized_y_discriminant: Fraction
    factorization_holds: bool
    shared_factor_discriminant: Fraction
    shared_factor_discriminant_is_square: bool


@dataclass(frozen=True, order=True)
class SumAbRatioShadowOrbit:
    """A lightweight reciprocal-shadow grouping for ``sum=A+B`` obstructions."""

    key: tuple[Fraction, ...]
    members: tuple[SumAbSlopeObstruction, ...]
    failed_squareclasses: tuple[int, ...]

    @property
    def member_count(self) -> int:
        return len(self.members)


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _validate_positive(name: str, value: Fraction) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _is_rational_square(value: Fraction) -> bool:
    if value < 0:
        return False
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    return num * num == value.numerator and den * den == value.denominator


def _rational_sqrt(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    if num * num == value.numerator and den * den == value.denominator:
        return Fraction(num, den)
    return None


def _factorize_positive(value: int) -> dict[int, int]:
    if value <= 0:
        raise ValueError("value must be positive")
    return {int(prime): int(exponent) for prime, exponent in factorint(value).items()}


def _rational_squareclass(value: Fraction) -> tuple[int, tuple[int, ...]]:
    """Return the positive squarefree representative of a rational squareclass."""
    if value <= 0:
        raise ValueError("value must be positive")
    parity: dict[int, int] = {}
    for part in (value.numerator, value.denominator):
        for prime, exponent in _factorize_positive(part).items():
            parity[prime] = (parity.get(prime, 0) + exponent) % 2
    primes = tuple(sorted(prime for prime, exponent in parity.items() if exponent))
    squarefree = 1
    for prime in primes:
        squarefree *= prime
    return squarefree, primes


def _integer_squareclass(value: int) -> int:
    """Return the positive squarefree representative of an integer squareclass."""
    if value <= 0:
        raise ValueError("value must be positive")
    squarefree = 1
    for prime, exponent in _factorize_positive(value).items():
        if exponent % 2:
            squarefree *= prime
    return squarefree


def _two_square_decomposition(value: int) -> tuple[int, int] | None:
    if value <= 0:
        raise ValueError("value must be positive")
    limit = isqrt(value)
    for first in range(limit + 1):
        second_squared = value - first * first
        second = isqrt(second_squared)
        if second * second == second_squared:
            return tuple(sorted((first, second), reverse=True))
    return None


def _rational_valuation(value: Fraction, prime: int) -> int | None:
    if prime <= 1:
        raise ValueError("prime must be greater than 1")
    if value == 0:
        return None
    numerator_exponent = _factorize_positive(abs(value.numerator)).get(prime, 0)
    denominator_exponent = _factorize_positive(value.denominator).get(prime, 0)
    return numerator_exponent - denominator_exponent


def _prime_support(values: tuple[Fraction | None, ...]) -> tuple[int, ...]:
    primes: set[int] = set()
    for value in values:
        if value is None or value == 0:
            continue
        for part in (abs(value.numerator), value.denominator):
            primes.update(_factorize_positive(part))
    return tuple(sorted(primes))


def squareclass_two_square_absorption(
    ratio: Fraction | int,
    squareclass: int,
) -> SquareclassTwoSquareAbsorption:
    """Absorb a two-square squareclass from ``ratio^2+1`` by Gaussian division."""
    value = _as_fraction(ratio)
    _validate_positive("ratio", value)
    if squareclass <= 0:
        raise ValueError("squareclass must be positive")
    decomposition = _two_square_decomposition(squareclass)
    if decomposition is None:
        raise ValueError("squareclass is not a sum of two squares")
    first, second = decomposition
    if first == 0:
        raise ValueError("two-square decomposition must have nonzero real part")
    absorbed_plus = (first * value + second) / (first - second * value)
    absorbed_minus = (first * value - second) / (first + second * value)
    plus_value = absorbed_plus * absorbed_plus + 1
    minus_value = absorbed_minus * absorbed_minus + 1
    return SquareclassTwoSquareAbsorption(
        ratio=value,
        squareclass=squareclass,
        two_square_decomposition=decomposition,
        absorbed_plus=absorbed_plus,
        absorbed_minus=absorbed_minus,
        absorbed_plus_value=plus_value,
        absorbed_minus_value=minus_value,
        absorbed_plus_is_member=_is_rational_square(plus_value),
        absorbed_minus_is_member=_is_rational_square(minus_value),
    )


def _absorbed_member_values(
    absorption: SquareclassTwoSquareAbsorption,
) -> tuple[Fraction, ...]:
    values: list[Fraction] = []
    if absorption.absorbed_plus > 0 and absorption.absorbed_plus_is_member:
        values.append(absorption.absorbed_plus)
    if absorption.absorbed_minus > 0 and absorption.absorbed_minus_is_member:
        values.append(absorption.absorbed_minus)
    return tuple(sorted(set(values)))


def _absorbed_branch_for_member(
    absorption: SquareclassTwoSquareAbsorption,
    absorbed: Fraction,
) -> str:
    if absorption.absorbed_plus == absorbed:
        return "plus"
    if absorption.absorbed_minus == absorbed:
        return "minus"
    raise ValueError("absorbed value is not produced by this absorption")


def residual_gaussian_absorption_ledger(
    condition: ClosureProductSquareConditions,
) -> ResidualGaussianAbsorptionLedger:
    """Absorb a common residual squareclass from both roots when possible."""
    if len(condition.roots) != 2:
        raise ValueError("condition must have two positive roots")
    if len(condition.member_squareclass_pair) != 2:
        raise ValueError("condition must expose a member squareclass pair")
    if condition.member_squareclass_pair[0] != condition.member_squareclass_pair[1]:
        raise ValueError("condition must have a common member squareclass")
    squareclass = condition.member_squareclass_pair[0]
    if squareclass == 1:
        raise ValueError("condition must have a nontrivial member squareclass")
    r, s = condition.roots
    r_absorption = squareclass_two_square_absorption(r, squareclass)
    s_absorption = squareclass_two_square_absorption(s, squareclass)
    common_absorbed_members = tuple(
        sorted(set(_absorbed_member_values(r_absorption)).intersection(
            _absorbed_member_values(s_absorption)
        ))
    )
    return ResidualGaussianAbsorptionLedger(
        condition=condition,
        squareclass=squareclass,
        r_absorption=r_absorption,
        s_absorption=s_absorption,
        common_absorbed_members=common_absorbed_members,
        centerline_shadow=bool(common_absorbed_members),
    )


def _inverse_gaussian_absorption_branch(
    absorbed: Fraction,
    decomposition: tuple[int, int],
    branch: str,
) -> Fraction:
    first, second = decomposition
    if branch == "plus":
        denominator = second * absorbed + first
        if denominator == 0:
            raise ValueError("inverse plus branch has zero denominator")
        return (first * absorbed - second) / denominator
    if branch == "minus":
        denominator = first - second * absorbed
        if denominator == 0:
            raise ValueError("inverse minus branch has zero denominator")
        return (first * absorbed + second) / denominator
    raise ValueError("branch must be 'plus' or 'minus'")


def inverse_gaussian_absorption_pair(
    *,
    absorbed: Fraction | int,
    squareclass: int,
    r_branch: str,
    s_branch: str,
) -> InverseGaussianAbsorptionPair:
    """Generate a ``sum=A+B`` product-layer pair from one absorbed slope."""
    absorbed_fraction = _as_fraction(absorbed)
    _validate_positive("absorbed", absorbed_fraction)
    decomposition = _two_square_decomposition(squareclass)
    if decomposition is None:
        raise ValueError("squareclass is not a sum of two squares")
    r = _inverse_gaussian_absorption_branch(absorbed_fraction, decomposition, r_branch)
    s = _inverse_gaussian_absorption_branch(absorbed_fraction, decomposition, s_branch)
    if r <= 0 or s <= 0:
        raise ValueError("inverse branches must generate positive roots")
    lam = r + s - 1
    _validate_positive("lambda_ratio", lam)
    product = r * s
    condition = closure_product_square_conditions(lam, lam + 1, product, REL_SUM_AB)
    return InverseGaussianAbsorptionPair(
        absorbed=absorbed_fraction,
        squareclass=squareclass,
        two_square_decomposition=decomposition,
        r_branch=r_branch,
        s_branch=s_branch,
        r=r,
        s=s,
        lambda_ratio=lam,
        product=product,
        condition=condition,
    )


def inverse_gaussian_absorption_pair_terms(
    *,
    absorbed: Fraction | int,
    squareclass: int,
    r_branch: str,
    s_branch: str,
) -> InverseGaussianAbsorptionPairTerms:
    """Return exact factor terms for the inverse Gaussian ``plus,minus`` pair."""
    if (r_branch, s_branch) != ("plus", "minus"):
        raise ValueError("symbolic terms are currently implemented for plus,minus")
    pair = inverse_gaussian_absorption_pair(
        absorbed=absorbed,
        squareclass=squareclass,
        r_branch=r_branch,
        s_branch=s_branch,
    )
    z = pair.absorbed
    first, second = pair.two_square_decomposition
    first_sq = first * first
    second_sq = second * second
    squareclass_fraction = Fraction(pair.squareclass)

    denominator_product = first_sq - second_sq * z * z
    if denominator_product == 0:
        raise ValueError("inverse plus,minus branch has zero product denominator")

    lambda_numerator = (
        2 * first_sq * z - first_sq + second_sq * z * z + 2 * second_sq * z
    )
    product_numerator = first_sq * z * z - second_sq

    lambda_minus_left = first + second - z * (first - second)
    lambda_minus_right = z * (first + second) - (first - second)
    lambda_plus_z_factor = z * z + 2 * z - 1
    lambda_squared_minus_one_extra = (
        first_sq * z - first_sq + second_sq * z * z + second_sq * z
    )

    denominator_squared = denominator_product * denominator_product
    denominator_fourth = denominator_squared * denominator_squared
    z_unit_factor = z * z + 1

    lambda_minus_product_factorized = (
        lambda_minus_left * lambda_minus_right / denominator_product
    )
    lambda_plus_product_factorized = (
        squareclass_fraction * lambda_plus_z_factor / denominator_product
    )
    lambda_squared_minus_product_squared_factorized = (
        squareclass_fraction
        * lambda_plus_z_factor
        * lambda_minus_left
        * lambda_minus_right
        / denominator_squared
    )
    lambda_squared_minus_one_factorized = (
        4
        * z
        * squareclass_fraction
        * lambda_squared_minus_one_extra
        / denominator_squared
    )
    a_term_factorized = (
        squareclass_fraction
        * squareclass_fraction
        * z_unit_factor
        * z_unit_factor
        / denominator_squared
    )
    r_unit_value_factorized = (
        squareclass_fraction * z_unit_factor / (first + second * z) ** 2
    )
    s_unit_value_factorized = (
        squareclass_fraction * z_unit_factor / (first - second * z) ** 2
    )
    b_term_minus_factor = (
        5 * first_sq * z * z
        - 4 * first_sq * z
        + first_sq
        - 2 * first * second * z**3
        - 2 * first * second * z
        + second_sq * z**4
        + 4 * second_sq * z**3
        + 5 * second_sq * z * z
    )
    b_term_plus_factor = (
        5 * first_sq * z * z
        - 4 * first_sq * z
        + first_sq
        + 2 * first * second * z**3
        + 2 * first * second * z
        + second_sq * z**4
        + 4 * second_sq * z**3
        + 5 * second_sq * z * z
    )
    b_term_factorized = (
        squareclass_fraction
        * squareclass_fraction
        * b_term_minus_factor
        * b_term_plus_factor
        / denominator_fourth
    )
    r_lambda_value_factorized = (
        squareclass_fraction * b_term_minus_factor / denominator_squared
    )
    s_lambda_value_factorized = (
        squareclass_fraction * b_term_plus_factor / denominator_squared
    )
    b_minus_lambda_sq_a_factorized = (
        lambda_squared_minus_one_factorized
        * lambda_squared_minus_product_squared_factorized
    )
    identity_terms = pair.condition.identity_terms
    member_factorization_holds = (
        r_unit_value_factorized == pair.r * pair.r + 1
        and s_unit_value_factorized == pair.s * pair.s + 1
        and r_lambda_value_factorized
        == pair.r * pair.r + pair.lambda_ratio * pair.lambda_ratio
        and s_lambda_value_factorized
        == pair.s * pair.s + pair.lambda_ratio * pair.lambda_ratio
        and r_unit_value_factorized * s_unit_value_factorized == identity_terms.a_term
        and r_lambda_value_factorized * s_lambda_value_factorized
        == identity_terms.b_term
    )
    factorization_holds = (
        pair.lambda_ratio == lambda_numerator / denominator_product
        and pair.product == product_numerator / denominator_product
        and lambda_minus_product_factorized == pair.lambda_ratio - pair.product
        and lambda_plus_product_factorized == pair.lambda_ratio + pair.product
        and lambda_squared_minus_product_squared_factorized
        == pair.lambda_ratio * pair.lambda_ratio - pair.product * pair.product
        and lambda_squared_minus_one_factorized
        == pair.lambda_ratio * pair.lambda_ratio - 1
        and a_term_factorized == identity_terms.a_term
        and b_term_factorized == identity_terms.b_term
        and b_minus_lambda_sq_a_factorized == identity_terms.b_minus_lambda_sq_a
        and member_factorization_holds
    )
    return InverseGaussianAbsorptionPairTerms(
        pair=pair,
        identity_terms=identity_terms,
        denominator_product=denominator_product,
        lambda_numerator=lambda_numerator,
        product_numerator=product_numerator,
        lambda_minus_product_left_factor=lambda_minus_left,
        lambda_minus_product_right_factor=lambda_minus_right,
        lambda_minus_product_factorized=lambda_minus_product_factorized,
        lambda_plus_product_z_factor=lambda_plus_z_factor,
        lambda_plus_product_factorized=lambda_plus_product_factorized,
        lambda_squared_minus_product_squared_factorized=(
            lambda_squared_minus_product_squared_factorized
        ),
        lambda_squared_minus_one_extra_factor=lambda_squared_minus_one_extra,
        lambda_squared_minus_one_factorized=lambda_squared_minus_one_factorized,
        r_unit_value_factorized=r_unit_value_factorized,
        s_unit_value_factorized=s_unit_value_factorized,
        r_lambda_value_factorized=r_lambda_value_factorized,
        s_lambda_value_factorized=s_lambda_value_factorized,
        a_term_factorized=a_term_factorized,
        b_term_minus_factor=b_term_minus_factor,
        b_term_plus_factor=b_term_plus_factor,
        b_term_factorized=b_term_factorized,
        b_minus_lambda_sq_a_factorized=b_minus_lambda_sq_a_factorized,
        member_factorization_holds=member_factorization_holds,
        factorization_holds=factorization_holds,
    )


def inverse_gaussian_centerline_shadow_obstruction(
    *,
    absorbed: Fraction | int,
    squareclass: int,
    r_branch: str,
    s_branch: str,
) -> InverseGaussianCenterlineShadowObstruction:
    """Detect the unit-square obstruction for a Gaussian centerline shadow."""
    terms = inverse_gaussian_absorption_pair_terms(
        absorbed=absorbed,
        squareclass=squareclass,
        r_branch=r_branch,
        s_branch=s_branch,
    )
    absorbed_unit_value = terms.pair.absorbed * terms.pair.absorbed + 1
    absorbed_unit_value_is_square = _is_rational_square(absorbed_unit_value)
    squareclass_is_trivial = _rational_squareclass(Fraction(squareclass))[0] == 1
    r_unit_squareclass = _rational_squareclass(terms.r_unit_value_factorized)[0]
    s_unit_squareclass = _rational_squareclass(terms.s_unit_value_factorized)[0]
    unit_squareclass_obstruction = (
        absorbed_unit_value_is_square
        and not squareclass_is_trivial
        and r_unit_squareclass == squareclass
        and s_unit_squareclass == squareclass
    )
    true_member_pair_blocked = (
        not _is_rational_square(terms.r_unit_value_factorized)
        or not _is_rational_square(terms.s_unit_value_factorized)
    )
    if unit_squareclass_obstruction:
        obstruction_reason = "nontrivial-squareclass-on-unit-terms"
    elif true_member_pair_blocked:
        obstruction_reason = "unit-terms-not-square"
    else:
        obstruction_reason = None
    return InverseGaussianCenterlineShadowObstruction(
        terms=terms,
        absorbed_unit_value=absorbed_unit_value,
        absorbed_unit_value_is_square=absorbed_unit_value_is_square,
        squareclass_is_trivial=squareclass_is_trivial,
        r_unit_squareclass=r_unit_squareclass,
        s_unit_squareclass=s_unit_squareclass,
        unit_squareclass_obstruction=unit_squareclass_obstruction,
        true_member_pair_blocked=true_member_pair_blocked,
        obstruction_reason=obstruction_reason,
    )


def is_rational_ratio_member(lambda_ratio: Fraction | int, r: Fraction | int) -> bool:
    """Return True iff ``r`` lies in ``R_lambda``.

    ``R_lambda`` is the set of positive rational ratios satisfying both:

        r^2 + 1        is a rational square
        r^2 + lambda^2 is a rational square
    """
    lam = _as_fraction(lambda_ratio)
    ratio = _as_fraction(r)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", ratio)
    return _is_rational_square(ratio * ratio + 1) and _is_rational_square(
        ratio * ratio + lam * lam
    )


def is_pythagorean_leg_ratio(ratio: Fraction | int) -> bool:
    """Return True iff ``ratio`` has rational distance to a unit leg."""
    value = _as_fraction(ratio)
    _validate_positive("ratio", value)
    return _is_rational_square(value * value + 1)


def positive_rational_ratios(
    max_numerator: int,
    max_denominator: int,
) -> tuple[Fraction, ...]:
    """Return reduced positive rationals with bounded numerator and denominator."""
    if max_numerator < 1:
        raise ValueError("max_numerator must be positive")
    if max_denominator < 1:
        raise ValueError("max_denominator must be positive")
    ratios = {
        Fraction(numerator, denominator)
        for numerator in range(1, max_numerator + 1)
        for denominator in range(1, max_denominator + 1)
    }
    return tuple(sorted(ratios))


def leg_ratio_squareclass(ratio: Fraction | int) -> LegRatioSquareclass:
    """Explain the ``z^2+1`` square test by its rational squareclass.

    This is a diagnostic helper, not a high-throughput sieve.
    """
    value = _as_fraction(ratio)
    _validate_positive("ratio", value)
    square_candidate = value * value + 1
    squarefree, primes = _rational_squareclass(square_candidate)
    return LegRatioSquareclass(
        ratio=value,
        value=square_candidate,
        is_square=squarefree == 1,
        squarefree_part=squarefree,
        squareclass_primes=primes,
        three_mod_four_primes=tuple(prime for prime in primes if prime % 4 == 3),
    )


def pythagorean_leg_ratios(max_m: int) -> tuple[Fraction, ...]:
    """Generate primitive Pythagorean leg ratios from Euclid parameters ``m <= max_m``.

    Both leg orientations are included.  The bound is on the Euclid parameter,
    not on denominator, numerator, or hypotenuse.
    """
    if max_m < 2:
        return ()
    ratios: list[Fraction] = []
    seen: set[Fraction] = set()
    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue
            if _gcd(m, n) != 1:
                continue
            legs = (m * m - n * n, 2 * m * n)
            for numerator, denominator in (legs, (legs[1], legs[0])):
                ratio = Fraction(numerator, denominator)
                if ratio not in seen:
                    seen.add(ratio)
                    ratios.append(ratio)
    return tuple(ratios)


def pythagorean_leg_ratio_from_param(param: PythagoreanLegParam) -> Fraction:
    """Return the rational leg ratio represented by Euclid parameters."""
    return param.ratio()


def reciprocal_ratio(lambda_ratio: Fraction | int, r: Fraction | int) -> Fraction:
    """Return the reciprocal-orbit mate ``lambda / r``."""
    lam = _as_fraction(lambda_ratio)
    ratio = _as_fraction(r)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", ratio)
    return lam / ratio


def _targets(lambda_ratio: Fraction) -> tuple[tuple[Fraction, str], ...]:
    diff = abs(lambda_ratio - 1)
    targets: list[tuple[Fraction, str]] = [(lambda_ratio + 1, REL_SUM_AB)]
    if diff != 0:
        targets.append((diff, REL_SUM_DIFF))
    return tuple(targets)


def find_rational_ratio_hits(
    lambda_ratio: Fraction | int,
    ratios: tuple[Fraction, ...],
    *,
    include_centerline: bool = False,
) -> tuple[RationalRatioHit, ...]:
    """Check full-plane closure for an arbitrary rational ``A/B`` ratio."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    sorted_ratios = tuple(sorted(set(ratios)))
    hits: list[RationalRatioHit] = []

    sum_targets = _targets(lam)
    diff_targets: list[tuple[Fraction, str]] = [(lam + 1, REL_DIFF_AB)]
    diff = abs(lam - 1)
    if diff != 0:
        diff_targets.append((diff, REL_DIFF_DIFF))

    for i, r1 in enumerate(sorted_ratios):
        _validate_positive("r", r1)
        for j in range(i, len(sorted_ratios)):
            r2 = sorted_ratios[j]
            _validate_positive("r", r2)
            centerline = r1 == r2
            if centerline and not include_centerline:
                continue
            for target, relation in sum_targets:
                if r1 + r2 == target:
                    hits.append(RationalRatioHit(r1, r2, relation, centerline))
            if centerline:
                continue
            ratio_diff = abs(r2 - r1)
            for target, relation in diff_targets:
                if ratio_diff == target:
                    hits.append(RationalRatioHit(r1, r2, relation, False))
    return tuple(sorted(hits))


def rational_ratio_hit_product_diagnostics(
    lambda_ratio: Fraction | int,
    ratios: tuple[Fraction, ...],
    *,
    include_centerline: bool = False,
) -> tuple[RationalRatioHitProductDiagnostic, ...]:
    """Annotate ratio-level closure hits with the product target ``p=λ``.

    This is a diagnostic for the ``R_λ`` translation theorem.  It does not
    prove that every possible closure hit has ``p=λ``; it only reports whether
    the hits found in the supplied finite ratio pool are reciprocal pairs.
    """
    lam = _as_fraction(lambda_ratio)
    diagnostics: list[RationalRatioHitProductDiagnostic] = []
    for hit in find_rational_ratio_hits(
        lam,
        ratios,
        include_centerline=include_centerline,
    ):
        product = hit.r1 * hit.r2
        diagnostics.append(
            RationalRatioHitProductDiagnostic(
                lambda_ratio=lam,
                r1=hit.r1,
                r2=hit.r2,
                relation=hit.relation,
                product=product,
                product_equals_lambda=product == lam,
                reciprocal_pair=hit.r2 == reciprocal_ratio(lam, hit.r1),
                true_member_pair=is_rational_ratio_member(lam, hit.r1)
                and is_rational_ratio_member(lam, hit.r2),
            )
        )
    return tuple(sorted(diagnostics))


def sum_ab_point_from_slopes(
    slope1: Fraction | int,
    slope2: Fraction | int,
) -> SumAbSlopePoint | None:
    """Return the ``sum=A+B`` rational-ratio candidate from scaled slopes.

    If ``x = r/lambda`` and ``y = s/lambda``, then ``r+s=lambda+1`` forces
    ``lambda = 1 / (x+y-1)``.  True membership additionally requires both
    ``x,y`` and ``lambda*x, lambda*y`` to be Pythagorean leg ratios.
    """
    x = _as_fraction(slope1)
    y = _as_fraction(slope2)
    _validate_positive("slope1", x)
    _validate_positive("slope2", y)
    denominator = x + y - 1
    if denominator <= 0:
        return None
    lam = 1 / denominator
    r1 = lam * x
    r2 = lam * y
    return SumAbSlopePoint(
        lambda_ratio=lam,
        r1=r1,
        r2=r2,
        slope1=x,
        slope2=y,
        product=r1 * r2,
        reciprocal_pair=r1 * r2 == lam,
        true_member_pair=is_rational_ratio_member(lam, r1)
        and is_rational_ratio_member(lam, r2),
    )


def sum_ab_product_square_condition_from_slopes(
    slope1: Fraction | int,
    slope2: Fraction | int,
) -> ClosureProductSquareConditions | None:
    """Return the ``sum=A+B`` product-square ledger induced by scaled slopes."""
    point = sum_ab_point_from_slopes(slope1, slope2)
    if point is None:
        return None
    return closure_product_square_conditions(
        point.lambda_ratio,
        point.lambda_ratio + 1,
        point.product,
        REL_SUM_AB,
    )


def sum_ab_slope_obstruction(
    slope1: Fraction | int,
    slope2: Fraction | int,
) -> SumAbSlopeObstruction | None:
    """Return four-term squareclass diagnostics for a ``sum=A+B`` slope pair."""
    return _sum_ab_slope_obstruction_with_squareclass_cache(slope1, slope2, {})


def sum_ab_three_pass_mobius_model(
    slope: Fraction | int,
    scaled_term: Fraction | int,
) -> SumAbThreePassMobiusModel:
    """Return the Möbius equation model for one ``sum=A+B`` three-pass branch.

    This helper parameterizes the case where ``x`` and ``r=lambda*x`` are the
    two known passing terms.  It does not assume that the reconstructed ``y``
    passes; the returned squareclasses say exactly which terms do.
    """
    x = _as_fraction(slope)
    r = _as_fraction(scaled_term)
    _validate_positive("slope", x)
    _validate_positive("scaled_term", r)
    lam = r / x
    y = 1 - x + x / r
    s = lam * y
    if y <= 0 or s <= 0:
        raise ValueError("reconstructed terms must be positive")
    slope_diag = leg_ratio_squareclass(x)
    other_slope_diag = leg_ratio_squareclass(y)
    scaled_diag = leg_ratio_squareclass(r)
    failed_diag = leg_ratio_squareclass(s)
    return SumAbThreePassMobiusModel(
        lambda_ratio=lam,
        slope=x,
        other_slope=y,
        scaled_term=r,
        failed_scaled_term=s,
        slope_squareclass=slope_diag.squarefree_part,
        other_slope_squareclass=other_slope_diag.squarefree_part,
        scaled_term_squareclass=scaled_diag.squarefree_part,
        failed_squareclass=failed_diag.squarefree_part,
    )


def _square_equation_for_leg_ratio(ratio: Fraction) -> tuple[Fraction, Fraction | None]:
    value = ratio * ratio + 1
    root = _rational_sqrt(value)
    return value, root * root if root is not None else None


def _integer_square_equation_for_leg_ratio(ratio: Fraction) -> tuple[int, int, int | None]:
    numerator = ratio.numerator
    denominator = ratio.denominator
    square_sum = numerator * numerator + denominator * denominator
    root = isqrt(square_sum)
    hypotenuse = root if root * root == square_sum else None
    return numerator, denominator, hypotenuse


def _integer_square_equation_from_terms(
    terms: tuple[int, int],
) -> tuple[int, int, int | None]:
    numerator, denominator = terms
    square_sum = numerator * numerator + denominator * denominator
    root = isqrt(square_sum)
    hypotenuse = root if root * root == square_sum else None
    return numerator, denominator, hypotenuse


def _hypotenuse_factor_pair(
    equation: tuple[int, int, int | None],
) -> tuple[int, int] | None:
    _, denominator, hypotenuse = equation
    if hypotenuse is None:
        return None
    return hypotenuse - denominator, hypotenuse + denominator


def _factor_pair_gcd(pair: tuple[int, int] | None) -> int | None:
    if pair is None:
        return None
    left, right = pair
    return _gcd(left, right)


def _reduced_factor_pair(pair: tuple[int, int] | None) -> tuple[int, int] | None:
    common = _factor_pair_gcd(pair)
    if pair is None or common is None:
        return None
    left, right = pair
    return left // common, right // common


def _factor_pair_square_roots(pair: tuple[int, int] | None) -> tuple[int, int] | None:
    if pair is None:
        return None
    left, right = pair
    left_root = isqrt(left)
    right_root = isqrt(right)
    if left_root * left_root != left or right_root * right_root != right:
        return None
    return left_root, right_root


def _factor_pair_parameterization(
    common: int | None,
    square_roots: tuple[int, int] | None,
) -> tuple[int, int, int] | None:
    if common is None or square_roots is None:
        return None
    return common, square_roots[0], square_roots[1]


def _parameterized_shared_numerator(
    parameterization: tuple[int, int, int] | None,
) -> int | None:
    if parameterization is None:
        return None
    common, left_root, right_root = parameterization
    return common * left_root * right_root


def _parameterized_denominator(
    parameterization: tuple[int, int, int] | None,
) -> int | None:
    if parameterization is None:
        return None
    common, left_root, right_root = parameterization
    return common * (right_root * right_root - left_root * left_root) // 2


def _parameterized_hypotenuse(
    parameterization: tuple[int, int, int] | None,
) -> int | None:
    if parameterization is None:
        return None
    common, left_root, right_root = parameterization
    return common * (right_root * right_root + left_root * left_root) // 2


def _sum_ab_mobius_polynomial_terms_from_legs(
    slope_terms: tuple[int, int],
    scaled_term_terms: tuple[int, int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return unreduced integer numerator/denominator terms for ``y`` and ``s``.

    For ``x=a/b`` and ``r=c/d``:

        y = 1 - x + x/r = (bc - ac + ad) / bc
        s = 1 - r + r/x = (ad - ac + bc) / ad

    Keeping these unreduced terms preserves the polynomial shape needed for
    later Euclid-parameter expansion.
    """
    a, b = slope_terms
    c, d = scaled_term_terms
    return (
        (b * c - a * c + a * d, b * c),
        (a * d - a * c + b * c, a * d),
    )


def sum_ab_three_pass_mobius_model_from_params(
    slope: PythagoreanLegParam,
    scaled_term: PythagoreanLegParam,
) -> SumAbThreePassEuclidModel:
    """Build the three-pass Möbius model from two Euclid-parameterized legs."""
    model = sum_ab_three_pass_mobius_model(slope.ratio(), scaled_term.ratio())
    other_terms, failed_terms = _sum_ab_mobius_polynomial_terms_from_legs(
        slope.leg_terms(),
        scaled_term.leg_terms(),
    )
    return SumAbThreePassEuclidModel(
        slope_param=slope,
        scaled_term_param=scaled_term,
        mobius=model,
        other_slope_square_equation=_square_equation_for_leg_ratio(model.other_slope),
        failed_square_equation=_square_equation_for_leg_ratio(model.failed_scaled_term),
        other_slope_integer_equation=_integer_square_equation_for_leg_ratio(
            model.other_slope
        ),
        failed_integer_equation=_integer_square_equation_for_leg_ratio(
            model.failed_scaled_term
        ),
        other_slope_polynomial_terms=other_terms,
        failed_polynomial_terms=failed_terms,
        other_slope_polynomial_equation=_integer_square_equation_from_terms(other_terms),
        failed_polynomial_equation=_integer_square_equation_from_terms(failed_terms),
    )


def sum_ab_euclid_orientation_equations(
    *,
    slope_m: int,
    slope_n: int,
    scaled_term_m: int,
    scaled_term_n: int,
) -> tuple[SumAbEuclidOrientationEquation, ...]:
    """Expand the four odd/even Euclid orientation cases for ``sum=A+B``.

    This is an equationization helper: it records the unreduced integer square
    equations after substituting two Euclid-parameterized leg ratios.  It does
    not assert that any branch is impossible.
    """
    cases: list[SumAbEuclidOrientationEquation] = []
    for slope_orientation in ("odd", "even"):
        slope_param = PythagoreanLegParam(slope_m, slope_n, slope_orientation)
        slope_terms = slope_param.leg_terms()
        for scaled_term_orientation in ("odd", "even"):
            scaled_term_param = PythagoreanLegParam(
                scaled_term_m,
                scaled_term_n,
                scaled_term_orientation,
            )
            scaled_term_terms = scaled_term_param.leg_terms()
            other_terms, failed_terms = _sum_ab_mobius_polynomial_terms_from_legs(
                slope_terms,
                scaled_term_terms,
            )
            cases.append(
                SumAbEuclidOrientationEquation(
                    slope_orientation=slope_orientation,
                    scaled_term_orientation=scaled_term_orientation,
                    slope_terms=slope_terms,
                    scaled_term_terms=scaled_term_terms,
                    other_slope_polynomial_equation=_integer_square_equation_from_terms(
                        other_terms
                    ),
                    failed_polynomial_equation=_integer_square_equation_from_terms(
                        failed_terms
                    ),
                )
            )
    return tuple(cases)


def sum_ab_same_orientation_shared_leg_terms(
    slope: PythagoreanLegParam,
    scaled_term: PythagoreanLegParam,
) -> SumAbSameOrientationSharedLegTerms:
    """Return the shared numerator and denominator square equations.

    This helper is only for same-orientation cases.  It exposes the structure
    ``N^2 + (bc)^2`` and ``N^2 + (ad)^2`` without claiming either equation is
    impossible.
    """
    if slope.orientation != scaled_term.orientation:
        raise ValueError("same-orientation shared-leg terms require matching orientations")
    slope_terms = slope.leg_terms()
    scaled_term_terms = scaled_term.leg_terms()
    other_terms, failed_terms = _sum_ab_mobius_polynomial_terms_from_legs(
        slope_terms,
        scaled_term_terms,
    )
    shared_numerator, other_denominator = other_terms
    failed_numerator, failed_denominator = failed_terms
    if shared_numerator != failed_numerator:
        raise ValueError("sum=A+B polynomial terms should share a numerator")
    return SumAbSameOrientationSharedLegTerms(
        orientation=slope.orientation,
        slope_terms=slope_terms,
        scaled_term_terms=scaled_term_terms,
        shared_numerator=shared_numerator,
        other_denominator=other_denominator,
        failed_denominator=failed_denominator,
        other_square_equation=_integer_square_equation_from_terms(other_terms),
        failed_square_equation=_integer_square_equation_from_terms(failed_terms),
    )


def sum_ab_same_orientation_denominator_factorization(
    *,
    slope_m: int,
    slope_n: int,
    scaled_term_m: int,
    scaled_term_n: int,
    orientation: str,
) -> SumAbSameOrientationDenominatorFactorization:
    """Return the ``P±Q`` factors for same-orientation Euclid denominators."""
    slope = PythagoreanLegParam(slope_m, slope_n, orientation)
    scaled_term = PythagoreanLegParam(scaled_term_m, scaled_term_n, orientation)
    shared_terms = sum_ab_same_orientation_shared_leg_terms(slope, scaled_term)
    m = slope_m
    n = slope_n
    u = scaled_term_m
    v = scaled_term_n
    nu_minus_mv = n * u - m * v
    difference_sign = 2 if orientation == "odd" else -2
    first_difference_factor = m * u + n * v
    first_sum_factor = m * u - n * v
    second_sum_factor = m * v + n * u
    slope_numerator, slope_denominator = shared_terms.slope_terms
    scaled_numerator, scaled_denominator = shared_terms.scaled_term_terms
    return SumAbSameOrientationDenominatorFactorization(
        orientation=orientation,
        shared_numerator=shared_terms.shared_numerator,
        other_denominator=shared_terms.other_denominator,
        failed_denominator=shared_terms.failed_denominator,
        denominator_difference=shared_terms.other_denominator
        - shared_terms.failed_denominator,
        denominator_sum=shared_terms.other_denominator + shared_terms.failed_denominator,
        shared_minus_other_denominator=shared_terms.shared_numerator
        - shared_terms.other_denominator,
        shared_minus_failed_denominator=shared_terms.shared_numerator
        - shared_terms.failed_denominator,
        nu_minus_mv=nu_minus_mv,
        difference_factorization=(
            difference_sign,
            first_difference_factor,
            nu_minus_mv,
        ),
        sum_factorization=(2, first_sum_factor, second_sum_factor),
        shared_minus_other_factorization=(
            slope_numerator,
            scaled_denominator - scaled_numerator,
        ),
        shared_minus_failed_factorization=(
            scaled_numerator,
            slope_denominator - slope_numerator,
        ),
    )


def sum_ab_same_orientation_cross_gcd_terms(
    slope: PythagoreanLegParam,
    scaled_term: PythagoreanLegParam,
) -> SumAbSameOrientationCrossGcdTerms:
    """Expose gcd structure forced by the cross-products ``P=bc`` and ``Q=ad``.

    For primitive leg ratios ``gcd(a,b)=gcd(c,d)=1``, the denominator gcd is:

        gcd(bc, ad) = gcd(a, c) * gcd(b, d)

    The helper records both sides instead of assuming primitivity silently.
    """
    shared_terms = sum_ab_same_orientation_shared_leg_terms(slope, scaled_term)
    a, b = shared_terms.slope_terms
    c, d = shared_terms.scaled_term_terms
    m = slope.m
    n = slope.n
    u = scaled_term.m
    v = scaled_term.n
    nu_minus_mv = n * u - m * v
    difference_sign = 2 if slope.orientation == "odd" else -2
    return SumAbSameOrientationCrossGcdTerms(
        orientation=shared_terms.orientation,
        slope_terms=shared_terms.slope_terms,
        scaled_term_terms=shared_terms.scaled_term_terms,
        other_denominator=shared_terms.other_denominator,
        failed_denominator=shared_terms.failed_denominator,
        denominator_difference=shared_terms.other_denominator
        - shared_terms.failed_denominator,
        denominator_sum=shared_terms.other_denominator + shared_terms.failed_denominator,
        gcd_a_b=_gcd(a, b),
        gcd_c_d=_gcd(c, d),
        gcd_a_c=_gcd(a, c),
        gcd_a_d=_gcd(a, d),
        gcd_b_c=_gcd(b, c),
        gcd_b_d=_gcd(b, d),
        gcd_p_q=_gcd(shared_terms.other_denominator, shared_terms.failed_denominator),
        difference_factorization=(
            difference_sign,
            m * u + n * v,
            nu_minus_mv,
        ),
        sum_factorization=(2, m * u - n * v, m * v + n * u),
    )


def sum_ab_same_orientation_both_pass_residue_summary(
    modulus: int,
    *,
    example_limit: int = 5,
) -> SumAbSameOrientationBothPassResidueSummary:
    """Count same-orientation noncenter both-pass residue classes modulo ``modulus``.

    The scan keeps primitive residue classes modulo ``modulus`` for both Euclid
    parameter pairs and, when the modulus is even, the usual opposite-parity
    necessary condition.  A noncenter survivor is a class with ``P != Q`` where
    both ``N^2+P^2`` and ``N^2+Q^2`` are square residues.
    """
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    square_residues = {value * value % modulus for value in range(modulus)}
    total_by_orientation: dict[str, int] = {}
    p_equals_q_by_orientation: dict[str, int] = {}
    survivor_by_orientation: dict[str, int] = {}
    examples_by_orientation: dict[str, tuple[tuple[int, ...], ...]] = {}

    for orientation in ("odd", "even"):
        total = 0
        p_equals_q = 0
        survivors = 0
        examples: list[tuple[int, ...]] = []
        for m in range(modulus):
            for n in range(modulus):
                if _gcd(_gcd(m, n), modulus) != 1:
                    continue
                if modulus % 2 == 0 and (m - n) % 2 == 0:
                    continue
                for u in range(modulus):
                    for v in range(modulus):
                        if _gcd(_gcd(u, v), modulus) != 1:
                            continue
                        if modulus % 2 == 0 and (u - v) % 2 == 0:
                            continue
                        total += 1
                        if orientation == "odd":
                            slope_numerator = (m * m - n * n) % modulus
                            slope_denominator = (2 * m * n) % modulus
                            scaled_numerator = (u * u - v * v) % modulus
                            scaled_denominator = (2 * u * v) % modulus
                        else:
                            slope_numerator = (2 * m * n) % modulus
                            slope_denominator = (m * m - n * n) % modulus
                            scaled_numerator = (2 * u * v) % modulus
                            scaled_denominator = (u * u - v * v) % modulus
                        other_denominator = slope_denominator * scaled_numerator % modulus
                        failed_denominator = slope_numerator * scaled_denominator % modulus
                        shared_numerator = (
                            other_denominator
                            - slope_numerator * scaled_numerator
                            + failed_denominator
                        ) % modulus
                        if (other_denominator - failed_denominator) % modulus == 0:
                            p_equals_q += 1
                            continue
                        other_square = (
                            shared_numerator * shared_numerator
                            + other_denominator * other_denominator
                        ) % modulus
                        failed_square = (
                            shared_numerator * shared_numerator
                            + failed_denominator * failed_denominator
                        ) % modulus
                        if (
                            other_square in square_residues
                            and failed_square in square_residues
                        ):
                            survivors += 1
                            if len(examples) < example_limit:
                                examples.append(
                                    (
                                        m,
                                        n,
                                        u,
                                        v,
                                        shared_numerator,
                                        other_denominator,
                                        failed_denominator,
                                    )
                                )
        total_by_orientation[orientation] = total
        p_equals_q_by_orientation[orientation] = p_equals_q
        survivor_by_orientation[orientation] = survivors
        examples_by_orientation[orientation] = tuple(examples)

    return SumAbSameOrientationBothPassResidueSummary(
        modulus=modulus,
        total_classes_by_orientation=total_by_orientation,
        p_equals_q_count_by_orientation=p_equals_q_by_orientation,
        noncenter_survivor_count_by_orientation=survivor_by_orientation,
        noncenter_examples_by_orientation=examples_by_orientation,
    )


def _same_orientation_residue_terms(
    *,
    modulus: int,
    orientation: str,
    residue: tuple[int, int, int, int],
) -> tuple[int, int, int]:
    m, n, u, v = residue
    if orientation == "odd":
        slope_numerator = (m * m - n * n) % modulus
        slope_denominator = (2 * m * n) % modulus
        scaled_numerator = (u * u - v * v) % modulus
        scaled_denominator = (2 * u * v) % modulus
    elif orientation == "even":
        slope_numerator = (2 * m * n) % modulus
        slope_denominator = (m * m - n * n) % modulus
        scaled_numerator = (2 * u * v) % modulus
        scaled_denominator = (u * u - v * v) % modulus
    else:
        raise ValueError("orientation must be 'odd' or 'even'")
    other_denominator = slope_denominator * scaled_numerator % modulus
    failed_denominator = slope_numerator * scaled_denominator % modulus
    shared_numerator = (
        other_denominator - slope_numerator * scaled_numerator + failed_denominator
    ) % modulus
    return shared_numerator, other_denominator, failed_denominator


def _same_orientation_integer_terms(
    *,
    orientation: str,
    residue: tuple[int, int, int, int],
) -> tuple[int, int, int]:
    m, n, u, v = residue
    if orientation == "odd":
        slope_numerator = m * m - n * n
        slope_denominator = 2 * m * n
        scaled_numerator = u * u - v * v
        scaled_denominator = 2 * u * v
    elif orientation == "even":
        slope_numerator = 2 * m * n
        slope_denominator = m * m - n * n
        scaled_numerator = 2 * u * v
        scaled_denominator = u * u - v * v
    else:
        raise ValueError("orientation must be 'odd' or 'even'")
    other_denominator = slope_denominator * scaled_numerator
    failed_denominator = slope_numerator * scaled_denominator
    shared_numerator = (
        other_denominator - slope_numerator * scaled_numerator + failed_denominator
    )
    return shared_numerator, other_denominator, failed_denominator


def _integer_valuation(value: int, prime: int) -> int:
    if prime <= 1:
        raise ValueError("prime must be greater than 1")
    if value == 0:
        raise ValueError("valuation of zero is not finite")
    remaining = abs(value)
    exponent = 0
    while remaining % prime == 0:
        exponent += 1
        remaining //= prime
    return exponent


def _integer_valuation_or_zero_sentinel(value: int, prime: int) -> int:
    if value == 0:
        return 99
    return _integer_valuation(value, prime)


def sum_ab_same_orientation_both_pass_lift_summary(
    *,
    modulus: int,
    orientation: str,
    residue: tuple[int, int, int, int],
    prime: int,
    example_limit: int = 5,
) -> SumAbSameOrientationBothPassLiftSummary:
    """Count noncenter both-pass lifts of one residue class to ``prime*modulus``."""
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    if prime <= 1:
        raise ValueError("prime must be greater than 1")
    if len(residue) != 4:
        raise ValueError("residue must contain four entries")
    next_modulus = modulus * prime
    square_residues = {value * value % next_modulus for value in range(next_modulus)}
    lift_count = 0
    valuation_counts: dict[int, int] = {}
    examples: list[tuple[int, ...]] = []
    m, n, u, v = residue
    for dm in range(prime):
        for dn in range(prime):
            for du in range(prime):
                for dv in range(prime):
                    lifted = (
                        m + modulus * dm,
                        n + modulus * dn,
                        u + modulus * du,
                        v + modulus * dv,
                    )
                    if _gcd(_gcd(lifted[0], lifted[1]), next_modulus) != 1:
                        continue
                    if _gcd(_gcd(lifted[2], lifted[3]), next_modulus) != 1:
                        continue
                    if next_modulus % 2 == 0 and (lifted[0] - lifted[1]) % 2 == 0:
                        continue
                    if next_modulus % 2 == 0 and (lifted[2] - lifted[3]) % 2 == 0:
                        continue
                    shared_numerator, other_denominator, failed_denominator = (
                        _same_orientation_residue_terms(
                            modulus=next_modulus,
                            orientation=orientation,
                            residue=lifted,
                        )
                    )
                    difference = (other_denominator - failed_denominator) % next_modulus
                    if difference == 0:
                        continue
                    other_square = (
                        shared_numerator * shared_numerator
                        + other_denominator * other_denominator
                    ) % next_modulus
                    failed_square = (
                        shared_numerator * shared_numerator
                        + failed_denominator * failed_denominator
                    ) % next_modulus
                    if (
                        other_square not in square_residues
                        or failed_square not in square_residues
                    ):
                        continue
                    lift_count += 1
                    valuation = _integer_valuation(difference, prime)
                    valuation_counts[valuation] = valuation_counts.get(valuation, 0) + 1
                    if len(examples) < example_limit:
                        examples.append(
                            (
                                lifted[0],
                                lifted[1],
                                lifted[2],
                                lifted[3],
                                shared_numerator,
                                other_denominator,
                                failed_denominator,
                            )
                        )
    return SumAbSameOrientationBothPassLiftSummary(
        modulus=modulus,
        next_modulus=next_modulus,
        orientation=orientation,
        residue=residue,
        prime=prime,
        lift_count=lift_count,
        diff_valuation_counts=dict(sorted(valuation_counts.items())),
        examples=tuple(examples),
    )


def sum_ab_same_orientation_difference_factor_valuation_summary(
    *,
    modulus: int,
    orientation: str,
    prime: int,
) -> SumAbSameOrientationDifferenceFactorValuationSummary:
    """Summarize which ``P-Q`` factor carries ``prime`` among survivors."""
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    if prime <= 1:
        raise ValueError("prime must be greater than 1")
    square_residues = {value * value % modulus for value in range(modulus)}
    pattern_counts: dict[tuple[int, int, int], int] = {}
    examples: dict[tuple[int, int, int], tuple[int, ...]] = {}
    total = 0
    for m in range(modulus):
        for n in range(modulus):
            if _gcd(_gcd(m, n), modulus) != 1:
                continue
            if modulus % 2 == 0 and (m - n) % 2 == 0:
                continue
            for u in range(modulus):
                for v in range(modulus):
                    if _gcd(_gcd(u, v), modulus) != 1:
                        continue
                    if modulus % 2 == 0 and (u - v) % 2 == 0:
                        continue
                    shared_numerator, other_denominator, failed_denominator = (
                        _same_orientation_residue_terms(
                            modulus=modulus,
                            orientation=orientation,
                            residue=(m, n, u, v),
                        )
                    )
                    difference = (other_denominator - failed_denominator) % modulus
                    if difference == 0:
                        continue
                    other_square = (
                        shared_numerator * shared_numerator
                        + other_denominator * other_denominator
                    ) % modulus
                    failed_square = (
                        shared_numerator * shared_numerator
                        + failed_denominator * failed_denominator
                    ) % modulus
                    if (
                        other_square not in square_residues
                        or failed_square not in square_residues
                    ):
                        continue
                    first_factor = m * u + n * v
                    second_factor = n * u - m * v
                    pattern = (
                        _integer_valuation(first_factor, prime),
                        _integer_valuation(second_factor, prime),
                        _integer_valuation(difference, prime),
                    )
                    total += 1
                    pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
                    examples.setdefault(
                        pattern,
                        (
                            m,
                            n,
                            u,
                            v,
                            shared_numerator,
                            other_denominator,
                            failed_denominator,
                            first_factor,
                            second_factor,
                        ),
                    )
    return SumAbSameOrientationDifferenceFactorValuationSummary(
        modulus=modulus,
        orientation=orientation,
        prime=prime,
        total_survivors=total,
        pattern_counts=dict(sorted(pattern_counts.items())),
        examples=dict(sorted(examples.items())),
    )


def sum_ab_same_orientation_combined_valuation_summary(
    *,
    modulus: int,
    orientation: str,
    prime: int,
    top_limit: int = 20,
) -> SumAbSameOrientationCombinedValuationSummary:
    """Summarize combined ``P±Q`` and ``N-P,N-Q`` valuations for survivors.

    Survivor membership is a residue condition modulo ``modulus``.  Valuations
    are then taken on the corresponding integer polynomial representatives, so
    a residue that is zero modulo ``modulus`` is not mistaken for literal zero.
    The sentinel value ``99`` records literal zero offsets in a pattern.
    """
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    if prime <= 1:
        raise ValueError("prime must be greater than 1")
    square_residues = {value * value % modulus for value in range(modulus)}
    pattern_counts: Counter[tuple[int, ...]] = Counter()
    examples: dict[tuple[int, ...], tuple[int, ...]] = {}
    total = 0
    for m in range(modulus):
        for n in range(modulus):
            if _gcd(_gcd(m, n), modulus) != 1:
                continue
            if modulus % 2 == 0 and (m - n) % 2 == 0:
                continue
            for u in range(modulus):
                for v in range(modulus):
                    if _gcd(_gcd(u, v), modulus) != 1:
                        continue
                    if modulus % 2 == 0 and (u - v) % 2 == 0:
                        continue
                    shared_numerator, other_denominator, failed_denominator = (
                        _same_orientation_residue_terms(
                            modulus=modulus,
                            orientation=orientation,
                            residue=(m, n, u, v),
                        )
                    )
                    difference = (other_denominator - failed_denominator) % modulus
                    if difference == 0:
                        continue
                    other_square = (
                        shared_numerator * shared_numerator
                        + other_denominator * other_denominator
                    ) % modulus
                    failed_square = (
                        shared_numerator * shared_numerator
                        + failed_denominator * failed_denominator
                    ) % modulus
                    if (
                        other_square not in square_residues
                        or failed_square not in square_residues
                    ):
                        continue
                    integer_n, integer_p, integer_q = _same_orientation_integer_terms(
                        orientation=orientation,
                        residue=(m, n, u, v),
                    )
                    pattern = (
                        _integer_valuation_or_zero_sentinel(m * u + n * v, prime),
                        _integer_valuation_or_zero_sentinel(n * u - m * v, prime),
                        _integer_valuation_or_zero_sentinel(m * u - n * v, prime),
                        _integer_valuation_or_zero_sentinel(m * v + n * u, prime),
                        _integer_valuation_or_zero_sentinel(integer_n - integer_p, prime),
                        _integer_valuation_or_zero_sentinel(integer_n - integer_q, prime),
                        _integer_valuation_or_zero_sentinel(integer_p - integer_q, prime),
                        _integer_valuation_or_zero_sentinel(integer_p + integer_q, prime),
                    )
                    total += 1
                    pattern_counts[pattern] += 1
                    examples.setdefault(
                        pattern,
                        (
                            m,
                            n,
                            u,
                            v,
                            integer_n,
                            integer_p,
                            integer_q,
                        ),
                    )
    top_patterns = tuple(pattern_counts.most_common(top_limit))
    return SumAbSameOrientationCombinedValuationSummary(
        modulus=modulus,
        orientation=orientation,
        prime=prime,
        total_survivors=total,
        pattern_count=len(pattern_counts),
        top_patterns=top_patterns,
        zero_offset_pattern_count=sum(
            1 for pattern in pattern_counts if 99 in pattern[4:6]
        ),
        examples=dict(sorted(examples.items())),
    )


def sum_ab_same_orientation_normalized_near_miss_summary(
    *,
    max_m: int,
    max_examples_per_bucket: int = 5,
) -> SumAbNormalizedNearMissSummary:
    """Scan bounded same-orientation three-pass near-misses by normalized ``P,Q``.

    This is a diagnostic scan, not a proof.  It only counts positive primitive
    Euclid parameter pairs where exactly one reconstructed term passes.
    """
    if max_m < 2:
        raise ValueError("max_m must be at least 2")
    if max_examples_per_bucket < 1:
        raise ValueError("max_examples_per_bucket must be positive")

    abs_difference_counts: Counter[int] = Counter()
    failing_squareclass_counts: Counter[int] = Counter()
    normalized_pair_counts: Counter[tuple[tuple[int, int], str]] = Counter()
    examples: dict[int, list[SumAbNormalizedNearMissExample]] = {}
    squareclass_examples: dict[int, list[SumAbNormalizedNearMissExample]] = {}
    canonical_triples: dict[int, set[tuple[int, int, int]]] = {}
    total = 0

    primitive_params = tuple(_primitive_euclid_params(max_m))
    for orientation in ("odd", "even"):
        for slope_m, slope_n in primitive_params:
            slope = PythagoreanLegParam(slope_m, slope_n, orientation)
            for scaled_m, scaled_n in primitive_params:
                scaled = PythagoreanLegParam(scaled_m, scaled_n, orientation)
                shared_terms = sum_ab_same_orientation_shared_leg_terms(slope, scaled)
                if shared_terms.shared_numerator <= 0:
                    continue
                other_passes = shared_terms.other_square_equation[2] is not None
                failed_passes = shared_terms.failed_square_equation[2] is not None
                if other_passes == failed_passes:
                    continue

                cross_terms = sum_ab_same_orientation_cross_gcd_terms(slope, scaled)
                normalized_pair = cross_terms.normalized_denominator_pair
                difference_over_gcd = cross_terms.denominator_difference_over_gcd
                sum_over_gcd = cross_terms.denominator_sum_over_gcd
                if (
                    normalized_pair is None
                    or difference_over_gcd is None
                    or sum_over_gcd is None
                ):
                    continue

                total += 1
                abs_difference = abs(difference_over_gcd)
                abs_difference_counts[abs_difference] += 1
                normalized_pair_counts[(normalized_pair, orientation)] += 1
                gcd_n_p_q = _gcd(
                    shared_terms.shared_numerator,
                    _gcd(shared_terms.other_denominator, shared_terms.failed_denominator),
                )
                normalized_n = shared_terms.shared_numerator // gcd_n_p_q
                normalized_p = shared_terms.other_denominator // gcd_n_p_q
                normalized_q = shared_terms.failed_denominator // gcd_n_p_q
                normalized_other_squareclass = _integer_squareclass(
                    normalized_n * normalized_n + normalized_p * normalized_p
                )
                normalized_failed_squareclass = _integer_squareclass(
                    normalized_n * normalized_n + normalized_q * normalized_q
                )
                failing_squareclass = (
                    normalized_failed_squareclass
                    if other_passes
                    else normalized_other_squareclass
                )
                failing_squareclass_counts[failing_squareclass] += 1
                bucket = examples.setdefault(abs_difference, [])
                squareclass_bucket = squareclass_examples.setdefault(
                    failing_squareclass, []
                )
                canonical_bucket = canonical_triples.setdefault(failing_squareclass, set())
                canonical_bucket.add(
                    (
                        normalized_n,
                        min(normalized_p, normalized_q),
                        max(normalized_p, normalized_q),
                    )
                )
                example = SumAbNormalizedNearMissExample(
                    orientation=orientation,
                    slope_params=(slope_m, slope_n),
                    scaled_term_params=(scaled_m, scaled_n),
                    shared_numerator=shared_terms.shared_numerator,
                    other_denominator=shared_terms.other_denominator,
                    failed_denominator=shared_terms.failed_denominator,
                    gcd_p_q=cross_terms.gcd_p_q,
                    gcd_n_p_q=gcd_n_p_q,
                    normalized_denominator_pair=normalized_pair,
                    normalized_shared_leg_triple=(normalized_n, normalized_p, normalized_q),
                    normalized_other_squareclass=normalized_other_squareclass,
                    normalized_failed_squareclass=normalized_failed_squareclass,
                    denominator_difference_over_gcd=difference_over_gcd,
                    denominator_sum_over_gcd=sum_over_gcd,
                    other_square_passes=other_passes,
                    failed_square_passes=failed_passes,
                )
                if len(bucket) < max_examples_per_bucket:
                    bucket.append(example)
                if len(squareclass_bucket) < max_examples_per_bucket:
                    squareclass_bucket.append(example)

    family_edges_by_squareclass = {
        key: _squareclass_family_edges(tuple(sorted(value)))
        for key, value in sorted(canonical_triples.items())
    }
    n_descending_edge_count, n_descending_continuation_count = (
        _n_descending_edge_stats(family_edges_by_squareclass)
    )

    return SumAbNormalizedNearMissSummary(
        max_m=max_m,
        total_near_misses=total,
        abs_difference_over_gcd_counts=dict(sorted(abs_difference_counts.items())),
        failing_squareclass_counts=dict(sorted(failing_squareclass_counts.items())),
        normalized_pair_counts=dict(sorted(normalized_pair_counts.items())),
        examples_by_abs_difference={
            key: tuple(value) for key, value in sorted(examples.items())
        },
        examples_by_failing_squareclass={
            key: tuple(value) for key, value in sorted(squareclass_examples.items())
        },
        canonical_triples_by_failing_squareclass={
            key: tuple(sorted(value)) for key, value in sorted(canonical_triples.items())
        },
        family_edges_by_failing_squareclass=family_edges_by_squareclass,
        n_descending_edge_count=n_descending_edge_count,
        n_descending_continuation_count=n_descending_continuation_count,
    )


def sum_ab_four_slope_squareclass_summary(
    *,
    max_m: int,
) -> SumAbFourSlopeSquareclassSummary:
    """Summarize the weak product-square layer in the four-slope model.

    In the ``sum=A+B`` branch, choose Pythagorean slopes ``x,y`` and set
    ``lambda = 1/(x+y-1)``.  Then ``r=lambda*x`` and ``s=lambda*y`` are the two
    unit-side checks.  This diagnostic counts when those two unit-side checks
    have equal squareclass; that is the product-square condition before asking
    whether each unit-side check is individually square.
    """
    if max_m < 2:
        raise ValueError("max_m must be at least 2")

    slopes = pythagorean_leg_ratios(max_m)
    squareclass_cache: dict[Fraction, int] = {}
    centerline_squareclasses: Counter[int] = Counter()
    equal_unit_squareclass_pairs = 0
    centerline_equal_unit_squareclass_pairs = 0
    noncenter_equal_unit_squareclass_pairs = 0
    true_four_pass_pairs = 0

    def unit_squareclass(value: Fraction) -> int:
        if value not in squareclass_cache:
            squareclass_cache[value] = leg_ratio_squareclass(value).squarefree_part
        return squareclass_cache[value]

    for x in slopes:
        for y in slopes:
            denominator = x + y - 1
            if denominator <= 0:
                continue
            lam = 1 / denominator
            r = lam * x
            s = lam * y
            r_squareclass = unit_squareclass(r)
            s_squareclass = unit_squareclass(s)
            if r_squareclass != s_squareclass:
                continue

            equal_unit_squareclass_pairs += 1
            if r_squareclass == 1:
                true_four_pass_pairs += 1
            if x == y:
                centerline_equal_unit_squareclass_pairs += 1
                centerline_squareclasses[r_squareclass] += 1
            else:
                noncenter_equal_unit_squareclass_pairs += 1

    return SumAbFourSlopeSquareclassSummary(
        max_m=max_m,
        slope_count=len(slopes),
        equal_unit_squareclass_pairs=equal_unit_squareclass_pairs,
        centerline_equal_unit_squareclass_pairs=centerline_equal_unit_squareclass_pairs,
        noncenter_equal_unit_squareclass_pairs=noncenter_equal_unit_squareclass_pairs,
        true_four_pass_pairs=true_four_pass_pairs,
        centerline_squareclasses=dict(sorted(centerline_squareclasses.items())),
    )


def sum_ab_four_slope_squareclass_witnesses(
    *,
    max_m: int,
    limit: int | None = None,
    include_centerline: bool = True,
) -> tuple[SumAbFourSlopeSquareclassWitness, ...]:
    """Return bounded equal-unit-squareclass witnesses for ``sum=A+B``.

    This is only a diagnostic extractor.  Absence of witnesses in a finite
    bound is not a proof.
    """
    if max_m < 2:
        raise ValueError("max_m must be at least 2")
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")

    slopes = pythagorean_leg_ratios(max_m)
    squareclass_cache: dict[Fraction, int] = {}
    witnesses: list[SumAbFourSlopeSquareclassWitness] = []

    def unit_squareclass(value: Fraction) -> int:
        if value not in squareclass_cache:
            squareclass_cache[value] = leg_ratio_squareclass(value).squarefree_part
        return squareclass_cache[value]

    for x in slopes:
        for y in slopes:
            denominator = x + y - 1
            if denominator <= 0:
                continue
            lam = 1 / denominator
            r = lam * x
            s = lam * y
            r_squareclass = unit_squareclass(r)
            if r_squareclass != unit_squareclass(s):
                continue
            centerline = x == y
            if centerline and not include_centerline:
                continue
            witnesses.append(
                SumAbFourSlopeSquareclassWitness(
                    slope1=x,
                    slope2=y,
                    lambda_ratio=lam,
                    r=r,
                    s=s,
                    unit_squareclass=r_squareclass,
                    centerline=centerline,
                    true_four_pass=r_squareclass == 1,
                )
            )
            if limit is not None and len(witnesses) >= limit:
                return tuple(witnesses)

    return tuple(witnesses)


def sum_ab_four_square_dual_slope_model(
    slope_x: Fraction | int,
    slope_y: Fraction | int,
) -> SumAbFourSquareDualSlopeModel:
    """Record the dual Pythagorean slopes forced by the four square tests."""
    x = _as_fraction(slope_x)
    y = _as_fraction(slope_y)
    _validate_positive("slope_x", x)
    _validate_positive("slope_y", y)

    common_leg = x + y - 1
    _validate_positive("common_leg", common_leg)
    dual_x = common_leg / x
    dual_y = common_leg / y
    dual_denominator = dual_x + dual_y - dual_x * dual_y
    if dual_denominator == 0:
        raise ValueError("dual denominator must be nonzero")

    reconstructed_x = dual_y / dual_denominator
    reconstructed_y = dual_x / dual_denominator
    reconstructed_common_leg = dual_x * dual_y / dual_denominator
    x_is_pythagorean = _is_rational_square(x * x + 1)
    y_is_pythagorean = _is_rational_square(y * y + 1)
    dual_x_is_pythagorean = _is_rational_square(dual_x * dual_x + 1)
    dual_y_is_pythagorean = _is_rational_square(dual_y * dual_y + 1)
    all_four_slopes_are_pythagorean = (
        x_is_pythagorean
        and y_is_pythagorean
        and dual_x_is_pythagorean
        and dual_y_is_pythagorean
    )
    return SumAbFourSquareDualSlopeModel(
        slope_x=x,
        slope_y=y,
        common_leg=common_leg,
        dual_slope_x=dual_x,
        dual_slope_y=dual_y,
        x_is_pythagorean=x_is_pythagorean,
        y_is_pythagorean=y_is_pythagorean,
        dual_x_is_pythagorean=dual_x_is_pythagorean,
        dual_y_is_pythagorean=dual_y_is_pythagorean,
        all_four_slopes_are_pythagorean=all_four_slopes_are_pythagorean,
        dual_denominator=dual_denominator,
        reconstructed_x=reconstructed_x,
        reconstructed_y=reconstructed_y,
        reconstructed_common_leg=reconstructed_common_leg,
        self_dual_identity_holds=(
            reconstructed_x == x
            and reconstructed_y == y
            and reconstructed_common_leg == common_leg
        ),
    )


def sum_ab_dual_slope_parameterization(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
) -> SumAbDualSlopeParameterization:
    """Parameterize the dual slopes in the four-square closed-loop model."""
    t = _as_fraction(parameter_t)
    u = _as_fraction(parameter_u)
    _validate_positive("parameter_t", t)
    _validate_positive("parameter_u", u)
    if t == 1 or u == 1:
        raise ValueError("parameters must not make the dual slope zero")

    dual_x = (1 - t * t) / (2 * t)
    dual_y = (1 - u * u) / (2 * u)
    _validate_positive("dual_slope_x", dual_x)
    _validate_positive("dual_slope_y", dual_y)

    dual_denominator = dual_x + dual_y - dual_x * dual_y
    _validate_positive("dual_denominator", dual_denominator)
    generated_x = dual_y / dual_denominator
    generated_y = dual_x / dual_denominator
    common_leg = dual_x * dual_y / dual_denominator
    generated_x_recovery_value = generated_x * generated_x + 1
    generated_y_recovery_value = generated_y * generated_y + 1

    denominator_polynomial = (
        t * t * u * u
        + 2 * t * t * u
        - t * t
        + 2 * t * u * u
        - 2 * t
        - u * u
        - 2 * u
        + 1
    )
    centerline_factor = (t - u) * (t + u) * (t * u - 1) * (t * u + 1)
    generated_x_minus_y_factorized = (
        -2 * (t - u) * (t * u + 1) / denominator_polynomial
    )
    recovery_value_difference_factorized = (
        -4 * centerline_factor / (denominator_polynomial * denominator_polynomial)
    )
    centerline_recovery_quartic = t**4 + 8 * t**3 + 18 * t * t - 8 * t + 1

    return SumAbDualSlopeParameterization(
        parameter_t=t,
        parameter_u=u,
        dual_slope_x=dual_x,
        dual_slope_y=dual_y,
        dual_denominator=dual_denominator,
        generated_x=generated_x,
        generated_y=generated_y,
        common_leg=common_leg,
        generated_x_recovery_value=generated_x_recovery_value,
        generated_y_recovery_value=generated_y_recovery_value,
        generated_x_is_pythagorean=_is_rational_square(generated_x_recovery_value),
        generated_y_is_pythagorean=_is_rational_square(generated_y_recovery_value),
        generated_x_minus_y=generated_x - generated_y,
        generated_x_minus_y_factorized=generated_x_minus_y_factorized,
        recovery_value_difference_factorized=recovery_value_difference_factorized,
        centerline_factor=centerline_factor,
        centerline_factor_zero=centerline_factor == 0,
        centerline_recovery_quartic=centerline_recovery_quartic,
    )


def sum_ab_dual_slope_valuation_ledger(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
) -> SumAbDualSlopeValuationLedger:
    """Return prime valuations for the dual-slope recovery square values."""
    parameterization = sum_ab_dual_slope_parameterization(parameter_t, parameter_u)
    recovery_values = (
        parameterization.generated_x_recovery_value,
        parameterization.generated_y_recovery_value,
    )
    recovery_difference = recovery_values[0] - recovery_values[1]
    centerline_factor = parameterization.centerline_factor
    primes = _prime_support((*recovery_values, recovery_difference, centerline_factor))
    rows: list[SumAbDualSlopeValuationRow] = []
    for prime in primes:
        recovery_valuations = tuple(
            _rational_valuation(value, prime) for value in recovery_values
        )
        if any(valuation is None for valuation in recovery_valuations):
            raise ValueError("recovery values should be positive nonzero rationals")
        rows.append(
            SumAbDualSlopeValuationRow(
                prime=prime,
                recovery_valuations=recovery_valuations,  # type: ignore[arg-type]
                recovery_difference_valuation=_rational_valuation(
                    recovery_difference,
                    prime,
                ),
                centerline_factor_valuation=_rational_valuation(
                    centerline_factor,
                    prime,
                ),
                all_recovery_valuations_even=all(
                    valuation % 2 == 0 for valuation in recovery_valuations
                ),
            )
        )
    rows_tuple = tuple(rows)
    recovery_squareclasses = (
        _rational_squareclass(recovery_values[0])[0],
        _rational_squareclass(recovery_values[1])[0],
    )
    recovery_squareclass_primes = tuple(
        prime for prime in primes if prime in recovery_squareclasses
    )
    return SumAbDualSlopeValuationLedger(
        parameterization=parameterization,
        recovery_squareclasses=recovery_squareclasses,
        recovery_squareclass_primes=recovery_squareclass_primes,
        three_mod_four_recovery_squareclass_primes=tuple(
            prime for prime in recovery_squareclass_primes if prime % 4 == 3
        ),
        primes=primes,
        three_mod_four_primes=tuple(prime for prime in primes if prime % 4 == 3),
        rows=rows_tuple,
        rows_by_prime={row.prime: row for row in rows_tuple},
    )


def _sum_ab_p_plus_lambda_q_norm(parameter: Fraction) -> Fraction:
    """Return the quartic norm controlling the ``p+lambda`` shadow."""
    return (
        parameter**4
        - 4 * parameter**3
        - 6 * parameter * parameter
        + 4 * parameter
        + 1
    )


def sum_ab_dual_slope_qadic_norm_ledger(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
    *,
    prime: int,
) -> SumAbDualSlopeQAdicNormLedger:
    """Return the global squareclass ledger for one q-adic norm shadow."""
    if prime <= 1:
        raise ValueError("prime must be an odd prime")
    parameterization = sum_ab_dual_slope_parameterization(parameter_t, parameter_u)
    q_norm_values = (
        _sum_ab_p_plus_lambda_q_norm(parameterization.parameter_t),
        _sum_ab_p_plus_lambda_q_norm(parameterization.parameter_u),
    )
    q_norm_squareclass_data = tuple(
        _rational_squareclass(abs(value)) for value in q_norm_values
    )
    recovery_values = (
        parameterization.generated_x_recovery_value,
        parameterization.generated_y_recovery_value,
    )
    recovery_squareclass_data = tuple(
        _rational_squareclass(value) for value in recovery_values
    )
    recovery_valuations_at_prime = tuple(
        _rational_valuation(value, prime) for value in recovery_values
    )
    recovery_squareclass_primes = tuple(
        primes for _, primes in recovery_squareclass_data
    )
    return SumAbDualSlopeQAdicNormLedger(
        parameterization=parameterization,
        parameter_pairs=(
            parameterization.parameter_t,
            parameterization.parameter_u,
        ),
        prime=prime,
        q_norm_values=q_norm_values,  # type: ignore[arg-type]
        q_norm_valuations=tuple(
            _rational_valuation(value, prime) for value in q_norm_values
        ),  # type: ignore[arg-type]
        q_norm_squareclasses=tuple(
            squareclass for squareclass, _ in q_norm_squareclass_data
        ),  # type: ignore[arg-type]
        odd_q_norm_squareclass_primes=tuple(
            primes for _, primes in q_norm_squareclass_data
        ),  # type: ignore[arg-type]
        recovery_squareclasses=tuple(
            squareclass for squareclass, _ in recovery_squareclass_data
        ),  # type: ignore[arg-type]
        recovery_squareclass_primes=recovery_squareclass_primes,  # type: ignore[arg-type]
        recovery_valuations_at_prime=recovery_valuations_at_prime,  # type: ignore[arg-type]
        shadow_prime_balanced_in_recovery_squareclasses=(
            all(
                valuation is not None and valuation % 2 == 0
                for valuation in recovery_valuations_at_prime
            )
            and all(prime not in primes for primes in recovery_squareclass_primes)
        ),
    )


def sum_ab_dual_slope_qadic_norm_summary(
    parameter_pairs: tuple[tuple[Fraction | int, Fraction | int], ...],
    *,
    prime: int,
) -> SumAbDualSlopeQAdicNormSummary:
    """Summarize q-adic norm shadow squareclass patterns for sample pairs."""
    ledgers = tuple(
        sum_ab_dual_slope_qadic_norm_ledger(t, u, prime=prime)
        for t, u in parameter_pairs
    )
    q_norm_valuation_pair_counts: Counter[tuple[int | None, int | None]] = Counter()
    recovery_prime_mod4_counts: Counter[int] = Counter()
    recovery_prime_mod8_counts: Counter[int] = Counter()
    recovery_prime_mod16_counts: Counter[int] = Counter()
    examples_by_bucket: dict[str, SumAbDualSlopeQAdicNormLedger] = {}
    shadow_prime_balanced_count = 0
    recovery_contains_shadow_prime_count = 0
    recovery_has_three_mod_four_prime_count = 0
    recovery_has_only_two_or_one_mod_four_primes_count = 0

    for ledger in ledgers:
        q_norm_valuation_pair_counts[ledger.q_norm_valuations] += 1
        recovery_primes = {
            prime_value
            for primes in ledger.recovery_squareclass_primes
            for prime_value in primes
        }
        for primes in ledger.recovery_squareclass_primes:
            for prime_value in primes:
                recovery_prime_mod4_counts[prime_value % 4] += 1
                recovery_prime_mod8_counts[prime_value % 8] += 1
                recovery_prime_mod16_counts[prime_value % 16] += 1
        contains_shadow_prime = prime in recovery_primes
        has_three_mod_four_prime = any(
            prime_value % 4 == 3 for prime_value in recovery_primes
        )
        if ledger.shadow_prime_balanced_in_recovery_squareclasses:
            shadow_prime_balanced_count += 1
        if contains_shadow_prime:
            recovery_contains_shadow_prime_count += 1
            examples_by_bucket.setdefault("contains_shadow_prime", ledger)
        if has_three_mod_four_prime:
            recovery_has_three_mod_four_prime_count += 1
            examples_by_bucket.setdefault("has_three_mod_four", ledger)
        else:
            recovery_has_only_two_or_one_mod_four_primes_count += 1
            examples_by_bucket.setdefault("only_two_or_one_mod_four", ledger)

    return SumAbDualSlopeQAdicNormSummary(
        prime=prime,
        sample_count=len(ledgers),
        shadow_prime_balanced_count=shadow_prime_balanced_count,
        recovery_contains_shadow_prime_count=recovery_contains_shadow_prime_count,
        recovery_has_three_mod_four_prime_count=recovery_has_three_mod_four_prime_count,
        recovery_has_only_two_or_one_mod_four_primes_count=(
            recovery_has_only_two_or_one_mod_four_primes_count
        ),
        q_norm_valuation_pair_counts=dict(sorted(q_norm_valuation_pair_counts.items())),
        recovery_prime_mod4_counts=dict(sorted(recovery_prime_mod4_counts.items())),
        recovery_prime_mod8_counts=dict(sorted(recovery_prime_mod8_counts.items())),
        recovery_prime_mod16_counts=dict(sorted(recovery_prime_mod16_counts.items())),
        examples_by_bucket=examples_by_bucket,
    )


def _sum_ab_p_plus_lambda_shadow_f_mod(
    parameter_t: int,
    parameter_u: int,
    modulus: int,
) -> int:
    t = parameter_t
    u = parameter_u
    return (
        -t * t * u * u
        - 2 * t * t * u
        + t * t
        - 2 * t * u * u
        + 4 * t * u
        + 2 * t
        + u * u
        + 2 * u
        - 1
    ) % modulus


def _sum_ab_p_plus_lambda_shadow_e_mod(
    parameter_t: int,
    parameter_u: int,
    modulus: int,
) -> int:
    t = parameter_t
    u = parameter_u
    return (
        t * t * u * u
        + t * t * u
        - t * t
        + t * u * u
        - t
        - u * u
        - u
        + 1
    ) % modulus


def _sum_ab_p_plus_lambda_shadow_roots_mod_prime(
    prime: int,
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (t, u)
        for t in range(prime)
        for u in range(prime)
        if _sum_ab_p_plus_lambda_shadow_f_mod(t, u, prime) == 0
        and _sum_ab_p_plus_lambda_shadow_e_mod(t, u, prime) == 0
    )


def _sum_ab_p_plus_lambda_shadow_lifts(
    roots_mod_prime: tuple[tuple[int, int], ...],
    *,
    prime: int,
    exponent: int,
) -> tuple[tuple[int, int], ...]:
    lifted = roots_mod_prime
    current_modulus = prime
    for current_exponent in range(2, exponent + 1):
        next_modulus = prime**current_exponent
        next_lifted: list[tuple[int, int]] = []
        for t0, u0 in lifted:
            for t_digit in range(prime):
                for u_digit in range(prime):
                    t = t0 + current_modulus * t_digit
                    u = u0 + current_modulus * u_digit
                    if (
                        _sum_ab_p_plus_lambda_shadow_f_mod(t, u, next_modulus)
                        == 0
                        and _sum_ab_p_plus_lambda_shadow_e_mod(t, u, next_modulus)
                        == 0
                    ):
                        next_lifted.append((t % next_modulus, u % next_modulus))
        lifted = tuple(sorted(next_lifted))
        current_modulus = next_modulus
    return lifted


def _positive_fraction_representatives_for_residue(
    residue: int,
    *,
    modulus: int,
    bound: int,
) -> tuple[Fraction, ...]:
    representatives: set[Fraction] = set()
    for height in range(1, bound + 1):
        for denominator in range(1, height + 1):
            if _gcd(denominator, modulus) != 1:
                continue
            numerator = residue * denominator % modulus
            if 0 < numerator <= height:
                representatives.add(Fraction(numerator, denominator))
    return tuple(
        sorted(
            representatives,
            key=lambda value: (
                max(value.numerator, value.denominator),
                value.numerator,
                value.denominator,
            ),
        )
    )


def sum_ab_dual_slope_qadic_norm_generated_summary(
    *,
    prime: int,
    exponent: int,
    representative_bound: int,
    sample_limit: int | None = None,
) -> SumAbDualSlopeQAdicNormGeneratedSummary:
    """Generate q-adic ``p+lambda`` shadow samples and summarize them.

    This is a diagnostic generator, not a proof certificate.  It keeps only
    positive representatives that enter the existing dual-slope chart.
    """
    if prime <= 2 or factorint(prime) != {prime: 1}:
        raise ValueError("prime must be an odd prime")
    if prime % 16 != 15:
        raise ValueError("prime must be 15 mod 16")
    if exponent < 2:
        raise ValueError("exponent must be at least 2")
    if representative_bound < 1:
        raise ValueError("representative_bound must be positive")
    if sample_limit is not None and sample_limit < 1:
        raise ValueError("sample_limit must be positive when provided")

    modulus = prime**exponent
    roots_mod_prime = _sum_ab_p_plus_lambda_shadow_roots_mod_prime(prime)
    lifted_residue_pairs = _sum_ab_p_plus_lambda_shadow_lifts(
        roots_mod_prime,
        prime=prime,
        exponent=exponent,
    )
    parameter_pairs: list[tuple[Fraction, Fraction]] = []
    for t_residue, u_residue in lifted_residue_pairs:
        found_pair = False
        t_representatives = _positive_fraction_representatives_for_residue(
            t_residue,
            modulus=modulus,
            bound=representative_bound,
        )
        u_representatives = _positive_fraction_representatives_for_residue(
            u_residue,
            modulus=modulus,
            bound=representative_bound,
        )
        for t in t_representatives:
            for u in u_representatives:
                try:
                    sum_ab_dual_slope_parameterization(t, u)
                except ValueError:
                    continue
                parameter_pairs.append((t, u))
                found_pair = True
                break
            if found_pair:
                break
        if sample_limit is not None and len(parameter_pairs) >= sample_limit:
            break

    parameter_pairs_tuple = tuple(parameter_pairs)
    return SumAbDualSlopeQAdicNormGeneratedSummary(
        prime=prime,
        exponent=exponent,
        modulus=modulus,
        representative_bound=representative_bound,
        root_count_mod_prime=len(roots_mod_prime),
        lift_count=len(lifted_residue_pairs),
        lifted_residue_pairs=lifted_residue_pairs,
        parameter_pairs=parameter_pairs_tuple,
        summary=sum_ab_dual_slope_qadic_norm_summary(
            parameter_pairs_tuple,
            prime=prime,
        ),
    )


def sum_ab_dual_slope_qadic_norm_bridge_summary(
    *,
    prime: int,
    exponent: int,
    representative_bound: int,
    sample_limit: int | None = None,
) -> SumAbDualSlopeQAdicNormBridgeSummary:
    """Rewrite generated q-adic norm shadow samples as Gaussian bridge cycles."""
    generated_summary = sum_ab_dual_slope_qadic_norm_generated_summary(
        prime=prime,
        exponent=exponent,
        representative_bound=representative_bound,
        sample_limit=sample_limit,
    )
    ledgers: list[SumAbDualSlopeQAdicNormBridgeLedger] = []
    for t, u in generated_summary.parameter_pairs:
        norm_ledger = sum_ab_dual_slope_qadic_norm_ledger(t, u, prime=prime)
        bridge_cycle = sum_ab_dual_slope_gaussian_bridge_cycle(t, u)
        ledgers.append(
            SumAbDualSlopeQAdicNormBridgeLedger(
                norm_ledger=norm_ledger,
                bridge_cycle=bridge_cycle,
                recovery_matches_bridge_squareclasses=(
                    norm_ledger.recovery_squareclasses
                    == bridge_cycle.bridge_squareclasses
                ),
                generated_flags_match_bridge_flags=(
                    bridge_cycle.generated_flags_match_bridge_flags
                ),
            )
        )

    ledgers_tuple = tuple(ledgers)
    return SumAbDualSlopeQAdicNormBridgeSummary(
        generated_summary=generated_summary,
        ledgers=ledgers_tuple,
        sample_count=len(ledgers_tuple),
        recovery_matches_bridge_squareclass_count=sum(
            ledger.recovery_matches_bridge_squareclasses for ledger in ledgers_tuple
        ),
        generated_flags_match_bridge_flags_count=sum(
            ledger.generated_flags_match_bridge_flags for ledger in ledgers_tuple
        ),
        all_cross_bridges_pythagorean_count=sum(
            ledger.bridge_cycle.all_cross_bridges_are_pythagorean
            for ledger in ledgers_tuple
        ),
        first_ledger=ledgers_tuple[0] if ledgers_tuple else None,
    )


def sum_ab_dual_slope_qadic_bridge_valuation_summary(
    *,
    prime: int,
    exponent: int,
    representative_bound: int,
    sample_limit: int | None = None,
) -> SumAbDualSlopeQAdicBridgeValuationSummary:
    """Summarize q-adic valuations of generated bridge-cycle samples."""
    generated_summary = sum_ab_dual_slope_qadic_norm_generated_summary(
        prime=prime,
        exponent=exponent,
        representative_bound=representative_bound,
        sample_limit=sample_limit,
    )
    rows: list[SumAbDualSlopeQAdicBridgeValuationRow] = []
    centerline_factor_valuation_counts: Counter[
        tuple[int | None, int | None, int | None, int | None]
    ] = Counter()
    extra_factor_valuation_counts: Counter[int | None] = Counter()
    bridge_difference_valuation_counts: Counter[int | None] = Counter()
    bridge_value_valuation_pair_counts: Counter[tuple[int | None, int | None]] = (
        Counter()
    )
    bridge_value_2adic_pair_counts: Counter[tuple[int | None, int | None]] = Counter()
    for t, u in generated_summary.parameter_pairs:
        factorization = sum_ab_dual_slope_bridge_difference_factorization(t, u)
        centerline_factors = (t - u, t + u, t * u - 1, t * u + 1)
        centerline_factor_valuations = tuple(
            _rational_valuation(value, prime) for value in centerline_factors
        )
        bridge_values = (
            factorization.bridge_cycle.x_to_dual_y.bridge_value,
            factorization.bridge_cycle.y_to_dual_x.bridge_value,
        )
        bridge_value_valuation_pair = tuple(
            _rational_valuation(value, prime) for value in bridge_values
        )
        bridge_value_2adic_pair = tuple(
            _rational_valuation(value, 2) for value in bridge_values
        )
        row = SumAbDualSlopeQAdicBridgeValuationRow(
            parameter_pairs=(t, u),
            centerline_factor_valuations=centerline_factor_valuations,  # type: ignore[arg-type]
            extra_factor_valuation=_rational_valuation(
                factorization.extra_equal_bridge_factor,
                prime,
            ),
            bridge_difference_valuation=_rational_valuation(
                factorization.bridge_value_difference,
                prime,
            ),
            bridge_value_valuation_pair=bridge_value_valuation_pair,  # type: ignore[arg-type]
            bridge_value_2adic_pair=bridge_value_2adic_pair,  # type: ignore[arg-type]
        )
        rows.append(row)
        centerline_factor_valuation_counts[row.centerline_factor_valuations] += 1
        extra_factor_valuation_counts[row.extra_factor_valuation] += 1
        bridge_difference_valuation_counts[row.bridge_difference_valuation] += 1
        bridge_value_valuation_pair_counts[row.bridge_value_valuation_pair] += 1
        bridge_value_2adic_pair_counts[row.bridge_value_2adic_pair] += 1

    rows_tuple = tuple(rows)
    return SumAbDualSlopeQAdicBridgeValuationSummary(
        generated_summary=generated_summary,
        rows=rows_tuple,
        sample_count=len(rows_tuple),
        centerline_factor_valuation_counts=dict(
            sorted(centerline_factor_valuation_counts.items())
        ),
        extra_factor_valuation_counts=dict(
            sorted(extra_factor_valuation_counts.items())
        ),
        bridge_difference_valuation_counts=dict(
            sorted(bridge_difference_valuation_counts.items())
        ),
        bridge_value_valuation_pair_counts=dict(
            sorted(bridge_value_valuation_pair_counts.items())
        ),
        bridge_value_2adic_pair_counts=dict(
            sorted(bridge_value_2adic_pair_counts.items())
        ),
        first_row=rows_tuple[0] if rows_tuple else None,
    )


def _rational_odd_unit_mod_8(value: Fraction) -> int:
    if value == 0:
        raise ValueError("value must be nonzero")

    def strip_twos(part: int) -> int:
        odd_part = abs(part)
        while odd_part % 2 == 0:
            odd_part //= 2
        return odd_part

    numerator_unit = strip_twos(value.numerator)
    denominator_unit = strip_twos(value.denominator)
    return (numerator_unit % 8) * pow(denominator_unit % 8, -1, 8) % 8


def sum_ab_dual_slope_qadic_bridge_2adic_summary(
    *,
    prime: int,
    exponent: int,
    representative_bound: int,
    sample_limit: int | None = None,
) -> SumAbDualSlopeQAdicBridgeTwoAdicSummary:
    """Classify generated bridge values by the two-adic square test."""
    valuation_summary = sum_ab_dual_slope_qadic_bridge_valuation_summary(
        prime=prime,
        exponent=exponent,
        representative_bound=representative_bound,
        sample_limit=sample_limit,
    )
    local_square_unit_mod8_pair_counts: Counter[tuple[int, int]] = Counter()
    parity_killed_count = 0
    two_adic_local_square_count = 0
    for row in valuation_summary.rows:
        valuation_pair = row.bridge_value_2adic_pair
        if any(valuation is None or valuation % 2 for valuation in valuation_pair):
            parity_killed_count += 1
            continue
        t, u = row.parameter_pairs
        factorization = sum_ab_dual_slope_bridge_difference_factorization(t, u)
        bridge_values = (
            factorization.bridge_cycle.x_to_dual_y.bridge_value,
            factorization.bridge_cycle.y_to_dual_x.bridge_value,
        )
        unit_pair = tuple(_rational_odd_unit_mod_8(value) for value in bridge_values)
        if unit_pair == (1, 1):
            two_adic_local_square_count += 1
        local_square_unit_mod8_pair_counts[unit_pair] += 1

    return SumAbDualSlopeQAdicBridgeTwoAdicSummary(
        valuation_summary=valuation_summary,
        sample_count=valuation_summary.sample_count,
        parity_killed_count=parity_killed_count,
        two_adic_local_square_count=two_adic_local_square_count,
        bridge_value_2adic_pair_counts=(
            valuation_summary.bridge_value_2adic_pair_counts
        ),
        local_square_unit_mod8_pair_counts=dict(
            sorted(local_square_unit_mod8_pair_counts.items())
        ),
    )


def sum_ab_dual_slope_qadic_bridge_local_square_summary(
    *,
    prime: int,
    exponent: int,
    representative_bound: int,
    sample_limit: int | None = None,
) -> SumAbDualSlopeQAdicBridgeLocalSquareSummary:
    """Count generated bridge samples passing both q-adic and two-adic tests."""
    two_adic_summary = sum_ab_dual_slope_qadic_bridge_2adic_summary(
        prime=prime,
        exponent=exponent,
        representative_bound=representative_bound,
        sample_limit=sample_limit,
    )
    q_adic_local_square_flag_pair_counts: Counter[tuple[bool, bool]] = Counter()
    q_adic_local_square_count = 0
    combined_survivors: list[tuple[Fraction, Fraction]] = []
    for row in two_adic_summary.valuation_summary.rows:
        t, u = row.parameter_pairs
        factorization = sum_ab_dual_slope_bridge_difference_factorization(t, u)
        bridge_values = (
            factorization.bridge_cycle.x_to_dual_y.bridge_value,
            factorization.bridge_cycle.y_to_dual_x.bridge_value,
        )
        q_flags = tuple(
            _is_odd_prime_local_square(value, prime) for value in bridge_values
        )
        q_adic_local_square_flag_pair_counts[q_flags] += 1
        q_passes = q_flags == (True, True)
        if q_passes:
            q_adic_local_square_count += 1
        two_adic_passes = (
            all(
                valuation is not None and valuation % 2 == 0
                for valuation in row.bridge_value_2adic_pair
            )
            and tuple(_rational_odd_unit_mod_8(value) for value in bridge_values)
            == (1, 1)
        )
        if q_passes and two_adic_passes:
            combined_survivors.append(row.parameter_pairs)

    return SumAbDualSlopeQAdicBridgeLocalSquareSummary(
        two_adic_summary=two_adic_summary,
        sample_count=two_adic_summary.sample_count,
        two_adic_local_square_count=two_adic_summary.two_adic_local_square_count,
        q_adic_local_square_count=q_adic_local_square_count,
        combined_q_and_2_adic_local_square_count=len(combined_survivors),
        q_adic_local_square_flag_pair_counts=dict(
            sorted(q_adic_local_square_flag_pair_counts.items())
        ),
        combined_survivor_parameter_pairs=tuple(combined_survivors),
    )


def _safe_gaussian_absorption_branch(
    value: Fraction,
    decomposition: tuple[int, int],
    branch: str,
) -> Fraction | None:
    first, second = decomposition
    if branch == "plus":
        denominator = first - second * value
        if denominator == 0:
            return None
        return (first * value + second) / denominator
    if branch == "minus":
        denominator = first + second * value
        if denominator == 0:
            return None
        return (first * value - second) / denominator
    raise ValueError("branch must be 'plus' or 'minus'")


def sum_ab_dual_slope_gaussian_absorption(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
    *,
    failed_side: str,
) -> SumAbDualSlopeGaussianAbsorption:
    """Absorb a failed dual-slope recovery squareclass when possible."""
    parameterization = sum_ab_dual_slope_parameterization(parameter_t, parameter_u)
    if failed_side == "x":
        failed_slope = parameterization.generated_x
        failed_value = parameterization.generated_x_recovery_value
    elif failed_side == "y":
        failed_slope = parameterization.generated_y
        failed_value = parameterization.generated_y_recovery_value
    else:
        raise ValueError("failed_side must be 'x' or 'y'")

    failed_squareclass = _rational_squareclass(failed_value)[0]
    decomposition = _two_square_decomposition(failed_squareclass)
    if decomposition is None:
        raise ValueError("failed squareclass is not a sum of two squares")
    absorbed_plus = _safe_gaussian_absorption_branch(
        failed_slope,
        decomposition,
        "plus",
    )
    absorbed_minus = _safe_gaussian_absorption_branch(
        failed_slope,
        decomposition,
        "minus",
    )
    targets = (
        ("dual_x", parameterization.dual_slope_x),
        ("dual_y", parameterization.dual_slope_y),
    )
    matches: list[tuple[str, str, Fraction]] = []
    for branch, absorbed in (("plus", absorbed_plus), ("minus", absorbed_minus)):
        if absorbed is None:
            continue
        for target_name, target in targets:
            if absorbed == target:
                matches.append((branch, target_name, absorbed))
    matching_absorptions = tuple(matches)
    return SumAbDualSlopeGaussianAbsorption(
        parameterization=parameterization,
        failed_side=failed_side,
        failed_slope=failed_slope,
        failed_value=failed_value,
        failed_squareclass=failed_squareclass,
        two_square_decomposition=decomposition,
        absorbed_plus=absorbed_plus,
        absorbed_minus=absorbed_minus,
        matching_absorptions=matching_absorptions,
        absorbs_to_existing_dual_slope=bool(matching_absorptions),
    )


def sum_ab_dual_slope_gaussian_bridge(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
    *,
    failed_side: str,
    target_side: str,
) -> SumAbDualSlopeGaussianBridge:
    """Return the Gaussian angle bridge from a failed slope to a dual slope."""
    parameterization = sum_ab_dual_slope_parameterization(parameter_t, parameter_u)
    if failed_side == "x":
        failed_slope = parameterization.generated_x
        failed_value = parameterization.generated_x_recovery_value
    elif failed_side == "y":
        failed_slope = parameterization.generated_y
        failed_value = parameterization.generated_y_recovery_value
    else:
        raise ValueError("failed_side must be 'x' or 'y'")

    if target_side == "dual_x":
        target_slope = parameterization.dual_slope_x
    elif target_side == "dual_y":
        target_slope = parameterization.dual_slope_y
    else:
        raise ValueError("target_side must be 'dual_x' or 'dual_y'")

    bridge_denominator = target_slope * failed_slope + 1
    if bridge_denominator == 0:
        raise ValueError("bridge denominator must be nonzero")
    bridge_ratio = (failed_slope - target_slope) / bridge_denominator
    bridge_value = bridge_ratio * bridge_ratio + 1
    recovered_target = (failed_slope - bridge_ratio) / (
        1 + bridge_ratio * failed_slope
    )
    failed_squareclass = _rational_squareclass(failed_value)[0]
    bridge_squareclass = _rational_squareclass(bridge_value)[0]
    return SumAbDualSlopeGaussianBridge(
        parameterization=parameterization,
        failed_side=failed_side,
        target_side=target_side,
        failed_slope=failed_slope,
        target_slope=target_slope,
        failed_squareclass=failed_squareclass,
        bridge_ratio=bridge_ratio,
        bridge_value=bridge_value,
        bridge_squareclass=bridge_squareclass,
        squareclass_matches_failure=bridge_squareclass == failed_squareclass,
        recovered_target=recovered_target,
        recovery_identity_holds=recovered_target == target_slope,
    )


def sum_ab_dual_slope_gaussian_bridge_cycle(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
) -> SumAbDualSlopeGaussianBridgeCycle:
    """Record both cross bridges in the dual-slope four-square loop."""
    parameterization = sum_ab_dual_slope_parameterization(parameter_t, parameter_u)
    x_to_dual_y = sum_ab_dual_slope_gaussian_bridge(
        parameter_t,
        parameter_u,
        failed_side="x",
        target_side="dual_y",
    )
    y_to_dual_x = sum_ab_dual_slope_gaussian_bridge(
        parameter_t,
        parameter_u,
        failed_side="y",
        target_side="dual_x",
    )
    generated_squareclasses = (
        _rational_squareclass(parameterization.generated_x_recovery_value)[0],
        _rational_squareclass(parameterization.generated_y_recovery_value)[0],
    )
    bridge_squareclasses = (
        x_to_dual_y.bridge_squareclass,
        y_to_dual_x.bridge_squareclass,
    )
    generated_pythagorean_flags = (
        parameterization.generated_x_is_pythagorean,
        parameterization.generated_y_is_pythagorean,
    )
    bridge_pythagorean_flags = (
        bridge_squareclasses[0] == 1,
        bridge_squareclasses[1] == 1,
    )
    return SumAbDualSlopeGaussianBridgeCycle(
        parameterization=parameterization,
        x_to_dual_y=x_to_dual_y,
        y_to_dual_x=y_to_dual_x,
        generated_slopes=(
            parameterization.generated_x,
            parameterization.generated_y,
        ),
        dual_slopes=(
            parameterization.dual_slope_x,
            parameterization.dual_slope_y,
        ),
        bridge_ratios=(
            x_to_dual_y.bridge_ratio,
            y_to_dual_x.bridge_ratio,
        ),
        generated_squareclasses=generated_squareclasses,
        bridge_squareclasses=bridge_squareclasses,
        generated_pythagorean_flags=generated_pythagorean_flags,
        bridge_pythagorean_flags=bridge_pythagorean_flags,
        generated_flags_match_bridge_flags=(
            generated_pythagorean_flags == bridge_pythagorean_flags
        ),
        all_generated_slopes_are_pythagorean=all(generated_pythagorean_flags),
        all_cross_bridges_are_pythagorean=all(bridge_pythagorean_flags),
    )


def sum_ab_dual_slope_bridge_difference_factorization(
    parameter_t: Fraction | int,
    parameter_u: Fraction | int,
) -> SumAbDualSlopeBridgeDifferenceFactorization:
    """Factor the difference of the two cross-bridge square values."""
    t = _as_fraction(parameter_t)
    u = _as_fraction(parameter_u)
    bridge_cycle = sum_ab_dual_slope_gaussian_bridge_cycle(t, u)
    bridge_value_difference = (
        bridge_cycle.x_to_dual_y.bridge_value
        - bridge_cycle.y_to_dual_x.bridge_value
    )

    centerline_factor = (t - u) * (t + u) * (t * u - 1) * (t * u + 1)
    extra_equal_bridge_factor = (
        t * t * u * u
        + t * t * u
        - t * t
        + t * u * u
        - t
        - u * u
        - u
        + 1
    )
    shared_t_factor = t * t + 2 * t - 1
    shared_u_factor = u * u + 2 * u - 1
    x_denominator_factor = (
        t * t * u**3
        + 2 * t * t * u * u
        - t * t * u
        - t * u**4
        + 2 * t * u**3
        + 2 * t * u * u
        - 2 * t * u
        - t
        - u**3
        - 2 * u * u
        + u
    )
    y_denominator_factor = (
        t**4 * u
        - t**3 * u * u
        - 2 * t**3 * u
        + t**3
        - 2 * t * t * u * u
        - 2 * t * t * u
        + 2 * t * t
        + t * u * u
        + 2 * t * u
        - t
        + u
    )
    if x_denominator_factor == 0 or y_denominator_factor == 0:
        raise ValueError("bridge difference denominator must be nonzero")

    bridge_difference_factorized = (
        -centerline_factor
        * (t + u)
        * (t * u - 1)
        * shared_t_factor
        * shared_t_factor
        * shared_u_factor
        * shared_u_factor
        * extra_equal_bridge_factor
        / (x_denominator_factor * x_denominator_factor)
        / (y_denominator_factor * y_denominator_factor)
    )
    extra_factor_u_quadratic_coefficients = (
        t * t + t - 1,
        t * t - 1,
        1 - t - t * t,
    )
    extra_factor_u_discriminant = (
        extra_factor_u_quadratic_coefficients[1]
        * extra_factor_u_quadratic_coefficients[1]
        - 4
        * extra_factor_u_quadratic_coefficients[0]
        * extra_factor_u_quadratic_coefficients[2]
    )
    new_curve_value_t = 5 * t**4 + 8 * t**3 - 6 * t * t - 8 * t + 5
    return SumAbDualSlopeBridgeDifferenceFactorization(
        bridge_cycle=bridge_cycle,
        bridge_value_difference=bridge_value_difference,
        centerline_factor=centerline_factor,
        extra_equal_bridge_factor=extra_equal_bridge_factor,
        bridge_difference_factorized=bridge_difference_factorized,
        factorization_holds=bridge_difference_factorized == bridge_value_difference,
        extra_factor_u_quadratic_coefficients=extra_factor_u_quadratic_coefficients,
        extra_factor_u_discriminant=extra_factor_u_discriminant,
        new_curve_value_t=new_curve_value_t,
        extra_factor_discriminant_matches_new_curve=(
            extra_factor_u_discriminant == new_curve_value_t
        ),
    )


def _sum_ab_squareclass_ratio_terms(
    t: Fraction,
    u: Fraction,
) -> tuple[Fraction, Fraction]:
    numerator = (
        2 * t**4 * u**2
        + 2 * t**3 * u**3
        + 4 * t**3 * u**2
        - 2 * t**3 * u
        + t**2 * u**4
        + 4 * t**2 * u**3
        - 2 * t**2 * u**2
        - 4 * t**2 * u
        + t**2
        - 2 * t * u**3
        - 4 * t * u**2
        + 2 * t * u
        + 2 * u**2
    )
    denominator = (
        t**4 * u**2
        + 2 * t**3 * u**3
        + 4 * t**3 * u**2
        - 2 * t**3 * u
        + 2 * t**2 * u**4
        + 4 * t**2 * u**3
        - 2 * t**2 * u**2
        - 4 * t**2 * u
        + 2 * t**2
        - 2 * t * u**3
        - 4 * t * u**2
        + 2 * t * u
        + u**2
    )
    return numerator, denominator


def sum_ab_squareclass_ratio_z_reduction(
    t: Fraction | int,
    u: Fraction | int,
) -> SumAbSquareclassRatioZReduction:
    """Reduce the four-slope squareclass ratio by ``z = u - 1/u``.

    For ``x=(1-t^2)/(2t)`` and ``y=(1-u^2)/(2u)``, the unit-side squareclass
    ratio is ``A/B``.  Substituting ``z = u - 1/u`` lowers the expression from a
    quartic in ``u`` to a quadratic in ``z``; this helper records that exact
    identity.
    """
    t_fraction = _as_fraction(t)
    u_fraction = _as_fraction(u)
    _validate_positive("t", t_fraction)
    _validate_positive("u", u_fraction)

    z = u_fraction - 1 / u_fraction
    direct_numerator, direct_denominator = _sum_ab_squareclass_ratio_terms(
        t_fraction,
        u_fraction,
    )
    reduced_numerator = (
        2 * t_fraction**4
        + 2 * t_fraction**3 * z
        + 4 * t_fraction**3
        + t_fraction**2 * z**2
        + 4 * t_fraction**2 * z
        - 2 * t_fraction * z
        - 4 * t_fraction
        + 2
    )
    reduced_denominator = (
        t_fraction**4
        + 2 * t_fraction**3 * z
        + 4 * t_fraction**3
        + 2 * t_fraction**2 * z**2
        + 4 * t_fraction**2 * z
        + 2 * t_fraction**2
        - 2 * t_fraction * z
        - 4 * t_fraction
        + 1
    )
    direct_ratio = direct_numerator / direct_denominator
    reduced_ratio = reduced_numerator / reduced_denominator
    return SumAbSquareclassRatioZReduction(
        t=t_fraction,
        u=u_fraction,
        z=z,
        direct_ratio=direct_ratio,
        reduced_ratio=reduced_ratio,
        ratio_is_square=_is_rational_square(direct_ratio),
        u_recovery_square=z * z + 4,
    )


def sum_ab_squareclass_ratio_z_parameterization(
    t: Fraction | int,
    parameter: Fraction | int,
) -> SumAbSquareclassRatioZParameterization:
    """Parameterize ``z^2+4`` and expose the self-similar ratio.

    Setting ``z = a - 1/a`` recovers the same squareclass-ratio formula with
    ``u`` replaced by ``a``.  This records the self-similarity instead of
    treating the ``z`` reduction as a new proof.
    """
    t_fraction = _as_fraction(t)
    parameter_fraction = _as_fraction(parameter)
    _validate_positive("t", t_fraction)
    _validate_positive("parameter", parameter_fraction)

    z = parameter_fraction - 1 / parameter_fraction
    reduced = sum_ab_squareclass_ratio_z_reduction(t_fraction, parameter_fraction)
    self_numerator, self_denominator = _sum_ab_squareclass_ratio_terms(
        t_fraction,
        parameter_fraction,
    )
    self_similar_ratio = self_numerator / self_denominator
    centerline_factor = (
        (t_fraction - parameter_fraction)
        * (t_fraction + parameter_fraction)
        * (t_fraction * parameter_fraction - 1)
        * (t_fraction * parameter_fraction + 1)
    )
    return SumAbSquareclassRatioZParameterization(
        t=t_fraction,
        parameter=parameter_fraction,
        z=z,
        reduced_ratio=reduced.reduced_ratio,
        self_similar_ratio=self_similar_ratio,
        ratio_is_square=_is_rational_square(self_similar_ratio),
        centerline_factor=centerline_factor,
    )


def sum_ab_squareclass_ratio_tu_quotient_model(
    t_quotient: Fraction | int,
    u_quotient: Fraction | int,
) -> SumAbSquareclassRatioTUQuotientModel:
    """Return the quotient model for ``T=t-1/t`` and ``U=u-1/u``.

    The four-slope squareclass ratio can be written as two quadratic forms in
    ``T`` and ``U``.  A rational ``T`` comes from a rational positive ``t`` only
    when ``T^2+4`` is a rational square.
    """
    t_value = _as_fraction(t_quotient)
    u_value = _as_fraction(u_quotient)
    numerator = (
        2 * t_value**2
        + 2 * t_value * u_value
        + 4 * t_value
        + u_value**2
        + 4 * u_value
        + 4
    )
    denominator = (
        t_value**2
        + 2 * t_value * u_value
        + 4 * t_value
        + 2 * u_value**2
        + 4 * u_value
        + 4
    )
    ratio = numerator / denominator
    return SumAbSquareclassRatioTUQuotientModel(
        t_quotient=t_value,
        u_quotient=u_value,
        numerator_quadratic=numerator,
        denominator_quadratic=denominator,
        ratio=ratio,
        ratio_is_square=_is_rational_square(ratio),
        t_recovery_square=_is_rational_square(t_value * t_value + 4),
        u_recovery_square=_is_rational_square(u_value * u_value + 4),
    )


def sum_ab_squareclass_ratio_slope_quadratic_model(
    slope_x: Fraction | int,
    slope_y: Fraction | int,
) -> SumAbSquareclassRatioSlopeQuadraticModel:
    """Return the squareclass-ratio model directly in the slopes ``x,y``."""
    x = _as_fraction(slope_x)
    y = _as_fraction(slope_y)
    numerator = 2 * x**2 + 2 * x * y - 2 * x + y**2 - 2 * y + 1
    denominator = x**2 + 2 * x * y - 2 * x + 2 * y**2 - 2 * y + 1
    ratio = numerator / denominator
    numerator_is_square = _is_rational_square(numerator)
    denominator_is_square = _is_rational_square(denominator)
    return SumAbSquareclassRatioSlopeQuadraticModel(
        slope_x=x,
        slope_y=y,
        numerator_quadratic=numerator,
        denominator_quadratic=denominator,
        ratio=ratio,
        ratio_is_square=_is_rational_square(ratio),
        numerator_is_square=numerator_is_square,
        denominator_is_square=denominator_is_square,
        individual_unit_terms_are_squares=(
            numerator_is_square and denominator_is_square
        ),
        x_recovery_square=_is_rational_square(x * x + 1),
        y_recovery_square=_is_rational_square(y * y + 1),
    )


def sum_ab_slope_ratio_y_discriminant_ledger(
    slope_x: Fraction | int,
    square_ratio: Fraction | int,
) -> SumAbSlopeRatioYDiscriminantLedger:
    """Return the ``y``-quadratic discriminant for ``P = KQ``.

    Here ``K`` is the square ratio ``P/Q``.  The discriminant has shape
    ``-4*inner``; viewing ``inner`` as a quadratic in ``K`` exposes the factor
    ``(x^2+1)(5x^2-4x+1)``.
    """
    x = _as_fraction(slope_x)
    k = _as_fraction(square_ratio)
    a = 1 - 2 * k
    b = -2 * k * x + 2 * k + 2 * x - 2
    c = -k * x * x + 2 * k * x - k + 2 * x * x - 2 * x + 1
    y_discriminant = b * b - 4 * a * c
    inner = -y_discriminant / 4
    inner_as_quadratic = (
        k * k * x * x
        - 2 * k * k * x
        + k * k
        - 3 * k * x * x
        + 2 * k * x
        - k
        + x * x
    )
    pythagorean_recovery_square = x * x + 1
    new_curve_factor = 5 * x * x - 4 * x + 1
    return SumAbSlopeRatioYDiscriminantLedger(
        slope_x=x,
        square_ratio=k,
        quadratic_coefficients=(a, b, c),
        y_discriminant=y_discriminant,
        y_discriminant_inner=inner,
        inner_as_quadratic_in_square_ratio=inner_as_quadratic,
        inner_square_ratio_discriminant=pythagorean_recovery_square
        * new_curve_factor,
        pythagorean_recovery_square=pythagorean_recovery_square,
        slope_x_is_pythagorean=_is_rational_square(pythagorean_recovery_square),
        new_curve_factor=new_curve_factor,
        new_curve_factor_is_square=_is_rational_square(new_curve_factor),
    )


def _sum_ab_new_curve_homogeneous_value(a: int, b: int) -> int:
    return 5 * a**4 + 8 * a**3 * b - 6 * a * a * b * b - 8 * a * b**3 + 5 * b**4


def sum_ab_new_curve_residue_summary(modulus: int) -> SumAbNewCurveResidueSummary:
    """Summarize square residues for the new quartic curve modulo ``modulus``."""
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    square_residues = {value * value % modulus for value in range(modulus)}
    primitive_classes = 0
    square_classes = 0
    boundary_square_classes = 0
    nonboundary_square_classes = 0
    boundary_examples: list[tuple[int, int, int]] = []
    nonboundary_examples: list[tuple[int, int, int]] = []

    for a in range(modulus):
        for b in range(modulus):
            if _gcd(_gcd(a, b), modulus) != 1:
                continue
            primitive_classes += 1
            value = _sum_ab_new_curve_homogeneous_value(a, b) % modulus
            if value not in square_residues:
                continue
            square_classes += 1
            is_boundary = (a - b) % modulus == 0 or (a + b) % modulus == 0
            row = (a, b, value)
            if is_boundary:
                boundary_square_classes += 1
                if len(boundary_examples) < 3:
                    boundary_examples.append(row)
            else:
                nonboundary_square_classes += 1
                if len(nonboundary_examples) < 3:
                    nonboundary_examples.append(row)

    return SumAbNewCurveResidueSummary(
        modulus=modulus,
        primitive_classes=primitive_classes,
        square_classes=square_classes,
        boundary_square_classes=boundary_square_classes,
        nonboundary_square_classes=nonboundary_square_classes,
        boundary_examples=tuple(boundary_examples),
        nonboundary_examples=tuple(nonboundary_examples),
    )


def sum_ab_new_curve_z_reduction(parameter_t: Fraction | int) -> SumAbNewCurveZReduction:
    """Return the ``z=t-1/t`` ledger for the new quartic curve."""
    t = _as_fraction(parameter_t)
    if t == 0:
        raise ValueError("parameter_t must be nonzero")
    original = 5 * t**4 + 8 * t**3 - 6 * t * t - 8 * t + 5
    z = t - 1 / t
    scaled = original / (t * t)
    new_curve_square = 5 * z * z + 8 * z + 4
    z_recovery_square = z * z + 4
    return SumAbNewCurveZReduction(
        parameter_t=t,
        z_value=z,
        original_quartic_value=original,
        scaled_quartic_value=scaled,
        z_recovery_square=z_recovery_square,
        new_curve_square=new_curve_square,
        identity_holds=scaled == new_curve_square,
        z_recovery_is_square=_is_rational_square(z_recovery_square),
        new_curve_is_square=_is_rational_square(new_curve_square),
    )


def sum_ab_z_lemma_centerline_bridge(
    parameter: Fraction | int,
) -> SumAbZLemmaCenterlineBridge:
    """Return the bridge from the ``z`` lemma to the centerline quartic."""
    m = _as_fraction(parameter)
    denominator = (m - 1) * (m + 1)
    if denominator == 0:
        raise ValueError("parameter must not be ±1")
    z = -4 * m / denominator
    denominator_square = denominator * denominator
    remaining = m**4 - 8 * m**3 + 18 * m * m + 8 * m + 1
    centerline_parameter = -m
    centerline_quartic = (
        centerline_parameter**4
        + 8 * centerline_parameter**3
        + 18 * centerline_parameter * centerline_parameter
        - 8 * centerline_parameter
        + 1
    )
    scaled_second_square = 5 * z * z + 8 * z + 4
    return SumAbZLemmaCenterlineBridge(
        parameter=m,
        z_value=z,
        denominator_square=denominator_square,
        scaled_second_square=scaled_second_square,
        remaining_quartic=remaining,
        centerline_parameter=centerline_parameter,
        centerline_quartic=centerline_quartic,
        identity_holds=(
            remaining == centerline_quartic
            and scaled_second_square == 4 * remaining / denominator_square
        ),
        remaining_quartic_is_square=_is_rational_square(remaining),
    )


def sum_ab_bridge_extra_factor_z_lemma_reduction(
    parameter_t: Fraction | int,
) -> SumAbBridgeExtraFactorZLemmaReduction:
    """Reduce the bridge extra-factor new curve to the centerline quartic."""
    t = _as_fraction(parameter_t)
    if t == 0:
        raise ValueError("parameter_t must be nonzero")
    if t == -1:
        raise ValueError("parameter_t must not be -1")

    z = t - 1 / t
    z_parameter_m = (t - 1) / (t + 1)
    new_curve_value_t = 5 * t**4 + 8 * t**3 - 6 * t * t - 8 * t + 5
    scaled_new_curve_value = new_curve_value_t / (t * t)
    z_recovery_square = z * z + 4
    z_lemma_new_curve_square = 5 * z * z + 8 * z + 4
    centerline_bridge = sum_ab_z_lemma_centerline_bridge(z_parameter_m)
    z_reduction_identity_holds = (
        scaled_new_curve_value == z_lemma_new_curve_square
        and z_recovery_square == (t + 1 / t) * (t + 1 / t)
        and centerline_bridge.z_value == z
    )
    centerline_bridge_identity_holds = centerline_bridge.identity_holds
    return SumAbBridgeExtraFactorZLemmaReduction(
        parameter_t=t,
        z_value=z,
        z_parameter_m=z_parameter_m,
        new_curve_value_t=new_curve_value_t,
        scaled_new_curve_value=scaled_new_curve_value,
        z_recovery_square=z_recovery_square,
        z_lemma_new_curve_square=z_lemma_new_curve_square,
        z_reduction_identity_holds=z_reduction_identity_holds,
        centerline_bridge=centerline_bridge,
        centerline_bridge_identity_holds=centerline_bridge_identity_holds,
        extra_factor_reduces_to_centerline=(
            z_reduction_identity_holds and centerline_bridge_identity_holds
        ),
    )


_BRIDGE_X_NUMERATOR_TERMS = (
    (1, 4, 4),
    (4, 4, 3),
    (2, 4, 2),
    (-4, 4, 1),
    (1, 4, 0),
    (4, 3, 4),
    (8, 3, 3),
    (-8, 3, 2),
    (-8, 3, 1),
    (4, 3, 0),
    (6, 2, 4),
    (-8, 2, 3),
    (-20, 2, 2),
    (8, 2, 1),
    (6, 2, 0),
    (-4, 1, 4),
    (-8, 1, 3),
    (8, 1, 2),
    (8, 1, 1),
    (-4, 1, 0),
    (1, 0, 4),
    (4, 0, 3),
    (2, 0, 2),
    (-4, 0, 1),
    (1, 0, 0),
)

_BRIDGE_Y_NUMERATOR_TERMS = (
    (1, 4, 4),
    (4, 4, 3),
    (6, 4, 2),
    (-4, 4, 1),
    (1, 4, 0),
    (4, 3, 4),
    (8, 3, 3),
    (-8, 3, 2),
    (-8, 3, 1),
    (4, 3, 0),
    (2, 2, 4),
    (-8, 2, 3),
    (-20, 2, 2),
    (8, 2, 1),
    (2, 2, 0),
    (-4, 1, 4),
    (-8, 1, 3),
    (8, 1, 2),
    (8, 1, 1),
    (-4, 1, 0),
    (1, 0, 4),
    (4, 0, 3),
    (6, 0, 2),
    (-4, 0, 1),
    (1, 0, 0),
)

_BRIDGE_EXTRA_FACTOR_TERMS = (
    (1, 2, 2),
    (1, 2, 1),
    (-1, 2, 0),
    (1, 1, 2),
    (-1, 1, 0),
    (-1, 0, 2),
    (-1, 0, 1),
    (1, 0, 0),
)


def _eval_bihomogeneous_terms_fraction(
    terms: tuple[tuple[int, int, int], ...],
    t_value: Fraction,
    u_value: Fraction,
) -> Fraction:
    return sum(
        Fraction(coefficient) * t_value**t_power * u_value**u_power
        for coefficient, t_power, u_power in terms
    )


def _rational_square_root_or_none(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator_root = isqrt(value.numerator)
    denominator_root = isqrt(value.denominator)
    if (
        numerator_root * numerator_root == value.numerator
        and denominator_root * denominator_root == value.denominator
    ):
        return Fraction(numerator_root, denominator_root)
    return None


def _is_rational_square(value: Fraction) -> bool:
    return _rational_square_root_or_none(value) is not None


def _is_odd_prime_local_square(value: Fraction, prime: int) -> bool:
    if prime <= 2:
        raise ValueError("prime must be an odd prime")
    if value == 0:
        return True
    valuation = _rational_valuation(value, prime)
    if valuation is None or valuation % 2:
        return False
    if valuation > 0:
        value /= prime**valuation
    elif valuation < 0:
        value *= prime ** (-valuation)
    unit = (value.numerator % prime) * pow(value.denominator % prime, -1, prime)
    return unit % prime in {residue * residue % prime for residue in range(prime)}


def _shifted_u_coefficients_fraction(
    terms: tuple[tuple[int, int, int], ...],
    t_value: Fraction,
    base_u: Fraction,
) -> tuple[Fraction, ...]:
    degree = max(u_power for _, _, u_power in terms)
    coefficients = [Fraction(0) for _ in range(degree + 1)]
    for coefficient, t_power, u_power in terms:
        for h_power in range(u_power + 1):
            coefficients[h_power] += (
                Fraction(coefficient)
                * t_value**t_power
                * Fraction(comb(u_power, h_power))
                * base_u ** (u_power - h_power)
            )
    return tuple(coefficients)


def sum_ab_dual_slope_bridge_centerline_branch_restrictions(
    parameter_t: Fraction | int,
) -> tuple[SumAbDualSlopeBridgeCenterlineBranchRestriction, ...]:
    """Restrict bridge numerator polynomials to the four centerline factors."""
    t = _as_fraction(parameter_t)
    if t == 0:
        raise ValueError("parameter_t must be nonzero")

    centerline_quartic = t**4 + 8 * t**3 + 18 * t * t - 8 * t + 1
    visible_square = (t - 1) * (t - 1) * (t + 1) * (t + 1)
    trivial_square = visible_square * (t * t + 1) * (t * t + 1)
    centerline_extra = (t - 1) * (t + 1) * (t * t + 2 * t - 1)
    branches = (
        (
            "t-u",
            "centerline-quartic",
            t,
            visible_square * centerline_quartic,
            centerline_extra,
        ),
        (
            "t+u",
            "trivial-square",
            -t,
            trivial_square,
            visible_square,
        ),
        (
            "tu-1",
            "trivial-square",
            1 / t,
            trivial_square / (t**4),
            -visible_square / (t * t),
        ),
        (
            "tu+1",
            "centerline-quartic",
            -1 / t,
            visible_square * centerline_quartic / (t**4),
            -centerline_extra / (t * t),
        ),
    )

    restrictions: list[SumAbDualSlopeBridgeCenterlineBranchRestriction] = []
    for (
        branch,
        restriction_kind,
        u_value,
        predicted_common,
        predicted_extra,
    ) in branches:
        x_numerator = _eval_bihomogeneous_terms_fraction(
            _BRIDGE_X_NUMERATOR_TERMS,
            t,
            u_value,
        )
        y_numerator = _eval_bihomogeneous_terms_fraction(
            _BRIDGE_Y_NUMERATOR_TERMS,
            t,
            u_value,
        )
        extra_factor = _eval_bihomogeneous_terms_fraction(
            _BRIDGE_EXTRA_FACTOR_TERMS,
            t,
            u_value,
        )
        restrictions.append(
            SumAbDualSlopeBridgeCenterlineBranchRestriction(
                branch=branch,
                restriction_kind=restriction_kind,
                parameter_t=t,
                parameter_u=u_value,
                x_bridge_numerator=x_numerator,
                y_bridge_numerator=y_numerator,
                common_bridge_numerator=x_numerator,
                predicted_common_bridge_numerator=predicted_common,
                extra_factor=extra_factor,
                predicted_extra_factor=predicted_extra,
                bridge_numerators_equal=x_numerator == y_numerator,
                common_identity_holds=(
                    x_numerator == y_numerator == predicted_common
                ),
                extra_identity_holds=extra_factor == predicted_extra,
            )
        )

    return tuple(restrictions)


def sum_ab_dual_slope_bridge_trivial_tube_expansions(
    parameter_t: Fraction | int,
) -> tuple[SumAbDualSlopeBridgeTrivialTubeExpansion, ...]:
    """Expand bridge numerators at the two trivial-square centerline tubes."""
    t = _as_fraction(parameter_t)
    if t == 0:
        raise ValueError("parameter_t must be nonzero")

    expansions: list[SumAbDualSlopeBridgeTrivialTubeExpansion] = []
    for branch, base_u in (("t+u", -t), ("tu-1", 1 / t)):
        x_coefficients = _shifted_u_coefficients_fraction(
            _BRIDGE_X_NUMERATOR_TERMS,
            t,
            base_u,
        )
        y_coefficients = _shifted_u_coefficients_fraction(
            _BRIDGE_Y_NUMERATOR_TERMS,
            t,
            base_u,
        )
        extra_coefficients = _shifted_u_coefficients_fraction(
            _BRIDGE_EXTRA_FACTOR_TERMS,
            t,
            base_u,
        )
        difference_coefficients = tuple(
            x_coefficient - y_coefficient
            for x_coefficient, y_coefficient in zip(
                x_coefficients,
                y_coefficients,
                strict=True,
            )
        )
        common_constant = x_coefficients[0]
        common_constant_square_root = _rational_square_root_or_none(
            common_constant
        )
        expansions.append(
            SumAbDualSlopeBridgeTrivialTubeExpansion(
                branch=branch,
                parameter_t=t,
                base_u=base_u,
                x_coefficients=x_coefficients,
                y_coefficients=y_coefficients,
                extra_coefficients=extra_coefficients,
                difference_coefficients=difference_coefficients,
                bridge_constants_equal=common_constant == y_coefficients[0],
                common_constant=common_constant,
                common_constant_square_root=common_constant_square_root,
                common_constant_is_square=common_constant_square_root is not None,
                nonzero_square_constant=(
                    common_constant != 0 and common_constant_square_root is not None
                ),
            )
        )

    return tuple(expansions)


def sum_ab_dual_slope_centerline_factor_positive_domain(
    parameter_t: Fraction | int,
) -> tuple[SumAbDualSlopeCenterlineFactorPositiveDomainRow, ...]:
    """Classify exact centerline-factor branches in the positive parameter domain."""
    t = _as_fraction(parameter_t)
    if t == 0:
        raise ValueError("parameter_t must be nonzero")

    dual_x = (1 - t * t) / (2 * t)
    restrictions = sum_ab_dual_slope_bridge_centerline_branch_restrictions(t)
    rows: list[SumAbDualSlopeCenterlineFactorPositiveDomainRow] = []
    for restriction in restrictions:
        u = restriction.parameter_u
        parameter_u_in_unit_interval = 0 < u < 1
        dual_slope_y: Fraction | None = None
        dual_slope_y_positive = False
        dual_denominator: Fraction | None = None
        dual_denominator_positive = False
        if u != 0:
            dual_slope_y = (1 - u * u) / (2 * u)
            dual_slope_y_positive = dual_slope_y > 0
            dual_denominator = dual_x + dual_slope_y - dual_x * dual_slope_y
            dual_denominator_positive = dual_denominator > 0
        rows.append(
            SumAbDualSlopeCenterlineFactorPositiveDomainRow(
                branch=restriction.branch,
                restriction_kind=restriction.restriction_kind,
                parameter_t=t,
                parameter_u=u,
                parameter_u_in_unit_interval=parameter_u_in_unit_interval,
                dual_slope_y=dual_slope_y,
                dual_slope_y_positive=dual_slope_y_positive,
                dual_denominator=dual_denominator,
                dual_denominator_positive=dual_denominator_positive,
                admissible_positive_parameterization=(
                    0 < t < 1
                    and parameter_u_in_unit_interval
                    and dual_x > 0
                    and dual_slope_y_positive
                    and dual_denominator_positive
                ),
            )
        )

    return tuple(rows)


def sum_ab_dual_slope_positive_trivial_tube_local_witnesses(
) -> tuple[SumAbDualSlopePositiveTrivialTubeLocalWitness, ...]:
    """Return positive 5-adic tube witnesses for the local-square gap."""
    prime = 5
    samples = (
        ("t+u", Fraction(1, 4), Fraction(19, 24)),
        ("tu-1", Fraction(1, 4), Fraction(7, 8)),
    )
    witnesses: list[SumAbDualSlopePositiveTrivialTubeLocalWitness] = []
    for branch, t, u in samples:
        parameterization = sum_ab_dual_slope_parameterization(t, u)
        tube_value = t + u if branch == "t+u" else t * u - 1
        tube_valuation = _rational_valuation(tube_value, prime)
        if tube_valuation is None:
            raise ValueError("tube value must be nonzero")
        recovery_values = (
            parameterization.generated_x_recovery_value,
            parameterization.generated_y_recovery_value,
        )
        local_square_flags = tuple(
            _is_odd_prime_local_square(value, prime) for value in recovery_values
        )
        rational_square_flags = tuple(
            _is_rational_square(value) for value in recovery_values
        )
        witnesses.append(
            SumAbDualSlopePositiveTrivialTubeLocalWitness(
                branch=branch,
                prime=prime,
                parameter_t=t,
                parameter_u=u,
                tube_value=tube_value,
                tube_valuation=tube_valuation,
                dual_denominator=parameterization.dual_denominator,
                generated_slopes=(
                    parameterization.generated_x,
                    parameterization.generated_y,
                ),
                recovery_values=recovery_values,
                local_square_flags=local_square_flags,
                rational_square_flags=rational_square_flags,
                admissible_positive_parameterization=(
                    0 < t < 1
                    and 0 < u < 1
                    and parameterization.dual_slope_x > 0
                    and parameterization.dual_slope_y > 0
                    and parameterization.dual_denominator > 0
                ),
                recovery_values_are_local_squares=all(local_square_flags),
                recovery_values_are_rational_squares=all(rational_square_flags),
            )
        )

    return tuple(witnesses)


def sum_ab_dual_slope_positive_trivial_tube_squareclass_ledgers(
) -> tuple[SumAbDualSlopePositiveTrivialTubeSquareclassLedger, ...]:
    """Record global squareclass obstructions for trivial-tube witnesses."""
    ledgers: list[SumAbDualSlopePositiveTrivialTubeSquareclassLedger] = []
    for witness in sum_ab_dual_slope_positive_trivial_tube_local_witnesses():
        squareclass_data = tuple(
            _rational_squareclass(value) for value in witness.recovery_values
        )
        recovery_squareclasses = tuple(
            squareclass for squareclass, _ in squareclass_data
        )
        recovery_squareclass_primes = tuple(primes for _, primes in squareclass_data)
        all_primes = tuple(
            sorted(
                {
                    prime
                    for primes in recovery_squareclass_primes
                    for prime in primes
                }
            )
        )
        one_mod_four_squareclass_primes = tuple(
            prime for prime in all_primes if prime % 4 == 1
        )
        three_mod_four_squareclass_primes = tuple(
            prime for prime in all_primes if prime % 4 == 3
        )
        ledgers.append(
            SumAbDualSlopePositiveTrivialTubeSquareclassLedger(
                witness=witness,
                recovery_squareclasses=recovery_squareclasses,  # type: ignore[arg-type]
                recovery_squareclass_primes=recovery_squareclass_primes,  # type: ignore[arg-type]
                one_mod_four_squareclass_primes=one_mod_four_squareclass_primes,
                three_mod_four_squareclass_primes=three_mod_four_squareclass_primes,
                all_squareclass_primes_are_one_mod_four=(
                    bool(all_primes) and all_primes == one_mod_four_squareclass_primes
                ),
            )
        )

    return tuple(ledgers)


def sum_ab_dual_slope_positive_trivial_tube_member_ledgers(
) -> tuple[SumAbDualSlopePositiveTrivialTubeMemberLedger, ...]:
    """Record full ``R_lambda`` member terms for trivial-tube witnesses."""
    ledgers: list[SumAbDualSlopePositiveTrivialTubeMemberLedger] = []
    for witness in sum_ab_dual_slope_positive_trivial_tube_local_witnesses():
        parameterization = sum_ab_dual_slope_parameterization(
            witness.parameter_t,
            witness.parameter_u,
        )
        common_leg = parameterization.common_leg
        lambda_ratio = 1 / common_leg
        r_ratio = parameterization.generated_x / common_leg
        s_ratio = parameterization.generated_y / common_leg
        member_values = (
            r_ratio * r_ratio + 1,
            s_ratio * s_ratio + 1,
            r_ratio * r_ratio + lambda_ratio * lambda_ratio,
            s_ratio * s_ratio + lambda_ratio * lambda_ratio,
        )
        squareclass_data = tuple(
            _rational_squareclass(value) for value in member_values
        )
        member_squareclasses = tuple(
            squareclass for squareclass, _ in squareclass_data
        )
        member_squareclass_primes = tuple(primes for _, primes in squareclass_data)
        all_primes = tuple(
            sorted(
                {
                    prime
                    for primes in member_squareclass_primes
                    for prime in primes
                }
            )
        )
        one_mod_four_member_squareclass_primes = tuple(
            prime for prime in all_primes if prime % 4 == 1
        )
        three_mod_four_member_squareclass_primes = tuple(
            prime for prime in all_primes if prime % 4 == 3
        )
        unit_terms_are_squares = member_squareclasses[:2] == (1, 1)
        lambda_terms_are_squares = member_squareclasses[2:] == (1, 1)
        ledgers.append(
            SumAbDualSlopePositiveTrivialTubeMemberLedger(
                witness=witness,
                lambda_ratio=lambda_ratio,
                ratios=(r_ratio, s_ratio),
                product=r_ratio * s_ratio,
                member_values=member_values,
                member_squareclasses=member_squareclasses,  # type: ignore[arg-type]
                member_squareclass_primes=member_squareclass_primes,  # type: ignore[arg-type]
                one_mod_four_member_squareclass_primes=(
                    one_mod_four_member_squareclass_primes
                ),
                three_mod_four_member_squareclass_primes=(
                    three_mod_four_member_squareclass_primes
                ),
                closes_sum_ab=r_ratio + s_ratio == lambda_ratio + 1,
                unit_terms_are_squares=unit_terms_are_squares,
                lambda_terms_are_squares=lambda_terms_are_squares,
                true_member_pair=unit_terms_are_squares and lambda_terms_are_squares,
            )
        )

    return tuple(ledgers)


def _eval_bihomogeneous_terms_mod(
    terms: tuple[tuple[int, int, int], ...],
    degree_t: int,
    degree_u: int,
    t_num: int,
    t_den: int,
    u_num: int,
    u_den: int,
    modulus: int,
) -> int:
    value = 0
    for coefficient, t_power, u_power in terms:
        term = coefficient % modulus
        term *= pow(t_num, t_power, modulus)
        term *= pow(t_den, degree_t - t_power, modulus)
        term *= pow(u_num, u_power, modulus)
        term *= pow(u_den, degree_u - u_power, modulus)
        value = (value + term) % modulus
    return value


def _projective_line_classes(modulus: int) -> tuple[tuple[int, int], ...]:
    return (*((value, 1) for value in range(modulus)), (1, 0))


def _local_projective_line_classes(
    prime: int,
    exponent: int,
) -> tuple[tuple[int, int], ...]:
    modulus = prime**exponent
    return (
        *((value, 1) for value in range(modulus)),
        *((1, prime * value) for value in range(prime ** (exponent - 1))),
    )


def _truncated_mod_valuation(value: int, prime: int, exponent: int) -> int:
    modulus = prime**exponent
    value %= modulus
    if value == 0:
        return exponent
    valuation = 0
    while value % prime == 0:
        valuation += 1
        value //= prime
    return valuation


def _bridge_centerline_factor_mod(
    t_num: int,
    t_den: int,
    u_num: int,
    u_den: int,
    modulus: int,
) -> int:
    return (
        (t_num * u_den - t_den * u_num)
        * (t_num * u_den + t_den * u_num)
        * (t_num * u_num - t_den * u_den)
        * (t_num * u_num + t_den * u_den)
    ) % modulus


def _bridge_centerline_factor_components_mod(
    t_num: int,
    t_den: int,
    u_num: int,
    u_den: int,
    modulus: int,
) -> tuple[int, int, int, int]:
    return (
        (t_num * u_den - t_den * u_num) % modulus,
        (t_num * u_den + t_den * u_num) % modulus,
        (t_num * u_num - t_den * u_den) % modulus,
        (t_num * u_num + t_den * u_den) % modulus,
    )


def sum_ab_dual_slope_bridge_projective_residue_summary(
    modulus: int,
) -> SumAbDualSlopeBridgeProjectiveResidueSummary:
    """Count projective residue classes for both cross-bridge square tests."""
    if modulus <= 2:
        raise ValueError("modulus must be an odd prime")
    factors = factorint(modulus)
    if len(factors) != 1 or next(iter(factors.values())) != 1:
        raise ValueError("modulus must be an odd prime")

    square_residues = {value * value % modulus for value in range(modulus)}
    projective_classes = _projective_line_classes(modulus)
    both_bridge_square_classes = 0
    centerline_square_classes = 0
    noncenter_square_classes = 0
    noncenter_extra_factor_zero_classes = 0
    noncenter_extra_factor_nonzero_classes = 0
    noncenter_extra_factor_nonzero_examples: list[tuple[int, ...]] = []

    for t_num, t_den in projective_classes:
        for u_num, u_den in projective_classes:
            x_value = _eval_bihomogeneous_terms_mod(
                _BRIDGE_X_NUMERATOR_TERMS,
                4,
                4,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            y_value = _eval_bihomogeneous_terms_mod(
                _BRIDGE_Y_NUMERATOR_TERMS,
                4,
                4,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            if x_value not in square_residues or y_value not in square_residues:
                continue

            both_bridge_square_classes += 1
            centerline_factor = _bridge_centerline_factor_mod(
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            extra_factor = _eval_bihomogeneous_terms_mod(
                _BRIDGE_EXTRA_FACTOR_TERMS,
                2,
                2,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            if centerline_factor == 0:
                centerline_square_classes += 1
                continue

            noncenter_square_classes += 1
            if extra_factor == 0:
                noncenter_extra_factor_zero_classes += 1
                continue

            noncenter_extra_factor_nonzero_classes += 1
            if len(noncenter_extra_factor_nonzero_examples) < 5:
                noncenter_extra_factor_nonzero_examples.append(
                    (
                        t_num,
                        t_den,
                        u_num,
                        u_den,
                        x_value,
                        y_value,
                        centerline_factor,
                        extra_factor,
                    )
                )

    return SumAbDualSlopeBridgeProjectiveResidueSummary(
        modulus=modulus,
        projective_class_count=len(projective_classes) ** 2,
        both_bridge_square_classes=both_bridge_square_classes,
        centerline_square_classes=centerline_square_classes,
        noncenter_square_classes=noncenter_square_classes,
        noncenter_extra_factor_zero_classes=noncenter_extra_factor_zero_classes,
        noncenter_extra_factor_nonzero_classes=(
            noncenter_extra_factor_nonzero_classes
        ),
        noncenter_extra_factor_nonzero_examples=tuple(
            noncenter_extra_factor_nonzero_examples
        ),
    )


def sum_ab_dual_slope_bridge_prime_power_lift_summary(
    prime: int,
    exponent: int,
) -> SumAbDualSlopeBridgePrimePowerLiftSummary:
    """Count prime-power bridge-square lifts by ``(v_p(C), v_p(E))``."""
    if prime <= 2:
        raise ValueError("prime must be an odd prime")
    factors = factorint(prime)
    if len(factors) != 1 or next(iter(factors.values())) != 1:
        raise ValueError("prime must be an odd prime")
    if exponent <= 0:
        raise ValueError("exponent must be positive")

    modulus = prime**exponent
    square_residues = {value * value % modulus for value in range(modulus)}
    projective_classes = _local_projective_line_classes(prime, exponent)
    valuation_pair_counts: dict[tuple[int, int], int] = {}
    both_bridge_square_classes = 0

    for t_num, t_den in projective_classes:
        for u_num, u_den in projective_classes:
            x_value = _eval_bihomogeneous_terms_mod(
                _BRIDGE_X_NUMERATOR_TERMS,
                4,
                4,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            y_value = _eval_bihomogeneous_terms_mod(
                _BRIDGE_Y_NUMERATOR_TERMS,
                4,
                4,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            if x_value not in square_residues or y_value not in square_residues:
                continue

            both_bridge_square_classes += 1
            centerline_factor = _bridge_centerline_factor_mod(
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            extra_factor = _eval_bihomogeneous_terms_mod(
                _BRIDGE_EXTRA_FACTOR_TERMS,
                2,
                2,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            valuation_pair = (
                _truncated_mod_valuation(centerline_factor, prime, exponent),
                _truncated_mod_valuation(extra_factor, prime, exponent),
            )
            valuation_pair_counts[valuation_pair] = (
                valuation_pair_counts.get(valuation_pair, 0) + 1
            )

    centerline_unit_entries = [
        (extra_valuation, count)
        for (centerline_valuation, extra_valuation), count in valuation_pair_counts.items()
        if centerline_valuation == 0
    ]
    centerline_unit_classes = sum(count for _, count in centerline_unit_entries)
    return SumAbDualSlopeBridgePrimePowerLiftSummary(
        prime=prime,
        exponent=exponent,
        modulus=modulus,
        projective_class_count=len(projective_classes) ** 2,
        both_bridge_square_classes=both_bridge_square_classes,
        valuation_pair_counts=dict(sorted(valuation_pair_counts.items())),
        centerline_unit_extra_unit_classes=valuation_pair_counts.get((0, 0), 0),
        centerline_unit_classes=centerline_unit_classes,
        centerline_unit_min_extra_valuation=(
            min(extra_valuation for extra_valuation, _ in centerline_unit_entries)
            if centerline_unit_entries
            else None
        ),
    )


def sum_ab_dual_slope_bridge_centerline_factor_lift_summary(
    prime: int,
    exponent: int,
) -> SumAbDualSlopeBridgeCenterlineFactorLiftSummary:
    """Count bridge-square lifts by the four centerline-factor valuations."""
    if prime <= 2:
        raise ValueError("prime must be an odd prime")
    factors = factorint(prime)
    if len(factors) != 1 or next(iter(factors.values())) != 1:
        raise ValueError("prime must be an odd prime")
    if exponent <= 0:
        raise ValueError("exponent must be positive")

    modulus = prime**exponent
    square_residues = {value * value % modulus for value in range(modulus)}
    projective_classes = _local_projective_line_classes(prime, exponent)
    factor_extra_valuation_counts: Counter[tuple[int, int, int, int, int]] = (
        Counter()
    )
    centerline_factor_valuation_counts: Counter[tuple[int, int, int, int]] = Counter()
    max_centerline_factor_extra_valuation_counts: Counter[tuple[int, int]] = (
        Counter()
    )
    both_bridge_square_classes = 0

    for t_num, t_den in projective_classes:
        for u_num, u_den in projective_classes:
            x_value = _eval_bihomogeneous_terms_mod(
                _BRIDGE_X_NUMERATOR_TERMS,
                4,
                4,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            y_value = _eval_bihomogeneous_terms_mod(
                _BRIDGE_Y_NUMERATOR_TERMS,
                4,
                4,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            if x_value not in square_residues or y_value not in square_residues:
                continue

            both_bridge_square_classes += 1
            factor_values = _bridge_centerline_factor_components_mod(
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            factor_valuations = tuple(
                _truncated_mod_valuation(value, prime, exponent)
                for value in factor_values
            )
            extra_factor = _eval_bihomogeneous_terms_mod(
                _BRIDGE_EXTRA_FACTOR_TERMS,
                2,
                2,
                t_num,
                t_den,
                u_num,
                u_den,
                modulus,
            )
            extra_valuation = _truncated_mod_valuation(
                extra_factor,
                prime,
                exponent,
            )
            factor_extra_valuation = (*factor_valuations, extra_valuation)
            factor_extra_valuation_counts[factor_extra_valuation] += 1
            centerline_factor_valuation_counts[factor_valuations] += 1
            max_centerline_factor_extra_valuation_counts[
                (max(factor_valuations), extra_valuation)
            ] += 1

    return SumAbDualSlopeBridgeCenterlineFactorLiftSummary(
        prime=prime,
        exponent=exponent,
        modulus=modulus,
        projective_class_count=len(projective_classes) ** 2,
        both_bridge_square_classes=both_bridge_square_classes,
        factor_extra_valuation_counts=dict(
            sorted(factor_extra_valuation_counts.items())
        ),
        centerline_factor_valuation_counts=dict(
            sorted(centerline_factor_valuation_counts.items())
        ),
        max_centerline_factor_extra_valuation_counts=dict(
            sorted(max_centerline_factor_extra_valuation_counts.items())
        ),
    )


def sum_ab_k_discriminant_quartic_completion(
    parameter: Fraction | int,
    square_ratio: Fraction | int,
) -> SumAbKDiscriminantQuarticCompletion:
    """Return the square-completion identity for the remaining ``K`` quartic."""
    a = _as_fraction(parameter)
    k = _as_fraction(square_ratio)
    centerline_quartic = a**4 + 8 * a**3 + 18 * a * a - 8 * a + 1
    shared_factor = a * a + 2 * a - 1
    linear_factor = a * a + 4 * a - 1
    remaining = (
        centerline_quartic * k * k
        - 4 * shared_factor * linear_factor * k
        + 4 * shared_factor * shared_factor
    )
    linear_square_term = 2 * centerline_quartic * k - 4 * shared_factor * linear_factor
    positive_square_term = 8 * a * shared_factor
    positive_remainder = positive_square_term * positive_square_term
    left_side = 4 * centerline_quartic * remaining
    right_side = linear_square_term * linear_square_term + positive_remainder
    return SumAbKDiscriminantQuarticCompletion(
        parameter=a,
        square_ratio=k,
        centerline_quartic=centerline_quartic,
        remaining_quartic=remaining,
        linear_square_term=linear_square_term,
        positive_square_term=positive_square_term,
        positive_remainder=positive_remainder,
        left_side=left_side,
        right_side=right_side,
        identity_holds=left_side == right_side,
    )


def sum_ab_k_square_candidate_y_discriminant(
    parameter: Fraction | int,
    square_ratio: Fraction | int,
) -> SumAbKSquareCandidateYDiscriminant:
    """Separate the ``K``-quartic square layer from the actual ``y`` roots."""
    a = _as_fraction(parameter)
    k = _as_fraction(square_ratio)
    if a == 0:
        raise ValueError("parameter must be nonzero")
    x = (1 - a * a) / (2 * a)
    completion = sum_ab_k_discriminant_quartic_completion(a, k)
    y_a = 1 - 2 * k
    y_b = -2 * k * x + 2 * k + 2 * x - 2
    y_c = -k * x * x + 2 * k * x - k + 2 * x * x - 2 * x + 1
    y_discriminant = y_b * y_b - 4 * y_a * y_c
    return SumAbKSquareCandidateYDiscriminant(
        parameter=a,
        slope_x=x,
        square_ratio=k,
        square_ratio_is_square=_is_rational_square(k),
        remaining_quartic=completion.remaining_quartic,
        remaining_quartic_is_square=_is_rational_square(completion.remaining_quartic),
        y_discriminant=y_discriminant,
        y_discriminant_is_square=_is_rational_square(y_discriminant),
    )


def sum_ab_k_square_y_discriminant_factorization(
    parameter: Fraction | int,
    square_ratio_root: Fraction | int,
) -> SumAbKSquareYDiscriminantFactorization:
    """Return the actual ``y`` discriminant split after writing ``K=k^2``.

    With ``x=(1-a^2)/(2a)`` and ``K=k^2``, the discriminant of ``P=KQ`` as a
    quadratic in ``y`` factors as ``-F_-(a,k)F_+(a,k)/a^2``.  The two factors
    have the same discriminant in ``k``: the new quartic from the outer
    ``K``-discriminant entry.
    """
    a = _as_fraction(parameter)
    k = _as_fraction(square_ratio_root)
    if a == 0:
        raise ValueError("parameter must be nonzero")
    x = (1 - a * a) / (2 * a)
    square_ratio = k * k
    candidate = sum_ab_k_square_candidate_y_discriminant(a, square_ratio)
    minus_factor = (
        a * a * k * k
        - a * a * k
        - a * a
        + 2 * a * k * k
        - k * k
        - k
        + 1
    )
    plus_factor = (
        a * a * k * k
        + a * a * k
        - a * a
        + 2 * a * k * k
        - k * k
        + k
        + 1
    )
    factorized = -minus_factor * plus_factor / (a * a)
    shared_discriminant = 5 * a**4 + 8 * a**3 - 6 * a * a - 8 * a + 5
    return SumAbKSquareYDiscriminantFactorization(
        parameter=a,
        slope_x=x,
        square_ratio_root=k,
        square_ratio=square_ratio,
        minus_factor=minus_factor,
        plus_factor=plus_factor,
        y_discriminant=candidate.y_discriminant,
        factorized_y_discriminant=factorized,
        factorization_holds=factorized == candidate.y_discriminant,
        shared_factor_discriminant=shared_discriminant,
        shared_factor_discriminant_is_square=_is_rational_square(shared_discriminant),
    )


def _n_descending_edge_stats(
    family_edges_by_squareclass: dict[int, tuple[SumAbSquareclassFamilyEdge, ...]],
) -> tuple[int, int]:
    descending_edges = [
        edge
        for edges in family_edges_by_squareclass.values()
        for edge in edges
        if edge.decreases_n
    ]
    sources_with_descending_edge = {edge.source for edge in descending_edges}
    continuations = sum(
        1 for edge in descending_edges if edge.target in sources_with_descending_edge
    )
    return len(descending_edges), continuations


def _squareclass_family_edges(
    canonical_triples: tuple[tuple[int, int, int], ...],
) -> tuple[SumAbSquareclassFamilyEdge, ...]:
    edges: list[SumAbSquareclassFamilyEdge] = []
    for source in canonical_triples:
        source_n, source_p, source_q = source
        for target in canonical_triples:
            if source == target:
                continue
            target_n, target_p, target_q = target
            target_uses_source_failed_leg = target_n in (source_p, source_q)
            target_uses_source_shared_leg = source_n in (target_p, target_q)
            if target_uses_source_failed_leg and target_uses_source_shared_leg:
                edges.append(
                    SumAbSquareclassFamilyEdge(
                        source=source,
                        target=target,
                        target_uses_source_failed_leg=target_uses_source_failed_leg,
                        target_uses_source_shared_leg=target_uses_source_shared_leg,
                    )
                )
    return tuple(edges)


def _primitive_euclid_params(max_m: int) -> tuple[tuple[int, int], ...]:
    params: list[tuple[int, int]] = []
    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue
            if _gcd(m, n) != 1:
                continue
            params.append((m, n))
    return tuple(params)


def _leg_terms_mod(
    m: int,
    n: int,
    orientation: str,
    modulus: int,
) -> tuple[int, int]:
    odd_leg = (m * m - n * n) % modulus
    even_leg = (2 * m * n) % modulus
    if orientation == "odd":
        return odd_leg, even_leg
    if orientation == "even":
        return even_leg, odd_leg
    raise ValueError("orientation must be 'odd' or 'even'")


def _euclid_param_residue_passes_primitive_filters(
    m: int,
    n: int,
    modulus: int,
) -> bool:
    return _gcd(_gcd(m, n), modulus) == 1 and (m - n) % 2 != 0


def _terms_square_sum_is_residue_mod(
    terms: tuple[int, int],
    square_residues: set[int],
    modulus: int,
) -> bool:
    numerator, denominator = terms
    square_sum = (numerator * numerator + denominator * denominator) % modulus
    return square_sum in square_residues


def _empty_residue_summary(
    *,
    modulus: int,
    slope_orientation: str,
    scaled_term_orientation: str,
) -> SumAbEuclidResidueSummary:
    return SumAbEuclidResidueSummary(
        modulus=modulus,
        slope_orientation=slope_orientation,
        scaled_term_orientation=scaled_term_orientation,
        total_classes=0,
        other_square_classes=0,
        failed_square_classes=0,
        both_square_classes=0,
        other_only_classes=0,
        failed_only_classes=0,
        neither_square_classes=0,
    )


def sum_ab_euclid_residue_summaries(
    *,
    modulus: int,
) -> tuple[SumAbEuclidResidueSummary, ...]:
    """Count square-residue obstructions for the four orientation cases.

    The enumeration is intentionally residue-only: it does not impose
    primitivity, positivity, or ``m > n``.  That makes the result a conservative
    modular diagnostic rather than a proof over the original integer domain.
    """
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    square_residues = {value * value % modulus for value in range(modulus)}
    summaries: list[SumAbEuclidResidueSummary] = []
    for slope_orientation in ("odd", "even"):
        for scaled_term_orientation in ("odd", "even"):
            total_classes = 0
            other_square_classes = 0
            failed_square_classes = 0
            both_square_classes = 0
            other_only_classes = 0
            failed_only_classes = 0
            neither_square_classes = 0
            for m in range(modulus):
                for n in range(modulus):
                    slope_terms = _leg_terms_mod(m, n, slope_orientation, modulus)
                    for u in range(modulus):
                        for v in range(modulus):
                            scaled_term_terms = _leg_terms_mod(
                                u,
                                v,
                                scaled_term_orientation,
                                modulus,
                            )
                            other_terms, failed_terms = (
                                _sum_ab_mobius_polynomial_terms_from_legs(
                                    slope_terms,
                                    scaled_term_terms,
                                )
                            )
                            other_square = _terms_square_sum_is_residue_mod(
                                other_terms,
                                square_residues,
                                modulus,
                            )
                            failed_square = _terms_square_sum_is_residue_mod(
                                failed_terms,
                                square_residues,
                                modulus,
                            )
                            total_classes += 1
                            other_square_classes += int(other_square)
                            failed_square_classes += int(failed_square)
                            both_square_classes += int(other_square and failed_square)
                            other_only_classes += int(other_square and not failed_square)
                            failed_only_classes += int(failed_square and not other_square)
                            neither_square_classes += int(
                                not other_square and not failed_square
                            )
            summaries.append(
                SumAbEuclidResidueSummary(
                    modulus=modulus,
                    slope_orientation=slope_orientation,
                    scaled_term_orientation=scaled_term_orientation,
                    total_classes=total_classes,
                    other_square_classes=other_square_classes,
                    failed_square_classes=failed_square_classes,
                    both_square_classes=both_square_classes,
                    other_only_classes=other_only_classes,
                    failed_only_classes=failed_only_classes,
                    neither_square_classes=neither_square_classes,
                )
            )
    return tuple(summaries)


def sum_ab_euclid_conditional_residue_summaries(
    *,
    modulus: int,
) -> tuple[SumAbEuclidResidueSummary, ...]:
    """Count residue classes after primitive/parity/denominator filters.

    This is a stricter diagnostic than :func:`sum_ab_euclid_residue_summaries`.
    It keeps only residue classes with primitive-compatible Euclid parameters,
    opposite parity, nonzero selected leg denominators, and nonzero reconstructed
    polynomial denominators modulo ``modulus``.
    """
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")
    square_residues = {value * value % modulus for value in range(modulus)}
    summaries: list[SumAbEuclidResidueSummary] = []
    for slope_orientation in ("odd", "even"):
        for scaled_term_orientation in ("odd", "even"):
            summary = _empty_residue_summary(
                modulus=modulus,
                slope_orientation=slope_orientation,
                scaled_term_orientation=scaled_term_orientation,
            )
            total_classes = 0
            other_square_classes = 0
            failed_square_classes = 0
            both_square_classes = 0
            other_only_classes = 0
            failed_only_classes = 0
            neither_square_classes = 0
            for m in range(modulus):
                for n in range(modulus):
                    if not _euclid_param_residue_passes_primitive_filters(m, n, modulus):
                        continue
                    slope_terms = _leg_terms_mod(m, n, slope_orientation, modulus)
                    _, slope_denominator = slope_terms
                    if slope_denominator == 0:
                        continue
                    for u in range(modulus):
                        for v in range(modulus):
                            if not _euclid_param_residue_passes_primitive_filters(
                                u,
                                v,
                                modulus,
                            ):
                                continue
                            scaled_term_terms = _leg_terms_mod(
                                u,
                                v,
                                scaled_term_orientation,
                                modulus,
                            )
                            _, scaled_term_denominator = scaled_term_terms
                            if scaled_term_denominator == 0:
                                continue
                            other_terms, failed_terms = (
                                _sum_ab_mobius_polynomial_terms_from_legs(
                                    slope_terms,
                                    scaled_term_terms,
                                )
                            )
                            _, other_denominator = other_terms
                            _, failed_denominator = failed_terms
                            if (
                                other_denominator % modulus == 0
                                or failed_denominator % modulus == 0
                            ):
                                continue
                            other_square = _terms_square_sum_is_residue_mod(
                                other_terms,
                                square_residues,
                                modulus,
                            )
                            failed_square = _terms_square_sum_is_residue_mod(
                                failed_terms,
                                square_residues,
                                modulus,
                            )
                            total_classes += 1
                            other_square_classes += int(other_square)
                            failed_square_classes += int(failed_square)
                            both_square_classes += int(other_square and failed_square)
                            other_only_classes += int(other_square and not failed_square)
                            failed_only_classes += int(failed_square and not other_square)
                            neither_square_classes += int(
                                not other_square and not failed_square
                            )
            summaries.append(
                SumAbEuclidResidueSummary(
                    modulus=summary.modulus,
                    slope_orientation=summary.slope_orientation,
                    scaled_term_orientation=summary.scaled_term_orientation,
                    total_classes=total_classes,
                    other_square_classes=other_square_classes,
                    failed_square_classes=failed_square_classes,
                    both_square_classes=both_square_classes,
                    other_only_classes=other_only_classes,
                    failed_only_classes=failed_only_classes,
                    neither_square_classes=neither_square_classes,
                )
            )
    return tuple(summaries)


def _sum_ab_slope_obstruction_with_squareclass_cache(
    slope1: Fraction | int,
    slope2: Fraction | int,
    squareclass_cache: dict[Fraction, LegRatioSquareclass],
) -> SumAbSlopeObstruction | None:
    point = sum_ab_point_from_slopes(slope1, slope2)
    if point is None:
        return None
    terms = (
        ("slope1", point.slope1),
        ("slope2", point.slope2),
        ("r1", point.r1),
        ("r2", point.r2),
    )
    diagnostics = tuple(
        (name, _cached_leg_ratio_squareclass(value, squareclass_cache)) for name, value in terms
    )
    return SumAbSlopeObstruction(
        lambda_ratio=point.lambda_ratio,
        slope1=point.slope1,
        slope2=point.slope2,
        r1=point.r1,
        r2=point.r2,
        failed_terms=tuple(name for name, diagnostic in diagnostics if not diagnostic.is_square),
        passed_terms=tuple(name for name, diagnostic in diagnostics if diagnostic.is_square),
        term_squareclasses=tuple(
            (name, diagnostic.squarefree_part) for name, diagnostic in diagnostics
        ),
    )


def _cached_leg_ratio_squareclass(
    ratio: Fraction,
    squareclass_cache: dict[Fraction, LegRatioSquareclass],
) -> LegRatioSquareclass:
    if ratio not in squareclass_cache:
        squareclass_cache[ratio] = leg_ratio_squareclass(ratio)
    return squareclass_cache[ratio]


def _obstruction_ratios(obstruction: SumAbSlopeObstruction) -> tuple[Fraction, ...]:
    return (
        obstruction.slope1,
        obstruction.slope2,
        obstruction.r1,
        obstruction.r2,
    )


def sum_ab_ratio_shadow_key(obstruction: SumAbSlopeObstruction) -> tuple[Fraction, ...]:
    """Return a conservative key under swaps and simultaneous reciprocals.

    This is not a full D4 action.  It only forgets the order of ``x,y,r,s`` and
    identifies that multiset with the multiset of reciprocal ratios.
    """
    ratios = _obstruction_ratios(obstruction)
    direct = tuple(sorted(ratios))
    reciprocal = tuple(sorted(1 / ratio for ratio in ratios))
    return min(direct, reciprocal)


def _failed_squareclasses(obstruction: SumAbSlopeObstruction) -> tuple[int, ...]:
    by_name = dict(obstruction.term_squareclasses)
    return tuple(sorted(by_name[name] for name in obstruction.failed_terms))


def group_sum_ab_ratio_shadow_orbits(
    obstructions: tuple[SumAbSlopeObstruction, ...],
) -> tuple[SumAbRatioShadowOrbit, ...]:
    """Group obstructions by the conservative ratio-shadow key."""
    buckets: dict[tuple[Fraction, ...], list[SumAbSlopeObstruction]] = {}
    squareclasses: dict[tuple[Fraction, ...], set[int]] = {}
    for obstruction in obstructions:
        key = sum_ab_ratio_shadow_key(obstruction)
        buckets.setdefault(key, []).append(obstruction)
        squareclasses.setdefault(key, set()).update(_failed_squareclasses(obstruction))
    orbits = [
        SumAbRatioShadowOrbit(
            key=key,
            members=tuple(sorted(buckets[key])),
            failed_squareclasses=tuple(sorted(squareclasses[key])),
        )
        for key in sorted(buckets)
    ]
    return tuple(sorted(orbits, key=lambda orbit: (orbit.member_count, orbit.key)))


def scan_sum_ab_slope_obstructions(
    slopes: tuple[Fraction, ...],
    *,
    pass_count: int | None = None,
) -> tuple[SumAbSlopeObstruction, ...]:
    """Scan ``sum=A+B`` slope pairs and return squareclass diagnostics."""
    sorted_slopes = tuple(sorted(set(slopes)))
    obstructions: list[SumAbSlopeObstruction] = []
    squareclass_cache: dict[Fraction, LegRatioSquareclass] = {}
    for i, slope1 in enumerate(sorted_slopes):
        _validate_positive("slope", slope1)
        if not is_pythagorean_leg_ratio(slope1):
            continue
        for slope2 in sorted_slopes[i:]:
            _validate_positive("slope", slope2)
            if not is_pythagorean_leg_ratio(slope2):
                continue
            obstruction = _sum_ab_slope_obstruction_with_squareclass_cache(
                slope1,
                slope2,
                squareclass_cache,
            )
            if obstruction is None:
                continue
            if pass_count is not None and obstruction.pass_count != pass_count:
                continue
            obstructions.append(obstruction)
    return tuple(obstructions)


def scan_sum_ab_slope_pairs(
    slopes: tuple[Fraction, ...],
    *,
    include_false_members: bool = False,
) -> tuple[SumAbSlopePoint, ...]:
    """Scan scaled slopes for ``sum=A+B`` rational-ratio candidates."""
    sorted_slopes = tuple(sorted(set(slopes)))
    points: list[SumAbSlopePoint] = []
    for i, slope1 in enumerate(sorted_slopes):
        _validate_positive("slope", slope1)
        if not is_pythagorean_leg_ratio(slope1):
            continue
        for slope2 in sorted_slopes[i:]:
            _validate_positive("slope", slope2)
            if not is_pythagorean_leg_ratio(slope2):
                continue
            point = sum_ab_point_from_slopes(slope1, slope2)
            if point is None:
                continue
            if point.true_member_pair or include_false_members:
                points.append(point)
    return tuple(sorted(points))


def sum_ab_product_square_bucket_summary(
    *,
    lambda_ratios: tuple[Fraction, ...],
    max_denominator: int,
    extra_conditions: tuple[ClosureProductSquareConditions, ...] = (),
) -> ProductSquareBucketSummary:
    """Summarize finite ``sum=A+B`` product-square hits by diagnostic bucket."""
    if max_denominator < 1:
        raise ValueError("max_denominator must be positive")

    bucket_counts: Counter[str] = Counter()
    true_member_counts: Counter[str] = Counter()
    pair_counts_by_bucket: dict[str, Counter[tuple[int, int]]] = {}
    examples: dict[str, ClosureProductSquareConditions] = {}

    def record(condition: ClosureProductSquareConditions) -> None:
        if (
            not condition.discriminant_is_square
            or not condition.product_terms_are_squares
            or len(condition.roots) != 2
        ):
            return
        bucket = condition.product_square_bucket
        bucket_counts[bucket] += 1
        if condition.true_member_pair:
            true_member_counts[bucket] += 1
        if len(condition.member_squareclass_pair) == 2:
            pair_counts_by_bucket.setdefault(bucket, Counter())[
                condition.member_squareclass_pair
            ] += 1
        examples.setdefault(bucket, condition)

    for lambda_ratio in lambda_ratios:
        lam = _as_fraction(lambda_ratio)
        _validate_positive("lambda_ratio", lam)
        target = lam + 1
        for denominator in range(1, max_denominator + 1):
            max_numerator = int(target * denominator)
            for numerator in range(1, max_numerator + 1):
                r = Fraction(numerator, denominator)
                s = target - r
                if s <= 0:
                    continue
                record(
                    closure_product_square_conditions(
                        lam,
                        target,
                        r * s,
                        REL_SUM_AB,
                    )
                )

    for condition in extra_conditions:
        record(condition)

    return ProductSquareBucketSummary(
        bucket_counts=dict(sorted(bucket_counts.items())),
        true_member_counts=dict(sorted(true_member_counts.items())),
        squareclass_pair_counts_by_bucket={
            bucket: dict(sorted(pair_counts.items()))
            for bucket, pair_counts in sorted(pair_counts_by_bucket.items())
        },
        examples_by_bucket=dict(sorted(examples.items())),
    )


def sum_ab_product_square_residuals_from_grid(
    *,
    lambda_ratios: tuple[Fraction, ...],
    max_denominator: int,
) -> tuple[ClosureProductSquareConditions, ...]:
    """Return finite-grid ``sum=A+B`` residual product-square diagnostics."""
    if max_denominator < 1:
        raise ValueError("max_denominator must be positive")

    residuals: set[ClosureProductSquareConditions] = set()
    for lambda_ratio in lambda_ratios:
        lam = _as_fraction(lambda_ratio)
        _validate_positive("lambda_ratio", lam)
        target = lam + 1
        for denominator in range(1, max_denominator + 1):
            max_numerator = int(target * denominator)
            for numerator in range(1, max_numerator + 1):
                r = Fraction(numerator, denominator)
                s = target - r
                if s <= 0:
                    continue
                condition = closure_product_square_conditions(
                    lam,
                    target,
                    r * s,
                    REL_SUM_AB,
                )
                if condition.product_square_bucket == "residual":
                    residuals.add(condition)
    return tuple(sorted(residuals, key=lambda item: (item.lambda_ratio, item.roots)))


def sum_ab_product_square_residuals_from_root_grid(
    *,
    max_numerator: int,
    max_denominator: int,
) -> tuple[ClosureProductSquareConditions, ...]:
    """Return residual diagnostics by choosing roots first, then ``lambda``.

    For the ``sum=A+B`` closure, roots satisfy ``r+s=lambda+1``.  This helper
    enumerates a finite rational root grid and derives ``lambda = r+s-1``.
    It is a diagnostic generator for residual examples, not a proof.
    """
    ratios = positive_rational_ratios(max_numerator, max_denominator)
    residuals: set[ClosureProductSquareConditions] = set()
    for index, r in enumerate(ratios):
        for s in ratios[index:]:
            lam = r + s - 1
            if lam <= 0:
                continue
            condition = closure_product_square_conditions(
                lam,
                lam + 1,
                r * s,
                REL_SUM_AB,
            )
            if condition.product_square_bucket == "residual":
                residuals.add(condition)
    return tuple(sorted(residuals, key=lambda item: (item.lambda_ratio, item.roots)))


def sum_ab_residual_squareclass_equations(
    *,
    lambda_ratio: Fraction | int,
    r: Fraction | int,
    s: Fraction | int,
) -> ResidualSquareclassEquations:
    """Explain product-square checks as pairwise squareclass equations."""
    lam = _as_fraction(lambda_ratio)
    root1 = _as_fraction(r)
    root2 = _as_fraction(s)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", root1)
    _validate_positive("s", root2)

    unit_values = (root1 * root1 + 1, root2 * root2 + 1)
    lambda_values = (root1 * root1 + lam * lam, root2 * root2 + lam * lam)
    unit_squareclasses = (
        _rational_squareclass(unit_values[0])[0],
        _rational_squareclass(unit_values[1])[0],
    )
    lambda_squareclasses = (
        _rational_squareclass(lambda_values[0])[0],
        _rational_squareclass(lambda_values[1])[0],
    )

    return ResidualSquareclassEquations(
        lambda_ratio=lam,
        r=root1,
        s=root2,
        unit_values=unit_values,
        lambda_values=lambda_values,
        unit_squareclasses=unit_squareclasses,
        lambda_squareclasses=lambda_squareclasses,
        unit_product_is_square=_is_rational_square(unit_values[0] * unit_values[1]),
        lambda_product_is_square=_is_rational_square(
            lambda_values[0] * lambda_values[1]
        ),
        closes_sum_ab=root1 + root2 == lam + 1,
        reciprocal_pair=root1 * root2 == lam,
        all_terms_are_squares=all(
            _is_rational_square(value) for value in (*unit_values, *lambda_values)
        ),
        squareclasses_all_trivial={*unit_squareclasses, *lambda_squareclasses} == {1},
    )


def sum_ab_true_closure_relation(
    *,
    lambda_ratio: Fraction | int,
    r: Fraction | int,
    s: Fraction | int,
) -> SumAbTrueClosureRelation:
    """Classify a ``sum=A+B`` pair for the reciprocal-closure proof target."""
    lam = _as_fraction(lambda_ratio)
    root1 = _as_fraction(r)
    root2 = _as_fraction(s)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", root1)
    _validate_positive("s", root2)

    closes_sum_ab = root1 + root2 == lam + 1
    r_true = is_rational_ratio_member(lam, root1)
    s_true = is_rational_ratio_member(lam, root2)
    both_true = r_true and s_true
    reciprocal_pair = root1 * root2 == lam
    centerline = root1 == root2
    if not closes_sum_ab:
        branch = "not-sum-ab"
    elif centerline and not both_true:
        branch = "false-centerline"
    elif centerline:
        branch = "true-centerline"
    elif reciprocal_pair and both_true:
        branch = "true-reciprocal"
    elif reciprocal_pair:
        branch = "false-reciprocal"
    elif both_true:
        branch = "true-nonreciprocal"
    else:
        branch = "false-residual"

    return SumAbTrueClosureRelation(
        lambda_ratio=lam,
        r=root1,
        s=root2,
        closes_sum_ab=closes_sum_ab,
        r_true_member=r_true,
        s_true_member=s_true,
        both_true_members=both_true,
        reciprocal_pair=reciprocal_pair,
        centerline=centerline,
        branch=branch,
    )


def _full_plane_relation_target(lambda_ratio: Fraction, relation: str) -> Fraction:
    if relation in (REL_SUM_AB, REL_DIFF_AB):
        return lambda_ratio + 1
    if relation in (REL_SUM_DIFF, REL_DIFF_DIFF):
        target = abs(lambda_ratio - 1)
        if target == 0:
            raise ValueError("|A-B| target is zero when lambda_ratio = 1")
        return target
    raise ValueError(f"unknown relation: {relation}")


def full_plane_true_closure_relation(
    *,
    lambda_ratio: Fraction | int,
    r: Fraction | int,
    s: Fraction | int,
    relation: str,
) -> FullPlaneTrueClosureRelation:
    """Classify one full-plane closure pair for the reciprocal proof target.

    This is the full-plane analogue of :func:`sum_ab_true_closure_relation`.
    It records all four closure truth values so a later proof note cannot
    accidentally treat the ``sum=A+B`` branch as the whole plane.
    """
    lam = _as_fraction(lambda_ratio)
    root1, root2 = sorted((_as_fraction(r), _as_fraction(s)))
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", root1)
    _validate_positive("s", root2)

    target = _full_plane_relation_target(lam, relation)
    sum_value = root1 + root2
    diff_value = abs(root2 - root1)
    closure_value = sum_value if relation.startswith("sum=") else diff_value
    diff_target = abs(lam - 1)
    closes_sum_ab = sum_value == lam + 1
    closes_sum_diff = diff_target != 0 and sum_value == diff_target
    closes_diff_ab = diff_value == lam + 1
    closes_diff_diff = diff_target != 0 and diff_value == diff_target
    closes_relation = closure_value == target

    r_true = is_rational_ratio_member(lam, root1)
    s_true = is_rational_ratio_member(lam, root2)
    both_true = r_true and s_true
    reciprocal_pair = root1 * root2 == lam
    centerline = root1 == root2
    if not closes_relation:
        branch = "not-closure"
    elif centerline and not both_true:
        branch = "false-centerline"
    elif centerline:
        branch = "true-centerline"
    elif reciprocal_pair and both_true:
        branch = "true-reciprocal"
    elif reciprocal_pair:
        branch = "false-reciprocal"
    elif both_true:
        branch = "true-nonreciprocal"
    else:
        branch = "false-residual"

    return FullPlaneTrueClosureRelation(
        lambda_ratio=lam,
        relation=relation,
        target=target,
        r=root1,
        s=root2,
        closure_value=closure_value,
        closes_relation=closes_relation,
        closes_sum_ab=closes_sum_ab,
        closes_sum_diff=closes_sum_diff,
        closes_diff_ab=closes_diff_ab,
        closes_diff_diff=closes_diff_diff,
        r_true_member=r_true,
        s_true_member=s_true,
        both_true_members=both_true,
        reciprocal_pair=reciprocal_pair,
        centerline=centerline,
        branch=branch,
    )


def scan_sum_ab_true_closure_relations(
    *,
    lambda_ratios: tuple[Fraction, ...],
    max_numerator: int,
    max_denominator: int,
    branches: tuple[str, ...] | None = None,
) -> tuple[SumAbTrueClosureRelation, ...]:
    """Scan a finite rational root pool for ``sum=A+B`` closure branches."""
    ratios = positive_rational_ratios(max_numerator, max_denominator)
    ratio_set = set(ratios)
    branch_filter = set(branches) if branches is not None else None
    relations: set[SumAbTrueClosureRelation] = set()

    for lambda_ratio in lambda_ratios:
        lam = _as_fraction(lambda_ratio)
        _validate_positive("lambda_ratio", lam)
        target = lam + 1
        for r in ratios:
            s = target - r
            if s <= 0 or s not in ratio_set:
                continue
            root1, root2 = sorted((r, s))
            relation = sum_ab_true_closure_relation(
                lambda_ratio=lam,
                r=root1,
                s=root2,
            )
            if branch_filter is not None and relation.branch not in branch_filter:
                continue
            relations.add(relation)

    return tuple(
        sorted(
            relations,
            key=lambda item: (item.lambda_ratio, item.branch, item.r, item.s),
        )
    )


def scan_full_plane_true_closure_relations(
    *,
    lambda_ratios: tuple[Fraction, ...],
    max_numerator: int,
    max_denominator: int,
    include_centerline: bool = False,
    branches: tuple[str, ...] | None = None,
) -> tuple[FullPlaneTrueClosureRelation, ...]:
    """Scan a finite rational root pool for full-plane closure branches."""
    ratios = positive_rational_ratios(max_numerator, max_denominator)
    branch_filter = set(branches) if branches is not None else None
    relations: set[FullPlaneTrueClosureRelation] = set()

    for lambda_ratio in lambda_ratios:
        lam = _as_fraction(lambda_ratio)
        _validate_positive("lambda_ratio", lam)
        for hit in find_rational_ratio_hits(
            lam,
            ratios,
            include_centerline=include_centerline,
        ):
            relation = full_plane_true_closure_relation(
                lambda_ratio=lam,
                r=hit.r1,
                s=hit.r2,
                relation=hit.relation,
            )
            if branch_filter is not None and relation.branch not in branch_filter:
                continue
            relations.add(relation)

    return tuple(
        sorted(
            relations,
            key=lambda item: (
                item.lambda_ratio,
                item.relation,
                item.branch,
                item.r,
                item.s,
            ),
        )
    )


def full_plane_closure_product_ledger(
    *,
    lambda_ratio: Fraction | int,
    r: Fraction | int,
    s: Fraction | int,
    relation: str,
) -> FullPlaneClosureProductLedger:
    """Attach the product-square ledger to one full-plane closure classification."""
    classification = full_plane_true_closure_relation(
        lambda_ratio=lambda_ratio,
        r=r,
        s=s,
        relation=relation,
    )
    if not classification.closes_relation:
        raise ValueError(
            "full-plane closure product ledger requires a pair that does close"
        )
    product = classification.r * classification.s
    conditions = closure_product_square_conditions(
        classification.lambda_ratio,
        classification.target,
        product,
        classification.relation,
    )
    return FullPlaneClosureProductLedger(
        classification=classification,
        conditions=conditions,
        target=classification.target,
        product=product,
        product_equals_lambda=product == classification.lambda_ratio,
        danger_branch=classification.branch == "true-nonreciprocal",
    )


def full_plane_closure_product_summary(
    *,
    lambda_ratios: tuple[Fraction, ...],
    max_numerator: int,
    max_denominator: int,
    include_centerline: bool = False,
    branches: tuple[str, ...] | None = None,
) -> FullPlaneClosureProductSummary:
    """Summarize finite full-plane closure product ledgers.

    This is a bounded diagnostic.  It counts buckets in the supplied rational
    root pool; it does not prove that missing buckets are impossible.
    """
    branch_counts: Counter[str] = Counter()
    relation_branch_counts: Counter[tuple[str, str]] = Counter()
    product_bucket_counts: Counter[tuple[str, str]] = Counter()
    danger_count = 0

    for relation in scan_full_plane_true_closure_relations(
        lambda_ratios=lambda_ratios,
        max_numerator=max_numerator,
        max_denominator=max_denominator,
        include_centerline=include_centerline,
        branches=branches,
    ):
        ledger = full_plane_closure_product_ledger(
            lambda_ratio=relation.lambda_ratio,
            r=relation.r,
            s=relation.s,
            relation=relation.relation,
        )
        branch = ledger.classification.branch
        product_bucket = ledger.conditions.product_square_bucket
        branch_counts[branch] += 1
        relation_branch_counts[(ledger.classification.relation, branch)] += 1
        product_bucket_counts[(ledger.classification.relation, product_bucket)] += 1
        if ledger.danger_branch:
            danger_count += 1

    return FullPlaneClosureProductSummary(
        total_relations=sum(branch_counts.values()),
        branch_counts=dict(sorted(branch_counts.items())),
        relation_branch_counts=dict(sorted(relation_branch_counts.items())),
        product_bucket_counts=dict(sorted(product_bucket_counts.items())),
        danger_count=danger_count,
    )


def sum_ab_root_grid_residual_summary(
    *,
    max_numerator: int,
    max_denominator: int,
) -> ProductSquareBucketSummary:
    """Summarize finite root-grid residuals and their squareclass pairs."""
    bucket_counts: Counter[str] = Counter()
    true_member_counts: Counter[str] = Counter()
    pair_counts_by_bucket: dict[str, Counter[tuple[int, int]]] = {}
    examples: dict[str, ClosureProductSquareConditions] = {}

    for condition in sum_ab_product_square_residuals_from_root_grid(
        max_numerator=max_numerator,
        max_denominator=max_denominator,
    ):
        bucket = condition.product_square_bucket
        bucket_counts[bucket] += 1
        if condition.true_member_pair:
            true_member_counts[bucket] += 1
        if len(condition.member_squareclass_pair) == 2:
            pair_counts_by_bucket.setdefault(bucket, Counter())[
                condition.member_squareclass_pair
            ] += 1
        examples.setdefault(bucket, condition)

    return ProductSquareBucketSummary(
        bucket_counts=dict(sorted(bucket_counts.items())),
        true_member_counts=dict(sorted(true_member_counts.items())),
        squareclass_pair_counts_by_bucket={
            bucket: dict(sorted(pair_counts.items()))
            for bucket, pair_counts in sorted(pair_counts_by_bucket.items())
        },
        examples_by_bucket=dict(sorted(examples.items())),
    )


def sum_ab_root_grid_residual_prime_class_summary(
    *,
    max_numerator: int,
    max_denominator: int,
) -> ResidualPrimeClassSummary:
    """Classify finite root-grid residuals by their member squareclass primes."""
    bucket_counts: Counter[str] = Counter()
    squareclass_prime_counts: Counter[tuple[int, ...]] = Counter()
    three_mod_four_prime_counts: Counter[tuple[int, ...]] = Counter()
    examples: dict[str, ClosureProductSquareConditions] = {}

    for condition in sum_ab_product_square_residuals_from_root_grid(
        max_numerator=max_numerator,
        max_denominator=max_denominator,
    ):
        valuation = closure_member_prime_valuation_ledger(
            condition.lambda_ratio,
            condition.target,
            condition.product,
            condition.relation,
        )
        squareclass_primes = valuation.member_squareclass_primes
        three_mod_four_primes = valuation.three_mod_four_member_squareclass_primes
        if not squareclass_primes:
            bucket = "trivial_squareclass"
        elif three_mod_four_primes:
            bucket = "has_3_mod_4_squareclass"
        else:
            bucket = "only_1_mod_4_squareclass"
        bucket_counts[bucket] += 1
        squareclass_prime_counts[squareclass_primes] += 1
        three_mod_four_prime_counts[three_mod_four_primes] += 1
        examples.setdefault(bucket, condition)

    return ResidualPrimeClassSummary(
        total_residuals=sum(bucket_counts.values()),
        bucket_counts=dict(sorted(bucket_counts.items())),
        squareclass_prime_counts=dict(sorted(squareclass_prime_counts.items())),
        three_mod_four_squareclass_prime_counts=dict(
            sorted(three_mod_four_prime_counts.items())
        ),
        examples_by_bucket=dict(sorted(examples.items())),
    )


def sum_ab_root_grid_gaussian_shadow_summary(
    *,
    max_numerator: int,
    max_denominator: int,
) -> GaussianShadowSummary:
    """Summarize whether finite residuals are Gaussian centerline shadows."""
    centerline_shadow_count = 0
    nonshadow_count = 0
    common_counts: Counter[tuple[Fraction, ...]] = Counter()
    examples: dict[str, ClosureProductSquareConditions] = {}

    for condition in sum_ab_product_square_residuals_from_root_grid(
        max_numerator=max_numerator,
        max_denominator=max_denominator,
    ):
        try:
            ledger = residual_gaussian_absorption_ledger(condition)
        except ValueError:
            nonshadow_count += 1
            examples.setdefault("nonshadow", condition)
            common_counts[()] += 1
            continue
        common_counts[ledger.common_absorbed_members] += 1
        if ledger.centerline_shadow:
            centerline_shadow_count += 1
            examples.setdefault("centerline_shadow", condition)
        else:
            nonshadow_count += 1
            examples.setdefault("nonshadow", condition)

    return GaussianShadowSummary(
        total_residuals=centerline_shadow_count + nonshadow_count,
        centerline_shadow_count=centerline_shadow_count,
        nonshadow_count=nonshadow_count,
        common_absorbed_member_counts=dict(sorted(common_counts.items())),
        examples_by_bucket=dict(sorted(examples.items())),
    )


def sum_ab_root_grid_gaussian_shadow_obstruction_summary(
    *,
    max_numerator: int,
    max_denominator: int,
) -> GaussianShadowObstructionSummary:
    """Summarize whether finite Gaussian shadows are blocked by unit terms."""
    centerline_shadow_count = 0
    unit_obstructed_count = 0
    nonobstructed_count = 0
    reason_counts: Counter[str] = Counter()
    examples: dict[str, ClosureProductSquareConditions] = {}

    for condition in sum_ab_product_square_residuals_from_root_grid(
        max_numerator=max_numerator,
        max_denominator=max_denominator,
    ):
        try:
            ledger = residual_gaussian_absorption_ledger(condition)
        except ValueError:
            nonobstructed_count += 1
            examples.setdefault("nonshadow", condition)
            continue
        if not ledger.centerline_shadow:
            nonobstructed_count += 1
            examples.setdefault("nonshadow", condition)
            continue
        centerline_shadow_count += 1
        obstruction_found = False
        for absorbed in ledger.common_absorbed_members:
            try:
                r_branch = _absorbed_branch_for_member(
                    ledger.r_absorption,
                    absorbed,
                )
                s_branch = _absorbed_branch_for_member(
                    ledger.s_absorption,
                    absorbed,
                )
                obstruction = inverse_gaussian_centerline_shadow_obstruction(
                    absorbed=absorbed,
                    squareclass=ledger.squareclass,
                    r_branch=r_branch,
                    s_branch=s_branch,
                )
            except ValueError:
                continue
            if obstruction.unit_squareclass_obstruction:
                obstruction_found = True
                unit_obstructed_count += 1
                if obstruction.obstruction_reason is not None:
                    reason_counts[obstruction.obstruction_reason] += 1
                examples.setdefault("unit_obstructed", condition)
                break
        if not obstruction_found:
            nonobstructed_count += 1
            examples.setdefault("not_unit_obstructed", condition)

    return GaussianShadowObstructionSummary(
        total_residuals=centerline_shadow_count + nonobstructed_count,
        centerline_shadow_count=centerline_shadow_count,
        unit_obstructed_count=unit_obstructed_count,
        nonobstructed_count=nonobstructed_count,
        obstruction_reason_counts=dict(sorted(reason_counts.items())),
        examples_by_bucket=dict(sorted(examples.items())),
    )


def sum_ab_root_grid_residual_watchlist(
    *,
    max_numerator: int,
    max_denominator: int,
    extra_conditions: tuple[ClosureProductSquareConditions, ...] = (),
) -> tuple[ClosureProductSquareConditions, ...]:
    """Return finite residuals that would be dangerous for the proof direction."""
    conditions = (
        *sum_ab_product_square_residuals_from_root_grid(
            max_numerator=max_numerator,
            max_denominator=max_denominator,
        ),
        *extra_conditions,
    )
    watched = {
        condition
        for condition in conditions
        if condition.true_member_pair or condition.member_squareclass_pair == (1, 1)
    }
    return tuple(sorted(watched, key=lambda item: (item.lambda_ratio, item.roots)))


def reciprocal_sum_ab_roots(lambda_ratio: Fraction | int) -> tuple[Fraction, Fraction]:
    """Return roots forced by ``r + lambda/r = lambda + 1``.

    Algebraically the roots are always ``1`` and ``lambda``.  They need not be
    true ``R_lambda`` members; use :func:`true_reciprocal_sum_ab_roots` for that.
    """
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    return (Fraction(1), lam)


def sum_ab_reciprocal_obstruction(
    lambda_ratio: Fraction | int,
) -> SumAbReciprocalObstruction:
    """Return the closed-form obstruction for the ``sum=A+B`` reciprocal branch."""
    lam = _as_fraction(lambda_ratio)
    roots = reciprocal_sum_ab_roots(lam)
    unit_leg_value = Fraction(2)
    true_roots = true_reciprocal_sum_ab_roots(lam)
    return SumAbReciprocalObstruction(
        lambda_ratio=lam,
        roots=roots,
        forced_unit_root=Fraction(1),
        unit_leg_value=unit_leg_value,
        unit_leg_is_square=_is_rational_square(unit_leg_value),
        true_roots=true_roots,
        branch_closed=true_roots == (),
    )


def true_reciprocal_sum_ab_roots(lambda_ratio: Fraction | int) -> tuple[Fraction, ...]:
    """Return the ``sum=A+B`` same-orbit roots that are true ``R_lambda`` points."""
    lam = _as_fraction(lambda_ratio)
    return tuple(r for r in reciprocal_sum_ab_roots(lam) if is_rational_ratio_member(lam, r))


def product_identity_terms(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
) -> ProductIdentityTerms:
    """Return the terms in the sum-closure product identity.

    For ``r+s=T`` and ``p=rs``:

        A_p = p^2 - 2p + T^2 + 1
        B_p = p^2 - 2lambda^2 p + lambda^2 T^2 + lambda^4

    and:

        B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2)
    """
    lam = _as_fraction(lambda_ratio)
    t = _as_fraction(target)
    p = _as_fraction(product)
    _validate_positive("lambda_ratio", lam)
    if t <= 0:
        raise ValueError("target must be positive")

    lam_sq = lam * lam
    a_term = p * p - 2 * p + t * t + 1
    b_term = p * p - 2 * lam_sq * p + lam_sq * t * t + lam_sq * lam_sq
    return ProductIdentityTerms(
        lambda_ratio=lam,
        target=t,
        product=p,
        a_term=a_term,
        b_term=b_term,
        b_minus_lambda_sq_a=b_term - lam_sq * a_term,
    )


def closure_product_identity_terms(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ProductIdentityTerms:
    """Return product-identity terms for a sum or difference closure relation."""
    lam = _as_fraction(lambda_ratio)
    t = _as_fraction(target)
    p = _as_fraction(product)
    _validate_positive("lambda_ratio", lam)
    if t <= 0:
        raise ValueError("target must be positive")

    if relation.startswith("sum="):
        sign = -1
    elif relation.startswith("diff="):
        sign = 1
    else:
        raise ValueError(f"unknown closure relation: {relation}")

    lam_sq = lam * lam
    a_term = p * p + sign * 2 * p + t * t + 1
    b_term = p * p + sign * 2 * lam_sq * p + lam_sq * t * t + lam_sq * lam_sq
    return ProductIdentityTerms(
        lambda_ratio=lam,
        target=t,
        product=p,
        a_term=a_term,
        b_term=b_term,
        b_minus_lambda_sq_a=b_term - lam_sq * a_term,
    )


def _closure_roots_from_target_product(
    target: Fraction,
    product: Fraction,
    relation: str,
) -> tuple[Fraction, ...]:
    if relation.startswith("sum="):
        discriminant = target * target - 4 * product
        sqrt_disc = _rational_sqrt(discriminant)
        return (
            tuple(sorted(((target - sqrt_disc) / 2, (target + sqrt_disc) / 2)))
            if sqrt_disc is not None
            else ()
        )
    if relation.startswith("diff="):
        discriminant = target * target + 4 * product
        sqrt_disc = _rational_sqrt(discriminant)
        return (
            tuple(sorted(((sqrt_disc - target) / 2, (sqrt_disc + target) / 2)))
            if sqrt_disc is not None
            else ()
        )
    raise ValueError(f"unknown closure relation: {relation}")


def closure_member_product_square_ledger(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ClosureMemberProductSquareLedger:
    """Translate individual member squares into the product identity ledger."""
    terms = closure_product_identity_terms(lambda_ratio, target, product, relation)
    roots = tuple(root for root in _closure_roots_from_target_product(
        terms.target,
        terms.product,
        relation,
    ) if root > 0)
    if len(roots) != 2:
        return ClosureMemberProductSquareLedger(
            lambda_ratio=terms.lambda_ratio,
            target=terms.target,
            product=terms.product,
            relation=relation,
            identity_terms=terms,
            roots=roots,
            unit_values=(),
            lambda_values=(),
            unit_product=None,
            lambda_product=None,
            unit_product_is_square=False,
            lambda_product_is_square=False,
            member_squareclasses=(),
            member_squareclass_pair=(),
            member_squareclasses_pairwise_equal=False,
            member_squareclasses_all_trivial=False,
            true_member_pair=False,
        )

    r, s = roots
    lam = terms.lambda_ratio
    unit_values = (r * r + 1, s * s + 1)
    lambda_values = (r * r + lam * lam, s * s + lam * lam)
    member_squareclasses = (
        _rational_squareclass(unit_values[0])[0],
        _rational_squareclass(unit_values[1])[0],
        _rational_squareclass(lambda_values[0])[0],
        _rational_squareclass(lambda_values[1])[0],
    )
    member_squareclasses_pairwise_equal = (
        member_squareclasses[0] == member_squareclasses[1]
        and member_squareclasses[2] == member_squareclasses[3]
    )
    member_squareclass_pair: tuple[int, int] | tuple[()] = (
        (member_squareclasses[0], member_squareclasses[2])
        if member_squareclasses_pairwise_equal
        else ()
    )
    member_square_flags = (
        _is_rational_square(unit_values[0]),
        _is_rational_square(unit_values[1]),
        _is_rational_square(lambda_values[0]),
        _is_rational_square(lambda_values[1]),
    )
    unit_product = unit_values[0] * unit_values[1]
    lambda_product = lambda_values[0] * lambda_values[1]
    return ClosureMemberProductSquareLedger(
        lambda_ratio=terms.lambda_ratio,
        target=terms.target,
        product=terms.product,
        relation=relation,
        identity_terms=terms,
        roots=roots,
        unit_values=unit_values,
        lambda_values=lambda_values,
        unit_product=unit_product,
        lambda_product=lambda_product,
        unit_product_is_square=_is_rational_square(unit_product),
        lambda_product_is_square=_is_rational_square(lambda_product),
        member_squareclasses=member_squareclasses,
        member_squareclass_pair=member_squareclass_pair,
        member_squareclasses_pairwise_equal=member_squareclasses_pairwise_equal,
        member_squareclasses_all_trivial=set(member_squareclasses) == {1},
        true_member_pair=all(member_square_flags),
    )


def closure_member_prime_valuation_ledger(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ClosureMemberPrimeValuationLedger:
    """Record prime valuations for the true member terms and product identity."""
    member_ledger = closure_member_product_square_ledger(
        lambda_ratio,
        target,
        product,
        relation,
    )
    terms = member_ledger.identity_terms
    lam_sq = terms.lambda_ratio * terms.lambda_ratio
    member_values = (*member_ledger.unit_values, *member_ledger.lambda_values)
    identity_values = (
        terms.a_term,
        terms.b_term,
        terms.b_minus_lambda_sq_a,
        lam_sq - 1,
        lam_sq - terms.product * terms.product,
    )
    primes = _prime_support((*member_values, *identity_values))
    rows: list[ClosureMemberPrimeValuationRow] = []
    for prime in primes:
        member_valuations = tuple(
            _rational_valuation(value, prime) for value in member_values
        )
        if any(valuation is None for valuation in member_valuations):
            raise ValueError("member values should be positive nonzero rationals")
        identity_valuations = tuple(
            _rational_valuation(value, prime) for value in identity_values
        )
        finite_identity_valuations = tuple(
            valuation for valuation in identity_valuations[:2] if valuation is not None
        )
        rows.append(
            ClosureMemberPrimeValuationRow(
                prime=prime,
                member_valuations=member_valuations,  # type: ignore[arg-type]
                identity_valuations=identity_valuations,
                all_member_valuations_even=all(
                    valuation % 2 == 0 for valuation in member_valuations
                ),
                product_valuations_even=all(
                    valuation % 2 == 0 for valuation in finite_identity_valuations
                ),
            )
        )
    rows_tuple = tuple(rows)
    rows_by_prime = {row.prime: row for row in rows_tuple}
    member_squareclass_primes = tuple(
        prime
        for prime in primes
        if prime in member_ledger.member_squareclasses
        or any(
            _rational_valuation(value, prime) % 2
            for value in member_values
        )
    )
    three_mod_four_primes = tuple(prime for prime in primes if prime % 4 == 3)
    return ClosureMemberPrimeValuationLedger(
        member_ledger=member_ledger,
        primes=primes,
        three_mod_four_primes=three_mod_four_primes,
        member_squareclass_primes=member_squareclass_primes,
        three_mod_four_member_squareclass_primes=tuple(
            prime for prime in member_squareclass_primes if prime % 4 == 3
        ),
        rows=rows_tuple,
        three_mod_four_rows=tuple(
            row for row in rows_tuple if row.prime in three_mod_four_primes
        ),
        rows_by_prime=rows_by_prime,
    )


def _valuation_is_odd(valuation: int | None) -> bool:
    return valuation is not None and valuation % 2 != 0


def closure_identity_three_mod_four_balance_ledger(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ClosureIdentityThreeModFourBalanceLedger:
    """Summarize parity balance at primes ``q == 3 mod 4`` in the identity."""
    valuation_ledger = closure_member_prime_valuation_ledger(
        lambda_ratio,
        target,
        product,
        relation,
    )
    rows: list[ClosureIdentityThreeModFourBalanceRow] = []
    for valuation_row in valuation_ledger.three_mod_four_rows:
        identity_valuations = valuation_row.identity_valuations
        lambda_squared_minus_one_odd = _valuation_is_odd(identity_valuations[3])
        lambda_squared_minus_product_squared_odd = _valuation_is_odd(
            identity_valuations[4]
        )
        rows.append(
            ClosureIdentityThreeModFourBalanceRow(
                prime=valuation_row.prime,
                identity_valuations=identity_valuations,
                identity_difference_odd=_valuation_is_odd(identity_valuations[2]),
                lambda_squared_minus_one_odd=lambda_squared_minus_one_odd,
                lambda_squared_minus_product_squared_odd=(
                    lambda_squared_minus_product_squared_odd
                ),
                shared_odd_compensation=(
                    lambda_squared_minus_one_odd
                    and lambda_squared_minus_product_squared_odd
                ),
            )
        )
    rows_tuple = tuple(rows)
    rows_by_prime = {row.prime: row for row in rows_tuple}
    odd_lambda_squared_minus_product_squared_primes = tuple(
        row.prime for row in rows_tuple if row.lambda_squared_minus_product_squared_odd
    )
    shared_odd_lambda_squared_minus_one_primes = tuple(
        row.prime for row in rows_tuple if row.shared_odd_compensation
    )
    return ClosureIdentityThreeModFourBalanceLedger(
        valuation_ledger=valuation_ledger,
        rows=rows_tuple,
        rows_by_prime=rows_by_prime,
        odd_identity_difference_primes=tuple(
            row.prime for row in rows_tuple if row.identity_difference_odd
        ),
        odd_lambda_squared_minus_product_squared_primes=(
            odd_lambda_squared_minus_product_squared_primes
        ),
        shared_odd_lambda_squared_minus_one_primes=(
            shared_odd_lambda_squared_minus_one_primes
        ),
        unshared_odd_lambda_squared_minus_product_squared_primes=tuple(
            prime
            for prime in odd_lambda_squared_minus_product_squared_primes
            if prime not in shared_odd_lambda_squared_minus_one_primes
        ),
    )


def closure_identity_shared_gcd_ledger(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ClosureIdentitySharedGcdLedger:
    """Track shared odd factors through ``p^2-1`` and the closure discriminant."""
    balance_ledger = closure_identity_three_mod_four_balance_ledger(
        lambda_ratio,
        target,
        product,
        relation,
    )
    terms = balance_ledger.valuation_ledger.member_ledger.identity_terms
    if relation.startswith("sum="):
        closure_discriminant = terms.target * terms.target - 4 * terms.product
    elif relation.startswith("diff="):
        closure_discriminant = terms.target * terms.target + 4 * terms.product
    else:
        raise ValueError(f"unknown closure relation: {relation}")

    p_squared_minus_one = terms.product * terms.product - 1
    rows: list[ClosureIdentitySharedGcdRow] = []
    for balance_row in balance_ledger.rows:
        lambda_squared_minus_one_valuation = balance_row.identity_valuations[3]
        lambda_squared_minus_product_squared_valuation = (
            balance_row.identity_valuations[4]
        )
        p_squared_minus_one_valuation = _rational_valuation(
            p_squared_minus_one,
            balance_row.prime,
        )
        closure_discriminant_valuation = _rational_valuation(
            closure_discriminant,
            balance_row.prime,
        )
        shared_minimum = (
            min(
                lambda_squared_minus_one_valuation,
                lambda_squared_minus_product_squared_valuation,
            )
            if lambda_squared_minus_one_valuation is not None
            and lambda_squared_minus_product_squared_valuation is not None
            else None
        )
        rows.append(
            ClosureIdentitySharedGcdRow(
                prime=balance_row.prime,
                lambda_squared_minus_one_valuation=(
                    lambda_squared_minus_one_valuation
                ),
                lambda_squared_minus_product_squared_valuation=(
                    lambda_squared_minus_product_squared_valuation
                ),
                p_squared_minus_one_valuation=p_squared_minus_one_valuation,
                closure_discriminant_valuation=closure_discriminant_valuation,
                shared_odd_compensation=balance_row.shared_odd_compensation,
                p_squared_minus_one_carries_shared_factor=(
                    shared_minimum is not None
                    and shared_minimum > 0
                    and p_squared_minus_one_valuation is not None
                    and p_squared_minus_one_valuation >= shared_minimum
                ),
                closure_discriminant_valuation_even=(
                    closure_discriminant_valuation is not None
                    and closure_discriminant_valuation % 2 == 0
                ),
            )
        )
    rows_tuple = tuple(rows)
    return ClosureIdentitySharedGcdLedger(
        balance_ledger=balance_ledger,
        closure_discriminant=closure_discriminant,
        rows=rows_tuple,
        rows_by_prime={row.prime: row for row in rows_tuple},
        shared_odd_compensation_primes=(
            balance_ledger.shared_odd_lambda_squared_minus_one_primes
        ),
        unshared_odd_lambda_squared_minus_product_squared_primes=(
            balance_ledger.unshared_odd_lambda_squared_minus_product_squared_primes
        ),
    )


def sum_ab_shared_odd_prime_residue_summary(
    prime: int,
) -> SumAbSharedOddPrimeResidueSummary:
    """Enumerate shared-prime sign cases that survive member-square residues."""
    if prime <= 2 or factorint(prime) != {prime: 1}:
        raise ValueError("prime must be an odd prime")
    if prime % 4 != 3:
        raise ValueError("prime must be 3 mod 4")

    square_residues = {residue * residue % prime for residue in range(prime)}
    all_case_keys = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    cases: list[SumAbSharedOddPrimeResidueCase] = []
    for lambda_residue, product_residue in all_case_keys:
        target_residue = (lambda_residue + 1) % prime
        product_mod = product_residue % prime
        root_residues: list[tuple[int, int]] = []
        member_square_residue_pairs: list[tuple[int, int]] = []
        for r_residue in range(prime):
            s_residue = (target_residue - r_residue) % prime
            if (r_residue * s_residue - product_mod) % prime:
                continue
            unit_pair = (
                (r_residue * r_residue + 1) % prime,
                (s_residue * s_residue + 1) % prime,
            )
            lambda_pair = unit_pair
            if all(value in square_residues for value in (*unit_pair, *lambda_pair)):
                root_residues.append((r_residue, s_residue))
                member_square_residue_pairs.append(unit_pair)

        if root_residues:
            cases.append(
                SumAbSharedOddPrimeResidueCase(
                    prime=prime,
                    lambda_residue=lambda_residue,
                    product_residue=product_residue,
                    target_residue=target_residue,
                    discriminant_residue=(
                        target_residue * target_residue - 4 * product_mod
                    )
                    % prime,
                    root_residues=tuple(root_residues),
                    member_square_residue_pairs=tuple(
                        member_square_residue_pairs
                    ),
                )
            )

    cases_tuple = tuple(cases)
    case_keys = tuple(
        (case.lambda_residue, case.product_residue) for case in cases_tuple
    )
    killed_case_keys = tuple(
        case_key for case_key in all_case_keys if case_key not in case_keys
    )
    return SumAbSharedOddPrimeResidueSummary(
        prime=prime,
        prime_mod_8=prime % 8,
        prime_mod_16=prime % 16,
        cases=cases_tuple,
        case_keys=case_keys,
        killed_case_keys=killed_case_keys,
        all_cases_killed=case_keys == (),
    )


def sum_ab_shared_odd_prime_power_lift_summary(
    prime: int,
    exponent: int,
) -> SumAbSharedOddPrimePowerLiftSummary:
    """Enumerate small prime-power lifts of shared-prime local shadows."""
    if prime <= 2 or factorint(prime) != {prime: 1}:
        raise ValueError("prime must be an odd prime")
    if prime % 4 != 3:
        raise ValueError("prime must be 3 mod 4")
    if exponent < 2:
        raise ValueError("exponent must be at least 2")

    modulus = prime**exponent
    square_residues = {residue * residue % modulus for residue in range(modulus)}
    pattern_counts: Counter[
        tuple[int, int, int, int, tuple[int, int, int, int]]
    ] = Counter()
    examples_by_pattern: dict[
        tuple[int, int, int, int, tuple[int, int, int, int]],
        tuple[int, int, int, int, tuple[int, int, int, int]],
    ] = {}
    for lambda_residue in range(1, modulus):
        if _gcd(lambda_residue, prime) != 1:
            continue
        if _truncated_mod_valuation(
            lambda_residue * lambda_residue - 1,
            prime,
            exponent,
        ) != 1:
            continue
        target_residue = (lambda_residue + 1) % modulus
        for r_residue in range(1, modulus):
            if _gcd(r_residue, prime) != 1:
                continue
            s_residue = (target_residue - r_residue) % modulus
            if _gcd(s_residue, prime) != 1:
                continue
            product_residue = r_residue * s_residue % modulus
            if _truncated_mod_valuation(
                lambda_residue * lambda_residue
                - product_residue * product_residue,
                prime,
                exponent,
            ) != 1:
                continue
            member_residues = (
                (r_residue * r_residue + 1) % modulus,
                (s_residue * s_residue + 1) % modulus,
                (r_residue * r_residue + lambda_residue * lambda_residue) % modulus,
                (s_residue * s_residue + lambda_residue * lambda_residue) % modulus,
            )
            if not all(value in square_residues for value in member_residues):
                continue

            lambda_mod_prime = lambda_residue % prime
            product_mod_prime = product_residue % prime
            pattern = (
                lambda_mod_prime if lambda_mod_prime != prime - 1 else -1,
                product_mod_prime if product_mod_prime != prime - 1 else -1,
                _truncated_mod_valuation(
                    product_residue - lambda_residue,
                    prime,
                    exponent,
                ),
                _truncated_mod_valuation(
                    product_residue + lambda_residue,
                    prime,
                    exponent,
                ),
                tuple(
                    _truncated_mod_valuation(value, prime, exponent)
                    for value in member_residues
                ),
            )
            pattern_counts[pattern] += 1
            examples_by_pattern.setdefault(
                pattern,
                (
                    lambda_residue,
                    r_residue,
                    s_residue,
                    product_residue,
                    member_residues,
                ),
            )

    pattern_counts_dict = dict(sorted(pattern_counts.items()))
    return SumAbSharedOddPrimePowerLiftSummary(
        prime=prime,
        exponent=exponent,
        modulus=modulus,
        total_lifts=sum(pattern_counts_dict.values()),
        pattern_counts=pattern_counts_dict,
        examples_by_pattern={
            pattern: examples_by_pattern[pattern]
            for pattern in pattern_counts_dict
        },
        p_minus_lambda_shadow_count=sum(
            count
            for pattern, count in pattern_counts_dict.items()
            if pattern[2] > 0
        ),
        p_plus_lambda_shadow_count=sum(
            count
            for pattern, count in pattern_counts_dict.items()
            if pattern[3] > 0
        ),
    )


def closure_product_square_conditions(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ClosureProductSquareConditions:
    """Return necessary and true square checks for one closure ``T,p`` pair.

    ``A_p`` and ``B_p`` being squares is only a necessary product-level check.
    The real ``R_lambda`` condition still needs the two recovered roots to pass
    their four individual square tests.
    """
    terms = closure_product_identity_terms(lambda_ratio, target, product, relation)
    lam = terms.lambda_ratio
    t = terms.target
    p = terms.product

    if relation.startswith("sum="):
        discriminant = t * t - 4 * p
    elif relation.startswith("diff="):
        discriminant = t * t + 4 * p
    else:
        raise ValueError(f"unknown closure relation: {relation}")
    roots = _closure_roots_from_target_product(t, p, relation)
    sqrt_disc = _rational_sqrt(discriminant)

    positive_roots = tuple(root for root in roots if root > 0)
    if len(positive_roots) == 2:
        r, s = positive_roots
        member_values = (
            r * r + 1,
            s * s + 1,
            r * r + lam * lam,
            s * s + lam * lam,
        )
        member_square_flags: tuple[bool, bool, bool, bool] | tuple[()] = (
            _is_rational_square(member_values[0]),
            _is_rational_square(member_values[1]),
            _is_rational_square(member_values[2]),
            _is_rational_square(member_values[3]),
        )
        member_squareclasses: tuple[int, int, int, int] | tuple[()] = (
            _rational_squareclass(member_values[0])[0],
            _rational_squareclass(member_values[1])[0],
            _rational_squareclass(member_values[2])[0],
            _rational_squareclass(member_values[3])[0],
        )
    else:
        member_square_flags = ()
        member_squareclasses = ()

    product_terms_are_squares = _is_rational_square(
        terms.a_term
    ) and _is_rational_square(terms.b_term)
    member_squareclasses_pairwise_equal = (
        len(member_squareclasses) == 4
        and member_squareclasses[0] == member_squareclasses[1]
        and member_squareclasses[2] == member_squareclasses[3]
    )
    member_squareclass_pair: tuple[int, int] | tuple[()] = (
        (member_squareclasses[0], member_squareclasses[2])
        if member_squareclasses_pairwise_equal
        else ()
    )
    product_square_explained_by_pairwise_squareclasses = (
        len(member_squareclasses) == 4
        and product_terms_are_squares == member_squareclasses_pairwise_equal
    )
    member_squareclasses_all_equal = (
        len(member_squareclasses) == 4 and len(set(member_squareclasses)) == 1
    )
    member_squareclasses_all_trivial = (
        len(member_squareclasses) == 4 and set(member_squareclasses) == {1}
    )
    centerline = len(positive_roots) == 2 and positive_roots[0] == positive_roots[1]
    reciprocal_pair = len(positive_roots) == 2 and positive_roots[0] * positive_roots[1] == lam
    if not product_terms_are_squares or len(positive_roots) != 2:
        product_square_bucket = "none"
    elif centerline:
        product_square_bucket = "centerline"
    elif reciprocal_pair:
        product_square_bucket = "reciprocal"
    else:
        product_square_bucket = "residual"
    centerline_obstruction = None
    if centerline:
        unit_leg_fails = (
            len(member_squareclass_pair) == 2 and member_squareclass_pair[0] != 1
        )
        lambda_leg_fails = (
            len(member_squareclass_pair) == 2 and member_squareclass_pair[1] != 1
        )
        if unit_leg_fails and lambda_leg_fails:
            centerline_obstruction = "both-legs"
        elif unit_leg_fails:
            centerline_obstruction = "unit-leg"
        elif lambda_leg_fails:
            centerline_obstruction = "lambda-leg"
    return ClosureProductSquareConditions(
        lambda_ratio=lam,
        target=t,
        product=p,
        relation=relation,
        identity_terms=terms,
        discriminant=discriminant,
        discriminant_is_square=sqrt_disc is not None,
        roots=positive_roots,
        centerline=centerline,
        reciprocal_pair=reciprocal_pair,
        product_square_bucket=product_square_bucket,
        product_terms_are_squares=product_terms_are_squares,
        member_square_flags=member_square_flags,
        member_squareclasses=member_squareclasses,
        member_squareclass_pair=member_squareclass_pair,
        member_squareclasses_pairwise_equal=member_squareclasses_pairwise_equal,
        product_square_explained_by_pairwise_squareclasses=(
            product_square_explained_by_pairwise_squareclasses
        ),
        member_squareclasses_all_equal=member_squareclasses_all_equal,
        member_squareclasses_all_trivial=member_squareclasses_all_trivial,
        centerline_obstruction=centerline_obstruction,
        true_member_pair=all(member_square_flags) if member_square_flags else False,
    )


def sum_ab_centerline_squareclass_conditions(
    lambda_ratio: Fraction | int,
) -> ClosureProductSquareConditions:
    """Return the ``sum=A+B`` centerline squareclass ledger ``r=s=(λ+1)/2``."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    center = (lam + 1) / 2
    return closure_product_square_conditions(
        lam,
        lam + 1,
        center * center,
        REL_SUM_AB,
    )


def sum_ab_centerline_equations(lambda_ratio: Fraction | int) -> SumAbCenterlineEquations:
    """Return the two square equations for a ``sum=A+B`` centerline point."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    center = (lam + 1) / 2
    unit_value = center * center + 1
    lambda_value = center * center + lam * lam
    unit_is_square = _is_rational_square(unit_value)
    lambda_is_square = _is_rational_square(lambda_value)
    if unit_is_square and lambda_is_square:
        obstruction = None
    elif unit_is_square:
        obstruction = "lambda-leg"
    elif lambda_is_square:
        obstruction = "unit-leg"
    else:
        obstruction = "both-legs"
    return SumAbCenterlineEquations(
        lambda_ratio=lam,
        center=center,
        unit_value=unit_value,
        lambda_value=lambda_value,
        unit_is_square=unit_is_square,
        lambda_is_square=lambda_is_square,
        unit_squareclass=_rational_squareclass(unit_value)[0],
        lambda_squareclass=_rational_squareclass(lambda_value)[0],
        true_member=unit_is_square and lambda_is_square,
        obstruction=obstruction,
    )


def sum_ab_centerline_from_unit_leg_param(
    parameter: Fraction | int,
) -> SumAbCenterlineUnitLegParam:
    """Parameterize the centerline after forcing ``center^2+1`` to be square."""
    t = _as_fraction(parameter)
    _validate_positive("parameter", t)
    denominator = 1 - t * t
    if denominator == 0:
        raise ValueError("parameter must not be 1")
    center = 2 * t / denominator
    if center <= 0:
        raise ValueError("parameter must produce a positive center")
    lam = 2 * center - 1
    if lam <= 0:
        raise ValueError("parameter must produce a positive lambda_ratio")
    unit_hypotenuse = (1 + t * t) / denominator
    equations = sum_ab_centerline_equations(lam)
    return SumAbCenterlineUnitLegParam(
        parameter=t,
        center=center,
        lambda_ratio=lam,
        unit_hypotenuse=unit_hypotenuse,
        equations=equations,
        remaining_squareclass=equations.lambda_squareclass,
        true_member=equations.true_member,
    )


def sum_ab_centerline_remaining_quartic(
    parameter: Fraction | int,
) -> SumAbCenterlineRemainingQuartic:
    """Return the quartic left after the centerline unit-leg parameterization."""
    t = _as_fraction(parameter)
    _validate_positive("parameter", t)
    denominator = 1 - t * t
    if denominator == 0:
        raise ValueError("parameter must not be 1")
    coefficients = (1, 8, 18, -8, 1)
    quartic_value = (
        t**4
        + 8 * t**3
        + 18 * t * t
        - 8 * t
        + 1
    )
    denominator_square = denominator * denominator
    lambda_value = quartic_value / denominator_square
    return SumAbCenterlineRemainingQuartic(
        parameter=t,
        coefficients=coefficients,
        quartic_value=quartic_value,
        denominator_square=denominator_square,
        lambda_value=lambda_value,
        squareclass=_rational_squareclass(lambda_value)[0],
        is_square=_is_rational_square(lambda_value),
    )


def sum_ab_centerline_quartic_self_similarity(
    parameter: Fraction | int,
) -> SumAbCenterlineQuarticSelfSimilarity:
    """Return the self-similar quadratic ledger for the centerline quartic."""
    q = _as_fraction(parameter)
    first_square_term = q * q + 4 * q - 1
    second_square_term = 2 * q
    quartic_value = first_square_term * first_square_term + second_square_term * second_square_term
    coefficients = (
        q,
        first_square_term,
        -q,
    )
    discriminant = first_square_term * first_square_term + 4 * q * q
    if q == 0:
        root_sum = None
        root_product = None
        roots_are_negative_reciprocals = False
        descent_warning = "degenerate-linear-root"
        roots = (Fraction(0),)
    else:
        root_sum = -first_square_term / q
        root_product = Fraction(-1)
        roots_are_negative_reciprocals = True
        descent_warning = "negative-reciprocal-roots"
        if _is_rational_square(discriminant):
            sqrt_discriminant = Fraction(
                isqrt(discriminant.numerator),
                isqrt(discriminant.denominator),
            )
            roots = tuple(
                sorted(
                    {
                        (-first_square_term - sqrt_discriminant) / (2 * q),
                        (-first_square_term + sqrt_discriminant) / (2 * q),
                    }
                )
            )
        else:
            roots = ()
    return SumAbCenterlineQuarticSelfSimilarity(
        parameter=q,
        quartic_value=quartic_value,
        first_square_term=first_square_term,
        second_square_term=second_square_term,
        quadratic_coefficients=coefficients,
        quadratic_discriminant=discriminant,
        quadratic_root_sum=root_sum,
        quadratic_root_product=root_product,
        roots_are_negative_reciprocals=roots_are_negative_reciprocals,
        direct_positive_descent_warning=descent_warning,
        has_rational_lift=bool(roots),
        lift_roots=roots,
    )


def sum_ab_centerline_quartic_negative_reciprocal_quotient(
    parameter: Fraction | int,
) -> SumAbCenterlineQuarticNegativeReciprocalQuotient:
    """Return the quotient ledger for the ``t -> -1/t`` quartic symmetry."""
    t = _as_fraction(parameter)
    if t == 0:
        raise ValueError("parameter must be nonzero")
    negative_reciprocal = -1 / t
    quotient_variable = t - 1 / t
    quartic_value = (
        t**4
        + 8 * t**3
        + 18 * t * t
        - 8 * t
        + 1
    )
    negative_reciprocal_quartic_value = (
        negative_reciprocal**4
        + 8 * negative_reciprocal**3
        + 18 * negative_reciprocal * negative_reciprocal
        - 8 * negative_reciprocal
        + 1
    )
    scaled_quartic_value = quartic_value / (t * t)
    quotient_quadratic_value = (
        quotient_variable * quotient_variable
        + 8 * quotient_variable
        + 20
    )
    coefficients = (
        Fraction(1),
        -quotient_variable,
        Fraction(-1),
    )
    reconstruction_discriminant = quotient_variable * quotient_variable + 4
    if _is_rational_square(reconstruction_discriminant):
        sqrt_discriminant = Fraction(
            isqrt(reconstruction_discriminant.numerator),
            isqrt(reconstruction_discriminant.denominator),
        )
        roots = tuple(
            sorted(
                {
                    (quotient_variable - sqrt_discriminant) / 2,
                    (quotient_variable + sqrt_discriminant) / 2,
                }
            )
        )
    else:
        roots = ()
    return SumAbCenterlineQuarticNegativeReciprocalQuotient(
        parameter=t,
        negative_reciprocal=negative_reciprocal,
        quotient_variable=quotient_variable,
        quartic_value=quartic_value,
        negative_reciprocal_quartic_value=negative_reciprocal_quartic_value,
        negative_reciprocal_symmetry_holds=(
            negative_reciprocal_quartic_value == quartic_value / t**4
        ),
        scaled_quartic_value=scaled_quartic_value,
        quotient_quadratic_value=quotient_quadratic_value,
        reconstructing_quadratic_coefficients=coefficients,
        reconstruction_discriminant=reconstruction_discriminant,
        reconstruction_discriminant_is_square=bool(roots),
        reconstruction_roots=roots,
    )


def sum_ab_centerline_quotient_w_parameterization(
    parameter: Fraction | int,
) -> SumAbCenterlineQuotientWParameterization:
    """Parameterize ``W²=u²+4`` and record the remaining quotient condition."""
    a = _as_fraction(parameter)
    if a == 0:
        raise ValueError("parameter must be nonzero")
    denominator = 1 - a * a
    if denominator == 0:
        raise ValueError("parameter must not be ±1")
    quotient_variable = 4 * a / denominator
    w_value = 2 * (1 + a * a) / denominator
    remaining_quartic_value = (
        5 * a**4
        - 8 * a**3
        - 6 * a * a
        + 8 * a
        + 5
    )
    z_square_value = 4 * remaining_quartic_value / (denominator * denominator)
    negative_reciprocal = -1 / a
    negative_reciprocal_remaining_quartic_value = (
        5 * negative_reciprocal**4
        - 8 * negative_reciprocal**3
        - 6 * negative_reciprocal * negative_reciprocal
        + 8 * negative_reciprocal
        + 5
    )
    second_quotient_variable = a - 1 / a
    second_quotient_quadratic_value = (
        5 * second_quotient_variable * second_quotient_variable
        - 8 * second_quotient_variable
        + 4
    )
    remaining_over_square = remaining_quartic_value / (a * a)
    return SumAbCenterlineQuotientWParameterization(
        parameter=a,
        quotient_variable=quotient_variable,
        w_value=w_value,
        w_condition_holds=w_value * w_value == quotient_variable * quotient_variable + 4,
        remaining_quartic_value=remaining_quartic_value,
        z_square_value=z_square_value,
        z_square_value_is_square=_is_rational_square(z_square_value),
        negative_reciprocal_parameter=negative_reciprocal,
        negative_reciprocal_remaining_quartic_value=negative_reciprocal_remaining_quartic_value,
        negative_reciprocal_symmetry_holds=(
            negative_reciprocal_remaining_quartic_value
            == remaining_quartic_value / a**4
        ),
        second_quotient_variable=second_quotient_variable,
        second_quotient_quadratic_value=second_quotient_quadratic_value,
        remaining_quartic_over_parameter_square=remaining_over_square,
    )


def _pari_point_strings(points) -> tuple[tuple[str, str], ...]:
    return tuple(sorted((str(point[0]), str(point[1])) for point in points))


def _pari_integral_points(points) -> tuple[tuple[int, int], ...]:
    integral_points: list[tuple[int, int]] = []
    for point in points:
        x = point[0]
        y = point[1]
        if str(x).lstrip("-").isdigit() and str(y).lstrip("-").isdigit():
            integral_points.append((int(x), int(y)))
    return tuple(sorted(integral_points))


def sum_ab_centerline_quartic_pari_diagnostics(
    *,
    point_height_bound: int = 100,
) -> SumAbCenterlineQuarticPARIDiagnostics:
    """Return PARI rank/torsion diagnostics for the centerline quartics."""
    try:
        import cypari2
    except ImportError as exc:
        return SumAbCenterlineQuarticPARIDiagnostics(
            available=False,
            centerline_model=(),
            centerline_rank_bounds=(),
            centerline_sha2_lower=None,
            centerline_generators=(),
            centerline_torsion_order=None,
            centerline_small_points=(),
            w_parameterized_model=(),
            w_parameterized_rank_bounds=(),
            w_parameterized_sha2_lower=None,
            w_parameterized_generators=(),
            w_parameterized_torsion_order=None,
            w_parameterized_small_points=(),
            proof_status="pari-unavailable",
            notes=f"cypari2 unavailable: {exc}",
        )
    try:
        pari = cypari2.Pari()
        models: list[tuple[int, int, int, int, int]] = []
        rank_bounds: list[tuple[int, int]] = []
        sha2_lowers: list[int] = []
        generators: list[tuple[tuple[str, str], ...]] = []
        torsion_orders: list[int] = []
        small_points: list[tuple[tuple[int, int], ...]] = []
        polynomials = (
            "x^4+8*x^3+18*x^2-8*x+1",
            "5*x^4-8*x^3-6*x^2+8*x+5",
        )
        for polynomial in polynomials:
            model = pari(f"ellfromeqn(y^2-({polynomial}))")
            models.append(tuple(int(model[i]) for i in range(5)))
            curve = pari.ellinit(model)
            rank_result = pari.ellrank(curve, 1)
            rank_bounds.append((int(rank_result[0]), int(rank_result[1])))
            sha2_lowers.append(int(rank_result[2]))
            generators.append(_pari_point_strings(rank_result[3]))
            torsion = pari.elltors(curve)
            torsion_orders.append(int(torsion[0]))
            points = pari.ellratpoints(curve, point_height_bound)
            small_points.append(_pari_integral_points(points))
    except Exception as exc:
        return SumAbCenterlineQuarticPARIDiagnostics(
            available=False,
            centerline_model=(),
            centerline_rank_bounds=(),
            centerline_sha2_lower=None,
            centerline_generators=(),
            centerline_torsion_order=None,
            centerline_small_points=(),
            w_parameterized_model=(),
            w_parameterized_rank_bounds=(),
            w_parameterized_sha2_lower=None,
            w_parameterized_generators=(),
            w_parameterized_torsion_order=None,
            w_parameterized_small_points=(),
            proof_status="pari-error",
            notes=f"PARI diagnostics failed: {exc}",
        )
    return SumAbCenterlineQuarticPARIDiagnostics(
        available=True,
        centerline_model=models[0],
        centerline_rank_bounds=rank_bounds[0],
        centerline_sha2_lower=sha2_lowers[0],
        centerline_generators=generators[0],
        centerline_torsion_order=torsion_orders[0],
        centerline_small_points=small_points[0],
        w_parameterized_model=models[1],
        w_parameterized_rank_bounds=rank_bounds[1],
        w_parameterized_sha2_lower=sha2_lowers[1],
        w_parameterized_generators=generators[1],
        w_parameterized_torsion_order=torsion_orders[1],
        w_parameterized_small_points=small_points[1],
        proof_status="needs-birational-pullback",
        notes=(
            "PARI gives rank-zero elliptic models; proof still needs an explicit "
            "birational pullback from torsion points to quartic points."
        ),
    )


def sum_ab_centerline_quartic_integer_equation(
    u: int,
    v: int,
) -> SumAbCenterlineQuarticIntegerEquation:
    """Return the integer quartic for ``t=u/v`` in the centerline branch."""
    if u <= 0:
        raise ValueError("u must be positive")
    if v <= 0:
        raise ValueError("v must be positive")
    value = (
        u**4
        + 8 * u**3 * v
        + 18 * u * u * v * v
        - 8 * u * v**3
        + v**4
    )
    denominator_square = (v * v - u * u) ** 2
    reduced_lambda_value = Fraction(value, denominator_square)
    return SumAbCenterlineQuarticIntegerEquation(
        u=u,
        v=v,
        value=value,
        denominator_square=denominator_square,
        reduced_lambda_value=reduced_lambda_value,
        squareclass=_rational_squareclass(reduced_lambda_value)[0],
        is_square=_is_rational_square(reduced_lambda_value),
    )


def sum_ab_centerline_quartic_residue_summary(
    modulus: int,
) -> SumAbCenterlineQuarticResidueSummary:
    """Summarize square-residue hits of the centerline quartic modulo ``modulus``."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    square_residues = tuple(sorted({value * value % modulus for value in range(modulus)}))
    square_residue_set = set(square_residues)
    square_classes = 0
    zero_classes = 0
    for u in range(modulus):
        for v in range(modulus):
            value = (
                u**4
                + 8 * u**3 * v
                + 18 * u * u * v * v
                - 8 * u * v**3
                + v**4
            ) % modulus
            if value in square_residue_set:
                square_classes += 1
            if value == 0:
                zero_classes += 1
    total = modulus * modulus
    return SumAbCenterlineQuarticResidueSummary(
        modulus=modulus,
        total_classes=total,
        square_residue_classes=square_classes,
        non_square_residue_classes=total - square_classes,
        zero_residue_classes=zero_classes,
        square_residues=square_residues,
    )


def sum_ab_centerline_quartic_primitive_residue_summary(
    modulus: int,
) -> SumAbCenterlineQuarticPrimitiveResidueSummary:
    """Summarize quartic residues for primitive classes with nonzero denominator."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    square_residues = tuple(sorted({value * value % modulus for value in range(modulus)}))
    square_residue_set = set(square_residues)
    primitive_classes = 0
    degenerate_classes = 0
    square_classes = 0
    zero_classes = 0
    for u in range(modulus):
        for v in range(modulus):
            if _gcd(_gcd(u, v), modulus) != 1:
                continue
            primitive_classes += 1
            if (v * v - u * u) % modulus == 0:
                degenerate_classes += 1
                continue
            value = (
                u**4
                + 8 * u**3 * v
                + 18 * u * u * v * v
                - 8 * u * v**3
                + v**4
            ) % modulus
            if value in square_residue_set:
                square_classes += 1
            if value == 0:
                zero_classes += 1
    total = primitive_classes - degenerate_classes
    return SumAbCenterlineQuarticPrimitiveResidueSummary(
        modulus=modulus,
        primitive_classes=primitive_classes,
        degenerate_denominator_classes=degenerate_classes,
        total_classes=total,
        square_residue_classes=square_classes,
        non_square_residue_classes=total - square_classes,
        zero_residue_classes=zero_classes,
        square_residues=square_residues,
    )


def _sum_ab_centerline_quartic_residue(u: int, v: int, modulus: int) -> int:
    return (
        u**4
        + 8 * u**3 * v
        + 18 * u * u * v * v
        - 8 * u * v**3
        + v**4
    ) % modulus


def _sum_ab_centerline_square_primitive_residue_classes(
    modulus: int,
) -> tuple[tuple[int, int, int, bool], ...]:
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    square_residues = {value * value % modulus for value in range(modulus)}
    classes: list[tuple[int, int, int, bool]] = []
    for u in range(modulus):
        for v in range(modulus):
            if _gcd(_gcd(u, v), modulus) != 1:
                continue
            residue = _sum_ab_centerline_quartic_residue(u, v, modulus)
            if residue not in square_residues:
                continue
            denominator_degenerate = (v * v - u * u) % modulus == 0
            classes.append((u, v, residue, denominator_degenerate))
    return tuple(classes)


def sum_ab_centerline_quartic_live_residue_classes(
    modulus: int,
) -> tuple[SumAbCenterlineQuarticLiveResidueClass, ...]:
    """Return primitive nondegenerate classes where the quartic is a square residue."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    square_residues = {value * value % modulus for value in range(modulus)}
    live: list[SumAbCenterlineQuarticLiveResidueClass] = []
    for u in range(modulus):
        for v in range(modulus):
            if _gcd(_gcd(u, v), modulus) != 1:
                continue
            if (v * v - u * u) % modulus == 0:
                continue
            residue = _sum_ab_centerline_quartic_residue(u, v, modulus)
            if residue in square_residues:
                live.append(
                    SumAbCenterlineQuarticLiveResidueClass(
                        u=u,
                        v=v,
                        residue=residue,
                    )
                )
    return tuple(live)


def _crt_pair(left_value: int, left_modulus: int, right_value: int, right_modulus: int) -> int:
    right_inverse = pow(left_modulus, -1, right_modulus)
    lift = ((right_value - left_value) * right_inverse) % right_modulus
    return (left_value + left_modulus * lift) % (left_modulus * right_modulus)


def sum_ab_centerline_quartic_crt_live_residue_classes(
    left_modulus: int,
    right_modulus: int,
) -> tuple[SumAbCenterlineQuarticLiveResidueClass, ...]:
    """Merge square primitive classes into live classes modulo ``mn`` by CRT."""
    if left_modulus <= 0 or right_modulus <= 0:
        raise ValueError("moduli must be positive")
    if _gcd(left_modulus, right_modulus) != 1:
        raise ValueError("moduli must be coprime")
    left_classes = _sum_ab_centerline_square_primitive_residue_classes(left_modulus)
    right_classes = _sum_ab_centerline_square_primitive_residue_classes(right_modulus)
    combined_modulus = left_modulus * right_modulus
    merged: set[SumAbCenterlineQuarticLiveResidueClass] = set()
    for left_u, left_v, _, left_degenerate in left_classes:
        for right_u, right_v, _, right_degenerate in right_classes:
            if left_degenerate and right_degenerate:
                continue
            u = _crt_pair(left_u, left_modulus, right_u, right_modulus)
            v = _crt_pair(left_v, left_modulus, right_v, right_modulus)
            if _gcd(_gcd(u, v), combined_modulus) != 1:
                continue
            if (v * v - u * u) % combined_modulus == 0:
                continue
            residue = _sum_ab_centerline_quartic_residue(u, v, combined_modulus)
            merged.add(
                SumAbCenterlineQuarticLiveResidueClass(
                    u=u,
                    v=v,
                    residue=residue,
                )
            )
    return tuple(sorted(merged))


def sum_ab_centerline_quartic_crt_live_residue_summary(
    left_modulus: int,
    right_modulus: int,
) -> SumAbCenterlineQuarticCRTLiveResidueSummary:
    """Summarize CRT propagation and compare it with direct enumeration."""
    left_classes = _sum_ab_centerline_square_primitive_residue_classes(left_modulus)
    right_classes = _sum_ab_centerline_square_primitive_residue_classes(right_modulus)
    left_live_count = sum(not item[3] for item in left_classes)
    right_live_count = sum(not item[3] for item in right_classes)
    left_degenerate_count = len(left_classes) - left_live_count
    right_degenerate_count = len(right_classes) - right_live_count
    live_live_pairs = left_live_count * right_live_count
    one_sided_degenerate_pairs = (
        left_degenerate_count * right_live_count
        + left_live_count * right_degenerate_count
    )
    both_degenerate_pairs = left_degenerate_count * right_degenerate_count
    merged_live_classes = sum_ab_centerline_quartic_crt_live_residue_classes(
        left_modulus,
        right_modulus,
    )
    combined_modulus = left_modulus * right_modulus
    direct_live_classes = sum_ab_centerline_quartic_live_residue_classes(combined_modulus)
    return SumAbCenterlineQuarticCRTLiveResidueSummary(
        left_modulus=left_modulus,
        right_modulus=right_modulus,
        combined_modulus=combined_modulus,
        left_square_primitive_classes=len(left_classes),
        right_square_primitive_classes=len(right_classes),
        left_live_classes=left_live_count,
        right_live_classes=right_live_count,
        left_degenerate_square_classes=left_degenerate_count,
        right_degenerate_square_classes=right_degenerate_count,
        live_live_pairs=live_live_pairs,
        one_sided_degenerate_pairs=one_sided_degenerate_pairs,
        both_degenerate_pairs=both_degenerate_pairs,
        merged_live_classes=len(merged_live_classes),
        direct_live_classes=len(direct_live_classes),
        matches_direct=merged_live_classes == direct_live_classes,
    )


def square_rectangle_terms(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    mover: Fraction | int,
) -> SquareRectangleTerms:
    """Return the four square-candidate corners from the wl113 rectangle model.

    The unified form is:

        (M-T)^2 + 4
        (M+T)^2 + 4
        (M-T)^2 + 4lambda^2
        (M+T)^2 + 4lambda^2

    For sum closure, ``M`` is ``q=s-r``.  For difference closure, ``M`` is
    ``L=r+s``.
    """
    lam = _as_fraction(lambda_ratio)
    t = _as_fraction(target)
    m = _as_fraction(mover)
    _validate_positive("lambda_ratio", lam)
    if t <= 0:
        raise ValueError("target must be positive")
    lam_sq = lam * lam
    left = m - t
    right = m + t
    return SquareRectangleTerms(
        lambda_ratio=lam,
        target=t,
        mover=m,
        x=left * left + 4,
        y=right * right + 4,
        z=left * left + 4 * lam_sq,
        w=right * right + 4 * lam_sq,
    )


def reciprocal_closure_roots(
    lambda_ratio: Fraction | int,
    relation: str,
) -> tuple[ReciprocalClosureRoot, ...]:
    """Return rational same-orbit roots for one closure relation.

    This intentionally separates "the quadratic has rational roots" from
    "those roots are true ``R_lambda`` points"; the distinction is the main
    pitfall when upgrading integer ``k`` proofs to rational ``lambda``.
    """
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    roots: list[Fraction] = []
    if relation == REL_SUM_AB:
        roots = list(reciprocal_sum_ab_roots(lam))
    elif relation == REL_DIFF_DIFF:
        roots = [Fraction(1), lam]
    elif relation == REL_SUM_DIFF:
        target = abs(lam - 1)
        sqrt_disc = _rational_sqrt(target * target - 4 * lam)
        if sqrt_disc is not None:
            roots = [(target - sqrt_disc) / 2, (target + sqrt_disc) / 2]
    elif relation == REL_DIFF_AB:
        target = lam + 1
        sqrt_disc = _rational_sqrt(target * target + 4 * lam)
        if sqrt_disc is not None:
            roots = [(target - sqrt_disc) / 2, (target + sqrt_disc) / 2]
    else:
        raise ValueError(f"unknown relation: {relation}")

    out = [
        ReciprocalClosureRoot(
            r=root,
            relation=relation,
            true_member=is_rational_ratio_member(lam, root),
        )
        for root in sorted(set(roots))
        if root > 0
    ]
    return tuple(out)


def reciprocal_closure_squareclass_ledger(
    lambda_ratio: Fraction | int,
    relation: str,
) -> tuple[ReciprocalClosureSquareclassRoot, ...]:
    """Return squareclass diagnostics for reciprocal/mirror closure roots."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    rows: list[ReciprocalClosureSquareclassRoot] = []
    for root in reciprocal_closure_roots(lam, relation):
        unit_value = root.r * root.r + 1
        lambda_value = root.r * root.r + lam * lam
        rows.append(
            ReciprocalClosureSquareclassRoot(
                r=root.r,
                relation=root.relation,
                unit_value=unit_value,
                lambda_value=lambda_value,
                unit_squareclass=_rational_squareclass(unit_value)[0],
                lambda_squareclass=_rational_squareclass(lambda_value)[0],
                true_member=root.true_member,
            )
        )
    return tuple(rows)


def reciprocal_closure_discriminant_ledger(
    lambda_ratio: Fraction | int,
    relation: str,
) -> ReciprocalClosureDiscriminantLedger:
    """Return the discriminant ledger for the two quadratic reciprocal branches."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    if relation == REL_SUM_DIFF:
        target = abs(lam - 1)
        discriminant = target * target - 4 * lam
    elif relation == REL_DIFF_AB:
        target = lam + 1
        discriminant = target * target + 4 * lam
    else:
        raise ValueError(
            "discriminant ledger is only defined for sum=|A-B| and diff=A+B"
        )

    roots = reciprocal_closure_squareclass_ledger(lam, relation)
    true_roots = tuple(row.r for row in roots if row.true_member)
    discriminant_squareclass = (
        _rational_squareclass(discriminant)[0] if discriminant > 0 else None
    )
    return ReciprocalClosureDiscriminantLedger(
        lambda_ratio=lam,
        lambda_numerator=lam.numerator,
        lambda_denominator=lam.denominator,
        relation=relation,
        target=target,
        discriminant=discriminant,
        discriminant_numerator=discriminant.numerator,
        discriminant_denominator=discriminant.denominator,
        discriminant_is_square=_is_rational_square(discriminant),
        discriminant_squareclass=discriminant_squareclass,
        discriminant_integer_squareclass=(
            _integer_squareclass(discriminant.numerator * discriminant.denominator)
            if discriminant > 0
            else None
        ),
        roots=roots,
        true_roots=true_roots,
        branch_closed=true_roots == (),
    )


def full_plane_reciprocal_obstruction(
    lambda_ratio: Fraction | int,
) -> FullPlaneReciprocalObstruction:
    """Return the reciprocal/mirror obstruction ledger for all full-plane relations."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    by_relation: dict[str, ReciprocalClosureObstruction] = {}
    for relation in (REL_SUM_AB, REL_SUM_DIFF, REL_DIFF_AB, REL_DIFF_DIFF):
        roots = reciprocal_closure_roots(lam, relation)
        true_roots = tuple(root.r for root in roots if root.true_member)
        by_relation[relation] = ReciprocalClosureObstruction(
            relation=relation,
            roots=tuple(root.r for root in roots),
            true_roots=true_roots,
            branch_closed=true_roots == (),
        )
    return FullPlaneReciprocalObstruction(
        lambda_ratio=lam,
        by_relation=by_relation,
        all_branches_closed=all(row.branch_closed for row in by_relation.values()),
    )


__all__ = [
    "ClosureIdentitySharedGcdLedger",
    "ClosureIdentitySharedGcdRow",
    "ClosureIdentityThreeModFourBalanceLedger",
    "ClosureIdentityThreeModFourBalanceRow",
    "ClosureMemberPrimeValuationLedger",
    "ClosureMemberPrimeValuationRow",
    "ClosureMemberProductSquareLedger",
    "ClosureProductSquareConditions",
    "FullPlaneClosureProductLedger",
    "FullPlaneClosureProductSummary",
    "FullPlaneReciprocalObstruction",
    "FullPlaneTrueClosureRelation",
    "GaussianShadowObstructionSummary",
    "GaussianShadowSummary",
    "InverseGaussianAbsorptionPair",
    "InverseGaussianAbsorptionPairTerms",
    "InverseGaussianCenterlineShadowObstruction",
    "LegRatioSquareclass",
    "ProductIdentityTerms",
    "ProductSquareBucketSummary",
    "PythagoreanLegParam",
    "RationalRatioHit",
    "RationalRatioHitProductDiagnostic",
    "ReciprocalClosureDiscriminantLedger",
    "ReciprocalClosureObstruction",
    "ReciprocalClosureRoot",
    "ReciprocalClosureSquareclassRoot",
    "ResidualGaussianAbsorptionLedger",
    "ResidualPrimeClassSummary",
    "ResidualSquareclassEquations",
    "SquareRectangleTerms",
    "SquareclassTwoSquareAbsorption",
    "SumAbBridgeExtraFactorZLemmaReduction",
    "SumAbCenterlineEquations",
    "SumAbCenterlineQuarticCRTLiveResidueSummary",
    "SumAbCenterlineQuarticIntegerEquation",
    "SumAbCenterlineQuarticLiveResidueClass",
    "SumAbCenterlineQuarticNegativeReciprocalQuotient",
    "SumAbCenterlineQuarticPARIDiagnostics",
    "SumAbCenterlineQuarticPrimitiveResidueSummary",
    "SumAbCenterlineQuarticResidueSummary",
    "SumAbCenterlineQuarticSelfSimilarity",
    "SumAbCenterlineQuotientWParameterization",
    "SumAbCenterlineRemainingQuartic",
    "SumAbCenterlineUnitLegParam",
    "SumAbDualSlopeBridgeCenterlineBranchRestriction",
    "SumAbDualSlopeBridgeCenterlineFactorLiftSummary",
    "SumAbDualSlopeBridgeDifferenceFactorization",
    "SumAbDualSlopeBridgePrimePowerLiftSummary",
    "SumAbDualSlopeBridgeProjectiveResidueSummary",
    "SumAbDualSlopeBridgeTrivialTubeExpansion",
    "SumAbDualSlopeCenterlineFactorPositiveDomainRow",
    "SumAbDualSlopeGaussianAbsorption",
    "SumAbDualSlopeGaussianBridge",
    "SumAbDualSlopeGaussianBridgeCycle",
    "SumAbDualSlopeParameterization",
    "SumAbDualSlopePositiveTrivialTubeLocalWitness",
    "SumAbDualSlopePositiveTrivialTubeMemberLedger",
    "SumAbDualSlopePositiveTrivialTubeSquareclassLedger",
    "SumAbDualSlopeQAdicBridgeLocalSquareSummary",
    "SumAbDualSlopeQAdicBridgeTwoAdicSummary",
    "SumAbDualSlopeQAdicBridgeValuationRow",
    "SumAbDualSlopeQAdicBridgeValuationSummary",
    "SumAbDualSlopeQAdicNormBridgeLedger",
    "SumAbDualSlopeQAdicNormBridgeSummary",
    "SumAbDualSlopeQAdicNormGeneratedSummary",
    "SumAbDualSlopeQAdicNormLedger",
    "SumAbDualSlopeQAdicNormSummary",
    "SumAbDualSlopeValuationLedger",
    "SumAbDualSlopeValuationRow",
    "SumAbFourSlopeSquareclassSummary",
    "SumAbFourSlopeSquareclassWitness",
    "SumAbFourSquareDualSlopeModel",
    "SumAbKDiscriminantQuarticCompletion",
    "SumAbKSquareCandidateYDiscriminant",
    "SumAbKSquareYDiscriminantFactorization",
    "SumAbNewCurveResidueSummary",
    "SumAbNewCurveZReduction",
    "SumAbRatioShadowOrbit",
    "SumAbReciprocalObstruction",
    "SumAbSameOrientationBothPassLiftSummary",
    "SumAbSameOrientationBothPassResidueSummary",
    "SumAbSameOrientationCombinedValuationSummary",
    "SumAbSameOrientationDifferenceFactorValuationSummary",
    "SumAbSharedOddPrimePowerLiftSummary",
    "SumAbSharedOddPrimeResidueCase",
    "SumAbSharedOddPrimeResidueSummary",
    "SumAbSlopeObstruction",
    "SumAbSlopePoint",
    "SumAbSquareclassRatioSlopeQuadraticModel",
    "SumAbSquareclassRatioTUQuotientModel",
    "SumAbSquareclassRatioZParameterization",
    "SumAbSquareclassRatioZReduction",
    "SumAbThreePassEuclidModel",
    "SumAbThreePassMobiusModel",
    "SumAbTrueClosureRelation",
    "SumAbZLemmaCenterlineBridge",
    "closure_identity_shared_gcd_ledger",
    "closure_identity_three_mod_four_balance_ledger",
    "closure_member_prime_valuation_ledger",
    "closure_member_product_square_ledger",
    "closure_product_identity_terms",
    "closure_product_square_conditions",
    "find_rational_ratio_hits",
    "full_plane_closure_product_ledger",
    "full_plane_closure_product_summary",
    "full_plane_reciprocal_obstruction",
    "full_plane_true_closure_relation",
    "group_sum_ab_ratio_shadow_orbits",
    "inverse_gaussian_absorption_pair",
    "inverse_gaussian_absorption_pair_terms",
    "inverse_gaussian_centerline_shadow_obstruction",
    "is_pythagorean_leg_ratio",
    "is_rational_ratio_member",
    "leg_ratio_squareclass",
    "positive_rational_ratios",
    "product_identity_terms",
    "pythagorean_leg_ratio_from_param",
    "pythagorean_leg_ratios",
    "rational_ratio_hit_product_diagnostics",
    "reciprocal_closure_discriminant_ledger",
    "reciprocal_closure_roots",
    "reciprocal_closure_squareclass_ledger",
    "reciprocal_ratio",
    "reciprocal_sum_ab_roots",
    "residual_gaussian_absorption_ledger",
    "scan_full_plane_true_closure_relations",
    "scan_sum_ab_slope_obstructions",
    "scan_sum_ab_slope_pairs",
    "scan_sum_ab_true_closure_relations",
    "square_rectangle_terms",
    "squareclass_two_square_absorption",
    "sum_ab_bridge_extra_factor_z_lemma_reduction",
    "sum_ab_centerline_equations",
    "sum_ab_centerline_from_unit_leg_param",
    "sum_ab_centerline_quartic_crt_live_residue_classes",
    "sum_ab_centerline_quartic_crt_live_residue_summary",
    "sum_ab_centerline_quartic_integer_equation",
    "sum_ab_centerline_quartic_live_residue_classes",
    "sum_ab_centerline_quartic_negative_reciprocal_quotient",
    "sum_ab_centerline_quartic_pari_diagnostics",
    "sum_ab_centerline_quartic_primitive_residue_summary",
    "sum_ab_centerline_quartic_residue_summary",
    "sum_ab_centerline_quartic_self_similarity",
    "sum_ab_centerline_quotient_w_parameterization",
    "sum_ab_centerline_remaining_quartic",
    "sum_ab_centerline_squareclass_conditions",
    "sum_ab_dual_slope_bridge_centerline_branch_restrictions",
    "sum_ab_dual_slope_bridge_centerline_factor_lift_summary",
    "sum_ab_dual_slope_bridge_difference_factorization",
    "sum_ab_dual_slope_bridge_prime_power_lift_summary",
    "sum_ab_dual_slope_bridge_projective_residue_summary",
    "sum_ab_dual_slope_bridge_trivial_tube_expansions",
    "sum_ab_dual_slope_centerline_factor_positive_domain",
    "sum_ab_dual_slope_gaussian_absorption",
    "sum_ab_dual_slope_gaussian_bridge",
    "sum_ab_dual_slope_gaussian_bridge_cycle",
    "sum_ab_dual_slope_parameterization",
    "sum_ab_dual_slope_positive_trivial_tube_local_witnesses",
    "sum_ab_dual_slope_positive_trivial_tube_member_ledgers",
    "sum_ab_dual_slope_positive_trivial_tube_squareclass_ledgers",
    "sum_ab_dual_slope_qadic_bridge_2adic_summary",
    "sum_ab_dual_slope_qadic_bridge_local_square_summary",
    "sum_ab_dual_slope_qadic_bridge_valuation_summary",
    "sum_ab_dual_slope_qadic_norm_bridge_summary",
    "sum_ab_dual_slope_qadic_norm_generated_summary",
    "sum_ab_dual_slope_qadic_norm_ledger",
    "sum_ab_dual_slope_qadic_norm_summary",
    "sum_ab_dual_slope_valuation_ledger",
    "sum_ab_four_slope_squareclass_summary",
    "sum_ab_four_slope_squareclass_witnesses",
    "sum_ab_four_square_dual_slope_model",
    "sum_ab_k_discriminant_quartic_completion",
    "sum_ab_k_square_candidate_y_discriminant",
    "sum_ab_k_square_y_discriminant_factorization",
    "sum_ab_new_curve_residue_summary",
    "sum_ab_new_curve_z_reduction",
    "sum_ab_point_from_slopes",
    "sum_ab_product_square_bucket_summary",
    "sum_ab_product_square_condition_from_slopes",
    "sum_ab_product_square_residuals_from_grid",
    "sum_ab_product_square_residuals_from_root_grid",
    "sum_ab_ratio_shadow_key",
    "sum_ab_reciprocal_obstruction",
    "sum_ab_residual_squareclass_equations",
    "sum_ab_root_grid_gaussian_shadow_obstruction_summary",
    "sum_ab_root_grid_gaussian_shadow_summary",
    "sum_ab_root_grid_residual_prime_class_summary",
    "sum_ab_root_grid_residual_summary",
    "sum_ab_root_grid_residual_watchlist",
    "sum_ab_same_orientation_both_pass_lift_summary",
    "sum_ab_same_orientation_both_pass_residue_summary",
    "sum_ab_same_orientation_combined_valuation_summary",
    "sum_ab_same_orientation_difference_factor_valuation_summary",
    "sum_ab_shared_odd_prime_power_lift_summary",
    "sum_ab_shared_odd_prime_residue_summary",
    "sum_ab_slope_obstruction",
    "sum_ab_slope_ratio_y_discriminant_ledger",
    "sum_ab_squareclass_ratio_slope_quadratic_model",
    "sum_ab_squareclass_ratio_tu_quotient_model",
    "sum_ab_squareclass_ratio_z_parameterization",
    "sum_ab_squareclass_ratio_z_reduction",
    "sum_ab_three_pass_mobius_model",
    "sum_ab_three_pass_mobius_model_from_params",
    "sum_ab_true_closure_relation",
    "sum_ab_z_lemma_centerline_bridge",
    "true_reciprocal_sum_ab_roots",
]
