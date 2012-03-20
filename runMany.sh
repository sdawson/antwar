#!/bin/sh
# Run a large (1000?) number of ant simulations and write the results to a single file

p=0.43
f=0.02
steps=500
size=20
filename="antsim-p$p-f$f-steps$steps-size$size-`date "+%Y%m%d%H%M"`.out"

unamestr=`uname`

touch $filename
echo "${size}x$size grid, p = $p, f = $f, $steps steps" >> $filename
echo -e "Ma D\tMi D\tRed D\t Blue D\ts+\ts-" >> $filename

for i in `eval echo {1..1000}`
do
  if [ "$unamestr" = Linux ]
  then
    echo "running simulation $i..."
    python2 antwar.py $size $p $f $steps >> $filename
  elif [ "$unamestr" = Darwin ]
  then
    echo "running simulation $i..."
    python antwar.py $size $p $f $steps >> $filename
  fi
done
echo "Output in: $filename"
