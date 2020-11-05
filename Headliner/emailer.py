from flask import Flask
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zipfile import ZipFile


# create mailbot
class MailBot:
    def __init__(self, email, password):
        self.app = Flask(__name__)
        self.smtpObj = smtplib.SMTP('smtp.office365.com', 587)
        self.smtpObj.ehlo()
        self.smtpObj.starttls()

        # set email and password
        self.email = email
        self.password = password

    # create a function to send messages
    def send_message(self, subject, body, recipients, zip_file=None):
        # authenticate
        self.smtpObj.login(self.email, self.password)

        # create the body
        text = MIMEText(body)

        # process the zip attachment
        if zip_file:
            zip_attachment = MIMEBase('application', 'zip')

            zf = open(zip_file, 'rb')
            zip_attachment.set_payload(zf.read())

            encoders.encode_base64(zip_attachment)
            zip_attachment.add_header('Content-Disposition', 'attachment',
                                      filename=zip_file)

        # make the message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg.attach(text)
        if zip_file:
            msg.attach(zip_attachment)

        # send it to different people
        for recipient in recipients:
            msg['To'] = recipient

            self.smtpObj.sendmail(self.email, recipient, msg.as_string())
