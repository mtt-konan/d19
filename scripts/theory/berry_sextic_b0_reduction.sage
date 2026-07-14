"""Exact fixed-center radial audit at pi=1+i.

This is proof-data for the fixed center z=t+1 only.  It deliberately does not
claim a complete stable-model obstruction: the right PGL2(O) factor in a
Cartan decomposition acts on the original branch sextic, and the remaining
Bruhat-Tits-tree directions and centers are not audited here.
"""

K.<ii> = QuadraticField(-1)
R.<z> = PolynomialRing(K)
S.<x> = PolynomialRing(K)
pi = K(1 + ii)
residue = K.residue_field(pi)
reduce_pi = residue.reduction_map()

g = (z^6 + (-2 - 2*ii)*z^5 + (-35 - 8*ii)*z^4
     + (-52 - 28*ii)*z^3 + (19 - 40*ii)*z^2
     + (6 + 14*ii)*z - 1)
H = R(g(z=-1 + z))
hvals = [coefficient.valuation(pi) for coefficient in H.list()]

assert pi^2 == 2*ii
assert K(2) == -ii*pi^2
assert pi^4 == -4
assert H == (z^6 + (-2*ii - 8)*z^5 + (2*ii - 10)*z^4
             + (-16*ii + 48)*z^3 + 16*ii*z^2
             + (32*ii - 64)*z + 32 - 32*ii)
assert hvals == [11, 10, 8, 9, 3, 2, 0]
assert H[5]/pi^2 == 4*ii - 1
assert H[0]/pi^11 == -1
assert reduce_pi(H[5]/pi^2) == residue(1)
assert reduce_pi(H[0]/pi^11) == residue(1)


# The fixed-center radial coordinate scale is F_r=pi^(-6*r)*H(pi^r*x).
def normalized_sextic(r):
    return S([pi^(-6*r + r*j)*H[j] for j in range(7)])


for r in [1, 0, -1, -2, -3]:
    F = normalized_sextic(r)
    assert F[6] == 1
    assert F[5].valuation(pi) == 2 - r
    assert F[4].valuation(pi) == 3 - 2*r

F_minus_two = normalized_sextic(-2)
assert F_minus_two[5]/pi^4 == 4*ii - 1
assert all((F_minus_two - x^6)[j].valuation(pi) >= 4 for j in range(6))

# Fixed-center result: for r=1,0,-1, the X^5/X^4 valuations rule out p^2
# modulo pi^4.
assert normalized_sextic(1)[5].valuation(pi) == 1
assert normalized_sextic(0)[5].valuation(pi) == 2
assert normalized_sextic(-1)[5].valuation(pi) == 3
assert normalized_sextic(-1)[4].valuation(pi) == 5


# Fixed-center result: for r<=-2, p=X^3+pi^2*s is the only possible square
# lift modulo pi^4. Its reduced Q is X^3. The following exact F_2 residue
# check verifies the singular derivative at X=0 for every cubic residue s.
k = GF(2)
R2.<X> = PolynomialRing(k)
residue_cubics = [
    a0 + a1*X + a2*X^2 + a3*X^3
    for a0 in [0, 1]
    for a1 in [0, 1]
    for a2 in [0, 1]
    for a3 in [0, 1]
]


def lift_residue(s):
    return S([K(ZZ(s[j])) for j in range(4)])


def reduce_polynomial(poly):
    return R2([reduce_pi(coefficient) for coefficient in poly.list()])


for r in [0, -1, -2, -3]:
    F = normalized_sextic(r)
    for s in residue_cubics:
        s_lift = lift_residue(s)
        p1 = x^3 + pi*s_lift
        q1 = (F - p1^2)/pi^2
        assert all(coefficient.valuation(pi) >= 0 for coefficient in q1.list())
        expected_q1 = (X^5 if r == 0 else 0) + s^2
        assert reduce_polynomial(q1) == expected_q1
        if r <= -2:
            p2 = x^3 + pi^2*s_lift
            q2 = (F - p2^2)/pi^4
            assert all(coefficient.valuation(pi) >= 0 for coefficient in q2.list())
            expected_q2 = (X^5 if r == -2 else 0) + X^3*s + s^2
            assert reduce_polynomial(q2) == expected_q2

assert all((X^5 + X^3*s + s^2).derivative()(0) == 0 for s in residue_cubics)
assert all((X^3*s + s^2).derivative()(0) == 0 for s in residue_cubics)
assert all((s^2).is_square() for s in residue_cubics)

# These are fixed-center residue forms only. They do not classify other
# quotient-lattice centers or directions.
assert all((X^5 + s^2).derivative()(0) == 0 for s in residue_cubics)

# For the i-twist, -i is not a square even modulo pi^2.
assert (-ii - 1) == -pi
assert (-ii - 1).valuation(pi) == 1

# For r>=2, the raw binary sextic H(pi^r*x) has odd content 11.  The
# inequalities below prove this for r=2 and for every r>=3.
raw_r2_vals = [hvals[j] + 2*j for j in range(7)]
assert min(raw_r2_vals) == 11
assert all(hvals[j] + 3*j > 11 for j in range(1, 7))
assert hvals[0] == 11

# The unit twist does not change any valuation or content in the argument.
assert all((-ii*H[j]).valuation(pi) == H[j].valuation(pi) for j in range(7))

print("status=ok")
print("fixed_center_radial_audit=True")
print("actual_varpi_reduction=unresolved")
print("full_bruhat_tits_tree_audit=missing")
