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

    def mail_from_str(self, mail_str: str):
        mail = email.message_from_string(mail_str)
        return mail

    def imap_search_query(self, query: str):
        res, emails = self.imap.search(None, query)
        emails = emails[0].split()
        return emails

    def str_mail_ids(self, mail_ids: [str]) -> str:
        return ','.join(mail_ids)

    def mail_ids_from_filenames(self, filenames: [str]) -> [str]:
        return list(map(lambda f: f.split('.')[0], filenames))

    def format_mail_ids(self, mail_ids: [str]) -> [str]:
        return list(map(lambda i: i.decode('utf-8'), mail_ids))

    def imap_store_query(self, email_id: str, command, flags, return_raw=False) -> str:
        res, emails = self.imap.store(email_id, command, flags)
        emails = list(map(lambda e: e.decode('utf-8'), filter(None, emails)))
        if return_raw is False and len(emails) > 0:
            emails = list(map(lambda e: e.split()[0], emails))
        return self.str_mail_ids(emails)

    def get_mail_with(self, email_id: str, selection='(BODY.PEEK[])') -> str:
        res, data = self.imap.fetch(email_id, selection)
        return data[0][1].decode('utf-8') # mail body

    def send_mail(self, mail, port=SMTP_PORT):
        server = smtplib.SMTP()
        server.connect(self.server, port)
        if self.use_tls:
            server.starttls()
        server.login(self.username, self.password)
        server.sendmail(mail['From'], mail['To'], mail.as_string())
        self.imap.append('INBOX.Sent', '', imaplib.Time2Internaldate(time.time()), mail.as_bytes())
        server.quit()
