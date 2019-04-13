import smtplib
import os.path as op
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

def create_mail(send_from, send_to, subject, message, file):
    # msg = MIMEMultipart()
    msg = MIMEBase('application', "EDIFACT")
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    fh = open(file, 'rb')
    msg.set_payload(fh.read())
    encoders.encode_base64(msg)
    msg.add_header('Content-Disposition', 'attachment; filename="{}"'.format(op.basename(file)))

    return msg

def send_mail(mail, server="localhost", port=587, username='', password='', use_tls=True):
    msg = mail
    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()

def send_mail_dir(username, password, server, input_dir):
    emails = os.listdir(input_dir)
    emails = list(filter(lambda e: "@" in e, emails))
    for email in emails:
        email_dir = op.join(input_dir, email)
        edi_messages = os.listdir(email_dir)
        for message in edi_messages:
            file = op.join(email_dir, message)
            mail = create_mail(username, ['viregistermail@gmail.com'], 'UNB Message', '', file=file)
            print(mail)
            send_mail(mail, server=server, username=username, password=password)
            exit(0)
            # send mail
            # move to sent folder
    # print('sent')