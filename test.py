# from django.core.mail import send_mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads
from datetime import datetime
import csv

with open('convertcsv.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print row
        RawLeads(
            name_zone=row[0],
            name_redemption=row[2],
            date=datetime.now().date(),
            page=1,
            activated=1,
        )
