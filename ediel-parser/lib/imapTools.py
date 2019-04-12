import imaplib
import email
import os

# Connect to an IMAP server
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select()
    return m

# Download all attachment files for a given email
def downloaAttachmentsInEmail(m, emailid, outputdir):
    emailid_dec = emailid.decode('utf-8')
    resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    email_body = data[0][1]
    mail = email.message_from_bytes(data[0][1])
    # print(mail.get_content_maintype())
    #if mail.get_content_maintype() != 'multipart':
        #return
    for i, part in enumerate(mail.walk()):
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            mail_from = mail.get('from')
            filename = "{}-{}-{}".format(emailid_dec, i, part.get_filename())
            dir_path = "{}/{}".format(outputdir, mail_from)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            file_path = "{}/{}".format(dir_path, filename)
            file = open(file_path, 'wb')
            file.write(part.get_payload(decode=True))

# Download all the attachment files for all emails in the inbox.
def downloadAllAttachmentsInInbox(m, outputdir, query="(ALL)"):
    resp, items = m.search(None, query)
    items = items[0].split()
    for emailid in items:
        downloaAttachmentsInEmail(m, emailid, outputdir)
