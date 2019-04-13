import imaplib
import smtplib
import os
import email
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders

SMTP_PORT = 587
EDI_FILENAME = 'edifact.edi'
class EDICommunicator():
    def __init__(self, *, username=None, password=None, server=None, output_dir=None, input_dir=None, use_tls=True):
        self.username = username
        self.password = password
        self.server = server
        self.use_tls = use_tls
        if username is not None and password is not None and server is not None:
            self.init_imap(username, password, server, use_tls)

    def init_imap(self, username, password, server, use_tls):
        self.imap = imaplib.IMAP4_SSL(server)
        self.imap.login(user, password)

    def set_labels_email(self, email_ids: [str], labels: [str]):
        emails_str = ','.join(email_ids)
        labels_str = '({})'.format(' '.join(labels))
        m.store(emails_str, '+FLAGS', labels_str)

    def send_mail(self, mail, port=SMTP_PORT):
        server = smtplib.SMTP()
        server.connect(self.server, port)
        if self.use_tls:
            server.starttls()
        server.login(self.username, self.password)
        server.sendmail(mail['From'], mail['To'], mail.as_string())
        server.quit()

    def read_file(self, file_path):
        fh = open(file_path, 'rb')
        content = fh.read()
        fh.close()
        return content

    def create_edi_mail(self, *, send_from, send_to, subject, file_content, file=None, file_name=''):
        mail = MIMEBase('application', "EDIFACT")
        mail['From'] = send_from
        mail['To'] = COMMASPACE.join(send_to) if type(send_to) is list else send_to
        mail['Date'] = formatdate(localtime=True)
        mail['Subject'] = subject

        file_content = file_content if file is None else self.read_file(file)
        mail.set_payload(file_content)
        encoders.encode_base64(mail)
        mail.add_header('Content-Disposition', 'attachment; filename="{}"'.format(EDI_FILENAME))

        return mail
