#!/usr/bin/pypy
import django
import sys, requests, json, hashlib, traceback
from datetime import datetime, timedelta
from random import randint
from domain.apps import *
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

from domain.models import BlackList, AllHash, RawLeads, Setting, SuperBlacklist, Emails
from django.core import mail
from django.conf import settings
from os import popen


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

    def whois(self):
        f = open('deleted.txt', 'a')

        number_of_days = Setting.objects.get(id=1).number_of_days
        margin = (datetime.now() - timedelta(days=number_of_days))
        datas = RawLeads.objects.filter(date__gte=margin, activated=1, mail__isnull=True, no_email_found=0)[0:2100]
        for data in datas:
            uslov = True
            i = 0
            email = None

            try:
                email = Emails.objects.get(name_zone=data.name_zone).email
            except:
                while uslov:
                    try:
                        tube = popen("whois '" + str(
                            (data.name_zone).replace('\n', '').replace('\r', '')) + "' | egrep -i 'Registrant Email|Status:'",
                                     'r')
                        response = tube.read()
                        if ('pendingDelete' in response) or ('redemptionPeriod' in response) or ('No match for' in response):
                            print data.name_zone, 'entry 1'
                            f.write((data.name_zone).replace('\n', '').replace('\r', '') + ': REASON, STATUS! \n\r')
                            RawLeads.objects.filter(id=data.id).delete()
                        else:
                            index = response.find('Registrant Email')
                            if index == -1:
                                print data.name_zone, 'entry 2'
                                RawLeads.objects.filter(id=data.id).update(no_email_found=1)
                                break
                            new = response[index:]
                            response = new.splitlines()[0]
                            email = response.replace('Registrant Email: ', '').replace('\n', '').replace('\r', '')
                        break
                    except:
                        if i > 5:
                            uslov = False
                        else:
                            i += 1
            if email and '@' in email:                
                email = "".join(email.split())
                blacklisted = BlackList.objects.filter(email=email)
                same_shit = RawLeads.objects.filter(name_redemption=data.name_redemption, mail=email)
                domain = email.split('@', 1)[1]
                super_blacklisted = SuperBlacklist.objects.filter(domain=domain)
                super_same_shit = RawLeads.objects.filter(mail__endswith='@' + str(domain))
                if blacklisted.exists():
                    print data.name_zone, 'entry 3'
                    RawLeads.objects.filter(id=data.id).delete()
                elif super_blacklisted.exists():
                    print data.name_zone, 'entry 4'
                    RawLeads.objects.filter(id=data.id).delete()
                elif same_shit.exists():
                    print data.name_zone, 'entry 5'
                    RawLeads.objects.filter(id=data.id).delete()
                elif super_same_shit.exists():
                    print data.name_zone, 'entry 5'
                    RawLeads.objects.filter(id=data.id).delete()
                else:
                    print data.name_zone, 'entry 6'
                    RawLeads.objects.filter(id=data.id).update(mail=email)
                    if Emails.objects.filter(name_zone=data.name_zone).exists():
                        Emails.objects.filter(name_zone=data.name_zone).update(email=email)
                    else:
                        new = Emails(name_zone=data.name_zone, email=email)
                        new.save()
            elif email and '@' not in email:
                print data.name_zone, 'entry 7'
                RawLeads.objects.filter(id=data.id).update(no_email_found=1)

            print data.name_zone, 'entry 8'

        file = open('zone_with_no_emails.txt', 'w')
        file.seek(0)
        file.truncate()

        datas = RawLeads.objects.filter(date__gte=margin, activated=1, mail__isnull=True)
        for data in datas:
            file.write(data.name_zone + '\n')

        f.close()

c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'delete':
        c_j.deleteOldData()
    elif sys.argv[1] == 'send':
        c_j.send()
    elif sys.argv[1] == 'whois':
        c_j.whois()
