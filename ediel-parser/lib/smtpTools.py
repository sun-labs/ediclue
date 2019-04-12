import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

def create_mail(send_from, send_to, subject, message, files=[]):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

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
    mail = create_mail(username, ['viregistermail@gmail.com'], 'Hello world', 'test message from myself.', files=['/Users/victoringman/edi-messages/se.el@edilink.eu/1-0-EdilinkServices.edi'])
    send_mail(mail, server=server, username=username, password=password)
    print('sent')