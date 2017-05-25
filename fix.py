# from django.core import mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, DomainException, Tlds

if __name__ == "__main__":
    #ASD
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
    #EMD ASD
    tlds = []
    TLDS = Tlds.objects.all()
    for TLD in TLDS:
        tlds.append(TLD.extension)

    for tld in tlds:
        raw_leads = RawLeads.objects.filter(name_redemption__contains=tld)
        for lead in raw_leads:
            domain_z = lead.name_zone
            domain_r = lead.name_redemption
            lead.name_redemption = domain_z
            lead.name_zone = domain_r
            lead.save()

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
