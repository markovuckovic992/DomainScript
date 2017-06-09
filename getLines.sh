#!/bin/sh

if [ $4 ]
then
	regex=$2'|'$3'|'$4
	tmp=`egrep -i $regex $1`
elif [ $3 ]
then
	regex=$2'|'$3
	tmp=`egrep -i $regex $1`
else
	tmp=`grep -i $2 $1`
fi
echo $tmp


