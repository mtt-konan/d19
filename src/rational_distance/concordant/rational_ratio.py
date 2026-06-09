"""Rational fixed-ratio ``A / B = lambda`` identities.

This module is the proof-side analogue of :mod:`fixed_ratio_exact`.  It does
not generate integer candidates.  Instead it records exact ``Fraction``-level
identities that still make sense after replacing an integer ratio ``k`` by an
arbitrary positive rational ratio ``lambda``.
"""

from __future__ import annotations

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
class RationalRatioHit:
    """A ratio-level full-plane closure hit for rational ``A/B``."""

    r1: Fraction
    r2: Fraction
    relation: str
    centerline: bool


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
    "LegRatioSquareclass",
    "ProductIdentityTerms",
    "RationalRatioHit",
    "ReciprocalClosureRoot",
    "SquareRectangleTerms",
    "SumAbRatioShadowOrbit",
    "SumAbSlopeObstruction",
    "SumAbSlopePoint",
    "SumAbThreePassMobiusModel",
    "closure_product_identity_terms",
    "find_rational_ratio_hits",
    "group_sum_ab_ratio_shadow_orbits",
    "is_pythagorean_leg_ratio",
    "is_rational_ratio_member",
    "leg_ratio_squareclass",
    "product_identity_terms",
    "pythagorean_leg_ratios",
    "reciprocal_closure_roots",
    "reciprocal_ratio",
    "reciprocal_sum_ab_roots",
    "scan_sum_ab_slope_obstructions",
    "scan_sum_ab_slope_pairs",
    "square_rectangle_terms",
    "sum_ab_point_from_slopes",
    "sum_ab_ratio_shadow_key",
    "sum_ab_slope_obstruction",
    "sum_ab_three_pass_mobius_model",
    "true_reciprocal_sum_ab_roots",
]
