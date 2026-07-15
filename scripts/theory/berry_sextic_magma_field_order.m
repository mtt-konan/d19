// Stage 1: construct L, its absolute maximal order, and support ideals.
// No descent intrinsic is called here.
SetSeed(1);
print "BERRY_C1_FIELD_ORDER_V1_START";

K<i> := QuadraticField(-1);
R<t> := PolynomialRing(K);
g6 := t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4
    + (-52 - 28*i)*t^3 + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1;
L<theta> := ext<K | g6>;
La, absolute_map := AbsoluteField(L);
O := MaximalOrder(La);

print "BERRY_C1_RELATIVE_DEGREE", Degree(L);
print "BERRY_C1_ABSOLUTE_DEGREE", Degree(La);
print "BERRY_C1_ORDER_DISCRIMINANT", Discriminant(O);
print "BERRY_C1_ABSOLUTE_POLYNOMIAL", DefiningPolynomial(La);

for p in [2, 37397] do
    factors := Factorization(ideal<O | p>);
    print "BERRY_C1_RATIONAL_SUPPORT", p, #factors;
    for j in [1..#factors] do
        P := factors[j][1];
        print "BERRY_C1_ABSOLUTE_PRIME", p, j, Norm(P),
            RamificationIndex(P), InertiaDegree(P);
    end for;
end for;

print "BERRY_C1_FIELD_ORDER_V1_DONE";
