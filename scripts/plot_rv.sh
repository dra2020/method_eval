#!/bin/bash
#
# Plot the r(v) graph for a given map:
#
# For example:
#
# $ scripts/plot_rv.sh NC 2022
# $ scripts/plot_rv.sh IL 2022
# $ scripts/plot_rv.sh SC 2022
#

xx=$1
yy=$2

echo
echo Plotting rank-votes curve for: $xx $yy
echo

cd data
cd $xx

../../scripts/plot_rv.py $xx $yy

cd ../..

echo
echo ... done.
echo
