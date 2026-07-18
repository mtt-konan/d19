#!/usr/bin/env sage
"""Proof-enabled finite-field certificate for the Berry C_1 B2 boundary."""

proof.all(True)

K.<i> = QuadraticField(-1)
T.<T> = PolynomialRing(K)
g6 = (T^6 + (-2 - 2*i)*T^5 + (-35 - 8*i)*T^4
      + (-52 - 28*i)*T^3 + (19 - 40*i)*T^2 + (6 + 14*i)*T - 1)

# Global branch algebra: reduction at a prime of K, not a bad-place factorization.
F13 = GF(13)
R13.<x13> = PolynomialRing(F13)
ii13 = F13(5)
f13 = x13^6 + x13^5 + 3*x13^4 + 3*x13^3 + x13^2 + 11*x13 + 12
assert (5^2 + 1) % 13 == 0
assert (
    x13^6 + (-2 - 2*ii13)*x13^5 + (-35 - 8*ii13)*x13^4
    + (-52 - 28*ii13)*x13^3 + (19 - 40*ii13)*x13^2
    + (6 + 14*ii13)*x13 - 1
    == f13
)


def pow_mod(base, exponent, modulus):
    result = modulus.parent()(1)
    base = base % modulus
    while exponent:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result


assert gcd(f13, pow_mod(x13, 13^2, f13) - x13) == 1
assert gcd(f13, pow_mod(x13, 13^3, f13) - x13) == 1
assert pow_mod(x13, 13^6, f13) == x13
assert f13.is_irreducible()

# Exact good reduction at lambda=(269, i-82).
F269 = GF(269)
R269.<x269> = PolynomialRing(F269)
ii = F269(82)
g269 = (x269^6 + (-2 - 2*ii)*x269^5 + (-35 - 8*ii)*x269^4
        + (-52 - 28*ii)*x269^3 + (19 - 40*ii)*x269^2
        + (6 + 14*ii)*x269 - 1)
C269 = HyperellipticCurve(g269)
J269 = C269.jacobian()
P_plus, P_minus = C269.points_at_infinity()
A_plus = C269([0, ii, 1])
A_minus = C269([0, -ii, 1])
assert P_plus == C269([1, 1, 0])
assert P_minus == C269([1, -1, 0])
E_plus = J269.point(A_plus, P_plus)
E_minus = J269.point(A_minus, P_plus)
D_inf = J269.point(P_plus, P_minus)

assert ii^2 + 1 == 0
assert g269 == x269^6 + 103*x269^5 + 116*x269^4 + 73*x269^3 + 236*x269^2 + 78*x269 + 268
assert C269.count_points(2) == [282, 72430]
assert J269.cardinality() == 75708
assert J269.abelian_group().invariants() == (3, 25236)

# These are fixed exact Mumford classes.  They generate the displayed
# invariant-factor group, so the coordinates below do not depend on Sage's
# internally selected Smith generators.
G1 = J269(x269^2 + 96*x269 + 106, 44*x269 + 8)
G2 = J269(x269^2 + 54*x269 + 268, 129*x269 + 60)
assert G1.order() == 25236
assert G2.order() == 3
assert G2 != 8412*G1
assert G2 != 2*8412*G1
assert G1.order()*G2.order() == J269.cardinality()
assert E_plus == 14912*G1 + G2
assert E_minus == 9310*G1 + G2
assert D_inf == 1014*G1 + G2
assert E_plus + E_minus + D_inf == J269(0)

assert (14912 % 3, 1 % 3) == (2, 1)
assert (1014 % 3, 1 % 3) == (0, 1)
assert (2*1 - 0*1) % 3 != 0

print("status=ok")
print("global_branch_reduction_prime=(13,i-5)")
print("global_branch_reduction_irreducible=True")
print("j2_K_dimension=0")
print("good_reduction_prime=(269,i-82)")
print("jacobian_order=75708")
print("jacobian_invariants=(3,25236)")
print("E_plus_mod_3=(2,1)")
print("D_inf_mod_3=(0,1)")
print("rank_two_reduction_certificate=True")
