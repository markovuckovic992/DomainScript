#!/usr/bin/pypy
import django
import sys, requests, json, hashlib, traceback
from datetime import datetime, timedelta
from random import randint
from domain.apps import *
import os, pytz
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

from domain.models import BlackList, AllHash, RawLeads, Setting, SuperBlacklist, Emails, ProcessTracker, DeletedInfo
from django.core import mail
from django.conf import settings
from os import popen


class CronJobs:
    def __init__(self):
        self.hosts = [
            'webdomainexpert.us',
            'webdomainexpert.host',
            'webdomainexpert.site',
            'webdomainexpert.club',
        ]

    def deleteOldData(self):
        date = datetime.now().date() - timedelta(days=28)
        date2 = datetime.now().date() - timedelta(days=5)

        # START LOG
        datas = RawLeads.objects.filter(date__lt=date)
        for data in datas:
            record = DeletedInfo(
                name_zone=data.name_zone,
                name_redemption=data.name_redemption,
                date=data.date,
                email=data.mail,
                reason='older then 28'
            )
            record.save()
            RawLeads.objects.filter(id=data.id).delete()
        # END LOGGING

        AllHash.objects.filter(date__lt=date).delete()
        DeletedInfo.objects.filter(datetime__lt=date2).delete()

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

        margin = (datetime.now() - timedelta(days=7)).date()
        ProcessTracker.objects.filter(date__lte=margin).delete()

    def send(self):
        potential_profits = RawLeads.objects.filter(mail__isnull=False, activated=1, reminder=0).order_by('id')[:8]
        connection = mail.get_connection()
        connection.open()

        for potential_profit in potential_profits:
            hash_base_id = potential_profit.hash_base_id
            try:
                iterator = randint(0, 3)
                link = ('http://www.' + str(self.hosts[iterator]) + '/offer/?id=' + str(hash_base_id))
                unsubscribe = ('http://www.' + str(self.hosts[iterator]) + '/unsubscribe/?id=' + str(hash_base_id))
                case = randint(1, 10)
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
                if req.status_code == 204:
                    hash = hashlib.md5()
                    hash.update(str(potential_profit.id + 100000))
                    hash_base_id = hash.hexdigest()

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
                    AllHash.objects.filter(hash_base_id=hash_base_id)
                    RawLeads.objects.filter(id=potential_profit.id).update(reminder=1, hash_base_id=hash_base_id)

                    emails = []
                    email = mail.EmailMultiAlternatives(
                        msg[0],
                        'potential_profit.name_zone',
                        'Web Domain Expert <' + str(settings.EMAIL_HOST_USER) + '>',
                        [potential_profit.mail],
                        reply_to=("support@webdomainexpert.com", ),
                        bcc=["bcc-webdomainexpert@outlook.com"],
                    )
                    email.attach_alternative(msg[1], "text/html")
                    emails.append(email)
                    try:
                        connection.send_messages(emails)
                        asdi += 1
                    except SMTPServerDisconnected:
                        connection = mail.get_connection()
                        connection.open()
                        connection.send_messages(emails)
            except:
                print traceback.format_exc()
        connection.close()


    def whois(self):
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
                            (data.name_zone).replace('\n', '').replace('\r', '')) + "' | egrep -i 'Registrant Email|Status:|No match for'",
                                     'r')
                        response = tube.read()
                        if ('pendingDelete' in response) or ('redemptionPeriod' in response) or ('No match for' in response):
                            record = DeletedInfo(name_zone=data.name_zone, name_redemption=data.name_redemption, date=data.date, reason='domain has bad status')
                            record.save()
                            RawLeads.objects.filter(id=data.id).delete()
                        else:
                            index = response.find('Registrant Email')
                            if index == -1:
                                # RawLeads.objects.filter(id=data.id).update(no_email_found=1)
                                rl = awLeads.objects.get(id=data.id)
                                rl.no_email_found = 1
                                rl.save()
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
                blacklisted = BlackList.objects.filter(email__iexact=email)
                same_shit = ProcessTracker.objects.filter(name_redemption=data.name_redemption, email=email)
                same_shit_2 = RawLeads.objects.filter(name_redemption=data.name_redemption, mail=email)
                domain = email.split('@', 1)[1]
                c_domain = domain.split('.', 1)[0]
                super_blacklisted = SuperBlacklist.objects.filter(domain=domain)
                super_same_shit = ProcessTracker.objects.filter(email__endswith='@' + str(domain), name_redemption=data.name_redemption)
                super_same_shit_2 = RawLeads.objects.filter(mail__endswith='@' + str(domain), name_redemption=data.name_redemption)
                if blacklisted.exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='email is blacklisted, cron'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif super_blacklisted.exists() and not DomainException.objects.filter(domain=c_domain).exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='domain is blacklisted, cron'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif same_shit.exists() or same_shit_2.exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='duplicate --, cron'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif (super_same_shit.exists() or super_same_shit_2.exists()) and not (DomainException.objects.filter(domain=c_domain).exists() or DomainException.objects.filter(domain=domain).exists):
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='duplicate domain --, cron'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                else:
                    # RawLeads.objects.filter(id=data.id).update(mail=email)
                    rl = RawLeads.objects.get(id=data.id)
                    rl.mail = email
                    rl.save()
                    new = ProcessTracker(email=email, name_redemption=data.name_redemption, date=datetime.now().date())
                    new.save()
                    if Emails.objects.filter(name_zone=data.name_zone).exists():
                        # Emails.objects.filter(name_zone=data.name_zone).update(email=email)
                        ems = Emails.objects.filter(name_zone=data.name_zone)
                        for em in ems:
                            em.email = email
                            em.save()
                    else:
                        new = Emails(name_zone=data.name_zone, email=email)
                        new.save()
            elif email and '@' not in email:
                # RawLeads.objects.filter(id=data.id).update(no_email_found=1)
                rl = RawLeads.objects.get(id=data.id)
                rl.no_email_found = 1
                rl.save()


        file = open('zone_with_no_emails.txt', 'w')
        file.seek(0)
        file.truncate()

        datas = RawLeads.objects.filter(date__gte=margin, activated=1, mail__isnull=True)
        for data in datas:
            file.write(data.name_zone + '\n')

    def check(self):
        req = requests.post("http://www.webdomainexpert.pw/check_for_offers/")
        if req.status_code == 200:
            items = req.json()
            ids = items['ids']
            datas = RawLeads.objects.filter(hash_base_id__in=ids, reminder=1)
            for data in datas:
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=data.mail,
                    reason='--already left an offer, no reminders needed--'
                )
                record.save()
            RawLeads.objects.filter(hash_base_id__in=ids, reminder=1).delete()

        # SENDING
        two_days_ago = (datetime.now() - timedelta(days=2))
        two_days_ago = pytz.timezone('Europe/Belgrade').localize(two_days_ago)
        reminders = RawLeads.objects.filter(reminder=1, last_email_date__lt=two_days_ago)[0:15]
        connection = mail.get_connection()
        connection.open()
        asdi = 0
        emails = []

        for reminder in reminders:
            name = ''
            # case = randint(1, 10)
            case = 1
            index = randint(0, 3)
            link = ('http://www.' + str(self.hosts[index]) + '/offer/?id=' + str(reminder.hash_base_id))
            unsubscribe = ('http://www.' + str(self.hosts[index]) + '/unsubscribe/?id=' + str(reminder.hash_base_id))
            sub, msg = eval('pr_msg' + str(case) + '("' + str(reminder.name_redemption) + '", "' + str(name) + '", "' + str(unsubscribe) + '", "' + str(link) + '")')

            email = mail.EmailMultiAlternatives(
                sub,
                '',
                'Web Domain Expert <' + settings.EMAIL_HOST_USER + '>',
                [reminder.mail],
                bcc=["bcc-webdomainexpert@outlook.com"],
            )

            email.attach_alternative(msg, "text/html")
            emails.append(email)

            record = DeletedInfo(
                name_zone=reminder.name_zone,
                name_redemption=reminder.name_redemption,
                date=reminder.date,
                email=reminder.mail,
                reason='--reminder sent--'
            )
            record.save()

            RawLeads.objects.filter(id=reminder.id).delete()

        connection.send_messages(emails)
        connection.close()

c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'delete':
        c_j.deleteOldData()
    elif sys.argv[1] == 'send':
        c_j.send()
    elif sys.argv[1] == 'whois':
        c_j.whois()
    elif sys.argv[1] == 'dont_touch':
        c_j.check()
