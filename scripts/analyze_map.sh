#!/bin/bash
#
# Analyze a redistricting map:
# - This isn't the most elegant script, but it works.
# - It essentially automates what would otherwise be a manual workflow 
# - starting with a district abstract export from DRA, and
# - then creating a partisan profile, running analytics on it, and
# - finally producing statistics files for metrics, the S(V) curve & r(v) points, and 
# - district-by-district vote shares.
#
# Sample states:
#
# scripts/analyze_map.sh AL 2022 P2020 P2016 S2020 S2017 G2018 AG2018 <<<
# scripts/analyze_map.sh AR 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<< DONE - LO & DECL undefined for all
# scripts/analyze_map.sh AZ 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<<
# scripts/analyze_map.sh CO 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<<
# scripts/analyze_map.sh CT 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<< LO & DECL undefined for all
# scripts/analyze_map.sh FL 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<<
# scripts/analyze_map.sh GA 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<<
# scripts/analyze_map.sh IL 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<< DONE
# scripts/analyze_map.sh IN 2022 P2020 P2016 S2018 S2016 G2020 AG2020 <<< 
# scripts/analyze_map.sh KS 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<< LO & DECL undefined for all
# scripts/analyze_map.sh LA 2022 P2020 P2016 S2020 S2016 G2019 AG2019 <<<  
# scripts/analyze_map.sh MA 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<< LO & DECL undefined for all
# scripts/analyze_map.sh MD 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<<
# scripts/analyze_map.sh MI 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<< 
# scripts/analyze_map.sh MN 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<<
# scripts/analyze_map.sh MO 2022 P2020 P2016 S2018 S2016 G2020 AG2020 <<<
# scripts/analyze_map.sh MS 2022 P2020 P2016 S2020 S2018 G2019 AG2019 <<< LO & DECL undefined for all
# scripts/analyze_map.sh NC 2022 P2020 P2016 S2020 S2016 G2020 AG2020 <<< DONE
# scripts/analyze_map.sh NM 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<< LO & DECL undefined for all
# scripts/analyze_map.sh NV 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<< LO & DECL undefined for all
# scripts/analyze_map.sh NY 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<< LO & DECL undefined *sometimes*
# scripts/analyze_map.sh OH 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<<
# scripts/analyze_map.sh OK 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<< LO & DECL undefined for all
# scripts/analyze_map.sh OR 2022 P2020 P2016 S2020 S2016 G2018 AG2020 <<< LO & DECL undefined *sometimes*
# scripts/analyze_map.sh PA 2022 P2020 P2016 S2018 S2016 G2018 AG2020 <<<
# scripts/analyze_map.sh SC 2022 P2020 P2016 S2020 S2016 G2018 AG2018 <<< DONE
# scripts/analyze_map.sh TX 2022 P2020 P2016 S2020 S2018 G2018 AG2018 <<<
# scripts/analyze_map.sh WA 2022 P2020 P2016 S2018 S2016 G2020 AG2020 <<< 
# scripts/analyze_map.sh WI 2022 P2020 P2016 S2018 S2016 G2018 AG2018 <<<

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

~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-composite-profile.json -j > _$xx$yy-composite-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-$e1-profile.json -j > _$xx$yy-$e1-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-$e2-profile.json -j > _$xx$yy-$e2-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-$e3-profile.json -j > _$xx$yy-$e3-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-$e4-profile.json -j > _$xx$yy-$e4-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-$e5-profile.json -j > _$xx$yy-$e5-scorecard.json
~/dev/dra-analytics/cli/partisan.js -i _$xx$yy-$e6-profile.json -j > _$xx$yy-$e6-scorecard.json

echo ... culling the results ...

../../scripts/cull_results.py $xx $yy composite -v
../../scripts/cull_results.py $xx $yy $e1
../../scripts/cull_results.py $xx $yy $e2
../../scripts/cull_results.py $xx $yy $e3
../../scripts/cull_results.py $xx $yy $e4
../../scripts/cull_results.py $xx $yy $e5
../../scripts/cull_results.py $xx $yy $e6

echo ... districts implicitly sorted by id ...

echo ... combining individual election files ...

paste -d "," _$xx$yy-composite-metrics.csv _$xx$yy-$e1-metrics.csv _$xx$yy-$e2-metrics.csv _$xx$yy-$e3-metrics.csv _$xx$yy-$e4-metrics.csv _$xx$yy-$e5-metrics.csv _$xx$yy-$e6-metrics.csv > _$xx$yy-metrics-RAW.csv
paste -d "," _$xx$yy-composite-SV-points.csv _$xx$yy-$e1-SV-points.csv _$xx$yy-$e2-SV-points.csv _$xx$yy-$e3-SV-points.csv _$xx$yy-$e4-SV-points.csv _$xx$yy-$e5-SV-points.csv _$xx$yy-$e6-SV-points.csv > _$xx$yy-SV-points-RAW.csv
paste -d "," _$xx$yy-composite-vi-points-BY_CD.csv _$xx$yy-$e1-vi-points-BY_CD.csv _$xx$yy-$e2-vi-points-BY_CD.csv _$xx$yy-$e3-vi-points-BY_CD.csv _$xx$yy-$e4-vi-points-BY_CD.csv _$xx$yy-$e5-vi-points-BY_CD.csv _$xx$yy-$e6-vi-points-BY_CD.csv > _$xx$yy-vi-points-RAW.csv

cut -d "," -f 1,2,4,6,8,10,12,14 _$xx$yy-metrics-RAW.csv > _$xx$yy-metrics.csv
cut -d "," -f 1,2,4,6,8,10,12,14 _$xx$yy-SV-points-RAW.csv > _$xx$yy-SV-points.csv
cut -d "," -f 1,2,4,6,8,10,12,14 _$xx$yy-vi-points-RAW.csv > _$xx$yy-vi-points-UNSORTED.csv

echo ... sort districts by v_i ...

../../scripts/sort_csv.sh _$xx$yy-vi-points-UNSORTED.csv _$xx$yy-vi-points.csv

echo ... calculating statistics ...

../../scripts/calc_stats.py $xx $yy metrics str
../../scripts/calc_stats.py $xx $yy SV-points float
../../scripts/calc_stats.py $xx $yy vi-points int

echo ... pickling plot data ...

../../scripts/recombine_data.py $xx $yy

cd ../..

echo
echo ... done.
echo
