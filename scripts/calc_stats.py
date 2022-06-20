#!/usr/bin/env python3

"""
Calculate statistics for each file.

For example:

$ scripts/calc_stats.py NC 2022 metrics str
$ scripts/calc_stats.py NC 2022 SV-points float
$ scripts/calc_stats.py NC 2022 vi-points int

$ ../../scripts/calc_stats.py NC 2022 metrics str

"""

import argparse

import os
from csv import DictReader, DictWriter
import builtins
import math
import statistics
from csv import DictReader, DictWriter

from method_eval.helpers import read_typed_csv, write_csv


parser = argparse.ArgumentParser(description="Calculate statistics")

parser.add_argument("state", help="Two-character state abbreviation")
parser.add_argument("year", help="yyyy year")
parser.add_argument("file", help="file")
parser.add_argument("type", help="key type")

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()

try:
    # Args

    xx = args.state
    year = args.year
    file = args.file
    type = args.type

    verbose = args.verbose

    # Read the temp file w/o stats

    in_path = "_" + xx + year + "-" + file + ".csv"
    types = [getattr(builtins, type)] + [float] * 7

    rows = read_typed_csv(in_path, types)

    # Calculate stats

    for row in rows:
        values = list(row.values())[2:]
        row["MEAN"] = round(statistics.mean(values), 6)
        row["SEM"] = round(statistics.stdev(values) / math.sqrt(len(values)), 6)
        row["STDEV"] = round(statistics.stdev(values), 6)
        # Calculate these downstream, if needed
        # row["RSE"] = round(row["SEM"] / row["MEAN"], 6)
        # row["RΔ"] = round((row["composite"] - row["MEAN"]) / row["MEAN"], 6)

    # Write the new CSV w/ stats

    out_path = xx + year + "-" + file + ".csv"
    cols = rows[0].keys()
    write_csv(out_path, rows, cols)

except:
    raise Exception("Exception reading CSV file")
