#!/bin/bash
#
# Analyze partisan profiles for NC
#
# $ scripts/analyze_profiles_NC.sh

echo
echo "Analyzing partisan profiles ..."
echo

cd data
cd NC

~/dev/dra-analytics/cli/partisan.js -i NC2022-composite-profile.json -j > NC2022-composite-analytics.json
~/dev/dra-analytics/cli/partisan.js -i NC2022-P2020-profile.json -j > NC2022-P2020-analytics.json
~/dev/dra-analytics/cli/partisan.js -i NC2022-P2016-profile.json -j > NC2022-P2016-analytics.json
~/dev/dra-analytics/cli/partisan.js -i NC2022-S2020-profile.json -j > NC2022-S2020-analytics.json
~/dev/dra-analytics/cli/partisan.js -i NC2022-S2016-profile.json -j > NC2022-S2016-analytics.json
~/dev/dra-analytics/cli/partisan.js -i NC2022-G2020-profile.json -j > NC2022-G2020-analytics.json
~/dev/dra-analytics/cli/partisan.js -i NC2022-AG2020-profile.json -j > NC2022-AG2020-analytics.json

cd ../..

echo
echo "... finished."
echo
