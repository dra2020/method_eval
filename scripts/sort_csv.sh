#!/bin/bash

# Sort a .csv file with a first row of field names on the *second* field.
# 
# For example:
#
# sort_csv.sh input.csv output.csv

echo "Sorting ..."
head -n 1 $1 > $2 &&
tail -n +2 $1 | sort -t "|" -k 2,2 >> $2

echo "... done."
