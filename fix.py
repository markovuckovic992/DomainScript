# from django.core import mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, DomainException, Tlds, WhoisAnalytics, ZoneDomains
import time
from random import randint

if __name__ == "__main__":
    # ASD
    # DeletedInfo.objects.filter(reason='')

    # deleted = DeletedInfo.objects.get(id=id_)
    # condition = True
    # while condition:
    #     try:
    #         entry = RawLeads(
    #             name_zone=deleted.name_zone,
    #             name_redemption=deleted.name_redemption,
    #             date=deleted.date,
    #             mail=deleted.email,
    #             page=1,
    #             activated=1,
    #             hash_base_id=binascii.hexlify(os.urandom(16))
    #         )
    #         entry.save()
    #         condition = False
    #     except:
    #         pass
    # DeletedInfo.objects.filter(id=id_).delete()
    # return HttpResponse('{"status": "success"}', content_type="application/json")
    start_time = time.time()

    file = open('info_zone_14Feb.txt', "r")
    all_domains = set(file.readlines())

    for line in all_domains:
        tmp_d = line.lower()[:100]  
        if not ZoneDomains.objects.filter(domain=tmp_d).exists():
            ZoneDomains(domain=tmp_d).save()

    duration = int(time.time() - start_time)
    print duration
# connection = mail.get_connection()
# connection.open()
# emails = []
# email = mail.EmailMultiAlternatives(
#     'TEST',
#     'TEST',
#     'Web Domain Expert <info@webdomainexpert.club>',
#     ['markovuckovic992@yahoo.com'],
# )
# emails.append(email)
# connection.send_messages(emails)
# connection.close()
