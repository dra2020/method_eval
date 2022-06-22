#!/bin/bash
#
# $ scripts/test.sh IL 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<<
# $ scripts/test.sh NC 2022 P2020 P2016 S2020 S2016 G2020 AG2020 <<<
# $ scripts/test.sh SC 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<<

xx=$1
yy=$2
e1=$3
e2=$4
e3=$5
e4=$6
e5=$7
e6=$8

echo
echo Analyzing $xx $yy for: composite $e1 $e2 $e3 $e4 $e5 $e6
echo

cd data
cd $xx

echo ... converting "District Abstracts" to partisan profiles ...

../../scripts/make_profile.py $xx $yy composite
../../scripts/make_profile.py $xx $yy $e1
../../scripts/make_profile.py $xx $yy $e2
../../scripts/make_profile.py $xx $yy $e3
../../scripts/make_profile.py $xx $yy $e4
../../scripts/make_profile.py $xx $yy $e5
../../scripts/make_profile.py $xx $yy $e6

cd ../..

echo
echo ... done.
echo
