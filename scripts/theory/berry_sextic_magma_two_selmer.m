// Exact full 2-Selmer attempt for the selected Berry Jacobian over Q(i).
// The free Calculator currently terminates this at its 60-second hard limit.
SetSeed(1);
print "BERRY_TWO_SELMER_V1_START";

K<i> := QuadraticField(-1);
P<t> := PolynomialRing(K);
g6 := t^6 + (-2 - 2*i)*t^5 + (-35 - 8*i)*t^4
    + (-52 - 28*i)*t^3 + (19 - 40*i)*t^2 + (6 + 14*i)*t - 1;
J := Jacobian(HyperellipticCurve(g6));

S, selmer_map, aux1, aux2 := TwoSelmerGroup(J);
print "BERRY_TWO_SELMER_V1_DONE";
print "SELMER_GROUP", S;
print "SELMER_INVARIANTS", Invariants(S);
print "SELMER_MAP_TYPE", Type(selmer_map);
print "AUX1_TYPE", Type(aux1);
print "AUX2_TYPE", Type(aux2);
