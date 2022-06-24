#!/bin/bash
#
# Plot the S(V) curve for a given map:
#
# For example:
#
# $ scripts/plot_sv.sh NC 2022
# $ scripts/plot_sv.sh IL 2022
# $ scripts/plot_sv.sh SC 2022
#

xx=$1
yy=$2

echo
echo Plotting seats-votes curve for: $xx $yy
echo

cd data
cd $xx

../../scripts/plot_sv.py $xx $yy

cd ../..

echo
echo ... done.
echo
