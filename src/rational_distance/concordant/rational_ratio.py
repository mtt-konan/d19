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
from math import gcd as _gcd
from math import isqrt

from sympy import factorint

REL_SUM_AB = "sum=A+B"
REL_SUM_DIFF = "sum=|A-B|"
REL_DIFF_AB = "diff=A+B"
REL_DIFF_DIFF = "diff=|A-B|"


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
    product_terms_are_squares: bool
    member_square_flags: tuple[bool, bool, bool, bool] | tuple[()]
    member_squareclasses: tuple[int, int, int, int] | tuple[()]
    true_member_pair: bool


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
    other_denominator: int
    failed_denominator: int
    denominator_difference: int
    denominator_sum: int
    nu_minus_mv: int
    difference_factorization: tuple[int, int, int]
    sum_factorization: tuple[int, int, int]


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
    return SumAbSameOrientationDenominatorFactorization(
        orientation=orientation,
        other_denominator=shared_terms.other_denominator,
        failed_denominator=shared_terms.failed_denominator,
        denominator_difference=shared_terms.other_denominator
        - shared_terms.failed_denominator,
        denominator_sum=shared_terms.other_denominator + shared_terms.failed_denominator,
        nu_minus_mv=nu_minus_mv,
        difference_factorization=(
            difference_sign,
            first_difference_factor,
            nu_minus_mv,
        ),
        sum_factorization=(2, first_sum_factor, second_sum_factor),
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


def reciprocal_sum_ab_roots(lambda_ratio: Fraction | int) -> tuple[Fraction, Fraction]:
    """Return roots forced by ``r + lambda/r = lambda + 1``.

    Algebraically the roots are always ``1`` and ``lambda``.  They need not be
    true ``R_lambda`` members; use :func:`true_reciprocal_sum_ab_roots` for that.
    """
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    return (Fraction(1), lam)


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
        sqrt_disc = _rational_sqrt(discriminant)
        roots = (
            tuple(sorted(((t - sqrt_disc) / 2, (t + sqrt_disc) / 2)))
            if sqrt_disc is not None
            else ()
        )
    elif relation.startswith("diff="):
        discriminant = t * t + 4 * p
        sqrt_disc = _rational_sqrt(discriminant)
        roots = (
            tuple(sorted(((sqrt_disc - t) / 2, (sqrt_disc + t) / 2)))
            if sqrt_disc is not None
            else ()
        )
    else:
        raise ValueError(f"unknown closure relation: {relation}")

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
    return ClosureProductSquareConditions(
        lambda_ratio=lam,
        target=t,
        product=p,
        relation=relation,
        identity_terms=terms,
        discriminant=discriminant,
        discriminant_is_square=sqrt_disc is not None,
        roots=positive_roots,
        product_terms_are_squares=product_terms_are_squares,
        member_square_flags=member_square_flags,
        member_squareclasses=member_squareclasses,
        true_member_pair=all(member_square_flags) if member_square_flags else False,
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


__all__ = [
    "ClosureProductSquareConditions",
    "LegRatioSquareclass",
    "ProductIdentityTerms",
    "PythagoreanLegParam",
    "RationalRatioHit",
    "RationalRatioHitProductDiagnostic",
    "ReciprocalClosureRoot",
    "SquareRectangleTerms",
    "SumAbRatioShadowOrbit",
    "SumAbThreePassEuclidModel",
    "SumAbSlopeObstruction",
    "SumAbSlopePoint",
    "SumAbThreePassMobiusModel",
    "closure_product_identity_terms",
    "closure_product_square_conditions",
    "find_rational_ratio_hits",
    "group_sum_ab_ratio_shadow_orbits",
    "is_pythagorean_leg_ratio",
    "is_rational_ratio_member",
    "leg_ratio_squareclass",
    "product_identity_terms",
    "pythagorean_leg_ratios",
    "pythagorean_leg_ratio_from_param",
    "rational_ratio_hit_product_diagnostics",
    "reciprocal_closure_roots",
    "reciprocal_ratio",
    "reciprocal_sum_ab_roots",
    "scan_sum_ab_slope_obstructions",
    "scan_sum_ab_slope_pairs",
    "square_rectangle_terms",
    "sum_ab_point_from_slopes",
    "sum_ab_ratio_shadow_key",
    "sum_ab_slope_obstruction",
    "sum_ab_three_pass_mobius_model_from_params",
    "sum_ab_three_pass_mobius_model",
    "true_reciprocal_sum_ab_roots",
]
