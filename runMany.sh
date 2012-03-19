#!/bin/sh
# Run a large (1000?) number of ant simulations and write the results to a single file

filename="antsim-`date "+%Y%m%d%H%M"`.out"

touch $filename
for i in `seq 1 1000`:
  echo "Ma D\tMi D\ts+\ts-" >> $filename
  python2 antwar.py 10 .5 .25 10000 >> $filename
