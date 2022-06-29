#!/usr/bin/env python3
#
# PLOT METRICS (MANUAL)
#
# For states like SC that have missing DECL and/or LO metrics,
# - Fix up the metrics.csv by hand, and
# - Then run this script in sandbox.py at top-level.
#

from method_eval import *

xx = "SC"
year = "2022"

in_path = "data/" + xx + "/" + xx + year + "-" + "metrics-REVISED" + ".csv"
types = [str] + [float] * 11

metrics = read_typed_csv(in_path, types)

metrics_data = {}
metrics_data["metrics"] = metrics
metrics_data["name"] = xx + " " + year + " Congress"

plot_metrics(metrics_data)
# plot_metrics(metrics_data, normalize=True)
