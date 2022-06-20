#!/usr/bin/env python3

"""
Cull per-election results from the previously generated files.

For example:

$ scripts/cull_results.py NC 2022 composite


Metrics in metrics file:

* ELECTION = abbreviation of the election dataset
* Vf = the statewide D vote share

* S_V = the estimated D seats, using seat probabilities
* FPTP = the estimated # of D seats using first past the post
* PR = the D seats closest to proportional

* BS_50 = Seat bias as a fraction of CD
* BV_50 = Votes bias as a fraction
* DECL = Declination
* GS = Global symmetry

* EG = Efficiency gap as a fraction
* BS_V = Seats bias @ Vf (geometric)
* PROP = Disproportionality
* MM = Mean – median difference using statewide Vf
* TO = Turnout bias
* MM' = Mean – median difference using average district v 
* LO = Lopsided outcomes

* R (BIG_R) = Overall responsiveness or winner’s bonus 
* r (LIL_R) = The point responsiveness at Vf, i.e., the slope of the S(V) curve at Vf
* Rd (R_V) = the estimated responsive districts, using seat probabilities

* L_Vf = the D vote share of the inferred S(V) point ~2.0% below Vf
* L_Sf = the corresponding D seat share
* U_Vf = the D vote share of the inferred S(V) point ~2.0% above Vf
* U_Sf = the corresponding D seat share

"""

import json
import argparse

parser = argparse.ArgumentParser(description="Cull analytics results")

parser.add_argument("state", help="Two-character state abbreviation")
parser.add_argument("year", help="yyyy year")
parser.add_argument("election", help="Election datasets")

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()

try:
    # Args

    xx = args.state
    year = args.year
    election = args.election
    verbose = args.verbose

    # From profile

    in_path = "_" + args.state + args.year + "-" + args.election + "-profile.json"
    with open(in_path, "r") as f:
        p = json.load(f)

    Vf = p["statewide"]
    n = len(p["byDistrict"])

    # From scorecard

    in_path = "_" + args.state + args.year + "-" + args.election + "-scorecard.json"
    with open(in_path, "r") as f:
        s = json.load(f)

    bestS = s["bias"]["bestS"]
    fptpS = s["bias"]["fptpS"]
    estS = s["bias"]["estS"]
    estSf = s["bias"]["estSf"]

    bS50 = s["bias"]["bS50"]
    bV50 = s["bias"]["bV50"]
    decl = s["bias"]["decl"] if "decl" in s["bias"] else 0
    if "decl" not in s["bias"]:
        print("decl is undefined")
    gSym = s["bias"]["gSym"]

    eG = s["bias"]["eG"]
    bSV = s["bias"]["bSV"]
    prop = s["bias"]["prop"]
    mMs = s["bias"]["mMs"]
    tOf = s["bias"]["tOf"]
    mMd = s["bias"]["mMd"]
    lO = s["bias"]["lO"] if "lO" in s["bias"] else 0
    if "lO" not in s["bias"]:
        print("LO is undefined")

    # Responsiveness

    bigR = s["responsiveness"]["bigR"]
    littleR = s["responsiveness"]["littleR"]
    rD = s["responsiveness"]["rD"]

    # r(v) points
    Sb = s["bias"]["rvPoints"]["Sb"]
    Ra = s["bias"]["rvPoints"]["Ra"]
    Rb = s["bias"]["rvPoints"]["Rb"]
    Va = s["bias"]["rvPoints"]["Va"]
    Vb = s["bias"]["rvPoints"]["Vb"]

    # Add +/– 2% bracketing S(V) points

    # For Vf = 0.4873, [0.485, 0.490] => [0.465, 0.510]
    # For Vf = 0.4833, [0.480, 0.485] => [0.460, 0.505]

    t = 0.005
    base = round(Vf, 2)
    lower = base if base < Vf else base - t
    upper = base + t if base < Vf else base

    margin = 0.02
    lower = max(round(lower - margin, 3), 0.25)
    upper = min(round(upper + margin, 3), 0.75)

    epsilon = 1.0e-12

    lower_Vf = None
    lower_Sf = None
    upper_Vf = None
    upper_Sf = None

    for i, pt in enumerate(s["dSVpoints"]):
        if abs(pt["v"] - lower) < epsilon:
            lower_Vf = pt["v"]
            lower_Sf = pt["s"]
        if abs(pt["v"] - upper) < epsilon:
            upper_Vf = pt["v"]
            upper_Sf = pt["s"]

    # Write the metrics to a file

    out_path = "_" + args.state + args.year + "-" + args.election + "-metrics.csv"
    with open(out_path, "w") as f:
        print("{},{}".format("METRIC", args.election), file=f)
        # print("{},{}".format("CD", xx), file=f)
        print("{},{:.6f}".format("Vf", Vf), file=f)
        print("{},{:.6f}".format("S_V", estS), file=f)
        print("{},{:.6f}".format("Sf", estS), file=f)
        print("{},{:.6f}".format("FPTP", fptpS), file=f)
        print("{},{:.6f}".format("PR", bestS), file=f)
        print("{},{:.6f}".format("BS_50", bS50), file=f)
        print("{},{:.6f}".format("BV_50", bV50), file=f)
        print("{},{:.6f}".format("DECL", decl), file=f)
        print("{},{:.6f}".format("GS", gSym), file=f)
        print("{},{:.6f}".format("EG", eG), file=f)
        print("{},{:.6f}".format("BS_V", bSV), file=f)
        print("{},{:.6f}".format("PROP", prop), file=f)
        print("{},{:.6f}".format("MM", mMs), file=f)
        print("{},{:.6f}".format("TO", tOf), file=f)
        print("{},{:.6f}".format("MM'", mMd), file=f)
        print("{},{:.6f}".format("LO", lO), file=f)
        print("{},{:.6f}".format("R", bigR), file=f)
        print("{},{:.6f}".format("r", littleR), file=f)
        print("{},{:.6f}".format("Rd", rD), file=f)
        print("{},{:.6f}".format("L_Vf", lower_Vf), file=f)
        print("{},{:.6f}".format("L_Sf", lower_Sf), file=f)
        print("{},{:.6f}".format("U_Vf", upper_Vf), file=f)
        print("{},{:.6f}".format("U_Sf", upper_Sf), file=f)

    # Write the r(v) points to a file

    out_path = "_" + args.state + args.year + "-" + args.election + "-rv-points.csv"
    with open(out_path, "w") as f:
        print("{},{}".format("POINT", args.election), file=f)
        print("{},{:.6f}".format("Sb", Sb), file=f)
        print("{},{:.6f}".format("Ra", Ra), file=f)
        print("{},{:.6f}".format("Rb", Rb), file=f)
        print("{},{:.6f}".format("Va", Va), file=f)
        print("{},{:.6f}".format("Vb", Vb), file=f)

    # Write the v(i) points to a file

    out_path = "_" + args.state + args.year + "-" + args.election + "-vi-points.csv"
    with open(out_path, "w") as f:
        print(
            "{},{}".format("CD", args.election),  # + "_" + "Vf"),
            file=f,
        )

        for i, v in enumerate(p["byDistrict"]):
            j = i + 1
            print("{},{:.6f}".format(j, v), file=f)

    # Write the S(V) points to a file

    out_path = "_" + args.state + args.year + "-" + args.election + "-SV-points.csv"
    with open(out_path, "w") as f:
        print(
            "{},{}".format("Vf", args.election),  # + "_" + "Sf"),
            file=f,
        )

        for pt in s["dSVpoints"]:
            print("{:.3f},{:.6f}".format(pt["v"], pt["s"]), file=f)


except:
    raise Exception("Exception reading JSON file")
