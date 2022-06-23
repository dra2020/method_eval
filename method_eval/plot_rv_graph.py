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
    name = data["name"]
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
    diagramWidth = rvSize
    shadedColor = "beige"
    delta = 5 / 100  # COMPETITIVE: 0.5 +/– 0.05
    N = len(byDistrict)
    W = diagramWidth * (2 / 3)
    markerSize = min(max(1, round(W / N)), 12)

    bgcolor = "#fafafa"
    traces = []

    # EXTRACT R(V) GRAPH DATA

    # Step 1 - The districts are already sorted
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

    # Step 7 - Split the sorted Vf, rank, and label arrays into R and D subsets.

    nRWins = len([x for x in sortedVfArray if x <= 0.5])  # Ties credited to R's
    rWinVfs = sortedVfArray[0:nRWins]
    rWinRanks = districtRanks[0:nRWins]
    rWinLabels = sortedLabels[0:nRWins]

    dWinVfs = sortedVfArray[nRWins:]
    dWinRanks = districtRanks[nRWins:]
    dWinLabels = sortedLabels[nRWins:]

    # CREATE THE TRACES

    # TOD) - Add district labels
    repWinTrace = go.Scatter(
        x=rWinRanks,
        y=rWinVfs,
        mode="markers",
        type="scatter",
        text=rWinLabels,
        marker=dict(color="black", symbol="square", size=markerSize),
        hoverinfo="none",
        showlegend=False,
    )

    demWinTrace = go.Scatter(
        x=dWinRanks,
        y=dWinVfs,
        mode="markers",
        type="scatter",
        text=dWinLabels,
        marker=dict(color="black", symbol="square-open", size=markerSize),
        hoverinfo="none",
        showlegend=False,
    )

    hr50Trace = go.Scatter(
        x=[0.0, 1.0],
        y=[0.5, 0.5],
        type="scatter",
        mode="lines",
        line=dict(color="black", width=1),
        hoverinfo="none",
        showlegend=False,
    )

    # TODO - HERE

    # Add traces in the right order

    # traces.append(hr50Trace)
    traces.append(repWinTrace)
    traces.append(demWinTrace)

    # The r(v) plot layout

    rankRange = [0.0, 1.0]
    vfRange = [max(minVf - 0.025, 0.0), min(maxVf + 0.025, 1.0)]

    heightPct = vfRange[1] - vfRange[0]
    diagramHeight = 700 if ((heightPct * diagramWidth) > 450) else 450

    rvLayout = go.Layout(
        title=name,
        width=diagramWidth,
        height=diagramHeight,
        xaxis=dict(
            title="District",
            range=rankRange,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            title="D Vote %",
            range=vfRange,
            scaleanchor="x",
            scaleratio=1,
            zeroline=False,
            tickformat=".0%",
            showgrid=True,
            gridcolor="lightgrey",
        ),
        # dragmode='zoom',
        # hovermode='closest',
        showlegend=False,
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor,
    )

    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
    fig = go.Figure(data=traces, layout=rvLayout)
    py.plot(fig, filename="rv-graph")


### HELPERS ###


def rank(i, n):
    return (i - 0.5) / n


def distance(pt1, pt2):
    X = 0
    Y = 1

    d = sqrt(((pt2[X] - pt1[X]) ** 2) + ((pt2[Y] - pt1[Y]) ** 2))

    return d
