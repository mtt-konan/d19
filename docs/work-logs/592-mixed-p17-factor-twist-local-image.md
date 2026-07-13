# wl592 Mixed p=17 Factor-Twist Local Image

## Scope and result

This checkpoint treats only the frozen `wl589` mixed cover

~~~text
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)
~~~

over `Q_17`.  It computes the exact normalized relative constant factor-twist
image, with no rank, Selmer, rational-point, family, or D2 claim.

The local squareclass basis is

~~~text
Q_17^*/Q_17^{*2} = {[1], [u], [17], [17u]},
~~~

where `u` is any nonsquare unit modulo `17`.  The exact image is

~~~text
I_{17,m} = {[u]}.
~~~

The sole mixed twist from `wl591` is

~~~text
91205 = 17*5365, 5365 = 10 mod 17,
~~~

and `10` is a nonsquare unit modulo `17`.  Hence

~~~text
[91205] = [17u] not in I_{17,m}.
~~~

This is an exact local exclusion of `d=91205`. Combined with `wl590` and
`wl591`, it exhausts the factor-twist candidate ledger for this frozen mixed
representative. It is not a family exclusion, Selmer/rank theorem, or D2
result.

## Frozen normalized cover

The computation keeps the `wl589` functions

~~~text
W^2=f(r)=289*r^4-408*r^3+274*r^2-120*r+25,
D=17*r^2-5,
A=17*r^2-17*r+5,
B=17*r^2-20*r+5,
t=-17*B*W/(D*A),
N=(10+t)/2, M=(10-t)/2.
~~~

The normalized factors and frozen cleared identities are

~~~text
F_plus=N^2+49, F_minus=M^2+49,
J_plus=(2*D*A)^2*F_plus,
J_minus=(2*D*A)^2*F_minus.
~~~

For `F_plus=d*a_plus^2` and `F_minus=d*a_minus^2`, the fixed-cover coordinate
is retained:

~~~text
R=d*a_plus*a_minus,
R^2=(N^2+49)*(M^2+49).
~~~

The exact AA+BB lift is also retained:

~~~text
(N^2+9)*(M^2+9)=(Z/4)^2,
-10<t<10,
source leg=3, opposite leg=7.
~~~

The inequality is the global real positivity condition; it is recorded but is
not silently replaced by a `Q_17` ordering condition.  No individual factor
square condition is added to AA+BB.

## Complete source strata at 17

Every finite `r in Q_17` has either `v_17(r)>=0` or `v_17(r)<0`.  The first
case is the integral chart.  Reducing the frozen source equation gives

~~~text
f(r) = 2*r^2-r+8 mod 17.
~~~

Its discriminant is `5`, a nonsquare modulo `17`, so there is no `W=0`
residue and every source row has `W` a unit.  The complete integral table,
with `tau=t/17 mod 17`, is

~~~text
(r,W;tau):
(0,5;1), (0,12;16),
(1,3;5), (1,14;12),
(4,6;16), (4,11;1),
(5,6;1), (5,11;16),
(8,3;12), (8,14;5),
(9,5;16), (9,12;1),
(11,1;5), (11,16;12),
(15,1;12), (15,16;5).
~~~

On this chart `D=-5 mod 17` and `A=5 mod 17`, and

~~~text
tau = -B*W/(D*A) mod 17,
t=17*tau in 17*Z_17.
~~~

Since `2W` is a unit, every listed row is a complete Hensel residue disk.

For every negative-valuation point, set

~~~text
s=1/(17*r) in Z_17,
y=17*s^2*W.
~~~

The value `s=0` is the projective infinity chart and gives its two points at
infinity.  Direct substitution into the frozen source gives

~~~text
y^2=H(s)=1-24*s+274*s^2-2040*s^3+7225*s^4.
~~~

Modulo `17`,

~~~text
H(s)=2*s^2-7*s+1,
~~~

whose discriminant is `7`, also a nonsquare modulo `17`.  Thus every infinity
row has `y` a unit and `2y` is a Hensel unit.  Put

~~~text
d_inf=1-85*s^2,
a_inf=1-17*s+85*s^2,
b_inf=1-20*s+85*s^2.
~~~

Then

~~~text
D=d_inf/(17*s^2),
A=a_inf/(17*s^2),
B=b_inf/(17*s^2),
W=y/(17*s^2),
t=-17*b_inf*y/(d_inf*a_inf).
~~~

Both `d_inf` and `a_inf` are `1 mod 17`, so `t` again lies in
`17*Z_17`.  The complete infinity table is

~~~text
(s,y;tau):
(0,1;16), (0,16;1),
(1,8;16), (1,9;1),
(3,7;5), (3,10;12),
(5,4;5), (5,13;12),
(7,4;12), (7,13;5),
(9,7;12), (9,10;5),
(11,8;1), (11,9;16),
(12,1;1), (12,16;16).
~~~

The two charts therefore cover every smooth proper `Q_17` source point,
including all negative-valuation and projective infinity disks.  In every
case,

~~~text
t in 17*Z_17,
N = M = 5 mod 17,
F_plus = F_minus = 5^2+7^2 = 6 mod 17.
~~~

The unit `6` is a nonsquare modulo `17`.  Consequently every nonzero local
factor has class `[u]`.

## D/A denominator poles

There is no finite `Q_17` denominator-pole branch.  Indeed,

~~~text
D=0 -> r^2=5/17,
~~~

whose right-hand side has odd valuation `-1`.  Also `A=0` has discriminant

~~~text
(-17)^2-4*17*5=-51,
~~~

whose `17`-adic valuation is `1`, so it is not a square.  More directly, for
`v_17(r)=-k<0`,

~~~text
v_17(D)=v_17(A)=1-2*k<0,
~~~

while for integral `r` both are units.  The normalized infinity factors
`d_inf` and `a_inf` are units as shown above.  Thus `D=0` and `A=0` introduce
no `Q_17` source point; their projective behavior is already covered by the
infinity chart.  Since the cleared identities multiply by the square
`(2*D*A)^2`, they introduce no new twist class on any existing source point.

## Factor-zero, R=0, and zero-value branches

At `17`, `-1` is a square, with residues `i=4,13`, so the factor-zero fibers
cannot be discarded by a nonsquare-`-1` argument.  Their `t` values are

~~~text
F_plus=0:  t=-10+14*i or -10-14*i,
F_minus=0: t=10+14*i or 10-14*i.
~~~

Modulo `17` these have residues `{2,5,12,15}`, all units.  They are therefore
outside the proven source image `t in 17*Z_17`.  Hence the normalized
factor-zero source branches are empty over `Q_17`, and so is `R=0`, since
`R^2=F_plus*F_minus`.

The formal zero-value branches add no `[17u]` possibility:

~~~text
t=0:  F_plus=F_minus=74=6 mod 17, class [u],
N=0:  t=-10, F_plus=49, F_minus=149=13 mod 17,
M=0:  t=10,  F_plus=149=13 mod 17, F_minus=49.
~~~

The last two are not source branches because `+/-10` is not in `17*Z_17`.

## Exact image and inclusion of [u]

The complete strata prove

~~~text
I_{17,m} subseteq {[u]}.
~~~

The reverse inclusion is supplied by the exact frozen source point

~~~text
r=0, W=5, f(0)=25,
t=17, N=27/2, M=-7/2,
F_plus=925/4, F_minus=245/4.
~~~

Take the unit twist representative `d=5`, which has class `[u]`.  Then

~~~text
F_plus/5=185/4 = 8 mod 17,
F_minus/5=49/4 = 8 mod 17.
~~~

Both are unit square residues modulo `17`, so Hensel lifts their square roots
in `Q_17`; the second ratio is visibly `(7/2)^2`.  Multiplying by the square
`(2*D*A)^2` gives the corresponding cleared `J_plus` and `J_minus` roots.
Choosing those roots and setting `R=5*a_plus*a_minus` retains the fixed-cover
equation.  Therefore

~~~text
{[u]} subseteq I_{17,m}.
~~~

Thus the exact image is `I_{17,m}={[u]}`, and `[91205]=[17u]` is excluded.

## Executable certificate

The certificate is

~~~text
scripts/theory/aa_bb/wl592_mixed_p17_factor_twist_local_image.py
~~~

with focused tests in

~~~text
tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py
~~~

The strict validation commands are:

~~~text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py
3 passed

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check scripts/theory/aa_bb/wl592_mixed_p17_factor_twist_local_image.py tests/theory/aa_bb/test_wl592_mixed_p17_factor_twist_local_image.py
All checks passed!

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/aa_bb/wl592_mixed_p17_factor_twist_local_image.py --out /private/tmp/wl592-mixed-p17.json --strict
status=ok
work_log=wl592
ready=True
local_image=['[u]']
target_twist_class=[17u]
target_twist_in_image=False
violations=[]
~~~

No frozen `wl587`, `wl589`, `wl590`, or `wl591` file is edited.  No other
prime, bounded rational search, rank computation, equivalent model, or D2
step is used.
