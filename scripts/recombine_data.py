#!/usr/bin/env python3

"""
Recombine data into data for S(V) and r(v) plots.

For example:

$ scripts/recombine_data.py NC 2022

"""

import argparse
import json

from method_eval.helpers import read_typed_csv, write_pickle


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

    avgDWin = s["averageDVf"] if "averageDVf" in s else None
    avgRWin = s["averageRVf"] if "averageRVf" in s else None
    decl = s["bias"]["decl"] if "decl" in s["bias"] else None
    rvPoints = s["bias"]["rvPoints"] if "rvPoints" in s["bias"] else None

    # Read the SV-points file w/ stats

    in_path = xx + year + "-" + "SV-points" + ".csv"
    types = [float] + [float] * 13

    dSVpoints = read_typed_csv(in_path, types)

    # Read the vi-points file w/ stats

    in_path = xx + year + "-" + "vi-points" + ".csv"
    types = [int] + [float] * 13

    byDistrict = read_typed_csv(in_path, types)

    # Read the metrics file w/ stats

    in_path = xx + year + "-" + "metrics" + ".csv"
    types = [str] + [float] * 13

    metrics = read_typed_csv(in_path, types)

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

    metrics_data = {}
    metrics_data["metrics"] = metrics

    # Pickle these native structures for use by plots

    out_path = xx + year + "-" + "SV-data" + ".pickle"
    write_pickle(out_path, sv_data)

    out_path = xx + year + "-" + "rv-data" + ".pickle"
    write_pickle(out_path, rv_data)

    out_path = xx + year + "-" + "metrics-data" + ".pickle"
    write_pickle(out_path, metrics_data)

except:
    raise Exception("Exception reading or writing file")
