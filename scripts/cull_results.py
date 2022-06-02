#!/usr/bin/env python3

"""
Cull results from dra-analytics output.

For example:

$ scripts/cull_results.py NC 2022 composite

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

    in_path = args.state + args.year + "-" + args.election + "-profile.json"
    with open(in_path, "r") as f:
        p = json.load(f)

    Vf = p["statewide"]
    n = len(p["byDistrict"])

    # From scorecard

    in_path = args.state + args.year + "-" + args.election + "-scorecard.json"
    with open(in_path, "r") as f:
        s = json.load(f)

    """
    Metrics (from dra-analytics):

    * S_V = the estimated Democratic seats, using seat probabilities
    * FPTP = the estimated number of Democratic seats using first past the post
    * PR = the Democratic seats closest to proportional

    * BS_50 = Seat bias as a fraction of N
    * BV_50 = Votes bias as a fraction
    * DECL = Declination
    * GS = Global symmetry

    * EG = Efficiency gap as a fraction
    * BS_V = Seats bias @ <V> (geometric)
    * PROP = Disproportionality
    * MM = Mean – median difference using statewide Vf
    * TO = Turnout bias
    * MM' = Mean – median difference using average district v 
    * LO = Lopsided outcomes

    """

    bestS = s["bias"]["bestS"]
    fptpS = s["bias"]["fptpS"]
    estS = s["bias"]["estS"]

    bS50 = s["bias"]["bS50"]
    bV50 = s["bias"]["bV50"]
    decl = s["bias"]["decl"]
    gSym = s["bias"]["gSym"]

    eG = s["bias"]["eG"]
    bSV = s["bias"]["bSV"]
    prop = s["bias"]["prop"]
    mMs = s["bias"]["mMs"]
    tOf = s["bias"]["tOf"]
    mMd = s["bias"]["mMd"]
    lO = s["bias"]["lO"]

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

    # Append row

    out_path = args.state + args.year + "-elections-analysis.csv"
    with open(out_path, "a") as f:
        if verbose:
            print(
                "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
                    "XX",
                    "YEAR",
                    "ELECTION",
                    "CD",
                    "Vf",
                    "S_V",
                    "FPTP",
                    "PR",
                    "BS_50",
                    "BV_50",
                    "DECL",
                    "GS",
                    "EG",
                    "BS_V",
                    "PROP",
                    "MM",
                    "TO",
                    "MM'",
                    "LO",
                    "L_Vf",
                    "L_Sf",
                    "U_Vf",
                    "U_Sf",
                ),
                file=f,
            )
        print(
            "{}, {}, {}, {}, {:.6f}, {:.6f}, {}, {}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}".format(
                xx,
                year,
                election,
                n,
                Vf,
                estS,
                fptpS,
                bestS,
                bS50,
                bV50,
                decl,
                gSym,
                eG,
                bSV,
                prop,
                mMs,
                tOf,
                mMd,
                lO,
                lower_Vf,
                lower_Sf,
                upper_Vf,
                upper_Sf,
            ),
            file=f,
        )

except:
    raise Exception("Exception reading JSON file")
