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
    in_path = args.state + args.year + "-" + args.election + "-profile.json"
    with open(in_path, "r") as f:
        data = json.load(f)

    xx = args.state
    year = args.year
    election = args.election
    statewide = data["statewide"]
    n = len(data["byDistrict"])

    print("{}, {}, {}, {}".format("xx", "year", "election", "n"))
    print("{}, {}, {}, {}".format(xx, year, election, n))

    # out_path = args.state + args.year + "-" + args.election + "-profile.json"
    # with open(out_path, "w") as f:
    #     json.dump(profile, f)

except:
    raise Exception("Exception reading JSON file")
