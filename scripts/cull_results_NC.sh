#!/bin/bash
#
# Cull analytics for NC
#
# $ scripts/cull_results_NC.sh

echo
echo "Culling analytics results ..."
echo

cd data
cd NC

../../scripts/cull_results.py NC 2022 composite
# ../../scripts/make_profile.py NC 2022 P2020
# ../../scripts/make_profile.py NC 2022 P2016
# ../../scripts/make_profile.py NC 2022 S2020
# ../../scripts/make_profile.py NC 2022 S2016
# ../../scripts/make_profile.py NC 2022 G2020
# ../../scripts/make_profile.py NC 2022 AG2020

cd ../..

echo
echo "... finished."
echo
