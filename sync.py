import django
import sys
import traceback
import os
from django.core import mail
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads
from domain.models import AllHash

offers = RawLeads.objects.all()
for offer in offers:
    if offer.hash_base_id:
        AllHash(
            hash_base_id=offer.hash_base_id,
            date=offer.date,
        ).save()

offers = AllHash.objects.raw("SELECT * FROM hashes_hzn")
for offer in offers:
    if offer.hash_base_id:
        try:
            AllHash(
                hash_base_id=offer.hash_base_id,
                date=offer.date,
            ).save()
        except:
            pass
