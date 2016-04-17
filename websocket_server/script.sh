#!/bin/bash

#echo '$#:' $#
#echo '$@:' $@
#echo '$1:' $1
#echo '$2:' $2


for i in `seq 0 5`
do
    echo "[$@]: $i"
    sleep 1
done

all=($@)
len=${#all[@]}
((len--))

eval ${all[@]:0:len}
