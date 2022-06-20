#!/bin/bash
#
# Plot the S(V) curve for a given map:
#
# For example:
#
# $ scripts/plot_sv.sh NC 2022
#

xx=$1
yy=$2

echo
echo Plotting seats-votes curve for: $xx $yy
echo

cd analysis
cd $xx

../../scripts/plot_sv.py $xx $yy

cd ../..

echo
echo ... done.
echo
