#!/usr/bin/env python3

"""
PLOT r(v) GRAPH

"""

import chart_studio.plotly as py
import plotly.graph_objs as go  # https://plotly.com/python-api-reference/plotly.graph_objects.html

import numpy as np
from math import erf, sqrt, isclose


def plot_rv_graph(data):
    # Bind data
    Vf = data["Vf"]
    avgDWin = data["avgDWin"]
    avgRWin = data["avgRWin"]
    decl = data["decl"]
    Sb = data["rvPoints"]["Sb"]
    Ra = data["rvPoints"]["Ra"]
    Rb = data["rvPoints"]["Rb"]
    Va = data["rvPoints"]["Va"]
    Vb = data["rvPoints"]["Vb"]

    byDistrict = data["byDistrict"]

    # Housekeeping

    rvSize = 700 - 25
    bgcolor = "#fafafa"
    traces = []

    # Extract r(v) graph data - cloned from the TypeScript implementation in DRA proper

    # Step 1 - The districts are already sorted
    N = len(byDistrict)
    minVf = byDistrict[0]["composite"]
    maxVf = byDistrict[-1]["composite"]

    # Step 2 - Because the districts are already sorted, skip this step.
    # Step 3 - Ditto

    # Step 4 - Unzip that into separate sorted Vf and sorted districtId arrays.
    # Step 5 - Create a sorted array of district labels.

    sortedVfArray = []
    sortedIndexes = []
    sortedLabels = []

    for i, d in enumerate(byDistrict):
        sortedVfArray.append(d["composite"])
        sortedIndexes.append(d["CD"])
        sortedLabels.append(str(d["CD"]))

    # Step 6 - Create an array of district ranks that correspond to the 1–N ordering.
    districtRanks = [rank(i + 1, N) for i in range(0, N)]

    # TODO - HERE
    # Step 7 - Split the sorted Vf, rank, and label arrays into R and D subsets.

    ###

    B = np.linspace(0.35, 0.65, 100)

    A = [(1 - est_seat_probability(i)) for i in B]
    r = [est_district_responsiveness(i) for i in B]

    trace1 = go.Scatter(
        x=B, y=A, mode="lines", name="Probability of party A seat", marker=dict(size=3)
    )

    trace2 = go.Scatter(
        x=B, y=r, mode="lines", name="Responsiveness fraction", marker=dict(size=3)
    )

    layout = go.Layout(
        title="Seat Probability & Responsiveness",
        xaxis=dict(
            title="Fraction that voted for party B",
            range=[0.35, 0.65],
            tickmode="linear",
            ticks="outside",
            tick0=0.35,
            dtick=0.05,
        ),
        yaxis=dict(
            range=[0.0, 1.0], tickmode="linear", ticks="outside", tick0=0, dtick=0.25
        ),
    )

    traces.append(trace1)
    traces.append(trace2)

    ###

    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename="rv-graph")


### HELPERS ###


def rank(i, n):
    return (i - 0.5) / n


def distance(pt1, pt2):
    X = 0
    Y = 1

    d = sqrt(((pt2[X] - pt1[X]) ** 2) + ((pt2[Y] - pt1[Y]) ** 2))

    return d


### DELETE ###


def est_seat_probability(vpi):
    return 0.5 * (1 + erf((vpi - 0.50) / (0.02 * sqrt(8))))


def est_district_responsiveness(vpi):
    return 1 - 4 * (est_seat_probability(vpi) - 0.5) ** 2
