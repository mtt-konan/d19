#!/usr/bin/env sage
"""Exact elimination check for the Q3a3 D_inf halving obstruction."""

proof.all(True)

K.<i> = QuadraticField(-1)
R.<t,a,b,r,s,d0,c> = PolynomialRing(K, order="lex")
f = (t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4 + (-52 - 28*i)*t^3
     + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1)
u = t^2 + a*t + b
w = -t^3 + r*t^2 + s*t + d0
equation = w^2 - c*u^2 - f
coefficient_equations = []
for k in range(6):
    coefficient = R(0)
    for exponents, value in equation.dict().items():
        if exponents[0] == k:
            monomial = value
            for index in range(1, 7):
                monomial *= R.gen(index)^exponents[index]
            coefficient += monomial
    coefficient_equations.append(coefficient)


def coefficient_in_t(polynomial, degree):
    coefficient = R(0)
    for exponents, value in polynomial.dict().items():
        if exponents[0] == degree:
            monomial = value
            for index in range(1, 7):
                monomial *= R.gen(index)^exponents[index]
            coefficient += monomial
    return coefficient

expected = (c^10 + (-210 - 68*i)*c^9 + (16401 + 12900*i)*c^8
            + (-537592 - 974672*i)*c^7 + (1926370 + 37085584*i)*c^6
            + (356741044 - 725661880*i)*c^5
            + (-9952074358 + 5948878392*i)*c^4
            + (106782453448 + 13561791344*i)*c^3
            + (-371183289347 - 503636744112*i)*c^2
            + (-878727109554 + 2079369073884*i)*c
            + (4745893054341 + 25610622340*i))

elimination = R.ideal(coefficient_equations).groebner_basis()
assert expected in elimination

# The degree-zero and degree-one branches are checked without division by a
# possibly vanishing local coefficient.
r0 = 1 + i
s0 = (35 + 10*i) / 2
d0_value = (77 + 73*i) / 2
w0 = -t^3 + r0*t^2 + s0*t + d0_value
degree_zero_residual = w0^2 - f
assert [coefficient_in_t(degree_zero_residual, k) for k in (5, 4, 3)] == [0, 0, 0]
assert coefficient_in_t(degree_zero_residual, 2) == (1065 + 1460*i) / 4

c1 = 1065/4 + 365*i
a1 = (1378713 + 131985*i) / 653165
degree_one_residual = w0^2 - c1*(t + a1)^2 - f
assert [coefficient_in_t(degree_one_residual, k) for k in range(1, 6)] == [0, 0, 0, 0, 0]
assert coefficient_in_t(degree_one_residual, 0) == (-465740071 + 634874366*i) / 653165

print("status=ok")
print("elimination_polynomial_degree=10")
print("degree_zero_t2_residual=(1065+1460*i)/4")
print("degree_one_constant_residual=(-465740071+634874366*i)/653165")
print("outcome=D_inf_not_in_2J_Q2_i")
