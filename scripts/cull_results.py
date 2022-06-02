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

    * bestS = the Democratic seats closest to proportional
    * fptpS = the estimated number of Democratic seats using first past the post
    * estS = the estimated Democratic seats, using seat probabilities

    * bS50 = Seat bias as a fraction of N
    * bV50 = Votes bias as a fraction
    * decl = Declination
    * gSym = Global symmetry

    * EG = Efficiency gap as a fraction
    * bSV = Seats bias @ <V> (geometric)
    * prop = Disproportionality
    * mMs = Mean – median difference using statewide Vf
    * tOf = Turnout bias
    * mMd = Mean – median difference using average district v 
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

    # Append row

    out_path = args.state + args.year + "-elections-analysis.csv"
    with open(out_path, "a") as f:
        if verbose:
            print(
                "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
                    "xx",
                    "year",
                    "election",
                    "n",
                    "Vf",
                    "estS",
                    "bestS",
                    "fptpS",
                    "bS50",
                    "bV50",
                    "decl",
                    "gSym",
                    "EG",
                    "bSV",
                    "prop",
                    "mMs",
                    "tOf",
                    "mMd",
                    "LO",
                ),
                file=f,
            )
        print(
            "{}, {}, {}, {}, {:.6f}, {:.6f}, {}, {}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f},".format(
                xx,
                year,
                election,
                n,
                Vf,
                estS,
                bestS,
                fptpS,
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
            ),
            file=f,
        )


except:
    raise Exception("Exception reading JSON file")
