# from django.core import mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, DomainException

if __name__ == "__main__":
    DeletedInfo.objects.filter(reason='')

    deleted = DeletedInfo.objects.get(id=id_)
    condition = True
    while condition:
        try:
            entry = RawLeads(
                name_zone=deleted.name_zone,
                name_redemption=deleted.name_redemption,
                date=deleted.date,
                mail=deleted.email,
                page=1,
                activated=1,
                hash_base_id=binascii.hexlify(os.urandom(16))
            )
            entry.save()
            condition = False
        except:
            pass
    DeletedInfo.objects.filter(id=id_).delete()
    return HttpResponse('{"status": "success"}', content_type="application/json")


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
