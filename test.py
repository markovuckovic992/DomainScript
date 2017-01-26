# from django.core.mail import send_mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, BlackList, AllHash
from datetime import datetime
import csv
from operator import attrgetter


# with open('convertcsv.csv', 'r') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     for row in spamreader:
#         new = RawLeads(
#             name_zone=row[1],
#             name_redemption=row[3],
#             date=datetime.now().date(),
#             page=1,
#             activated=1,
#             mail=row[4],
#         )
#         new.save()

bls = BlackList.objects.all()

for bl in bls:    
    hash_base_ids = map(attrgetter('hash_base_id'), RawLeads.objects.filter(mail=bl.email))
    AllHash.objects.filter(hash_base_id__in=hash_base_ids)
    RawLeads.objects.filter(mail=bl.email).delete()
