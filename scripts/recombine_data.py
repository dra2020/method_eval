#!/usr/bin/env python3

"""
Recombine data into data for S(V) and r(v) plots.

For example:

$ scripts/recombine_data.py NC 2022

"""

import argparse
import builtins

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

    # Output dicts

    sv_data = {}
    rv_data = {}

    # Read the metrics file w/ stats

    in_path = xx + year + "-" + "metrics" + ".csv"
    types = [getattr(builtins, "str")] + [float] * 10

    rows = read_typed_csv(in_path, types)

    for row in rows:
        if row["METRIC"] == "VF":
            sv_data["Vf"] = row

        if row["METRIC"] == "Sf":
            sv_data["Sf"] = row

    # Read the SV-points file w/ stats

    in_path = xx + year + "-" + "SV-points" + ".csv"
    types = [float] + [float] * 10

    rows = read_typed_csv(in_path, types)
    sv_data["dSVpoints"] = rows

    # Write the new JSON files
    print("S(V) data:", sv_data)

    # out_path = xx + year + "-" + file + ".csv"

except:
    raise Exception("Exception reading or writing file")
