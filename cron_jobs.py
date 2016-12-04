# -*- coding: UTF-8 -*-
import django
import sys, requests
from datetime import datetime, timedelta

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()



class CronJobs:
    def __init__(self):
        pass

    def deleteOldData(self):
        requests.post(
            "http://www.webdomainexpert.pw/zakazani_delete_for_old_datas__/",
        )


c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'delete':
        c_j.deleteOldData()
