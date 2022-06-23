#!/usr/bin/env python3

"""
Recombine data into data for S(V) and r(v) plots.

For example:

$ scripts/recombine_data.py NC 2022

"""

import argparse
import json

from method_eval import *


parser = argparse.ArgumentParser(description="Calculate statistics")

parser.add_argument("state", help="Two-character state abbreviation")
parser.add_argument("year", help="yyyy year")

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()

try:
    # Args

    xx = args.state
    year = args.year

    verbose = args.verbose

    # From profile

    in_path = "_" + args.state + args.year + "-" + "composite" + "-profile.json"
    with open(in_path, "r") as f:
        p = json.load(f)

    Vf = p["statewide"]

    # From scorecard

    in_path = "_" + args.state + args.year + "-" + "composite" + "-scorecard.json"
    with open(in_path, "r") as f:
        s = json.load(f)

    Sf = s["bias"]["estSf"]

    avgDWin = s["averageDVf"]
    avgRWin = s["averageRVf"]
    decl = s["bias"]["decl"]
    rvPoints = s["bias"]["rvPoints"]

    # Read the SV-points file w/ stats

    in_path = xx + year + "-" + "SV-points" + ".csv"
    types = [float] + [float] * 10

    dSVpoints = read_typed_csv(in_path, types)

    # Read the vi-points file w/ stats

    in_path = xx + year + "-" + "vi-points" + ".csv"
    types = [int] + [float] * 10

    byDistrict = read_typed_csv(in_path, types)

    # Populate the output dicts

    sv_data = {}
    sv_data["Vf"] = Vf
    sv_data["Sf"] = Sf
    sv_data["dSVpoints"] = dSVpoints

    rv_data = {}
    rv_data["Vf"] = Vf
    rv_data["byDistrict"] = byDistrict
    rv_data["avgDWin"] = avgDWin
    rv_data["avgRWin"] = avgRWin
    rv_data["decl"] = decl
    rv_data["rvPoints"] = rvPoints

    # Pickle these native structures for use by S(V) and r(v) plots

    out_path = xx + year + "-" + "SV-data" + ".pickle"
    write_pickle(out_path, sv_data)

    out_path = xx + year + "-" + "rv-data" + ".pickle"
    write_pickle(out_path, rv_data)

except:
    raise Exception("Exception reading or writing file")
