#!/bin/sh
# Run multiple rounds of the simulation to determine how fast the grid becomes 
# one colour.

p=0.21
rf=0.025
bf=0.04
steps=1000
size=30
print="noprint"

unamestr=`uname`

#filename="antsim-p$p-rf$rf-bf$bf-steps$steps-size$size-`date "+%Y%m%d%H%M"`.out"
#touch $filename
#echo "${size}x$size grid, p = $p, redf = $rf, bluef = $bf, $steps steps" >> $filename
for i in `eval echo {1..10}`
do
  if [ "$unamestr" = Linux ]
  then
    echo "running simulation $i..."
    python2 antwar.py $size $p $rf $bf $steps $print
  elif [ "$unamestr" = Darwin ]
  then
    echo "running simulation $i..."
    python $python $size $p $rf $bf $steps $print
  fi
done
