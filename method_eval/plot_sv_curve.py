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
    # blue = "#0000ff"
    traces = []
    # x_range = [0.0, 1.0]
    # y_range = [0.0, 1.0]

    sym = 0.5
    S_EG = 0.5 + (2.0 * (Vf - 0.5))
    margin = 0.05

    lo_x = max(0, min(sym, Vf, Sf, S_EG) - margin)
    hi_x = min(1, max(sym, Vf, Sf, S_EG) + margin)

    x_range = [lo_x, hi_x]
    y_range = x_range

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

    # Add traces in the right order

    traces.append(h_rule)
    traces.append(v_rule)
    traces.append(prop_rule)
    traces.append(prop2_rule)

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
            tickmode="linear",
            ticks="outside",
            # tick0=0.0,
            # dtick=0.1,
            # tickformat=".0%",
            # tickformat="%{x:5.2%}",
            # showline=True,
            # showgrid=True,
            # showticklabels=True,
            # linecolor="black",
            # gridcolor="black",
            # tickcolor="black",
            # ticklabelposition="outside",
        ),
        yaxis=dict(
            # range=[0.0, 1.0], tickmode="linear", ticks="outside", tick0=0, dtick=0.25
            title="Seat %",
            range=y_range,
            scaleanchor="x",
            scaleratio=1,
            tickmode="linear",
            ticks="outside",
            # tick0=0.0,
            # dtick=0.1,
            # tickformat=".0%",
            # tickformat="%{y:5.2%}",
            # showline=True,
            # showgrid=True,
            # showticklabels=True,
            # linecolor="black",
            # # gridcolor="black",
            # tickcolor="black",
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


"""
Copied from dra-analytics-app:

  renderSVCurveDiagram(bLegend: boolean, bRCurve: boolean): void
  {
    // Called only if openView, which guarantees profile and scorecard are not null
    const { designSize } = this.props;

    type SVpoint = {
      v: number;  // A fraction [0.0–1.0]
      s: number   // A fraction [0.0–1.0]
    };

    // NOTE - The variable names use Python naming conventions, because I cloned
    //   this code from my Python implementation.

    if (!document.getElementById('sv-curve') || !this.profile || !this.scorecard || !this.state.svDirty)
      return;

    // BIND DATA FROM PROFILE & SCORECARD

    const name = this.name;

    // Unzip the D S/V curve points into separate V and S arrays.
    const dSVpoints: SVpoint[] = this.scorecard.dSVpoints;
    const v_d: number[] = dSVpoints.map(pt => pt.v);
    const s_d: number[] = dSVpoints.map(pt => pt.s);

    const Bv = this.scorecard.bias.bV50 as number;
    const Bs = this.scorecard.bias.bS50 as number;

    const rSVpoints: SVpoint[] = this.scorecard.rSVpoints;
    const v_r: number[] = rSVpoints.map(pt => pt.v);
    const s_r: number[] = rSVpoints.map(pt => pt.s);

    const Vf: number = this.profile.statewide;
    const Sf: number = Vf - this.scorecard.bias.prop;

    // END BIND

    let svTraces = [];
    let svLayout = {};
    let svConfig = {};

    // Pre-zoom the graph in on the square region that encompasses:
    // * The center point of symmetry -- (0.5, 0.5)
    // * Proportionality at Vf -- (Vf, Sf)
    // * Seats bias -- (0.5, 0.5 - seats bias)
    // * Votes bias -- (0.5 + votes bias, 0.5)
    // * Extra credit: EG at Vf

    let x_range: number[] = [0.0, 1.0];
    let y_range: number[] = [0.0, 1.0];

    const sym: number = 0.5;
    const S_BS_50: number = 0.5 - this.scorecard.bias.bS50;  // More binding
    const V_BV_50: number = 0.5 + this.scorecard.bias.bV50;  // More binding
    const S_EG: number = 0.5 + (2.0 * (Vf - 0.5));

    const margin: number = 0.05;  // +/– 5%

    const lo_x: number = Math.min(sym, Vf, Sf, S_BS_50, V_BV_50, S_EG) - margin;
    const hi_x: number = Math.max(sym, Vf, Sf, S_BS_50, V_BV_50, S_EG) + margin;

    x_range = [lo_x, hi_x];
    y_range = x_range;

    // End pre-zoom

    // Make horizontal and vertical rules @ 0.50. And proportional rule.

    const r_x = [0.0, 0.5, 1.0];
    const r_y = [0.0, 0.5, 1.0];
    const r_s = [0.5, 0.5, 0.5];
    const r_v = [0.5, 0.5, 0.5];
    // The S=V line
    const prop_x = [0.0, 0.5, 1.0];
    // The EG=0 line
    const prop2_x = [0.25, 0.5, 0.75];
    const prop_y = [0.0, 0.5, 1.0];

    // "Local" region traces
    const shadedColor = 'whitesmoke';
    const local = 5 / 100;          // "Local" range = 5%
    const delta = local / 2;        // +/– Vf
  
    const vrVMinusTrace = {
      x: [Vf - delta, Vf - delta],
      y: [0.0, 1.0],
      type: 'scatter',
      mode: 'lines',
      line: {
        color: shadedColor,
        width: 0.5
      },
      hoverinfo: 'none',
      showlegend: false
    };

    const vrVPlusTrace = {
      x: [Vf + delta, Vf + delta],
      y: [0.0, 1.0],
      fill: 'tonextx',
      fillcolor: shadedColor,
      type: 'scatter',
      name: 'Uncertainty',
      text: 'uncertainty',
      mode: 'lines',
      line: {
        color: shadedColor,
        width: 0.5
      },
      hoverinfo: 'none',
      showlegend: true
    };
  

    const hoverTemplate = 'Vote %: %{x:5.2%}, Seat %: %{y:5.2%}<extra></extra>';
    const d_sv_curve = {
      x: v_d,
      y: s_d,
      mode: 'lines',
      name: 'Democratic',
      marker: {
        color: blue,
        size: 5
      },
      hovertemplate: hoverTemplate,
      showlegend: (bRCurve) ? true : false
    }

    const halfPtHoverTemplate = 'Vote %: 50%, Seat %: 50%<extra></extra>';
    const half_pt_trace = {
      x: [0.5],
      y: [0.5],
      mode: 'markers',
      type: 'scatter',
      marker: {
        color: 'black',
        symbol: 'circle',
        size: 8,
      },
      hoverinfo: 'text',
      hovertemplate: halfPtHoverTemplate,
      showlegend: false
    };

    const bvPtLabel = 'Votes bias: ' + AU.formatNumber(Bv, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
    const bvPtHoverTemplate = bvPtLabel + '<extra></extra>';
    const bvFormatted = AU.formatNumber(Bv, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
    const bv_pt_trace = {
      x: [Bv + 0.5],
      y: [0.5],
      mode: 'markers',
      type: 'scatter',
      name: 'Votes bias: ' + bvFormatted,
      marker: {
        color: 'black',
        symbol: 'diamond',
        size: 8,
      },
      hoverinfo: 'text',
      hovertemplate: bvPtHoverTemplate,
      showlegend: true
    };

    const bsPtLabel = 'Seats bias: ' + AU.formatNumber(Bs, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
    const bsPtHoverTemplate = bsPtLabel + '<extra></extra>';
    const bsFormatted = AU.formatNumber(Bs, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
    const bs_pt_trace = {
      x: [0.5],
      y: [0.5 - Bs],
      mode: 'markers',
      type: 'scatter',
      name: 'Seats bias: ' + bsFormatted,
      marker: {
        color: 'black',
        symbol: 'square',
        size: 8,
      },
      hoverinfo: 'text',
      hovertemplate: bsPtHoverTemplate,
      showlegend: true
    };

    const bv_ray = {
      x: [0.5, Bv + 0.5],
      y: [0.5, 0.5],
      mode: 'lines',
      line: {
        color: 'black',
        width: 1,
        dash: 'solid'
      },
      hoverinfo: 'none',
      showlegend: false
    }

    const bs_ray = {
      x: [0.5, 0.5],
      y: [0.5, 0.5 - Bs],
      mode: 'lines',
      line: {
        color: 'black',
        width: 1,
        dash: 'solid'
      },
      hoverinfo: 'none',
      showlegend: false
    }

    const r_sv_curve = {
      x: v_r,
      y: s_r,
      mode: 'lines',
      name: 'Republican',
      marker: {
        color: red,
        size: 5
      },
      hovertemplate: hoverTemplate,
      showlegend: true
    }

    const h_rule = {
      x: r_x,
      y: r_s,
      name: 'Seat % = 50%',
      mode: 'lines',
      line: {
        color: 'black',
        width: 0.5,
        dash: 'solid'     // 'dash'
      },
      hoverinfo: 'none',  // 'text',
      // hoveron: 'points',
      showlegend: false   // true
    }

    const v_rule = {
      x: r_v,
      y: r_y,
      name: 'Vote % = 50%',
      mode: 'lines',
      line: {
        color: 'black',
        width: 0.5,
        dash: 'solid'     // 'dot'
      },
      hoverinfo: 'none',  // 'text',
      // hoveron: 'points',
      showlegend: false   // true
    }

    const prop_rule = {
      x: prop_x,
      y: prop_y,
      mode: 'lines',
      line: {
        color: 'black',
        width: 0.5,
        dash: 'dot'
      },
      hoverinfo: 'none',
      showlegend: false
    }
    const prop2_rule = {
      x: prop2_x,
      y: prop_y,
      mode: 'lines',
      line: {
        color: 'black',
        width: 0.5,
        dash: 'dash'
      },
      hoverinfo: 'none',
      showlegend: false
    }

    const statewideVf = this.profile.statewide;
    const nPts = 20;
    const statewideVfXs = [...Array(nPts + 1).keys()].map(x => statewideVf);
    const ruleYs = [...Array(nPts + 1).keys()].map(y => ((100 / nPts) * y) / 100);
    const statewideVfWinHoverLabel = 'Total D vote: ' + AU.formatNumber(statewideVf, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
    const statewideVfTrace = {
      x: statewideVfXs,
      y: ruleYs,
      type: 'scatter',
      mode: 'lines',
      name: statewideVfWinHoverLabel,  //'Statewide D vote %',
      line: {
        color: 'black',
        width: 1,
        dash: 'dashdot'
      },
      text: statewideVfWinHoverLabel,
      hoverinfo: 'text',
      hoveron: 'points',
      showlegend: true
    };

    svTraces.push(vrVMinusTrace);
    svTraces.push(vrVPlusTrace);
    svTraces.push(prop2_rule);

    svTraces.push(h_rule);
    svTraces.push(v_rule);
    svTraces.push(prop_rule);
    svTraces.push(statewideVfTrace);
    svTraces.push(d_sv_curve);
    if (bRCurve)
      svTraces.push(r_sv_curve);
    svTraces.push(half_pt_trace);
    svTraces.push(bv_pt_trace);
    svTraces.push(bs_pt_trace);
    svTraces.push(bv_ray);
    svTraces.push(bs_ray);

    const svSize = AU.plotWidth(designSize) - 25;

    // Place the legend based on whether & where the plot is pre-zoomed
    // - If (Sf > 0.5) => lower right
    // - If (Sf < 0.5) => upper left
    // - x,y units are normalized, not Vf, Sf

    const tab = 0.02;  // 2% indent margin
    const x_anchor = (Sf > 0.5) ? 'right' : 'left';
    const y_anchor = (Sf > 0.5) ?  'bottom' : 'top';
    const x_pos = (Sf > 0.5) ? 1 - tab : 0 + tab;
    const y_pos = (Sf > 0.5) ? 0 + tab : 1 - tab;

    svLayout = {
      title: 'Seats-Votes Curve: ' + name,
      width: svSize,
      height: svSize,
      xaxis: {
        title: "Vote %",
        range: x_range,
        // rangemode: 'nonnegative',  // Experimented w/ this to keep axis positive
        tickmode: 'linear',
        ticks: 'outside',
        tick0: 0.0,
        dtick: 0.1,
        tickformat: '%{x:5.2%}'
      },
      yaxis: {
        title: "Seat %",
        range: y_range,
        // rangemode: 'nonnegative',  // Experimented w/ this to keep axis positive
        scaleanchor: 'x',
        scaleratio: 1,
        tickmode: 'linear',
        ticks: 'outside',
        tick0: 0.0,
        dtick: 0.1,
        tickformat: '%{y:5.2%}'
      },
      dragmode: 'zoom',
      hovermode: 'closest',
      showlegend: bLegend,
      legend: {
        xanchor: x_anchor,
        yanchor: y_anchor,
        x: x_pos,
        y: y_pos,
        // x: 0.60,
        // y: 0.01,
        bordercolor: 'black',
        borderwidth: 1
      },
      paper_bgcolor: bgcolor,
      plot_bgcolor: bgcolor
    }

    // Configure hover menu options & behavior

    svConfig = {
      toImageButtonOptions: {
        format: 'png', // one of png, svg, jpeg, webp
        filename: 's(v)-curve'
      },
      // Remove the unwanted plotly hover commands. Let users pan & zoom.
      modeBarButtonsToRemove: ['zoom2d', 'select2d', 'lasso2d', 'autoScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian'],
      // modeBarButtonsToRemove: ['zoom2d', /* 'select2d', */ 'lasso2d', 'autoScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian'],
      scrollZoom: true,
      displayModeBar: true,
      displaylogo: false,
      responsive: true
    };

    var svDiv = document.getElementById('sv-curve');

    Plotly.react(svDiv, svTraces, svLayout, svConfig);
    this.setState({svDirty: false});
  }

"""
