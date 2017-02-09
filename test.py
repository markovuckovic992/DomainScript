# from django.core.mail import send_mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()
from domain.models import RawLeads, Emails
from datetime import datetime
import csv
from operator import attrgetter

leads = RawLeads.objects.filter(mail__isnull=False)

for lead in leads:
    mail = "".join(lead.mail.split())
    mail = mail.replace('Registrant Email:', '')
    if '@' in mail:
        RawLeads.objects.filter(id=lead.id).update(mail=mail)
    else:
        RawLeads.objects.filter(id=lead.id).update(mail=None)

emails = Emails.objects.all()

for email in emails:
    tmp = "".join(email.email.split())
    Emails.objects.filter(id=email.id).update(email=tmp)
