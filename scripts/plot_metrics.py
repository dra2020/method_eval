#!/usr/bin/env python3

"""
Plot metric

For example:

$ scripts/plot_metrics.py NC 2022 main

"""

import argparse

from method_eval import read_pickle, plot_metrics


parser = argparse.ArgumentParser(description="Plot metrics with errors")

parser.add_argument("state", help="Two-character state abbreviation")
parser.add_argument("year", help="yyyy year")
parser.add_argument("metrics", help="Metrics")

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()

try:
    xx = args.state
    year = args.year
    metrics = args.metrics

    verbose = args.verbose

    in_path = xx + year + "-metrics-data.pickle"

    data = read_pickle(in_path)
    data["name"] = xx + " " + year + " Congress"

    bNormalize = False if metrics == "main" else True

    plot_metrics(data, bNormalize)

except:
    raise Exception("Exception reading input file")
