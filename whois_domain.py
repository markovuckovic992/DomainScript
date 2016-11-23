from os import popen

import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads

def main(date):
    usefull_data = []
    print date
    datas_to_move = RawLeads.objects.filter(send_mail=0, date=date).update(archive=1)
    datas = RawLeads.objects.filter(send_mail=1, mail__isnull=True)
    for data in datas:
        uslov = True
        i = 0
        email = None
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
        if email:
            RawLeads.objects.filter(id=data.id).update(mail=email)
