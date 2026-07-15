// Q3a2: exact dyadic factor-field embedding test for the selected Berry sextic.
// The containment test is the exact root criterion for the quadratic factor:
// E2 embeds in E4 iff f2 becomes reducible over E4.
SetSeed(1);
print "BERRY_Q3A2_EMBEDDING_V1_START";

K<i> := QuadraticField(-1);
R<t> := PolynomialRing(K);
g6 := t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4
    + (-52 - 28*i)*t^3 + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1;
OK := RingOfIntegers(K);
P := ideal<OK | 1+i>;
Kv, completion_map := Completion(K, P);
Rp<x> := PolynomialRing(Kv);
g6v := Rp![completion_map(c) : c in Eltseq(g6)];

factor_data := Factorization(g6v);
assert &and[entry[2] eq 1 : entry in factor_data];
assert &*[entry[1]^entry[2] : entry in factor_data] eq g6v;

f2_data := [entry[1] : entry in factor_data | Degree(entry[1]) eq 2];
f4_data := [entry[1] : entry in factor_data | Degree(entry[1]) eq 4];
assert #f2_data eq 1;
assert #f4_data eq 1;
f2 := f2_data[1];
f4 := f4_data[1];
assert IsIrreducible(f2);
assert IsIrreducible(f4);

E2<theta2> := ext<Kv | f2>;
E4<theta4> := ext<Kv | f4>;
assert Degree(E2) eq 2;
assert Degree(E4) eq 4;

RE4<y> := PolynomialRing(E4);
f2_over_E4 := RE4![E4!c : c in Eltseq(f2)];
root_data := Roots(f2_over_E4);
embedding_bit := #root_data eq 2;
assert embedding_bit eq (not IsIrreducible(f2_over_E4));

print "BERRY_Q3A2_FACTOR_DEGREES", [Degree(entry[1]) : entry in factor_data];
print "BERRY_Q3A2_E2_RELATIVE_DEGREE", Degree(E2);
print "BERRY_Q3A2_E4_RELATIVE_DEGREE", Degree(E4);
print "BERRY_Q3A2_F2_ROOT_COUNT_IN_E4", #root_data;
print "BERRY_Q3A2_E2_EMBEDS_IN_E4", embedding_bit;
print "BERRY_Q3A2_CONTAINMENT_INTRINSIC", "Roots and IsIrreducible over E4";
print "BERRY_Q3A2_EMBEDDING_V1_DONE";
