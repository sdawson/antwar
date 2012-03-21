#!/bin/sh
# Run a large (1000?) number of ant simulations and write the results to a single file

p=0.7
f=0.7
rf=0.4
bf=0.2
steps=500
size=20
python=$1

unamestr=`uname`

if [ "$python" = "diffbirth.py" ]
then
  filename="antsim-p$p-rf$rf-bf$bf-steps$steps-size$size-`date "+%Y%m%d%H%M"`.out"
  touch $filename
  echo "${size}x$size grid, p = $p, redf = $rf, bluef = $bf, $steps steps" >> $filename
  echo -e "Ma D\tMi D\tRed D\t Blue D\tred s+\tblue s+\ts-" >> $filename
  for i in `eval echo {1..500}`
  do
    if [ "$unamestr" = Linux ]
    then
      echo "running simulation $i..."
      python2 $python $size $p $rf $bf $steps >> $filename
    elif [ "$unamestr" = Darwin ]
    then
      echo "running simulation $i..."
      python $python $size $p $rf $bf $steps >> $filename
    fi
  done
echo "Output in: $filename"
elif [ "$python" = "antwar.py" ]
then
  filename="antsim-p$p-f$f-steps$steps-size$size-`date "+%Y%m%d%H%M"`.out"
  touch $filename
  echo "${size}x$size grid, p = $p, f = $f, $steps steps" >> $filename
  echo -e "Ma D\tMi D\tRed D\t Blue D\ts+\ts-" >> $filename
  for i in `eval echo {1..500}`
  do
    if [ "$unamestr" = Linux ]
    then
      echo "running simulation $i..."
      python2 $python $size $p $f $steps >> $filename
    elif [ "$unamestr" = Darwin ]
    then
      echo "running simulation $i..."
      python $python $size $p $f $steps >> $filename
    fi
  done
echo "Output in: $filename"
fi
