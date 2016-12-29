#!/usr/bin/python2.7
import django
import sys, requests, json, hashlib, traceback
from datetime import datetime, timedelta

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

from domain.models import BlackList, AllHash, RawLeads
from django.core import mail

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

    def send(self):
        potential_profits = RawLeads.objects.filter(mail__isnull=False, activated=1).order_by('id')[:15]
        connection = mail.get_connection()
        connection.open()
        emails = []

        for potential_profit in potential_profits:
            hash = hashlib.md5()
            hash.update(str(potential_profit.id))
            hash_base_id = hash.hexdigest()
            i = 0
            while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
                hash.update(str(potential_profit.id + i))
                hash_base_id = hash.hexdigest()
                i += 1
            new_entry = AllHash(hash_base_id=hash_base_id)
            new_entry.save()
            try:
                link = ('http://www.webdomainexpert.pw/offer/?id=' + str(hash_base_id))
                unsubscribe = ('http://www.webdomainexpert.pw/unsubscribe/?id=' + str(hash_base_id))
                case = randint(1, 4)
                msg = eval('form_a_msg' + str(case) + '("' + str(potential_profit.name_redemption) + '","' + str(
                    link) + '","' + str(unsubscribe) + '")')

                req = requests.post(
                    "http://www.webdomainexpert.pw/add_offer/",
                    data={
                        'base_id': potential_profit.id,
                        'drop': potential_profit.name_redemption,
                        'lead': potential_profit.name_zone,
                        'hash_base_id': hash_base_id,
                        'remail': potential_profit.mail,
                    }
                )
                if req.status_code == 200:
                    RawLeads.objects.filter(id=potential_profit.id).delete()

                    email = mail.EmailMultiAlternatives(
                        msg[0],
                        'potential_profit.name_zone',
                        'Web Domain Expert <' + settings.EMAIL_HOST_USER + '>',
                        [potential_profit.mail],
                    )

                    email.attach_alternative(msg[1], "text/html")
                    emails.append(email)

            except:
                print traceback.format_exc()
        connection.send_messages(emails)
        connection.close()

c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'delete':
        c_j.deleteOldData()
    elif sys.argv[1] == 'send':
        c_j.send()
