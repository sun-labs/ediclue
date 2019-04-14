import imaplib
import smtplib
import os
import email
import time

SMTP_PORT = 587
class EDICommunicator():
    def __init__(self, *, username=None, password=None, server=None, output_dir=None, input_dir=None, use_tls=True):
        self.username = username
        self.password = password
        self.server = server
        self.use_tls = use_tls
        if username is not None and password is not None and server is not None:
            self.init_imap()

    def init_imap(self):
        self.imap = imaplib.IMAP4_SSL(self.server)
        self.imap.login(self.username, self.password)
        self.imap.select()

    def list_labels(self):
        return self.imap.list()

    def set_labels_email(self, email_id: str, labels: str):
        return self.imap.store(email_id, '+FLAGS', '({})'.format(labels))

    def mail_from_str(self, mail_str):
        mail = email.message_from_string(mail_str)
        return mail

    def imap_search_query(self, query):
        res, emails = self.imap.search(None, query)
        emails = emails[0].split()
        return emails

    def str_mail_ids(self, mail_ids: [str]):
        return ','.join(mail_ids)

    def format_mail_ids(self, mail_ids: [str]):
        return list(map(lambda i: i.decode('utf-8'), mail_ids))

    def imap_store_query(self, email_id, command, flags, return_raw=False):
        res, emails = self.imap.store(email_id, command, flags)
        emails = list(map(lambda e: e.decode('utf-8'), filter(None, emails)))
        if return_raw is False and len(emails) > 0:
            emails = list(map(lambda e: e.split()[0], emails))
        return emails

    def get_mail_without_label(self, labels:[str]):
        query_str = '(ALL)'
        if labels is not None:
            if type(labels) is str: 
                labels = [labels]
            query_str = 'UNKEYWORD {}'.format(' '.join(labels))
        res, emails = self.imap.search(None, query_str)
        emails = emails[0].split()
        return emails

    def get_mail_with(self, email_id, selection='(BODY.PEEK[])'):
        res, data = self.imap.fetch(email_id, selection)
        return data[0][1] # mail body
        # mail = email.message_from_bytes(data[0][1])
        # return mail

    def send_mail(self, mail, port=SMTP_PORT):
        server = smtplib.SMTP()
        server.connect(self.server, port)
        if self.use_tls:
            server.starttls()
        server.login(self.username, self.password)
        server.sendmail(mail['From'], mail['To'], mail.as_string())
        self.imap.append('INBOX.Sent', '', imaplib.Time2Internaldate(time.time()), mail.as_bytes())
        server.quit()
