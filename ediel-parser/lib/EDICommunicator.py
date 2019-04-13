import imaplib
import email
import os

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

    def send_mail(self, mail):
        pass