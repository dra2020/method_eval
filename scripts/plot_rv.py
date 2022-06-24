#!/usr/bin/env python3

"""
Plot r(v) graph

For example:

$ scripts/plot_rv.py NC 2022

"""

import argparse

from method_eval import read_pickle, plot_rv_graph


parser = argparse.ArgumentParser(description="Plot an r(v) graph")

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

    in_path = xx + year + "-rv-data.pickle"

    data = read_pickle(in_path)
    data["name"] = xx + " " + year + " Congress"

    plot_rv_graph(data)

except:
    raise Exception("Exception reading input file")
