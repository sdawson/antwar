#!/bin/sh
# Run a large (1000?) number of ant simulations and write the results to a single file

filename="antsim-`date "+%Y%m%d%H%M"`.out"

unamestr=`uname`

touch $filename
echo "10x10 grid, p = 0.43, f = 0.02, 1000 steps" >> $filename
echo -e "Ma D\tMi D\ts+\ts-" >> $filename

for i in `eval echo {1..1000}`
do
  if [ "$unamestr" = Linux ]
  then
    echo "running simulation $i..."
    python2 antwar.py 10 .43 .02 1000 >> $filename
  elif [ "$unamestr" = Darwin ]
  then
    echo "running simulation $i..."
    python antwar.py 10 .43 .02 1000 >> $filename
  fi
done
echo "Output in: $filename"
