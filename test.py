# from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPServerDisconnected
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

# send_mail(
#     'Test',  # Title
#     'Test',  # Body
#     settings.EMAIL_HOST_USER,
#     ['markovuckovic992@yahoo.com'],
#     fail_silently=False,
#     html_message='<h1>Test</h1>',
#     reply_to=("edomainexpert@gmail.com", ),
# )
from django.core import mail

connection = mail.get_connection()
connection.open()
emails = []

email = mail.EmailMultiAlternatives(
    'Test',
    'Test',
    'Web Domain Expert <' + settings.EMAIL_HOST_USER + '>',
    ['markovuckovic992@yahoo.com'],
    reply_to=("edomainexpert@gmail.com", ),
)
emails.append(email)
try:
	connection.send_messages(emails)
	raise SMTPServerDisconnected
except SMTPServerDisconnected:
	pass
connection.close()
