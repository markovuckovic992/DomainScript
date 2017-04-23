import time
current_time = time.time()

a = range(1, 20000000)
tmp = []
# for item in a:
# 	if len(tmp) >= 1000:
# 		break
# 	if item % 2:
# 		tmp.append(item)
a = range(1, 1000)
tmp = [item for item in a if item % 2]
# cProfile.run('tmp = [item for item in a if item % 2]')

def my_range(start, end, array):
	while start <= end:
		yield array[start]
		start += 1
# for x in my_range(0, 1000, a):
#     tmp.append(x)

print time.time() - current_time
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
