#!/bin/bash
#
# Analyze partisan profiles for a map
#
# $ scripts/analyze_map.sh AL 2022 P2020 P2016 S2020 S2017 G2018 AG2018
#
# $ scripts/analyze_map.sh NC 2022 P2020 P2016 S2020 S2016 G2020 AG2020

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

echo ... running analytics on the profiles ...

~/dev/dra-analytics/cli/partisan.js -i $xx$yy-composite-profile.json -j > $xx$yy-composite-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i $xx$yy-$e1-profile.json -j > $xx$yy-$e1-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i $xx$yy-$e2-profile.json -j > $xx$yy-$e2-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i $xx$yy-$e3-profile.json -j > $xx$yy-$e3-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i $xx$yy-$e4-profile.json -j > $xx$yy-$e4-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i $xx$yy-$e5-profile.json -j > $xx$yy-$e5-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i $xx$yy-$e6-profile.json -j > $xx$yy-$e6-scorecard.json

echo ... culling the results ...

../../scripts/cull_results.py $xx $yy composite -v
../../scripts/cull_results.py $xx $yy $e1
../../scripts/cull_results.py $xx $yy $e2
../../scripts/cull_results.py $xx $yy $e3
../../scripts/cull_results.py $xx $yy $e4
../../scripts/cull_results.py $xx $yy $e5
../../scripts/cull_results.py $xx $yy $e6

cd ../..

echo
echo ... done.
echo
