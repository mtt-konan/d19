#!/usr/bin/env sage
"""Proof-enabled Sage checks for the post-B0 Berry feasibility audit."""

proof.all(True)

K.<i> = QuadraticField(-1)
pi = K(1 + i)
T.<T> = PolynomialRing(K)
g6 = (T^6 + (-2 - 2*i)*T^5 + (-35 - 8*i)*T^4
      + (-52 - 28*i)*T^3 + (19 - 40*i)*T^2 + (6 + 14*i)*T - 1)
Z.<z> = PolynomialRing(K)
f_shift = -i*g6(z - 1)


def unit_residue(value):
    """Reduce a Gaussian unit modulo (1+i)."""
    return (ZZ(value[0]) + ZZ(value[1])) % 2


def valuation_table(poly):
    return [coefficient.valuation(pi) for coefficient in poly.list()]


# Exact dyadic obstruction on the finite chart.
assert pi^2 == 2*i
assert K(2) == -i*pi^2
assert valuation_table(f_shift) == [11, 10, 8, 9, 3, 2, 0]
assert all(
    unit_residue(coefficient / pi^valuation_table(f_shift)[j]) == 1
    for j, coefficient in enumerate(f_shift.list())
)

# z has valuation 0, 1, 2, or at least 3.  The first, second, and fourth
# cases follow from the unique lowest terms in the displayed coefficient table.
unit_mod_pi2 = [1, 1 + pi]
assert all(
    f_shift(rep).valuation(pi) == 0 and (f_shift(rep) - (1 + pi)).valuation(pi) >= 2
    for rep in unit_mod_pi2
)
assert all(
    f_shift(pi*rep).valuation(pi) == 6
    and (f_shift(pi*rep)/pi^6 - (1 + pi)).valuation(pi) >= 2
    for rep in unit_mod_pi2
)
assert f_shift(pi^2).valuation(pi) == 13
assert f_shift(pi^3).valuation(pi) == 11

# The valuation-2 branch is uniform in the unit u.  This exact polynomial is
# Q(u)=pi^(-11)*f_shift(pi^2*u), and units modulo pi^3 have four representatives.
S.<u> = PolynomialRing(K)
Q = (i + (3 + i)*u + (1 + i)*u^2 + (8 + 4*i)*u^3
     + (2 - 3*i)*u^4 + (3 + 5*i)*u^5 + (1 - i)*u^6)
assert Q == S([K(coefficient)*pi^(2*j - 11) for j, coefficient in enumerate(f_shift.list())])
unit_representatives = [1, 1 + pi, 1 + pi^2, 1 + pi + pi^2]
assert all(
    Q(rep).valuation(pi) == 2 and unit_residue(Q(rep) / pi^2) == 1
    for rep in unit_representatives
)

# Reciprocal chart, including infinity x=0.  For x in pi*O, all nonconstant
# terms vanish modulo pi^2 and the constant is -i, a nonsquare unit.
X.<x> = PolynomialRing(K)
g_star = (1 + (-2 - 2*i)*x + (-35 - 8*i)*x^2 + (-52 - 28*i)*x^3
          + (19 - 40*i)*x^4 + (6 + 14*i)*x^5 - x^6)
f_star = -i*g_star
assert f_star(0) == -i
assert (f_star(0) - (1 + pi)).valuation(pi) >= 2
assert (f_star(pi) - (-i)).valuation(pi) >= 2


def finite_i(p):
    if p % 4 == 1:
        F = GF(p, 'ii')
        return F, next(root for root in F if root^2 + 1 == 0)
    P = PolynomialRing(GF(p), 'X')
    Xp = P.gen()
    F = FiniteField(p^2, 'ii', modulus=Xp^2 + 1)
    return F, F.gen()


def reduction_row(p, twist):
    F, ii = finite_i(p)
    R = PolynomialRing(F, 'x')
    x = R.gen()
    g = (x^6 + (-2 - 2*ii)*x^5 + (-35 - 8*ii)*x^4
         + (-52 - 28*ii)*x^3 + (19 - 40*ii)*x^2 + (6 + 14*ii)*x - 1)
    f = g if twist == '1' else -ii*g
    C = HyperellipticCurve(f)
    counts = C.count_points(2)
    J = C.jacobian().cardinality()
    q = F.cardinality()
    a1 = q + 1 - counts[0]
    a2 = (counts[1] - q^2 - 1 + a1^2) // 2
    assert J == q^2 + 1 + a2 - (q + 1)*a1
    return q, counts[0], counts[1], J


# The discriminant support is exact, so all rows below are certified good.
assert g6.discriminant() == (i - 1)^75*(94*i - 169)
primes = [3, 5, 7, 13, 17, 29, 37]
assert all(p not in [2, 37397] for p in primes)
expected = {
    '1': {
        3: (9, 8, 106, 76), 5: (5, 7, 39, 39), 7: (49, 58, 2448, 2857),
        13: (13, 10, 188, 131), 17: (17, 16, 342, 282),
        29: (29, 35, 895, 1031), 37: (37, 56, 1344, 2203),
    },
    'i': {
        3: (9, 8, 106, 76), 5: (5, 5, 39, 27), 7: (49, 58, 2448, 2857),
        13: (13, 18, 188, 243), 17: (17, 16, 342, 282),
        29: (29, 25, 895, 731), 37: (37, 20, 1344, 835),
    },
}
rows = {twist: {p: reduction_row(p, twist) for p in primes} for twist in ['1', 'i']}
assert rows == expected


def primary_safe_bound(twist):
    candidate_primes = set()
    for p in primes:
        candidate_primes.update(ZZ(rows[twist][p][3]).prime_factors())
    bound = ZZ(1)
    for ell in candidate_primes:
        exponents = [ZZ(rows[twist][p][3]).valuation(ell) for p in primes if p != ell]
        bound *= ell^min(exponents)
    return bound


assert all(gcd([rows[twist][p][3] for p in primes]) == 1 for twist in ['1', 'i'])
assert primary_safe_bound('1') == 1
assert primary_safe_bound('i') == 1

# This is an exact number-field S-squareclass computation, not a Jacobian
# Selmer computation. It records the live API and proof flag used in the audit.
P2 = K.ideal(1 + i)
Pp = K.ideal(94*i - 169)
S_generators, S_orders = K.selmer_generators([P2, Pp], 2, proof=True, orders=True)
assert [str(value) for value in S_generators] == ['i - 1', '94*i - 169', 'i']
assert S_orders == [2, 2, 2]

print('status=ok')
print('proof_all=True')
print('C_i_local_at_(1+i)=obstructed')
print('torsion_bound_C1=1')
print('torsion_bound_Ci=1')
print('S_squareclass_generators=[i-1,94*i-169,i]')
print('jacobian_2_selmer_computation=not_available_in_installed_Sage')
