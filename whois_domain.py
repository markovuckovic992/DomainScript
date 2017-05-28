from os import popen
from datetime import datetime
import os, django, hashlib
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
import binascii
import requests
from domain.models import *


def main_submit(date):
    non_hashed_leads = RawLeads.objects.filter(activated__gte=1, hash_base_id__isnull=True, no_email_found=0)
    for non_hashed_lead in non_hashed_leads:
        hash = hashlib.md5()
        hash.update(str(non_hashed_lead.id))
        hash_base_id = hash.hexdigest()

        while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
            hash_base_id = binascii.hexlify(os.urandom(16))

        new_entry = AllHash(hash_base_id=hash_base_id)
        new_entry.save()
        rls = RawLeads.objects.filter(id=non_hashed_lead.id)
        for rl in rls:
            rl.hash_base_id = hash_base_id
            rl.save()
    datas = RawLeads.objects.filter(date=date, activated__gte=1, mail__isnull=True)

    for data in datas:
        uslov = True
        i = 0
        email = None

        try:
            email = Emails.objects.get(name_zone=data.name_zone).email
        except:
            pass

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
                    reason='email is blacklisted'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            elif super_blacklisted.exists():
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=email,
                    reason='domain is blacklisted'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            elif same_shit.exists() or same_shit_2.exists():
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=email,
                    reason='duplicate -- 1'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            elif (super_same_shit.exists() or super_same_shit_2.exists()) and not (DomainException.objects.filter(domain=c_domain).exists() or DomainException.objects.filter(domain=domain).exists):
                reason = 'duplicate domain -- 1 '
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=email,
                    reason=reason
                )

                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            else:
                rl = RawLeads.objects.get(id=data.id)
                rl.mail = email
                rl.save()

                new = ProcessTracker(email=email, name_redemption=data.name_redemption)
                new.save()

def main(date, mode):
    new_analytics = WhoisAnalytics(source=mode)
    # hashes
    non_hashed_leads = RawLeads.objects.filter(activated__gte=1, hash_base_id__isnull=True, no_email_found=0)
    for non_hashed_lead in non_hashed_leads:
        hash = hashlib.md5()
        hash.update(str(non_hashed_lead.id))
        hash_base_id = hash.hexdigest()

        while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
            hash_base_id = binascii.hexlify(os.urandom(16))

        new_entry = AllHash(hash_base_id=hash_base_id)
        new_entry.save()
            # RawLeads.objects.filter(id=non_hashed_lead.id).update(hash_base_id=hash_base_id)
        rls = RawLeads.objects.filter(id=non_hashed_lead.id)
        for rl in rls:
            rl.hash_base_id = hash_base_id
            rl.save()
    # endhashes
    datas = RawLeads.objects.filter(date=date, activated__gte=1, mail__isnull=True)
    # ANALYTICS
    new_analytics.total = len(datas)
    new_analytics.save()
    master_of_index = 0
    # END
    for data in datas:
        uslov = True
        i = 0
        email = None

        try:
            email = Emails.objects.get(name_zone=data.name_zone).email
        except:
            if mode == "internal":
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
                                rl = RawLeads.objects.get(id=data.id)
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
            else:
                try:
                    r = requests.get('http://api.whoxy.com/?key=3d28dc0e398efe01dp7caa9f21e7b4fdf&whois=' + data.name_zone + '&format=json')
                    resp_data = r.json()
                    status = resp_data['domain_status'] if 'domain_status' in resp_data.keys() else 0
                    email = resp_data['registrant_contact']['email_address']

                    domain_registrar
                    if ('pendingDelete' in status) or ('redemptionPeriod' in status) or ('No match for' in status):
                        record = DeletedInfo(name_zone=data.name_zone, name_redemption=data.name_redemption, date=data.date, reason='domain has bad status')
                        record.save()
                        RawLeads.objects.filter(id=data.id).delete()
                except:
                    pass

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
                    reason='email is blacklisted'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            elif super_blacklisted.exists():
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=email,
                    reason='domain is blacklisted'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            elif same_shit.exists() or same_shit_2.exists():
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=email,
                    reason='duplicate -- 1'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            elif (super_same_shit.exists() or super_same_shit_2.exists()) and not (DomainException.objects.filter(domain=c_domain).exists() or DomainException.objects.filter(domain=domain).exists):
                reason = 'duplicate domain -- 1 '
                # if super_same_shit.exists():
                #     for asd in super_same_shit:
                #         reason += (asd.name_redemption + asd.email + ' ')
                # if super_same_shit_2.exists():
                #     for asd in super_same_shit_2:
                #         reason += (' ' + asd.name_redemption + asd.mail)
                record = DeletedInfo(
                    name_zone=data.name_zone,
                    name_redemption=data.name_redemption,
                    date=data.date,
                    email=email,
                    reason=reason
                )

                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            else:
                master_of_index += 1
                rl = RawLeads.objects.get(id=data.id)
                rl.mail = email
                rl.save()

                new = ProcessTracker(email=email, name_redemption=data.name_redemption)
                new.save()
                if Emails.objects.filter(name_zone=data.name_zone).exists():
                    ems = Emails.objects.filter(name_zone=data.name_zone)
                    for em in ems:
                        em.email = email
                        em.save()
                else:
                    new = Emails(name_zone=data.name_zone, email=email)
                    new.save()

    new_analytics.succeeded = master_of_index
    new_analytics.save()

def main_period(dates, mode):
    new_analytics = WhoisAnalytics(source=mode)
    master_of_index = 0
    for date in dates:
        # hashes
        non_hashed_leads = RawLeads.objects.filter(activated__gte=1, hash_base_id__isnull=True)
        for non_hashed_lead in non_hashed_leads:
            hash = hashlib.md5()
            hash.update(str(non_hashed_lead.id))
            hash_base_id = hash.hexdigest()

            while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
                hash_base_id = binascii.hexlify(os.urandom(16))

            new_entry = AllHash(hash_base_id=hash_base_id)
            new_entry.save()
            rls = RawLeads.objects.filter(id=non_hashed_lead.id)
            for rl in rls:
                rl.hash_base_id = hash_base_id
                rl.save()
        # endhashes

        datas = RawLeads.objects.filter(date=date, activated__gte=1, mail__isnull=True)
        # ANALYTICS
        ttls = new_analytics.total
        new_analytics.total = len(datas) + ttls
        new_analytics.save()
        # END
        for data in datas:
            uslov = True
            i = 0
            email = None

            try:
                email = Emails.objects.get(name_zone=data.name_zone).email
            except:
                if mode == "internal":
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
                                    rl = RawLeads.objects.get(id=data.id)
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
                else:
                    try:
                        r = requests.get('http://api.whoxy.com/?key=3d28dc0e398efe01dp7caa9f21e7b4fdf&whois=' + data.name_zone + '&format=json')
                        resp_data = r.json()
                        status = resp_data['domain_status'] if 'domain_status' in resp_data.keys() else 0
                        email = resp_data['registrant_contact']['email_address']

                        domain_registrar
                        if ('pendingDelete' in status) or ('redemptionPeriod' in status) or ('No match for' in status):
                            record = DeletedInfo(name_zone=data.name_zone, name_redemption=data.name_redemption, date=data.date, reason='domain has bad status')
                            record.save()
                            RawLeads.objects.filter(id=data.id).delete()
                    except:
                        pass

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
                        reason='email is blacklisted'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif super_blacklisted.exists() and not DomainException.objects.filter(domain=c_domain).exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='domain is blacklisted'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif same_shit.exists() or same_shit_2.exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='duplicate -- 2'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif (super_same_shit.exists() or super_same_shit_2.exists()) and not (DomainException.objects.filter(domain=c_domain).exists() or DomainException.objects.filter(domain=domain).exists):
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='duplicate domain -- 2'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                else:
                    master_of_index += 1
                    rl = RawLeads.objects.get(id=data.id)
                    rl.mail = email
                    rl.save()

                    new = ProcessTracker(email=email, name_redemption=data.name_redemption, date=date)
                    new.save()
                    if Emails.objects.filter(name_zone=data.name_zone).exists():
                        ems = Emails.objects.filter(name_zone=data.name_zone)
                        for em in ems:
                            em.email = email
                            em.save()
                    else:
                        new = Emails(name_zone=data.name_zone, email=email)
                        new.save()

    new_analytics.succeeded = master_of_index
    new_analytics.save()

# if __name__ == "__main__":
#     main(datetime.now().date())
