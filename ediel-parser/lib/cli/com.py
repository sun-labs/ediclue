import os
from lib.EDICommunicator import EDICommunicator
from lib.EDIParser import EDIParser
import lib.cli.tools as tools

com = None

def set_args(subparsers):
    parser = subparsers.add_parser('com', description='communication between EDI systems')
    parser.add_argument('action', choices=['send', 'get', 'set'])
    parser.add_argument('--send-to')
    parser.add_argument('--send-from')
    parser.add_argument('--from', dest='from_type', choices=['edi', 'mail'], default='edi', help='The input content type'),
    parser.add_argument('--username', default=os.environ.get('SL_COM_USERNAME'))
    parser.add_argument('--password', default=os.environ.get('SL_COM_PASSWORD'))
    parser.add_argument('--server', default=os.environ.get('SL_COM_SERVER'))
    parser.add_argument('--outgoing-server', default=os.environ.get('SL_COM_OUTGOING_SERVER'))
    parser.add_argument('--incoming-server', default=os.environ.get('SL_COM_INCOMING_SERVER'))
    parser.add_argument('--dry-run', action='store_true', help='Print mail without sending it')
    parser.add_argument('--dont-store', help='do not store sent email in sent folder')
    parser.add_argument('--verbose', action='store_true')

    parser.add_argument('--filter-label')
    parser.add_argument('--set-label', nargs='+')

    parser.add_argument('--input-dir')
    parser.add_argument('--output-dir')

def handle_send(payload, args):
    com = get_com(args)
    mail = None # result email
    if args.from_type == "edi":
        parser = EDIParser(payload, format=args.from_type)
        subject = parser['UNB'].toEdi()

        mail = com.create_edi_mail(
            send_from=args.send_from,
            send_to=args.send_to,
            subject=subject,
            file_content=payload
        )
    elif args.from_type == "mail":
        mail = com.mail_from_str(payload)
        
    if args.dry_run is False:
        com.send_mail(mail)

    return mail

def get_com(args):
    com = EDICommunicator()
    com.server = args.server
    com.username = args.username
    com.password = args.password
    com.init_imap()
    return com

def filter_dirs(path):
    return os.path.isfile(path)
def filter_blacklist(file):
    file = file.lower()
    return file not in ['.ds_store']

def vprint(args, *margs):
    if args.verbose is True:
        print(*margs)

def run(args):
    # dependencies on other arguments
    args.outgoing_server = args.server if args.outgoing_server is None else args.outgoing_server
    args.incoming_server = args.server if args.incoming_server is None else args.incoming_server
    args.send_from = args.username if args.send_from is None else args.send_from

    action = args.action
    com = get_com(args)

    if action == "send":
        mail = None
        if args.input_dir is not None:
            vprint(args,"Collecting files from {} with format {}".format(args.input_dir, args.from_type))
            files = tools.get_files(args.input_dir)
            for file_path in files:
                fh = open(file_path, 'r')
                content = fh.read()
                vprint(args,content)
                fh.close()
                mail = handle_send(content, args)
            get_filename = lambda f: (f.split('/')[-1]).split('.')[0]
            email_ids = list(map(get_filename, files))
            email_str = ' '.join(email_ids)
            if args.dry_run is False:
                print(email_str)
        else:
            payload = args.input.read()
            mail = handle_send(payload, args)
    elif action == "set":
        if args.set_label is not None:
            payload = args.input.read() # email ids as string
            resp = com.set_labels_email(email_ids, args.set_label)
            print(resp)
    elif action == "get":
        ids = com.get_mail_without_label(args.filter_label)
        files = []
        if args.output_dir is not None:
            filenames = os.listdir(args.output_dir)
            cleaned = map(lambda x: x.replace('.mail', ''), filenames)
            files = list(filter(lambda f: f.isdigit(), cleaned))
            vprint(args,"Storing {} mails in folder {}".format(len(ids), args.output_dir))
        ids_encoded = list(map(lambda i: i.decode('utf-8'), ids))
        print(ids_encoded)
        for mailid in ids_encoded:
            if mailid in files: 
                vprint(args,'skipping {}, already exists'.format(mailid))
                continue
            result = com.get_mail_with(mailid)
            result = result.decode('utf-8')
            file_name = '{}.mail'.format(mailid)
            file_path = os.path.join(args.output_dir, file_name)
            fh = open(file_path, 'w')
            vprint(args,result)
            fh.write(result)
            fh.close()
        downloaded_ids = filter(lambda i: i not in files, ids_encoded)
        downloaded_str = ' '.join(downloaded_ids)
        if downloaded_str != '':
            print(downloaded_str)
        # emails = com.get_email('UID SEARCH HEADER Message-ID <>')