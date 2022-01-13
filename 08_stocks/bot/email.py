import smtplib, ssl
import os

from dotenv import load_dotenv


port = 465  # for SSL
load_dotenv(os.path.join(os.getcwd(), '.env'))
print(os.path.join(os.getcwd(), '.env'))
email_sender = os.getenv("EMAIL_HOST")
password = os.getenv("HOST_PASSWORD")
print(email_sender)
print(password)
# create a secure SSL context
context = ssl.create_default_context()


def send_email(email_to, subject, body):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_sender, password)

        modified_body = "\r\n".join((
            "From: %s" % email_sender,
            "To: %s" % email_to,
            "Subject: %s" % subject,
            "",
            body
        ))
        server.sendmail(email_sender, email_to, modified_body)
