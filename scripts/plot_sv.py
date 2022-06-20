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

    # Read the temp file w/o stats

    in_path = xx + year + "-" + "SV-points" + ".csv"
    # Vf, composite, P2020, P2016, S2020, S2016, G2020, AG2020, MEAN, SEM, STDEV
    types = [float] * 11

    rows = read_typed_csv(in_path, types)

    # TODO - Plot S(V) curve
    print(rows)

except:
    raise Exception("Exception reading CSV file")
