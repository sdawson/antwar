#!/bin/sh
# Run a large (1000?) number of ant simulations and write the results to a single file

filename="antsim-`date "+%Y%m%d%H%M"`.out"

touch $filename
echo "10x10 grid, p = 0.03, f = 0.21, 1000 steps" >> $filename
echo -e "Ma D\tMi D\ts+\ts-" >> $filename

for i in `seq 1 1000`
do
  echo "running simulation $i..."
  python2 antwar.py 10 .03 .21 1000 >> $filename
done
echo "Output in: $filename"
