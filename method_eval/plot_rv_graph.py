#!/usr/bin/env python3

"""
PLOT r(v) GRAPH

"""


def plot_rv_graph():
    print("TODO - Plot r(v) graph")


"""
Copied from dra-analytics-app:

  renderRankVoteDiagram(bLegend: boolean): void
  {
    // Called only if openView, which guarantees profile and scorecard are set
    if (!document.getElementById('rank-vote-graph') || !this.profile || !this.scorecard || !this.state.rvDirty)
      return;

    const name = this.name;

    // DATA - RANK-VOTE DIAGRAM
    let rvTraces = [];
    let rvLayout = {};
    let rvConfig = {};
    {
      // Resources for future reference:
      // * https://plotly.com/javascript/reference/
      // * https://plotly.com/javascript/plotlyjs-function-reference/

      // Parameters
      const diagramWidth = AU.plotWidth(this.props.designSize);
      const shadedColor = 'beige';  // #F5F5DC
      const delta = 5 / 100;        // COMPETITIVE - Relaxed range = 0.5 +/– 0.05

      // Traces for R wins & D wins points

      // Set district marker size between 1–12 px, based on the # of districts
      const N = this.profile.byDistrict.length;
      const W = diagramWidth * (2 / 3);
      const markerSize = Math.min(Math.max(1, Math.round(W / N)), 12);

      const { rWinVfs, rWinRanks, rWinLabels, dWinVfs, dWinRanks, dWinLabels, minVf, maxVf } = this.extractRVGraphData();

      const districtHoverTemplate = 'District %{text}<br>%{y:5.2%}<extra></extra>';
      const repWinTrace = {
        x: rWinRanks,
        y: rWinVfs,
        mode: 'markers',
        type: 'scatter',
        text: rWinLabels,
        marker: {
          color: red,
          symbol: 'square',
          size: markerSize
        },
        hovertemplate: districtHoverTemplate,
        showlegend: false
      };

      const demWinTrace = {
        x: dWinRanks,
        y: dWinVfs,
        mode: 'markers',
        type: 'scatter',
        text: dWinLabels,
        marker: {
          color: blue,
          symbol: 'square',
          size: markerSize
        },
        hovertemplate: districtHoverTemplate,
        showlegend: false
      };

      // Traces for the "competitive" region

      const hr50PlusTrace = {
        x: [0.0, 1.0],
        y: [0.5 + delta, 0.5 + delta],
        fill: 'tonexty',
        fillcolor: shadedColor,
        type: 'scatter',
        name: 'Competitive range',
        text: 'competitive',
        mode: 'lines',
        line: {
          color: shadedColor,
          width: 0.5
        },
        hoverinfo: 'none',
        showlegend: true
      };

      const hr50Trace = {
        x: [0.0, 1.0],
        y: [0.5, 0.5],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: 'black',
          width: 1
        },
        hoverinfo: 'none',
        showlegend: false
      };

      const hr50MinusTrace = {
        x: [0.0, 1.0],
        y: [0.5 - delta, 0.5 - delta],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: shadedColor,
          width: 0.5
        },
        hoverinfo: 'none',
        showlegend: false
      };
      
      // Traces for statewide vote share and average D & R win percentages

      const nPts = 20;
      const ruleXs = [...Array(nPts + 1).keys()].map(x => ((100 / nPts) * x) / 100);

      /// EDITED ///
      const statewideVf = this.profile.statewide;
      const avgDWin = this.scorecard.averageDVf;
      const avgRWin = this.scorecard.averageRVf;
      const invertedAvgRWin = 1.0 - avgRWin;

      const statewideVfYs = [...Array(nPts + 1).keys()].map(x => statewideVf);
      const statewideVfWinHoverLabel = 'Total D vote: ' + AU.formatNumber(statewideVf, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
      const statewideVfTrace = {
        x: ruleXs,
        y: statewideVfYs,
        type: 'scatter',
        mode: 'lines',
        name: statewideVfWinHoverLabel,  // 'Statewide D vote %',
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

      const vrRuleHeight = 0.10;
      const invertedPRSfXs = [(1.0 - statewideVf), (1.0 - statewideVf)];
      const prSfYs = [statewideVf - vrRuleHeight, statewideVf + vrRuleHeight];
      const proportionalSfTrace = {
        x: invertedPRSfXs,
        y: prSfYs,
        type: 'scatter',
        mode: 'lines',
        line: {
          color: 'black',
          width: 1,
          dash: 'dashdot'
        },
        hoverinfo: 'none',
        showlegend: false
      };

      const avgDWinYs = [...Array(nPts + 1).keys()].map(x => avgDWin);
      const avgDWinHoverLabel = 'Average D win: ' + AU.formatNumber(avgDWin, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
      const avgDWinTrace = {
        x: ruleXs,
        y: avgDWinYs,
        type: 'scatter',
        mode: 'lines',
        name: avgDWinHoverLabel, // 'Average D win %',
        line: {
          color: blue,
          width: 0.5,
          dash: 'dot'
        },
        text: avgDWinHoverLabel,
        hoverinfo: 'text',
        hoveron: 'points',
        showlegend: true
      };

      const avgRWinYs = [...Array(nPts + 1).keys()].map(x => avgRWin);
      const avgRWinHoverLabel = 'Average R win: ' + AU.formatNumber(invertedAvgRWin, AU.Units.Percentage) + AU.unitsSymbol(AU.Units.Percentage);
      const avgRWinTrace = {
        x: ruleXs,
        y: avgRWinYs,
        type: 'scatter',
        mode: 'lines',
        name: avgRWinHoverLabel,  // 'Average R win %',
        line: {
          color: red,
          width: 0.5,
          dash: 'dot'
        },
        text: avgRWinHoverLabel,
        hoverinfo: 'text',
        hoveron: 'points',
        showlegend: true
      };

      // NOTE - The order is important!
      rvTraces.push(hr50MinusTrace);
      rvTraces.push(hr50PlusTrace);
      rvTraces.push(hr50Trace);
      rvTraces.push(proportionalSfTrace);
      rvTraces.push(statewideVfTrace);
      if (avgDWin)
        rvTraces.push(avgDWinTrace);
      if (avgRWin)
        rvTraces.push(avgRWinTrace);
      if (rWinVfs.length > 0)
        rvTraces.push(repWinTrace);
      if (dWinVfs.length > 0)
        rvTraces.push(demWinTrace);

      // If declination is defined, add traces for the R points & line, the D points
      // & lines, and the extension of the R line.
      const decl = this.scorecard.bias.decl;
      if (decl)
      {
        const X = 0; const Y = 1;

        const { Sb, Ra, Rb, Va, Vb } = this.scorecard.bias.rvPoints;

        // Convert R vote shares (used in dra-score for 'decl') to D vote shares
        const rDeclPt = [(1 - Ra), (1 - Va)];
        const dDeclPt = [(1 - Rb), (1 - Vb)];
        const pivotDeclPt = [(1 - Sb), 0.5];

        // Make traces for the R & D line segments and the pivot point

        const rDeclXs = [rDeclPt[X], pivotDeclPt[X]];
        const rDeclYs = [rDeclPt[Y], pivotDeclPt[Y]];
        const dDeclXs = [pivotDeclPt[X], dDeclPt[X]];
        const dDeclYs = [pivotDeclPt[Y], dDeclPt[Y]];
        const pivotDeclXs = [pivotDeclPt[X]];
        const pivotDeclYs = [pivotDeclPt[Y]];

        const rDeclTrace = {
          x: rDeclXs,
          y: rDeclYs,
          mode: 'lines',
          type: 'scatter',
          line: {
            color: 'black',
            width: 1
          },
          hoverinfo: 'none',
          showlegend: false
        };
        rvTraces.push(rDeclTrace);

        const dDeclTrace = {
          x: dDeclXs,
          y: dDeclYs,
          mode: 'lines',
          type: 'scatter',
          line: {
            color: 'black',
            width: 1
          },
          hoverinfo: 'none',
          showlegend: false
        };
        rvTraces.push(dDeclTrace);

        const pivotPtLabel = AU.formatNumber(decl, AU.Meta.decl.units) + AU.unitsSymbol(AU.Meta.decl.units);
        const pivotPtHoverTemplate = pivotPtLabel + '<extra></extra>';
        const pivotPtTrace = {
          x: pivotDeclXs,
          y: pivotDeclYs,
          mode: 'markers',
          type: 'scatter',
          name: 'Declination: ' + pivotPtLabel,
          marker: {
            color: 'white',
            symbol: 'circle',
            size: 10,
            line: {
              color: 'black',
              width: 2
            }
          },
          hovertemplate: pivotPtHoverTemplate,
          showlegend: true
        };

        // Make the dotted line extension of the R trace, if decl is significant
        const declThreshold = 5;  // degrees

        if (Math.abs(decl) > declThreshold) 
        {
          const rDy = (pivotDeclPt[Y] - rDeclPt[Y]);
          const rDx = (pivotDeclPt[X] - rDeclPt[X]);
          const dDy = (dDeclPt[Y] - pivotDeclPt[Y]);
          const dDx = (dDeclPt[X] - pivotDeclPt[X]);

          const slope = rDy / rDx;

          const dDistance = distance([pivotDeclPt[X], pivotDeclPt[Y]], [dDeclPt[X], dDeclPt[Y]]);
          const rDistance = distance([rDeclPt[X], rDeclPt[Y]], [pivotDeclPt[X], pivotDeclPt[Y]]);
          const ratio = dDistance / rDistance;

          const beyondPt = [
            pivotDeclPt[X] + (ratio * rDx),
            pivotDeclPt[Y] + (ratio * rDy)
          ];

          const beyondDeclXs = [pivotDeclPt[X], beyondPt[X]];
          const beyondDeclYs = [pivotDeclPt[Y], beyondPt[Y]];

          const dottedDeclTrace = {
            x: beyondDeclXs,
            y: beyondDeclYs,
            mode: 'lines',
            type: 'scatter',
            line: {
              color: 'black',
              width: 1,
              dash: 'dash'
            },
            hoverinfo: 'none',
            showlegend: false
          };
          rvTraces.push(dottedDeclTrace);
        }

        // Add the pivot point *after* a potential dotted line, so that it's on "top"
        rvTraces.push(pivotPtTrace);
      }

      // The r(v) plot layout

      const rankRange = [0.0, 1.0];
      const vfRange = [
        Math.max(minVf - 0.025, 0.0),
        Math.min(maxVf + 0.025, 1.0)
      ];

      const heightPct = (vfRange[1] - vfRange[0]);
      const diagramHeight = ((heightPct * diagramWidth) > 450) ? 700 : 450;

      const X = 0;
      const Y = 1;
      const lowerRight = [0.67, 0];
      const upperLeft = [0.02, 0.85];
      let legendPosition = upperLeft;
      if (decl)
      {
        if (decl < 0) legendPosition = lowerRight;
      }
      else  // 'decl' undefined
      {
        // If there are 5 or more districts and 'decl' is undefined, then the 
        // result was/is a sweep for one party or the other.
        const bSweep = (N >= 5) ? true : false;

        if ((!bSweep) && (rWinRanks.length > dWinRanks.length)) legendPosition = lowerRight;
      }
      // const legendPosition = (dWinRanks.length > rWinRanks.length) ? lowerRight : upperLeft;

      rvLayout = {
        title: 'Rank-Votes Graph: ' + name,
        // autosize: true,        // Explored setting this to 'true'
        width: diagramWidth,
        height: diagramHeight,
        xaxis: {
          title: 'District',
          range: rankRange,       // Explored removing this
          // domain: [0.0, 1.0],  // Explored adding this instead
          showgrid: false,
          zeroline: false,
          // fixedrange: true,    // Removed this, zoom maintains aspect ratio
          showticklabels: false
        },
        yaxis: {
          title: "D Vote %",
          range: vfRange,
          scaleanchor: 'x',       // Explored removing this
          scaleratio: 1,          // Explored removing this
          // constrain: "range",  // Explored adding this
          // automargin: true,    // Explored adding this
          showgrid: true,
          zeroline: false,
          tickformat: '%{y:5.2%}'
        },
        dragmode: 'zoom',
        hovermode: 'closest',
        showlegend: bLegend,
        legend: {
          x: legendPosition[X],
          y: legendPosition[Y],
          // traceorder="normal",
          // font=dict(
          //     family="sans-serif",
          //     size=12,
          //     color="black"
          // ),
          // bgcolor="LightSteelBlue",
          bordercolor: 'black',
          borderwidth: 1
        },
        paper_bgcolor: bgcolor,
        plot_bgcolor: bgcolor
      };

      // Configure hover menu options & behavior

      rvConfig = {
        toImageButtonOptions: {
          format: 'png', // one of png, svg, jpeg, webp
          filename: 'r(v)-graph'
        },
        // Remove the unwanted plotly hover commands. Let users pan & zoom.
        modeBarButtonsToRemove: ['zoom2d', 'select2d', 'lasso2d', 'autoScale2d', 'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian'],
        scrollZoom: true,         // Helps w/ lots of districts
        displayModeBar: true,     // Always show the download icon
        displaylogo: false,
        responsive: true
      };
      Plotly.newPlot('rank-vote-graph', rvTraces, rvLayout, rvConfig);
      this.setState({rvDirty: false});
    }
  }
  
"""
