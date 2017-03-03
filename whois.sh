#!/bin/bash
file="whois-results.csv"

if [ -f $file ] ; then
    rm $file
fi

for domain in `cat domains.txt`
do
    {
		echo $domain, $(whois $domain | grep 'Registrant Email:' | awk 'BEGIN{FS=" "}{print $3}') >> whois-results.csv
	} || {
		continue
	}
done

