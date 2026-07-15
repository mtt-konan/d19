# Q1 Fake 2-Descent Certificate

## Accepted Scope

For the selected curve

```text
C_1: v^2=g6(t),  K=Q(i),  deg(g6)=6,
```

the Q1 object is the fake divisor-evaluation target

```text
L^*/L^{*2}K^*,  L=K[theta]/(g6(theta)),
```

with norm condition `N_{L/K}(alpha) in K^{*2}`.  The conservative support
above `2` and `37397` gives the fixed squareclass coordinate order

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10,
```

and dimension `16` over `F_2` after the torsion relation is handled.

## Even-Degree Infinity Kernel

The smooth even-degree projective model has two `K`-rational points at
infinity, `P_+` and `P_-`.  For a root coordinate `theta`, the divisor of the
standard evaluation function has the form

```text
div(t-theta)=2D_theta-P_+-P_-.
```

Consequently the fake divisor evaluation does not distinguish the two infinity
signs.  Its even-degree kernel contains the class

```text
D_inf=[P_+-P_-] in J(K)/2J(K).
```

This is a kernel statement for the fake map, not a claim that `D_inf` is zero.

## Kummer Image

The leading coefficient of `g6` is `1`.  The infinity-difference Kummer class
therefore has trivial squareclass in the fake target:

```text
delta_fake(D_inf)=[1]=0,
coordinate_vector(D_inf)=(0,...,0) in F_2^16.
```

The exact certificate and round-trip test are in
`scripts/theory/berry_sextic_q1.py` and `tests/test_berry_sextic_q1.py`.

## Boundary

This Q1 certificate does not compute either local Kummer image, a fake or true
Selmer group, a rank bound, saturation, rational `t`-values, or Berry-point
reconstruction.  Q2 must independently prove the odd-prime image, and Q3 the
dyadic image, before any global Selmer conclusion.
