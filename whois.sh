#!/bin/bash
for domain in `cat domains.txt`
do
   echo $domain $(whois $domain | grep 'Registrant Email:' | awk 'BEGIN{FS=" "}{print $3}') >> whois-results.txt
done

