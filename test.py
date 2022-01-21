import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='contact@olam-erp.com',
    to_emails='amuriuki@olam-erp.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)