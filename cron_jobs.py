#!/usr/bin/python2.7
import django
import sys, requests, json
from datetime import datetime, timedelta

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

from domain.models import BlackList, AllHash


class CronJobs:
    def __init__(self):
        pass

    def deleteOldData(self):
        condition = True
        while condition:
            response = requests.post(
                "http://www.webdomainexpert.pw/zakazani_delete_for_old_datas__/",
            ) 
            if response.status_code != 503:
                condition = False
        items = response.json()
        blocks = json.loads(items['blk'])
        for item in blocks:	
            email = item['fields']['email']			
            entry = BlackList.objects.filter(email=email)
            if not entry.exists():
                new = BlackList(email=email)
                new.save()

        hashes = json.loads(items['hashes'])
        for item in hashes:
            hash_base_id = item['fields']['hash_base_id']         
            AllHash.objects.filter(hash_base_id=hash_base_id).delete()


c_j = CronJobs()
if len(sys.argv) > 1:
	if sys.argv[1] == 'delete':
	    c_j.deleteOldData()
