import os
from lib.EDICommunicator import EDICommunicator
from lib.EDIParser import EDIParser

com = None

def set_args(subparsers):
    parser = subparsers.add_parser('com', description='communication between EDI systems')
    parser.add_argument('action', choices=['send', 'get'])
    parser.add_argument('--send-to')
    parser.add_argument('--send-from')
    parser.add_argument('--from', dest='from_type', choices=['edi', 'mail'], default='edi', help='The input content type'),
    parser.add_argument('--username', default=os.environ.get('SL_COM_USERNAME'))
    parser.add_argument('--password', default=os.environ.get('SL_COM_PASSWORD'))
    parser.add_argument('--server', default=os.environ.get('SL_COM_SERVER'))
    parser.add_argument('--outgoing-server', default=os.environ.get('SL_COM_OUTGOING_SERVER'))
    parser.add_argument('--incoming-server', default=os.environ.get('SL_COM_INCOMING_SERVER'))
    parser.add_argument('--dry-run', action='store_true', help='Print mail without sending it')

    parser.add_argument('--filter-label')

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
        print(mail)

    if args.dry_run is False:
        #com.send_mail(mail)
        pass

    return mail

def get_com(args):
    com = EDICommunicator()
    com.server = args.server
    com.username = args.username
    com.password = args.password
    com.init_imap()
    return com


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
            print("Collecting files from {} with format {}".format(args.input_dir, args.from_type))
            files = os.listdir(args.input_dir)
            for file in files:
                file_path = os.path.join(args.input_dir, file)
                fh = open(file_path, 'r')
                content = fh.read()
                fh.close()
                mail = handle_send(content, args)
        else:
            payload = args.input.read()
            mail = handle_send(payload, args)
        print(mail)

    elif action == "get":
        ids = com.get_mail_without_label(args.filter_label)
        if args.output_dir is not None:
                print("Storing {} mails in folder {}".format(len(ids), args.output_dir))
        for mailid in ids:
            result = com.get_mail_with(mailid)
            file_name = '{}.mail'.format(mailid.decode('utf-8'))
            file_path = os.path.join(args.output_dir, file_name)
            fh = open(file_path, 'w')
            fh.write(result.decode('utf-8'))
            fh.close()
        # emails = com.get_email('UID SEARCH HEADER Message-ID <>')