from os import popen

tube = popen('hello.sh "pera asdas \n\r asdasdads"')
res = tube.read()
print res
# from django.core import mail
# from django.conf import settings
# import os, django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
# django.setup()

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
