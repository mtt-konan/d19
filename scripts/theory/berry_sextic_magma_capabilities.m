// Fast capability probe for the public Magma Calculator.
SetSeed(1);
print "BERRY_MAGMA_CAPABILITIES_V1_START";

K<i> := QuadraticField(-1);
P<t> := PolynomialRing(K);
g6 := t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4
    + (-52 - 28*i)*t^3 + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1;
C := HyperellipticCurve(g6);
J := Jacobian(C);

assert Degree(K) eq 2;
assert Genus(C) eq 2;
assert Discriminant(g6) ne 0;
print "FIELD_DEGREE", Degree(K);
print "CURVE_GENUS", Genus(C);
print "JACOBIAN_TYPE", Type(J);
print "G6_IRREDUCIBLE", IsIrreducible(g6);

has_two_selmer, _ := IsIntrinsic("TwoSelmerGroup");
has_two_cover, _ := IsIntrinsic("TwoCoverDescent");
has_rank_bounds, _ := IsIntrinsic("RankBounds");
has_local_kummer, _ := IsIntrinsic("LocalKummerImage");
print "HAS_TWO_SELMER_GROUP", has_two_selmer;
print "HAS_TWO_COVER_DESCENT", has_two_cover;
print "HAS_RANK_BOUNDS", has_rank_bounds;
print "HAS_LOCAL_KUMMER_IMAGE", has_local_kummer;
print "BERRY_MAGMA_CAPABILITIES_V1_DONE";
