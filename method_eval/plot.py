#!/usr/bin/env python3
#
# TEST PLOTLY INTEGRATION
#

import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import numpy as np
from math import erf, sqrt, isclose

chart_studio.tools.set_credentials_file(
    username="alecramsay", api_key="z1yBCOsQV3ARxY1CoQLa"
)


def plot_figure_1():
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

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    py.plot(fig, filename="Figure-1")


def est_seat_probability(vpi):
    return 0.5 * (1 + erf((vpi - 0.50) / (0.02 * sqrt(8))))


def est_district_responsiveness(vpi):
    return 1 - 4 * (est_seat_probability(vpi) - 0.5) ** 2
