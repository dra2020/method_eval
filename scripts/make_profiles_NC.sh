#!/bin/bash
#
# Make partisan profiles for NC
#
# $ scripts/make_profiles_NC.sh

echo
echo "Making partisan profiles ..."
echo

cd data
cd NC

../../scripts/make_profile.py NC 2022 composite
../../scripts/make_profile.py NC 2022 P2020
../../scripts/make_profile.py NC 2022 P2016
../../scripts/make_profile.py NC 2022 S2020
../../scripts/make_profile.py NC 2022 S2016
../../scripts/make_profile.py NC 2022 G2020
../../scripts/make_profile.py NC 2022 AG2020

cd ../..

echo
echo "... finished."
echo
