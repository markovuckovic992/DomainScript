from os import popen
from datetime import datetime
import os, django, hashlib
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import *

def main(date):
    usefull_data = []
    if not Log.objects.filter(date=datetime.now().date()).exists():
        Log().save()
    number_of_new = len(RawLeads.objects.filter(date=date, mark=1, activated=0))
    number_of_old = Log.objects.get(date=datetime.now().date()).number_act
    number_of_old_2 = Log.objects.get(date=datetime.now().date()).number_act_2
    Log.objects.filter(date=datetime.now().date()).update(number_act=(int(number_of_old) + int(number_of_new)))
    Log.objects.filter(date=date).update(number_act_2=(int(number_of_old_2) + int(number_of_new)))

    # RawLeads.objects.filter(date=date, mark=1, activated=0).update(activated=1)

    # hashes
    non_hashed_leads = RawLeads.objects.filter(activated=1, hash_base_id__isnull=True, no_email_found=0)
    for non_hashed_lead in non_hashed_leads:
        hash = hashlib.md5()
        hash.update(str(non_hashed_lead.id))
        hash_base_id = hash.hexdigest()
        i = 0
        while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
            hash.update(str(non_hashed_lead.id + i))
            hash_base_id = hash.hexdigest()
            i += 1
        new_entry = AllHash(hash_base_id=hash_base_id)
        new_entry.save()
        RawLeads.objects.filter(id=non_hashed_lead.id).update(hash_base_id=hash_base_id)
    # endhashes

    datas = RawLeads.objects.filter(date=date, activated=1, mail__isnull=True)
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
                        (data.name_zone).replace('\n', '').replace('\r', '')) + "' | egrep -i 'Registrant Email'",
                                 'r')
                    email = tube.read()
                    email = email.replace('Registrant Email: ', '').replace('\n', '').replace('\r', '')
                    tube.close()
                    break
                except:
                    if i > 5:
                        uslov = False
                    else:
                        i += 1

        if email and '@' in email:
            email = "".join(email.split())
            blacklisted = BlackList.objects.filter(email=email)
            same_shit = ProcessTracker.objects.filter(name_redemption=data.name_redemption, email=email)
            same_shit_2 = RawLeads.objects.filter(name_redemption=data.name_redemption, mail=email)
            domain = email.split('@', 1)[1]
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
                record.save()
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
                    reason='duplicate'
                )
                record.save()
                RawLeads.objects.filter(id=data.id).delete()
            # elif super_same_shit.exists() or super_same_shit_2.exists():
            #     record = DeletedInfo(
            #         name_zone=data.name_zone,
            #         name_redemption=data.name_redemption,
            #         date=data.date,
            #         email=email,
            #         reason='duplicate domain'
            #     )
            #     record.save()
            #     RawLeads.objects.filter(id=data.id).delete()
            else:
                RawLeads.objects.filter(id=data.id).update(mail=email)
                new = ProcessTracker(email=email, name_redemption=data.name_redemption)
                new.save()
                if Emails.objects.filter(name_zone=data.name_zone).exists():
                    Emails.objects.filter(name_zone=data.name_zone).update(email=email)
                else:
                    new = Emails(name_zone=data.name_zone, email=email)
                    new.save()



def main_period(dates):
    for date in dates:
        usefull_data = []
        if not Log.objects.filter(date=datetime.now().date()).exists():
            Log().save()
        number_of_new = len(RawLeads.objects.filter(date=date, mark=1, activated=0))
        number_of_old = Log.objects.get(date=datetime.now().date()).number_act
        number_of_old_2 = Log.objects.get(date=datetime.now().date()).number_act_2
        Log.objects.filter(date=datetime.now().date()).update(number_act=(int(number_of_old) + int(number_of_new)))
        Log.objects.filter(date=date).update(number_act_2=(int(number_of_old_2) + int(number_of_new)))

        # RawLeads.objects.filter(date=date, mark=1, activated=0).update(activated=1)

        # hashes
        non_hashed_leads = RawLeads.objects.filter(activated=1, hash_base_id__isnull=True)
        for non_hashed_lead in non_hashed_leads:
            hash = hashlib.md5()
            hash.update(str(non_hashed_lead.id))
            hash_base_id = hash.hexdigest()
            i = 0
            while AllHash.objects.filter(hash_base_id=hash_base_id).exists():
                hash.update(str(non_hashed_lead.id + i))
                hash_base_id = hash.hexdigest()
                i += 1
            new_entry = AllHash(hash_base_id=hash_base_id)
            new_entry.save()
            RawLeads.objects.filter(id=non_hashed_lead.id).update(hash_base_id=hash_base_id)
        # endhashes

        datas = RawLeads.objects.filter(date=date, activated=1, mail__isnull=True)
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
                            (data.name_zone).replace('\n', '').replace('\r', '')) + "' | egrep -i 'Registrant Email'",
                                     'r')
                        email = tube.read()
                        email = email.replace('Registrant Email: ', '').replace('\n', '').replace('\r', '')
                        tube.close()
                        break
                    except:
                        if i > 5:
                            uslov = False
                        else:
                            i += 1
            if email and '@' in email:
                email = "".join(email.split())
                blacklisted = BlackList.objects.filter(email=email)
                same_shit = ProcessTracker.objects.filter(name_redemption=data.name_redemption, email=email)
                same_shit_2 = RawLeads.objects.filter(name_redemption=data.name_redemption, mail=email)
                domain = email.split('@', 1)[1]
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
                # elif super_blacklisted.exists():
                #     record = DeletedInfo(
                #         name_zone=data.name_zone,
                #         name_redemption=data.name_redemption,
                #         date=data.date,
                #         email=email,
                #         reason='domain is blacklisted'
                #     )
                #     record.save()
                #     RawLeads.objects.filter(id=data.id).delete()
                elif same_shit.exists() or same_shit_2.exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='duplicate'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                elif super_same_shit.exists() or super_same_shit_2.exists():
                    record = DeletedInfo(
                        name_zone=data.name_zone,
                        name_redemption=data.name_redemption,
                        date=data.date,
                        email=email,
                        reason='duplicate domain'
                    )
                    record.save()
                    RawLeads.objects.filter(id=data.id).delete()
                else:
                    RawLeads.objects.filter(id=data.id).update(mail=email)
                    new = ProcessTracker(email=email, name_redemption=data.name_redemption, date=date)
                    new.save()
                    if Emails.objects.filter(name_zone=data.name_zone).exists():
                        Emails.objects.filter(name_zone=data.name_zone).update(email=email)
                    else:
                        new = Emails(name_zone=data.name_zone, email=email)
                        new.save()


if __name__ == "__main__":
    main(datetime.now().date())

