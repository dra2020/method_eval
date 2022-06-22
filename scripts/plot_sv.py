#!/usr/bin/env python3

"""
Plot S(V) curve

For example:

$ scripts/plot_sv.py NC 2022

"""

import argparse

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

    in_path = xx + year + "-SV-data.pickle"

    data = read_pickle(in_path)
    data["name"] = xx + " " + year + " Congress"

    plot_sv_curve(data)

except:
    raise Exception("Exception reading input file")
