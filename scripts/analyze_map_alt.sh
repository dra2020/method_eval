#!/bin/bash
#
# Alternate version of analyze_map.sh which sorts districts by v_i vs. id.
#

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

echo ... sort districts by v_i ...

../../scripts/sort_csv.sh _$xx$yy-composite-vi-points-BY_CD.csv _$xx$yy-composite-vi-points-BY_vi.csv
../../scripts/sort_csv.sh _$xx$yy-$e1-vi-points-BY_CD.csv _$xx$yy-$e1-vi-points-BY_vi.csv
../../scripts/sort_csv.sh _$xx$yy-$e2-vi-points-BY_CD.csv _$xx$yy-$e2-vi-points-BY_vi.csv
../../scripts/sort_csv.sh _$xx$yy-$e3-vi-points-BY_CD.csv _$xx$yy-$e3-vi-points-BY_vi.csv
../../scripts/sort_csv.sh _$xx$yy-$e4-vi-points-BY_CD.csv _$xx$yy-$e4-vi-points-BY_vi.csv
../../scripts/sort_csv.sh _$xx$yy-$e5-vi-points-BY_CD.csv _$xx$yy-$e5-vi-points-BY_vi.csv
../../scripts/sort_csv.sh _$xx$yy-$e6-vi-points-BY_CD.csv _$xx$yy-$e6-vi-points-BY_vi.csv

echo ... combining individual election files ...

paste -d "," _$xx$yy-composite-metrics.csv _$xx$yy-$e1-metrics.csv _$xx$yy-$e2-metrics.csv _$xx$yy-$e3-metrics.csv _$xx$yy-$e4-metrics.csv _$xx$yy-$e5-metrics.csv _$xx$yy-$e6-metrics.csv > _$xx$yy-metrics-RAW.csv
paste -d "," _$xx$yy-composite-SV-points.csv _$xx$yy-$e1-SV-points.csv _$xx$yy-$e2-SV-points.csv _$xx$yy-$e3-SV-points.csv _$xx$yy-$e4-SV-points.csv _$xx$yy-$e5-SV-points.csv _$xx$yy-$e6-SV-points.csv > _$xx$yy-SV-points-RAW.csv
paste -d "," _$xx$yy-composite-vi-points-BY_vi.csv _$xx$yy-$e1-vi-points-BY_vi.csv _$xx$yy-$e2-vi-points-BY_vi.csv _$xx$yy-$e3-vi-points-BY_vi.csv _$xx$yy-$e4-vi-points-BY_vi.csv _$xx$yy-$e5-vi-points-BY_vi.csv _$xx$yy-$e6-vi-points-BY_vi.csv > _$xx$yy-vi-points-RAW.csv

cut -d "," -f 1,2,4,6,8,10,12,14 _$xx$yy-metrics-RAW.csv > _$xx$yy-metrics.csv
cut -d "," -f 1,2,4,6,8,10,12,14 _$xx$yy-SV-points-RAW.csv > _$xx$yy-SV-points.csv
cut -d "," -f 1,2,4,6,8,10,12,14 _$xx$yy-vi-points-RAW.csv > _$xx$yy-vi-points.csv

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
