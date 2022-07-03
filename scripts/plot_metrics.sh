#!/bin/bash
#
# Plot the metrics curve for a given map:
#
# For example:
#
# $ scripts/plot_metrics.sh NC 2022 main
# $ scripts/plot_metrics.sh NC 2022 responsiveness <<< NOT USED
# $ scripts/plot_metrics.sh NC 2022 VS             <<< NOT USED
#

xx=$1
yy=$2
which=$3

echo
echo Plotting $which metrics for: $xx $yy
echo

cd data
cd $xx

../../scripts/plot_metrics.py $xx $yy $which

cd ../..

echo
echo ... done.
echo
