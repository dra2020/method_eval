#!/usr/bin/env python3

"""
PLOT METRICS

"""

import matplotlib.pyplot as plt


def plot_metrics(data, set):
    metrics = []
    if set == "main":
        metrics = ["EG", "PR", "GAMMA", "BS_50", "BV_50", "BS_V", "GS", "MM", "LO"]
    elif set == "responsiveness":
        metrics = ["R", "r"]
    elif set == "VS":
        metrics = ["Vf", "Sf"]

    normalize = True if set == "responsiveness" else False

    composites = []
    means = []
    mean_errs = []

    for _, m in enumerate(data["metrics"]):
        name = m["METRIC"]
        base = m["MEAN"] if normalize else 1
        if name in metrics:
            composites.append(m["composite"] / base)
            means.append(m["MEAN"] / base)
            err = m["SEM"] * 2
            mean_errs.append([(m["MEAN"] - err) / base, (m["MEAN"] + err) / base])
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
