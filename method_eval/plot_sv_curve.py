#!/usr/bin/env python3

"""
PLOT S(V) CURVE

"""

import chart_studio.plotly as py
import plotly.graph_objs as go  # https://plotly.com/python-api-reference/plotly.graph_objects.html


def plot_sv_curve(data):
    # Bind data

    Vf = data["Vf"]
    Sf = data["Sf"]
    dSVpoints = data["dSVpoints"]
    name = data["name"]

    # Housekeeping

    svSize = 700 - 25

    bgcolor = "#fafafa"
    # red = "#ff0000"
    blue = "#0000ff"
    # shadedColor = "beige"

    traces = []

    # Set view range

    # lo_x = 0.350
    # hi_x = 0.650
    sym = 0.5
    lo_x = min(Vf - 0.10, sym - 0.05)
    hi_x = max(Vf + 0.10, sym + 0.05)
    x_range = [lo_x, hi_x]
    y_range = x_range

    # Create core S(V) traces
    v_d = []
    s_d = []
    mean_s = []
    sem_s_minus = []
    sem_s_plus = []

    for pt in dSVpoints:
        v_d.append(pt["Vf"])
        s_d.append(pt["composite"])
        mean_s.append(pt["MEAN"])
        sem_s_minus.append(pt["MEAN"] - pt["SEM"])
        sem_s_plus.append(pt["MEAN"] + pt["SEM"])

    # Make horizontal and vertical rules @ 0.50. And proportional rule.

    r_x = [0.0, 0.5, 1.0]
    r_y = [0.0, 0.5, 1.0]
    r_s = [0.5, 0.5, 0.5]
    r_v = [0.5, 0.5, 0.5]
    # The S=V line
    prop_x = [0.0, 0.5, 1.0]
    # The EG=0 line
    prop2_x = [0.25, 0.5, 0.75]
    prop_y = [0.0, 0.5, 1.0]

    h_rule = go.Scatter(
        x=r_x,
        y=r_s,
        mode="lines",
        name="Seat % = 50%",
        line=dict(color="black", width=0.5, dash="solid"),
        hoverinfo="none",
        showlegend=False,
    )
    v_rule = go.Scatter(
        x=r_v,
        y=r_y,
        mode="lines",
        name="Vote % = 50%",
        line=dict(color="black", width=0.5, dash="solid"),
        hoverinfo="none",
        showlegend=False,
    )
    prop_rule = go.Scatter(
        x=prop_x,
        y=prop_y,
        mode="lines",
        name="Proportionality",
        line=dict(color="black", width=0.5, dash="dot"),
        hoverinfo="none",
        showlegend=False,
    )
    prop2_rule = go.Scatter(
        x=prop2_x,
        y=prop_y,
        mode="lines",
        name="EG = 0",
        line=dict(color="black", width=0.5, dash="dash"),
        hoverinfo="none",
        showlegend=False,
    )

    # Statewide D vote share

    v_Vf = [Vf, Vf, Vf]
    s_Vf = [0.0, 0.5, 1.0]
    Vf_rule = go.Scatter(
        x=v_Vf,
        y=s_Vf,
        mode="lines",
        name="Statewide D vote %",
        line=dict(color="black", width=1, dash="dashdot"),
        hoverinfo="none",
        showlegend=False,
    )

    # 'Local' region

    local = 5 / 100  # "Local" range = 5%
    delta = local / 2

    vrVMinusTrace = go.Scatter(
        x=[Vf - delta, Vf - delta],
        y=[0.0, 1.0],
        mode="lines",
        line=dict(color="lightgrey", width=1, dash="dashdot"),
        # line=dict(color=shadedColor, width=0.5),
        hoverinfo="none",
        showlegend=False,
    )
    vrVPlusTrace = go.Scatter(
        x=[Vf + delta, Vf + delta],
        y=[0.0, 1.0],
        # fill="tonextx",
        # fillcolor=shadedColor,
        # type="scatter",
        # name="Uncertainty",
        # text="uncertainty",
        mode="lines",
        line=dict(color="lightgrey", width=1, dash="dashdot"),
        # line=dict(color=shadedColor, width=0.5),
        hoverinfo="none",
        showlegend=False,
    )

    # Inferred D S(V) curve

    d_sv_curve = go.Scatter(
        x=v_d,
        y=s_d,
        mode="lines",
        name="Inferred S(V) curve",
        line=dict(color=blue, width=1),
        # hovertemplate=hoverTemplate,
        showlegend=False,
    )
    means_trace = go.Scatter(
        x=v_d,
        y=mean_s,
        mode="markers",
        marker=dict(color="black", symbol="diamond", size=3),
        showlegend=False,
    )

    # Error bars
    # https://plotly.com/chart-studio-help/make-a-graph-with-error-bars/

    # Add traces in the right order

    traces.append(vrVMinusTrace)
    traces.append(vrVPlusTrace)
    # traces.append(prop2_rule)
    # traces.append(h_rule)
    # traces.append(v_rule)
    # traces.append(prop_rule)
    traces.append(Vf_rule)
    traces.append(d_sv_curve)
    traces.append(means_trace)

    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html#plotly.graph_objects.Layout
    # For tick formatting
    # https://github.com/d3/d3-format/tree/v1.4.5#d3-format

    layout = go.Layout(
        title=name,
        width=svSize,
        height=svSize,
        xaxis=dict(
            title="Vote %",
            range=x_range,
            # tickmode="linear",
            # ticks="outside",
            # tick0=0.0,
            dtick=0.05,
            tickformat=".0%",
            # showline=True,
            showgrid=True,
            # showticklabels=True,
            # linecolor="black",
            gridcolor="lightgrey",
            # tickcolor="black",
            # ticklabelposition="outside",
        ),
        yaxis=dict(
            # range=[0.0, 1.0], tickmode="linear", ticks="outside", tick0=0, dtick=0.25
            title="Seat %",
            range=y_range,
            scaleanchor="x",
            scaleratio=1,
            # tickmode="linear",
            # ticks="outside",
            # tick0=0.0,
            dtick=0.05,
            tickformat=".0%",
            # showline=True,
            showgrid=True,
            # showticklabels=True,
            # linecolor="black",
            gridcolor="lightgrey",
            # tickcolor="black",
            # ticklabelposition="outside",
        ),
        dragmode="zoom",
        hovermode="closest",
        showlegend=False,
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor,
    )

    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename="s(v)-curve")
