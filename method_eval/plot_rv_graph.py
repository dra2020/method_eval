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
    # avgDWin = data["avgDWin"]
    # avgRWin = data["avgRWin"]
    decl = data["decl"]
    byDistrict = data["byDistrict"]

    # Housekeeping

    rvSize = 700 - 25
    diagramWidth = rvSize
    N = len(byDistrict)
    markerSize = 5

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
    sortedMeans = []
    sortedErrs = []

    for i, d in enumerate(byDistrict):
        sortedVfArray.append(d["composite"])
        sortedIndexes.append(d["CD"])
        sortedLabels.append(str(d["CD"]))
        sortedMeans.append(d["MEAN"])
        sortedErrs.append(d["SEM"] * 1.96)

    # Step 6 - Create an array of district ranks that correspond to the 1–N ordering.
    districtRanks = [(i + 1) / N for i in range(0, N)]

    # Step 7 - Split the sorted Vf, rank, and label arrays into R and D subsets.

    nRWins = len([x for x in sortedVfArray if x <= 0.5])  # Ties credited to R's
    rWinVfs = sortedVfArray[0:nRWins]
    rWinRanks = districtRanks[0:nRWins]
    rWinLabels = sortedLabels[0:nRWins]
    rMeans = sortedMeans[0:nRWins]
    rErrs = sortedErrs[0:nRWins]

    dWinVfs = sortedVfArray[nRWins:]
    dWinRanks = districtRanks[nRWins:]
    dWinLabels = sortedLabels[nRWins:]
    dMeans = sortedMeans[nRWins:]
    dErrs = sortedErrs[nRWins:]

    bSweep = True if (nRWins == N) or (nRWins == 0) else False

    # CREATE THE TRACES

    repWinTrace = go.Scatter(
        x=rWinRanks,
        y=rWinVfs,
        mode="markers",
        type="scatter",
        text=rWinLabels,
        marker=dict(
            color="white",
            symbol="square",
            size=markerSize,
            line=dict(color="black", width=1),
        ),
        hoverinfo="none",
        showlegend=False,
    )
    rMeansTrace = go.Scatter(
        x=rWinRanks,
        y=rMeans,
        mode="markers",
        marker=dict(color="black", symbol="cross", size=markerSize),
        hoverinfo="none",
        showlegend=False,
        error_y=dict(
            type="data",  # value of error bar given in data coordinates
            array=rErrs,
            visible=True,
            color="black",
            width=1,
        ),
    )

    demWinTrace = go.Scatter(
        x=dWinRanks,
        y=dWinVfs,
        mode="markers",
        type="scatter",
        text=dWinLabels,
        marker=dict(
            color="white",
            symbol="square",
            size=markerSize,
            line=dict(color="black", width=1),
        ),
        hoverinfo="none",
        showlegend=False,
    )
    dMeansTrace = go.Scatter(
        x=dWinRanks,
        y=dMeans,
        mode="markers",
        marker=dict(color="black", symbol="cross", size=markerSize),
        hoverinfo="none",
        showlegend=False,
        error_y=dict(
            type="data",  # value of error bar given in data coordinates
            array=dErrs,
            visible=True,
            color="black",
            width=1,
        ),
    )

    if not bSweep and decl != 0:
        X = 0
        Y = 1

        Sb = data["rvPoints"]["Sb"]
        Ra = data["rvPoints"]["Ra"]
        Rb = data["rvPoints"]["Rb"]
        Va = data["rvPoints"]["Va"]
        Vb = data["rvPoints"]["Vb"]

        # Shift the pivot point to halfway between the R & D districts

        shift = (2 * nRWins + 1) / (2 * N) - (1 - Sb)

        # Convert R vote shares (used in dra-score for 'decl') to D vote shares

        pivotDeclPt = [(1 - Sb) + shift, 0.5]
        # pivotDeclPt = [(1 - Sb), 0.5]
        rDeclPt = [(1 - Ra) + shift, (1 - Va)]
        # rDeclPt = [(1 - Ra), (1 - Va)]
        dDeclPt = [(1 - Rb) + shift, (1 - Vb)]
        # dDeclPt = [(1 - Rb), (1 - Vb)]

        # Make traces for the R & D line segments and the pivot point

        rDeclXs = [rDeclPt[X], pivotDeclPt[X]]
        rDeclYs = [rDeclPt[Y], pivotDeclPt[Y]]
        dDeclXs = [pivotDeclPt[X], dDeclPt[X]]
        dDeclYs = [pivotDeclPt[Y], dDeclPt[Y]]

        rDeclTrace = go.Scatter(
            x=rDeclXs,
            y=rDeclYs,
            mode="lines",
            type="scatter",
            line=dict(color="black", width=1),
            hoverinfo="none",
            showlegend=False,
        )
        traces.append(rDeclTrace)

        dDeclTrace = go.Scatter(
            x=dDeclXs,
            y=dDeclYs,
            mode="lines",
            type="scatter",
            line=dict(color="black", width=1),
            hoverinfo="none",
            showlegend=False,
        )
        traces.append(dDeclTrace)

        pivotPtTrace = go.Scatter(
            x=[pivotDeclPt[X]],
            y=[pivotDeclPt[Y]],
            mode="markers",
            type="scatter",
            marker=dict(
                color="white",
                symbol="circle",
                size=10,
                line=dict(color="black", width=2),
            ),
            hoverinfo="none",
            showlegend=False,
        )

        # Make the dotted line extension of the R trace, if decl is significant
        declThreshold = 5

        if abs(decl) > declThreshold:
            rDy = pivotDeclPt[Y] - rDeclPt[Y]
            rDx = pivotDeclPt[X] - rDeclPt[X]

            dDistance = distance(
                [pivotDeclPt[X], pivotDeclPt[Y]], [dDeclPt[X], dDeclPt[Y]]
            )
            rDistance = distance(
                [rDeclPt[X], rDeclPt[Y]], [pivotDeclPt[X], pivotDeclPt[Y]]
            )
            ratio = dDistance / rDistance

            beyondPt = [pivotDeclPt[X] + (ratio * rDx), pivotDeclPt[Y] + (ratio * rDy)]

            beyondDeclXs = [pivotDeclPt[X], beyondPt[X]]
            beyondDeclYs = [pivotDeclPt[Y], beyondPt[Y]]

            dottedDeclTrace = go.Scatter(
                x=beyondDeclXs,
                y=beyondDeclYs,
                mode="lines",
                type="scatter",
                line=dict(color="black", width=1, dash="dash"),
                hoverinfo="none",
                showlegend=False,
            )
            traces.append(dottedDeclTrace)

        # Add the pivot point *after* a potential dotted line, so that it's on "top"
        traces.append(pivotPtTrace)

    if len(rWinVfs) > 0:
        traces.append(rMeansTrace)
        traces.append(repWinTrace)
    if len(dWinVfs) > 0:
        traces.append(dMeansTrace)
        traces.append(demWinTrace)

    # The r(v) plot layout

    vfRange = [max(minVf - 0.025, 0.0), min(maxVf + 0.025, 1.0)]

    heightPct = vfRange[1] - vfRange[0]
    diagramHeight = 700 if ((heightPct * diagramWidth) > 450) else 450

    pad = 0.05
    rankRange = [1 / N - pad, 1 + pad]

    rvLayout = go.Layout(
        title=name,
        width=diagramWidth,
        height=diagramHeight,
        xaxis=dict(
            title="District rank",
            range=rankRange,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            title="Vote fraction",
            range=vfRange,
            scaleanchor="x",
            scaleratio=1,
            zeroline=False,
            tickformat="0.2f",
            # tickformat=".0%",
            showgrid=True,
            gridcolor="lightgrey",
        ),
        showlegend=False,
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor,
    )

    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
    fig = go.Figure(data=traces, layout=rvLayout)
    py.plot(fig, filename="rv-graph")


### HELPERS ###


# DELETE
# def rankDistricts(N, Sb, nRWins):
#     """
#     Compute left-to-right district "ranks" for the r(v) graph.
#     - Compute N + 1 ranks, where N is the # of districts.
#       The extra position is to accommodate the pivot point.
#     - Shift the district ranks so that the spacing of all districts and
#       the pivot point is equal.
#     - Make the rank/x-axis be from the first rank minus a pad to the last rank plus a pad.

#     - Handle both D & R sweeps, i.e. no pivot point.
#     """

#     bSweep = True if (nRWins == N) or (nRWins == 0) else False

#     nRanks = N if bSweep else N + 1
#     pivotRank = 1 - Sb

#     districtRanks = [(i + 1) / nRanks for i in range(0, nRanks)]

#     if not bSweep:
#         shift = pivotRank - districtRanks[nRWins]
#         districtRanks = list(map(lambda x: x + shift, districtRanks))

#     rWinRanks = districtRanks[0:nRWins] if nRWins > 0 else []
#     dWinRanks = districtRanks[nRWins + 1 :] if nRWins < N else []

#     pad = 0.05
#     rankRange = [districtRanks[0] - pad, districtRanks[-1] + pad]

#     return rWinRanks, dWinRanks, rankRange


def distance(pt1, pt2):
    X = 0
    Y = 1

    d = sqrt(((pt2[X] - pt1[X]) ** 2) + ((pt2[Y] - pt1[Y]) ** 2))

    return d
