#!/usr/bin/env python3

"""
Calculate FPTP declination.

For example:

$ scripts/calc_fptp_decl.py

"""

from method_eval import read_typed_csv, decl_degrees

# Args are hardcoded

xx = "IL"
year = "2022"
elections = [
    "composite",
    "P2020",
    "P2016",
    "S2020",
    "S2016",
    "G2018",
    "AG2018",
]

try:
    in_path = "data/" + xx + "/" + xx + year + "-vi-points.csv"
    types = [int] + [float] * 11

    rows = read_typed_csv(in_path, types)

    # Compute FPTP declination

    VfArrays = {}
    for e in elections:
        VfArrays[e] = []

    for row in rows:
        for e in elections:
            VfArrays[e].append(row[e])

    decls = [decl_degrees(vals) for vals in VfArrays.values()]

    print(decls)

except:
    raise Exception("Exception reading CSV file")
