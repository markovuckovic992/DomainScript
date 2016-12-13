#!/usr/bin/python2.7
import django
import sys, requests
from datetime import datetime, timedelta

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

from domain.models import BlackList


class CronJobs:
    def __init__(self):
        pass

    def deleteOldData(self):
        response = requests.post(
            "http://www.webdomainexpert.pw/zakazani_delete_for_old_datas__/",
        )
        file = open('error.html', 'w')
        file.write(str(response.json()))
        items = response.json()
        for item in items:	
			email = item['fields']['email']			
			entry = BlackList.objects.filter(email=email)
			if not entry.exists():
				new = BlackList(email=email)
				new.save()


c_j = CronJobs()
if len(sys.argv) > 1:
	if sys.argv[1] == 'delete':
	    c_j.deleteOldData()
