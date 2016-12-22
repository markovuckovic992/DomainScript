from django.core.mail import send_mail
from django.conf import settings

import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

send_mail(
    'Test',  # Title
    'Test',  # Body
    settings.EMAIL_HOST_USER,
    ['markovuckovic992@yahoo.com'],
    fail_silently=False,
    html_message='<h1>Test</h1>',
)
