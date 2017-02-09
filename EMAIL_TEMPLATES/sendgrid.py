# For support@webdomainexpert.com - Alex says you can use Google SMTP details and it'll work

# So can you try that? p/w is - asdQWE123

# domainexpert , pw sbb12345

import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey="f9_blKFgQoiWtQJ5FOmGwg")

from_email = Email("edomainexpert@gmail.com")
subject = "Hello World from the SendGrid Python Library!"
to_email = Email("markovuckovic992@yahoo.com")
content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
