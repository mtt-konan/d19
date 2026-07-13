# wl591 Mixed p=7 Factor-Twist Local Image

## Scope and result

This checkpoint treats only the frozen `wl589` mixed cover

~~~text
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)
~~~

at `p=7`.  The source curve, normalized factor functions, fixed-cover
coordinate, and AA+BB lift are read-only inputs.  The exact local squareclass
basis is

~~~text
Q_7^*/Q_7^{*2} = {[1], [u], [7], [7u]},
~~~

where `u` is any nonsquare unit modulo `7`.  The exact normalized image is

~~~text
I_{7,m} = {[1]}.
~~~

Consequently the four `wl590` mixed survivors map as follows:

~~~text
5      -> [u]  -> delete
3045   -> [7]  -> delete
66045  -> [7u] -> delete
91205  -> [1]  -> survive
~~~

This is an exact deletion of three named representatives.  It is not a rank,
Selmer, rational-point, family-exclusion, or D2 statement.

## Frozen normalized cover

Keep the `wl589` source and abbreviations

~~~text
W^2=f(r)=289*r^4-408*r^3+274*r^2-120*r+25,
D=17*r^2-5,
A=17*r^2-17*r+5,
B=17*r^2-20*r+5,
t=-17*B*W/(D*A),
N=(10+t)/2, M=(10-t)/2.
~~~

The factors are

~~~text
F_plus=N^2+49=(t^2+20*t+296)/4,
F_minus=M^2+49=(t^2-20*t+296)/4.
~~~

The frozen cleared identities are

~~~text
J_plus=(2*D*A)^2*F_plus,
J_minus=(2*D*A)^2*F_minus.
~~~

For `F_plus=d*a_plus^2` and `F_minus=d*a_minus^2`, retain the fixed-cover
coordinate

~~~text
R=d*a_plus*a_minus,
R^2=(N^2+49)*(M^2+49).
~~~

The exact AA+BB lift remains the `wl589` lift

~~~text
(N^2+9)*(M^2+9)=(Z/4)^2,
-10<t<10,
source leg=3, opposite leg=7,
~~~

with no individual square condition added to AA+BB.  The first identity is
verified in the frozen source function field; the real inequality is retained
as the global positivity condition and is not replaced by a `Q_7` condition.

## Complete source strata

Modulo `7`,

~~~text
f(r)=2*(r^2-3*r+1)*(r^2+2*r+2).
~~~

This reduction is squarefree.  The complete affine source table is

~~~text
(r,W) mod 7:
(0,2), (0,5), (1,2), (1,5),
(2,1), (2,6), (4,1), (4,6),
(5,3), (5,4).
~~~

Every row has `W` a unit, so `2W` is a Hensel unit.  The rows with `D` a
unit, together with the reduction of `t`, are

~~~text
(r,W,t) mod 7:
(0,2,4), (0,5,3),
(1,2,4), (1,5,3),
(4,1,3), (4,6,4).
~~~

The remaining affine rows are exactly the denominator rows

~~~text
(r,W) mod 7:
(2,1), (2,6), (5,3), (5,4),
~~~

because `D` has simple roots `2,5` modulo `7`.  The other denominator factor
has discriminant `-51=5 mod 7`, a nonsquare, so `A=0` has no `Q_7` branch.
The source rows above `D=0` are genuine `Q_7` disks: `D'` is a unit and
`f(r)` is a square unit on both disks.

The two projective infinity disks use `z=1/r`, `v=W/r^2`:

~~~text
v^2=289-408*z+274*z^2-120*z^3+25*z^4.
~~~

At `z=0`, `v=+/-17` reduces to `3,4`, and `2v` is a unit.  The two infinity
rows are

~~~text
v mod 7   t mod 7
3         4
4         3
~~~

Thus the affine table and the two infinity disks cover every `Q_7` point of
the smooth proper source.  The `r=0` boundary-visible rows are already in the
affine table; there is no `W=0` source row modulo `7`.

## Exclusion of the three nontrivial classes

For `t=3 mod 7`,

~~~text
N=3 mod 7, M=0 mod 7,
F_plus=2 mod 7,
~~~

so `F_plus` is a unit square in `Q_7`.  For `t=4 mod 7`,

~~~text
N=0 mod 7, M=3 mod 7,
F_minus=2 mod 7,
~~~

so `F_minus` is a unit square in `Q_7`.  Here `2` is a square modulo `7`.
If a nonzero factor satisfies `F=d*s^2`, its squareclass equals `[d]`.
Therefore every non-pole local factor-cover point above a regular source row
has

~~~text
[d]=[1].
~~~

At a `D` pole, the normalized factors have the Laurent form

~~~text
F_plus=(t^2/4)*(1+20/t+296/t^2),
F_minus=(t^2/4)*(1-20/t+296/t^2).
~~~

Since `v_7(t)<0`, both parenthesized terms are principal units.  They are
Hensel squares, and `t^2/4` is a square.  Equivalently, at `D=0` the cleared
values are

~~~text
J_plus=J_minus=289*B^2*f,
~~~

whose residues on the four pole rows are `1,1,4,4`.  Hence the normalized
pole branch also has class `[1]`; clearing `D*A` introduces no extra twist
class.  The fixed-cover coordinate has the corresponding even pole order.

The zero-value branches add no class:

~~~text
t=0: F_plus=F_minus=74=4 mod 7,
N=0: F_plus=49,
M=0: F_minus=49.
~~~

The normalized factor-zero branches are empty over `Q_7`.  Indeed

~~~text
F_plus=0 -> N^2=-49 -> (N/7)^2=-1,
F_minus=0 -> M^2=-49 -> (M/7)^2=-1,
~~~

and `-1` is a nonsquare modulo `7`.  Thus `R=0`, which is contained in the
two factor-zero divisors, has no `Q_7` point.  This also closes the factor-zero
branches separately from the denominator-pole branches.

These strata prove the exclusion

~~~text
I_{7,m} subseteq {[1]}.
~~~

## Hensel inclusion of `[1]`

Take the source residue disk `r=1`, `W=2 mod 7`.  Since `f(1)=60` and

~~~text
16^2=60 mod 49,
2*16 is a 7-adic unit,
~~~

Hensel gives a `Q_7` source point with `W=16 mod 49`.  The denominator
`D(1)A(1)=60` is a unit, and direct substitution gives

~~~text
t=4 mod 49,
N=7 mod 49,
M=3 mod 49.
~~~

Consequently

~~~text
F_plus/49=2 mod 7,
F_minus=2 mod 7.
~~~

Both are unit squares by Hensel, and `49` is itself a square.  Choose their
two `Q_7` square roots as `a_plus,a_minus`, set `d=1`, and define

~~~text
R=a_plus*a_minus.
~~~

This is a point of the normalized factor cover and of the retained fixed-cover
equation.  Hence

~~~text
{[1]} subseteq I_{7,m}.
~~~

Together with the exclusion, this proves `I_{7,m}={[1]}`.

## Named mapping and verification

The four `wl590` survivors have the exact `Q_7` classes

~~~text
v_7(5)=0,      5 mod 7=5  nonsquare -> [u],
v_7(3045)=1,  3045/7=435=1 mod 7 -> [7],
v_7(66045)=1, 66045/7=9435=6 mod 7 -> [7u],
v_7(91205)=0, 91205=2 mod 7       -> [1].
~~~

The executable certificate is

~~~text
scripts/theory/aa_bb/wl591_mixed_p7_factor_twist_local_image.py
~~~

with focused tests in

~~~text
tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py
~~~

The strict checks pass:

~~~text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py
3 passed

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/aa_bb/wl591_mixed_p7_factor_twist_local_image.py \
  tests/theory/aa_bb/test_wl591_mixed_p7_factor_twist_local_image.py
All checks passed!

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/aa_bb/wl591_mixed_p7_factor_twist_local_image.py \
  --out /private/tmp/wl591-mixed-p7.json --strict
status=ok
work_log=wl591
ready=True
violations=[]
~~~

The residue enumeration is only the complete `F_7` stratum certificate.  The
local conclusions use unit square criteria and Hensel arguments; no bounded
rational-point search, rank computation, other prime, pure-family calculation,
`wl535` re-entry, or D2 step is used.
