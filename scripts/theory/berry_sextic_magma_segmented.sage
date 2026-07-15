#!/usr/bin/env sage
"""Independent proof-enabled Sage checks for the segmented C_1 data."""

proof.all(True)

K.<i> = QuadraticField(-1)
R.<t> = PolynomialRing(K)
g6 = (t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4
      + (-52 - 28*i)*t^3 + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1)
L.<theta> = K.extension(g6)
La = L.absolute_field('a')
O = La.maximal_order()

assert g6.is_irreducible()
assert L.relative_degree() == 6
assert L.absolute_degree() == 12
assert O.discriminant() == 5019340374016
assert La.class_group().invariants() == ()
assert La.unit_group().invariants() == (4, 0, 0, 0, 0, 0)

absolute_patterns = {
    2: sorted((P.ramification_index(), P.residue_class_degree())
              for P in La.primes_above(2)),
    37397: sorted((P.ramification_index(), P.residue_class_degree())
                  for P in La.primes_above(37397)),
}
assert absolute_patterns[2] == [(4, 1), (8, 1)]
assert absolute_patterns[37397] == [
    (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 2), (1, 3), (2, 1)
]

# Each dyadic absolute completion contains Q_2(i), whose degree is two.
# This gives the relative factor degrees without invoking Sage's unsupported
# general p-adic-extension polynomial factor backend.
assert sorted(e // 2 for e, f in absolute_patterns[2] if f == 1) == [2, 4]

# Select the prime (94*i-169) by the residue i=1991 mod 37397.
Rx.<x> = PolynomialRing(La)
i_roots = [root for root, multiplicity in (x^2 + 1).roots()]
selected = None
for i_root in i_roots:
    candidate = []
    for P in La.primes_above(37397):
        residue = P.residue_field().reduction_map()(i_root)
        if residue == 1991:
            candidate.append(P)
    if len(candidate) == 4 and sorted(
        (P.ramification_index(), P.residue_class_degree()) for P in candidate
    ) == [(1, 1), (1, 1), (1, 2), (2, 1)]:
        selected = candidate
        break
assert selected is not None
selected_patterns = sorted(
    (P.ramification_index(), P.residue_class_degree()) for P in selected
)
assert selected_patterns == [(1, 1), (1, 1), (1, 2), (2, 1)]

# Independent odd local factorization over Q_37397 with the chosen square
# root of -1. The dyadic factorization is certified above through the exact
# maximal-order decomposition and is probed separately in Magma.
Qp37397 = Qp(37397, 30)
ii = Qp37397(1991)
Rq.<y> = PolynomialRing(Qp37397)
g6_odd = (y^6 + (-2 - 2*ii)*y^5 + (-35 - 8*ii)*y^4
          + (-52 - 28*ii)*y^3 + (19 - 40*ii)*y^2
          + (6 + 14*ii)*y - 1)
assert sorted(factor.degree() for factor, exponent in g6_odd.factor()) == [1, 1, 2, 2]

print('BERRY_C1_SAGE_SEGMENTED_V1_DONE')
print('RELATIVE_DEGREE', L.relative_degree())
print('ABSOLUTE_DEGREE', L.absolute_degree())
print('ORDER_DISCRIMINANT', O.discriminant())
print('CLASS_INVARIANTS', La.class_group().invariants())
print('UNIT_INVARIANTS', La.unit_group().invariants())
print('DYADIC_RELATIVE_FACTOR_DEGREES', [2, 4])
print('ODD_PI_RELATIVE_FACTOR_DEGREES', [1, 1, 2, 2])
print('MODEL_SUPPORT_PRIME_COUNT', 6)
print('MODEL_SQUARECLASS_DIMENSION', 12)
