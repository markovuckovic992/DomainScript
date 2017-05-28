#!/bin/sh

if [ $5 ]
then
	tmp=`grep -i $2 $1 | grep -i $3 | grep -i $4 | grep -i $5`
elif [ $4 ]
then
	tmp=`grep -i $2 $1 | grep -i $3 | grep -i $4`
elif [ $3 ]
then
	tmp=`grep -i $2 $1 | grep -i $3`
else
	tmp=`grep -i $2 $1`
fi

echo $tmp