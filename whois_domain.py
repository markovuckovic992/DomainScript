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

    RawLeads.objects.filter(date=date, mark=1, activated=0).update(activated=1)

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
            same_shit = RawLeads.objects.filter(name_redemption=data.name_redemption, mail=email)
            domain = email.split('@', 1)[1]
            super_blacklisted = SuperBlacklist.objects.filter(domain=domain)
            super_same_shit = RawLeads.objects.filter(mail__endswith='@' + str(domain))
            if blacklisted.exists():
                RawLeads.objects.filter(id=data.id).delete()
            elif super_blacklisted.exists():
                RawLeads.objects.filter(id=data.id).delete()
            elif same_shit.exists():
                RawLeads.objects.filter(id=data.id).delete()
            elif super_same_shit.exists():
                RawLeads.objects.filter(id=data.id).delete()
            else:
                RawLeads.objects.filter(id=data.id).update(mail=email)
                if Emails.objects.filter(name_zone=data.name_zone).exists():
                    Emails.objects.filter(name_zone=data.name_zone).update(email=email)
                else:
                    new = Emails(name_zone=data.name_zone, email=email)
                    new.save()

    file = open('zone_with_no_emails.txt', 'w')
    file.seek(0)
    file.truncate()

    datas = RawLeads.objects.filter(date=date, activated=1, mail__isnull=True)
    for data in datas:
        file.write(data.name_zone + '\n')



def main_status(date):
    datas = Offer.objects.filter(date=date)
    for data in datas:
        uslov = True
        i = 0
        status = None
        while uslov:
            try:
                tube = popen("whois '" + str(
                    (data.zone).replace('\n', '').replace('\r', '')) + "' | egrep -i 'Status'",
                             'r')
                status = tube.read()
                status = status.replace('Status: ', '').replace('\n', '').replace('\r', '')
                tube.close()
                break
            except:
                if i > 5:
                    uslov = False
                else:
                    i += 1
        if status:
            Offer.objects.filter(id=data.id).update(status=status)

if __name__ == "__main__":
    main(datetime.now().date())

