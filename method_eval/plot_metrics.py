#!/usr/bin/env python3

"""
PLOT METRICS

"""

import matplotlib.pyplot as plt


def plot_metrics(data, metrics):
    composites = []
    means = []
    mean_errs = []

    for _, m in enumerate(data["metrics"]):
        name = m["METRIC"]
        if name in metrics:
            composites.append(m["composite"])
            means.append(m["MEAN"])
            err = m["SEM"] * 2
            mean_errs.append([m["MEAN"] - err, m["MEAN"] + err])
        else:
            continue

    # Reverse the lists, so metrics plot in the correct top-to-bottom order.
    metrics.reverse()
    means.reverse()
    mean_errs.reverse()
    composites.reverse()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title(data["name"])

    for i, m in enumerate(metrics):
        ax1.plot(mean_errs[i], [m, m], color="black")
    ax1.scatter(means, metrics, marker="|", color="black")
    ax1.scatter(
        composites,
        metrics,
        marker="x",
        color="black"
        # marker="s",
        # color="white",
        # edgecolors="black",
    )

    plt.show()
