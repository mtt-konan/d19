// Stage 4 prototype: reconstruct the absolute field from stable scalar data.
// It does not yet rebuild support ideals or generators emitted by Stage 2.
SetSeed(1);
print "BERRY_C1_REBUILD_V1_START";

serialized_version := "berry-c1-magma-segmented-v1";
serialized_absolute_polynomial :=
    "x^12 - 4*x^11 - 62*x^10 + 68*x^9 + 1647*x^8 + 4184*x^7 "
    * "+ 2716*x^6 - 376*x^5 + 623*x^4 - 788*x^3 + 194*x^2 - 12*x + 1";
serialized_support := [
    <1, "1+i", 2, 2, 1>, <2, "1+i", 2, 4, 1>,
    <3, "94*i-169", 37397, 1, 1>,
    <4, "94*i-169", 37397, 1, 1>,
    <5, "94*i-169", 37397, 2, 1>,
    <6, "94*i-169", 37397^2, 1, 2>
];
serialized_unit_relation := [4];
serialized_sunit_relation := [4];

assert serialized_version eq "berry-c1-magma-segmented-v1";
assert #serialized_support eq 6;
assert &and[serialized_support[j][1] eq j : j in [1..#serialized_support]];
assert &and[serialized_support[j][4] * serialized_support[j][5]
    in {1, 2, 4} : j in [1..#serialized_support]];
assert serialized_unit_relation eq [4];
assert serialized_sunit_relation eq [4];

Q<x> := PolynomialRing(Rationals());
// Magma source is deliberately reconstructed from the stable polynomial
// below; no serialized map or transient object handle is consumed.
f12 := x^12 - 4*x^11 - 62*x^10 + 68*x^9 + 1647*x^8
    + 4184*x^7 + 2716*x^6 - 376*x^5 + 623*x^4
    - 788*x^3 + 194*x^2 - 12*x + 1;
La<a> := NumberField(f12);
O := MaximalOrder(La);
assert Degree(La) eq 12;
assert Discriminant(O) eq 5019340374016;

print "BERRY_C1_REBUILD_FIELD", serialized_version, Degree(La), Discriminant(O);
print "BERRY_C1_REBUILD_SUPPORT_SLOT_METADATA", #serialized_support;
print "BERRY_C1_REBUILD_RELATIONS", serialized_unit_relation, serialized_sunit_relation;
print "BERRY_C1_REBUILD_V1_DONE";
