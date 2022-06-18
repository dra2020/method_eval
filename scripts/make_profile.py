#!/usr/bin/env python3

"""
Convert a DRA "District Abstract" to a partisan profile for dra-analytics.

For example:

$ scripts/make_profile.py NC 2022 composite

"""

import json
import argparse

parser = argparse.ArgumentParser(description="Make a partisan profile")

parser.add_argument("state", help="Two-character state abbreviation")
parser.add_argument("year", help="yyyy year")
parser.add_argument("election", help="Election datasets")

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()

try:
    in_path = args.state + args.year + "-" + args.election + "-district-abstract.json"
    with open(in_path, "r") as f:
        data = json.load(f)

    profile = {}
    profile["statewide"] = data["partisanship"]["statewide"]
    profile["byDistrict"] = data["partisanship"]["byDistrict"]

    out_path = "_" + args.state + args.year + "-" + args.election + "-profile.json"
    with open(out_path, "w") as f:
        json.dump(profile, f)

except:
    raise Exception("Exception reading JSON file")
