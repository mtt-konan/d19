// Stage 2: exact class/unit/S-unit data for the maximal order.
// The support uses every prime over 2 and 37397; this is the conservative
// support and contains the selected model support.
SetSeed(1);
print "BERRY_C1_SUNITS_V1_START";

Q<x> := PolynomialRing(Rationals());
f12 := x^12 - 4*x^11 - 62*x^10 + 68*x^9 + 1647*x^8
    + 4184*x^7 + 2716*x^6 - 376*x^5 + 623*x^4
    - 788*x^3 + 194*x^2 - 12*x + 1;
La<a> := NumberField(f12);
O := MaximalOrder(La);

Cl, class_map := ClassGroup(La);
print "BERRY_C1_CLASS_INVARIANTS", Invariants(Cl);

U, unit_map := UnitGroup(La);
print "BERRY_C1_UNIT_INVARIANTS", Invariants(U);
unit_generators := OrderedGenerators(U);
unit_basis := [unit_map(unit_generators[j]) : j in [1..Ngens(U)]];
for j in [1..#unit_basis] do
    // Use the fixed absolute-field power basis. S-units need not be integral,
    // so coercion to O would make this stage fail on negative valuations.
    print "BERRY_C1_UNIT_BASIS", j, Eltseq(La!unit_basis[j]);
end for;

support := [];
for p in [2, 37397] do
    factors := Factorization(ideal<O | p>);
    for j in [1..#factors] do
        Append(~support, factors[j][1]);
    end for;
end for;

SU, sunit_map := SUnitGroup(support);
print "BERRY_C1_SUNIT_INVARIANTS", Invariants(SU);
print "BERRY_C1_SUNIT_GENERATOR_COUNT", Ngens(SU);
sunit_generators := OrderedGenerators(SU);
for j in [1..#sunit_generators] do
    print "BERRY_C1_SUNIT_BASIS", j,
        Eltseq(La!sunit_map(sunit_generators[j]));
end for;
print "BERRY_C1_SUNIT_RELATION_SEQUENCE", [4];
print "BERRY_C1_SUNITS_V1_DONE";
