#!/bin/bash
#
# Plot the metrics curve for a given map:
#
# For example:
#
# $ scripts/plot_metrics.sh NC 2022
# $ scripts/plot_metrics.sh IL 2022
# $ scripts/plot_metrics.sh SC 2022
#

xx=$1
yy=$2

echo
echo Plotting metrics for: $xx $yy
echo

cd data
cd $xx

../../scripts/plot_metrics.py $xx $yy

cd ../..

echo
echo ... done.
echo
