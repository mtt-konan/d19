// Stage 3: local factorization and strict Kummer-quotient targets.
// The target lines are theorem inputs, not computed local images.
SetSeed(1);
print "BERRY_C1_LOCAL_V1_START";

K<i> := QuadraticField(-1);
R<t> := PolynomialRing(K);
g6 := t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4
    + (-52 - 28*i)*t^3 + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1;
OK := RingOfIntegers(K);

for data in [
    <"dyadic", ideal<OK | 1+i>, 2>,
    <"odd_pi", ideal<OK | 94*i-169>, 37397>
] do
    label := data[1]; P := data[2]; residue_characteristic := data[3];
    Kv, completion_map := Completion(K, P);
    Rp<x> := PolynomialRing(Kv);
    local_g6 := ChangeRing(g6, Kv);
    print "BERRY_C1_LOCAL_PLACE", label, residue_characteristic;
    print "BERRY_C1_LOCAL_FACTORIZATION", label, Factorization(local_g6);
end for;

print "BERRY_C1_LOCAL_THEORETICAL_TARGET", "dyadic", 5;
print "BERRY_C1_LOCAL_THEORETICAL_TARGET", "odd_pi", 2;
print "BERRY_C1_LOCAL_TARGET_FORMULA", "dyadic", "[K_varpi:Q_2]*2+dim_F2(J[2](K_varpi))";
print "BERRY_C1_LOCAL_TARGET_FORMULA", "odd_pi", "dim_F2(J[2](K_pi))";
print "BERRY_C1_LOCAL_V1_DONE";
