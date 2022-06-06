#!/bin/bash
#
# Analyze partisan profiles for a map
#
# $ scripts/analyze_map.sh AL 2022 P2020 P2016 S2020 S2017 G2018 AG2018
# $ scripts/analyze_map.sh AR 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh AZ 2022 P2020 P2016 S2020 S2018 G2018 AG2018
# $ scripts/analyze_map.sh CA 2022 P2020 P2016             G2018 AG2018 <<< SKIP: No Senatorial elections.
# $ scripts/analyze_map.sh CO 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh CT 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<< 'About Data' wrong re: P?
# $ scripts/analyze_map.sh FL 2022 P2020 P2016 S2018 S2016 G2018 AG2018
# $ scripts/analyze_map.sh GA 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh HI 2022 P2020 P2016 S2018 S2016 G2018        <<< SKIP: No AG election! Only two districts.
# $ scripts/analyze_map.sh IA 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh ID 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh IL 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh IN 2022 P2020 P2016 S2018 S2016 G2020 AG2020

# $ scripts/analyze_map.sh KS 2022 P2020 P2016 S2020 S2016 G2018 AG2018
# $ scripts/analyze_map.sh KY 2022       P2016 S2016       G2019 AG2019 <<< SKIP: Only one Senate election & P2012 not accessible!
# $ scripts/analyze_map.sh LA 2022 P2020 P2016 S2020 S2016 G2019 AG2019 <<< NOTE: Not runoff G2019 but runoff S2016.
# $ scripts/analyze_map.sh MA 2022 P2020 P2016 S2020 S2018 G2018 AG2018
# $ scripts/analyze_map.sh MD 2022 P2020 P2016 S2018 S2016 G2018 AG2018
# $ scripts/analyze_map.sh ME 2022 P2020 P2016 S2020       G2018        <<< TODO: S2018 not *'d. No AG election.
# $ scripts/analyze_map.sh MI 2022 P2020 P2016 S2020 S2018 G2018 AG2018
# $ scripts/analyze_map.sh MN 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<< TODO: Which S2018?
# $ scripts/analyze_map.sh MO 2022 P2020 P2016 S2018 S2016 G2020 AG2020
# $ scripts/analyze_map.sh MS 2022 P2020 P2016 S2020 S2018 G2019 AG2019 <<< TODO: Which S2018?
#
# $ scripts/analyze_map.sh MT 2022 P2020 P2016 S2020 S2018 G2020 AG2020
# $ scripts/analyze_map.sh NC 2022 P2020 P2016 S2020 S2016 G2020 AG2020 <<< DONE
# $ scripts/analyze_map.sh NE 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<< TODO: AG2018 not *'d.
# $ scripts/analyze_map.sh NH 2022 P2020 P2016 S2020 S2016 G2020        <<< SKIP: No AG election! Only two districts.
# $ scripts/analyze_map.sh NJ 2022 P2020 P2016 S2020 S2018 G2017        <<< TODO: No AG election. 
# $ scripts/analyze_map.sh NM 2022 P2020 P2016 S2020 S2018 G2018 AG2018
#
# AK, DE, ND, SD, VT, and WY each have only one congressional district.

# TODO: inventory map share links

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

echo ... combining S-V points ...

paste -d "," $xx$yy-composite-s(v)-points.csv $xx$yy-$e1-s(v)-points.csv $xx$yy-$e2-s(v)-points.csv $xx$yy-$e3-s(v)-points.csv $xx$yy-$e4-s(v)-points.csv $xx$yy-$e5-s(v)-points.csv $xx$yy-$e6-s(v)-points.csv > $xx$yy-s(v)-points.csv
paste -d "," $xx$yy-composite-v(i)-points.csv $xx$yy-$e1-v(i)-points.csv $xx$yy-$e2-v(i)-points.csv $xx$yy-$e3-v(i)-points.csv $xx$yy-$e4-v(i)-points.csv $xx$yy-$e5-v(i)-points.csv $xx$yy-$e6-v(i)-points.csv > $xx$yy-v(i)-points.csv

cd ../..

echo
echo ... done.
echo
